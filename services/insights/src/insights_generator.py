"""
Project Insights Service for RAG Agent PM

This service provides intelligent project matching and AI-driven insights extraction
from meeting transcripts and documents. It automatically identifies relevant projects,
extracts actionable insights, and maintains a comprehensive knowledge graph of
project-related information.
"""

import os
import re
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncpg
from dotenv import load_dotenv

from shared.ai.providers import get_llm_model
from shared.utils.db_utils import db_pool

load_dotenv()
logger = logging.getLogger(__name__)


class InsightType(Enum):
    """Types of insights that can be extracted."""
    ACTION_ITEM = "action_item"
    DECISION = "decision"
    RISK = "risk"
    MILESTONE = "milestone"
    BLOCKER = "blocker"
    DEPENDENCY = "dependency"
    BUDGET_UPDATE = "budget_update"
    TIMELINE_CHANGE = "timeline_change"
    STAKEHOLDER_FEEDBACK = "stakeholder_feedback"
    TECHNICAL_DEBT = "technical_debt"


class InsightPriority(Enum):
    """Priority levels for insights."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ProjectInsight:
    """Structured representation of a project insight."""
    insight_type: InsightType
    title: str
    description: str
    project_id: Optional[int]
    confidence_score: float
    priority: InsightPriority
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    source_document_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    related_insights: List[str] = None


class ProjectInsightsService:
    """Service for extracting and managing project insights from documents."""
    
    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool
        self.llm_model = get_llm_model()
        
    async def match_document_to_project(
        self,
        document_id: str,
        title: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> Optional[int]:
        """
        Intelligently match a document (meeting transcript) to a project.
        
        Uses multiple strategies:
        1. Direct project name/ID mentions in title or content
        2. Participant matching to project team members
        3. Keyword and context matching
        4. Historical pattern recognition
        """
        
        async with self.db_pool.acquire() as conn:
            # Strategy 1: Direct project name/number mentions
            projects = await conn.fetch("""
                SELECT id, name, aliases, keywords, team_members, 
                       "job number", client_id
                FROM projects
                WHERE name IS NOT NULL
            """)
            
            # Build project matching patterns
            project_scores = {}
            
            for project in projects:
                score = 0
                project_id = project['id']
                
                # Check project name in title/content
                if project['name']:
                    name_pattern = re.compile(
                        r'\b' + re.escape(project['name']) + r'\b',
                        re.IGNORECASE
                    )
                    if name_pattern.search(title):
                        score += 10  # High weight for title match
                    if name_pattern.search(content[:2000]):  # Check first 2000 chars
                        score += 5
                
                # Check aliases
                if project['aliases']:
                    for alias in project['aliases']:
                        if alias and alias.lower() in title.lower():
                            score += 8
                        if alias and alias.lower() in content[:2000].lower():
                            score += 3
                
                # Check job number
                if project['job number']:
                    if project['job number'] in title or project['job number'] in content[:1000]:
                        score += 15  # Very high confidence
                
                # Check team members in participants
                if project['team_members'] and metadata.get('participants'):
                    participants = metadata.get('participants', [])
                    team_matches = sum(
                        1 for member in project['team_members']
                        if any(member.lower() in p.lower() for p in participants)
                    )
                    score += team_matches * 3
                
                # Check keywords
                if project['keywords']:
                    keyword_matches = sum(
                        1 for keyword in project['keywords']
                        if keyword.lower() in content.lower()
                    )
                    score += min(keyword_matches * 2, 10)  # Cap at 10
                
                if score > 0:
                    project_scores[project_id] = score
            
            # If no strong match, use LLM for intelligent matching
            if not project_scores or max(project_scores.values()) < 10:
                project_id = await self._llm_match_project(
                    title, content[:3000], metadata, projects
                )
                if project_id:
                    return project_id
            
            # Return highest scoring project if above threshold
            if project_scores:
                best_match = max(project_scores, key=project_scores.get)
                if project_scores[best_match] >= 8:
                    logger.info(
                        f"Matched document {document_id} to project {best_match} "
                        f"with score {project_scores[best_match]}"
                    )
                    return best_match
            
            return None
    
    async def _llm_match_project(
        self,
        title: str,
        content_snippet: str,
        metadata: Dict[str, Any],
        projects: List[asyncpg.Record]
    ) -> Optional[int]:
        """Use LLM to intelligently match document to project."""
        
        # Prepare project list for LLM
        project_list = []
        for p in projects[:20]:  # Limit to top 20 projects
            project_list.append({
                'id': p['id'],
                'name': p['name'],
                'keywords': p['keywords'] or [],
                'team': p['team_members'] or []
            })
        
        prompt = f"""Analyze this meeting transcript and match it to the most relevant project.

