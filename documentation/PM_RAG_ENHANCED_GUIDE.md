# PM RAG Agent - Elite Business Intelligence System

## Overview

The PM RAG Agent has been completely enhanced to serve as Alleato's **ultimate business strategist and project management partner**. This is NOT just a project management tool - it's a comprehensive business intelligence system with deep knowledge of:

- **All Projects**: Complete history, documents, meetings, decisions
- **Business Strategy**: Market positioning, competitive landscape, growth opportunities
- **Financial Intelligence**: Budgets, ROI analysis, cost optimization
- **Risk Management**: Proactive identification, mitigation strategies
- **Stakeholder Relations**: Client management, team coordination

## Key Distinction from FM Global Agent

**CRITICAL**: This PM RAG Agent is completely separate from the FM Global agent:
- **PM RAG Agent** (this system): Elite business strategy and comprehensive project intelligence
- **FM Global Agent** (separate repo): Focused solely on FM Global PDFs for lead generation

## Architecture Overview

```
alleato-rag-agents/rag-agent-pm/
├── core/                       # Core system components
│   ├── agent.py               # Main agent with enhanced prompts
│   └── prompts.py             # Elite business strategy prompts
├── intelligence/              # Advanced AI capabilities
│   ├── query_processor.py    # Intent classification & entity extraction
│   ├── search_strategies.py  # HyDE, multi-query fusion, context-aware
│   └── context_manager.py    # Conversation memory & business context
├── tools/                     # Search and retrieval tools
│   └── search_tools.py        # Semantic and hybrid search
├── api/                       # API endpoints
│   └── app.py                # FastAPI server
└── documentation/             # System documentation
```

## Enhanced Capabilities

### 1. Elite System Prompts

The agent now operates with comprehensive business intelligence prompts:

```python
ENHANCED_PM_SYSTEM_PROMPT = """
You are an elite Business Strategy and Project Management AI Partner...
- 20+ years expertise in construction/engineering
- Deep understanding of Alleato's business model
- Domain mastery in ASRS systems, MEP coordination
- Financial acumen for ROI analysis and forecasting
"""
```

### 2. Query Intent Classification

Automatically classifies queries to provide targeted responses:

- **STATUS_UPDATE**: Project progress, milestones, completion
- **RISK_ASSESSMENT**: Risk identification, mitigation strategies
- **BUDGET_TRACKING**: Financial analysis, cost optimization
- **STRATEGIC_ANALYSIS**: Business opportunities, competitive positioning
- **STAKEHOLDER_QUERY**: Client concerns, team performance
- **TECHNICAL_DETAIL**: Specifications, compliance requirements

### 3. Advanced Search Strategies

#### HyDE (Hypothetical Document Embeddings)
Generates hypothetical answers to improve semantic search:
```python
# Bridges vocabulary gap between questions and documents
hypothetical = hyde_generator.generate_hypothetical_document(query, intent)
```

#### Multi-Query Fusion
Creates query variations for comprehensive coverage:
```python
# Generates multiple perspectives on the same query
variations = multi_query.generate_query_variations(query, intent)
# Fuses results using Reciprocal Rank Fusion (RRF)
```

#### Context-Aware Retrieval
Enhances queries with conversation and business context:
```python
# Adds temporal, business, and conversation context
enhanced_query = context_retrieval.enhance_with_context(query, history)
```

### 4. Conversation Memory Management

Three-tier memory system:
- **Short-term**: Current conversation with compression
- **Working**: Session-level context and preferences
- **Episodic**: Project-specific memories and patterns

### 5. Business Context Integration

Maintains comprehensive business awareness:
- Current project focus and phase
- Strategic initiatives and priorities
- Temporal alerts (deadlines, overdue items)
- Stakeholder relationships

## Usage Examples

### Basic Query
```python
from agent import search_agent
from dependencies import AgentDependencies

deps = AgentDependencies(api_key="...", session_id="...")
result = await search_agent.run(
    "What's the status of the Tampa project?",
    deps=deps
)
```

