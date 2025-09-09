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
AS $function$
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
        OR p.summary_updated_at < NOW() - (hours_threshold || ' hours')::INTERVAL
    )
    ORDER BY p.summary_updated_at ASC NULLS FIRST;
END;
$function$;

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
AS $function$
BEGIN
    UPDATE projects
    SET 
        summary = p_summary,
        summary_metadata = COALESCE(summary_metadata, '{}'::jsonb) || p_metadata,
        summary_updated_at = NOW(),
        health_score = p_health_score,
        health_status = p_health_status
    WHERE id = p_project_id;
END;
$function$;

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
    CASE 
        WHEN p.budget IS NOT NULL AND p.budget > 0 AND p.budget_used IS NOT NULL 
        THEN (p.budget_used::numeric / p.budget::numeric * 100)
        ELSE 0 
    END as budget_utilization,
    p."est completion",
    -- Count recent insights
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.created_at::timestamp > (NOW() - INTERVAL '30 days')::timestamp) as recent_insights_count,
    -- Count open critical items
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.severity = 'critical' 
     AND ai.status = 'open') as open_critical_items,
    -- Count overdue items
    (SELECT COUNT(*) FROM ai_insights ai 
     WHERE ai.project_id = p.id 
     AND ai.due_date IS NOT NULL
     AND ai.due_date::timestamp < NOW()::timestamp 
     AND ai.status = 'open') as overdue_items,
    -- Latest meeting date (using created_at as fallback)
    (SELECT MAX(COALESCE(d.created_at::date, d.created_at::date)) FROM documents d 
     WHERE d.project_id = p.id 
     AND (d.document_type = 'meeting' OR d.title LIKE '%Meeting%' OR d.title LIKE '%meeting%')) as last_meeting_date
FROM projects p
WHERE p.name IS NOT NULL
ORDER BY p.health_score ASC NULLS LAST;