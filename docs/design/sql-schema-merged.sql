-- Mining Reliability Database: Direct Field Mapping Schema
-- Simple approach - original 41 fields + facility_name

-- =====================================================
-- ENTITY RELATIONSHIP DIAGRAM (TEXT FORMAT)
-- =====================================================

/*
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          MINING RELIABILITY DATABASE SCHEMA                     │
│                                5-Table Design                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│      ActionRequest       │
│─────────────────────────│
│ ◉ id (PK)               │
│ • facility_name         │
│ • action_request_number │
│ • title                 │
│ • initiation_date       │
│ • action_types          │
│ • categories            │
│ • requested_response_time│
│ • past_due_status       │
│ • days_past_due         │
│ • operating_centre      │
│ • stage                 │
│ • init_dept             │
│ • rec_dept              │
└──────────────────────────┘
│
│ 1:1
▼
┌──────────────────────────┐
│        Problem           │
│─────────────────────────│
│ ◉ id (PK)               │
│ ◆ action_request_id (FK)│
│ • recurring_problems    │
│ • recurring_comment     │
│ • what_happened         │
│ • requirement           │
│ • objective_evidence    │
│ • recommended_action    │
│ • asset_numbers         │
│ • amount_of_loss        │
│ • immediate_containment │
│ • root_cause            │
└──────────────────────────┘

┌─────────────────┼─────────────────┐
│ 1:1             │ 1:1             │ 1:1
▼                 ▼                 ▼
┌─────────────────────┐ ┌─────────────────┐ ┌──────────────────────┐
│     ActionPlan      │ │      Review     │ │     Verification     │
│────────────────────│ │────────────────│ │─────────────────────│
│ ◉ id (PK)          │ │ ◉ id (PK)      │ │ ◉ id (PK)           │
│ ◆ action_request_id│ │ ◆ action_req_id│ │ ◆ action_request_id │
│ • action_plan      │ │ • is_resp_sat  │ │ • effect_verif_date │
│ • due_date         │ │ • reason_if_not│ │ • is_plan_effective │
│ • complete         │ │ • reviewed_date│ │ • plan_eval_comment │
│ • completion_date  │ │ • plan_req_chg │ │ • plan_verif_date   │
│ • comments         │ │ • apss_doc_num │ └──────────────────────┘
│ • response_date    │ │ • asset_act_num│
│ • response_rev_date│ └─────────────────┘
│ • plan_req_strategy│
│ • corrective_act   │
└─────────────────────┘

LEGEND:
◉ Primary Key (PK)
◆ Foreign Key (FK)
• Regular Field
│ One-to-One Relationship
▼ Relationship Direction

WORKFLOW FLOW:
ActionRequest → Problem → (ActionPlan + Review + Verification)

UNIQUE CONSTRAINT:
ActionRequest: (facility_name, action_request_number) UNIQUE
*/

-- =====================================================
-- DIRECT MAPPING FROM 41 FIELDS + FACILITY_NAME
-- =====================================================

-- ActionRequest - Fields 1-12 + facility_name
CREATE TABLE ActionRequest (
    id INTEGER PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL,
    action_request_number VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    initiation_date DATE,
    action_types VARCHAR(100),
    categories VARCHAR(100),
    requested_response_time VARCHAR(50),
    past_due_status VARCHAR(50),
    days_past_due INTEGER,
    operating_centre VARCHAR(50),
    stage VARCHAR(100),
    init_dept VARCHAR(100),
    rec_dept VARCHAR(100),
    UNIQUE (
        facility_name,
        action_request_number
    )
);

-- Problem - Fields 13-22 (what happened, root cause analysis)
CREATE TABLE Problem (
    id INTEGER PRIMARY KEY,
    action_request_id INTEGER NOT NULL,
    recurring_problems BOOLEAN,
    recurring_comment TEXT,
    what_happened TEXT,
    requirement TEXT,
    objective_evidence TEXT,
    recommended_action TEXT,
    asset_numbers VARCHAR(100),
    amount_of_loss VARCHAR(100),
    immediate_containment TEXT,
    root_cause TEXT,
    FOREIGN KEY (action_request_id) REFERENCES ActionRequest (id)
);

-- ActionPlan - Fields 23-31 (action planning and execution)
CREATE TABLE ActionPlan (
    id INTEGER PRIMARY KEY,
    action_request_id INTEGER NOT NULL,
    action_plan TEXT,
    due_date DATE,
    complete BOOLEAN,
    completion_date DATE,
    comments TEXT,
    response_date DATE,
    response_revision_date DATE,
    did_plan_require_strategy_change BOOLEAN,
    are_there_corrective_actions_to_update BOOLEAN,
    FOREIGN KEY (action_request_id) REFERENCES ActionRequest (id)
);

-- Review - Fields 32-37 (review and strategy documentation)
CREATE TABLE Review (
    id INTEGER PRIMARY KEY,
    action_request_id INTEGER NOT NULL,
    is_resp_satisfactory BOOLEAN,
    reason_if_not_satisfactory TEXT,
    reviewed_date DATE,
    did_plan_require_change_review BOOLEAN,
    apss_doc_number VARCHAR(100),
    asset_activity_numbers VARCHAR(100),
    FOREIGN KEY (action_request_id) REFERENCES ActionRequest (id)
);

