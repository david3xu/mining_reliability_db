// Find proven excavator motor contamination solutions
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}
  AND v.is_action_plan_effective = true
RETURN ar.action_request_number AS incident_id,
       p.what_happened AS problem_description,
       rc.root_cause AS contamination_cause,
       ap.action_plan AS proven_solution,
       v.action_plan_eval_comment AS outcome_validation,
       f.facility_id AS success_location
ORDER BY ar.initiation_date DESC
LIMIT 10
