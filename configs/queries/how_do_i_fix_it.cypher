// how_do_i_fix_it.cypher
// Find proven action plans that successfully resolved similar symptoms
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE
  {filter_clause}AND
  COALESCE(v.is_action_plan_effective, "No") = "Yes" AND
  ap.complete = "Yes"
WITH
  ar.action_request_number AS incident_id,
  f.facility_id AS facility,
  p.what_happened AS similar_symptoms,
  rc.root_cause AS root_cause_addressed,
  ap.action_plan AS proven_solution,
  ap.immd_contain_action_or_comments AS immediate_actions,
  v.action_plan_eval_comment AS effectiveness_proof,
  ap.completion_date AS solution_timeline,
  ar.title AS incident_context,
  ar.initiation_date AS incident_date
RETURN
  incident_id,
  facility,
  similar_symptoms,
  root_cause_addressed,
  proven_solution,
  immediate_actions,
  effectiveness_proof,
  solution_timeline,
  incident_context,
  incident_date
ORDER BY incident_date DESC
LIMIT 8