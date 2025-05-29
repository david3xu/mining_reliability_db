#!/usr/bin/env python3
"""
Database Reset Script for Mining Reliability Database
Cleans Neo4j database by removing all data and schema.
"""

import argparse
import logging
from typing import Dict, List, Any

from mine_core.database.connection import get_connection
from mine_core.helpers.log_manager import setup_logging, get_logger

# Configure logging
setup_logging()
logger = get_logger(__name__)

def get_database_stats() -> Dict[str, Any]:
    """Get current database statistics"""
    connection = get_connection()

    with connection.session() as session:
        try:
            # Count nodes by label
            query = """
            CALL db.labels() YIELD label
            CALL apoc.cypher.run('MATCH (n:`' + $label + '`) RETURN count(n) as count', {}) YIELD value
            RETURN $label AS label, value.count AS count
            """

            label_results = []
            try:
                label_results = session.run("CALL db.labels() YIELD label RETURN collect(label) AS labels").single()["labels"]
            except Exception as e:
                logger.warning(f"Could not get labels: {e}")

            node_stats = {}
            total_nodes = 0

            for label in label_results:
                try:
                    result = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS count")
                    count = result.single()["count"]
                    node_stats[label] = count
                    total_nodes += count
                except Exception as e:
                    logger.warning(f"Could not count nodes with label '{label}': {e}")

            # If no specific labels found, get total node count
            if not node_stats:
                result = session.run("MATCH (n) RETURN count(n) AS count")
                total_nodes = result.single()["count"]
                node_stats["(unlabeled)"] = total_nodes

            # Count relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS count")
            rel_count = result.single()["count"]

            # Count constraints
            constraints = []
            try:
                constraints = session.run("SHOW CONSTRAINTS").data()
            except Exception as e:
                logger.warning(f"Could not get constraints: {e}")

            # Count indexes
            indexes = []
            try:
                indexes = session.run("SHOW INDEXES").data()
            except Exception as e:
                logger.warning(f"Could not get indexes: {e}")

            return {
                "nodes": node_stats,
                "total_nodes": total_nodes,
                "relationships": rel_count,
                "constraints": len(constraints),
                "indexes": len(indexes)
            }

        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                "nodes": {},
                "total_nodes": 0,
                "relationships": 0,
                "constraints": 0,
                "indexes": 0
            }

def delete_all_data(batch_size: int = 5000) -> bool:
    """Delete all nodes and relationships"""
    connection = get_connection()

    try:
        logger.info("Deleting all data...")

        with connection.session() as session:
            # First delete all relationships
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

            # Then delete all nodes
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

def drop_constraints() -> bool:
    """Drop all constraints"""
    connection = get_connection()

    try:
        logger.info("Dropping constraints...")

        with connection.session() as session:
            # Get all constraints
            constraints = []
            try:
                constraints = session.run("SHOW CONSTRAINTS").data()
            except Exception as e:
                logger.warning(f"Could not get constraints: {e}")
                return False

            # Drop each constraint
            for constraint in constraints:
                if 'name' in constraint:
                    try:
                        session.run(f"DROP CONSTRAINT {constraint['name']}")
                        logger.info(f"Dropped constraint: {constraint['name']}")
                    except Exception as e:
                        logger.warning(f"Could not drop constraint {constraint['name']}: {e}")

        return True

    except Exception as e:
        logger.error(f"Error dropping constraints: {e}")
        return False

def drop_indexes() -> bool:
    """Drop all indexes"""
    connection = get_connection()

    try:
        logger.info("Dropping indexes...")

        with connection.session() as session:
            # Get all indexes
            indexes = []
            try:
                indexes = session.run("SHOW INDEXES").data()
            except Exception as e:
                logger.warning(f"Could not get indexes: {e}")
                return False

            # Drop each index
            for index in indexes:
                if 'name' in index:
                    try:
                        session.run(f"DROP INDEX {index['name']}")
                        logger.info(f"Dropped index: {index['name']}")
                    except Exception as e:
                        logger.warning(f"Could not drop index {index['name']}: {e}")

        return True

    except Exception as e:
        logger.error(f"Error dropping indexes: {e}")
        return False

def reset_database(batch_size: int = 5000, drop_schema: bool = False) -> bool:
    """Reset Neo4j database"""
    logger.info("Resetting Neo4j database...")

    # Get initial stats
    initial_stats = get_database_stats()
    logger.info(f"Initial database stats: {initial_stats['total_nodes']} nodes, {initial_stats['relationships']} relationships")

    # Delete all data
    if not delete_all_data(batch_size):
        logger.error("Failed to delete data")
        return False

    # Drop schema if requested
    if drop_schema:
        if not drop_constraints():
            logger.error("Failed to drop constraints")
            return False

        if not drop_indexes():
            logger.error("Failed to drop indexes")
            return False

    # Get final stats
    final_stats = get_database_stats()
    logger.info(f"Final database stats: {final_stats['total_nodes']} nodes, {final_stats['relationships']} relationships")

    return final_stats['total_nodes'] == 0 and final_stats['relationships'] == 0

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Reset Neo4j database for Mining Reliability DB"
    )
    parser.add_argument("--batch-size", type=int, default=5000,
                        help="Batch size for deleting nodes and relationships")
    parser.add_argument("--drop-schema", action="store_true",
                        help="Drop schema (constraints and indexes) in addition to data")
    parser.add_argument("--uri", type=str, default=None,
                        help="Neo4j URI (default: environment variable or bolt://localhost:7687)")
    parser.add_argument("--user", type=str, default=None,
                        help="Neo4j username (default: environment variable or neo4j)")
    parser.add_argument("--password", type=str, default=None,
                        help="Neo4j password (default: environment variable or password)")
    parser.add_argument("--force", action="store_true",
                        help="Skip confirmation prompt")

    args = parser.parse_args()

    try:
        # Setup connection
        connection = get_connection(args.uri, args.user, args.password)

        # Get initial stats
        initial_stats = get_database_stats()
        print("Current database stats:")
        print(f"  Nodes: {initial_stats['total_nodes']}")
        print(f"  Relationships: {initial_stats['relationships']}")
        print(f"  Constraints: {initial_stats['constraints']}")
        print(f"  Indexes: {initial_stats['indexes']}")
        print()

        # Confirm reset
        if not args.force:
            confirm = input("Are you sure you want to reset the database? This will delete all data. (y/n): ")
            if confirm.lower() != 'y':
                print("Reset cancelled")
                return 0

        # Reset database
        success = reset_database(args.batch_size, args.drop_schema)

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
        # Close connection
        try:
            connection = get_connection()
            connection.close()
        except:
            pass

if __name__ == "__main__":
    exit(main())