Meeting Title: {title}
Participants: {metadata.get('participants', [])}
Date: {metadata.get('meeting_date', 'Unknown')}

Content Preview:
{content_snippet}

Available Projects:
{json.dumps(project_list, indent=2)}

Return ONLY the project ID number as an integer, or 0 if no match.
Consider: project names mentioned, participants who are team members, 
keywords, and context clues."""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            response = await agent.run(prompt)
            result = response.data
            project_id = int(result.strip())
            return project_id if project_id > 0 else None
        except (ValueError, AttributeError) as e:
            logger.warning(f"LLM project matching failed: {e}")
            return None
    
    async def extract_insights(
        self,
        document_id: str,
        project_id: Optional[int] = None
    ) -> List[ProjectInsight]:
        """
        Extract comprehensive insights from a document.
        
        Uses multi-pass extraction strategy:
        1. Action items and assignments
        2. Decisions and approvals
        3. Risks and blockers
        4. Timeline and budget impacts
        5. Cross-functional dependencies
        """
        
        async with self.db_pool.acquire() as conn:
            # Get document content
            doc = await conn.fetchrow("""
                SELECT id, title, content, document_type, project_id,
                       metadata, meeting_date
                FROM documents
                WHERE id = $1::uuid
            """, document_id)
            
            if not doc:
                raise ValueError(f"Document {document_id} not found")
            
            # Use provided project_id or document's project_id
            project_id = project_id or doc['project_id']
            
            insights = []
            
            # Extract different types of insights
            insights.extend(await self._extract_action_items(doc, project_id))
            insights.extend(await self._extract_decisions(doc, project_id))
            insights.extend(await self._extract_risks_and_blockers(doc, project_id))
            insights.extend(await self._extract_timeline_updates(doc, project_id))
            insights.extend(await self._extract_stakeholder_feedback(doc, project_id))
            
            # Store insights in database
            await self._store_insights(insights, document_id, conn)
            
            # Trigger project-level aggregation
            if project_id:
                await self._update_project_summary(project_id, conn)
            
            return insights
    
    async def _extract_action_items(
        self,
        doc: asyncpg.Record,
        project_id: Optional[int]
    ) -> List[ProjectInsight]:
        """Extract action items with assignments and due dates."""
        
        prompt = f"""Extract ALL action items from this meeting transcript.

Title: {doc['title']}
Date: {doc['meeting_date']}
Content: {doc['content'][:4000]}

For each action item, identify:
1. Task description
2. Assigned person (if mentioned)
3. Due date or timeline (if mentioned)
4. Priority (critical/high/medium/low based on context)
5. Dependencies on other tasks

Return as JSON array with structure:
[{{
  "task": "description",
  "assignee": "name or null",
  "due_date": "YYYY-MM-DD or null",
  "priority": "high/medium/low",
  "dependencies": []
}}]

