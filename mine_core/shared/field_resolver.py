"""
Field Resolution Utilities for Unified Field Reference System

This module provides the architectural foundation for eliminating field mapping
duplications and enabling consistent field name resolution across all three
naming conventions: technical (database), business (UI), and raw data.

ARCHITECTURE IMPACT:
- Eliminates triple field name convention chaos
- Enables Phase 1 Core Foundation implementation
- Provides single source of truth for field resolution
- Supports seamless adapter pattern implementation

FIELD RESOLUTION METHODOLOGY:
- Technical fields: Database schema field names (root_cause, action_request_number)
- Business fields: Display/UI field names ("Root Cause", "Action Request Number:")
- Raw data fields: Exact raw data field names (with colons and case variations)
"""

import json
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import logging

from .constants import DEFAULT_CONFIG_DIR

logger = logging.getLogger(__name__)

class FieldResolver:
    """
    Unified field resolution system that eliminates field mapping duplications
    and provides consistent translation between technical, business, and raw data field names.

    This is the architectural foundation that enables the 4-phase refactoring methodology
    by providing a single source of truth for all field name mappings.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize field resolver with unified field mappings"""
        self.config_path = config_path or str(Path(DEFAULT_CONFIG_DIR) / "field_mappings_unified.json")
        self._unified_mappings = None
        self._load_unified_mappings()

    def _load_unified_mappings(self) -> None:
        """Load unified field mappings configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._unified_mappings = json.load(f)

            logger.info(f"Loaded unified field mappings from {self.config_path}")

            # Validate architecture compliance
            version = self._unified_mappings.get("mapping_version", "unknown")
            compliance = self._unified_mappings.get("architecture_compliance", "unknown")

            logger.info(f"Field mapping version: {version}, compliance: {compliance}")

        except FileNotFoundError:
            logger.error(f"Unified field mappings not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in unified field mappings: {e}")
            raise

    def get_technical_field(self, entity_name: str, field_identifier: str) -> Optional[str]:
        """
        Get technical database field name for a given entity and field identifier.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')
            field_identifier: Field identifier (can be technical, business, or raw field name)

        Returns:
            Technical database field name (e.g., 'root_cause', 'action_request_number')
        """
        if not self._unified_mappings:
            return None

        entity_mappings = self._unified_mappings.get("unified_field_references", {}).get(entity_name)
        if not entity_mappings:
            logger.warning(f"Entity '{entity_name}' not found in unified mappings")
            return None

        # First try exact match in technical fields
        technical_fields = entity_mappings.get("technical_fields", {})
        if field_identifier in technical_fields:
            return technical_fields[field_identifier]

        # Try reverse lookup from business fields
        business_fields = entity_mappings.get("business_fields", {})
        for tech_field, business_field in business_fields.items():
            if business_field == field_identifier:
                return tech_field

        # Try reverse lookup from raw data fields
        raw_data_fields = entity_mappings.get("raw_data_fields", {})
        for tech_field, raw_field in raw_data_fields.items():
            if raw_field == field_identifier:
                return tech_field

        logger.warning(f"Field '{field_identifier}' not found for entity '{entity_name}'")
        return None

    def get_business_field(self, entity_name: str, technical_field: str) -> Optional[str]:
        """
        Get business display field name for a given entity and technical field.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')
            technical_field: Technical database field name (e.g., 'root_cause')

        Returns:
            Business display field name (e.g., 'Root Cause', 'Action Request Number:')
        """
        if not self._unified_mappings:
            return None

        entity_mappings = self._unified_mappings.get("unified_field_references", {}).get(entity_name)
        if not entity_mappings:
            return None

        business_fields = entity_mappings.get("business_fields", {})
        return business_fields.get(technical_field)

    def get_raw_data_field(self, entity_name: str, technical_field: str) -> Optional[str]:
        """
        Get raw data field name for a given entity and technical field.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')
            technical_field: Technical database field name (e.g., 'action_request_number')

        Returns:
            Raw data field name (e.g., 'Action Request Number:', 'Root Cause')
        """
        if not self._unified_mappings:
            return None

        entity_mappings = self._unified_mappings.get("unified_field_references", {}).get(entity_name)
        if not entity_mappings:
            return None

        raw_data_fields = entity_mappings.get("raw_data_fields", {})
        return raw_data_fields.get(technical_field)

    def resolve_field_mapping(self, entity_name: str, source_type: str, target_type: str, field_name: str) -> Optional[str]:
        """
        Universal field mapping resolver that translates between all three naming conventions.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')
            source_type: Source field type ('technical', 'business', 'raw_data')
            target_type: Target field type ('technical', 'business', 'raw_data')
            field_name: Field name in source format

        Returns:
            Field name in target format
        """
        if source_type == target_type:
            return field_name

        # First get technical field name (our unified reference)
        if source_type == 'technical':
            technical_field = field_name
        else:
            technical_field = self.get_technical_field(entity_name, field_name)

        if not technical_field:
            return None

        # Then get target field name
        if target_type == 'technical':
            return technical_field
        elif target_type == 'business':
            return self.get_business_field(entity_name, technical_field)
        elif target_type == 'raw_data':
            return self.get_raw_data_field(entity_name, technical_field)

        return None

    def get_entity_field_mappings(self, entity_name: str) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Get complete field mappings for a specific entity across all naming conventions.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')

        Returns:
            Dictionary with technical_fields, business_fields, and raw_data_fields
        """
        if not self._unified_mappings:
            return None

        return self._unified_mappings.get("unified_field_references", {}).get(entity_name)

    def get_cascade_labeling_config(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """
        Get unified cascade labeling configuration for an entity using technical field names.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')

        Returns:
            Cascade labeling configuration with technical field names
        """
        if not self._unified_mappings:
            return None

        cascade_config = self._unified_mappings.get("unified_cascade_labeling", {}).get(entity_name)
        if cascade_config:
            logger.debug(f"Retrieved cascade config for {entity_name}: {cascade_config}")

        return cascade_config

    def get_all_technical_fields(self, entity_name: str) -> List[str]:
        """
        Get all technical field names for an entity.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')

        Returns:
            List of technical field names
        """
        entity_mappings = self.get_entity_field_mappings(entity_name)
        if not entity_mappings:
            return []

        return list(entity_mappings.get("technical_fields", {}).keys())

    def get_all_business_fields(self, entity_name: str) -> List[str]:
        """
        Get all business field names for an entity.

        Args:
            entity_name: Entity name (e.g., 'RootCause', 'ActionRequest')

        Returns:
            List of business field names
        """
        entity_mappings = self.get_entity_field_mappings(entity_name)
        if not entity_mappings:
            return []

        return list(entity_mappings.get("business_fields", {}).values())

    def validate_field_resolution(self) -> Dict[str, Any]:
        """
        Validate field resolution system for architecture compliance.

        Returns:
            Validation report with statistics and compliance metrics
        """
        if not self._unified_mappings:
            return {"status": "error", "message": "No unified mappings loaded"}

        entities = self._unified_mappings.get("unified_field_references", {})
        cascade_configs = self._unified_mappings.get("unified_cascade_labeling", {})

        validation_report = {
            "status": "success",
            "total_entities": len(entities),
            "entities_with_cascade_config": len(cascade_configs),
            "architecture_compliance": True,
            "field_mapping_consistency": True,
            "errors": [],
            "warnings": []
        }

        # Check each entity for complete field mappings
        for entity_name, entity_mapping in entities.items():
            required_sections = ["technical_fields", "business_fields", "raw_data_fields"]

            for section in required_sections:
                if section not in entity_mapping:
                    validation_report["errors"].append(
                        f"Entity '{entity_name}' missing '{section}' section"
                    )
                    validation_report["architecture_compliance"] = False

            # Check cascade configuration exists
            if entity_name not in cascade_configs:
                validation_report["warnings"].append(
                    f"Entity '{entity_name}' missing cascade labeling configuration"
                )

        return validation_report


# Global field resolver instance for application-wide use
_field_resolver = None

def get_field_resolver(config_path: Optional[str] = None) -> FieldResolver:
    """
    Get global field resolver instance (singleton pattern).

    Args:
        config_path: Optional path to unified field mappings configuration

    Returns:
        Global FieldResolver instance
    """
    global _field_resolver

    if _field_resolver is None:
        _field_resolver = FieldResolver(config_path)

    return _field_resolver


# Convenience functions for common field resolution operations
def get_technical_field(entity_name: str, field_identifier: str) -> Optional[str]:
    """Get technical database field name"""
    return get_field_resolver().get_technical_field(entity_name, field_identifier)

def get_business_field(entity_name: str, technical_field: str) -> Optional[str]:
    """Get business display field name"""
    return get_field_resolver().get_business_field(entity_name, technical_field)

def get_raw_data_field(entity_name: str, technical_field: str) -> Optional[str]:
    """Get raw data field name"""
    return get_field_resolver().get_raw_data_field(entity_name, technical_field)

def resolve_field_mapping(entity_name: str, source_type: str, target_type: str, field_name: str) -> Optional[str]:
    """Universal field mapping resolver"""
    return get_field_resolver().resolve_field_mapping(entity_name, source_type, target_type, field_name)
