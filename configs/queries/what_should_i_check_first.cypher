// what_should_i_check_first.cypher
// Prioritize investigation steps based on success patterns
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
WITH
  p.what_happened AS symptoms,
  rc.root_cause AS root_cause,
  split(ap.action_plan, '|') AS action_steps,
  rc.objective_evidence AS evidence_type,
  ap.recom_action AS immediate_action
UNWIND action_steps AS step
WITH
  trim(step) AS investigation_step,
  root_cause,
  evidence_type,
  immediate_action,
  symptoms,
  count(*) AS step_frequency
WHERE investigation_step <> "" AND size(investigation_step) > 15
RETURN
  investigation_step,
  step_frequency,
  immediate_action,
  collect(DISTINCT left(root_cause, 50)) AS root_causes_found,
  collect(DISTINCT left(evidence_type, 30)) AS evidence_types
ORDER BY step_frequency DESC
LIMIT 8