Include tasks mentioned as:
- Action items, to-dos, next steps
- "We need to...", "Someone should...", "Let's..."
- Commitments made by participants
"""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            response = await agent.run(prompt)
            result = response.data
            items = json.loads(response)
            
            insights = []
            for item in items:
                # Calculate due date if relative time given
                due_date = self._parse_due_date(
                    item.get('due_date'),
                    doc['meeting_date']
                )
                
                insights.append(ProjectInsight(
                    insight_type=InsightType.ACTION_ITEM,
                    title=item['task'][:200],  # Limit title length
                    description=item['task'],
                    project_id=project_id,
                    confidence_score=0.9,
                    priority=InsightPriority[item.get('priority', 'medium').upper()],
                    assigned_to=item.get('assignee'),
                    due_date=due_date,
                    source_document_id=str(doc['id']),
                    metadata={
                        'dependencies': item.get('dependencies', []),
                        'meeting_date': str(doc['meeting_date'])
                    }
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract action items: {e}")
            return []
    
    async def _extract_decisions(
        self,
        doc: asyncpg.Record,
        project_id: Optional[int]
    ) -> List[ProjectInsight]:
        """Extract key decisions and approvals."""
        
        prompt = f"""Extract key decisions from this meeting.

Content: {doc['content'][:4000]}

Identify decisions about:
- Budget approvals or changes
- Timeline adjustments
- Scope changes
- Technical choices
- Vendor selections
- Process changes

Return as JSON array:
[{{
  "decision": "what was decided",
  "rationale": "why",
  "impact": "consequences",
  "approver": "who approved"
}}]"""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            response = await agent.run(prompt)
            result = response.data
            decisions = json.loads(response)
            
            insights = []
            for decision in decisions:
                # Determine priority based on impact
                priority = self._assess_decision_priority(decision.get('impact', ''))
                
                insights.append(ProjectInsight(
                    insight_type=InsightType.DECISION,
                    title=decision['decision'][:200],
                    description=f"{decision['decision']}\n\nRationale: {decision.get('rationale', 'Not specified')}\n\nImpact: {decision.get('impact', 'Not specified')}",
                    project_id=project_id,
                    confidence_score=0.85,
                    priority=priority,
                    assigned_to=decision.get('approver'),
                    source_document_id=str(doc['id']),
                    metadata={
                        'meeting_date': str(doc['meeting_date']),
                        'impact_area': self._categorize_impact(decision.get('impact', ''))
                    }
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract decisions: {e}")
            return []
    
    async def _extract_risks_and_blockers(
        self,
        doc: asyncpg.Record,
        project_id: Optional[int]
    ) -> List[ProjectInsight]:
        """Extract risks, blockers, and concerns."""
        
        prompt = f"""Identify risks, blockers, and concerns from this meeting.

Content: {doc['content'][:4000]}

Look for:
- Explicit risks or concerns mentioned
- Blockers preventing progress
- Dependencies causing delays
- Resource constraints
- Technical challenges
- Compliance/regulatory issues

Return as JSON array:
[{{
  "type": "risk|blocker",
  "title": "brief description",
  "description": "detailed explanation",
  "severity": "critical|high|medium|low",
  "mitigation": "proposed solution if any"
}}]"""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            response = await agent.run(prompt)
            result = response.data
            items = json.loads(response)
            
            insights = []
            for item in items:
                insight_type = (
                    InsightType.BLOCKER if item['type'] == 'blocker'
                    else InsightType.RISK
                )
                
                insights.append(ProjectInsight(
                    insight_type=insight_type,
                    title=item['title'],
                    description=f"{item['description']}\n\nMitigation: {item.get('mitigation', 'None proposed')}",
                    project_id=project_id,
                    confidence_score=0.8,
                    priority=InsightPriority[item['severity'].upper()],
                    source_document_id=str(doc['id']),
                    metadata={
                        'meeting_date': str(doc['meeting_date']),
                        'has_mitigation': bool(item.get('mitigation'))
                    }
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract risks/blockers: {e}")
            return []
    
    async def _extract_timeline_updates(
        self,
        doc: asyncpg.Record,
        project_id: Optional[int]
    ) -> List[ProjectInsight]:
        """Extract timeline and milestone updates."""
        
        prompt = f"""Extract timeline and milestone information.

