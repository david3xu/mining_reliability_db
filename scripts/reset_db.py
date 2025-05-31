#!/usr/bin/env python3
"""
Database Reset Script for Mining Reliability Database
Standardized configuration access and unified initialization pattern.
"""

import argparse
from mine_core.shared.common import setup_project_environment, handle_error
from mine_core.database.db import get_database, close_database
from configs.environment import get_batch_size

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
        handle_error(logger, e, "getting database stats")
        return {"nodes": {}, "total_nodes": 0, "relationships": 0}

def delete_all_data(db, batch_size):
    """Delete all nodes and relationships in batches"""
    try:
        logger.info("Starting data deletion")

        with db.session() as session:
            # Delete relationships first
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

            # Delete nodes
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
        handle_error(logger, e, "deleting data")
        return False

def drop_constraints(db):
    """Drop all database constraints"""
    try:
        logger.info("Dropping constraints")
        with db.session() as session:
            try:
                constraints = session.run("SHOW CONSTRAINTS").data()
                constraint_count = 0
                for constraint in constraints:
                    if 'name' in constraint:
                        session.run(f"DROP CONSTRAINT {constraint['name']}")
                        constraint_count += 1
                        logger.info(f"Dropped constraint: {constraint['name']}")

                if constraint_count == 0:
                    logger.info("No constraints to drop")
                else:
                    logger.info(f"Dropped {constraint_count} constraints")

            except Exception as e:
                logger.warning(f"Could not drop constraints: {e}")
        return True
    except Exception as e:
        handle_error(logger, e, "dropping constraints")
        return False

def reset_database(db, batch_size, drop_schema=False):
    """Reset Neo4j database completely"""
    logger.info("Starting database reset")

    # Get initial stats
    initial_stats = get_database_stats(db)
    logger.info(f"Initial state: {initial_stats['total_nodes']} nodes, {initial_stats['relationships']} relationships")

    # Delete all data
    if not delete_all_data(db, batch_size):
        logger.error("Failed to delete data")
        return False

    # Drop schema if requested
    if drop_schema:
        if not drop_constraints(db):
            logger.error("Failed to drop constraints")
            return False
        logger.info("Schema constraints dropped")

    # Verify final state
    final_stats = get_database_stats(db)
    logger.info(f"Final state: {final_stats['total_nodes']} nodes, {final_stats['relationships']} relationships")

    success = final_stats['total_nodes'] == 0 and final_stats['relationships'] == 0
    if success:
        logger.info("Database reset completed successfully")
    else:
        logger.error("Database reset incomplete")

    return success

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Reset Neo4j database")
    parser.add_argument("--batch-size", type=int, help="Batch size for deletion")
    parser.add_argument("--drop-schema", action="store_true", help="Drop schema constraints")
    parser.add_argument("--uri", type=str, help="Neo4j URI")
    parser.add_argument("--user", type=str, help="Neo4j username")
    parser.add_argument("--password", type=str, help="Neo4j password")
    parser.add_argument("--force", action="store_true", help="Skip confirmation")
    parser.add_argument("--log-level", type=str, help="Logging level")

    args = parser.parse_args()

    # Standardized project initialization
    global logger
    logger = setup_project_environment("reset_db", args.log_level)

    try:
        # Setup database connection using unified configuration
        db = get_database(args.uri, args.user, args.password)

        # Use unified configuration for batch size
        batch_size = args.batch_size or get_batch_size()

        # Show current stats
        initial_stats = get_database_stats(db)
        print("Current database stats:")
        print(f"  Nodes: {initial_stats['total_nodes']}")
        print(f"  Relationships: {initial_stats['relationships']}")

        if initial_stats['nodes']:
            print("  Node breakdown:")
            for label, count in initial_stats['nodes'].items():
                print(f"    {label}: {count}")
        print()

        # Confirm reset unless forced
        if not args.force:
            if initial_stats['total_nodes'] == 0 and initial_stats['relationships'] == 0:
                print("Database is already empty.")
                return 0

            confirm = input("Reset database? This deletes all data. (y/n): ")
            if confirm.lower() != 'y':
                print("Reset cancelled")
                return 0

        # Reset database
        success = reset_database(db, batch_size, args.drop_schema)

        if success:
            print("Database reset successful!")
            return 0
        else:
            print("Database reset failed")
            return 1

    except Exception as e:
        handle_error(logger, e, "database reset")
        print(f"Database reset failed: {e}")
        return 1

    finally:
        close_database()

if __name__ == "__main__":
    exit(main())
