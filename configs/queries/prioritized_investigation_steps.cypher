// prioritized_investigation_steps.cypher
// Prioritize investigation steps based on successful root cause identification patterns
MATCH
  (ar:ActionRequest)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
WITH
  p.what_happened AS symptoms,
  rc.root_cause AS root_cause,
  split(ap.action_plan, '|') AS investigation_steps,
  rc.objective_evidence AS evidence_type
UNWIND investigation_steps AS step
WITH
  trim(step) AS investigation_step,
  root_cause,
  evidence_type,
  symptoms,
  count(*) AS step_frequency
WHERE investigation_step <> "" AND size(investigation_step) > 10
RETURN
  investigation_step,
  step_frequency,
  collect(DISTINCT left(root_cause, 60)) AS root_causes_found,
  collect(DISTINCT left(evidence_type, 40)) AS evidence_types
ORDER BY step_frequency DESC
LIMIT 6