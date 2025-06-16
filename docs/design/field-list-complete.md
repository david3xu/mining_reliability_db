# Mining Reliability Database: Complete Field List

## All 41 Raw Data Fields Organized by Entity

This document provides a comprehensive list of all 41 raw data fields from the mining reliability database, organized by their target entities for better understanding of the data model structure.

## Complete 41 Fields Reference Table

For quick reference, here is the complete sequential list of all 41 raw data fields:

| #   | Field Name                                         | Data Type    | Entity            | Description                               |
| --- | -------------------------------------------------- | ------------ | ----------------- | ----------------------------------------- |
| 1   | Action Request Number:                             | VARCHAR(50)  | ActionRequest     | Unique identifier for action requests     |
| 2   | Title                                              | VARCHAR(200) | ActionRequest     | Summary description of the action request |
| 3   | Initiation Date                                    | DATE         | ActionRequest     | Creation timestamp of the action request  |
| 4   | Action Types                                       | VARCHAR(100) | ActionRequest     | Classification of the action type         |
| 5   | Categories                                         | VARCHAR(100) | ActionRequest     | Domain categorization                     |
| 6   | Requested Response Time                            | VARCHAR(50)  | ActionRequest     | Timeline expectation for response         |
| 7   | Past Due Status                                    | VARCHAR(50)  | ActionRequest     | Current timeline status                   |
| 8   | Days Past Due                                      | INTEGER      | ActionRequest     | Number of days past the due date          |
| 9   | Operating Centre                                   | VARCHAR(50)  | ActionRequest     | Location identifier                       |
| 10  | Stage                                              | VARCHAR(100) | ActionRequest     | Current workflow state                    |
| 11  | Init. Dept.                                        | VARCHAR(100) | Department        | Initiating department                     |
| 12  | Rec. Dept.                                         | VARCHAR(100) | Department        | Receiving department                      |
| 13  | Recurring Problem(s)                               | BOOLEAN      | RecurringStatus   | Flag indicating recurring pattern         |
| 14  | Recurring Comment                                  | TEXT         | RecurringStatus   | Description of recurring pattern          |
| 15  | What happened?                                     | TEXT         | Problem           | Detailed incident description             |
| 16  | Requirement                                        | TEXT         | Problem           | Success criteria definition               |
| 17  | Obj. Evidence                                      | TEXT         | RootCause         | Supporting objective evidence (list)      |
| 18  | Recom.Action                                       | TEXT         | ActionPlan        | Suggested corrective action (list)        |
| 19  | Asset Number(s)                                    | VARCHAR(100) | Asset             | Equipment identification numbers          |
| 20  | Amount of Loss                                     | VARCHAR(100) | AmountOfLoss      | Financial impact assessment               |
| 21  | Immd. Contain. Action or Comments                  | TEXT         | ActionPlan        | Immediate containment measures (list)     |
| 22  | Root Cause                                         | TEXT         | RootCause         | Primary root cause analysis (list)        |
| 23  | Action Plan                                        | TEXT         | ActionPlan        | Detailed resolution steps                 |
| 24  | Due Date                                           | DATE         | ActionPlan        | Target completion date                    |
| 25  | Complete                                           | BOOLEAN      | ActionPlan        | Completion status flag                    |
| 26  | Completion Date                                    | DATE         | ActionPlan        | Actual completion date                    |
| 27  | Comments                                           | TEXT         | ActionPlan        | Additional notes and comments             |
| 28  | Response Date                                      | DATE         | ActionPlan        | Initial response timestamp                |
| 29  | Response Revision Date                             | DATE         | ActionPlan        | Updated response timestamp                |
| 30  | Did this action plan require a change...?          | BOOLEAN      | ActionPlan        | Strategy impact assessment                |
| 31  | If yes, are there any corrective actions...?       | BOOLEAN      | ActionPlan        | Update requirement flag                   |
| 32  | Is Resp Satisfactory?                              | BOOLEAN      | Review            | Response quality assessment               |
| 33  | Reason if not Satisfactory                         | TEXT         | Review            | Rejection reason details                  |
| 34  | Reviewed Date:                                     | DATE         | Review            | Review completion timestamp               |
| 35  | Did this action plan require a change...? (review) | BOOLEAN      | Review            | Review confirmation flag                  |
| 36  | If yes, APSS Doc #                                 | VARCHAR(100) | EquipmentStrategy | Reference document number                 |
| 37  | Asset Activity numbers                             | VARCHAR(100) | Asset             | Related activity identifiers              |
| 38  | Effectiveness Verification Due Date                | DATE         | Verification      | Verification deadline                     |
| 39  | IsActionPlanEffective                              | BOOLEAN      | Verification      | Effectiveness assessment flag             |
| 40  | Action Plan Eval Comment                           | TEXT         | Verification      | Evaluation notes and feedback             |
| 41  | Action Plan Verification Date:                     | DATE         | Verification      | Verification completion date              |

