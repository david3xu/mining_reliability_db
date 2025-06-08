// potential_root_causes.cypher
// Find potential root causes from similar symptom patterns
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
  ar.action_request_number IS NOT NULL AND
  f.facility_id IS NOT NULL AND
  p.what_happened IS NOT NULL AND
  rc.root_cause IS NOT NULL
WITH
  ar.action_request_number AS incident_id,
  f.facility_id AS facility,
  p.what_happened AS problem_description,
  rc.root_cause AS proven_solution,
  rc.root_cause_tail_extraction AS root_cause_details,
  ar.categories AS equipment_category,
  ar.initiation_date AS initiation_date
WHERE
  incident_id IS NOT NULL AND
  facility IS NOT NULL AND
  problem_description IS NOT NULL AND
  proven_solution IS NOT NULL
RETURN
  incident_id,
  facility,
  problem_description,
  proven_solution,
  root_cause_details,
  equipment_category,
  count(*) AS frequency,
  max(initiation_date) AS latest_date
ORDER BY frequency DESC, latest_date DESC
LIMIT 10