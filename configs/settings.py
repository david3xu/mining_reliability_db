"""
Configuration settings for the mining reliability database.
"""

# Database settings
DB_CONFIG = {
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "password"
}

# Entity settings
ENTITY_SETTINGS = {
    "primary_key_suffix": "_id",
    "relationship_prefix": "HAS_",
    "default_properties": {
        "created_at": None,
        "updated_at": None,
        "active": True
    }
}

# Field mapping settings
FIELD_MAPPINGS = {
    "ActionRequest": {
        "action_request_number": "number",
        "title": "title",
        "initiation_date": "date",
        "stage": "stage",
        "categories": "categories"
    },
    "Problem": {
        "what_happened": "description",
        "requirement": "requirement"
    },
    "RootCause": {
        "root_cause": "causes"
    }
}

# List field settings
LIST_FIELDS = {
    "RootCause": ["causes"],
    "ActionPlan": ["actions"],
    "Verification": ["evidence"]
}
