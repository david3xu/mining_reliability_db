#!/usr/bin/env python3
"""
Simplified Field Processing Utilities for Mining Reliability Database
Clean, efficient field validation and processing for single-value datasets.
"""

import re
import logging
from typing import Any, Optional, List, Dict

logger = logging.getLogger(__name__)

# Missing data indicators
MISSING_DATA_INDICATORS = {
    "DATA_NOT_AVAILABLE",
    "NOT_SPECIFIED",
    "NOT_APPLICABLE",
    None,
    "",
    "null",
    "NULL",
    "N/A",
    "n/a",
    "Unknown",
    "unknown"
}

def has_real_value(value: Any) -> bool:
    """Check if field has meaningful data"""
    if value in MISSING_DATA_INDICATORS:
        return False

    if isinstance(value, str):
        cleaned = value.strip().lower()
        return cleaned not in {"", "null", "n/a", "unknown", "data_not_available", "not_specified", "not_applicable"}

    return value is not None

def get_missing_indicator(field_name: str, context: str = "general") -> str:
    """Get appropriate missing data indicator"""
    field_lower = field_name.lower()

    if "date" in field_lower or "time" in field_lower:
        return "DATA_NOT_AVAILABLE"
    elif "comment" in field_lower or "description" in field_lower or "text" in field_lower:
        return "NOT_SPECIFIED"
    elif context == "optional":
        return "NOT_APPLICABLE"
    else:
        return "DATA_NOT_AVAILABLE"

def clean_label(value: str) -> str:
    """Clean field value for Neo4j label compatibility"""
    if not isinstance(value, str):
        value = str(value)

    # Remove special characters, keep alphanumeric and underscores
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', value.replace(' ', '_').replace('-', '_'))

    # Ensure it starts with letter
    if cleaned and cleaned[0].isdigit():
        cleaned = f"_{cleaned}"

    # Limit length for Neo4j compatibility
    return cleaned[:50] if cleaned else "UnknownValue"

def extract_field_priority(record: Dict[str, Any], priority_fields: List[str]) -> Optional[str]:
    """Extract first available field value from priority list"""
    for field_name in priority_fields:
        value = record.get(field_name)
        if has_real_value(value):
            return str(value)
    return None

def create_entity_id(entity_type: str, base_id: str) -> str:
    """Generate unique ID for entity"""
    return f"{entity_type.lower()}-{base_id}"

def validate_field_for_entity(field_name: str, value: Any, required_fields: List[str] = None) -> bool:
    """Validate if field should create entity"""
    # Must have real value
    if not has_real_value(value):
        return False

    # Check if it's a required field
    if required_fields and field_name in required_fields:
        return True

    # Check field patterns that should always create entities
    significant_patterns = [
        "number", "id", "title", "name", "type", "category",
        "status", "stage", "cause", "plan", "action"
    ]

    field_lower = field_name.lower()
    return any(pattern in field_lower for pattern in significant_patterns)

def normalize_field_value(value: Any, field_type: str = "string") -> Any:
    """Normalize field value based on type"""
    if not has_real_value(value):
        return get_missing_indicator("", "general")

    if field_type == "boolean":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"true", "yes", "1", "completed", "effective", "satisfactory"}
        return bool(value)

    if field_type == "date":
        # Basic date string normalization
        if isinstance(value, str):
            return value.strip()
        return str(value)

    if field_type == "integer":
        try:
            return int(float(str(value)))
        except:
            return get_missing_indicator("", "general")

    # Default to string
    return str(value).strip() if value else get_missing_indicator("", "general")

def get_entity_label_cascade(record: Dict[str, Any], entity_config: Dict[str, Any]) -> Optional[str]:
    """Get entity label using cascade priority"""
    priority_fields = entity_config.get("label_priority", [])

    # Try each priority field
    for field_name in priority_fields:
        value = record.get(field_name)
        if has_real_value(value):
            return clean_label(str(value))

    # Fallback to entity type
    return entity_config.get("entity_type", "UnknownEntity")

