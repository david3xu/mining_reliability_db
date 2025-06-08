// who_can_help_me.cypher
// Find departments with proven success for similar symptoms
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:ASSIGNED_TO]-(d:Department)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
WITH
  d.init_dept AS initiating_department,
  d.rec_dept AS receiving_department,
  f.facility_id AS facility,
  ar.operating_centre AS location,
  p.what_happened AS handled_symptoms,
  count(*) AS success_cases,
  count(
    CASE
      WHEN v.is_action_plan_effective = "Yes" THEN 1
    END) AS effective_solutions,
  collect(DISTINCT left(rc.root_cause, 60)) AS expertise_areas
WHERE success_cases >= 1
RETURN
  initiating_department,
  receiving_department,
  facility,
  location,
  effective_solutions,
  success_cases,
  round(toFloat(effective_solutions) * 100 / success_cases, 1) AS success_rate,
  expertise_areas
ORDER BY success_rate DESC, success_cases DESC
LIMIT 5