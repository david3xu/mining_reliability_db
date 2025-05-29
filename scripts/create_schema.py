#!/usr/bin/env python3
"""
Schema Creation Script for Mining Reliability Database
Creates Neo4j schema from model_schema.json
"""

import os
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Any

from mine_core.database.connection import get_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def find_schema_file(schema_filename: str = "model_schema.json") -> Path:
    """Find the schema definition file"""
    # Current directory
    current_dir = Path(__file__).resolve().parent

    # Project root is parent of scripts directory
    project_root = current_dir.parent

    # Possible schema file locations
    schema_paths = [
        current_dir / schema_filename,
        project_root / "configs" / schema_filename,
        project_root / schema_filename
    ]

    for path in schema_paths:
        if path.exists():
            return path

    raise FileNotFoundError(f"Schema file not found: {schema_filename}")

def load_schema(schema_file: Path) -> Dict[str, Any]:
    """Load schema from JSON file"""
    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        logger.info(f"Loaded schema from {schema_file}")
        return schema
    except Exception as e:
        logger.error(f"Error loading schema from {schema_file}: {e}")
        raise

def create_constraints(schema: Dict[str, Any]) -> int:
    """Create Neo4j constraints from schema"""
    connection = get_connection()
    constraints_created = 0

    # Clear existing constraints
    with connection.session() as session:
        try:
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
        with connection.session() as session:
            try:
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

def create_schema_structure(schema: Dict[str, Any]) -> int:
    """Create schema structure in Neo4j"""
    connection = get_connection()
    relationships_created = 0

    # Create relationships between entity types
    for relationship in schema.get("relationships", []):
        from_entity = relationship["from"]
        to_entity = relationship["to"]
        rel_type = relationship["type"]

        # Create template relationship
        with connection.session() as session:
            try:
                query = f"""
                MERGE (from:_SchemaTemplate:{from_entity} {{name: '{from_entity}'}})
                MERGE (to:_SchemaTemplate:{to_entity} {{name: '{to_entity}'}})
                MERGE (from)-[r:{rel_type}]->(to)
                """
                result = session.run(query)
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
    parser.add_argument("--schema", type=str, default="model_schema.json",
                        help="Schema definition file (default: model_schema.json)")
    parser.add_argument("--uri", type=str, default=None,
                        help="Neo4j URI (default: environment variable or bolt://localhost:7687)")
    parser.add_argument("--user", type=str, default=None,
                        help="Neo4j username (default: environment variable or neo4j)")
    parser.add_argument("--password", type=str, default=None,
                        help="Neo4j password (default: environment variable or password)")

    args = parser.parse_args()

    try:
        # Setup connection
        connection = get_connection(args.uri, args.user, args.password)

        # Find and load schema
        schema_file = find_schema_file(args.schema)
        schema = load_schema(schema_file)

        # Create constraints
        constraints_count = create_constraints(schema)
        logger.info(f"Created {constraints_count} constraints")

        # Create schema structure
        relationships_count = create_schema_structure(schema)
        logger.info(f"Created {relationships_count} relationship types")

        print("Schema creation successful!")
        return 0

    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        print(f"Schema creation failed: {e}")
        return 1

    finally:
        # Close connection
        connection = get_connection()
        connection.close()

if __name__ == "__main__":
    exit(main())
