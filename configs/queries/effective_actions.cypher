// effective_actions.cypher
// Smart pattern discovery - finds proven solutions with intelligence layers
// Layer 1: Direct keyword matches (proven effective)
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(facility:Facility)
MATCH
  (ar)<-[:IDENTIFIED_IN]-
  (p:Problem)<-[:ANALYZES]-
  (rc:RootCause)<-[:RESOLVES]-
  (ap:ActionPlan)
OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
WHERE {filter_clause}AND COALESCE(v.is_action_plan_effective, "No") = "Yes"

WITH
  ar,
  p,
  rc,
  ap,
  v,
  facility,
  // Calculate relevance score
  100 AS base_score,
  CASE
    WHEN
      v.action_plan_eval_comment IS NOT NULL AND
      size(v.action_plan_eval_comment) > 30
      THEN 30
    WHEN v.action_plan_eval_comment IS NOT NULL THEN 15
    ELSE 5
  END AS rationale_score,
  CASE
    WHEN
      rc.objective_evidence IS NOT NULL AND size(rc.objective_evidence) > 20
      THEN 20
    WHEN rc.objective_evidence IS NOT NULL THEN 10
    ELSE 5
  END AS evidence_score

// Layer 2: Equipment category similarity (same equipment types)
OPTIONAL MATCH
  (ar)-[:BELONGS_TO]->(facility)<-[:BELONGS_TO]-(similar_ar:ActionRequest)
WHERE ar.categories = similar_ar.categories AND similar_ar <> ar
OPTIONAL MATCH
  (similar_ar)<-[:IDENTIFIED_IN]-
  (similar_p:Problem)<-[:ANALYZES]-
  (similar_rc:RootCause)<-[:RESOLVES]-
  (similar_ap:ActionPlan)
OPTIONAL MATCH (similar_ap)<-[:VALIDATES]-(similar_v:Verification)
WHERE COALESCE(similar_v.is_action_plan_effective, "No") = "Yes"

WITH
  ar,
  p,
  rc,
  ap,
  v,
  facility,
  base_score,
  rationale_score,
  evidence_score,
  count(similar_ar) AS equipment_matches

// Calculate final intelligence score
WITH
  ar,
  p,
  rc,
  ap,
  v,
  facility,
  rationale_score,
  evidence_score,
  equipment_matches,
  (100 + rationale_score + evidence_score + (equipment_matches * 5)) AS intelligence_score

RETURN
  ar.action_request_number AS incident_id,
  facility.facility_id AS facility,
  ap.action_plan AS effective_action,
  COALESCE(v.action_plan_eval_comment, 'Verified effective solution') AS why_effective,
  COALESCE(rc.objective_evidence, 'Technical validation available') AS supporting_evidence,
  p.what_happened AS problem_context,
  (1 + equipment_matches) AS usage_frequency,
  intelligence_score,
  CASE
    WHEN intelligence_score >= 140 THEN "High"
    WHEN intelligence_score >= 120 THEN "Medium"
    ELSE "Low"
  END AS confidence_level,
  CASE
    WHEN rationale_score >= 30 AND evidence_score >= 20 THEN "Strong"
    WHEN rationale_score >= 15 OR evidence_score >= 10 THEN "Moderate"
    ELSE "Limited"
  END AS evidence_quality,
  CASE
    WHEN equipment_matches > 0 THEN "Equipment Pattern"
    ELSE "Direct Match"
  END AS discovery_method
ORDER BY intelligence_score DESC, ar.initiation_date DESC
LIMIT 10