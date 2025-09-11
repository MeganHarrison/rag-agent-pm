# Unified Insights Generation System

## Overview

The `generate_insights_unified.py` script is the consolidated solution for generating project insights from documents. It combines the best features from multiple previous approaches into a single, robust system.

## Features

- **Dual Processing Modes**: 
  - Rule-based extraction (fast, deterministic)
  - AI-powered extraction (sophisticated, context-aware)
- **Document Processing**:
  - Processes all documents associated with a project
  - Extracts insights from document content
- **Correct Database Constraints**:
  - Validates all insight types against DB constraints
  - Handles all required fields properly
- **Comprehensive Error Handling**:
  - Continues processing on individual errors
  - Provides detailed error reporting

## Usage

```bash
# Basic usage (rule-based extraction)
python3 generate_insights_unified.py <project_id>

# AI-powered extraction
python3 generate_insights_unified.py <project_id> --use-ai

# Examples
python3 generate_insights_unified.py 43          # Westfield Collective
python3 generate_insights_unified.py 59          # Tampa Event/Party
python3 generate_insights_unified.py 59 --use-ai # Tampa with AI extraction
```

## Valid Database Values

The script ensures all data conforms to database constraints:

### Insight Types
- `fact` - General information, summaries, or observations
- `decision` - Decisions made or approvals granted
- `action_item` - Tasks to be completed
- `risk` - Potential risks or concerns
- `stakeholder_feedback` - Feedback from stakeholders
- `timeline_change` - Changes to project timeline

### Severity Levels
- `critical` - Immediate attention required
- `high` - Important, time-sensitive
- `medium` - Standard priority (default)
- `low` - Informational, non-urgent

### Required Fields
- `title` - Must always be provided
- `description` - Must always be provided

## Generated Insights Examples

For **Westfield Collective** (Project ID: 43):
- 13 decisions documented
- 8 action items identified
- 3 strategic facts recorded
- Total: 24 insights from 29 documents

For **Tampa Event/Party** (Project ID: 59):
- 14 action items created
- 8 decisions recorded
- 8 risks identified
- 1 strategic summary
- Total: 31 insights from 4 documents

## Archived Scripts

The following scripts have been archived in `.archive/old_insights_scripts/`:
- `process_tampa_insights.py` - Original Tampa-specific script
- `generate_project_insights.py` - Earlier general version
- `test_insights.py` - Testing script
- `test_insights_simple.py` - Simple database verification

## Services Directory

The `services/` directory contains the sophisticated AI-powered extraction logic:
- `project_insights_service.py` - Core service class with AI extraction
- `insights_pipeline.py` - Pipeline orchestration

These services are imported and used by the unified script when `--use-ai` flag is provided.

## Database Connection

The script uses the DATABASE_URL environment variable or falls back to the configured connection string. Ensure your `.env` file contains:

```
DATABASE_URL=postgresql://[connection_string]
```

## Future Improvements

1. **Enhanced AI Extraction**: Integrate more sophisticated NLP models
2. **Batch Processing**: Process multiple projects in one run
3. **Incremental Updates**: Only process new documents since last run
4. **Custom Rules**: Allow project-specific extraction rules
5. **Export Capabilities**: Export insights to various formats (CSV, JSON, etc.)

## Troubleshooting

If you encounter database constraint violations:
1. Check that insight_type is one of the valid values
2. Ensure severity is one of: critical, high, medium, low
3. Verify title and description are not empty
4. Check date formats are proper Python date objects

For connection issues:
1. Verify DATABASE_URL is set correctly
2. Check network connectivity to Supabase
3. Ensure database credentials are valid