Content: {doc['content'][:4000]}

Look for:
- Deadline changes
- Milestone completions or delays
- Schedule updates
- Phase transitions
- Delivery dates

Return as JSON array:
[{{
  "type": "milestone|timeline_change",
  "description": "what changed",
  "original_date": "YYYY-MM-DD or null",
  "new_date": "YYYY-MM-DD or null",
  "impact": "consequence of change"
}}]"""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            response = await agent.run(prompt)
            result = response.data
            items = json.loads(response)
            
            insights = []
            for item in items:
                insight_type = (
                    InsightType.MILESTONE if item['type'] == 'milestone'
                    else InsightType.TIMELINE_CHANGE
                )
                
                # Assess priority based on impact
                priority = self._assess_timeline_priority(
                    item.get('original_date'),
                    item.get('new_date'),
                    item.get('impact')
                )
                
                insights.append(ProjectInsight(
                    insight_type=insight_type,
                    title=item['description'][:200],
                    description=self._format_timeline_description(item),
                    project_id=project_id,
                    confidence_score=0.85,
                    priority=priority,
                    due_date=self._parse_due_date(item.get('new_date'), None),
                    source_document_id=str(doc['id']),
                    metadata={
                        'original_date': item.get('original_date'),
                        'new_date': item.get('new_date'),
                        'impact': item.get('impact')
                    }
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract timeline updates: {e}")
            return []
    
    async def _extract_stakeholder_feedback(
        self,
        doc: asyncpg.Record,
        project_id: Optional[int]
    ) -> List[ProjectInsight]:
        """Extract stakeholder feedback and client requirements."""
        
        prompt = f"""Extract stakeholder feedback and requirements.

Content: {doc['content'][:3000]}

Look for:
- Client feedback or requests
- Stakeholder concerns
- Change requests
- Satisfaction indicators
- New requirements

