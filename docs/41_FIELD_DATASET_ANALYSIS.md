# 41-Field Raw Dataset Analysis

## Mining Reliability Database - Complete Field Documentation

### 📊 **Dataset Overview**

- **Total Fields**: 41 raw fields
- **Entity Distribution**: 12 logical entities
- **Data Source**: Mining reliability incident records
- **Architecture**: Graph database (Neo4j) with entity relationships

---

## 🗂️ **Field Categories Summary**

| **Category**       | **Field Count** | **Purpose**                   | **Data Types** |
| ------------------ | --------------- | ----------------------------- | -------------- |
| **Identification** | 4 fields        | Unique identifiers and titles | VARCHAR, TEXT  |
| **Temporal**       | 8 fields        | Date tracking across workflow | DATE           |
| **Categorical**    | 7 fields        | Classifications and statuses  | VARCHAR        |
| **Boolean**        | 7 fields        | Binary states and flags       | BOOLEAN        |
| **Descriptive**    | 12 fields       | Detailed text descriptions    | TEXT           |
| **Quantitative**   | 2 fields        | Numeric measurements          | INTEGER        |
| **List-based**     | 1 field         | Multiple values per record    | ARRAY          |

---

## 📋 **Complete Field Analysis**

### **IDENTIFICATION FIELDS** (4 fields)

#### **Field #1: Action Request Number:**

- **Entity**: ActionRequest
- **Database Field**: `action_request_number`
- **Data Type**: VARCHAR(50)
- **Purpose**: Primary unique identifier for each incident
- **Sample Values**: "2023-04657", "2021-08392"
- **Data Quality**: ✅ **Critical** (100% required)
- **Business Role**: Links all related records in the workflow

#### **Field #2: Title**

- **Entity**: ActionRequest
- **Database Field**: `title`
- **Data Type**: VARCHAR(200)
- **Purpose**: Brief incident summary description
- **Sample Values**: "Unplanned maintenance on generator due to conveyor roller issues"
- **Data Quality**: ✅ **High** (90%+ completion)
- **Business Role**: Quick reference for stakeholder identification

#### **Field #19: Asset Number(s)**

- **Entity**: Asset
- **Database Field**: `asset_numbers`
- **Data Type**: VARCHAR(100)
- **Purpose**: Equipment identification codes
- **Sample Values**: "ASSET-5596", "EQUIP-1234"
- **Data Quality**: 📊 **Medium** (70-80% completion)
- **Business Role**: Equipment tracking and maintenance history

#### **Field #37: Asset Activity numbers**

- **Entity**: Asset
- **Database Field**: `asset_activity_numbers`
- **Data Type**: VARCHAR(100)
- **Purpose**: Related maintenance activity codes
- **Sample Values**: "ACT-9836", "ACTIVITY-7821"
- **Data Quality**: 📊 **Medium** (60-70% completion)
- **Business Role**: Activity correlation and scheduling

---

### **TEMPORAL FIELDS** (8 fields)

#### **Field #3: Initiation Date**

- **Entity**: ActionRequest
- **Database Field**: `initiation_date`
- **Data Type**: DATE
- **Purpose**: When the incident was first reported
- **Sample Values**: "2022-12-11T00:00:00"
- **Data Quality**: ✅ **Critical** (95%+ completion)
- **Business Role**: Timeline tracking and performance metrics

#### **Field #24: Due Date**

- **Entity**: ActionPlan
- **Database Field**: `due_date`
- **Data Type**: DATE
- **Purpose**: Target completion date for action plan
- **Sample Values**: "2024-11-12T00:00:00"
- **Data Quality**: ✅ **High** (85%+ completion)
- **Business Role**: Resource planning and deadline management

#### **Field #26: Completion Date**

- **Entity**: ActionPlan
- **Database Field**: `completion_date`
- **Data Type**: DATE
- **Purpose**: Actual completion date of action plan
- **Sample Values**: "2023-04-20T00:00:00"
- **Data Quality**: 📊 **Medium** (75% completion)
- **Business Role**: Performance measurement and effectiveness tracking

#### **Field #28: Response Date**

- **Entity**: ActionPlan
- **Database Field**: `response_date`
- **Data Type**: DATE
- **Purpose**: Initial response to incident
- **Sample Values**: "2024-01-27T00:00:00"
- **Data Quality**: 📊 **Medium** (70% completion)
- **Business Role**: Response time analysis

#### **Field #29: Response Revision Date**

- **Entity**: ActionPlan
- **Database Field**: `response_revision_date`
- **Data Type**: DATE
- **Purpose**: Updated response timestamp
- **Sample Values**: "2023-02-15T00:00:00"
- **Data Quality**: ⚠️ **Low** (40% completion)
- **Business Role**: Change tracking and revision history

