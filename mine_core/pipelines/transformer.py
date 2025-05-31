#!/usr/bin/env python3
"""
Simplified Data Transformer for Mining Reliability Database
Clean implementation without backwards compatibility pollution.
"""

import logging
from typing import Dict, List, Any, Optional
from configs.environment import get_mappings, get_entity_names
from mine_core.shared.common import handle_error
from mine_core.shared.field_utils import (
    has_real_value,
    is_missing_data_indicator,
    get_missing_indicator,
    clean_label,
    extract_root_cause_tail
)

logger = logging.getLogger(__name__)

class DataTransformer:
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

        # Extract tail value for enhanced causal analysis using centralized utility
        original_cause = record.get("Root Cause", "")
        root_cause["root_cause_tail"] = extract_root_cause_tail(original_cause)

        return root_cause

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
                    entity[target_field] = extract_root_cause_tail(value)
                elif has_real_value(value):
                    entity[target_field] = self._normalize_value(value)
                else:
                    entity[target_field] = get_missing_indicator(source_field)
            else:
                entity[target_field] = get_missing_indicator(source_field)

        # Add semantic display name for graph visualization
        entity["name"] = self._get_display_name(entity, entity_type)

        # Apply cascade labeling
        dynamic_label = self._apply_cascade_labeling(entity, entity_type)
        if dynamic_label:
            entity["_dynamic_label"] = dynamic_label

        return entity

    def _get_display_name(self, entity_data: Dict[str, Any], entity_type: str) -> str:
        """Generate semantic display name for graph visualization"""
        # Priority field mapping for meaningful node labels
        display_priorities = {
            "Problem": ["what_happened", "requirement"],
            "RootCause": ["root_cause", "objective_evidence"],
            "ActionRequest": ["title", "categories", "action_request_number"],
            "ActionPlan": ["action_plan", "recommended_action"],
            "Verification": ["is_action_plan_effective", "action_plan_eval_comment"],
            "Department": ["init_dept", "rec_dept"],
            "Asset": ["asset_numbers", "asset_activity_numbers"],
            "Facility": ["facility_name", "facility_id"]
        }

        priority_fields = display_priorities.get(entity_type, [])

        # Try priority fields in order
        for field in priority_fields:
            value = entity_data.get(field)
            if has_real_value(value) and not is_missing_data_indicator(str(value)):
                # Truncate long text for display
                display_value = str(value).strip()
                return display_value[:50] + "..." if len(display_value) > 50 else display_value

        # Fallback to entity type
        return entity_type

    def _apply_cascade_labeling(self, entity_data: Dict[str, Any], entity_type: str) -> Optional[str]:
        """Apply simplified cascade labeling strategy"""
        cascade_config = self.cascade_config.get(entity_type, {})
        priority_fields = cascade_config.get("label_priority", [])

        # Try priority fields in order
        for field_name in priority_fields:
            value = entity_data.get(field_name)
            if has_real_value(value) and not is_missing_data_indicator(value):
                return clean_label(str(value))

        # Fallback to entity type
        return entity_type

    def _has_required_data(self, entity_name: str, record: Dict) -> bool:
        """Check if record has required data for entity creation"""
        cascade_config = self.cascade_config.get(entity_name, {})
        required_fields = cascade_config.get("required_fields", [])

        if not required_fields:
            return False

        # Check if any required field has real value using centralized validation
        for field_name in required_fields:
            value = record.get(field_name)
            if has_real_value(value):
                return True

        return False

    def _normalize_value(self, value: Any) -> Any:
        """Normalize field value for storage"""
        if isinstance(value, str):
            return value.strip()
        return value

    def _generate_base_id(self, action_request_number: str, facility_id: str, record_index: int = 0) -> str:
        """Generate base ID for all related entities"""
        clean_number = clean_label(action_request_number)
        clean_facility = clean_label(facility_id)

        if record_index > 0:
            return f"{clean_facility}_{clean_number}_{record_index}"
        return f"{clean_facility}_{clean_number}"
