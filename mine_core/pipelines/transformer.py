#!/usr/bin/env python3
"""
Data Transformer for Mining Reliability Database
Transforms raw data to match entity model.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from configs.settings import get_config

# Configure logging
logger = logging.getLogger(__name__)

class DataTransformer:
    """Transforms raw facility data into entity model format"""

    def __init__(self):
        """Initialize with field mappings from configuration"""
        # Get field mappings from configuration
        mappings = get_config("mappings")

        if not mappings:
            logger.warning("Field mappings not found in configuration, using empty defaults")
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

        # Initialize transformed data structure
        transformed = {
            "facility": {
                "facility_id": facility_id,
                "facility_name": facility_id,
                "active": True
            },
            "entities": {
                "ActionRequest": [],
                "Problem": [],
                "RootCause": [],
                "ActionPlan": [],
                "Verification": [],
                "Department": [],
                "Asset": [],
                "RecurringStatus": [],
                "AmountOfLoss": [],
                "Review": [],
                "EquipmentStrategy": []
            }
        }

        # Process each record
        for record in records:
            self._transform_record(record, facility_id, transformed)

        # Log transformation results
        for entity_type, entities in transformed["entities"].items():
            logger.info(f"Transformed {len(entities)} {entity_type} entities")

        return transformed

    def _transform_record(self, record: Dict[str, Any], facility_id: str,
                          transformed: Dict[str, Any]) -> None:
        """Transform a single record into entity model format"""
        # Get action request number
        action_request_number = record.get("Action Request Number:")
        if not action_request_number:
            return

        # Generate entity IDs
        entity_ids = self._generate_entity_ids(action_request_number)

        # Transform ActionRequest
        action_request = self._transform_entity(record, "ActionRequest")
        action_request["action_request_id"] = entity_ids["action_request_id"]
        action_request["facility_id"] = facility_id
        transformed["entities"]["ActionRequest"].append(action_request)

        # Transform Problem if required fields exist
        if record.get("What happened?"):
            problem = self._transform_entity(record, "Problem")
            problem["problem_id"] = entity_ids["problem_id"]
            problem["action_request_id"] = entity_ids["action_request_id"]
            transformed["entities"]["Problem"].append(problem)

            # Transform entities connected to Problem
            self._transform_problem_entities(record, entity_ids, transformed)

            # Transform RootCause if required fields exist
            if record.get("Root Cause"):
                self._transform_root_cause_chain(record, entity_ids, transformed)

        # Transform Department if required fields exist
        if record.get("Init. Dept.") or record.get("Rec. Dept."):
            department = self._transform_entity(record, "Department")
            department["dept_id"] = entity_ids["dept_id"]
            department["action_request_id"] = entity_ids["action_request_id"]
            transformed["entities"]["Department"].append(department)

    def _transform_problem_entities(self, record: Dict[str, Any], entity_ids: Dict[str, str],
                                   transformed: Dict[str, Any]) -> None:
        """Transform entities connected to Problem"""
        # Transform Asset if required fields exist
        if record.get("Asset Number(s)") or record.get("Asset Activity numbers"):
            asset = self._transform_entity(record, "Asset")
            asset["asset_id"] = entity_ids["asset_id"]
            asset["problem_id"] = entity_ids["problem_id"]
            transformed["entities"]["Asset"].append(asset)

        # Transform RecurringStatus if required fields exist
        if record.get("Recurring Problem(s)") or record.get("Recurring Comment"):
            recurring_status = self._transform_entity(record, "RecurringStatus")
            recurring_status["recurring_id"] = entity_ids["recurring_id"]
            recurring_status["problem_id"] = entity_ids["problem_id"]
            transformed["entities"]["RecurringStatus"].append(recurring_status)

        # Transform AmountOfLoss if required fields exist
        if record.get("Amount of Loss"):
            amount_of_loss = self._transform_entity(record, "AmountOfLoss")
            amount_of_loss["loss_id"] = entity_ids["loss_id"]
            amount_of_loss["problem_id"] = entity_ids["problem_id"]
            transformed["entities"]["AmountOfLoss"].append(amount_of_loss)

    def _transform_root_cause_chain(self, record: Dict[str, Any], entity_ids: Dict[str, str],
                                   transformed: Dict[str, Any]) -> None:
        """Transform RootCause and connected entities"""
        # Transform RootCause
        root_cause = self._transform_entity(record, "RootCause")
        root_cause["cause_id"] = entity_ids["cause_id"]
        root_cause["problem_id"] = entity_ids["problem_id"]
        transformed["entities"]["RootCause"].append(root_cause)

        # Transform ActionPlan if required fields exist
        if record.get("Action Plan"):
            action_plan = self._transform_entity(record, "ActionPlan")
            action_plan["plan_id"] = entity_ids["plan_id"]
            action_plan["root_cause_id"] = entity_ids["cause_id"]
            transformed["entities"]["ActionPlan"].append(action_plan)

            # Transform Verification if required fields exist
            if record.get("Effectiveness Verification Due Date") or record.get("IsActionPlanEffective"):
                verification = self._transform_entity(record, "Verification")
                verification["verification_id"] = entity_ids["verification_id"]
                verification["action_plan_id"] = entity_ids["plan_id"]
                transformed["entities"]["Verification"].append(verification)

            # Transform Review if required fields exist
            if record.get("Is Resp Satisfactory?") or record.get("Reviewed Date:"):
                review = self._transform_entity(record, "Review")
                review["review_id"] = entity_ids["review_id"]
                review["action_plan_id"] = entity_ids["plan_id"]
                transformed["entities"]["Review"].append(review)

            # Transform EquipmentStrategy if required fields exist
            if record.get("If yes, APSS Doc #"):
                equipment_strategy = self._transform_entity(record, "EquipmentStrategy")
                equipment_strategy["strategy_id"] = entity_ids["strategy_id"]
                equipment_strategy["action_plan_id"] = entity_ids["plan_id"]
                transformed["entities"]["EquipmentStrategy"].append(equipment_strategy)

    def _transform_entity(self, record: Dict[str, Any], entity_type: str) -> Dict[str, Any]:
        """Transform data for a specific entity type"""
        entity = {}

        # Get field mappings for this entity type
        field_mappings = self.field_mappings.get(entity_type, {})

        # Map fields according to the mapping definition
        for target_field, source_field in field_mappings.items():
            if source_field in record:
                value = record[source_field]

                # Handle list fields with special extraction logic
                if source_field in self.list_fields:
                    value = self._extract_list_field_value(source_field, value)

                # Skip empty values
                if value is None or (isinstance(value, str) and not value.strip()):
                    continue

                entity[target_field] = value

        return entity

    def _extract_list_field_value(self, field_name: str, value: Union[str, List[str]]) -> Optional[str]:
        """Apply field-specific extraction rules to list values"""
        # If it's not a list or empty, return as is
        if not isinstance(value, list) or not value:
            return value

        # Get extraction method for this field
        extraction_method = self.list_field_extraction.get(field_name,
                                                          self.list_field_extraction.get("default", "head"))

        # Apply extraction method
        if extraction_method == "tail" and len(value) > 1:
            return value[1]  # Return second item
        else:
            return value[0]  # Return first item (head)

    def _generate_entity_ids(self, action_request_number: str) -> Dict[str, str]:
        """Generate IDs for entities based on action request number"""
        # Use action request number as a seed for IDs
        # This ensures related entities have consistently derived IDs
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