#### **Field #34: Reviewed Date:**

- **Entity**: Review
- **Database Field**: `reviewed_date`
- **Data Type**: DATE
- **Purpose**: Quality review completion date
- **Sample Values**: "2023-11-02T00:00:00"
- **Data Quality**: 📊 **Medium** (65% completion)
- **Business Role**: Quality assurance timeline

#### **Field #38: Effectiveness Verification Due Date**

- **Entity**: Verification
- **Database Field**: `effectiveness_verification_due_date`
- **Data Type**: DATE
- **Purpose**: When effectiveness check is scheduled
- **Sample Values**: "2023-08-12T00:00:00"
- **Data Quality**: 📊 **Medium** (60% completion)
- **Business Role**: Follow-up scheduling and verification planning

#### **Field #41: Action Plan Verification Date:**

- **Entity**: Verification
- **Database Field**: `action_plan_verification_date`
- **Data Type**: DATE
- **Purpose**: Actual verification completion date
- **Sample Values**: "2023-09-01T00:00:00"
- **Data Quality**: ⚠️ **Low** (45% completion)
- **Business Role**: Solution effectiveness confirmation

---

### **CATEGORICAL FIELDS** (7 fields)

#### **Field #4: Action Types**

- **Entity**: ActionRequest
- **Database Field**: `action_types`
- **Data Type**: VARCHAR(100)
- **Purpose**: Classification of incident type
- **Sample Values**: "Reliability Action Request", "Maintenance Action"
- **Data Quality**: ✅ **High** (90% completion)
- **Business Role**: Resource allocation and workflow routing

#### **Field #5: Categories**

- **Entity**: ActionRequest
- **Database Field**: `categories`
- **Data Type**: VARCHAR(100)
- **Purpose**: Business domain classification
- **Sample Values**: "Production", "Safety", "Environmental"
- **Data Quality**: ✅ **High** (85% completion)
- **Business Role**: Priority setting and department routing

#### **Field #7: Past Due Status**

- **Entity**: ActionRequest
- **Database Field**: `past_due_status`
- **Data Type**: VARCHAR(50)
- **Purpose**: Timeline status indicator
- **Sample Values**: "N/A", "Past Due", "On Track"
- **Data Quality**: 📊 **Medium** (70% completion)
- **Business Role**: Performance monitoring and escalation

#### **Field #9: Operating Centre**

- **Entity**: ActionRequest
- **Database Field**: `operating_centre`
- **Data Type**: VARCHAR(50)
- **Purpose**: Physical location identifier
- **Sample Values**: "HUN", "WA-Mining", "Pinjarra"
- **Data Quality**: ✅ **High** (90% completion)
- **Business Role**: Geographic analysis and resource coordination

#### **Field #10: Stage**

- **Entity**: ActionRequest
- **Database Field**: `stage`
- **Data Type**: VARCHAR(100)
- **Purpose**: Current workflow state
- **Sample Values**: "Action Plan Implemented - Actions Effective - Closed"
- **Data Quality**: ✅ **High** (95% completion)
- **Business Role**: Workflow progression tracking

#### **Field #11: Init. Dept.**

- **Entity**: Department
- **Database Field**: `init_dept`
- **Data Type**: VARCHAR(100)
- **Purpose**: Department that initiated the incident report
- **Sample Values**: "Reliability", "Operations", "Maintenance"
- **Data Quality**: ✅ **High** (85% completion)
- **Business Role**: Departmental analytics and expertise routing

#### **Field #12: Rec. Dept.**

- **Entity**: Department
- **Database Field**: `rec_dept`
- **Data Type**: VARCHAR(100)
- **Purpose**: Department receiving the action request
- **Sample Values**: "Reliability", "Engineering", "Maintenance"
- **Data Quality**: 📊 **Medium** (75% completion)
- **Business Role**: Resource allocation and responsibility tracking

---

### **BOOLEAN FIELDS** (7 fields)

#### **Field #13: Recurring Problem(s)**

- **Entity**: RecurringStatus
- **Database Field**: `recurring_problems`
- **Data Type**: BOOLEAN
- **Purpose**: Indicates if incident is part of recurring pattern
- **Sample Values**: "Yes", "No"
- **Data Quality**: ✅ **High** (90% completion)
- **Business Role**: Pattern analysis and preventive action prioritization

#### **Field #25: Complete**

