-- Update ai_insights table to match our enhanced schema

-- Add missing columns if they don't exist
ALTER TABLE ai_insights 
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'completed', 'cancelled'));

ALTER TABLE ai_insights 
ADD COLUMN IF NOT EXISTS assigned_to TEXT;

ALTER TABLE ai_insights 
ADD COLUMN IF NOT EXISTS due_date DATE;

ALTER TABLE ai_insights 
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

ALTER TABLE ai_insights 
ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP WITH TIME ZONE;

-- Update severity column to use consistent values
UPDATE ai_insights 
SET severity = CASE 
    WHEN severity IN ('Critical', 'CRITICAL') THEN 'critical'
    WHEN severity IN ('High', 'HIGH') THEN 'high'
    WHEN severity IN ('Medium', 'MEDIUM') THEN 'medium'
    WHEN severity IN ('Low', 'LOW') THEN 'low'
    ELSE 'medium'
END
WHERE severity IS NOT NULL;

-- Add constraint for severity values
ALTER TABLE ai_insights 
DROP CONSTRAINT IF EXISTS ai_insights_severity_check;

ALTER TABLE ai_insights 
ADD CONSTRAINT ai_insights_severity_check 
CHECK (severity IN ('low', 'medium', 'high', 'critical'));

-- Update insight_type to use consistent values
UPDATE ai_insights 
SET insight_type = CASE 
    WHEN insight_type IN ('Action Item', 'ACTION_ITEM') THEN 'action_item'
    WHEN insight_type IN ('Decision', 'DECISION') THEN 'decision'
    WHEN insight_type IN ('Risk', 'RISK') THEN 'risk'
    WHEN insight_type IN ('Milestone', 'MILESTONE') THEN 'milestone'
    WHEN insight_type IN ('Blocker', 'BLOCKER') THEN 'blocker'
    ELSE 'fact'
END
WHERE insight_type IS NOT NULL;

-- Add constraint for insight_type values
ALTER TABLE ai_insights 
DROP CONSTRAINT IF EXISTS ai_insights_insight_type_check;

ALTER TABLE ai_insights 
ADD CONSTRAINT ai_insights_insight_type_check 
CHECK (insight_type IN ('action_item', 'decision', 'risk', 'milestone', 'fact', 'blocker', 'dependency', 'budget_update', 'timeline_change', 'stakeholder_feedback', 'technical_debt'));

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_ai_insights_status ON ai_insights(status);
CREATE INDEX IF NOT EXISTS idx_ai_insights_assigned_to ON ai_insights(assigned_to) WHERE assigned_to IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_ai_insights_due_date ON ai_insights(due_date) WHERE due_date IS NOT NULL;