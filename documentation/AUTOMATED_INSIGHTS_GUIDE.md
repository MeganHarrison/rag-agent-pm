# Automated AI Insights Generation System

## Overview

This system automatically generates AI-powered insights from project documents using OpenAI GPT-3.5-turbo. It extracts specific, actionable insights including action items, decisions, risks, and key facts - all with concrete details like names, dates, and amounts.

## Components

### 1. Core Scripts

#### `auto_insights_generator.py`
The main automation script with multiple processing modes:

```bash
# Process all unprocessed documents (batch mode)
python3 auto_insights_generator.py --mode batch

# Process a specific document
python3 auto_insights_generator.py --mode document --document-id 123

# Process new documents for a specific project
python3 auto_insights_generator.py --mode project --project-id 43
```

#### `generate_ai_insights.py`
Manual script for generating insights for a specific project:

```bash
python3 generate_ai_insights.py <project_id>
```

### 2. API Endpoint

#### `/api/generate-insights`

REST API endpoint for on-demand insights generation:

```javascript
// Process a single document
POST /api/generate-insights
{
  "mode": "document",
  "documentId": "abc-123"
}

// Process all unprocessed documents for a project
POST /api/generate-insights
{
  "mode": "project",
  "projectId": "43"
}

// Process all unprocessed documents globally (admin)
POST /api/generate-insights
{
  "mode": "batch"
}

// Check insights statistics
GET /api/generate-insights
```

### 3. Database Components

#### Triggers
- `trigger_new_document` - Notifies when new documents are added
- `trigger_queue_document` - Adds new documents to processing queue

#### Queue Table
- `insights_generation_queue` - Tracks documents pending insights generation

#### Helper Functions
- `get_next_queued_document()` - Retrieves next document for processing
- `complete_queued_document()` - Marks document as processed

#### Monitoring Views
- `insights_queue_status` - Overview of queue status
- `pending_insights_by_project` - Shows pending documents by project

## Automation Options

### Option 1: Cron Job (Scheduled Processing)

Set up automatic processing every hour/day:

```bash
# Make the setup script executable
chmod +x setup_cron.sh

# Run the setup script
./setup_cron.sh

# Add to crontab (choose one):
crontab -e

# Every hour
0 * * * * /path/to/cron_insights.sh

# Twice daily (9 AM and 5 PM)
0 9,17 * * * /path/to/cron_insights.sh

# Once daily at 2 AM
0 2 * * * /path/to/cron_insights.sh
```

### Option 2: Database Trigger (Real-time Processing)

Apply the database trigger to process documents immediately:

```sql
-- Apply the trigger SQL
psql $DATABASE_URL < database_trigger.sql
```

Then run a worker process to handle the queue:

```python
# Create a worker script that polls the queue
while True:
    # Get next document from queue
    # Process with auto_insights_generator.py
    # Mark as complete
    # Sleep for 30 seconds
```

### Option 3: Webhook Integration (Event-driven)

Call the API endpoint when documents are created:

```javascript
// In your document creation logic
async function createDocument(data) {
  // Save document to database
  const doc = await saveDocument(data);
  
  // Trigger insights generation
  await fetch('/api/generate-insights', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mode: 'document',
      documentId: doc.id
    })
  });
}
```

### Option 4: UI Button (Manual Trigger)

Add a button to the project page to generate insights on-demand:

```tsx
// In your React component
const generateInsights = async () => {
  const response = await fetch('/api/generate-insights', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mode: 'project',
      projectId: project.id
    })
  });
  
  const result = await response.json();
  console.log(`Generated ${result.insightsGenerated} insights`);
};

<button onClick={generateInsights}>
  Generate AI Insights
</button>
```

## Configuration

### Environment Variables

Required in `.env`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
DATABASE_URL=postgresql://connection_string

# Supabase Configuration (for API endpoint)
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key
```

### Processing Limits

Adjust these in the scripts as needed:

- **Batch size**: 50 documents per run (prevents timeouts)
- **Content length**: 8000 characters max per document (API token limits)
- **Retry attempts**: 3 attempts for failed documents
- **Processing interval**: Configurable via cron schedule

## Monitoring

### Check Queue Status

```sql
-- View queue status
SELECT * FROM insights_queue_status;

-- View pending documents by project
SELECT * FROM pending_insights_by_project;

-- Check recent insights
SELECT 
  p.name as project,
  COUNT(*) as insight_count,
  MAX(ai.created_at) as latest_insight
FROM ai_insights ai
JOIN projects p ON p.id = ai.project_id
WHERE ai.created_at > NOW() - INTERVAL '24 hours'
GROUP BY p.name
ORDER BY insight_count DESC;
```

### Check Logs

```bash
# View automation logs
tail -f insights_generation.log

# View cron logs
tail -f logs/insights_cron.log
```

## Insight Quality

The system generates high-quality insights with:

- **Specific names**: "Jeff", "Maria", "Nick Awoodhams"
- **Exact dates**: "March 27", "April 3", "2025-08-23"
- **Concrete actions**: "create elevation CAD files", "set up entity structure"
- **Financial details**: "$20,000 budget", "$500K construction estimate"
- **Clear ownership**: Assignee field populated when mentioned
- **Risk assessment**: Severity levels (critical/high/medium/low)

## Troubleshooting

### No insights generated?

1. Check document has content > 100 characters
2. Verify OpenAI API key is valid
3. Check for duplicate insights (system prevents duplicates)
4. Review logs for API errors

### Insights seem generic?

- The prompt specifically requests concrete details
- GPT-3.5-turbo is instructed to skip generic insights
- Documents with little specific information will yield fewer insights

### Processing too slow?

- Reduce batch size in `auto_insights_generator.py`
- Run multiple workers in parallel
- Consider upgrading to GPT-4 for better quality (but slower)

### Database errors?

- Ensure all required fields are provided
- Check insight_type is valid: 'action_item', 'decision', 'risk', 'fact'
- Verify severity is valid: 'critical', 'high', 'medium', 'low'

## Best Practices

1. **Start with manual testing**: Run `generate_ai_insights.py` on a test project first
2. **Monitor costs**: Each document costs ~$0.002-0.005 in OpenAI API fees
3. **Set reasonable schedules**: Hourly for active projects, daily for others
4. **Review quality regularly**: Check that insights remain actionable
5. **Clean up old insights**: Archive completed insights periodically

## Future Enhancements

Potential improvements to consider:

1. **Incremental processing**: Only process documents added since last run
2. **Priority queue**: Process high-priority projects first
3. **Custom prompts**: Project-specific insight extraction rules
4. **Notification system**: Alert PMs when critical insights are found
5. **Insight clustering**: Group related insights automatically
6. **GPT-4 upgrade**: Better quality but higher cost
7. **Parallel processing**: Process multiple documents simultaneously
8. **Caching**: Avoid reprocessing unchanged documents

## Support

For issues or questions:
1. Check the logs in `insights_generation.log`
2. Verify environment variables are set correctly
3. Test with a single document first
4. Review the database constraints in the schema