- **Entity**: ActionPlan
- **Database Field**: `complete`
- **Data Type**: BOOLEAN
- **Purpose**: Action plan completion status
- **Sample Values**: "Yes", "No"
- **Data Quality**: ✅ **High** (95% completion)
- **Business Role**: Progress tracking and closure management

#### **Field #30: Did this action plan require a change to the equipment management strategy ?**

- **Entity**: ActionPlan
- **Database Field**: `did_plan_require_strategy_change`
- **Data Type**: BOOLEAN
- **Purpose**: Strategic impact indicator
- **Sample Values**: "Yes", "No"
- **Data Quality**: 📊 **Medium** (65% completion)
- **Business Role**: Strategic planning and policy updates

#### **Field #31: If yes, are there any corrective actions to update the strategy in APSS, eAM, ASM and BOM as required ?**

- **Entity**: ActionPlan
- **Database Field**: `are_there_corrective_actions_to_update`
- **Data Type**: BOOLEAN
- **Purpose**: System update requirement flag
- **Sample Values**: "Yes", "No"
- **Data Quality**: ⚠️ **Low** (40% completion)
- **Business Role**: System maintenance and documentation updates

#### **Field #32: Is Resp Satisfactory?**

- **Entity**: Review
- **Database Field**: `is_resp_satisfactory`
- **Data Type**: BOOLEAN
- **Purpose**: Quality approval indicator
- **Sample Values**: "Yes", "No"
- **Data Quality**: 📊 **Medium** (70% completion)
- **Business Role**: Quality assurance and approval workflow

#### **Field #35: Did this action plan require a change to the equipment management strategy ? (review)**

- **Entity**: Review
- **Database Field**: `did_plan_require_change_review`
- **Data Type**: BOOLEAN
- **Purpose**: Review-level strategic impact confirmation
- **Sample Values**: "Yes", "No"
- **Data Quality**: ⚠️ **Low** (45% completion)
- **Business Role**: Strategic decision validation

#### **Field #39: IsActionPlanEffective**

- **Entity**: Verification
- **Database Field**: `is_action_plan_effective`
- **Data Type**: BOOLEAN
- **Purpose**: Solution effectiveness confirmation
- **Sample Values**: "Yes", "No"
- **Data Quality**: 📊 **Medium** (75% completion)
- **Business Role**: Solution validation and learning capture

---

### **DESCRIPTIVE FIELDS** (12 fields)

#### **Field #15: What happened?**

- **Entity**: Problem
- **Database Field**: `what_happened`
- **Data Type**: TEXT
- **Purpose**: Detailed incident description
- **Sample Values**: "The tertiary crusher tripped on high vibration which was traced to a brake system failure."
- **Data Quality**: ✅ **Critical** (95% completion)
- **Business Role**: Primary incident documentation for analysis

#### **Field #16: Requirement**

- **Entity**: Problem
- **Database Field**: `requirement`
- **Data Type**: TEXT
- **Purpose**: Success criteria and expected outcomes
- **Sample Values**: "Perform root cause analysis and implement corrective actions to prevent recurrence."
- **Data Quality**: 📊 **Medium** (70% completion)
- **Business Role**: Objective setting and outcome measurement

#### **Field #17: Obj. Evidence**

- **Entity**: RootCause
- **Database Field**: `objective_evidence`
- **Data Type**: TEXT (List-capable)
- **Purpose**: Supporting evidence for root cause analysis
- **Sample Values**: ["Shake enjoy site interview agent myself", "Score indeed kind clearly road today"]
- **Data Quality**: 📊 **Medium** (65% completion)
- **Business Role**: Evidence documentation and analytical support
- **Special Handling**: Uses head item (first element) from list

#### **Field #18: Recom.Action**

- **Entity**: ActionPlan
- **Database Field**: `recommended_action`
- **Data Type**: TEXT (List-capable)
- **Purpose**: Suggested corrective actions
- **Sample Values**: ["Dinner leader book nearly", "Cause onto beat debate listen test"]
- **Data Quality**: 📊 **Medium** (75% completion)
- **Business Role**: Solution recommendations and action guidance
- **Special Handling**: Uses head item (first element) from list

#### **Field #20: Amount of Loss**

- **Entity**: AmountOfLoss
- **Database Field**: `amount_of_loss`
- **Data Type**: VARCHAR(100)
- **Purpose**: Financial impact quantification
- **Sample Values**: "$15,000", "3.5 days production loss"
- **Data Quality**: ⚠️ **Low** (35% completion)
- **Business Role**: Financial impact analysis and prioritization

#### **Field #21: Immd. Contain. Action or Comments**

