# Comprehensive Dimensional Analysis for Mining Reliability Database
## Fact-Based Record Summarization for Ground Truth Questions

Based on analysis of actual facility data with **47 fields per record**, here are ALL extractable dimensions for dimensional modeling:

## Record Structure Summary

**Data Reality**: 6 sample records, 47 fields each
**Example Record Pattern**:
- **Equipment**: "generator due to conveyor roller issues" 
- **Problem**: "tertiary crusher tripped on high vibration traced to brake system failure"
- **Root Cause**: "Foreign material in wear plate; Inadequate training for replacement"
- **Action**: "Replace filter with upgraded design; Standardize work instructions; Review PM schedule"
- **Facility**: "HUN"
- **Year**: "2022"
- **Success**: "Yes"

## Complete Dimensional Taxonomy

### 1. EQUIPMENT DIMENSIONS (Text Mining Required)

#### 1.1 Primary Equipment Types (from Title + What happened?)
- **Extractable Equipment**: 
  - Generator, Conveyor, Crusher, Truck, Pump, Transfer Station
  - Hydraulic systems, Electrical systems, Filter assemblies
  - Drive systems, Brake systems, Coupling systems

#### 1.2 Equipment Components (Granular Level)
- **From "What happened?" field**:
  - Roller, Vibration sensors, Brake system, Hydraulic hose
  - Filter, Pump, Junction box, Seal, Shaft
  - Wear plate, Coupling, Drive system

#### 1.3 Asset Identification
- **Asset Number(s)**: "ASSET-5596", "ASSET-9822" (categorical)
- **Asset Activity numbers**: "ACT-9836" (tracking IDs)

### 2. FACILITY/LOCATION DIMENSIONS (Clean Categorical)

#### 2.1 Operating Centre (Primary Facility)
- **Values**: HUN, KWN, WDL, YRN, PNJ
- **Question Potential**: Very High - "How many incidents in Pinjarra?"

#### 2.2 Department Dimensions
- **Init. Dept.**: "Reliability", "HUN Mobile Plant", "HUN Fixed Plant"
- **Rec. Dept.**: "Reliability", "HUN Fixed Plant", "HUN Mobile Plant"
- **Organizational Flow**: Initiative → Receiving department patterns

#### 2.3 Derived Location Intelligence
- **Facility Name**: From "_facility_name" field
- **Cross-facility patterns**: HUN Fixed Plant → HUN Mobile Plant transfers

### 3. TEMPORAL DIMENSIONS (Date Processing)

#### 3.1 Primary Temporal Fields
- **Initiation Date**: "2022-12-11T00:00:00" → Year, Month, Season, Day-of-week
- **Due Date**: Target completion timeline
- **Completion Date**: Actual completion timeline
- **Response Date**: First response timing

#### 3.2 Derived Temporal Metrics
- **Response Time**: Due Date - Initiation Date
- **Completion Duration**: Completion Date - Initiation Date
- **Overdue Analysis**: Days Past Due (when not null)
- **Seasonal Patterns**: Month-based incident clustering

#### 3.3 Timeline Analysis Dimensions
- **Year-based**: 2021, 2022, 2023, 2024 patterns
- **Urgency**: Requested Response Time (1, 2, 14 days)
- **Status Timeline**: Past Due Status tracking

### 4. FAILURE MODE DIMENSIONS (Text Classification)

#### 4.1 Failure Types (from Title + What happened?)
- **Electrical**: "electrical system failure"
- **Mechanical**: "premature failure", "vibration", "coupling issues"  
- **Hydraulic**: "hydraulic hose overheating"
- **Contamination**: "leak", "moisture exposure"
- **Wear**: "wear plate", "fatigue"

#### 4.2 Failure Severity (from Amount of Loss)
- **Financial Impact**: 425, 4817, 5368 (numerical ranges)
- **Criticality**: Based on Requested Response Time (1=urgent, 14=routine)

#### 4.3 Failure Context
- **Planned vs Unplanned**: "Unplanned maintenance" pattern detection
- **Operational Impact**: "unplanned shutdown", "operational issues"

### 5. ROOT CAUSE DIMENSIONS (Complex Text Analysis)

#### 5.1 Root Cause Categories (from Root Cause field)
- **Material Issues**: "Foreign material in wear plate"
- **Design Issues**: "Design flaw in filter"
- **Environmental**: "Moisture exposure to filter assembly"
- **Human Factors**: "Inadequate training", "Communication gap between shifts"

#### 5.2 Root Cause Tail Extraction
- **Primary vs Secondary**: Field contains "Root Cause Tail Extraction"
- **Causal Chain**: Multi-level cause analysis

#### 5.3 Evidence Classification (from Obj. Evidence)
- **Evidence Quality**: Present vs null evidence
- **Evidence Type**: Investigation methods used

### 6. ACTION PLAN DIMENSIONS (Multi-Value Text Analysis)

