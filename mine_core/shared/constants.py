#!/usr/bin/env python3
"""
Simplified Constants for Mining Reliability Database
Core system constants only - field validation moved to field_utils.py
"""

# Database operation constants
DEFAULT_BATCH_SIZE = 5000
MAX_RETRIES = 3
CONNECTION_TIMEOUT = 30

# Default configuration values
DEFAULT_NEO4J_URI = "bolt://localhost:7687"
DEFAULT_NEO4J_USER = "neo4j"
DEFAULT_NEO4J_PASSWORD = "password"
DEFAULT_LOG_LEVEL = "INFO"

# Data processing constants
DEFAULT_DATA_DIR = "./data/facility_data"

# Entity processing order (hierarchical chain + supporting entities)
ENTITY_LOAD_ORDER = [
    "ActionRequest",
    "Problem",
    "RootCause",
    "ActionPlan",
    "Verification",
    "Department",
    "Asset",
    "RecurringStatus",
    "AmountOfLoss",
    "Review",
    "EquipmentStrategy"
]

# Traditional relationship configurations for loader
RELATIONSHIP_CONFIGS = [
    ("ActionRequest", "facility_id", "BELONGS_TO", "Facility", "facility_id"),
    ("Problem", "actionrequest_id", "IDENTIFIED_IN", "ActionRequest", "actionrequest_id"),
    ("RootCause", "problem_id", "ANALYZES", "Problem", "problem_id"),
    ("ActionPlan", "rootcause_id", "RESOLVES", "RootCause", "rootcause_id"),
    ("Verification", "actionplan_id", "VALIDATES", "ActionPlan", "actionplan_id"),
    ("Asset", "problem_id", "INVOLVED_IN", "Problem", "problem_id"),
    ("AmountOfLoss", "problem_id", "QUANTIFIES", "Problem", "problem_id"),
    ("RecurringStatus", "problem_id", "CLASSIFIES", "Problem", "problem_id"),
    ("Department", "actionrequest_id", "ASSIGNED_TO", "ActionRequest", "actionrequest_id"),
    ("Review", "actionplan_id", "EVALUATES", "ActionPlan", "actionplan_id"),
    ("EquipmentStrategy", "actionplan_id", "MODIFIES", "ActionPlan", "actionplan_id")
]

# Field processing priorities by category
FIELD_PRIORITY_CATEGORIES = {
    "critical": [
        "Action Request Number:",
        "Title",
        "What happened?",
        "Root Cause",
        "Action Plan"
    ],
    "high": [
        "Categories",
        "Stage",
        "Complete",
        "IsActionPlanEffective",
        "Initiation Date"
    ],
    "medium": [
        "Asset Number(s)",
        "Init. Dept.",
        "Due Date",
        "Recurring Problem(s)"
    ],
    "low": [
        "Comments",
        "Reason if not Satisfactory",
        "Days Past Due"
    ]
}

# Root cause intelligence configuration
ROOT_CAUSE_PROCESSING = {
    "tail_extraction_delimiters": [";", ",", "|", "\n", " - ", " / ", " and ", " & "],
    "preserve_original": True,
    "enable_causal_correlation": True,
    "primary_field": "root_cause",
    "secondary_field": "root_cause_tail"
}

# Dynamic labeling patterns
LABEL_PATTERNS = {
    "temporal": {
        "pattern": r'\d{4}-\d{2}-\d{2}',
        "prefix": "Date_"
    },
    "identifier": {
        "pattern": r'^[A-Z]{2,3}-\d{3,4}',
        "prefix": "ID_"
    },
    "category": {
        "pattern": r'^[A-Z][a-z]+$',
        "prefix": ""
    },
    "status": {
        "values": ["Open", "Closed", "InProgress", "Complete", "Pending"],
        "prefix": "Status_"
    },
    "boolean": {
        "values": ["true", "false", "yes", "no", "completed", "pending"],
        "prefix": "Is_"
    }
}

# Field value normalization rules
FIELD_NORMALIZATION = {
    "boolean_true_values": {
        "true", "yes", "1", "completed", "effective", "satisfactory",
        "applicable", "required", "success", "positive"
    },
    "boolean_false_values": {
        "false", "no", "0", "pending", "ineffective", "unsatisfactory",
        "not applicable", "not required", "failure", "negative"
    },
    "status_mappings": {
        "in progress": "InProgress",
        "in-progress": "InProgress",
        "not started": "NotStarted",
        "not_started": "NotStarted"
    }
}

# Entity creation thresholds
ENTITY_CREATION_THRESHOLDS = {
    "min_field_length": 3,
    "max_label_length": 50,
    "required_field_ratio": 0.3,  # At least 30% of mapped fields must have values
    "skip_common_values": {
        "unknown", "n/a", "none", "null", "empty", "tbd", "pending"
    }
}

# Field analytics categories for operational intelligence
ANALYTICS_CATEGORIES = {
    "causal_intelligence": [
        "Root Cause", "Obj. Evidence", "Recurring Problem(s)"
    ],
    "performance_indicators": [
        "Days Past Due", "Complete", "IsActionPlanEffective",
        "Is Resp Satisfactory?"
    ],
    "classification_dimensions": [
        "Categories", "Action Types", "Stage", "Operating Centre",
        "Init. Dept.", "Rec. Dept."
    ],
    "resolution_tracking": [
        "Action Plan", "Recom.Action", "Due Date", "Completion Date",
        "Effectiveness Verification Due Date"
    ]
}

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Neo4j query optimization settings
QUERY_OPTIMIZATION = {
    "batch_relationship_creation": True,
    "use_periodic_commit": True,
    "periodic_commit_size": 1000,
    "create_indexes_for_labels": True,
    "enable_query_caching": True
}

# Validation rules for data quality
VALIDATION_RULES = {
    "required_field_coverage": {
        "ActionRequest": ["Action Request Number:", "Title"],
        "Problem": ["What happened?"],
        "RootCause": ["Root Cause"],
        "ActionPlan": ["Action Plan"]
    },
    "field_dependency_rules": [
        ("Complete", "true", "Completion Date", "required"),
        ("IsActionPlanEffective", "true", "Action Plan Verification Date:", "required"),
        ("Is Resp Satisfactory?", "false", "Reason if not Satisfactory", "required")
    ],
    "causal_intelligence_rules": [
        ("Root Cause", "required", "root_cause", "primary_analysis"),
        ("Root Cause", "tail_extraction", "root_cause_tail", "secondary_analysis")
    ]
}

# Simplified processing configuration (no multi-value complexity)
PROCESSING_CONFIG = {
    "single_value_only": True,
    "enable_root_cause_intelligence": True,
    "dynamic_labeling": True,
    "missing_data_tracking": True,
    "cascade_entity_creation": True
}