- **Entity**: ActionPlan
- **Database Field**: `immediate_containment`
- **Data Type**: TEXT (List-capable)
- **Purpose**: Immediate response actions taken
- **Sample Values**: ["Their film job worker", "Effect action realize among short can ready"]
- **Data Quality**: 📊 **Medium** (60% completion)
- **Business Role**: Emergency response documentation
- **Special Handling**: Uses head item (first element) from list

#### **Field #22: Root Cause**

- **Entity**: RootCause
- **Database Field**: `root_cause`
- **Data Type**: TEXT (List-capable)
- **Purpose**: Identified primary and secondary causes
- **Sample Values**: ["Foreign material in wear plate", "Inadequate training for replacement"]
- **Data Quality**: ✅ **High** (85% completion)
- **Business Role**: Causal analysis and preventive action development
- **Special Handling**: Uses tail item (second element) from list for primary cause

#### **Field #23: Action Plan**

- **Entity**: ActionPlan
- **Database Field**: `action_plan`
- **Data Type**: TEXT (List-capable)
- **Purpose**: Detailed corrective action plan
- **Sample Values**: ["Replace filter with upgraded design", "Standardize work instructions", "Review PM schedule"]
- **Data Quality**: ✅ **High** (90% completion)
- **Business Role**: Solution implementation and resource planning

#### **Field #27: Comments**

- **Entity**: ActionPlan
- **Database Field**: `comments`
- **Data Type**: TEXT
- **Purpose**: Additional notes and context
- **Sample Values**: "Coordination required with maintenance team", "Seasonal considerations apply"
- **Data Quality**: ⚠️ **Low** (45% completion)
- **Business Role**: Contextual information and implementation notes

#### **Field #14: Recurring Comment**

- **Entity**: RecurringStatus
- **Database Field**: `recurring_comment`
- **Data Type**: TEXT
- **Purpose**: Pattern description for recurring issues
- **Sample Values**: "Similar failure occurred in Q2 2022", "Third occurrence this year"
- **Data Quality**: ⚠️ **Low** (30% completion)
- **Business Role**: Pattern analysis and trend identification

#### **Field #33: Reason if not Satisfactory**

- **Entity**: Review
- **Database Field**: `reason_if_not_satisfactory`
- **Data Type**: TEXT
- **Purpose**: Explanation for rejection or revision
- **Sample Values**: "Insufficient detail in root cause analysis", "Timeline unrealistic"
- **Data Quality**: ⚠️ **Low** (25% completion)
- **Business Role**: Quality feedback and improvement guidance

#### **Field #36: If yes, APSS Doc #**

- **Entity**: EquipmentStrategy
- **Database Field**: `apss_doc_number`
- **Data Type**: VARCHAR(100)
- **Purpose**: Equipment strategy document reference
- **Sample Values**: "APPS-23899", "STRATEGY-DOC-4567"
- **Data Quality**: ⚠️ **Low** (35% completion)
- **Business Role**: Strategic documentation and policy linkage

#### **Field #40: Action Plan Eval Comment**

- **Entity**: Verification
- **Database Field**: `action_plan_eval_comment`
- **Data Type**: TEXT
- **Purpose**: Effectiveness evaluation details
- **Sample Values**: "Consumer star those memory center quite simply", "Effective solution with no recurrence"
- **Data Quality**: 📊 **Medium** (60% completion)
- **Business Role**: Solution assessment and knowledge capture

---

### **QUANTITATIVE FIELDS** (2 fields)

#### **Field #6: Requested Response Time**

- **Entity**: ActionRequest
- **Database Field**: `requested_response_time`
- **Data Type**: VARCHAR(50)
- **Purpose**: Expected response timeline
- **Sample Values**: 2, "24 hours", "Critical - Immediate"
- **Data Quality**: 📊 **Medium** (65% completion)
- **Business Role**: Priority setting and resource allocation

#### **Field #8: Days Past Due**

- **Entity**: ActionRequest
- **Database Field**: `days_past_due`
- **Data Type**: INTEGER
- **Purpose**: Quantified delay measurement
- **Sample Values**: null, 5, 12
- **Data Quality**: ⚠️ **Low** (40% completion)
- **Business Role**: Performance metrics and escalation triggers

---

## 🔗 **Entity Relationships & Workflow**

### **Primary Workflow Sequence**

```
ActionRequest → Problem → RootCause → ActionPlan → Verification → Review
```

### **Supporting Entities**

```
Department (initiating/receiving)
Asset (equipment involved)
RecurringStatus (pattern analysis)
AmountOfLoss (financial impact)
EquipmentStrategy (strategic documentation)
```

### **Field Distribution by Entity**

