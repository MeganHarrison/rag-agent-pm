# Paradise Project Meeting - AI Insights for Supabase

## Table Structure for `ai_insights`

| id | meeting_id | project_id | insight_type | title | description | confidence_score | severity | resolved | source_meetings | created_at |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | action_item | Order Paradise Project geotechnical study | **CRITICAL PATH**: $40,000 geotechnical study must be ordered immediately. Drilling scheduled for September 15, results expected September 29. **Assignee**: Brandon Clymer. **Dependencies**: Results critical for project progression and landowner negotiations. | 0.95 | critical | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 2 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | action_item | Get permission for Paradise Project update | Email Minot & Vikram for permission to contact Bill regarding Paradise Project status update. **Assignee**: Phil. **Due**: Before Sept 29 results. Required for stakeholder communication. | 0.90 | high | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 3 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | decision | Four-partner cost-sharing agreement | **FINANCIAL DECISION**: Partners agreed to split $40,000 geotechnical study costs equally. **Rationale**: Strengthen negotiating position with landowner through unified financial commitment. **Impact**: Budget allocation and risk distribution across partnership. | 0.92 | high | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 4 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | decision | Private equity backup funding strategy | **STRATEGIC PIVOT**: Private equity being considered as backup financing if traditional Paradise funding fails. **Impact**: Alternative funding pathway to maintain project viability. Indicates potential concerns about primary funding route. | 0.85 | medium | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 5 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | risk | Paul's performance impacting relationships | **PERSONNEL RISK**: Paul's reliability issues are damaging business relationships. **Impact**: Team excluded Paul from Ryder Cup networking, Phil limiting Michael Bazinski contact. **Severity**: Ongoing relationship management problem affecting strategic partnerships. | 0.88 | high | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 6 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 43 | risk | Emerald Coast Marina funding challenges | **PROJECT FUNDING RISK**: Emerald Coast Marina Project doesn't meet standard funding criteria. **Impact**: Exploring non-traditional funding sources. **Risk**: Project viability threatened without alternative financing. | 0.82 | medium | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 7 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | timeline_change | Critical geotechnical study timeline | **TIMELINE CONSTRAINT**: Sept 15 drilling start, Sept 29 results deadline. **Risk**: Zero buffer time for delays. **Dependencies**: All subsequent project decisions depend on these results. **Critical Path**: Any delay impacts entire project schedule. | 0.93 | critical | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |
| 8 | 01K4B7WDZXYFF3KRAZB8BDTPQS | 42 | stakeholder_feedback | Enhanced negotiating position through partnership | **STRATEGIC ADVANTAGE**: Four-partner coalition provides stronger negotiating leverage with landowner. **Benefit**: Unified financial commitment and shared risk creates more credible negotiating position. **Impact**: Improved deal terms likelihood. | 0.87 | medium | 0 | ["01K4B7WDZXYFF3KRAZB8BDTPQS"] | 2024-09-09T14:30:00Z |

## Metadata Fields for Each Insight

### Action Items Additional Metadata
```json
{
  "assignee": "Brandon Clymer",
  "due_date": "2024-09-15",
  "dependencies": ["geotechnical_drilling", "landowner_negotiations"],
  "cost_impact": "$40,000",
  "urgency_reason": "drilling_schedule_fixed"
}
```

### Decision Additional Metadata
```json
{
  "decision_makers": ["Brandon Clymer", "Phil", "Mike", "Tony"],
  "financial_impact": "$40,000",
  "risk_mitigation": "shared_cost_risk_distribution",
  "strategic_benefit": "enhanced_negotiating_power"
}
```

### Risk Additional Metadata
```json
{
  "affected_relationships": ["Michael Bazinski", "Ryder Cup networking"],
  "mitigation_actions": ["exclude_from_events", "limit_client_contact"],
  "impact_assessment": "ongoing_business_development_harm"
}
```

### Timeline Additional Metadata
```json
{
  "critical_dates": {
    "drilling_start": "2024-09-15",
    "results_expected": "2024-09-29"
  },
  "buffer_time": "0_days",
  "dependencies": ["contractor_availability", "weather_conditions"],
  "risk_level": "high_schedule_risk"
}
```

## Key Implementation Notes

1. **meeting_id** references the Fireflies transcript ID
2. **project_id** should be auto-assigned by the project matching algorithm (42 for Paradise Project, 43 for Emerald Coast Marina)
3. **confidence_score** ranges from 0.8-0.95 based on extraction certainty
4. **severity** maps to business impact (critical/high/medium/low)
5. **resolved** starts at 0 (open), changes to 1 when completed
6. **source_meetings** array allows tracking insights across multiple meetings

## SQL Insert Example

```sql
INSERT INTO ai_insights (
  meeting_id, project_id, insight_type, title, description, 
  confidence_score, severity, resolved, source_meetings, created_at
) VALUES (
  '01K4B7WDZXYFF3KRAZB8BDTPQS', 
  42, 
  'action_item',
  'Order Paradise Project geotechnical study',
  '**CRITICAL PATH**: $40,000 geotechnical study must be ordered immediately. Drilling scheduled for September 15, results expected September 29. **Assignee**: Brandon Clymer. **Dependencies**: Results critical for project progression and landowner negotiations.',
  0.95,
  'critical',
  0,
  ARRAY['01K4B7WDZXYFF3KRAZB8BDTPQS'],
  NOW()
);
```