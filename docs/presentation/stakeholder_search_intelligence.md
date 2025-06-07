# Stakeholder Search Intelligence
## Mining Reliability Database - Graph Search Documentation

### Executive Summary

Maintenance engineers facing equipment failures require immediate decision intelligence, not data retrieval. This document defines core stakeholder concerns and demonstrates how graph search transforms historical incident data into actionable emergency response guidance.

---

## Core Stakeholder Concerns

### Emergency Decision Sequence

When equipment fails, maintenance engineers follow a predictable decision sequence:

1. **"What do I do RIGHT NOW?"** - Immediate containment actions
2. **"How bad is this?"** - Criticality and urgency assessment  
3. **"What actually works?"** - Proven solution validation
4. **"How long will this take?"** - Resource and timeline planning

### Critical Time Constraints

- **First 30 seconds**: Impact assessment and safety response
- **First 2 minutes**: Problem identification and pattern recognition
- **First 5 minutes**: Solution selection and resource mobilization

---

## Data Intelligence Framework

### Search Architecture

```
Equipment Keywords → Graph Search → Intelligence Processing → Decision Support
```

**Core Flow**: Core Layer Intelligence → Adapter Layer Processing → Component Layer Display

### Multi-Dimensional Search Strategy

#### 1. Direct Field Analysis
**Purpose**: Immediate problem identification
**Data Sources**: 41 structured fields across incident workflow
**Key Fields**: 
- What happened? (problem description)
- Title (equipment identification)
- Root Cause (diagnostic insight)
- Operating Centre (location context)

#### 2. Equipment Pattern Recognition
**Purpose**: Equipment-specific failure intelligence
**Search Logic**:
```cypher
MATCH (ar:ActionRequest)-[:IDENTIFIED_BY]->(p:Problem)-[:ANALYZES]->(rc:RootCause)
WHERE ar.title CONTAINS $equipment_term OR p.what_happened CONTAINS $equipment_term
```
**Intelligence Output**: Equipment type + failure mode + historical patterns

#### 3. Causal Chain Analysis
**Purpose**: Problem progression understanding
**Search Logic**:
```cypher
MATCH (p:Problem)-[:ANALYZES]->(rc:RootCause)-[:RESOLVES]->(ap:ActionPlan)-[:VALIDATES]->(v:Verification)
WHERE p.what_happened CONTAINS $search_term OR rc.root_cause CONTAINS $search_term
```
**Intelligence Output**: Problem → Cause → Solution → Verification chain

#### 4. Cross-Facility Intelligence
**Purpose**: Solution transferability assessment
**Search Logic**: Similar incidents across facilities with same equipment categories
**Intelligence Output**: Proven solutions from other sites

#### 5. Solution Effectiveness Analysis
**Purpose**: Proven solution identification
**Search Logic**:
```cypher
MATCH (ap:ActionPlan)-[:VALIDATES]->(v:Verification)
WHERE v.is_action_plan_effective = 'Yes'
```
**Intelligence Output**: Verified effective solutions only

---

## Stakeholder Intelligence Processing

### 1. Immediate Action Extraction

**Data Source**: `immediate_containment` field from ActionPlan entities
**Processing Logic**:
- Filter actions with >10 characters (meaningful content)
- Deduplicate similar actions
- Rank by frequency and effectiveness

**Output Format**:
```
🚨 IMMEDIATE ACTION:
• Isolate hydraulic system immediately
• Check oil contamination levels
• Replace primary filter
```

### 2. Criticality Assessment

**Data Sources**: 
- `days_past_due` (urgency indicator)
- `amount_of_loss` (financial impact)
- `recurring_problems` (pattern severity)

**Scoring Algorithm**:
```python
if avg_urgency > 10 days OR avg_loss > $5000:
    criticality = "HIGH" (red)
elif avg_urgency > 5 days OR avg_loss > $1000:
    criticality = "MEDIUM" (yellow)
else:
    criticality = "LOW" (green)
```

**Output Format**:
```
⚠️ CRITICALITY: HIGH (avg 8.2 days | avg loss: $12,500)
```

### 3. Proven Solution Validation

**Data Sources**:
- `is_action_plan_effective` from Verification entities
- `is_resp_satisfactory` from Review entities

**Validation Logic**:
- Include only solutions with positive verification
- Calculate success rates from historical data
- Rank by effectiveness and implementation frequency