### ActionRequest Entity Fields (10 fields - 24.4%)

Core action request identification and workflow management.

| #   | Field Name              | Data Type    | Description                               |
| --- | ----------------------- | ------------ | ----------------------------------------- |
| 1   | Action Request Number:  | VARCHAR(50)  | Unique identifier for action requests     |
| 2   | Title                   | VARCHAR(200) | Summary description of the action request |
| 3   | Initiation Date         | DATE         | Creation timestamp of the action request  |
| 4   | Action Types            | VARCHAR(100) | Classification of the action type         |
| 5   | Categories              | VARCHAR(100) | Domain categorization                     |
| 6   | Requested Response Time | VARCHAR(50)  | Timeline expectation for response         |
| 7   | Past Due Status         | VARCHAR(50)  | Current timeline status                   |
| 8   | Days Past Due           | INTEGER      | Number of days past the due date          |
| 9   | Operating Centre        | VARCHAR(50)  | Location identifier                       |
| 10  | Stage                   | VARCHAR(100) | Current workflow state                    |

### ActionPlan Entity Fields (11 fields - 26.8%)

Action planning, execution tracking, and strategy management.

| #   | Field Name                                   | Data Type | Description                           |
| --- | -------------------------------------------- | --------- | ------------------------------------- |
| 18  | Recom.Action                                 | TEXT      | Suggested corrective action (list)    |
| 21  | Immd. Contain. Action or Comments            | TEXT      | Immediate containment measures (list) |
| 23  | Action Plan                                  | TEXT      | Detailed resolution steps             |
| 24  | Due Date                                     | DATE      | Target completion date                |
| 25  | Complete                                     | BOOLEAN   | Completion status flag                |
| 26  | Completion Date                              | DATE      | Actual completion date                |
| 27  | Comments                                     | TEXT      | Additional notes and comments         |
| 28  | Response Date                                | DATE      | Initial response timestamp            |
| 29  | Response Revision Date                       | DATE      | Updated response timestamp            |
| 30  | Did this action plan require a change...?    | BOOLEAN   | Strategy impact assessment            |
| 31  | If yes, are there any corrective actions...? | BOOLEAN   | Update requirement flag               |

### Verification Entity Fields (4 fields - 9.8%)

Effectiveness verification and validation tracking.

| #   | Field Name                          | Data Type | Description                   |
| --- | ----------------------------------- | --------- | ----------------------------- |
| 38  | Effectiveness Verification Due Date | DATE      | Verification deadline         |
| 39  | IsActionPlanEffective               | BOOLEAN   | Effectiveness assessment flag |
| 40  | Action Plan Eval Comment            | TEXT      | Evaluation notes and feedback |
| 41  | Action Plan Verification Date:      | DATE      | Verification completion date  |

### Review Entity Fields (4 fields - 9.8%)

Quality review and approval process tracking.

| #   | Field Name                                         | Data Type | Description                 |
| --- | -------------------------------------------------- | --------- | --------------------------- |
| 32  | Is Resp Satisfactory?                              | BOOLEAN   | Response quality assessment |
| 33  | Reason if not Satisfactory                         | TEXT      | Rejection reason details    |
| 34  | Reviewed Date:                                     | DATE      | Review completion timestamp |
| 35  | Did this action plan require a change...? (review) | BOOLEAN   | Review confirmation flag    |

### Problem Entity Fields (2 fields - 4.9%)

Problem definition and requirements specification.

| #   | Field Name     | Data Type | Description                   |
| --- | -------------- | --------- | ----------------------------- |
| 15  | What happened? | TEXT      | Detailed incident description |
| 16  | Requirement    | TEXT      | Success criteria definition   |

### RootCause Entity Fields (2 fields - 4.9%)

Root cause analysis and supporting evidence.

| #   | Field Name    | Data Type | Description                          |
| --- | ------------- | --------- | ------------------------------------ |
| 17  | Obj. Evidence | TEXT      | Supporting objective evidence (list) |
| 22  | Root Cause    | TEXT      | Primary root cause analysis (list)   |

### Department Entity Fields (2 fields - 4.9%)

