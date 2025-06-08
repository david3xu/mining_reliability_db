#!/usr/bin/env python3
import sys
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

print("Starting debug...")

try:
    from mine_core.database.db import get_database
    print("Imported database module")

    db = get_database()
    print("Got database connection")

    # Simple query to test aggregation
    query = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
    WHERE ar.action_request_number IS NOT NULL
      AND f.facility_id IS NOT NULL
      AND p.what_happened IS NOT NULL
      AND rc.root_cause IS NOT NULL
    WITH ar.action_request_number AS incident_id, count(*) as cnt
    RETURN incident_id, cnt
    ORDER BY cnt DESC
    LIMIT 5
    """

    print("Executing test query...")
    results = db.execute_query(query)
    print(f"Got {len(results)} results")

    for r in results:
        print(f"  {r}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