| **Entity**            | **Field Count** | **Percentage** | **Primary Fields**       |
| --------------------- | --------------- | -------------- | ------------------------ |
| **ActionRequest**     | 10              | 24.4%          | Core workflow entry      |
| **ActionPlan**        | 11              | 26.8%          | Solution implementation  |
| **Verification**      | 4               | 9.8%           | Effectiveness validation |
| **Review**            | 4               | 9.8%           | Quality assurance        |
| **RootCause**         | 2               | 4.9%           | Causal analysis          |
| **Problem**           | 2               | 4.9%           | Incident documentation   |
| **Department**        | 2               | 4.9%           | Organizational tracking  |
| **Asset**             | 2               | 4.9%           | Equipment management     |
| **RecurringStatus**   | 2               | 4.9%           | Pattern recognition      |
| **AmountOfLoss**      | 1               | 2.4%           | Financial tracking       |
| **EquipmentStrategy** | 1               | 2.4%           | Strategic documentation  |

---

## 📊 **Data Quality Overview**

### **Completion Rate Summary**

- **Critical Fields** (95-100%): 5 fields
- **High Quality** (80-94%): 8 fields
- **Medium Quality** (60-79%): 17 fields
- **Low Quality** (25-59%): 11 fields

### **Special Data Handling**

#### **List Fields (4 fields)**

1. **Root Cause**: Uses tail extraction (second element)
2. **Obj. Evidence**: Uses head extraction (first element)
3. **Recom.Action**: Uses head extraction (first element)
4. **Immd. Contain. Action**: Uses head extraction (first element)

#### **Missing Data Indicators**

- `null`, `"N/A"`, `"DATA_NOT_AVAILABLE"`, `"NOT_SPECIFIED"`

---

## 🎯 **Business Intelligence Applications**

### **Stakeholder Essential Questions Support**

1. **"Why did this happen?"** → Root Cause, Obj. Evidence fields
2. **"How do I figure out what's wrong?"** → Recom.Action, Action Plan fields
3. **"Who can help me?"** → Init. Dept., Rec. Dept. fields
4. **"What should I check first?"** → Immd. Contain. Action field
5. **"How do I fix it?"** → Action Plan, Verification fields

### **Performance Metrics**

- **Response Time**: Initiation Date → Response Date
- **Resolution Time**: Due Date → Completion Date
- **Effectiveness Rate**: IsActionPlanEffective analysis
- **Recurring Pattern**: Recurring Problem(s) tracking

### **Cross-Facility Intelligence**

- **Equipment Patterns**: Asset Number(s) analysis across Operating Centres
- **Department Expertise**: Init. Dept. success rates by Categories
- **Solution Transferability**: Action Plan effectiveness across facilities

---

## 🔧 **Technical Implementation**

### **Database Schema**

- **Graph Database**: Neo4j with entity relationships
- **Field Mapping**: JSON configuration-driven
- **Data Processing**: List field extraction with head/tail logic
- **Validation**: Required field checking with quality scoring

### **Query Optimization**

- **Indexed Fields**: Action Request Number, Asset Number(s), Operating Centre
- **Composite Indexes**: Stage + Categories, Init. Dept. + Action Types
- **Full-text Search**: What happened?, Root Cause, Action Plan fields

### **API Integration**

- **Adapter Pattern**: Entity-specific data access
- **Caching Strategy**: Critical fields (3600s), High fields (1800s)
- **Real-time Updates**: Stage progression tracking
- **Error Handling**: Missing data fallback with quality indicators

---

## 📈 **Future Enhancement Opportunities**

### **Data Quality Improvements**

1. **Mandatory Field Validation**: Increase completion rates for critical workflow fields
2. **Standardized Vocabularies**: Categorical field consistency across facilities
3. **Automated Metrics**: Days Past Due calculation from date fields
4. **List Field Optimization**: Enhanced extraction logic for multi-value fields

### **Analytics Extensions**

1. **Predictive Modeling**: Equipment failure prediction using pattern analysis
2. **Resource Optimization**: Department expertise mapping for optimal routing
3. **Cost Analysis**: Enhanced Amount of Loss tracking with standardized formats
4. **Cross-Reference Intelligence**: APSS Doc # integration with equipment strategy

### **Integration Enhancements**

1. **Real-time Dashboards**: Live Stage progression monitoring
2. **Mobile Access**: Field-ready data entry for immediate containment actions
3. **Automated Alerts**: Past Due Status escalation workflows
4. **Knowledge Management**: Solution effectiveness learning capture

---

_Document Generated: June 11, 2025_
_Mining Reliability Database Intelligence Engine_
_Complete 41-Field Analysis - Production Ready_
