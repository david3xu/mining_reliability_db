#!/usr/bin/env python3
"""
Data Transformer for Mining Reliability Database
Transforms raw data to match entity model.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from configs.environment import get_mappings

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transforms raw facility data into entity model format"""

    def __init__(self):
        """Initialize with field mappings from configuration"""
        mappings = get_mappings()

        if not mappings:
            logger.warning("Field mappings not found in configuration")
            self.list_fields = []
            self.field_mappings = {}
            self.list_field_extraction = {"default": "head"}
        else:
            self.list_fields = mappings.get("list_fields", [])
            self.field_mappings = mappings.get("entity_mappings", {})
            self.list_field_extraction = mappings.get("list_field_extraction", {"default": "head"})

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

        for record in records:
            self._transform_record(record, facility_id, transformed)

        for entity_type, entities in transformed["entities"].items():
            logger.info(f"Transformed {len(entities)} {entity_type} entities")

        return transformed

    def _transform_record(self, record: Dict[str, Any], facility_id: str, transformed: Dict[str, Any]) -> None:
        """Transform a single record into entity model format"""
        action_request_number = record.get("Action Request Number:")
        if not action_request_number:
            return

        entity_ids = self._generate_entity_ids(action_request_number)

        # Transform ActionRequest
        action_request = self._transform_entity(record, "ActionRequest")
        action_request["action_request_id"] = entity_ids["action_request_id"]
        action_request["facility_id"] = facility_id
        transformed["entities"]["ActionRequest"].append(action_request)

        # Transform Problem if data exists
        if record.get("What happened?"):
            problem = self._transform_entity(record, "Problem")
            problem["problem_id"] = entity_ids["problem_id"]
            problem["action_request_id"] = entity_ids["action_request_id"]
            transformed["entities"]["Problem"].append(problem)

            self._transform_problem_entities(record, entity_ids, transformed)

            # Transform RootCause if data exists
            if record.get("Root Cause"):
                self._transform_root_cause_chain(record, entity_ids, transformed)

        # Transform Department if data exists
        if record.get("Init. Dept.") or record.get("Rec. Dept."):
            department = self._transform_entity(record, "Department")
            department["dept_id"] = entity_ids["dept_id"]
            department["action_request_id"] = entity_ids["action_request_id"]
            transformed["entities"]["Department"].append(department)

    def _transform_problem_entities(self, record: Dict[str, Any], entity_ids: Dict[str, str], transformed: Dict[str, Any]) -> None:
        """Transform entities connected to Problem"""
        entity_configs = [
            ("Asset", ["Asset Number(s)", "Asset Activity numbers"], "asset_id"),
            ("RecurringStatus", ["Recurring Problem(s)", "Recurring Comment"], "recurring_id"),
            ("AmountOfLoss", ["Amount of Loss"], "loss_id")
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
        root_cause["cause_id"] = entity_ids["cause_id"]
        root_cause["problem_id"] = entity_ids["problem_id"]
        transformed["entities"]["RootCause"].append(root_cause)

        # Transform ActionPlan if data exists
        if record.get("Action Plan"):
            action_plan = self._transform_entity(record, "ActionPlan")
            action_plan["plan_id"] = entity_ids["plan_id"]
            action_plan["root_cause_id"] = entity_ids["cause_id"]
            transformed["entities"]["ActionPlan"].append(action_plan)

            # Transform connected entities
            connected_configs = [
                ("Verification", ["Effectiveness Verification Due Date", "IsActionPlanEffective"], "verification_id"),
                ("Review", ["Is Resp Satisfactory?", "Reviewed Date:"], "review_id"),
                ("EquipmentStrategy", ["If yes, APSS Doc #"], "strategy_id")
            ]

            for entity_type, required_fields, id_field in connected_configs:
                if any(record.get(field) for field in required_fields):
                    entity = self._transform_entity(record, entity_type)
                    entity[id_field] = entity_ids[id_field]
                    entity["action_plan_id"] = entity_ids["plan_id"]
                    transformed["entities"][entity_type].append(entity)

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

    def _generate_entity_ids(self, action_request_number: str) -> Dict[str, str]:
        """Generate IDs for entities based on action request number"""
        request_id = action_request_number.replace('-', '').lower()

        return {
            "action_request_id": f"ar-{request_id}",
            "problem_id": f"prob-{request_id}",
            "cause_id": f"cause-{request_id}",
            "plan_id": f"plan-{request_id}",
            "verification_id": f"ver-{request_id}",
            "dept_id": f"dept-{request_id}",
            "asset_id": f"asset-{request_id}",
            "recurring_id": f"rec-{request_id}",
            "loss_id": f"loss-{request_id}",
            "review_id": f"rev-{request_id}",
            "strategy_id": f"strat-{request_id}"
        }
