// diagnostic_experts.cypher
// Find departments experienced with investigating similar symptoms
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:ASSIGNED_TO]-(d:Department)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}
  AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
WITH d.init_dept AS initiating_department,
     f.facility_id AS facility,
     ar.operating_centre AS location,
     p.what_happened AS investigated_symptoms,
     rc.root_cause AS successfully_identified_cause,
     count(*) AS diagnostic_cases,
     count(CASE WHEN v.is_action_plan_effective = "Yes" THEN 1 END) AS successful_diagnoses
WHERE diagnostic_cases >= 1
RETURN initiating_department,
       facility,
       location,
       successful_diagnoses,
       diagnostic_cases,
       round(toFloat(successful_diagnoses) * 100 / diagnostic_cases, 1) AS diagnostic_success_rate,
       collect(DISTINCT left(successfully_identified_cause, 50)) AS root_cause_experience
ORDER BY diagnostic_success_rate DESC, diagnostic_cases DESC
LIMIT 5
