# Mining Reliability Database: Field Mapping

## Raw Data to 12-Entity Mapping

This document maps the 41 raw data fields directly to our 12-entity database model. Field associations are based on functional grouping and workflow progression.

## Field Mapping Table

| # | Raw Field Name | Entity | Field Name | Data Type | Notes |
|---|---------------|--------|------------|-----------|-------|
| 1 | Action Request Number: | ActionRequest | action_request_number | VARCHAR(50) | Unique identifier |
| 2 | Title | ActionRequest | title | VARCHAR(200) | Summary description |
| 3 | Initiation Date | ActionRequest | initiation_date | DATE | Creation timestamp |
| 4 | Action Types | ActionRequest | action_types | VARCHAR(100) | Classification |
| 5 | Categories | ActionRequest | categories | VARCHAR(100) | Domain categorization |
| 6 | Requested Response Time | ActionRequest | requested_response_time | VARCHAR(50) | Timeline expectation |
| 7 | Past Due Status | ActionRequest | past_due_status | VARCHAR(50) | Timeline status |
| 8 | Days Past Due | ActionRequest | days_past_due | INTEGER | Timeline metric |
| 9 | Operating Centre | ActionRequest | operating_centre | VARCHAR(50) | Location identifier |
| 10 | Stage | ActionRequest | stage | VARCHAR(100) | Workflow state |
| 11 | Init. Dept. | Department | init_dept | VARCHAR(100) | Initiating department |
| 12 | Rec. Dept. | Department | rec_dept | VARCHAR(100) | Receiving department |
| 13 | Recurring Problem(s) | RecurringStatus | recurring_problems | BOOLEAN | Pattern flag |
| 14 | Recurring Comment | RecurringStatus | recurring_comment | TEXT | Pattern description |
| 15 | What happened? | Problem | what_happened | TEXT | Incident description |
| 16 | Requirement | Problem | requirement | TEXT | Success criteria |
| 17 | Obj. Evidence | RootCause | objective_evidence | TEXT | Supporting data (list) |
| 18 | Recom.Action | ActionPlan | recommended_action | TEXT | Suggested fix (list) |
| 19 | Asset Number(s) | Asset | asset_numbers | VARCHAR(100) | Equipment ID |
| 20 | Amount of Loss | AmountOfLoss | amount_of_loss | VARCHAR(100) | Financial impact |
| 21 | Immd. Contain. Action or Comments | ActionPlan | immediate_containment | TEXT | Interim measures (list) |
| 22 | Root Cause | RootCause | root_cause | TEXT | Primary cause (list) |
| 23 | Action Plan | ActionPlan | action_plan | TEXT | Resolution steps |
| 24 | Due Date | ActionPlan | due_date | DATE | Target date |
| 25 | Complete | ActionPlan | complete | BOOLEAN | Status flag |
| 26 | Completion Date | ActionPlan | completion_date | DATE | Actual completion |
| 27 | Comments | ActionPlan | comments | TEXT | Additional notes |
| 28 | Response Date | ActionPlan | response_date | DATE | Initial response |
| 29 | Response Revision Date | ActionPlan | response_revision_date | DATE | Updated response |
| 30 | Did this action plan require a change...? | ActionPlan | did_plan_require_strategy_change | BOOLEAN | Strategy impact |
| 31 | If yes, are there any corrective actions...? | ActionPlan | are_there_corrective_actions_to_update | BOOLEAN | Update flag |
| 32 | Is Resp Satisfactory? | Review | is_resp_satisfactory | BOOLEAN | Quality check |
| 33 | Reason if not Satisfactory | Review | reason_if_not_satisfactory | TEXT | Rejection reason |
| 34 | Reviewed Date: | Review | reviewed_date | DATE | Review timestamp |
| 35 | Did this action plan require a change...? (review) | Review | did_plan_require_change_review | BOOLEAN | Review confirmation |
| 36 | If yes, APSS Doc # | EquipmentStrategy | apss_doc_number | VARCHAR(100) | Reference document |
| 37 | Asset Activity numbers | Asset | asset_activity_numbers | VARCHAR(100) | Related activities |
| 38 | Effectiveness Verification Due Date | Verification | effectiveness_verification_due_date | DATE | Check due date |
| 39 | IsActionPlanEffective | Verification | is_action_plan_effective | BOOLEAN | Effectiveness flag |
| 40 | Action Plan Eval Comment | Verification | action_plan_eval_comment | TEXT | Evaluation notes |
| 41 | Action Plan Verification Date: | Verification | action_plan_verification_date | DATE | Verification date |

## List Field Handling

Four raw data fields contain multiple values requiring special handling:

### 1. Root Cause → RootCause.root_cause
- Extraction: Use tail item (second element) if available
- Example:
  ```
  ["Foreign material in wear plate", "Inadequate training for replacement"]
  → "Inadequate training for replacement"
  ```

### 2. Obj. Evidence → RootCause.objective_evidence
- Extraction: Use head item (first element)
- Example:
  ```
  ["Shake enjoy site interview agent myself", "Score indeed kind clearly road today"]
  → "Shake enjoy site interview agent myself"
  ```

### 3. Recom.Action → ActionPlan.recommended_action
- Extraction: Use head item (first element)
- Example:
  ```
  ["Dinner leader book nearly", "Cause onto beat debate listen test"]
  → "Dinner leader book nearly"
  ```

### 4. Immd. Contain. Action or Comments → ActionPlan.immediate_containment
- Extraction: Use head item (first element)
- Example:
  ```
  ["Their film job worker", "Effect action realize among short can ready"]
  → "Their film job worker"
  ```

## Field Distribution by Entity

| Entity | Field Count | Field % | Primary Raw Fields |
|--------|-------------|---------|-------------------|
| ActionRequest | 10 | 24.4% | 1-10 |
| Problem | 2 | 4.9% | 15-16 |
| RootCause | 2 | 4.9% | 17, 22 |
| ActionPlan | 11 | 26.8% | 18, 21, 23-31 |
| Verification | 4 | 9.8% | 38-41 |
| Department | 2 | 4.9% | 11-12 |
| Asset | 2 | 4.9% | 19, 37 |
| RecurringStatus | 2 | 4.9% | 13-14 |
| AmountOfLoss | 1 | 2.4% | 20 |
| Review | 4 | 9.8% | 32-35 |
| EquipmentStrategy | 1 | 2.4% | 36 |
| Facility | 0 | 0% | Container entity |
