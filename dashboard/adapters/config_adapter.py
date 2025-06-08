#!/usr/bin/env python3
"""
Configuration Adapter - Pure Configuration Access Layer (Enhanced)
Central configuration adapter with caching and validation.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Pure configuration imports
from configs.environment import (
    get_all_config,
    get_batch_size,
    get_case_study_config,
    get_connection_timeout,
    get_dashboard_chart_config,
    get_dashboard_config,
    get_dashboard_styling_config,
    get_db_config,
    get_entity_classification,
    get_entity_connections,
    get_entity_names,
    get_entity_primary_key,
    get_field_analysis_config,
    get_field_category_display_mapping,
    get_graph_search_config,
    get_mappings,
    get_max_retries,
    get_schema,
    get_stakeholder_queries_config,
    get_system_constants,
    get_workflow_stages_config,
)

# Interface imports for type compliance
from dashboard.adapters.interfaces import (
    ComponentMetadata,
    FacilityData,
    FieldData,
    PortfolioData,
    TimelineData,
    ValidationResult,
)
from mine_core.shared.common import handle_error

__all__ = [
    "ConfigAdapter",
    "get_config_adapter",
    "reset_config_adapter",
    "get_dashboard_metric_card_styling",
    "get_dashboard_chart_styling_template",
    "get_completion_thresholds",
    "get_completion_colors",
    "get_chart_display_config",
    "get_entity_names",
    "handle_error_utility",
    "get_dashboard_chart_config",
    "get_stakeholder_queries_config",
]

logger = logging.getLogger(__name__)


def handle_error_utility(logger: logging.Logger, error: Exception, context: str) -> None:
    """Unified error handling utility for adapters"""
    handle_error(logger, error, context)


class ConfigAdapter:
    """Pure configuration access - no processing logic (Enhanced for Graph Search)"""

    def __init__(self):
        """Initialize configuration adapter"""
        pass

    # Schema Configuration Access

    def get_schema_config(self) -> Dict[str, Any]:
        """Pure access to model schema configuration"""
        try:
            return get_schema()
        except Exception as e:
            handle_error_utility(logger, e, "schema configuration access")
            return {}

    def get_entity_definitions(self) -> Dict[str, Any]:
        """Pure access to entity definitions from schema"""
        try:
            schema = get_schema()
            entities = schema.get("entities", [])
            return {e["name"]: e for e in entities}
        except Exception as e:
            handle_error_utility(logger, e, "entity definitions access")
            return {}

    def get_entity_list(self) -> List[str]:
        """Pure access to entity names list"""
        try:
            return get_entity_names()
        except Exception as e:
            handle_error_utility(logger, e, "entity names access")
            return []

    def get_entity_primary_key_config(self, entity_name: str) -> Optional[str]:
        """Pure access to entity primary key"""
        try:
            return get_entity_primary_key(entity_name)
        except Exception as e:
            handle_error_utility(logger, e, f"primary key access for {entity_name}")
            return None

    # Field Mapping Configuration Access

    def get_field_mappings_config(self) -> Dict[str, Any]:
        """Pure access to field mappings configuration"""
        try:
            return get_mappings()
        except Exception as e:
            handle_error_utility(logger, e, "field mappings configuration access")
            return {}

    def get_entity_mappings(self) -> Dict[str, Any]:
        """Pure access to entity field mappings"""
        try:
            mappings = get_mappings()
            return mappings.get("entity_mappings", {})
        except Exception as e:
            handle_error_utility(logger, e, "entity mappings access")
            return {}

    def get_field_categories(self) -> Dict[str, List[str]]:
        """Pure access to field categories"""
        try:
            mappings = get_mappings()
            return mappings.get("field_categories", {})
        except Exception as e:
            handle_error_utility(logger, e, "field categories access")
            return {}

    def get_cascade_labeling_config(self) -> Dict[str, Any]:
        """Pure access to cascade labeling configuration"""
        try:
            mappings = get_mappings()
            return mappings.get("cascade_labeling", {})
        except Exception as e:
            handle_error_utility(logger, e, "cascade labeling configuration access")
            return {}

    # Workflow Configuration Access

    def get_workflow_stages_config(self) -> Dict[str, Any]:
        """Pure access to workflow stages configuration"""
        try:
            return get_workflow_stages_config()
        except Exception as e:
            handle_error_utility(logger, e, "workflow stages configuration access")
            return {}

    def get_workflow_stage_config(self, stage_number: int) -> Dict[str, Any]:
        """Enhanced stage config with field processing"""
        try:
            workflow_config = self.get_workflow_stages_config()
            stages = workflow_config.get("workflow_stages", [])

            stage_config = next((s for s in stages if s["stage_number"] == stage_number), {})
            business_fields = stage_config.get("business_fields", [])

            # Truncate long field names
            truncated_fields = []
            for field in business_fields:
                if len(field) > 35:
                    truncated_fields.append(field[:32] + "...")
                else:
                    truncated_fields.append(field)

            return {
                "stage_number": stage_config.get("stage_number"),
                "entity_name": stage_config.get("entity_name"),
                "title": stage_config.get("title"),
                "business_fields": truncated_fields,
                "field_count": len(business_fields),
                "card_color": stage_config.get("component_config", {}).get("card_color"),
            }
        except Exception as e:
            handle_error_utility(
                logger, e, f"workflow stage config access for stage {stage_number}"
            )
            return {}

    def get_supporting_entities_config(self) -> List[Dict[str, Any]]:
        """Supporting entities from workflow config"""
        try:
            workflow_config = self.get_workflow_stages_config()
            return workflow_config.get("supporting_entities_field_distribution", [])
        except Exception as e:
            handle_error_utility(logger, e, "supporting entities config access")
            return []

    def get_workflow_display_config(self) -> Dict[str, Any]:
        """Pure access to workflow display configuration"""
        try:
            workflow_config = get_workflow_stages_config()
            return workflow_config.get("display_config", {})
        except Exception as e:
            handle_error_utility(logger, e, "workflow display configuration access")
            return {}

    def get_entity_classification_config(self) -> Dict[str, Any]:
        """Pure access to entity classification configuration"""
        try:
            return get_entity_classification()
        except Exception as e:
            handle_error_utility(logger, e, "entity classification configuration access")
            return {}

    def get_entity_connections_config(self) -> Dict[str, Any]:
        """Pure access to entity connections configuration"""
        try:
            return get_entity_connections()
        except Exception as e:
            handle_error_utility(logger, e, "entity connections configuration access")
            return {}

    # New Graph Search Configuration Access

    def get_graph_search_config(self) -> Dict[str, Any]:
        """Pure access to graph search configuration"""
        try:
            return get_graph_search_config()
        except Exception as e:
            handle_error_utility(logger, e, "graph search configuration access")
            return {}

    def get_stakeholder_queries_config(self) -> Dict[str, Any]:
        """Pure access to stakeholder queries configuration"""
        try:
            return get_stakeholder_queries_config()
        except Exception as e:
            handle_error_utility(logger, e, "stakeholder queries configuration access")
            return {}

    def get_symptom_classification_config(self) -> Dict[str, Any]:
        """Load symptom classification configuration"""
        try:
            config_dir = Path(__file__).parent.parent.parent / "configs"
            config_path = config_dir / "symptom_classification_config.json"

            if not config_path.exists():
                logger.warning(f"Symptom classification config not found: {config_path}")
                return self._get_default_symptom_config()

            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.info("✅ Symptom classification config loaded successfully")
            return config

        except Exception as e:
            handle_error_utility(logger, e, "loading symptom classification config")
            return self._get_default_symptom_config()

    def _get_default_symptom_config(self) -> Dict[str, Any]:
        """Fallback default symptom classification configuration"""
        return {
            "keyword_categories": {
                "equipment_terms": {
                    "terms": ["motor", "pump", "excavator", "bearing", "engine"]
                },
                "symptom_terms": {
                    "terms": ["failed", "leak", "noise", "vibration", "contamination"]
                },
                "component_terms": {
                    "terms": ["swing", "rear", "front", "hydraulic", "seal"]
                }
            },
            "filter_logic": {
                "primary_pattern": "(equipment OR component) AND symptom",
                "conjunction_operator": "AND",
                "disjunction_operator": "OR"
            }
        }

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Pure access to main dashboard configuration"""
        try:
            return get_dashboard_config()
        except Exception as e:
            handle_error_utility(logger, e, "dashboard configuration access")
            return {}

    def get_dashboard_chart_config(self) -> Dict[str, Any]:
        """Pure access to dashboard chart configuration"""
        try:
            return get_dashboard_chart_config()
        except Exception as e:
            handle_error_utility(logger, e, "dashboard chart configuration access")
            return {}

    def get_styling_config(self) -> Dict[str, Any]:
        """Pure access to dashboard styling configuration"""
        try:
            return get_dashboard_styling_config()
        except Exception as e:
            handle_error_utility(logger, e, "styling configuration access")
            return {}

    def get_server_config(self) -> Dict[str, Any]:
        """Pure access to server configuration"""
        try:
            dashboard_config = self.get_dashboard_config()
            return dashboard_config.get("server", {})
        except Exception as e:
            handle_error_utility(logger, e, "server configuration access")
            return {}

    def get_performance_config(self) -> Dict[str, Any]:
        """Pure access to performance configuration"""
        try:
            dashboard_config = self.get_dashboard_config()
            return dashboard_config.get("performance", {})
        except Exception as e:
            handle_error_utility(logger, e, "performance configuration access")
            return {}

    def get_dashboard_metric_card_styling(self) -> Dict[str, Any]:
        """Access styling for metric cards from dashboard config"""
        try:
            dashboard_config = self.get_dashboard_config()
            styling = dashboard_config.get("styling", {})
            return styling.get("metric_cards", {})
        except Exception as e:
            handle_error_utility(logger, e, "metric card styling access")
            return {}

    def get_metric_card_styling(self) -> Dict[str, Any]:
        """Pure access to metric card styling"""
        try:
            styling = self.get_styling_config()
            return styling.get("metric_cards", {})
        except Exception as e:
            handle_error_utility(logger, e, "metric card styling access")
            return {}

    def get_dashboard_chart_styling_template(self) -> Dict[str, Any]:
        """Access chart styling template from dashboard config"""
        try:
            dashboard_config = self.get_dashboard_config()
            styling = dashboard_config.get("styling", {})
            return styling.get("chart_template", {})
        except Exception as e:
            handle_error_utility(logger, e, "chart styling template access")
            return {}

    def get_field_analysis_config(self) -> Dict[str, Any]:
        """Pure access to field analysis configuration"""
        try:
            return get_field_analysis_config()
        except Exception as e:
            handle_error_utility(logger, e, "field analysis configuration access")
            return {}

    def get_field_category_display_mapping(self) -> Dict[str, Any]:
        """Pure access to field category display mapping configuration"""
        try:
            return get_field_category_display_mapping()
        except Exception as e:
            handle_error_utility(logger, e, "field category display mapping access")
            return {}

    def get_completion_thresholds(self) -> Dict[str, int]:
        """Pure access to completion thresholds from system constants"""
        try:
            constants = get_system_constants()
            return constants.get("completion_thresholds", {})
        except Exception as e:
            handle_error_utility(logger, e, "completion thresholds access")
            return {}

    def get_completion_colors(self) -> Dict[str, str]:
        """Pure access to completion colors from dashboard styling"""
        try:
            styling = self.get_styling_config()
            return styling.get("completion_colors", {})
        except Exception as e:
            handle_error_utility(logger, e, "completion colors access")
            return {}

    def get_chart_display_config(self) -> Dict[str, Any]:
        """Pure access to chart display configuration"""
        try:
            return get_dashboard_chart_config()
        except Exception as e:
            handle_error_utility(logger, e, "chart display config access")
            return {}

    def get_system_constants(self) -> Dict[str, Any]:
        """Pure access to system constants configuration"""
        try:
            return get_system_constants()
        except Exception as e:
            handle_error_utility(logger, e, "system constants access")
            return {}

    def get_database_config(self) -> Dict[str, str]:
        """Pure access to database configuration"""
        try:
            return get_db_config()
        except Exception as e:
            handle_error_utility(logger, e, "database config access")
            return {}

    def get_processing_config(self) -> Dict[str, Any]:
        """Pure access to processing configuration"""
        try:
            all_config = get_all_config()
            return all_config.get("processing", {})
        except Exception as e:
            handle_error_utility(logger, e, "processing config access")
            return {}

    def get_relationships_config(self) -> Dict[str, Any]:
        """Pure access to relationships configuration (from entity connections)"""
        try:
            return get_entity_connections()
        except Exception as e:
            handle_error_utility(logger, e, "relationships config access")
            return {}

    def get_complete_config(self) -> Dict[str, Any]:
        """Pure access to all configurations merged into a single dictionary"""
        try:
            return get_all_config()
        except Exception as e:
            handle_error_utility(logger, e, "complete config access")
            return {}

    def validate_config_availability(self) -> Dict[str, bool]:
        """Check if all essential configurations are available"""
        validation_results = {
            "schema_available": self.get_schema_config() != {},
            "field_mappings_available": self.get_field_mappings_config() != {},
            "dashboard_config_available": self.get_dashboard_config() != {},
            "workflow_stages_available": self.get_workflow_stages_config() != {},
            "entity_classification_available": self.get_entity_classification_config() != {},
            "entity_connections_available": self.get_entity_connections_config() != {},
            "field_analysis_available": self.get_field_analysis_config() != {},
            "dashboard_styling_available": self.get_styling_config() != {},
            "dashboard_charts_available": self.get_dashboard_chart_config() != {},
            "system_constants_available": self.get_system_constants() != {},
            "case_study_available": self.get_case_study_config() != {},
            "graph_search_available": self.get_graph_search_config() != {},
        }
        return validation_results

    # Direct access to environment config functions for purity

    def get_mappings(self) -> Dict[str, Any]:
        """Direct access to field mappings"""
        return get_mappings()

    def get_schema(self) -> Dict[str, Any]:
        """Direct access to model schema"""
        return get_schema()

    def get_entity_classification(self) -> Dict[str, Any]:
        """Direct access to entity classification"""
        return get_entity_classification()

    def get_case_study_config(self) -> Dict[str, Any]:
        """Direct access to case study schema"""
        return get_case_study_config()


# Singleton pattern
_config_adapter: Optional[ConfigAdapter] = None


def get_config_adapter() -> ConfigAdapter:
    """Get singleton config adapter instance"""
    global _config_adapter
    if _config_adapter is None:
        _config_adapter = ConfigAdapter()
    return _config_adapter


def reset_config_adapter():
    """Reset config adapter for testing or re-initialization"""
    global _config_adapter
    _config_adapter = None
