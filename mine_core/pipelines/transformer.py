#!/usr/bin/env python3
"""
Data Transformer for Mining Reliability Database
Transforms raw data to match entity model - CORRECTED VERSION
"""

import logging
from typing import Dict, List, Any, Optional, Union
from configs.environment import get_mappings, get_schema

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transforms raw facility data into entity model format"""

    def __init__(self, mappings=None, schema=None, use_config=True):
        """Initialize with field mappings from configuration or provided mappings"""
        if use_config:
            self.mappings = mappings or get_mappings()
            self.schema = schema or get_schema()
        else:
            self.mappings = mappings or {}
            self.schema = schema or {}

        if not self.mappings:
            logger.warning("Field mappings not found in configuration")
            self.list_fields = []
            self.field_mappings = {}
            self.list_field_extraction = {"default": "head"}
        else:
            self.list_fields = self.mappings.get("list_fields", [])
            self.field_mappings = self.mappings.get("entity_mappings", {})
            self.list_field_extraction = self.mappings.get("list_field_extraction", {"default": "head"})

        # Get entity info from schema
        self.entities = {entity["name"]: entity for entity in self.schema.get("entities", [])}

    def transform_facility_data(self, facility_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform facility data into entity model format"""
        facility_id = facility_data.get("facility_id", "unknown")
        records = facility_data.get("records", [])

        transformed = {
            "facility": {
                "facility_id": facility_id,
                "facility_name": facility_id,
                "active": True
            },
            "entities": {
                "ActionRequest": [], "Problem": [], "RootCause": [], "ActionPlan": [],
                "Verification": [], "Department": [], "Asset": [], "RecurringStatus": [],
                "AmountOfLoss": [], "Review": [], "EquipmentStrategy": []
            }
        }

        # Track action request numbers to handle duplicates
        action_request_counts = {}

        for record_index, record in enumerate(records):
            action_request_number = record.get("Action Request Number:")
            if not action_request_number:
                continue

            # Handle duplicate action request numbers
            if action_request_number in action_request_counts:
                action_request_counts[action_request_number] += 1
                sequence = action_request_counts[action_request_number]
            else:
                action_request_counts[action_request_number] = 0
                sequence = 0

            self._transform_record(record, facility_id, transformed, sequence)

        for entity_type, entities in transformed["entities"].items():
            logger.info(f"Transformed {len(entities)} {entity_type} entities")

        return transformed

    def _transform_record(self, record: Dict[str, Any], facility_id: str, transformed: Dict[str, Any], sequence: int = 0) -> None:
        """Transform a single record into entity model format"""
        action_request_number = record.get("Action Request Number:")
        if not action_request_number:
            return

        entity_ids = self._generate_entity_ids(action_request_number, facility_id, sequence)

        # Transform ActionRequest
        action_request = self._transform_entity(record, "ActionRequest")
        action_request["actionrequest_id"] = entity_ids["actionrequest_id"]
        action_request["facility_id"] = facility_id
        transformed["entities"]["ActionRequest"].append(action_request)

        # Transform Problem if data exists
        if self._has_required_data("Problem", record):
            problem = self._transform_entity(record, "Problem")
            problem["problem_id"] = entity_ids["problem_id"]
            problem["actionrequest_id"] = entity_ids["actionrequest_id"]
            transformed["entities"]["Problem"].append(problem)

            self._transform_problem_entities(record, entity_ids, transformed)

            # Transform RootCause if data exists
            if self._has_required_data("RootCause", record):
                self._transform_root_cause_chain(record, entity_ids, transformed)

        # Transform Department if data exists
        if self._has_required_data("Department", record):
            department = self._transform_entity(record, "Department")
            department["department_id"] = entity_ids["department_id"]
            department["actionrequest_id"] = entity_ids["actionrequest_id"]
            transformed["entities"]["Department"].append(department)

    def _transform_problem_entities(self, record: Dict[str, Any], entity_ids: Dict[str, str], transformed: Dict[str, Any]) -> None:
        """Transform entities connected to Problem"""
        entity_configs = [
            ("Asset", ["Asset Number(s)", "Asset Activity numbers"], "asset_id"),
            ("RecurringStatus", ["Recurring Problem(s)", "Recurring Comment"], "recurringstatus_id"),
            ("AmountOfLoss", ["Amount of Loss"], "amountofloss_id")
        ]

        for entity_type, required_fields, id_field in entity_configs:
            if any(record.get(field) for field in required_fields):
                entity = self._transform_entity(record, entity_type)
                entity[id_field] = entity_ids[id_field]
                entity["problem_id"] = entity_ids["problem_id"]
                transformed["entities"][entity_type].append(entity)

    def _transform_root_cause_chain(self, record: Dict[str, Any], entity_ids: Dict[str, str], transformed: Dict[str, Any]) -> None:
        """Transform RootCause and connected entities"""
        # Transform RootCause
        root_cause = self._transform_entity(record, "RootCause")
        root_cause["rootcause_id"] = entity_ids["rootcause_id"]
        root_cause["problem_id"] = entity_ids["problem_id"]
        transformed["entities"]["RootCause"].append(root_cause)

        # Transform ActionPlan if data exists
        if self._has_required_data("ActionPlan", record):
            action_plan = self._transform_entity(record, "ActionPlan")
            action_plan["actionplan_id"] = entity_ids["actionplan_id"]
            action_plan["rootcause_id"] = entity_ids["rootcause_id"]
            transformed["entities"]["ActionPlan"].append(action_plan)

            # Transform connected entities
            connected_configs = [
                ("Verification", ["Effectiveness Verification Due Date", "IsActionPlanEffective"], "verification_id"),
                ("Review", ["Is Resp Satisfactory?", "Reviewed Date:"], "review_id"),
                ("EquipmentStrategy", ["If yes, APSS Doc #"], "equipmentstrategy_id")
            ]

            for entity_type, required_fields, id_field in connected_configs:
                if any(record.get(field) for field in required_fields):
                    entity = self._transform_entity(record, entity_type)
                    entity[id_field] = entity_ids[id_field]
                    entity["actionplan_id"] = entity_ids["actionplan_id"]
                    transformed["entities"][entity_type].append(entity)

    def _has_required_data(self, entity_name: str, record: Dict) -> bool:
        """Check if record has data for this entity type"""
        mappings = self.field_mappings.get(entity_name, {})
        if not mappings:
            logger.debug(f"No field mappings found for entity: {entity_name}")
            return False

        # Check if any mapped fields have data
        for target_field, source_field in mappings.items():
            value = record.get(source_field)
            if value is not None and (not isinstance(value, str) or value.strip()):
                logger.debug(f"Entity {entity_name} has required data: {source_field} = {value}")
                return True

        logger.debug(f"Entity {entity_name} lacks required data")
        return False

    def _transform_entity(self, record: Dict[str, Any], entity_type: str) -> Dict[str, Any]:
        """Transform data for a specific entity type"""
        entity = {}
        field_mappings = self.field_mappings.get(entity_type, {})

        for target_field, source_field in field_mappings.items():
            if source_field in record:
                value = record[source_field]

                if source_field in self.list_fields:
                    value = self._extract_list_field_value(source_field, value)

                if value is None or (isinstance(value, str) and not value.strip()):
                    continue

                entity[target_field] = value

        return entity

    def _extract_list_field_value(self, field_name: str, value: Union[str, List[str]]) -> Optional[str]:
        """Apply field-specific extraction rules to list values"""
        if not isinstance(value, list) or not value:
            return value

        extraction_method = self.list_field_extraction.get(field_name,
                                                          self.list_field_extraction.get("default", "head"))

        if extraction_method == "tail" and len(value) > 1:
            return value[1]
        else:
            return value[0]

    def _generate_entity_ids(self, action_request_number: str, facility_id: str, record_index: int = 0) -> Dict[str, str]:
        """Generate unique IDs for entities based on action request number, facility, and record position"""
        # Create unique base ID: facility + action_request + optional sequence
        clean_number = action_request_number.replace('-', '').replace(' ', '').lower()
        clean_facility = facility_id.replace('-', '').replace(' ', '').lower()

        # Ensure uniqueness across facilities and duplicate action requests
        if record_index > 0:
            base_id = f"{clean_facility}_{clean_number}_{record_index}"
        else:
            base_id = f"{clean_facility}_{clean_number}"

        return {
            "actionrequest_id": f"ar-{base_id}",
            "problem_id": f"prob-{base_id}",
            "rootcause_id": f"cause-{base_id}",
            "actionplan_id": f"plan-{base_id}",
            "verification_id": f"ver-{base_id}",
            "department_id": f"dept-{base_id}",
            "asset_id": f"asset-{base_id}",
            "recurringstatus_id": f"rec-{base_id}",
            "amountofloss_id": f"loss-{base_id}",
            "review_id": f"rev-{base_id}",
            "equipmentstrategy_id": f"strat-{base_id}"
        }
