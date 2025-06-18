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

### 🎯 Raw Data Strategy for Copilot Studio Integration

Based on practical implementation experience, here's how to map raw data dimensions to **business value categories** for Copilot Studio:

```bash
RAW_DATA_CATEGORIES = {
  "incident_identification": ["Action Request Number", "Title", "Initiation Date", "Operating Centre"],
  "problem_description": ["Title", "What happened?", "Categories"],
  "solution_tracking": ["Action Plan", "Stage", "Complete"],
  "outcome_verification": ["IsActionPlanEffective", "Complete", "Recurring Problem(s)"],
  "operational_context": ["Operating Centre", "Categories", "Action Types", "Past Due Status"]
}
```

### Level 1: Clean Categorical Dimensions (Direct Copilot Studio Implementation)

**1. Operating Centre** (Facility Dimension) - **PRIORITY 1**

- Values: `HUN`, `KWN`, `WDL`, `YRN`, `PNJ`
- **Copilot Studio Use**: Direct facility filtering in knowledge base searches
- **Implementation**: Create "Equipment_Incident_Lookup" tool with facility parameter
- **Question Potential**: High - "Show similar problems at Pinjarra facility"
- **Ground Truth**: Direct count queries

**2. Stage** (Workflow Progress) - **PRIORITY 1**

- Examples: "Action Plan Implemented - Actions Effective - Closed"
- **Copilot Studio Use**: Solution success filtering
- **Implementation**: "Solution_Success_Filter" tool for proven approaches
- **Question Potential**: High - "Show only completed solutions"
- **Ground Truth**: Status-based queries

**3. Past Due Status** - **PRIORITY 2**

- Values: "N/A", "Past Due", "Due Today"
- **Copilot Studio Use**: Urgency escalation triggers
- **Implementation**: Basic escalation logic for recurring patterns
- **Question Potential**: Medium - "Are there overdue similar issues?"
- **Ground Truth**: Status counting

**4. Action Types** - **PRIORITY 3**

- Values: "Reliability Action Request"
- **Copilot Studio Use**: Limited - appears uniform
- **Implementation**: Context filtering only
- **Question Potential**: Low - Appears uniform
- **Ground Truth**: Limited variation

### Level 2: Text Analysis Dimensions (Basic Pattern Matching for Copilot Studio)

**5. Title** (Equipment + Problem Description) - **PRIORITY 1**

- Examples:
  - "Unplanned maintenance on generator due to conveyor roller issues"
  - "electrical system failure in truck"
  - "Premature failure of seal in truck"
- **Copilot Studio Use**: Primary search field for "Historical_Pattern_Search" tool
- **Implementation**: Basic text matching without complex NLP
- **Extraction Strategy**: Simple keyword patterns for equipment types
- **Question Potential**: Very High - "Find similar generator problems"
- **Ground Truth**: Text pattern matching

**6. What happened?** (Detailed Problem Description) - **PRIORITY 1**

- Examples:
  - "The tertiary crusher tripped on high vibration which was traced to a brake system failure."
  - "A leak was discovered in the pump of the transfer station"
- **Copilot Studio Use**: Secondary search field for detailed pattern matching
- **Implementation**: File upload as PDF for guaranteed search priority
- **Extraction Strategy**: Basic keyword matching for failure modes
- **Question Potential**: Very High - Rich descriptive content
- **Ground Truth**: Text search and basic categorization

**7. Root Cause** (LIST field - Multiple values) - **PRIORITY 2**

- Examples: `["Foreign material in wear plate", "Inadequate training for replacement"]`
- **Copilot Studio Use**: Pattern recognition for escalation triggers
- **Implementation**: Simple list processing in knowledge base
- **Extraction Strategy**: Basic cause category matching (material, training, design)
- **Question Potential**: High - "Show training-related solutions"
- **Ground Truth**: List processing + basic text classification

**8. Action Plan** (LIST field - Multiple values) - **PRIORITY 1**

