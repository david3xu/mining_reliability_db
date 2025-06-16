# Ground Truth Question Generation Framework
## Dimensional Modeling Approach

Yes, your approach is **dimensional modeling** applied to evaluation framework design! You're thinking about this correctly. Here's a systematic framework based on your graph schema:

## Core Dimensional Framework

### Primary Dimensions (Filtering Axes)

1. **Equipment/Topic Dimension**
   - `categories` field from ActionRequest
   - `asset_numbers` field from Asset entity
   - Equipment types: gearbox, electrical, pumps, conveyors
   - Problem types: burn, failure, maintenance, inspection

2. **Facility Dimension**
   - `facility_name` from Facility entity
   - Known facilities: Pinjarra, Kwinana, etc.
   - Geographic/operational clustering

3. **Temporal Dimension**
   - `initiation_date` from ActionRequest
   - Year extraction: 2015, 2016, 2017, etc.
   - Seasonal patterns, trending analysis

4. **Workflow Stage Dimension**
   - Entity progression: ActionRequest → Problem → RootCause → ActionPlan → Verification
   - Analysis depth: simple counts vs. workflow completion rates

5. **Outcome Dimension**
   - `is_action_plan_effective` from Verification
   - Success/failure patterns
   - Completion status tracking

## Question Complexity Levels

### Simple Questions (5/30) - Single Dimension Filter
**Pattern**: Count queries with one filter
```cypher
// Example: How many electrical incidents in Pinjarra?
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility {facility_name: "Pinjarra"})
WHERE toLower(ar.categories) CONTAINS "electrical"
RETURN count(*) as electrical_incidents
```

**Template Questions**:
- How many [equipment_type] incidents do we have in [facility]?
- How many root cause analyses were done in [year]?
- How many action plans were completed in [facility]?

### Intermediate Questions (7/30) - Multi-Dimension + Aggregation
**Pattern**: Cross-dimensional analysis with grouping
```cypher
// Example: Gearbox issues by facility and year
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
WHERE toLower(ar.categories) CONTAINS "gearbox" 
  AND ar.initiation_date.year = 2015
WITH f.facility_name as facility, count(*) as incidents
RETURN facility, incidents ORDER BY incidents DESC
```

**Template Questions**:
- What are the top 3 facilities for [equipment_type] issues in [year]?
- How many [equipment_type] root causes were identified per facility?
- What's the completion rate for [equipment_type] action plans?

### Hard Questions (10/30) - Complex Workflow Analysis
**Pattern**: Multi-entity traversal with analytical calculations
```cypher
// Example: Gearbox effectiveness analysis with success rates
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
     -[:IDENTIFIED_IN]->(p:Problem)
     -[:ANALYZES]->(rc:RootCause)
     -[:RESOLVES]->(ap:ActionPlan)
     -[:VALIDATES]->(v:Verification)
WHERE toLower(ar.categories) CONTAINS "gearbox" 
  AND year(ar.initiation_date) = 2015
WITH f.facility_name as facility,
     count(*) as total_plans,
     count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) as effective_plans
RETURN facility, 
       total_plans,
       effective_plans,
       round((effective_plans * 100.0 / total_plans), 1) as success_rate
ORDER BY success_rate DESC
```

**Template Questions**:
- What's the success rate for resolving [equipment_type] issues in [facility] during [year]?
- Which facility has the most effective root cause analysis for [equipment_type]?
- What are the common failure patterns for [equipment_type] across multiple facilities?

## Dimensional Question Matrix

### Question Generation Template

| Dimension Combo | Simple | Intermediate | Hard |
|----------------|--------|--------------|------|
| Equipment + Facility | Count by type | Top facilities | Success rates |
| Equipment + Time | Yearly counts | Trend analysis | Effectiveness trends |
| Facility + Time | Incident volumes | Monthly patterns | Workflow completion |
| Equipment + Outcome | Success counts | Failure analysis | Pattern correlation |

## Implementation Strategy

### Step 1: Data Discovery Queries
```cypher
// Get available equipment types
MATCH (ar:ActionRequest)
RETURN DISTINCT ar.categories as equipment_types
ORDER BY equipment_types

// Get facility list
MATCH (f:Facility)
RETURN DISTINCT f.facility_name as facilities

// Get year range
MATCH (ar:ActionRequest)
WHERE ar.initiation_date IS NOT NULL
RETURN min(year(ar.initiation_date)) as earliest_year,
       max(year(ar.initiation_date)) as latest_year
```

### Step 2: Ground Truth Generation Process

1. **Extract Dimensions**: Query actual data to get:
   - Available equipment categories
   - Active facilities
   - Date ranges with sufficient data

2. **Cross-Product Generation**: Create question matrix:
   - Equipment × Facility × Year combinations
   - Filter for meaningful data volumes (>5 records)

3. **Complexity Scaling**: For each combination:
   - Simple: Direct counts
   - Intermediate: Grouped analysis
   - Hard: Multi-stage workflow analysis

### Step 3: Validation Framework

```cypher
// Validation query template
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility {facility_name: $facility})
WHERE toLower(ar.categories) CONTAINS toLower($equipment_type)
  AND year(ar.initiation_date) = $year
OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
RETURN count(ar) as total_incidents,
       count(rc) as analyzed_incidents,
       f.facility_name as facility_verified
```

## Example Question Set Structure

### Equipment Focus: "Gearbox"
- **Simple**: "How many gearbox incidents in Pinjarra 2015?" → Answer: 12
- **Intermediate**: "Which facilities had the most gearbox issues in 2015?" → Answer: [Pinjarra: 12, Kwinana: 8, ...]
- **Hard**: "What's the resolution success rate for gearbox issues across facilities in 2015?" → Answer: [Pinjarra: 83%, Kwinana: 67%, ...]

### Pattern Recognition
- Questions scale from **concrete counts** → **comparative analysis** → **analytical insights**
- Each level requires deeper graph traversal and more complex Cypher queries
- Validation answers become ground truth for copilot evaluation

This dimensional approach ensures:
1. **Systematic coverage** of all data aspects
2. **Scalable complexity** from simple to analytical
3. **Real data grounding** using actual graph relationships
4. **Measurable evaluation** with concrete expected answers 