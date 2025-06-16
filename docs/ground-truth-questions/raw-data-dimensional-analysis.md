# Raw Data Dimensional Analysis for Ground Truth Questions
## Based on 45 Fields from Actual Mining Reliability Data

You're absolutely right! I jumped to theoretical solutions without analyzing the actual raw data. Let me systematically analyze what dimensions are **actually available** from the 45 fields.

## Raw Data Reality Check

### Field Structure Analysis

From `sample_5_fab16f86-faa9-44d9-b9d7-cfbbb47061da.json`:

**Total Fields**: 45 (not 41 as originally thought)

**Field Type Breakdown**:
```
Action Request Number: str    → Unique identifier 
Title: str                   → Equipment problem description (TEXT analysis needed)
Initiation Date: str         → Temporal dimension (clean categorical)
Action Types: str            → Workflow type (categorical)
Categories: str              → Equipment category (categorical) 
Requested Response Time: int → Urgency dimension (numerical)
Past Due Status: str         → Status dimension (categorical)
Days Past Due: NoneType      → Duration analysis (often null)
Operating Centre: str        → Facility dimension (categorical)
Stage: str                   → Workflow stage (categorical)
```

## Dimension Classification by Analysis Complexity

### Level 1: Clean Categorical Dimensions (Direct Question Generation)

**1. Operating Centre** (Facility Dimension)
- Values: `HUN`, `KWN`, `WDL`, `YRN`, `PNJ`
- **Question Potential**: High - "How many incidents in Pinjarra?"
- **Ground Truth**: Direct count queries

**2. Categories** (Equipment Type)
- Common Values: `Production` (but may contain equipment types)
- **Question Potential**: Medium - Need text analysis to extract equipment types
- **Ground Truth**: Requires parsing/classification

**3. Stage** (Workflow Progress)
- Examples: "Action Plan Implemented - Actions Effective - Closed"
- **Question Potential**: High - "How many completed action plans?"
- **Ground Truth**: Status-based queries

**4. Action Types**
- Values: "Reliability Action Request"  
- **Question Potential**: Low - Appears uniform
- **Ground Truth**: Limited variation

**5. Past Due Status**
- Values: "N/A", "Past Due", "Due Today"
- **Question Potential**: Medium - Time-based analysis
- **Ground Truth**: Status counting

### Level 2: Text Analysis Dimensions (NLP Required)

**6. Title** (Equipment + Problem Description)
- Examples: 
  - "Unplanned maintenance on generator due to conveyor roller issues"
  - "electrical system failure in truck"
  - "Premature failure of seal in truck"
- **Extraction Needed**: Equipment type (generator, truck, conveyor) + failure mode (electrical, seal, roller)
- **Question Potential**: Very High - "How many electrical failures?"
- **Ground Truth**: Text mining + categorization

**7. What happened?** (Detailed Problem Description)
- Examples:
  - "The tertiary crusher tripped on high vibration which was traced to a brake system failure."
  - "A leak was discovered in the pump of the transfer station"
- **Extraction Needed**: Equipment (crusher, pump), failure mode (vibration, leak), component (brake, transfer station)
- **Question Potential**: Very High - Rich semantic content
- **Ground Truth**: Complex text analysis

**8. Root Cause** (LIST field - Multiple values)
- Examples: `["Foreign material in wear plate", "Inadequate training for replacement"]`
- **Extraction Needed**: Cause categories (material, training, design, maintenance)
- **Question Potential**: High - "How many training-related root causes?"
- **Ground Truth**: List processing + text classification

**9. Action Plan** (LIST field - Multiple values)
- Examples: `["Replace filter with upgraded design", "Standardize work instructions"]`
- **Extraction Needed**: Action types (replace, standardize, inspect, monitor)
- **Question Potential**: High - "What are common action plan types?"
- **Ground Truth**: List processing + text classification

### Level 3: Temporal and Numerical Dimensions

**10. Initiation Date**
- Format: ISO dates "2022-12-11T00:00:00"
- **Extraction**: Year, month, season, day of week
- **Question Potential**: High - "How many incidents in 2015?"
- **Ground Truth**: Date parsing and grouping

