// investigation_approaches.cypher
// Find investigation methods that led to successful root cause identification
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(facility:Facility)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}
  AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
WITH ar.action_request_number AS incident_id,
     facility.facility_id AS facility,
     p.what_happened AS symptoms,
     rc.root_cause AS identified_cause,
     ap.action_plan AS investigation_approach,
     ar.comments AS investigation_comments,
     rc.objective_evidence AS evidence_found,
     ar.initiation_date AS initiation_date
WHERE investigation_approach IS NOT NULL
RETURN incident_id,
       facility,
       symptoms,
       identified_cause,
       investigation_approach,
       investigation_comments,
       evidence_found,
       initiation_date
ORDER BY initiation_date DESC
LIMIT 8
