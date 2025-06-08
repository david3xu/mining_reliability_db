// Find proven solutions with comprehensive success validation
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}
WITH
  ar,
  f,
  p,
  rc,
  ap,
  v,
  CASE
    WHEN
      v.is_action_plan_effective = true OR v.is_action_plan_effective = "Yes"
      THEN 1
    ELSE 0
  END AS effectiveness_score
RETURN
  ar.action_request_number AS incident_id,
  f.facility_id AS facility,
  p.what_happened AS problem_description,
  rc.root_cause AS root_cause_details,
  ap.action_plan AS proven_solution,
  COALESCE(v.action_plan_eval_comment, 'Pending verification') AS solution_outcome,
  effectiveness_score AS verified_effective,
  CASE
    WHEN effectiveness_score = 1 THEN "Verified Effective"
    WHEN v.is_action_plan_effective IS NOT NULL THEN "Tested - Mixed Results"
    ELSE "Pending Verification"
  END AS success_status,
  ar.initiation_date AS implementation_date
ORDER BY effectiveness_score DESC, ar.initiation_date DESC
LIMIT 10