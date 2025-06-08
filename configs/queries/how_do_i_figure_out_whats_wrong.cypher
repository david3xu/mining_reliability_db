// how_do_i_figure_out_whats_wrong.cypher
// Find investigation approaches that led to successful diagnosis
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
  p.what_happened AS symptoms,
  rc.root_cause AS identified_cause,
  ar.comments AS investigation_comments,
  rc.objective_evidence AS evidence_found,
  ap.recom_action AS recommended_investigation,
  ar.initiation_date AS incident_date
WHERE investigation_comments IS NOT NULL OR evidence_found IS NOT NULL
RETURN
  incident_id,
  facility,
  symptoms,
  identified_cause,
  investigation_comments,
  evidence_found,
  recommended_investigation,
  incident_date
ORDER BY incident_date DESC
LIMIT 6