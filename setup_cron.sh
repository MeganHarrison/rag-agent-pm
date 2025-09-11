#!/bin/bash

# Setup script for automated insights generation cron jobs
# This script sets up periodic execution of the insights generator

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Setting up automated insights generation..."

# Create log directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Create the cron wrapper script
cat > "$SCRIPT_DIR/cron_insights.sh" << 'EOF'
#!/bin/bash
# Cron wrapper for insights generation

# Load environment variables
export $(cat /Users/meganharrison/Documents/github/alleato-project/alleato-ai-dashboard/alleato-rag-agents/rag-agent-pm/.env | xargs)

# Change to script directory
cd /Users/meganharrison/Documents/github/alleato-project/alleato-ai-dashboard/alleato-rag-agents/rag-agent-pm

# Run the batch processing
/usr/bin/python3 auto_insights_generator.py --mode batch >> logs/insights_cron.log 2>&1

# Keep only last 7 days of logs
find logs/ -name "*.log" -mtime +7 -delete
EOF

chmod +x "$SCRIPT_DIR/cron_insights.sh"

echo ""
echo "To set up automated processing, add one of these lines to your crontab:"
echo "(Run 'crontab -e' to edit your crontab)"
echo ""
echo "# Run every hour (recommended for active projects):"
echo "0 * * * * $SCRIPT_DIR/cron_insights.sh"
echo ""
echo "# Run every 4 hours:"
echo "0 */4 * * * $SCRIPT_DIR/cron_insights.sh"
echo ""
echo "# Run twice daily (9 AM and 5 PM):"
echo "0 9,17 * * * $SCRIPT_DIR/cron_insights.sh"
echo ""
echo "# Run once daily at 2 AM:"
echo "0 2 * * * $SCRIPT_DIR/cron_insights.sh"
echo ""
echo "Test the script manually first:"
echo "$SCRIPT_DIR/cron_insights.sh"