**11. Requested Response Time** (Integer)
- Values: 1, 2, 14 (days)
- **Question Potential**: Medium - "How many urgent (1-day) responses?"
- **Ground Truth**: Numerical filtering

**12. Days Past Due**
- Often null, sometimes integers
- **Question Potential**: Low - Data quality issues
- **Ground Truth**: Require null handling

### Level 4: Boolean and Status Dimensions

**13. Complete** (String but Boolean-like)
- Values: "Yes", "Cancelled", "Moved to long-term plan"
- **Question Potential**: High - "What's the completion rate?"
- **Ground Truth**: Status categorization

**14. IsActionPlanEffective** (String Boolean)
- Values: "Yes" (effectiveness tracking)
- **Question Potential**: Very High - "What's the success rate?"
- **Ground Truth**: Effectiveness analysis

**15. Recurring Problem(s)** (String Boolean)
- Values: "No", "Yes"
- **Question Potential**: High - "How many recurring issues?"
- **Ground Truth**: Pattern analysis

## Dimensional Complexity Matrix

| Dimension Type | Fields | Question Generation Difficulty | Ground Truth Complexity |
|----------------|--------|--------------------------------|-------------------------|
| **Clean Categorical** | Operating Centre, Stage, Past Due Status | Easy | Simple count queries |
| **Text Mining Required** | Title, What happened?, Root Cause, Action Plan | Hard | NLP + classification |
| **Temporal** | Initiation Date, Due Date, Completion Date | Medium | Date parsing + grouping |
| **Boolean/Status** | Complete, IsActionPlanEffective, Recurring | Easy | Status-based queries |
| **Numerical** | Requested Response Time, Days Past Due | Easy | Range-based queries |

## Dimensional Question Generation Strategy

### Simple Questions (5/30) - Clean Categorical Only
- "How many incidents in [Operating Centre]?"
- "How many [Past Due Status] incidents?"
- "How many [Stage] action plans?"

### Intermediate Questions (7/30) - Cross-Dimensional + Text Extraction
- "How many [equipment type from Title] incidents in [Operating Centre]?"
- "What's the completion rate by [Operating Centre]?"
- "How many incidents in [year] by facility?"

### Hard Questions (18/30) - Complex Text Analysis + Multi-Dimensional
- "What's the success rate for [equipment type] issues in [facility] during [year]?"
- "What are the most common root cause categories for [equipment type]?"
- "Which facilities have the most effective solutions for [failure type]?"

## Required Pre-Processing for Ground Truth

### 1. Text Mining Pipeline
```python
# Extract equipment types from Title and "What happened?"
equipment_patterns = ["pump", "crusher", "conveyor", "truck", "generator", "motor"]
failure_patterns = ["electrical", "mechanical", "leak", "vibration", "failure"]
```

### 2. Categorical Value Discovery
```cypher
// Discover actual categorical values
MATCH (ar:ActionRequest) 
RETURN DISTINCT ar.operating_centre as facilities
```

### 3. Text Classification for Semantic Dimensions
- Root cause categorization (design, maintenance, training, material)
- Action plan categorization (replace, inspect, monitor, standardize)
- Equipment type extraction (pump, crusher, conveyor, etc.)

## Recommended Implementation Approach

1. **Start with Level 1 (Clean Categorical)** - Generate 10 simple questions immediately
2. **Add Level 4 (Boolean/Status)** - Success rate and completion questions  
3. **Implement Level 3 (Temporal)** - Year-based analysis questions
4. **Build Level 2 (Text Mining)** - Advanced semantic questions

This approach generates ground truth questions **based on actual data capabilities** rather than theoretical dimensional modeling.

## Integration with Existing Search Queries

The existing search queries in `graph_search_config.json` already demonstrate:
- Equipment pattern recognition: `toLower(ar.categories) CONTAINS toLower($search_term)`
- Cross-facility analysis: Facility + Equipment combinations
- Temporal filtering: `year(ar.initiation_date) = $year`
- Effectiveness tracking: `v.is_action_plan_effective = 'Yes'`

These existing patterns should drive the ground truth question structure. 