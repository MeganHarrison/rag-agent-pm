"""
Automated Insights Pipeline for RAG Agent PM

This module provides automated workflows for continuous project insight generation
and monitoring. It integrates with document ingestion, vectorization, and the
project insights service to maintain up-to-date project intelligence.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from .insights_generator import ProjectInsightsService, process_meeting_with_insights
from shared.utils.db_utils import db_pool, initialize_database

logger = logging.getLogger(__name__)


class InsightsPipeline:
    """
    Automated pipeline for continuous insight generation and monitoring.
    
    Features:
    - Automatic processing of new documents
    - Scheduled insight refresh
    - Project health monitoring
    - Alert generation for critical issues
    """
    
    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool
        self.insights_service = ProjectInsightsService(db_pool)
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        
    async def start(self):
        """Start the automated insights pipeline."""
        if self.is_running:
            logger.warning("Insights pipeline is already running")
            return
        
        logger.info("Starting Insights Pipeline...")
        
        # Schedule regular tasks
        self._schedule_tasks()
        
        # Start the scheduler
        self.scheduler.start()
        self.is_running = True
        
        # Run initial processing
        await self.process_pending_documents()
        await self.refresh_project_summaries()
        
        logger.info("Insights Pipeline started successfully")
    
    def _schedule_tasks(self):
        """Configure scheduled tasks for the pipeline."""
        
        # Process new documents every 5 minutes
        self.scheduler.add_job(
            self.process_pending_documents,
            IntervalTrigger(minutes=5),
            id='process_pending_documents',
            name='Process pending documents for insights',
            replace_existing=True
        )
        
        # Refresh project summaries every hour
        self.scheduler.add_job(
            self.refresh_project_summaries,
            IntervalTrigger(hours=1),
            id='refresh_project_summaries',
            name='Refresh project summaries',
            replace_existing=True
        )
        
        # Daily comprehensive analysis at 2 AM
        self.scheduler.add_job(
            self.daily_comprehensive_analysis,
            CronTrigger(hour=2, minute=0),
            id='daily_comprehensive_analysis',
            name='Daily comprehensive project analysis',
            replace_existing=True
        )
        
        # Weekly executive report generation (Mondays at 8 AM)
        self.scheduler.add_job(
            self.generate_weekly_executive_report,
            CronTrigger(day_of_week='mon', hour=8, minute=0),
            id='weekly_executive_report',
            name='Generate weekly executive report',
            replace_existing=True
        )
        
        # Critical issue monitoring every 15 minutes
        self.scheduler.add_job(
            self.monitor_critical_issues,
            IntervalTrigger(minutes=15),
            id='monitor_critical_issues',
            name='Monitor for critical project issues',
            replace_existing=True
        )
    
    async def process_pending_documents(self):
        """Process documents that haven't had insights extracted yet."""
        
        try:
            async with self.db_pool.acquire() as conn:
                # Find documents without insights
                pending_docs = await conn.fetch("""
                    SELECT d.id, d.title, d.content, d.metadata, d.project_id
                    FROM documents d
                    LEFT JOIN ai_insights ai ON d.id = ai.document_id
                    WHERE d.processing_status = 'completed'
                    AND d.document_type IN ('meeting', 'email')
                    AND ai.id IS NULL
                    AND d.created_at > NOW() - INTERVAL '7 days'
                    ORDER BY d.created_at DESC
                    LIMIT 10
                """)
                
                logger.info(f"Found {len(pending_docs)} documents pending insight extraction")
                
                for doc in pending_docs:
                    try:
                        # Process document with insights
                        result = await process_meeting_with_insights(
                            str(doc['id']),
                            self.db_pool
                        )
                        
                        logger.info(
                            f"Processed document {doc['id']}: "
                            f"{result['insights_extracted']} insights extracted"
                        )
                        
                        # Mark document as processed for insights
                        await conn.execute("""
                            UPDATE documents
                            SET metadata = COALESCE(metadata, '{}'::jsonb) || 
                                '{"insights_processed": true, "insights_processed_at": "%s"}'::jsonb
                            WHERE id = $1::uuid
                        """ % datetime.now().isoformat(), doc['id'])
                        
                    except Exception as e:
                        logger.error(f"Failed to process document {doc['id']}: {e}")
                        continue
                
        except Exception as e:
            logger.error(f"Error in process_pending_documents: {e}")
    
    async def refresh_project_summaries(self):
        """Refresh summaries for active projects with recent activity."""
        
        try:
            async with self.db_pool.acquire() as conn:
                # Find projects needing summary updates
                projects = await conn.fetch("""
                    SELECT * FROM get_projects_needing_summary_update(24)
                """)
                
                logger.info(f"Refreshing summaries for {len(projects)} projects")
                
                for project in projects:
                    try:
                        # Update project summary
                        await self.insights_service._update_project_summary(
                            project['project_id'],
                            conn
                        )
                        
                        logger.info(f"Updated summary for project {project['project_name']}")
                        
                    except Exception as e:
                        logger.error(
                            f"Failed to update summary for project {project['project_id']}: {e}"
                        )
                        continue
                
        except Exception as e:
            logger.error(f"Error in refresh_project_summaries: {e}")
    
    async def daily_comprehensive_analysis(self):
        """Run comprehensive daily analysis for all active projects."""
        
        logger.info("Starting daily comprehensive analysis")
        
        try:
            async with self.db_pool.acquire() as conn:
                # Get all active projects
                projects = await conn.fetch("""
                    SELECT id, name
                    FROM projects
                    WHERE current_phase NOT IN ('Completed', 'Cancelled', 'On Hold')
                    OR current_phase IS NULL
                """)
                
                analysis_results = []
                
                for project in projects:
                    try:
                        # Get comprehensive insights
                        summary = await self.insights_service.aggregate_project_insights(
                            project['id'],
                            days_back=30
                        )
                        
                        # Store analysis results
                        await conn.execute("""
                            UPDATE projects
                            SET metadata = COALESCE(metadata, '{}'::jsonb) || 
                                $2::jsonb
                            WHERE id = $1
                        """,
                            project['id'],
                            {
                                'daily_analysis': {
                                    'date': datetime.now().isoformat(),
                                    'health_score': summary['health_score'],
                                    'health_status': summary['health_status'],
                                    'key_metrics': {
                                        'open_action_items': len(summary['insights_summary']['action_items']['open']),
                                        'overdue_items': len(summary['insights_summary']['action_items']['overdue']),
                                        'active_risks': len(summary['insights_summary']['risks']),
                                        'blockers': len(summary['insights_summary']['blockers'])
                                    }
                                }
                            }
                        )
                        
                        analysis_results.append({
                            'project': project['name'],
                            'health_score': summary['health_score'],
                            'status': summary['health_status']
                        })
                        
                    except Exception as e:
                        logger.error(f"Failed daily analysis for project {project['id']}: {e}")
                        continue
                
                # Log summary of analysis
                critical_projects = [
                    r for r in analysis_results 
                    if r['status'] in ['Critical', 'Needs Attention']
                ]
                
                if critical_projects:
                    logger.warning(
                        f"Daily analysis complete: {len(critical_projects)} projects need attention: "
                        f"{', '.join([p['project'] for p in critical_projects])}"
                    )
                else:
                    logger.info(f"Daily analysis complete: All {len(projects)} projects healthy")
                
        except Exception as e:
            logger.error(f"Error in daily_comprehensive_analysis: {e}")
    
    async def monitor_critical_issues(self):
        """Monitor for critical issues requiring immediate attention."""
        
        try:
            async with self.db_pool.acquire() as conn:
                # Check for new critical issues
                critical_issues = await conn.fetch("""
                    SELECT 
                        ai.id,
                        ai.title,
                        ai.description,
                        ai.project_id,
                        p.name as project_name,
                        ai.assigned_to,
                        ai.created_at
                    FROM ai_insights ai
                    JOIN projects p ON ai.project_id = p.id
                    WHERE ai.severity = 'critical'
                    AND ai.status = 'open'
                    AND ai.created_at > NOW() - INTERVAL '15 minutes'
                    ORDER BY ai.created_at DESC
                """)
                
                if critical_issues:
                    logger.critical(
                        f"ALERT: {len(critical_issues)} new critical issues detected"
                    )
                    
                    for issue in critical_issues:
                        # Generate alert
                        alert = {
                            'type': 'critical_issue',
                            'project': issue['project_name'],
                            'title': issue['title'],
                            'description': issue['description'],
                            'assigned_to': issue['assigned_to'],
                            'timestamp': issue['created_at'].isoformat()
                        }
                        
                        # Store alert
                        await self._store_alert(alert, conn)
                        
                        # Here you could also send notifications
                        # e.g., email, Slack, webhook, etc.
                        logger.critical(
                            f"Critical issue in {issue['project_name']}: {issue['title']}"
                        )
                
                # Check for projects with declining health
                declining_projects = await conn.fetch("""
                    SELECT 
                        p.id,
                        p.name,
                        p.health_score,
                        p.health_status,
                        LAG(p.health_score) OVER (PARTITION BY p.id ORDER BY p.summary_updated_at) as prev_score
                    FROM projects p
                    WHERE p.health_score IS NOT NULL
                    AND p.summary_updated_at > NOW() - INTERVAL '2 hours'
                """)
                
                for project in declining_projects:
                    if project['prev_score'] and project['health_score']:
                        decline = project['prev_score'] - project['health_score']
                        if decline >= 20:  # Significant decline
                            logger.warning(
                                f"Project {project['name']} health declined by {decline:.1f} points "
                                f"to {project['health_score']:.1f} ({project['health_status']})"
                            )
                            
                            # Store health decline alert
                            await self._store_alert({
                                'type': 'health_decline',
                                'project': project['name'],
                                'current_score': project['health_score'],
                                'previous_score': project['prev_score'],
                                'decline': decline,
                                'status': project['health_status']
                            }, conn)
                
        except Exception as e:
            logger.error(f"Error in monitor_critical_issues: {e}")
    
    async def generate_weekly_executive_report(self):
        """Generate comprehensive weekly executive report."""
        
        logger.info("Generating weekly executive report")
        
        try:
            async with self.db_pool.acquire() as conn:
                # Get all projects with activity
                projects = await conn.fetch("""
                    SELECT 
                        p.id,
                        p.name,
                        p.health_score,
                        p.health_status,
                        p.summary,
                        p.completion_percentage,
                        p."est completion",
                        COUNT(DISTINCT d.id) as meetings_count,
                        COUNT(DISTINCT ai.id) as insights_count
                    FROM projects p
                    LEFT JOIN documents d ON p.id = d.project_id 
                        AND d.created_at > NOW() - INTERVAL '7 days'
                        AND d.document_type = 'meeting'
                    LEFT JOIN ai_insights ai ON p.id = ai.project_id
                        AND ai.created_at > NOW() - INTERVAL '7 days'
                    WHERE p.name IS NOT NULL
                    GROUP BY p.id
                    HAVING COUNT(DISTINCT d.id) > 0 OR COUNT(DISTINCT ai.id) > 0
                    ORDER BY p.health_score ASC NULLS LAST
                """)
                
                report = {
                    'report_date': datetime.now().isoformat(),
                    'week_ending': (datetime.now() + timedelta(days=(4 - datetime.now().weekday()))).date().isoformat(),
                    'total_projects': len(projects),
                    'projects_at_risk': sum(1 for p in projects if p['health_status'] in ['At Risk', 'Needs Attention', 'Critical']),
                    'projects_healthy': sum(1 for p in projects if p['health_status'] == 'Healthy'),
                    'total_meetings': sum(p['meetings_count'] for p in projects),
                    'total_insights': sum(p['insights_count'] for p in projects),
                    'project_details': []
                }
                
                # Add project details
                for project in projects[:10]:  # Top 10 projects by health
                    project_detail = {
                        'name': project['name'],
                        'health_score': project['health_score'],
                        'health_status': project['health_status'],
                        'completion': project['completion_percentage'],
                        'target_date': str(project['est completion']) if project['est completion'] else None,
                        'weekly_meetings': project['meetings_count'],
                        'weekly_insights': project['insights_count'],
                        'summary': project['summary']
                    }
                    
                    # Get top issues for this project
                    top_issues = await conn.fetch("""
                        SELECT title, severity, insight_type
                        FROM ai_insights
                        WHERE project_id = $1
                        AND status = 'open'
                        AND severity IN ('critical', 'high')
                        ORDER BY 
                            CASE severity 
                                WHEN 'critical' THEN 1 
                                WHEN 'high' THEN 2 
                                ELSE 3 
                            END,
                            created_at DESC
                        LIMIT 3
                    """, project['id'])
                    
                    project_detail['top_issues'] = [
                        {
                            'title': issue['title'],
                            'severity': issue['severity'],
                            'type': issue['insight_type']
                        }
                        for issue in top_issues
                    ]
                    
                    report['project_details'].append(project_detail)
                
                # Store the report
                await conn.execute("""
                    INSERT INTO executive_reports (
                        report_date,
                        report_type,
                        content,
                        created_at
                    ) VALUES ($1, $2, $3, NOW())
                """,
                    datetime.now(),
                    'weekly',
                    report
                )
                
                logger.info(
                    f"Weekly executive report generated: "
                    f"{report['total_projects']} projects, "
                    f"{report['projects_at_risk']} at risk"
                )
                
                # Return report for potential email/notification
                return report
                
        except Exception as e:
            logger.error(f"Error generating weekly executive report: {e}")
            return None
    
    async def _store_alert(self, alert: Dict[str, Any], conn: asyncpg.Connection):
        """Store an alert in the database."""
        
        try:
            await conn.execute("""
                INSERT INTO project_alerts (
                    alert_type,
                    severity,
                    title,
                    description,
                    metadata,
                    created_at
                ) VALUES ($1, $2, $3, $4, $5, NOW())
            """,
                alert.get('type', 'unknown'),
                'critical' if alert.get('type') == 'critical_issue' else 'warning',
                alert.get('title', f"{alert['type']} for {alert.get('project', 'Unknown')}"),
                alert.get('description', ''),
                alert
            )
        except Exception as e:
            logger.error(f"Failed to store alert: {e}")
    
    async def stop(self):
        """Stop the insights pipeline."""
        
        if not self.is_running:
            return
        
        logger.info("Stopping Insights Pipeline...")
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("Insights Pipeline stopped")


