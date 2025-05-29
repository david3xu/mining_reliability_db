#!/usr/bin/env python3
"""
Database Reset Script for Mining Reliability Database
Cleans Neo4j database by removing all data and schema.
"""

import sys
import os
import logging
import argparse

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mine_core.database.db import get_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_database_stats(db):
    """Get current database statistics"""
    try:
        with db.session() as session:
            # Get node count by label
            label_results = []
            try:
                result = session.run("CALL db.labels() YIELD label RETURN collect(label) AS labels")
                label_results = result.single()["labels"]
            except Exception:
                pass

            node_stats = {}
            total_nodes = 0

            for label in label_results:
                try:
                    result = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS count")
                    count = result.single()["count"]
                    node_stats[label] = count
                    total_nodes += count
                except Exception:
                    pass

            if not node_stats:
                result = session.run("MATCH (n) RETURN count(n) AS count")
                total_nodes = result.single()["count"]

            # Count relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS count")
            rel_count = result.single()["count"]

            return {
                "nodes": node_stats,
                "total_nodes": total_nodes,
                "relationships": rel_count
            }

    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {"nodes": {}, "total_nodes": 0, "relationships": 0}

def delete_all_data(db, batch_size=5000):
    """Delete all nodes and relationships"""
    try:
        logger.info("Deleting all data...")

        with db.session() as session:
            deleted_rel_count = 0
            while True:
                result = session.run(f"""
                    MATCH ()-[r]->()
                    WITH r LIMIT {batch_size}
                    DELETE r
                    RETURN count(r) AS deleted
                """)
                deleted = result.single()["deleted"]
                deleted_rel_count += deleted
                if deleted == 0:
                    break
                logger.info(f"Deleted {deleted} relationships (Total: {deleted_rel_count})")

            deleted_node_count = 0
            while True:
                result = session.run(f"""
                    MATCH (n)
                    WITH n LIMIT {batch_size}
                    DELETE n
                    RETURN count(n) AS deleted
                """)
                deleted = result.single()["deleted"]
                deleted_node_count += deleted
                if deleted == 0:
                    break
                logger.info(f"Deleted {deleted} nodes (Total: {deleted_node_count})")

        logger.info(f"Data deletion complete: {deleted_node_count} nodes, {deleted_rel_count} relationships")
        return True

    except Exception as e:
        logger.error(f"Error deleting data: {e}")
        return False

def drop_constraints(db):
    """Drop all constraints"""
    try:
        logger.info("Dropping constraints...")
        with db.session() as session:
            try:
                constraints = session.run("SHOW CONSTRAINTS").data()
                for constraint in constraints:
                    if 'name' in constraint:
                        session.run(f"DROP CONSTRAINT {constraint['name']}")
                        logger.info(f"Dropped constraint: {constraint['name']}")
            except Exception as e:
                logger.warning(f"Could not drop constraints: {e}")
        return True
    except Exception as e:
        logger.error(f"Error dropping constraints: {e}")
        return False

def reset_database(db, batch_size=5000, drop_schema=False):
    """Reset Neo4j database"""
    logger.info("Resetting Neo4j database...")

    # Get initial stats
    initial_stats = get_database_stats(db)
    logger.info(f"Initial: {initial_stats['total_nodes']} nodes, {initial_stats['relationships']} relationships")

    # Delete all data
    if not delete_all_data(db, batch_size):
        return False

    # Drop schema if requested
    if drop_schema and not drop_constraints(db):
        return False

    # Get final stats
    final_stats = get_database_stats(db)
    logger.info(f"Final: {final_stats['total_nodes']} nodes, {final_stats['relationships']} relationships")

    return final_stats['total_nodes'] == 0 and final_stats['relationships'] == 0

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Reset Neo4j database")
    parser.add_argument("--batch-size", type=int, default=5000, help="Batch size for deletion")
    parser.add_argument("--drop-schema", action="store_true", help="Drop schema constraints")
    parser.add_argument("--uri", type=str, help="Neo4j URI")
    parser.add_argument("--user", type=str, help="Neo4j username")
    parser.add_argument("--password", type=str, help="Neo4j password")
    parser.add_argument("--force", action="store_true", help="Skip confirmation")

    args = parser.parse_args()

    try:
        # Setup database connection
        db = get_database(args.uri, args.user, args.password)

        # Show current stats
        initial_stats = get_database_stats(db)
        print("Current database stats:")
        print(f"  Nodes: {initial_stats['total_nodes']}")
        print(f"  Relationships: {initial_stats['relationships']}")
        print()

        # Confirm reset
        if not args.force:
            confirm = input("Reset database? This deletes all data. (y/n): ")
            if confirm.lower() != 'y':
                print("Reset cancelled")
                return 0

        # Reset database
        success = reset_database(db, args.batch_size, args.drop_schema)

        if success:
            print("Database reset successful!")
            return 0
        else:
            print("Database reset failed")
            return 1

    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        print(f"Database reset failed: {e}")
        return 1

    finally:
        try:
            db = get_database()
            db.close()
        except:
            pass

if __name__ == "__main__":
    exit(main())
