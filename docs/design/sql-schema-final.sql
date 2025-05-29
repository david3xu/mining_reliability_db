-- Mining Reliability Database: SQL Schema
-- Direct implementation for 12-entity model

-- =====================================================
-- CORE ENTITIES - Hierarchical Chain
-- =====================================================

-- Facility - Root entity
CREATE TABLE Facility (
    facility_id INTEGER PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    active BOOLEAN DEFAULT true
);

-- ActionRequest - Incident tracking entity
CREATE TABLE ActionRequest (
    action_request_id INTEGER PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    action_request_number VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    initiation_date DATE NOT NULL,
    action_types VARCHAR(100),
    categories VARCHAR(100),
    requested_response_time VARCHAR(50),
    stage VARCHAR(100),
    operating_centre VARCHAR(50),
    past_due_status VARCHAR(50),
    days_past_due INTEGER,
    CONSTRAINT fk_facility
        FOREIGN KEY (facility_id) REFERENCES Facility(facility_id),
    CONSTRAINT uq_action_request
        UNIQUE (facility_id, action_request_number)
);

-- Problem - Issue description entity
CREATE TABLE Problem (
    problem_id INTEGER PRIMARY KEY,
    action_request_id INTEGER NOT NULL,
    what_happened TEXT NOT NULL,
    requirement TEXT,
    CONSTRAINT fk_action_request
        FOREIGN KEY (action_request_id) REFERENCES ActionRequest(action_request_id)
);

-- RootCause - Analysis entity
CREATE TABLE RootCause (
    cause_id INTEGER PRIMARY KEY,
    problem_id INTEGER NOT NULL,
    -- List field handling: uses tail (second) item when available
    root_cause TEXT NOT NULL,
    -- List field handling: uses head (first) item
    objective_evidence TEXT,
    CONSTRAINT fk_problem
        FOREIGN KEY (problem_id) REFERENCES Problem(problem_id)
);

-- ActionPlan - Resolution entity
CREATE TABLE ActionPlan (
    plan_id INTEGER PRIMARY KEY,
    root_cause_id INTEGER NOT NULL,
    -- List field handling: uses head (first) item
    action_plan TEXT NOT NULL,
    -- List field handling: uses head (first) item
    recommended_action TEXT,
    -- List field handling: uses head (first) item
    immediate_containment TEXT,
    due_date DATE,
    complete BOOLEAN DEFAULT false,
    completion_date DATE,
    comments TEXT,
    response_date DATE,
    response_revision_date DATE,
    did_plan_require_strategy_change BOOLEAN DEFAULT false,
    are_there_corrective_actions_to_update BOOLEAN DEFAULT false,
    CONSTRAINT fk_root_cause
        FOREIGN KEY (root_cause_id) REFERENCES RootCause(cause_id)
);

-- Verification - Effectiveness assessment entity
CREATE TABLE Verification (
    verification_id INTEGER PRIMARY KEY,
    action_plan_id INTEGER NOT NULL,
    effectiveness_verification_due_date DATE,
    is_action_plan_effective BOOLEAN,
    action_plan_eval_comment TEXT,
    action_plan_verification_date DATE,
    CONSTRAINT fk_action_plan
        FOREIGN KEY (action_plan_id) REFERENCES ActionPlan(plan_id)
);

-- =====================================================
-- SUPPORT ENTITIES
-- =====================================================

-- Department - Organizational assignment tracking
CREATE TABLE Department (
    dept_id INTEGER PRIMARY KEY,
    action_request_id INTEGER NOT NULL,
    init_dept VARCHAR(100),
    rec_dept VARCHAR(100),
    CONSTRAINT fk_action_request
        FOREIGN KEY (action_request_id) REFERENCES ActionRequest(action_request_id)
);

-- Asset - Equipment identification
CREATE TABLE Asset (
    asset_id INTEGER PRIMARY KEY,
    problem_id INTEGER NOT NULL,
    asset_numbers VARCHAR(100),
    asset_activity_numbers VARCHAR(100),
    CONSTRAINT fk_problem
        FOREIGN KEY (problem_id) REFERENCES Problem(problem_id)
);

-- RecurringStatus - Pattern classification
CREATE TABLE RecurringStatus (
    recurring_id INTEGER PRIMARY KEY,
    problem_id INTEGER NOT NULL,
    recurring_problems BOOLEAN DEFAULT false,
    recurring_comment TEXT,
    CONSTRAINT fk_problem
        FOREIGN KEY (problem_id) REFERENCES Problem(problem_id)
);

-- AmountOfLoss - Financial impact
CREATE TABLE AmountOfLoss (
    loss_id INTEGER PRIMARY KEY,
    problem_id INTEGER NOT NULL,
    amount_of_loss VARCHAR(100),
    CONSTRAINT fk_problem
        FOREIGN KEY (problem_id) REFERENCES Problem(problem_id)
);

-- Review - Quality evaluation
CREATE TABLE Review (
    review_id INTEGER PRIMARY KEY,
    action_plan_id INTEGER NOT NULL,
    is_resp_satisfactory BOOLEAN,
    reason_if_not_satisfactory TEXT,
    reviewed_date DATE,
    did_plan_require_change_review BOOLEAN DEFAULT false,
    CONSTRAINT fk_action_plan
        FOREIGN KEY (action_plan_id) REFERENCES ActionPlan(plan_id)
);

-- EquipmentStrategy - System documentation
CREATE TABLE EquipmentStrategy (
    strategy_id INTEGER PRIMARY KEY,
    action_plan_id INTEGER NOT NULL,
    apss_doc_number VARCHAR(100),
    CONSTRAINT fk_action_plan
        FOREIGN KEY (action_plan_id) REFERENCES ActionPlan(plan_id)
);

-- =====================================================
-- LIST FIELD HANDLING (Implementation Note)
-- =====================================================

/*
-- List field extraction logic:
function extractListValue(fieldName, values) {
    if (!Array.isArray(values) || values.length === 0) {
        return null;
    }
    
    if (fieldName === 'Root Cause' && values.length > 1) {
        return values[1];  // Return tail (second) item for Root Cause
    }
    
    return values[0];  // Return head (first) item for all other fields
}
*/