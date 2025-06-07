// effective_actions_debug.cypher
// Debug query to check what Verification data exists

// First, let's see if we have any Verification nodes with is_action_plan_effective
MATCH (v:Verification)
WHERE v.is_action_plan_effective = true
RETURN count(v) AS effective_verifications_count
UNION
// Check all Verification nodes
MATCH (v:Verification)
RETURN count(v) AS total_verifications_count
UNION
// Check the property values
MATCH (v:Verification)
WHERE v.is_action_plan_effective IS NOT NULL
RETURN DISTINCT v.is_action_plan_effective AS effectiveness_values, count(*) AS count
UNION
// Check the full path availability
MATCH (ar:ActionRequest)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
RETURN count(*) AS full_path_count
UNION
// Check with filter for "leak"
MATCH (ar:ActionRequest)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE (ar.action_request_number CONTAINS "leak" OR
       ar.equipment_id CONTAINS "leak" OR
       p.what_happened CONTAINS "leak" OR
       ap.action_plan CONTAINS "leak")
RETURN count(*) AS filtered_path_count
