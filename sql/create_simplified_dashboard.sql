-- Simplified project health dashboard that works with existing schema

-- First, ensure we have the functions
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
AS $function$
BEGIN
    RETURN QUERY
    SELECT 
        p.id as project_id,
        p.name as project_name,
        p.summary_updated_at as last_update,
        EXTRACT(EPOCH FROM (NOW() - COALESCE(p.summary_updated_at, '2000-01-01'::timestamp with time zone))) / 3600 as hours_since_update
    FROM projects p
    WHERE p.name IS NOT NULL
    AND (
        p.summary_updated_at IS NULL 
        OR p.summary_updated_at < NOW() - (hours_threshold || ' hours')::INTERVAL
    )
    ORDER BY p.summary_updated_at ASC NULLS FIRST;
END;
$function$;

-- Create simplified view
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
    CASE 
        WHEN p.budget IS NOT NULL AND p.budget > 0 AND p.budget_used IS NOT NULL 
        THEN (p.budget_used::numeric / p.budget::numeric * 100)
        ELSE 0 
    END as budget_utilization,
    p."est completion",
    -- Count recent insights
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id) as total_insights_count,
    -- Count open items (using resolved field instead of status)
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.severity = 'critical' 
     AND (ai.resolved = 0 OR ai.resolved IS NULL)) as open_critical_items,
    -- Count recent documents
    (SELECT COUNT(*) FROM documents d 
     WHERE d.project_id = p.id 
     AND d.created_at > NOW() - INTERVAL '30 days') as recent_documents_count,
    -- Latest document date
    (SELECT MAX(d.created_at::date) FROM documents d 
     WHERE d.project_id = p.id) as last_document_date
FROM projects p
WHERE p.name IS NOT NULL
ORDER BY 
    CASE 
        WHEN p.health_score IS NULL THEN 999
        ELSE p.health_score
    END ASC;