# Create required tables for the pipeline
CREATE_PIPELINE_TABLES = """
-- Executive reports table
CREATE TABLE IF NOT EXISTS executive_reports (
    id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    report_type TEXT CHECK (report_type IN ('daily', 'weekly', 'monthly')),
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Project alerts table
CREATE TABLE IF NOT EXISTS project_alerts (
    id SERIAL PRIMARY KEY,
    alert_type TEXT NOT NULL,
    severity TEXT CHECK (severity IN ('info', 'warning', 'critical')),
    title TEXT NOT NULL,
    description TEXT,
    metadata JSONB,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by TEXT,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_executive_reports_date ON executive_reports(report_date DESC);
CREATE INDEX IF NOT EXISTS idx_executive_reports_type ON executive_reports(report_type);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON project_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_acknowledged ON project_alerts(acknowledged);
CREATE INDEX IF NOT EXISTS idx_alerts_created ON project_alerts(created_at DESC);
"""


async def initialize_pipeline():
    """Initialize the insights pipeline with database setup."""
    
    await initialize_database()
    
    async with db_pool.acquire() as conn:
        # Create required tables
        await conn.execute(CREATE_PIPELINE_TABLES)
    
    # Create and start pipeline
    pipeline = InsightsPipeline(db_pool)
    await pipeline.start()
    
    return pipeline


if __name__ == "__main__":
    # Run pipeline as standalone service
    async def main():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        pipeline = await initialize_pipeline()
        
        try:
            # Keep running
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            logger.info("Shutting down pipeline...")
            await pipeline.stop()
    
    asyncio.run(main())