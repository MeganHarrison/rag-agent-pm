-- Database trigger for automatic insights generation
-- This creates a PostgreSQL trigger that calls a webhook when new documents are added

-- First, create a function to notify about new documents
CREATE OR REPLACE FUNCTION notify_new_document()
RETURNS TRIGGER AS $$
BEGIN
  -- Only trigger for documents with substantial content
  IF NEW.content IS NOT NULL AND LENGTH(NEW.content) > 100 THEN
    -- Insert a notification record (or call pg_notify)
    PERFORM pg_notify(
      'new_document',
      json_build_object(
        'document_id', NEW.id,
        'project_id', NEW.project_id,
        'title', NEW.title,
        'created_at', NEW.created_at
      )::text
    );
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger on the documents table
DROP TRIGGER IF EXISTS trigger_new_document ON documents;
CREATE TRIGGER trigger_new_document
  AFTER INSERT ON documents
  FOR EACH ROW
  EXECUTE FUNCTION notify_new_document();

-- Alternative: Create a queue table for processing
CREATE TABLE IF NOT EXISTS insights_generation_queue (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  document_id UUID NOT NULL REFERENCES documents(id),
  project_id INTEGER NOT NULL REFERENCES projects(id),
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
  attempts INTEGER DEFAULT 0,
  error_message TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  processed_at TIMESTAMP WITH TIME ZONE,
  CONSTRAINT unique_document_queue UNIQUE (document_id)
);

-- Function to add documents to processing queue
CREATE OR REPLACE FUNCTION queue_document_for_insights()
RETURNS TRIGGER AS $$
BEGIN
  -- Only queue documents with substantial content
  IF NEW.content IS NOT NULL AND LENGTH(NEW.content) > 100 THEN
    INSERT INTO insights_generation_queue (document_id, project_id)
    VALUES (NEW.id, NEW.project_id)
    ON CONFLICT (document_id) DO NOTHING;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for queue-based processing
DROP TRIGGER IF EXISTS trigger_queue_document ON documents;
CREATE TRIGGER trigger_queue_document
  AFTER INSERT ON documents
  FOR EACH ROW
  EXECUTE FUNCTION queue_document_for_insights();

-- Function to get next document from queue for processing
CREATE OR REPLACE FUNCTION get_next_queued_document()
RETURNS TABLE (
  queue_id UUID,
  document_id UUID,
  project_id INTEGER
) AS $$
BEGIN
  RETURN QUERY
  UPDATE insights_generation_queue
  SET 
    status = 'processing',
    attempts = attempts + 1,
    processed_at = NOW()
  WHERE id = (
    SELECT id 
    FROM insights_generation_queue
    WHERE status IN ('pending', 'failed')
      AND attempts < 3
    ORDER BY created_at
    LIMIT 1
    FOR UPDATE SKIP LOCKED
  )
  RETURNING id, document_id, project_id;
END;
$$ LANGUAGE plpgsql;

-- Function to mark queue item as completed
CREATE OR REPLACE FUNCTION complete_queued_document(
  p_queue_id UUID,
  p_success BOOLEAN DEFAULT TRUE,
  p_error_message TEXT DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
  UPDATE insights_generation_queue
  SET 
    status = CASE WHEN p_success THEN 'completed' ELSE 'failed' END,
    error_message = p_error_message,
    processed_at = NOW()
  WHERE id = p_queue_id;
END;
$$ LANGUAGE plpgsql;

-- View to monitor queue status
CREATE OR REPLACE VIEW insights_queue_status AS
SELECT 
  q.status,
  COUNT(*) as count,
  MIN(q.created_at) as oldest,
  MAX(q.created_at) as newest,
  AVG(EXTRACT(EPOCH FROM (q.processed_at - q.created_at))) as avg_processing_time_seconds
FROM insights_generation_queue q
GROUP BY q.status;

-- View to see pending documents by project
CREATE OR REPLACE VIEW pending_insights_by_project AS
SELECT 
  p.id as project_id,
  p.name as project_name,
  COUNT(DISTINCT d.id) as pending_documents,
  MIN(d.created_at) as oldest_document
FROM documents d
JOIN projects p ON p.id = d.project_id
LEFT JOIN ai_insights ai ON ai.document_id = d.id::text
WHERE d.content IS NOT NULL
  AND LENGTH(d.content) > 100
  AND ai.id IS NULL
GROUP BY p.id, p.name
ORDER BY pending_documents DESC;