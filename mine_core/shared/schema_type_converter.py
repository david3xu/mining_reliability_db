#!/usr/bin/env python3
"""
Schema-Aware Type Converter
Converts preprocessed data to match model_schema.json type definitions.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

class SchemaTypeConverter:
    """Converts data types according to model_schema.json definitions"""

    def __init__(self, schema_file_path: str = None):
        """Initialize with schema definitions"""
        if schema_file_path is None:
            # Default path relative to project root
            project_root = Path(__file__).resolve().parent.parent.parent
            schema_file_path = project_root / "configs" / "model_schema.json"

        self.schema_path = Path(schema_file_path)
        self.schema = self._load_schema()
        self.entity_types = self._extract_entity_types()

    def _load_schema(self) -> Dict[str, Any]:
        """Load model schema from JSON file"""
        try:
            with open(self.schema_path, 'r') as f:
                schema = json.load(f)
            logger.info(f"Schema loaded from {self.schema_path}")
            return schema
        except Exception as e:
            logger.error(f"Failed to load schema from {self.schema_path}: {e}")
            raise

    def _extract_entity_types(self) -> Dict[str, Dict[str, str]]:
        """Extract entity type mappings from schema"""
        entity_types = {}

        for entity in self.schema.get("entities", []):
            entity_name = entity.get("name")
            if not entity_name:
                continue

            properties = entity.get("properties", {})
            field_types = {}

            for field_name, field_config in properties.items():
                field_type = field_config.get("type", "string")
                field_types[field_name] = field_type

            entity_types[entity_name] = field_types

        logger.info(f"Extracted type mappings for {len(entity_types)} entities")
        return entity_types

    def convert_value(self, value: Any, target_type: str, field_name: str = "") -> Any:
        """Convert single value to target type with enhanced handling"""
        # Handle None and empty values
        if value is None:
            return self._get_default_for_type(target_type)

        # Handle string representation of None
        if isinstance(value, str) and value.strip().lower() in {"none", "null", ""}:
            return self._get_default_for_type(target_type)

        # Handle missing data indicators
        if isinstance(value, str) and value.strip() in {
            "DATA_NOT_AVAILABLE", "NOT_SPECIFIED", "NOT_APPLICABLE", "N/A", "n/a", ""
        }:
            return self._get_default_for_type(target_type)

        try:
            # Normalize target type (handle schema variations)
            target_type = self._normalize_target_type(target_type)

            if target_type == "string":
                return self._convert_to_string(value)

            elif target_type == "text":
                return self._convert_to_text(value)

            elif target_type == "integer":
                return self._convert_to_integer(value)

            elif target_type == "boolean":
                return self._convert_to_boolean(value)

            elif target_type == "date":
                return self._convert_to_date(value)

            else:
                logger.warning(f"Unknown type '{target_type}' for field '{field_name}', defaulting to string")
                return self._convert_to_string(value)

        except Exception as e:
            logger.warning(f"Type conversion failed for field '{field_name}' value '{value}' to type '{target_type}': {e}")
            return self._get_default_for_type(target_type)

    def _normalize_target_type(self, target_type: str) -> str:
        """Normalize target type to handle variations"""
        type_mapping = {
            "str": "string",
            "varchar": "string",
            "char": "string",
            "txt": "text",
            "longtext": "text",
            "int": "integer",
            "number": "integer",
            "bool": "boolean",
            "datetime": "date",
            "timestamp": "date"
        }
        return type_mapping.get(target_type.lower(), target_type.lower())

    def _convert_to_string(self, value: Any) -> str:
        """Convert value to string type"""
        if isinstance(value, str):
            return value.strip()
        return str(value)

    def _convert_to_text(self, value: Any) -> str:
        """Convert value to text type (longer strings)"""
        if isinstance(value, str):
            return value.strip()
        return str(value)

    def _convert_to_integer(self, value: Any) -> Optional[int]:
        """Convert value to integer"""
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(value)

        if isinstance(value, str):
            # Clean string of common formatting
            cleaned = value.strip().replace(",", "").replace("$", "")

            # Handle negative numbers
            if cleaned.startswith("(") and cleaned.endswith(")"):
                cleaned = "-" + cleaned[1:-1]

            try:
                return int(float(cleaned))
            except ValueError:
                return None

        return None

    def _convert_to_boolean(self, value: Any) -> Optional[bool]:
        """Convert value to boolean with enhanced handling"""
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            value_lower = value.strip().lower()

            # Handle None/empty strings
            if value_lower in {"", "none", "null", "n/a"}:
                return None

            # True values (expanded list)
            if value_lower in {
                "true", "yes", "y", "1", "on", "enabled", "active",
                "completed", "effective", "satisfactory", "applicable",
                "required", "success", "positive", "ok", "good",
                "valid", "correct", "right", "up", "online"
            }:
                return True

            # False values (expanded list)
            if value_lower in {
                "false", "no", "n", "0", "off", "disabled", "inactive",
                "incomplete", "ineffective", "unsatisfactory", "not applicable",
                "not required", "failure", "negative", "bad", "invalid",
                "incorrect", "wrong", "down", "offline"
            }:
                return False

            # Handle "Not " prefixed values
            if value_lower.startswith("not "):
                return False

        if isinstance(value, (int, float)):
            return bool(value)

        # If we can't determine, return None for optional boolean fields
        return None

    def _convert_to_date(self, value: Any) -> Optional[str]:
        """Convert value to standardized date string with enhanced parsing"""
        if isinstance(value, str):
            value = value.strip()
            if not value or value.lower() in {"none", "null", "n/a", ""}:
                return None

            # Handle common date-like strings that should return None
            if value.lower() in {"data_not_available", "not_specified", "not_applicable"}:
                return None

            try:
                # Try parsing various date formats
                parsed_date = date_parser.parse(value, fuzzy=True)
                return parsed_date.strftime("%Y-%m-%d")
            except:
                # If parsing fails, check if it looks like a date
                if len(value) >= 8 and any(char in value for char in ["-", "/", ".", " "]):
                    # Try to extract year if it's there
                    year_match = re.search(r'(19|20)\d{2}', value)
                    if year_match:
                        return value  # Return as-is if it contains a reasonable year
                return None

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")

        return None

    def _get_default_for_type(self, target_type: str) -> Any:
        """Get default value for missing data based on type"""
        defaults = {
            "string": "DATA_NOT_AVAILABLE",
            "text": "NOT_SPECIFIED",
            "integer": None,
            "boolean": None,
            "date": None
        }
        return defaults.get(target_type, "DATA_NOT_AVAILABLE")

    def convert_entity_data(self, entity_name: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert all fields in entity data according to schema"""
        if entity_name not in self.entity_types:
            logger.warning(f"Entity '{entity_name}' not found in schema, skipping type conversion")
            return entity_data

        entity_field_types = self.entity_types[entity_name]
        converted_data = {}

        for field_name, value in entity_data.items():
            if field_name in entity_field_types:
                target_type = entity_field_types[field_name]
                converted_value = self.convert_value(value, target_type, field_name)
                converted_data[field_name] = converted_value

                # Log type conversion for debugging
                if type(value).__name__ != type(converted_value).__name__:
                    logger.debug(f"Converted {entity_name}.{field_name}: {type(value).__name__} → {type(converted_value).__name__}")
            else:
                # Field not in schema, keep as-is
                converted_data[field_name] = value
                logger.debug(f"Field '{field_name}' not in {entity_name} schema, keeping original value")

        return converted_data

    def convert_record(self, record: Dict[str, Any], entity_mappings: Dict[str, Any] = None,
                      use_smart_mapping: bool = True) -> Dict[str, Any]:
        """Convert a complete record with entity awareness and smart field mapping"""
        converted_record = {}

        # If no entity mappings provided, try to create smart mappings
        if entity_mappings is None and use_smart_mapping:
            entity_mappings = self._create_smart_entity_mappings(record)
        elif entity_mappings is None:
            # No mappings, return record with minimal type conversion
            return self._convert_record_simple(record)

        # Group fields by entity based on entity_mappings
        entity_fields = {}
        for entity_name, field_mapping in entity_mappings.items():
            entity_fields[entity_name] = {}

            for schema_field, source_field in field_mapping.items():
                if source_field in record:
                    entity_fields[entity_name][schema_field] = record[source_field]

        # Convert each entity's fields
        converted_fields_by_source = {}
        for entity_name, fields in entity_fields.items():
            if fields:  # Only process if entity has data
                converted_fields = self.convert_entity_data(entity_name, fields)

                # Map converted fields back to source field names
                if entity_name in entity_mappings:
                    for schema_field, converted_value in converted_fields.items():
                        source_field = entity_mappings[entity_name].get(schema_field)
                        if source_field:
                            converted_fields_by_source[source_field] = converted_value

        # Start with converted fields
        converted_record = converted_fields_by_source.copy()

        # Add any fields not covered by entity mappings
        for field_name, value in record.items():
            if field_name not in converted_record:
                converted_record[field_name] = value

        return converted_record

    def _create_smart_entity_mappings(self, record: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Create smart field mappings using field name similarity"""
        try:
            from .field_name_mapper import create_field_mapper
            mapper = create_field_mapper()

            source_fields = list(record.keys())
            entity_mappings = mapper.create_entity_field_mapping(
                source_fields, self.entity_types, min_similarity=0.4
            )

            logger.info(f"Created smart mappings for {len(entity_mappings)} entities")
            return entity_mappings

        except ImportError:
            logger.warning("Field name mapper not available, using exact field matching")
            return self._create_exact_entity_mappings(record)

    def _create_exact_entity_mappings(self, record: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """Create entity mappings using exact field name matching"""
        entity_mappings = {}
        source_fields = set(record.keys())

        for entity_name, entity_field_types in self.entity_types.items():
            schema_fields = set(entity_field_types.keys())

            # Find exact matches
            matching_fields = source_fields.intersection(schema_fields)
            if matching_fields:
                entity_mappings[entity_name] = {field: field for field in matching_fields}

        return entity_mappings

    def _convert_record_simple(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Simple record conversion without entity mappings"""
        converted_record = {}

        for field_name, value in record.items():
            # Try to infer type from value and convert appropriately
            if isinstance(value, str) and value.lower() in {"true", "false", "yes", "no"}:
                converted_record[field_name] = self.convert_value(value, "boolean", field_name)
            elif isinstance(value, str) and value.isdigit():
                converted_record[field_name] = self.convert_value(value, "integer", field_name)
            else:
                converted_record[field_name] = value

        return converted_record

    def get_schema_summary(self) -> Dict[str, Any]:
        """Get summary of schema type definitions"""
        summary = {
            "total_entities": len(self.entity_types),
            "entities": {}
        }

        for entity_name, field_types in self.entity_types.items():
            type_counts = {}
            for field_type in field_types.values():
                type_counts[field_type] = type_counts.get(field_type, 0) + 1

            summary["entities"][entity_name] = {
                "total_fields": len(field_types),
                "type_distribution": type_counts,
                "fields": field_types
            }

        return summary


def create_schema_converter(schema_file_path: str = None) -> SchemaTypeConverter:
    """Factory function to create schema converter"""
    return SchemaTypeConverter(schema_file_path)


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test the converter
    converter = create_schema_converter()

    # Print schema summary
    summary = converter.get_schema_summary()
    print("Schema Type Summary:")
    for entity_name, info in summary["entities"].items():
        print(f"  {entity_name}: {info['total_fields']} fields")
        for type_name, count in info["type_distribution"].items():
            print(f"    {type_name}: {count}")

    # Test type conversions
    test_cases = [
        ("true", "boolean", True),
        ("false", "boolean", False),
        ("yes", "boolean", True),
        ("123", "integer", 123),
        ("123.45", "integer", 123),
        ("2024-01-15", "date", "2024-01-15"),
        ("01/15/2024", "date", "2024-01-15"),
        ("Hello World", "string", "Hello World"),
    ]

    print("\nType Conversion Tests:")
    for value, target_type, expected in test_cases:
        result = converter.convert_value(value, target_type)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {value} → {target_type}: {result} (expected: {expected})")
