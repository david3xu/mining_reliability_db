#!/usr/bin/env python3
"""
Simplified Data Transformer for Mining Reliability Database
Clean single-value field processing with enhanced root cause intelligence.
"""

import logging
from typing import Dict, List, Any, Optional
from configs.environment import get_mappings, get_entity_names
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

class SimplifiedTransformer:
    """Streamlined transformer for clean datasets with causal intelligence"""

    def __init__(self, mappings=None, use_config=True):
        """Initialize with simplified configuration"""
        if use_config:
            self.mappings = mappings or get_mappings()
        else:
            self.mappings = mappings or {}

        # Simplified configuration
        self.field_mappings = self.mappings.get("entity_mappings", {})
        self.cascade_config = self.mappings.get("cascade_labeling", {})

        # Entity names from schema
        self.entity_names = get_entity_names()

    def transform_facility_data(self, facility_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform clean facility data with causal intelligence"""
        facility_id = facility_data.get("facility_id", "unknown")
        records = facility_data.get("records", [])

        # Initialize simplified structure
        transformed = {
            "facility": {
                "facility_id": facility_id,
                "facility_name": facility_id,
                "active": True
            },
            "entities": {entity_name: [] for entity_name in self.entity_names}
        }

        # Process each record with simplified logic
        for record_index, record in enumerate(records):
            try:
                self._transform_record(record, facility_id, transformed, record_index)
            except Exception as e:
                handle_error(logger, e, f"transforming record {record_index}")

        # Log transformation results
        total_entities = sum(len(entities) for entities in transformed["entities"].values())
        logger.info(f"Transformed {total_entities} entities from {len(records)} records")
        return transformed

    def _transform_record(self, record: Dict[str, Any], facility_id: str,
                         transformed: Dict[str, Any], record_index: int = 0) -> None:
        """Transform single record with simplified processing"""
        action_request_number = record.get("Action Request Number:")
        if not action_request_number:
            logger.warning(f"No action request number in record {record_index}")
            return

        base_id = self._generate_base_id(action_request_number, facility_id, record_index)

        # Create entities in hierarchical order
        self._create_hierarchical_entities(record, base_id, facility_id, transformed)

    def _create_hierarchical_entities(self, record: Dict[str, Any], base_id: str,
                                    facility_id: str, transformed: Dict[str, Any]) -> None:
        """Create entities following hierarchical workflow pattern"""

        # ActionRequest (always created)
        action_request = self._create_entity_with_labeling(record, "ActionRequest", base_id)
        action_request["facility_id"] = facility_id
        transformed["entities"]["ActionRequest"].append(action_request)

        # Problem (if data exists)
        if self._has_required_data("Problem", record):
            problem = self._create_entity_with_labeling(record, "Problem", base_id)
            problem["actionrequest_id"] = action_request["actionrequest_id"]
            transformed["entities"]["Problem"].append(problem)

            # Problem-connected entities
            self._create_problem_entities(record, base_id, transformed)

            # RootCause (if data exists) - with intelligence enhancement
            if self._has_required_data("RootCause", record):
                root_cause = self._create_root_cause_with_intelligence(record, base_id)
                root_cause["problem_id"] = problem["problem_id"]
                transformed["entities"]["RootCause"].append(root_cause)

                # ActionPlan and downstream entities
                self._create_action_plan_chain(record, base_id, transformed)

        # Department (if data exists)
        if self._has_required_data("Department", record):
            department = self._create_entity_with_labeling(record, "Department", base_id)
            department["actionrequest_id"] = action_request["actionrequest_id"]
            transformed["entities"]["Department"].append(department)

    def _create_root_cause_with_intelligence(self, record: Dict[str, Any], base_id: str) -> Dict[str, Any]:
        """Create RootCause entity with enhanced causal intelligence"""
        root_cause = self._create_entity_with_labeling(record, "RootCause", base_id)

        # Extract tail value for enhanced causal analysis
        original_cause = record.get("Root Cause", "")
        root_cause["root_cause_tail"] = self._extract_tail_value(original_cause)

        return root_cause

    def _extract_tail_value(self, value: str) -> str:
        """Extract tail component from root cause for causal intelligence"""
        if not value or isinstance(value, str) and not value.strip():
            return "NOT_SPECIFIED"

        str_value = str(value).strip()

        # Split on common delimiters and extract tail (final) component
        delimiters = [';', ',', '|', '\n', ' - ', ' / ', ' and ', ' & ']

        for delimiter in delimiters:
            if delimiter in str_value:
                parts = [part.strip() for part in str_value.split(delimiter) if part.strip()]
                if len(parts) > 1:
                    return parts[-1]  # Return tail item
                break

        # No delimiters found - return original value
        return str_value

    def _create_problem_entities(self, record: Dict[str, Any], base_id: str,
                               transformed: Dict[str, Any]) -> None:
        """Create entities connected to Problem"""
        entity_configs = [
            ("Asset", ["Asset Number(s)", "Asset Activity numbers"], "asset_id"),
            ("RecurringStatus", ["Recurring Problem(s)", "Recurring Comment"], "recurringstatus_id"),
            ("AmountOfLoss", ["Amount of Loss"], "amountofloss_id")
        ]

        for entity_type, required_fields, id_field in entity_configs:
            if any(record.get(field) for field in required_fields):
                entity = self._create_entity_with_labeling(record, entity_type, base_id)
                entity["problem_id"] = f"problem-{base_id}"
                transformed["entities"][entity_type].append(entity)

    def _create_action_plan_chain(self, record: Dict[str, Any], base_id: str,
                                transformed: Dict[str, Any]) -> None:
        """Create ActionPlan and connected entities"""
        # ActionPlan
        if self._has_required_data("ActionPlan", record):
            action_plan = self._create_entity_with_labeling(record, "ActionPlan", base_id)
            action_plan["rootcause_id"] = f"rootcause-{base_id}"
            transformed["entities"]["ActionPlan"].append(action_plan)

            # Connected entities
            connected_configs = [
                ("Verification", ["Effectiveness Verification Due Date", "IsActionPlanEffective"], "verification_id"),
                ("Review", ["Is Resp Satisfactory?", "Reviewed Date:"], "review_id"),
                ("EquipmentStrategy", ["If yes, APSS Doc #"], "equipmentstrategy_id")
            ]

            for entity_type, required_fields, id_field in connected_configs:
                if any(record.get(field) for field in required_fields):
                    entity = self._create_entity_with_labeling(record, entity_type, base_id)
                    entity["actionplan_id"] = action_plan["actionplan_id"]
                    transformed["entities"][entity_type].append(entity)

    def _create_entity_with_labeling(self, record: Dict[str, Any], entity_type: str, base_id: str) -> Dict[str, Any]:
        """Create entity with complete properties and dynamic labeling"""
        entity = {}

        # Add primary ID
        primary_id_field = f"{entity_type.lower()}_id"
        entity[primary_id_field] = f"{entity_type.lower()}-{base_id}"

        # Map all fields with missing data indicators
        field_mappings = self.field_mappings.get(entity_type, {})
        for target_field, source_field in field_mappings.items():
            if source_field in record:
                value = record[source_field]

                # Special handling for root_cause_tail
                if target_field == "root_cause_tail":
                    entity[target_field] = self._extract_tail_value(value)
                elif self._has_real_value(value):
                    entity[target_field] = self._normalize_value(value)
                else:
                    entity[target_field] = self._get_missing_indicator(source_field)
            else:
                entity[target_field] = self._get_missing_indicator(source_field)

        # Apply cascade labeling
        dynamic_label = self._apply_cascade_labeling(entity, entity_type)
        if dynamic_label:
            entity["_dynamic_label"] = dynamic_label

        return entity

    def _apply_cascade_labeling(self, entity_data: Dict[str, Any], entity_type: str) -> Optional[str]:
        """Apply simplified cascade labeling strategy"""
        cascade_config = self.cascade_config.get(entity_type, {})
        priority_fields = cascade_config.get("label_priority", [])

        # Try priority fields in order
        for field_name in priority_fields:
            value = entity_data.get(field_name)
            if self._has_real_value(value) and not self._is_missing_indicator(value):
                return self._clean_label(str(value))

        # Fallback to entity type
        return entity_type

    def _has_required_data(self, entity_name: str, record: Dict) -> bool:
        """Check if record has required data for entity creation"""
        cascade_config = self.cascade_config.get(entity_name, {})
        required_fields = cascade_config.get("required_fields", [])

        if not required_fields:
            return False

        # Check if any required field has real value
        for field_name in required_fields:
            value = record.get(field_name)
            if self._has_real_value(value):
                return True

        return False

    def _has_real_value(self, value: Any) -> bool:
        """Check if value contains meaningful data"""
        if value is None:
            return False
        if isinstance(value, str):
            cleaned = value.strip().lower()
            return cleaned not in {"", "null", "n/a", "unknown", "data_not_available", "not_specified", "not_applicable"}
        return True

    def _is_missing_indicator(self, value: str) -> bool:
        """Check if value is a missing data indicator"""
        if not isinstance(value, str):
            return False
        return value in {"DATA_NOT_AVAILABLE", "NOT_SPECIFIED", "NOT_APPLICABLE"}

    def _get_missing_indicator(self, field_name: str) -> str:
        """Get appropriate missing data indicator for field"""
        field_lower = field_name.lower()
        if "date" in field_lower or "time" in field_lower:
            return "DATA_NOT_AVAILABLE"
        elif "comment" in field_lower or "description" in field_lower:
            return "NOT_SPECIFIED"
        else:
            return "DATA_NOT_AVAILABLE"

    def _normalize_value(self, value: Any) -> Any:
        """Normalize field value for storage"""
        if isinstance(value, str):
            return value.strip()
        return value

    def _clean_label(self, value: str) -> str:
        """Clean value for Neo4j label compatibility"""
        import re
        if not isinstance(value, str):
            value = str(value)

        # Remove special characters, keep alphanumeric and underscores
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '', value.replace(' ', '_').replace('-', '_'))

        # Ensure starts with letter
        if cleaned and cleaned[0].isdigit():
            cleaned = f"_{cleaned}"

        # Limit length
        return cleaned[:50] if cleaned else "UnknownValue"

    def _generate_base_id(self, action_request_number: str, facility_id: str, record_index: int = 0) -> str:
        """Generate base ID for all related entities"""
        clean_number = self._clean_label(action_request_number)
        clean_facility = self._clean_label(facility_id)

        if record_index > 0:
            return f"{clean_facility}_{clean_number}_{record_index}"
        return f"{clean_facility}_{clean_number}"

# Backward compatibility
DataTransformer = SimplifiedTransformer