Return as JSON array:
[{{
  "stakeholder": "name/role",
  "feedback_type": "positive|negative|neutral|request",
  "content": "what was said",
  "action_required": true/false
}}]"""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            response = await agent.run(prompt)
            result = response.data
            items = json.loads(response)
            
            insights = []
            for item in items:
                # Determine priority based on feedback type and action required
                priority = InsightPriority.HIGH if (
                    item.get('action_required') or 
                    item.get('feedback_type') == 'negative'
                ) else InsightPriority.MEDIUM
                
                insights.append(ProjectInsight(
                    insight_type=InsightType.STAKEHOLDER_FEEDBACK,
                    title=f"Feedback from {item['stakeholder']}: {item['content'][:150]}",
                    description=item['content'],
                    project_id=project_id,
                    confidence_score=0.9,
                    priority=priority,
                    source_document_id=str(doc['id']),
                    metadata={
                        'stakeholder': item['stakeholder'],
                        'feedback_type': item['feedback_type'],
                        'action_required': item.get('action_required', False)
                    }
                ))
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract stakeholder feedback: {e}")
            return []
    
    async def _store_insights(
        self,
        insights: List[ProjectInsight],
        document_id: str,
        conn: asyncpg.Connection
    ) -> None:
        """Store insights in the database."""
        
        for insight in insights:
            await conn.execute("""
                INSERT INTO ai_insights (
                    document_id, project_id, insight_type,
                    title, description, confidence_score,
                    severity, assigned_to, due_date,
                    metadata, created_at
                ) VALUES ($1::uuid, $2, $3, $4, $5, $6, $7, $8, $9, $10, NOW())
            """,
                document_id,
                insight.project_id,
                insight.insight_type.value,
                insight.title,
                insight.description,
                insight.confidence_score,
                insight.priority.value,
                insight.assigned_to,
                insight.due_date,
                json.dumps(insight.metadata or {})
            )
    
    async def _update_project_summary(
        self,
        project_id: int,
        conn: asyncpg.Connection
    ) -> None:
        """Update project-level summary based on insights."""
        
        # Get project details
        project = await conn.fetchrow("""
            SELECT name, current_phase, completion_percentage,
                   "est completion", budget, budget_used, summary
            FROM projects
            WHERE id = $1
        """, project_id)
        
        if not project:
            return
        
        # Get recent insights for project
        recent_insights = await conn.fetch("""
            SELECT insight_type, severity, status, due_date, title, description
            FROM ai_insights
            WHERE project_id = $1
            AND created_at > NOW() - INTERVAL '30 days'
            ORDER BY created_at DESC
        """, project_id)
        
        # Calculate project health metrics
        open_critical = sum(
            1 for i in recent_insights
            if i['severity'] == 'critical' and i['status'] == 'open'
        )
        
        overdue_items = sum(
            1 for i in recent_insights
            if i['due_date'] and i['due_date'] < datetime.now() and i['status'] == 'open'
        )
        
        # Calculate health score
        health_score = 100.0
        health_score -= min(overdue_items * 5, 25)
        health_score -= min(open_critical * 10, 30)
        
        # Check budget utilization
        budget_utilization = None
        if project['budget'] and project['budget_used']:
            budget_utilization = float(project['budget_used']) / float(project['budget']) * 100
            if budget_utilization > 100:
                health_score -= min((budget_utilization - 100) * 2, 20)
        
        health_score = max(0, min(100, health_score))
        health_status = self._get_health_status(health_score)
        
        # Generate or update project summary if needed
        if not project['summary'] or len(recent_insights) > 0:
            summary = await self._generate_project_summary(
                project_id, project, recent_insights, conn
            )
        else:
            summary = project['summary']
        
        # Prepare metadata
        summary_metadata = {
            'health_metrics': {
                'open_critical_items': open_critical,
                'overdue_items': overdue_items,
                'total_recent_insights': len(recent_insights),
                'budget_utilization': budget_utilization
            },
            'recent_activity': {
                'action_items': sum(1 for i in recent_insights if i['insight_type'] == 'action_item'),
                'decisions': sum(1 for i in recent_insights if i['insight_type'] == 'decision'),
                'risks': sum(1 for i in recent_insights if i['insight_type'] == 'risk'),
                'blockers': sum(1 for i in recent_insights if i['insight_type'] == 'blocker')
            }
        }
        
        # Update project with summary and health metrics
        await conn.execute("""
            UPDATE projects
            SET 
                summary = $2,
                summary_metadata = COALESCE(summary_metadata, '{}'::jsonb) || $3::jsonb,
                summary_updated_at = NOW(),
                health_score = $4,
                health_status = $5,
                metadata = COALESCE(metadata, '{}'::jsonb) || $6::jsonb
            WHERE id = $1
        """,
            project_id,
            summary,
            json.dumps(summary_metadata),
            health_score,
            health_status,
            json.dumps({
                'last_insight_update': datetime.now().isoformat()
            })
        )
    
    async def _generate_project_summary(
        self,
        project_id: int,
        project: asyncpg.Record,
        recent_insights: List[asyncpg.Record],
        conn: asyncpg.Connection
    ) -> str:
        """Generate an AI-powered project summary."""
        
        # Get recent meeting titles for context
        recent_meetings = await conn.fetch("""
            SELECT title, meeting_date
            FROM documents
            WHERE project_id = $1
            AND document_type = 'meeting'
            ORDER BY meeting_date DESC
            LIMIT 5
        """, project_id)
        
        # Prepare insights summary
        action_items = [i for i in recent_insights if i['insight_type'] == 'action_item' and i['status'] == 'open']
        risks = [i for i in recent_insights if i['insight_type'] == 'risk']
        blockers = [i for i in recent_insights if i['insight_type'] == 'blocker']
        decisions = [i for i in recent_insights if i['insight_type'] == 'decision'][:3]
        
        prompt = f"""Generate a concise executive summary for this project.

Project: {project['name']}
Current Phase: {project['current_phase']}
Completion: {project['completion_percentage']}%
Target Completion: {project['est completion']}

