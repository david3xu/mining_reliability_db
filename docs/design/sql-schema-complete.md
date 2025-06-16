# Mining Reliability Database: Simple SQL Schema

## Clean Normalized Schema - No Duplicates

Simple, properly normalized database schema with foreign key relationships instead of duplicating fields.

---

## 1. ActionRequest Table (Main Table)

```sql
CREATE TABLE ActionRequest (
    id INT IDENTITY(1,1) PRIMARY KEY,
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

    -- Unique constraint for facility + action request
    UNIQUE (facility_name, action_request_number)
);
```

---

## 2. Department Table

```sql
CREATE TABLE Department (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    init_dept VARCHAR(100),
    rec_dept VARCHAR(100),

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 3. Problem Table

```sql
CREATE TABLE Problem (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    what_happened TEXT,
    requirement TEXT,

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 4. RootCause Table

```sql
CREATE TABLE RootCause (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    objective_evidence TEXT,
    root_cause TEXT,

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 5. ActionPlan Table

```sql
CREATE TABLE ActionPlan (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    recommended_action TEXT,
    immediate_containment TEXT,
    action_plan TEXT,
    due_date DATE,
    complete BIT,
    completion_date DATE,
    comments TEXT,
    response_date DATE,
    response_revision_date DATE,
    did_plan_require_strategy_change BIT,
    are_there_corrective_actions_to_update BIT,

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 6. Review Table

```sql
CREATE TABLE Review (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    is_resp_satisfactory BIT,
    reason_if_not_satisfactory TEXT,
    reviewed_date DATE,
    did_plan_require_change_review BIT,

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 7. Verification Table

```sql
CREATE TABLE Verification (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    effectiveness_verification_due_date DATE,
    is_action_plan_effective BIT,
    action_plan_eval_comment TEXT,
    action_plan_verification_date DATE,

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 8. Asset Table

```sql
CREATE TABLE Asset (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    asset_numbers VARCHAR(100),
    asset_activity_numbers VARCHAR(100),

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 9. RecurringStatus Table

```sql
CREATE TABLE RecurringStatus (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    recurring_problems BIT,
    recurring_comment TEXT,

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 10. AmountOfLoss Table

```sql
CREATE TABLE AmountOfLoss (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    amount_of_loss VARCHAR(100),

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## 11. EquipmentStrategy Table

```sql
CREATE TABLE EquipmentStrategy (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_request_id INT NOT NULL,
    apss_doc_number VARCHAR(100),

    FOREIGN KEY (action_request_id) REFERENCES ActionRequest(id)
);
```

---

## Quick Setup Script

```sql
-- Create all tables in order (run these statements in sequence)

-- Sample data insert
INSERT INTO ActionRequest (facility_name, action_request_number, title, initiation_date)
VALUES ('Mine_A', 'AR-2025-001', 'Sample Action Request', '2025-06-14');

INSERT INTO ActionPlan (action_request_id, action_plan, due_date)
VALUES (1, 'Fix equipment issue', '2025-07-01');

-- Simple query example
SELECT ar.facility_name, ar.action_request_number, ar.title, ap.action_plan
FROM ActionRequest ar
LEFT JOIN ActionPlan ap ON ar.id = ap.action_request_id
WHERE ar.facility_name = 'Mine_A';
```

## Clean Design Benefits

- **No Duplication**: `facility_name` and `action_request_number` only stored once in ActionRequest
- **Simple Foreign Keys**: All child tables use single `action_request_id` reference
- **Proper Normalization**: Eliminates redundant data storage
- **Easy Joins**: Standard `id` relationships for simple queries
- **Data Integrity**: Foreign key constraints maintain relationships
- **All 41 Fields**: Complete coverage of original requirements + facility_name
