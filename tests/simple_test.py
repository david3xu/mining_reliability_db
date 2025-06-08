#!/usr/bin/env python3
print("Starting test...")

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

print("Imports completed...")

try:
    from mine_core.database.db import get_database
    print("Database import successful...")

    db_connection = get_database()
    print("Database connection created...")

    simple_query = "MATCH (n) RETURN count(n) as total_nodes LIMIT 1"
    result = db_connection.execute_query(simple_query)
    print(f"Simple query result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