Organizational department tracking.

| #   | Field Name  | Data Type    | Description           |
| --- | ----------- | ------------ | --------------------- |
| 11  | Init. Dept. | VARCHAR(100) | Initiating department |
| 12  | Rec. Dept.  | VARCHAR(100) | Receiving department  |

### Asset Entity Fields (2 fields - 4.9%)

Equipment and asset identification.

| #   | Field Name             | Data Type    | Description                      |
| --- | ---------------------- | ------------ | -------------------------------- |
| 19  | Asset Number(s)        | VARCHAR(100) | Equipment identification numbers |
| 37  | Asset Activity numbers | VARCHAR(100) | Related activity identifiers     |

### RecurringStatus Entity Fields (2 fields - 4.9%)

Recurring problem pattern tracking.

| #   | Field Name           | Data Type | Description                       |
| --- | -------------------- | --------- | --------------------------------- |
| 13  | Recurring Problem(s) | BOOLEAN   | Flag indicating recurring pattern |
| 14  | Recurring Comment    | TEXT      | Description of recurring pattern  |

### AmountOfLoss Entity Fields (1 field - 2.4%)

Financial impact assessment.

| #   | Field Name     | Data Type    | Description                 |
| --- | -------------- | ------------ | --------------------------- |
| 20  | Amount of Loss | VARCHAR(100) | Financial impact assessment |

### EquipmentStrategy Entity Fields (1 field - 2.4%)

Equipment strategy documentation reference.

| #   | Field Name         | Data Type    | Description               |
| --- | ------------------ | ------------ | ------------------------- |
| 36  | If yes, APSS Doc # | VARCHAR(100) | Reference document number |

## Entity Summary

| Entity            | Field Count | Percentage | Primary Purpose                          |
| ----------------- | ----------- | ---------- | ---------------------------------------- |
| ActionRequest     | 10          | 24.4%      | Core request identification and workflow |
| ActionPlan        | 11          | 26.8%      | Action planning and execution tracking   |
| Verification      | 4           | 9.8%       | Effectiveness validation                 |
| Review            | 4           | 9.8%       | Quality review and approval              |
| Problem           | 2           | 4.9%       | Problem definition                       |
| RootCause         | 2           | 4.9%       | Cause analysis                           |
| Department        | 2           | 4.9%       | Organizational tracking                  |
| Asset             | 2           | 4.9%       | Equipment identification                 |
| RecurringStatus   | 2           | 4.9%       | Pattern tracking                         |
| AmountOfLoss      | 1           | 2.4%       | Financial impact                         |
| EquipmentStrategy | 1           | 2.4%       | Strategy documentation                   |
| **Total**         | **41**      | **100%**   | **Complete field coverage**              |

## Workflow Process Flow

The fields follow a logical workflow progression:

1. **Request Initiation**: ActionRequest → Department
2. **Problem Analysis**: Problem → RootCause → RecurringStatus
3. **Impact Assessment**: Asset → AmountOfLoss
4. **Solution Planning**: ActionPlan → EquipmentStrategy
5. **Quality Control**: Review
6. **Validation**: Verification

## Data Type Summary

| Data Type | Count | Percentage | Fields                                          |
| --------- | ----- | ---------- | ----------------------------------------------- |
| TEXT      | 11    | 26.8%      | 14, 15, 16, 17, 18, 21, 22, 23, 27, 33, 40      |
| VARCHAR   | 14    | 34.1%      | 1, 2, 4, 5, 6, 7, 9, 10, 11, 12, 19, 20, 36, 37 |
| DATE      | 10    | 24.4%      | 3, 24, 26, 28, 29, 34, 38, 41                   |
| BOOLEAN   | 6     | 14.6%      | 13, 25, 30, 31, 32, 35, 39                      |
| INTEGER   | 1     | 2.4%       | 8                                               |

## Special Handling Requirements

### List Fields (4 fields require extraction logic)

- **Field 17** (Obj. Evidence): Extract first element
- **Field 18** (Recom.Action): Extract first element
- **Field 21** (Immd. Contain. Action): Extract first element
- **Field 22** (Root Cause): Extract second element (tail)

### Database Design Notes

- **VARCHAR Sizing**: Optimized lengths (50-200) based on content type
- **TEXT Fields**: Variable-length content for descriptions and comments
- **DATE Fields**: Standard timestamp tracking across workflow stages
- **BOOLEAN Fields**: Binary status and assessment flags
- **Facility Entity**: Container entity with no direct field mappings
