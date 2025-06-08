// Find departments with excavator contamination expertise
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:ASSIGNED_TO]-(d:Department)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)<-[:VALIDATES]-
  (v:Verification)
WHERE {filter_clause}
WITH
  d.init_dept AS initiating_department,
  d.rec_dept AS receiving_department,
  f.facility_id AS facility,
  ar.action_request_number AS incident_id,
  ar.operating_centre AS location,
  count(*) AS contamination_cases,
  count(
    CASE
      WHEN v.is_action_plan_effective = true THEN 1
    END) AS successful_resolutions
WHERE contamination_cases >= 1
RETURN
  incident_id,
  initiating_department,
  receiving_department,
  facility,
  location,
  successful_resolutions,
  contamination_cases,
  round(toFloat(successful_resolutions) * 100 / contamination_cases, 1) AS success_rate
ORDER BY success_rate DESC, contamination_cases DESC