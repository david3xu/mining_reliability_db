#!/usr/bin/env python3
"""
Schema Creation Script for Mining Reliability Database
Creates Neo4j schema from configuration.
"""

import sys
import os
import logging
import argparse

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mine_core.database.db import get_database
from configs.environment import get_schema

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_constraints(schema, db):
    """Create Neo4j constraints from schema"""
    constraints_created = 0

    # Clear existing constraints
    try:
        with db.session() as session:
            constraints = session.run("SHOW CONSTRAINTS").data()
            for constraint in constraints:
                if 'name' in constraint:
                    session.run(f"DROP CONSTRAINT {constraint['name']}")
        logger.info("Dropped existing constraints")
    except Exception as e:
        logger.warning(f"Error dropping constraints: {e}")

    # Create unique constraints for each entity's primary key
    for entity in schema.get("entities", []):
        entity_name = entity["name"]
        properties = entity["properties"]

        # Find primary key property
        pk_property = None
        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                pk_property = prop_name
                break

        if not pk_property:
            logger.warning(f"No primary key found for entity {entity_name}")
            continue

        # Create constraint
        try:
            with db.session() as session:
                query = f"""
                CREATE CONSTRAINT IF NOT EXISTS FOR (n:{entity_name})
                REQUIRE n.{pk_property} IS UNIQUE
                """
                session.run(query)
                constraints_created += 1
                logger.info(f"Created constraint for {entity_name}.{pk_property}")
        except Exception as e:
            logger.error(f"Error creating constraint for {entity_name}.{pk_property}: {e}")

    return constraints_created

def create_schema_structure(schema, db):
    """Create schema structure in Neo4j"""
    relationships_created = 0

    for relationship in schema.get("relationships", []):
        from_entity = relationship["from"]
        to_entity = relationship["to"]
        rel_type = relationship["type"]

        try:
            with db.session() as session:
                query = f"""
                MERGE (from:_SchemaTemplate:{from_entity} {{name: '{from_entity}'}})
                MERGE (to:_SchemaTemplate:{to_entity} {{name: '{to_entity}'}})
                MERGE (from)-[r:{rel_type}]->(to)
                """
                session.run(query)
                relationships_created += 1
                logger.info(f"Created relationship: {from_entity}-[{rel_type}]->{to_entity}")
        except Exception as e:
            logger.error(f"Error creating relationship {from_entity}-[{rel_type}]->{to_entity}: {e}")

    return relationships_created

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Create Neo4j schema for Mining Reliability Database"
    )
    parser.add_argument("--uri", type=str, help="Neo4j URI")
    parser.add_argument("--user", type=str, help="Neo4j username")
    parser.add_argument("--password", type=str, help="Neo4j password")

    args = parser.parse_args()

    try:
        # Setup database connection
        db = get_database(args.uri, args.user, args.password)

        # Load schema
        schema = get_schema()
        if not schema:
            logger.error("No schema configuration found")
            return 1

        # Create constraints
        constraints_count = create_constraints(schema, db)
        logger.info(f"Created {constraints_count} constraints")

        # Create schema structure
        relationships_count = create_schema_structure(schema, db)
        logger.info(f"Created {relationships_count} relationship types")

        print("Schema creation successful!")
        return 0

    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        print(f"Schema creation failed: {e}")
        return 1

    finally:
        try:
            db = get_database()
            db.close()
        except:
            pass

if __name__ == "__main__":
    exit(main())