- Examples: `["Replace filter with upgraded design", "Standardize work instructions"]`
- **Copilot Studio Use**: Solution recommendation core content
- **Implementation**: Direct field search in "Solution_Success_Filter" tool
- **Extraction Strategy**: Action type patterns (replace, standardize, inspect)
- **Question Potential**: High - "What solutions worked for similar issues?"
- **Ground Truth**: List processing + action categorization

### Level 3: Temporal and Numerical Dimensions (Basic Filtering)

**9. Initiation Date** - **PRIORITY 2**

- Format: ISO dates "2022-12-11T00:00:00"
- **Copilot Studio Use**: Recent pattern detection for escalation
- **Implementation**: Simple date filtering in knowledge base queries
- **Extraction Strategy**: Basic date ranges (last 30 days, same year)
- **Question Potential**: High - "Show recent similar incidents"
- **Ground Truth**: Date parsing and grouping

**10. Requested Response Time** (Integer) - **PRIORITY 3**

- Values: 1, 2, 14 (days)
- **Copilot Studio Use**: Urgency context in responses
- **Implementation**: Simple numerical filtering
- **Question Potential**: Medium - "Find urgent response examples"
- **Ground Truth**: Numerical filtering

**11. Days Past Due** - **PRIORITY 4**

- Often null, sometimes integers
- **Copilot Studio Use**: Limited due to data quality
- **Implementation**: Skip or null handling only
- **Question Potential**: Low - Data quality issues
- **Ground Truth**: Require null handling

### Level 4: Boolean and Status Dimensions (Success Validation)

**12. Complete** (String but Boolean-like) - **PRIORITY 1**

- Values: "Yes", "Cancelled", "Moved to long-term plan"
- **Copilot Studio Use**: Core success filtering for solution validation
- **Implementation**: Primary filter in "Solution_Success_Filter" tool
- **Question Potential**: High - "Show only successful completions"
- **Ground Truth**: Status categorization

**13. IsActionPlanEffective** (String Boolean) - **PRIORITY 1**

- Values: "Yes" (effectiveness tracking)
- **Copilot Studio Use**: Solution effectiveness validation
- **Implementation**: Key filter for proven solution recommendations
- **Question Potential**: Very High - "What's the success rate?"
- **Ground Truth**: Effectiveness analysis

**14. Recurring Problem(s)** (String Boolean) - **PRIORITY 1**

- Values: "No", "Yes"
- **Copilot Studio Use**: Escalation trigger for expert consultation
- **Implementation**: Pattern detection for escalation logic
- **Question Potential**: High - "Is this a recurring issue type?"
- **Ground Truth**: Pattern analysis

### 🔧 Copilot Studio Implementation Priority

**Phase 1 (Week 1): Core Pattern Matching**

- Fields: Title, What happened?, Complete, IsActionPlanEffective, Operating Centre
- Tools: Historical_Pattern_Search, Solution_Success_Filter
- Focus: Basic text search and success validation

**Phase 2 (Week 2): Enhanced Filtering**

- Fields: Action Plan, Stage, Recurring Problems, Initiation Date
- Tools: Equipment_Incident_Lookup with date filtering
- Focus: Solution recommendations and escalation triggers

**Phase 3 (Week 3): Advanced Context**

- Fields: Root Cause, Past Due Status, Requested Response Time
- Tools: Enhanced escalation logic and urgency context
- Focus: Business intelligence and expert routing

## Dimensional Complexity Matrix

| Dimension Type           | Fields                                         | Question Generation Difficulty | Ground Truth Complexity |
| ------------------------ | ---------------------------------------------- | ------------------------------ | ----------------------- |
| **Clean Categorical**    | Operating Centre, Stage, Past Due Status       | Easy                           | Simple count queries    |
| **Text Mining Required** | Title, What happened?, Root Cause, Action Plan | Hard                           | NLP + classification    |
| **Temporal**             | Initiation Date, Due Date, Completion Date     | Medium                         | Date parsing + grouping |
| **Boolean/Status**       | Complete, IsActionPlanEffective, Recurring     | Easy                           | Status-based queries    |
| **Numerical**            | Requested Response Time, Days Past Due         | Easy                           | Range-based queries     |

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