Recent Meetings:
{chr(10).join([f"- {m['title']} ({m['meeting_date']})" for m in recent_meetings])}

Open Action Items ({len(action_items)}):
{chr(10).join([f"- {a['title']}" for a in action_items[:5]])}

Active Risks ({len(risks)}):
{chr(10).join([f"- {r['title']} (Severity: {r['severity']})" for r in risks[:3]])}

Blockers ({len(blockers)}):
{chr(10).join([f"- {b['title']}" for b in blockers[:3]])}

Recent Decisions:
{chr(10).join([f"- {d['title']}" for d in decisions])}

Write a 3-4 sentence executive summary that:
1. States the current project status and progress
2. Highlights the most critical issues or risks
3. Notes key recent decisions or achievements
4. Provides a forward-looking statement about next steps

Be concise and focus on what executives need to know."""

        try:
            from pydantic_ai import Agent
            agent = Agent(self.llm_model)
            summary_response = await agent.run(prompt)
            summary = summary_response.data
            return summary.strip()
        except Exception as e:
            logger.error(f"Failed to generate project summary: {e}")
            # Fallback to template-based summary
            return self._generate_fallback_summary(
                project, action_items, risks, blockers, decisions
            )
    
    def _generate_fallback_summary(
        self,
        project: asyncpg.Record,
        action_items: List[asyncpg.Record],
        risks: List[asyncpg.Record],
        blockers: List[asyncpg.Record],
        decisions: List[asyncpg.Record]
    ) -> str:
        """Generate a fallback summary if LLM fails."""
        
        summary_parts = []
        
        # Status
        summary_parts.append(
            f"{project['name']} is currently in {project['current_phase'] or 'active'} phase "
            f"with {project['completion_percentage'] or 0}% completion."
        )
        
        # Issues
        issues = []
        if blockers:
            issues.append(f"{len(blockers)} blocker(s)")
        if risks:
            high_risks = sum(1 for r in risks if r['severity'] in ['critical', 'high'])
            if high_risks:
                issues.append(f"{high_risks} high-priority risk(s)")
        
        if issues:
            summary_parts.append(f"The project faces {' and '.join(issues)} requiring attention.")
        
        # Action items
        if action_items:
            summary_parts.append(f"There are {len(action_items)} open action items to be completed.")
        
        # Decisions
        if decisions:
            summary_parts.append(f"Recent decisions have been made regarding project direction.")
        
        return " ".join(summary_parts)
    
    async def aggregate_project_insights(
        self,
        project_id: int,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Aggregate insights for a project to provide executive summary.
        
        Returns comprehensive project status including:
        - Open action items by priority
        - Recent decisions
        - Active risks and blockers
        - Timeline status
        - Stakeholder sentiment
        """
        
        async with self.db_pool.acquire() as conn:
            # Get project details
            project = await conn.fetchrow("""
                SELECT name, current_phase, completion_percentage,
                       "est completion", budget, budget_used
                FROM projects
                WHERE id = $1
            """, project_id)
            
            if not project:
                raise ValueError(f"Project {project_id} not found")
            
            # Get insights by type
            insights = await conn.fetch("""
                SELECT insight_type, severity, status, title, 
                       description, assigned_to, due_date, created_at
                FROM ai_insights
                WHERE project_id = $1
                AND created_at > NOW() - INTERVAL '%s days'
                ORDER BY severity DESC, created_at DESC
            """ % days_back, project_id)
            
            # Organize insights
            summary = {
                'project_name': project['name'],
                'current_phase': project['current_phase'],
                'completion_percentage': project['completion_percentage'],
                'estimated_completion': str(project['est completion']) if project['est completion'] else None,
                'budget_utilization': (
                    float(project['budget_used']) / float(project['budget']) * 100
                    if project['budget'] and project['budget_used'] else None
                ),
                'insights_summary': {
                    'total_insights': len(insights),
                    'action_items': {
                        'open': [],
                        'completed': [],
                        'overdue': []
                    },
                    'risks': [],
                    'blockers': [],
                    'recent_decisions': [],
                    'milestones': [],
                    'stakeholder_feedback': []
                }
            }
            
            # Categorize insights
            for insight in insights:
                insight_dict = {
                    'title': insight['title'],
                    'severity': insight['severity'],
                    'assigned_to': insight['assigned_to'],
                    'due_date': str(insight['due_date']) if insight['due_date'] else None,
                    'created_at': str(insight['created_at'])
                }
                
                if insight['insight_type'] == 'action_item':
                    if insight['status'] == 'completed':
                        summary['insights_summary']['action_items']['completed'].append(insight_dict)
                    elif insight['due_date'] and insight['due_date'] < datetime.now():
                        summary['insights_summary']['action_items']['overdue'].append(insight_dict)
                    else:
                        summary['insights_summary']['action_items']['open'].append(insight_dict)
                
                elif insight['insight_type'] == 'risk':
                    summary['insights_summary']['risks'].append(insight_dict)
                
                elif insight['insight_type'] == 'blocker':
                    summary['insights_summary']['blockers'].append(insight_dict)
                
                elif insight['insight_type'] == 'decision':
                    summary['insights_summary']['recent_decisions'].append(insight_dict)
                
                elif insight['insight_type'] == 'milestone':
                    summary['insights_summary']['milestones'].append(insight_dict)
                
                elif insight['insight_type'] == 'stakeholder_feedback':
                    summary['insights_summary']['stakeholder_feedback'].append(insight_dict)
            
            # Calculate health score
            health_score = self._calculate_project_health(summary)
            summary['health_score'] = health_score
            summary['health_status'] = self._get_health_status(health_score)
            
            return summary
    
    def _parse_due_date(
        self,
        date_str: Optional[str],
        reference_date: Optional[datetime]
    ) -> Optional[datetime]:
        """Parse due date from various formats."""
        if not date_str:
            return None
        
        # Handle relative dates
        if 'next week' in date_str.lower():
            base = reference_date or datetime.now()
            return base + timedelta(days=7)
        elif 'tomorrow' in date_str.lower():
            base = reference_date or datetime.now()
            return base + timedelta(days=1)
        elif 'end of month' in date_str.lower():
            base = reference_date or datetime.now()
            # Calculate last day of month
            if base.month == 12:
                return datetime(base.year + 1, 1, 1) - timedelta(days=1)
            else:
                return datetime(base.year, base.month + 1, 1) - timedelta(days=1)
        
        # Try parsing ISO format
        try:
            return datetime.fromisoformat(date_str)
        except:
            return None
    
    def _assess_decision_priority(self, impact: str) -> InsightPriority:
        """Assess priority based on decision impact."""
        impact_lower = impact.lower()
        
        if any(word in impact_lower for word in ['critical', 'major', 'significant', 'budget', 'deadline']):
            return InsightPriority.HIGH
        elif any(word in impact_lower for word in ['moderate', 'some', 'partial']):
            return InsightPriority.MEDIUM
        else:
            return InsightPriority.LOW
    
    def _categorize_impact(self, impact: str) -> str:
        """Categorize the area of impact."""
        impact_lower = impact.lower()
        
        if 'budget' in impact_lower or 'cost' in impact_lower:
            return 'budget'
        elif 'schedule' in impact_lower or 'timeline' in impact_lower or 'deadline' in impact_lower:
            return 'timeline'
        elif 'scope' in impact_lower or 'requirement' in impact_lower:
            return 'scope'
        elif 'quality' in impact_lower or 'technical' in impact_lower:
            return 'technical'
        else:
            return 'general'
    
    def _assess_timeline_priority(
        self,
        original_date: Optional[str],
        new_date: Optional[str],
        impact: Optional[str]
    ) -> InsightPriority:
        """Assess priority of timeline changes."""
        # If delay is mentioned or dates pushed back
        if original_date and new_date:
            try:
                orig = datetime.fromisoformat(original_date)
                new = datetime.fromisoformat(new_date)
                delay_days = (new - orig).days
                
                if delay_days > 30:
                    return InsightPriority.CRITICAL
                elif delay_days > 7:
                    return InsightPriority.HIGH
                elif delay_days > 0:
                    return InsightPriority.MEDIUM
            except:
                pass
        
        # Check impact description
        if impact and any(word in impact.lower() for word in ['critical', 'blocking', 'major']):
            return InsightPriority.HIGH
        
        return InsightPriority.MEDIUM
    
    def _format_timeline_description(self, item: Dict[str, Any]) -> str:
        """Format timeline change description."""
        desc = item['description']
        
        if item.get('original_date') and item.get('new_date'):
            desc += f"\n\nSchedule change: {item['original_date']} → {item['new_date']}"
        
        if item.get('impact'):
            desc += f"\n\nImpact: {item['impact']}"
        
        return desc
    
    def _calculate_project_health(self, summary: Dict[str, Any]) -> float:
        """Calculate overall project health score (0-100)."""
        score = 100.0
        
        insights = summary['insights_summary']
        
        # Deduct for overdue items
        overdue_count = len(insights['action_items']['overdue'])
        score -= min(overdue_count * 5, 25)
        
        # Deduct for blockers
        blocker_count = len(insights['blockers'])
        score -= min(blocker_count * 10, 30)
        
        # Deduct for high-priority risks
        high_risks = sum(1 for r in insights['risks'] if r['severity'] in ['critical', 'high'])
        score -= min(high_risks * 7, 20)
        
        # Deduct for budget overrun
        if summary.get('budget_utilization'):
            if summary['budget_utilization'] > 100:
                score -= min((summary['budget_utilization'] - 100) * 2, 20)
        
        # Bonus for completed items
        completed_count = len(insights['action_items']['completed'])
        open_count = len(insights['action_items']['open'])
        if open_count + completed_count > 0:
            completion_rate = completed_count / (open_count + completed_count)
            score += min(completion_rate * 10, 10)
        
        return max(0, min(100, score))
    
    def _get_health_status(self, score: float) -> str:
        """Get health status label from score."""
        if score >= 80:
            return "Healthy"
        elif score >= 60:
            return "At Risk"
        elif score >= 40:
            return "Needs Attention"
        else:
            return "Critical"


