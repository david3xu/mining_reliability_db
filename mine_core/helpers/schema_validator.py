#!/usr/bin/env python3
"""
Schema Validation Utilities
Provides validation functions for entity data against schema.
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

logger = logging.getLogger(__name__)

def load_schema(schema_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load schema from file"""
    if not schema_path:
        # Default schema location
        script_dir = Path(__file__).resolve().parent.parent.parent
        schema_path = script_dir / "configs" / "model_schema.json"

    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading schema from {schema_path}: {e}")
        return {}

def validate_entity(entity_type: str, data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
    """
    Validate entity data against schema

    Returns:
        Tuple of (is_valid, error_messages)
    """
    # Load schema if not provided
    if not schema:
        schema = load_schema()

    if not schema:
        return False, ["Schema not available"]

    # Map entity types to their primary key field names
    pk_mapping = {
        "RootCause": "cause_id",
        "ActionPlan": "plan_id",
        "RecurringStatus": "recurring_id",
        "AmountOfLoss": "loss_id",
        "EquipmentStrategy": "strategy_id",
        "Department": "dept_id"
    }

    # Find entity schema
    entity_schema = None
    for entity in schema.get("entities", []):
        if entity["name"] == entity_type:
            entity_schema = entity
            break

    if not entity_schema:
        return False, [f"Entity type '{entity_type}' not found in schema"]

    # Validate against schema
    errors = []
    properties = entity_schema.get("properties", {})

    # Get primary key field name
    pk_field = pk_mapping.get(entity_type, f"{entity_type.lower()}_id")

    # Check required properties
    for prop_name, prop_info in properties.items():
        # Map property name if needed (for primary keys)
        actual_prop = prop_name
        if prop_name.endswith("_id") and prop_name == pk_field:
            actual_prop = pk_field

        if prop_info.get("required", False) and actual_prop not in data:
            errors.append(f"Missing required property: {actual_prop}")

    # Check property types
    for prop_name, value in data.items():
        # Skip if property not in schema
        schema_prop = prop_name
        for schema_field in properties.keys():
            if schema_field.endswith("_id") and schema_field == pk_field and prop_name == pk_field:
                schema_prop = schema_field
                break

        if schema_prop not in properties:
            continue

        prop_info = properties[schema_prop]
        prop_type = prop_info.get("type", "string")

        # Validate type
        if value is not None:  # Skip None values
            if prop_type == "string" and not isinstance(value, str):
                errors.append(f"Property {prop_name} should be string, got {type(value).__name__}")
            elif prop_type == "integer" and not isinstance(value, int):
                errors.append(f"Property {prop_name} should be integer, got {type(value).__name__}")
            elif prop_type == "boolean" and not isinstance(value, bool):
                errors.append(f"Property {prop_name} should be boolean, got {type(value).__name__}")
            elif prop_type == "date" and not isinstance(value, str):
                # Simple date validation (could be enhanced)
                errors.append(f"Property {prop_name} should be date string, got {type(value).__name__}")
            elif prop_type == "text" and not isinstance(value, str):
                errors.append(f"Property {prop_name} should be text, got {type(value).__name__}")

    return len(errors) == 0, errors

def validate_relationship(from_type: str, to_type: str, rel_type: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
    """
    Validate relationship against schema

    Returns:
        Tuple of (is_valid, error_messages)
    """
    # Load schema if not provided
    if not schema:
        schema = load_schema()

    if not schema:
        return False, ["Schema not available"]

    # Check relationship in schema
    valid_relationship = False
    for relationship in schema.get("relationships", []):
        if relationship.get("from") == from_type and relationship.get("to") == to_type and relationship.get("type") == rel_type:
            valid_relationship = True
            break

    if not valid_relationship:
        return False, [f"Relationship {from_type}-[{rel_type}]->{to_type} not defined in schema"]

    return True, []

def validate_entity_chain(entities: Dict[str, List[Dict[str, Any]]], schema: Optional[Dict[str, Any]] = None) -> Tuple[bool, Dict[str, List[str]]]:
    """
    Validate entity chain against schema

    Returns:
        Tuple of (is_valid, {entity_type: [error_messages]})
    """
    # Load schema if not provided
    if not schema:
        schema = load_schema()

    if not schema:
        return False, {"schema": ["Schema not available"]}

    # Primary key mapping
    pk_mapping = {
        "RootCause": "cause_id",
        "ActionPlan": "plan_id",
        "RecurringStatus": "recurring_id",
        "AmountOfLoss": "loss_id",
        "EquipmentStrategy": "strategy_id",
        "Department": "dept_id"
    }

    # Validate each entity
    errors = {}
    all_valid = True

    for entity_type, entity_list in entities.items():
        entity_errors = []

        for entity in entity_list:
            # Check for consistent ID field naming
            pk_field = pk_mapping.get(entity_type, f"{entity_type.lower()}_id")
            if pk_field not in entity:
                non_standard_keys = [k for k in entity.keys() if k.endswith('_id')]
                if non_standard_keys:
                    entity_errors.append(f"Entity has non-standard ID field: expected {pk_field}, got {non_standard_keys}")
                    all_valid = False
                    continue

            valid, entity_error = validate_entity(entity_type, entity, schema)
            if not valid:
                all_valid = False
                entity_errors.extend(entity_error)

        if entity_errors:
            errors[entity_type] = entity_errors

    return all_valid, errors
