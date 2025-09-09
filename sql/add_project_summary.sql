-- Add project summary columns to projects table
-- This stores AI-generated summaries and health metrics

-- Add summary column if it doesn't exist
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS summary TEXT;

-- Add summary metadata column for structured summary data
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS summary_metadata JSONB DEFAULT '{}';

-- Add last summary update timestamp
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS summary_updated_at TIMESTAMP WITH TIME ZONE;

-- Add project health score (0-100)
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS health_score NUMERIC(5,2);

-- Add health status enum
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS health_status TEXT 
    CHECK (health_status IN ('Healthy', 'At Risk', 'Needs Attention', 'Critical'));

-- Create index on health score for quick filtering
CREATE INDEX IF NOT EXISTS idx_projects_health_score ON projects(health_score DESC);

-- Create index on summary update for tracking freshness
CREATE INDEX IF NOT EXISTS idx_projects_summary_updated ON projects(summary_updated_at DESC);

-- Function to get projects needing summary updates
CREATE OR REPLACE FUNCTION get_projects_needing_summary_update(
    hours_threshold INTEGER DEFAULT 24
)
RETURNS TABLE (
    project_id INTEGER,
    project_name TEXT,
    last_update TIMESTAMP WITH TIME ZONE,
    hours_since_update NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id as project_id,
        p.name as project_name,
        p.summary_updated_at as last_update,
        EXTRACT(EPOCH FROM (NOW() - COALESCE(p.summary_updated_at, '2000-01-01'::timestamp with time zone))) / 3600 as hours_since_update
    FROM projects p
    WHERE EXISTS (
        -- Has recent documents
        SELECT 1 FROM documents d 
        WHERE d.project_id = p.id 
        AND d.created_at > NOW() - INTERVAL '7 days'
    )
    AND (
        p.summary_updated_at IS NULL 
        OR p.summary_updated_at < NOW() - INTERVAL '1 hour' * hours_threshold
    )
    ORDER BY p.summary_updated_at ASC NULLS FIRST;
END;
$$;

-- Function to update project summary
CREATE OR REPLACE FUNCTION update_project_summary(
    p_project_id INTEGER,
    p_summary TEXT,
    p_health_score NUMERIC,
    p_health_status TEXT,
    p_metadata JSONB
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE projects
    SET 
        summary = p_summary,
        summary_metadata = COALESCE(summary_metadata, '{}'::jsonb) || p_metadata,
        summary_updated_at = NOW(),
        health_score = p_health_score,
        health_status = p_health_status,
        updated_at = NOW()
    WHERE id = p_project_id;
END;
$$;

-- View for project health dashboard
CREATE OR REPLACE VIEW project_health_dashboard AS
SELECT 
    p.id,
    p.name,
    p.current_phase,
    p.completion_percentage,
    p.health_score,
    p.health_status,
    p.summary,
    p.summary_updated_at,
    COALESCE(p.budget_used::numeric / NULLIF(p.budget::numeric, 0) * 100, 0) as budget_utilization,
    p."est completion",
    -- Count recent insights
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.created_at > NOW() - INTERVAL '30 days') as recent_insights_count,
    -- Count open critical items
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.severity = 'critical' 
     AND ai.status = 'open') as open_critical_items,
    -- Count overdue items
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.due_date < NOW() 
     AND ai.status = 'open') as overdue_items,
    -- Latest meeting date
    (SELECT MAX(d.meeting_date) FROM documents d 
     WHERE d.project_id = p.id 
     AND d.document_type = 'meeting') as last_meeting_date
FROM projects p
WHERE p.name IS NOT NULL
ORDER BY p.health_score ASC NULLS LAST;