async def process_meeting_with_insights(
    document_id: str,
    db_pool: asyncpg.Pool
) -> Dict[str, Any]:
    """
    Complete pipeline for processing a meeting transcript with insights.
    
    This is the main entry point for the insight extraction pipeline.
    """
    
    service = ProjectInsightsService(db_pool)
    
    async with db_pool.acquire() as conn:
        # Get document details
        doc = await conn.fetchrow("""
            SELECT id, title, content, metadata
            FROM documents
            WHERE id = $1::uuid
        """, document_id)
        
        if not doc:
            raise ValueError(f"Document {document_id} not found")
        
        # Step 1: Match to project if not already matched
        if not doc.get('project_id'):
            project_id = await service.match_document_to_project(
                document_id,
                doc['title'],
                doc['content'],
                doc['metadata'] or {}
            )
            
            if project_id:
                # Update document with project_id
                await conn.execute("""
                    UPDATE documents
                    SET project_id = $1, updated_at = NOW()
                    WHERE id = $2::uuid
                """, project_id, document_id)
                
                logger.info(f"Matched document {document_id} to project {project_id}")
        else:
            project_id = doc['project_id']
        
        # Step 2: Extract insights
        insights = await service.extract_insights(document_id, project_id)
        
        # Step 3: Get project summary if matched
        project_summary = None
        if project_id:
            project_summary = await service.aggregate_project_insights(project_id)
        
        return {
            'document_id': document_id,
            'project_id': project_id,
            'insights_extracted': len(insights),
            'insight_types': [i.insight_type.value for i in insights],
            'project_summary': project_summary
        }