#### 6.1 Action Types (from Action Plan field)
- **Replace**: "Replace filter with upgraded design"
- **Standardize**: "Standardize work instructions"
- **Review**: "Review and revise PM schedule"
- **Implement**: "Implement quarterly visual inspection"
- **Source**: "Source higher quality crusher jaw"

#### 6.2 Immediate Actions (from Immd. Contain. Action)
- **Containment Strategy**: Immediate response patterns
- **Emergency Measures**: Safety-focused actions

#### 6.3 Strategic Impact
- **Strategy Change Required**: "Did this action plan require a change to the equipment management strategy?"
- **Documentation Updates**: APSS Doc # references

### 7. RECURRING PROBLEM DIMENSIONS

#### 7.1 Recurrence Tracking
- **Recurring Problem(s)**: "Yes"/"No" (boolean)
- **Recurring Comment**: Additional recurrence context
- **Pattern Recognition**: Cross-incident similarity

#### 7.2 Problem Classification
- **Chronic vs Acute**: Based on recurrence patterns
- **Facility-specific vs Cross-facility**: Recurrence scope

### 8. WORKFLOW STAGE DIMENSIONS (Process Intelligence)

#### 8.1 Process Stage (from Stage field)
- **Open - Waiting on Receiver to document Root Cause/Action Plan**
- **Action Plan Implemented - Waiting on Effectiveness Verification**
- **Action Plan Implemented - Actions Effective - Closed**

#### 8.2 Completion Status (from Complete field)
- **Yes**: Successfully completed
- **Cancelled**: Terminated early
- **Moved to long-term plan**: Deferred

#### 8.3 Review Process
- **Is Resp Satisfactory?**: Quality assessment
- **Reviewed Date**: Review completion tracking

### 9. EFFECTIVENESS DIMENSIONS (Success Metrics)

#### 9.1 Action Plan Effectiveness
- **IsActionPlanEffective**: "Yes" (primary success metric)
- **Action Plan Eval Comment**: Effectiveness assessment details

#### 9.2 Verification Process
- **Effectiveness Verification Due Date**: Planned verification
- **Action Plan Verification Date**: Actual verification

#### 9.3 Success Rate Calculations
- **Facility-based Success**: Success rate by operating centre
- **Equipment-based Success**: Success rate by equipment type
- **Time-based Success**: Success rate trends over time

### 10. REQUIREMENT AND SPECIFICATION DIMENSIONS

#### 10.1 Requirements (from Requirement field)
- **Standard Requirement**: "Perform root cause analysis and implement corrective actions to prevent recurrence"
- **Custom Requirements**: Variation analysis

#### 10.2 Response Time Requirements
- **Urgency Classification**: 1-day, 2-day, 14-day response requirements
- **SLA Compliance**: Meeting requested response times

## Dimensional Question Matrix by Complexity

### SIMPLE (5/30) - Single Dimension
- **Facility**: "How many incidents in HUN?"
- **Year**: "How many incidents in 2022?"
- **Equipment**: "How many generator issues?"
- **Status**: "How many completed action plans?"
- **Effectiveness**: "How many effective solutions?"

### INTERMEDIATE (7/30) - Two-Dimension Cross Analysis  
- **Facility × Equipment**: "How many generator issues in HUN?"
- **Year × Facility**: "How many incidents per facility in 2022?"
- **Equipment × Effectiveness**: "What's the success rate for generator repairs?"
- **Department × Equipment**: "How many mobile plant equipment issues?"
- **Temporal × Status**: "How many overdue action plans this year?"
- **Recurrence × Facility**: "How many recurring problems by facility?"
- **Urgency × Equipment**: "How many urgent electrical issues?"

### HARD (18/30) - Multi-Dimension + Analytics
- **Triple Combinations**: Facility × Equipment × Year success rates
- **Root Cause Patterns**: "Most common root causes for electrical failures in HUN"
- **Action Effectiveness**: "Which action plan types are most effective for crusher issues?"
- **Cross-Facility Learning**: "Which facility has best practices for conveyor maintenance?"
- **Temporal Trends**: "How has generator reliability improved over time?"
- **Department Efficiency**: "Which departments resolve issues fastest?"
- **Recurrence Prevention**: "Success rate for preventing recurring problems"
- **Cost-Benefit Analysis**: "Return on investment by action plan type"

## Implementation Strategy

### Phase 1: Clean Dimensions (Immediate)
- Operating Centre, Year, Stage, Effectiveness (10 questions)

### Phase 2: Text Mining Dimensions (2-3 weeks)
- Equipment extraction, Failure mode classification (10 questions)

### Phase 3: Complex Analysis (1-2 months)  
- Root cause categorization, Action plan effectiveness (10 questions)

This comprehensive dimensional analysis provides **30+ distinct dimensions** from 47 fields, enabling systematic ground truth question generation across all complexity levels. 