**Output Format**:
```
✅ PROVEN SOLUTIONS:
#1: Complete hydraulic flush (89% success rate)
#2: Motor replacement with analysis (73% success rate)
```

### 4. Time Estimation

**Data Sources**:
- `initiation_date` to `completion_date` differential
- Similar incident resolution patterns

**Calculation Logic**:
```python
resolution_times = []
for incident in similar_incidents:
    if incident.completion_date and incident.initiation_date:
        days = calculate_difference(incident.completion_date, incident.initiation_date)
        resolution_times.append(days)

average_time = sum(resolution_times) / len(resolution_times)
```

**Output Format**:
```
⏱️ TIME ESTIMATE: 2.3 days average (1-5 days range, 8 similar cases)
```

---

## Implementation Architecture

### Core Layer Intelligence
**File**: `mine_core/business/intelligence_engine.py`
**Responsibility**: Execute multi-dimensional search and extract business intelligence
**Key Methods**:
- `execute_comprehensive_incident_search()`
- `_extract_immediate_actions()`
- `_calculate_criticality_score()`
- `_filter_proven_solutions()`

### Adapter Layer Processing
**File**: `dashboard/adapters/data_adapter.py`
**Responsibility**: Transform core intelligence into component-ready data
**Key Methods**:
- `get_incident_intelligence()`
- Data format standardization
- Error handling and fallback logic

### Component Layer Display
**File**: `dashboard/components/graph_search.py`
**Responsibility**: Render stakeholder intelligence in decision-support format
**Key Components**:
- Emergency action box (red-highlighted)
- Criticality indicator (color-coded)
- Proven solutions panel (success-rated)
- Time estimation display

### Configuration Management
**File**: `configs/incident_intelligence_config.json`
**Configuration Areas**:
- Criticality thresholds
- Solution validation criteria
- Display formatting rules
- Search result limits

---

## Search Result Intelligence

### Input Example
```
Search: "swing motor contamination"
```

### Intelligence Output
```
🚨 IMMEDIATE ACTION:
• Isolate hydraulic system, check oil contamination
• Replace contaminated filters immediately
• Test system pressure before restart

⚠️ CRITICALITY: HIGH (avg 3.2 days downtime | $8,400 average loss)

✅ PROVEN SOLUTIONS:
#1: Complete system flush + filter replacement (89% success, 12/13 cases)
#2: Motor replacement with contamination source analysis (73% success, 8/11 cases)  

⏱️ TIME ESTIMATE: 6-8 hours for flush, 1.5 days for motor replacement
Based on 15 similar swing motor contamination incidents
```

### Decision Intelligence Metrics
- **Response Speed**: Sub-second search to actionable intelligence
- **Solution Confidence**: Historical success rate validation
- **Resource Planning**: Time and complexity estimation
- **Risk Assessment**: Criticality scoring with impact analysis

---

## Data Quality Considerations

### Reliable Data Fields
**High Quality** (>90% completion):
- What happened?, Title, Operating Centre, Categories
- Root Cause, Action Plan, Stage

**Variable Quality** (50-80% completion):
- Immediate containment actions, Amount of loss
- Completion dates, Verification status

**Search Strategy**: Weight results by data quality scores, prioritize high-quality fields for primary matching.

### Confidence Indicators
Search results include confidence scores based on:
- Data completeness of source incidents
- Sample size for statistical analysis
- Verification status of solutions
- Temporal relevance of historical data

---

## Performance Standards

### Response Time Targets
- **Search Execution**: <2 seconds
- **Intelligence Processing**: <1 second  
- **Result Display**: <500ms
- **Total Response**: <3.5 seconds from query to decision intelligence

### Intelligence Quality Metrics
- **Immediate Action Coverage**: 70% of results include containment actions
- **Solution Verification**: 85% of recommended solutions have positive verification
- **Time Estimation Accuracy**: ±20% variance from actual resolution times
- **Criticality Assessment**: 90% correlation with actual incident impact

---

## Conclusion

Graph search transforms raw incident data into immediate decision intelligence for maintenance engineers. The system addresses core stakeholder concerns through multi-dimensional search and intelligent processing, delivering actionable emergency response guidance within critical time constraints.

**Key Success Factors**:
- Focus on stakeholder decision sequence, not data completeness
- Prioritize proven solutions over comprehensive historical analysis  
- Transform uncertainty into confidence through statistical validation
- Maintain architectural integrity while delivering emergency intelligence