// why_did_this_happen.cypher
// Find root causes from similar historical symptoms
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
WITH
  ar.action_request_number AS incident_id,
  f.facility_id AS facility,
  p.what_happened AS similar_symptoms,
  rc.root_cause AS identified_root_cause,
  rc.root_cause_tail_extraction AS additional_details,
  ar.categories AS equipment_category,
  ar.initiation_date AS incident_date,
  count(*) AS pattern_frequency
RETURN
  incident_id,
  facility,
  similar_symptoms,
  identified_root_cause,
  additional_details,
  equipment_category,
  pattern_frequency,
  incident_date
ORDER BY pattern_frequency DESC, incident_date DESC
LIMIT 8