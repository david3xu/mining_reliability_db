#!/bin/bash
# priority_analysis.sh

CONTAINER="neo4j-container"
USER="neo4j"
PASSWORD="password"

echo "=== EXCAVATOR-1020 IMMEDIATE ANALYSIS ==="

# Critical Question: Which facility handles contamination best?
echo "1. FACILITY EXPERTISE RANKING:"
docker exec -it $CONTAINER cypher-shell -u $USER -p $PASSWORD "
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE toLower(p.what_happened) CONTAINS 'excavator'
  AND toLower(p.what_happened) CONTAINS 'contamination'
WITH f.facility_id as facility, count(*) as cases,
     count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) as successful
RETURN facility, successful, cases, round(toFloat(successful)*100/cases,1) as rate
ORDER BY rate DESC
"

echo ""
echo "2. CONTAMINATION ROOT CAUSES:"
docker exec -it $CONTAINER cypher-shell -u $USER -p $PASSWORD "
MATCH (rc:RootCause)-[:ANALYZES]->(p:Problem)
WHERE toLower(p.what_happened) CONTAINS 'particles' OR toLower(rc.root_cause) CONTAINS 'contamination'
RETURN rc.root_cause, count(*) as frequency
ORDER BY frequency DESC LIMIT 5
"

echo ""
echo "3. PROVEN SOLUTIONS:"
docker exec -it $CONTAINER cypher-shell -u $USER -p $PASSWORD "
MATCH (ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE toLower(ap.action_plan) CONTAINS 'motor' AND v.is_action_plan_effective = true
RETURN ap.action_plan, count(*) as success_count
ORDER BY success_count DESC LIMIT 5
"
