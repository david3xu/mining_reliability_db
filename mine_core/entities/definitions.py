#!/usr/bin/env python3
"""
Entity Definitions for Mining Reliability Database
Defines data structures and relationships for the entity model.
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, ClassVar

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@dataclass
class Entity:
    """Base class for all entities"""
    id: str

    # Class variable to track entity types
    _entity_types: ClassVar[Set[str]] = set()

    def __init_subclass__(cls, **kwargs):
        """Register entity subclasses"""
        super().__init_subclass__(**kwargs)
        Entity._entity_types.add(cls.__name__)

    @classmethod
    def get_entity_types(cls) -> Set[str]:
        """Get all registered entity types"""
        return cls._entity_types

@dataclass
class Facility(Entity):
    """Facility entity definition"""
    facility_id: str
    facility_name: str
    location: Optional[str] = None
    active: bool = True

@dataclass
class ActionRequest(Entity):
    """ActionRequest entity definition"""
    action_request_id: str
    facility_id: str
    action_request_number: str
    title: str
    initiation_date: str
    action_types: Optional[str] = None
    categories: Optional[str] = None
    requested_response_time: Optional[str] = None
    stage: Optional[str] = None
    operating_centre: Optional[str] = None
    past_due_status: Optional[str] = None
    days_past_due: Optional[int] = None

@dataclass
class Problem(Entity):
    """Problem entity definition"""
    problem_id: str
    action_request_id: str
    what_happened: str
    requirement: Optional[str] = None

@dataclass
class RootCause(Entity):
    """RootCause entity definition"""
    cause_id: str
    problem_id: str
    root_cause: str
    objective_evidence: Optional[str] = None

@dataclass
class ActionPlan(Entity):
    """ActionPlan entity definition"""
    plan_id: str
    root_cause_id: str
    action_plan: str
    recommended_action: Optional[str] = None
    immediate_containment: Optional[str] = None
    due_date: Optional[str] = None
    complete: bool = False
    completion_date: Optional[str] = None
    comments: Optional[str] = None
    response_date: Optional[str] = None
    response_revision_date: Optional[str] = None
    did_plan_require_strategy_change: bool = False
    are_there_corrective_actions_to_update: bool = False

@dataclass
class Verification(Entity):
    """Verification entity definition"""
    verification_id: str
    action_plan_id: str
    effectiveness_verification_due_date: Optional[str] = None
    is_action_plan_effective: Optional[bool] = None
    action_plan_eval_comment: Optional[str] = None
    action_plan_verification_date: Optional[str] = None

@dataclass
class Department(Entity):
    """Department entity definition"""
    dept_id: str
    action_request_id: str
    init_dept: Optional[str] = None
    rec_dept: Optional[str] = None

@dataclass
class Asset(Entity):
    """Asset entity definition"""
    asset_id: str
    problem_id: str
    asset_numbers: Optional[str] = None
    asset_activity_numbers: Optional[str] = None

@dataclass
class RecurringStatus(Entity):
    """RecurringStatus entity definition"""
    recurring_id: str
    problem_id: str
    recurring_problems: bool = False
    recurring_comment: Optional[str] = None

@dataclass
class AmountOfLoss(Entity):
    """AmountOfLoss entity definition"""
    loss_id: str
    problem_id: str
    amount_of_loss: Optional[str] = None

@dataclass
class Review(Entity):
    """Review entity definition"""
    review_id: str
    action_plan_id: str
    is_resp_satisfactory: Optional[bool] = None
    reason_if_not_satisfactory: Optional[str] = None
    reviewed_date: Optional[str] = None
    did_plan_require_change_review: bool = False

@dataclass
class EquipmentStrategy(Entity):
    """EquipmentStrategy entity definition"""
    strategy_id: str
    action_plan_id: str
    apss_doc_number: Optional[str] = None

def get_entity_definitions() -> Dict[str, Any]:
    """Get entity definitions from schema file"""
    try:
        # Try to find schema file
        script_dir = Path(__file__).resolve().parent.parent.parent
        schema_paths = [
            script_dir / "configs" / "model_schema.json",
            script_dir / "model_schema.json"
        ]

        schema_file = None
        for path in schema_paths:
            if path.exists():
                schema_file = path
                break

        if not schema_file:
            logger.warning("Schema file not found, using built-in definitions")
            return {entity_type: globals()[entity_type] for entity_type in Entity.get_entity_types()}

        # Load schema file
        with open(schema_file, 'r') as f:
            schema = json.load(f)

        # Extract entity definitions
        entity_defs = {}
        for entity in schema.get("entities", []):
            entity_type = entity["name"]
            if entity_type in globals():
                entity_defs[entity_type] = globals()[entity_type]

        return entity_defs

    except Exception as e:
        logger.error(f"Error loading entity definitions: {e}")
        return {entity_type: globals()[entity_type] for entity_type in Entity.get_entity_types()}