### Strategic Analysis
```python
# Automatic intent detection triggers strategic search
result = await search_agent.run(
    "Analyze competitive advantages in ASRS market",
    deps=deps
)
# Uses HyDE strategy for deep strategic insights
```

### Project Intelligence
```python
# Comprehensive project analysis
result = await search_agent.run(
    "Give me complete analysis of Westfield Collective risks and opportunities",
    deps=deps
)
# Multi-query fusion for comprehensive coverage
```

## API Integration

### Streaming Endpoint
```bash
POST /chat/stream
{
    "message": "What are our strategic priorities?",
    "conversation_history": [...],
    "session_id": "uuid"
}
```

### Non-Streaming Endpoint
```bash
POST /chat
{
    "message": "Project status update",
    "conversation_history": [...],
    "session_id": "uuid"
}
```

## Search Strategy Selection

The system automatically selects optimal search strategies:

| Query Intent | Strategy | Reason |
|-------------|----------|---------|
| Strategic Analysis | HyDE | Generates strategic document hypotheses |
| Budget Tracking | Multi-Query | Multiple financial perspectives |
| Status Updates | Hybrid | Combines keyword and semantic |
| Risk Assessment | HyDE | Creates risk scenario documents |
| Stakeholder | Context-Aware | Uses conversation history |

## Performance Optimizations

1. **Token Management**: Automatic conversation compression at 4000 tokens
2. **Result Fusion**: RRF algorithm for multi-query result ranking
3. **Context Caching**: Session-level context persistence
4. **Parallel Search**: Concurrent execution of multiple search strategies

## Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://...
SUPABASE_SERVICE_KEY=...

# Optional
LLM_MODEL=gpt-4-turbo-preview
DEFAULT_MATCH_COUNT=10
MAX_MATCH_COUNT=20
DEFAULT_TEXT_WEIGHT=0.3
```

### Dynamic Context Settings
```python
# Customize per session
deps.business_context = {
    'current_quarter': 'Q3 2024',
    'strategic_focus': ['ASRS expansion', 'MEP integration'],
    'priority_clients': ['Amazon', 'Walmart']
}
```

## Testing the Enhanced System

### 1. Test Query Processing
```python
# Test different intent types
test_queries = [
    "Project 43 status and timeline",  # STATUS_UPDATE
    "Risks in Tampa warehouse project",  # RISK_ASSESSMENT
    "ROI analysis for ASRS investments",  # BUDGET_TRACKING
    "Competitive positioning vs XYZ Corp",  # STRATEGIC_ANALYSIS
]
```

### 2. Test Search Strategies
```python
# Force specific strategies
result = await advanced_search(
    ctx, 
    query="market opportunities",
    strategy="hyde",  # or "multi_query", "hybrid"
    match_count=15
)
```

### 3. Test Context Memory
```python
# Add conversation history
context_manager.conversation.add_exchange(
    "What's our budget?",
    "Current budget is $5M",
    {"topic": "financial", "project_id": "43"}
)
# Future queries will use this context
```

## Deployment

### Local Development
```bash
cd alleato-rag-agents/rag-agent-pm
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Production (Render)
```bash
./deploy_to_render.sh
```

## Monitoring & Analytics

The system tracks:
- Query intent distribution
- Search strategy effectiveness
- Response times by strategy
- User preference learning
- Session interaction patterns

## Future Enhancements

1. **Predictive Analytics**: Forecast project risks and opportunities
2. **Automated Insights**: Proactive alerts on important changes
3. **Multi-Agent Orchestration**: Coordinate with other specialized agents
4. **Real-time Collaboration**: Live updates across team members
5. **Advanced Visualizations**: Interactive dashboards and reports

## Support

For issues or questions about the PM RAG Agent:
- Review this documentation
- Check the logs in `/logs` directory
- Contact the Alleato AI Team

---

**Remember**: This is your elite business intelligence partner, not just a search tool. It should provide strategic insights, identify opportunities, and serve as institutional memory for Alleato's competitive advantage.