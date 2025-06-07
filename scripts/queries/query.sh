#!/bin/bash

# Configuration
CONTAINER="neo4j-container"  # Replace with your container name
USER="neo4j"
PASSWORD="your-password"     # Replace with your password
RESULTS_DIR="./excavator_analysis"

# Create results directory
mkdir -p $RESULTS_DIR

# Execute function
execute_query() {
    local query="$1"
    local output_file="$2"

    echo "Executing: $output_file"
    docker exec -it $CONTAINER cypher-shell -u $USER -p $PASSWORD \
        --format csv "$query" > "$RESULTS_DIR/$output_file"
}

# Core Investigation Queries
echo "=== EXCAVATOR CONTAMINATION INVESTIGATION ==="

# 1. Exact Pattern Matching
execute_query "
MATCH (p:Problem)-[:IDENTIFIED_IN]->(ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
WHERE toLower(p.what_happened) CONTAINS 'excavator'
  AND toLower(p.what_happened) CONTAINS 'motor'
  AND (toLower(p.what_happened) CONTAINS 'swing' OR toLower(p.what_happened) CONTAINS 'contamination')
OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
RETURN ar.action_request_number, ar.initiation_date, p.what_happened, rc.root_cause, f.facility_id
ORDER BY ar.initiation_date DESC LIMIT 15
" "01_excavator_motor_incidents.csv"

# 2. Contamination Source Analysis
execute_query "
MATCH (rc:RootCause)-[:ANALYZES]->(p:Problem)
WHERE toLower(rc.root_cause) CONTAINS 'particles'
   OR toLower(rc.root_cause) CONTAINS 'contamination'
   OR toLower(rc.root_cause) CONTAINS 'metal'
RETURN rc.root_cause, rc.root_cause_tail_extraction, count(*) as frequency
ORDER BY frequency DESC
" "02_contamination_sources.csv"

# 3. Facility Expertise Analysis
execute_query "
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE toLower(p.what_happened) CONTAINS 'excavator'
  AND (toLower(p.what_happened) CONTAINS 'contamination' OR toLower(rc.root_cause) CONTAINS 'contamination')
WITH f.facility_id as facility, count(*) as total_cases,
     count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) as successful_resolutions
WHERE total_cases >= 1
RETURN facility, successful_resolutions, total_cases,
       round(toFloat(successful_resolutions) * 100 / total_cases, 1) as expertise_rate
ORDER BY expertise_rate DESC
" "03_facility_expertise.csv"

# 4. Solution Effectiveness
execute_query "
MATCH (ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
MATCH (ap)-[:RESOLVES]->(rc:RootCause)-[:ANALYZES]->(p:Problem)
WHERE toLower(p.what_happened) CONTAINS 'contamination'
WITH CASE
  WHEN toLower(ap.action_plan) CONTAINS 'replace' THEN 'Component Replacement'
  WHEN toLower(ap.action_plan) CONTAINS 'clean' THEN 'System Cleaning'
  WHEN toLower(ap.action_plan) CONTAINS 'flush' THEN 'System Flushing'
  ELSE 'Other Approach'
END as solution_approach, v.is_action_plan_effective as effective
WITH solution_approach, count(*) as total_attempts,
     count(CASE WHEN effective = true THEN 1 END) as successful_attempts
WHERE total_attempts >= 2
RETURN solution_approach, successful_attempts, total_attempts,
       round(toFloat(successful_attempts) * 100 / total_attempts, 1) as success_rate
ORDER BY success_rate DESC
" "04_solution_effectiveness.csv"

# 5. Downtime Impact Analysis
execute_query "
MATCH (ar:ActionRequest)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
WHERE p.what_happened =~ '.*([0-9]+\\.?[0-9]*)\\s*(day|days).*'
RETURN ar.action_request_number, p.what_happened, ar.categories, ar.initiation_date
ORDER BY ar.initiation_date DESC
" "05_downtime_incidents.csv"

echo "=== ANALYSIS COMPLETE ==="
echo "Results saved to: $RESULTS_DIR/"
ls -la $RESULTS_DIR/