def extract_root_cause_tail(value: str, delimiters: List[str] = None) -> str:
    """Extract tail component from root cause for causal intelligence"""
    if not has_real_value(value):
        return "NOT_SPECIFIED"

    str_value = str(value).strip()

    # Default delimiters for root cause analysis
    if delimiters is None:
        delimiters = [";", ",", "|", "\n", " - ", " / ", " and ", " & "]

    # Split on delimiters and extract tail (final) component
    for delimiter in delimiters:
        if delimiter in str_value:
            parts = [part.strip() for part in str_value.split(delimiter) if part.strip()]
            if len(parts) > 1:
                return parts[-1]  # Return tail item for secondary causal analysis

    # No delimiters found - return original value
    return str_value

def validate_entity_completeness(entity_data: Dict[str, Any], required_fields: List[str]) -> float:
    """Calculate completeness ratio for entity data"""
    if not required_fields:
        return 1.0

    fields_with_data = sum(1 for field in required_fields
                          if has_real_value(entity_data.get(field)))

    return fields_with_data / len(required_fields)

def is_missing_data_indicator(value: str) -> bool:
    """Check if value is a missing data indicator"""
    return value in MISSING_DATA_INDICATORS

def get_field_category(field_name: str) -> str:
    """Categorize field for analytical purposes"""
    field_lower = field_name.lower()

    if any(term in field_lower for term in ["date", "time"]):
        return "temporal"
    elif any(term in field_lower for term in ["id", "number"]):
        return "identifier"
    elif any(term in field_lower for term in ["category", "type", "stage", "status"]):
        return "categorical"
    elif any(term in field_lower for term in ["comment", "description", "what", "plan", "action"]):
        return "descriptive"
    elif any(term in field_lower for term in ["complete", "effective", "satisfactory"]):
        return "boolean"
    elif any(term in field_lower for term in ["amount", "loss", "days"]):
        return "quantitative"
    else:
        return "general"

def validate_cascade_labeling(entity_data: Dict[str, Any], cascade_config: Dict[str, Any]) -> str:
    """Validate and apply cascade labeling strategy"""
    priority_fields = cascade_config.get("label_priority", [])
    entity_type = cascade_config.get("entity_type", "Unknown")

    # Try priority fields in order
    for field_name in priority_fields:
        value = entity_data.get(field_name)
        if has_real_value(value) and not is_missing_data_indicator(str(value)):
            clean_value = clean_label(str(value))
            if clean_value and clean_value != "UnknownValue":
                return clean_value

    # Fallback to entity type
    return entity_type

def get_causal_intelligence_fields(record: Dict[str, Any]) -> Dict[str, str]:
    """Extract causal intelligence fields for root cause analysis"""
    causal_fields = {}

    # Primary root cause
    root_cause = record.get("Root Cause")
    if has_real_value(root_cause):
        causal_fields["primary_cause"] = str(root_cause)
        causal_fields["secondary_cause"] = extract_root_cause_tail(str(root_cause))

    # Supporting evidence
    evidence = record.get("Obj. Evidence")
    if has_real_value(evidence):
        causal_fields["evidence"] = str(evidence)

    return causal_fields

def format_value_for_storage(value: Any) -> str:
    """Format value for consistent database storage"""
    if not has_real_value(value):
        return get_missing_indicator("", "storage")

    if isinstance(value, str):
        return value.strip()
    elif isinstance(value, bool):
        return "true" if value else "false"
    else:
        return str(value)

def calculate_data_quality_score(entity_data: Dict[str, Any], total_possible_fields: int) -> float:
    """Calculate data quality score for entity"""
    if total_possible_fields == 0:
        return 1.0

    fields_with_data = sum(1 for value in entity_data.values()
                          if has_real_value(value) and not is_missing_data_indicator(str(value)))

    return min(1.0, fields_with_data / total_possible_fields)