-- Verification - Fields 38-41 (effectiveness verification)
CREATE TABLE Verification (
    id INTEGER PRIMARY KEY,
    action_request_id INTEGER NOT NULL,
    effectiveness_verification_due_date DATE,
    is_action_plan_effective BOOLEAN,
    action_plan_eval_comment TEXT,
    action_plan_verification_date DATE,
    FOREIGN KEY (action_request_id) REFERENCES ActionRequest (id)
);

-- =====================================================
-- FIELD MAPPING REFERENCE
-- =====================================================

/*
ActionRequest Table:
- facility_name (NEW FIELD)
1. Action Request Number: -> action_request_number
2. Title -> title
3. Initiation Date -> initiation_date
4. Action Types -> action_types
5. Categories -> categories
6. Requested Response Time -> requested_response_time
7. Past Due Status -> past_due_status
8. Days Past Due -> days_past_due
9. Operating Centre -> operating_centre
10. Stage -> stage
11. Init. Dept. -> init_dept
12. Rec. Dept. -> rec_dept

Problem Table:
13. Recurring Problem(s) -> recurring_problems
14. Recurring Comment -> recurring_comment
15. What happened? -> what_happened
16. Requirement -> requirement
17. Obj. Evidence -> objective_evidence
18. Recom.Action -> recommended_action
19. Asset Number(s) -> asset_numbers
20. Amount of Loss -> amount_of_loss
21. Immd. Contain. Action or Comments -> immediate_containment
22. Root Cause -> root_cause

ActionPlan Table:
23. Action Plan -> action_plan
24. Due Date -> due_date
25. Complete -> complete
26. Completion Date -> completion_date
27. Comments -> comments
28. Response Date -> response_date
29. Response Revision Date -> response_revision_date
30. Did this action plan require a change...? -> did_plan_require_strategy_change
31. If yes, are there any corrective actions...? -> are_there_corrective_actions_to_update

Review Table:
32. Is Resp Satisfactory? -> is_resp_satisfactory
33. Reason if not Satisfactory -> reason_if_not_satisfactory
34. Reviewed Date: -> reviewed_date
35. Did this action plan require a change...? (review) -> did_plan_require_change_review
36. If yes, APSS Doc # -> apss_doc_number
37. Asset Activity numbers -> asset_activity_numbers

Verification Table:
38. Effectiveness Verification Due Date -> effectiveness_verification_due_date
39. IsActionPlanEffective -> is_action_plan_effective
40. Action Plan Eval Comment -> action_plan_eval_comment
41. Action Plan Verification Date: -> action_plan_verification_date
*/

-- =====================================================
-- SAMPLE DATA & USAGE
-- =====================================================

-- Insert sample action request
INSERT INTO
    ActionRequest (
        facility_name,
        action_request_number,
        title,
        initiation_date,
        action_types,
        init_dept,
        rec_dept,
        stage
    )
VALUES (
        'Mine_A',
        'AR-2025-001',
        'Excavator Motor Failure',
        '2025-06-14',
        'Maintenance',
        'Operations',
        'Engineering',
        'In Progress'
    );

-- Insert problem details
INSERT INTO
    Problem (
        action_request_id,
        what_happened,
        root_cause,
        asset_numbers,
        amount_of_loss
    )
VALUES (
        1,
        'Motor failed during operation causing equipment shutdown',
        'Inadequate maintenance schedule',
        'EX-001, EX-002',
        '$50,000'
    );

-- Insert action plan
INSERT INTO
    ActionPlan (
        action_request_id,
        action_plan,
        due_date,
        complete
    )
VALUES (
        1,
        'Replace motor and update maintenance schedule',
        '2025-06-30',
        false
    );

-- Insert review
INSERT INTO
    Review (
        action_request_id,
        is_resp_satisfactory,
        reviewed_date
    )
VALUES (1, true, '2025-06-15');

-- Insert verification
INSERT INTO
    Verification (
        action_request_id,
        effectiveness_verification_due_date,
        is_action_plan_effective
    )
VALUES (1, '2025-07-15', true);

-- =====================================================
-- SIMPLE QUERIES
-- =====================================================

-- Get complete record
SELECT ar.facility_name, ar.action_request_number, ar.title, p.what_happened, p.root_cause, ap.action_plan, r.is_resp_satisfactory, v.is_action_plan_effective
FROM
    ActionRequest ar
    LEFT JOIN Problem p ON ar.id = p.action_request_id
    LEFT JOIN ActionPlan ap ON ar.id = ap.action_request_id
    LEFT JOIN Review r ON ar.id = r.action_request_id
    LEFT JOIN Verification v ON ar.id = v.action_request_id
WHERE
    ar.facility_name = 'Mine_A';

-- =====================================================
-- DESIGN NOTES
-- =====================================================

/*
SIMPLE 5-TABLE DESIGN:
1. ActionRequest - Core request info + departments (Fields 1-12 + facility_name)
2. Problem - What happened + root cause analysis (Fields 13-22)
3. ActionPlan - Action planning and execution (Fields 23-31)
4. Review - Review process and documentation (Fields 32-37)
5. Verification - Effectiveness verification (Fields 38-41)

ALL 41 ORIGINAL FIELDS + facility_name PRESERVED
Simple foreign key relationships - all reference ActionRequest.id
*/