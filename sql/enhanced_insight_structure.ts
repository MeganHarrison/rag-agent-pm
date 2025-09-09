// Enhanced insight response structure for SQL generation
export interface EnhancedInsightResponse {
  businessIntelligence: {
    meetingId: string;
    projectId: number;
    executiveSummary: string;
    criticalPathItems: number;
    financialImpact: {
      budgetDiscussions: string[];
      costImplications: number | null;
      revenueImpact: number | null;
    };
    timelineConcerns: {
      delayRisks: string[];
      criticalDeadlines: Array<{
        task: string;
        deadline: string;
        impact: string;
      }>;
    };
  };
  
  insights: Array<{
    // Core insight data
    type: 'action_item' | 'decision' | 'risk' | 'timeline_change' | 'stakeholder_feedback' | 'financial_decision' | 'personnel_issue' | 'competitive_intel';
    title: string;
    description: string;
    confidenceScore: number;
    severity: 'critical' | 'high' | 'medium' | 'low';
    
    // Business context
    businessImpact: string;
    urgencyIndicators: string[];
    exactQuotes: string[];
    numericalData: Array<{
      type: 'budget' | 'timeline' | 'percentage' | 'cost';
      value: number;
      context: string;
    }>;
    
    // Stakeholder data
    assignedTo: string | null;
    stakeholdersAffected: string[];
    decisionMakers: string[];
    
    // Timeline data
    dueDate: string | null;
    criticalPathImpact: boolean;
    dependencies: string[];
    
    // SQL generation metadata
    sqlPriority: number; // For INSERT order
    meetingReferences: string[];
    crossProjectImpact: number[] | null; // Other project IDs affected
  }>;
}

// SQL generation template for enhanced insights
export const generateEnhancedInsightSQL = (insight: EnhancedInsightResponse['insights'][0], meetingId: string, projectId: number): string => {
  const description = formatBusinessDescription(insight);
  
  return `-- ${insight.type.toUpperCase()}: ${insight.title}
INSERT INTO ai_insights (
  meeting_id, 
  project_id, 
  insight_type, 
  title, 
  description, 
  confidence_score, 
  severity, 
  resolved, 
  source_meetings
) VALUES (
  '${meetingId}',
  ${projectId},
  '${insight.type}',
  '${insight.title.replace(/'/g, "''")}',
  '${description.replace(/'/g, "''")}',
  ${insight.confidenceScore},
  '${insight.severity}',
  0,
  '["${meetingId}"]'
);`;
};

// Format business-focused description
const formatBusinessDescription = (insight: EnhancedInsightResponse['insights'][0]): string => {
  let description = '';
  
  // Add business impact header
  if (insight.severity === 'critical') {
    description += '**CRITICAL BUSINESS IMPACT**: ';
  } else if (insight.severity === 'high') {
    description += '**HIGH PRIORITY**: ';
  }
  
  // Core description
  description += insight.description;
  
  // Add structured business context
  if (insight.assignedTo) {
    description += ` **Assignee**: ${insight.assignedTo}.`;
  }
  
  if (insight.dueDate) {
    description += ` **Due**: ${insight.dueDate}.`;
  }
  
  if (insight.dependencies.length > 0) {
    description += ` **Dependencies**: ${insight.dependencies.join(', ')}.`;
  }
  
  if (insight.businessImpact) {
    description += ` **Impact**: ${insight.businessImpact}`;
  }
  
  return description;
};