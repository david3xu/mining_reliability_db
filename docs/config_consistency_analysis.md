# Configuration Consistency Analysis Report

## Overview

This report analyzes inconsistencies between `model_schema.json` and `field_mappings.json` configuration files in the mining reliability database system.

## Status: RESOLVED ✅

**UPDATE (June 1, 2025)**: Configuration consistency issues have been systematically resolved through comprehensive alignment of both configuration files.

### Changes Applied:

1. ✅ **Added Missing Facility Configuration** to field_mappings.json
2. ✅ **Aligned Required Fields** - Added business field requirements to model_schema.json
3. ✅ **Fixed Dynamic Labeling Order** - Prioritized text fields over boolean fields for better Neo4j labels
4. ✅ **Field Name Consistency** - Resolved mapping inconsistencies

## Key Findings

### 1. Required Fields Mismatch

**CRITICAL ISSUE**: There's a fundamental inconsistency in how required fields are defined between the two files.

#### model_schema.json Required Fields Pattern:

- **Primary Keys**: All entities have `required: true` for their primary key fields
- **Foreign Keys**: All entities have `required: true` for their foreign key relationship fields
- **Business Logic Fields**: Only a few specific fields marked as required:
  - `ActionRequest`: facility_id, action_request_number
  - `RootCause`: root_cause
  - `Facility`: facility_name

#### field_mappings.json Required Fields Pattern:

- **Every entity** has exactly ONE required field in `required_fields` array
- These are business/functional requirements, not technical database constraints
- Pattern suggests required fields for data processing/validation, not database schema

### 2. Entity-by-Entity Analysis

#### ActionRequest

- **Schema**: `actionrequest_id`, `facility_id`, `action_request_number` (required)
- **Mappings**: `["Action Request Number:"]` (required)
- ✅ **ALIGNED**: Both consider action_request_number essential

#### Problem

- **Schema**: `problem_id`, `actionrequest_id`, `what_happened` (required)
- **Mappings**: `["What happened?"]` (required)
- ✅ **ALIGNED**: Both require what_happened field

#### RootCause

- **Schema**: `rootcause_id`, `problem_id`, `root_cause` (required)
- **Mappings**: `["Root Cause"]` (required)
- ✅ **ALIGNED**: Both consider root_cause essential

#### ActionPlan

- **Schema**: `actionplan_id`, `rootcause_id`, `action_plan` (required)
- **Mappings**: `["Action Plan"]` (required)
- ✅ **ALIGNED**: Both require action_plan field
- ❌ **MISALIGNED**: Schema has no business field requirements, mappings requires action_plan

#### Verification

- **Schema**: `verification_id`, `actionplan_id` (required)
- **Mappings**: `["IsActionPlanEffective"]` (required)
- ❌ **MISALIGNED**: Schema has no business field requirements, mappings requires boolean field

#### Other Entities (Department, Asset, RecurringStatus, AmountOfLoss, Review, EquipmentStrategy)

- **Schema**: Only ID and foreign key fields required
- **Mappings**: Each has one business field required
- ❌ **MISALIGNED**: Schema lacks business field requirements

### 3. Dynamic Labeling Inconsistencies

#### Field Name Mapping Issues:

Several field names in `cascade_priority` don't match the `entity_mappings`:

1. **Verification Entity**:

   - Schema: `cascade_priority: ["action_plan_eval_comment", "is_action_plan_effective"]`
   - Mappings: `label_priority: ["IsActionPlanEffective", "Action Plan Eval Comment"]`
   - ❌ **ORDER MISMATCH**: Schema prioritizes comment first, mappings prioritizes boolean first

2. **Field Name Inconsistencies**:
   - Schema uses `is_action_plan_effective` → Mappings maps to `"IsActionPlanEffective"`
   - Schema uses `action_plan_eval_comment` → Mappings maps to `"Action Plan Eval Comment"`

### 4. Missing Entity in field_mappings.json

- **Facility** entity is defined in model_schema.json but **completely missing** from field_mappings.json
- This breaks the cascade labeling system for Facility entities

## Impact Assessment

### High Priority Issues:

1. **Missing Facility Configuration**: Will cause runtime errors in cascade labeling
2. **Required Fields Philosophy Mismatch**: Different purposes - schema for DB constraints vs mappings for business validation
3. **Dynamic Labeling Order Conflicts**: May produce incorrect Neo4j labels

### Medium Priority Issues:

1. **Field Naming Inconsistencies**: Could cause mapping failures
2. **Business Logic Gaps**: Some entities lack business field requirements in schema

## Recommended Actions

### Immediate Fixes (Critical):

1. **Add Facility to field_mappings.json**:

```json
"Facility": {
  "label_priority": ["Facility Name", "Location"],
  "required_fields": ["Facility Name"],
  "entity_type": "Facility"
}
```

2. **Add Facility entity mappings**:

```json
"Facility": {
  "facility_name": "Facility Name",
  "location": "Location",
  "active": "Active"
}
```

### Alignment Strategy:

#### Option A: Align model_schema.json to field_mappings.json

Add `required: true` to business fields identified in field_mappings.json:

- Problem: `what_happened`
- ActionPlan: `action_plan`
- Verification: `is_action_plan_effective`
- Department: `init_dept`
- Asset: `asset_numbers`
- RecurringStatus: `recurring_problems`
- AmountOfLoss: `amount_of_loss`
- Review: `is_resp_satisfactory`
- EquipmentStrategy: `apss_doc_number`

#### Option B: Align field_mappings.json to model_schema.json

Reduce required_fields to only those marked as required in schema:

- ActionRequest: `["Action Request Number:"]` ✅ (already aligned)
- RootCause: `["Root Cause"]` ✅ (already aligned)
- All others: Remove business field requirements or make them optional

#### Option C: Dual-Purpose Configuration

Maintain both sets of requirements with clear documentation:

- Schema requirements = Database constraints
- Mapping requirements = Business validation rules

## Recommendation: Option A + Documentation

1. **Immediate**: Add missing Facility configuration
2. **Short-term**: Align schema to include business field requirements
3. **Long-term**: Document the dual nature of requirements (DB vs Business)

This ensures data integrity at both database and business logic levels while maintaining the flexibility of the current cascade labeling system.
