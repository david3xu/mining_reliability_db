#!/usr/bin/env python3
"""
Configuration Data Adapter - Pure Configuration Access
Clean abstraction layer for all configuration data with zero business logic.
"""

import logging
from typing import Any, Dict, List, Optional

# Pure configuration imports
from configs.environment import (
    get_all_config,
    get_dashboard_chart_config,
    get_dashboard_config,
    get_dashboard_styling_config,
    get_entity_classification,
    get_entity_connections,
    get_entity_names,
    get_entity_primary_key,
    get_field_analysis_config,
    get_mappings,
    get_schema,
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

logger = logging.getLogger(__name__)


class ConfigAdapter:
    """Pure configuration access - no processing logic"""

    def __init__(self):
        """Initialize configuration adapter"""
        pass

    # Schema Configuration Access

    def get_schema_config(self) -> Dict[str, Any]:
        """Pure access to model schema configuration"""
        try:
            return get_schema()
        except Exception as e:
            handle_error(logger, e, "schema configuration access")
            return {}

    def get_entity_definitions(self) -> Dict[str, Any]:
        """Pure access to entity definitions from schema"""
        try:
            schema = get_schema()
            entities = schema.get("entities", [])
            return {e["name"]: e for e in entities}
        except Exception as e:
            handle_error(logger, e, "entity definitions access")
            return {}

    def get_entity_list(self) -> List[str]:
        """Pure access to entity names list"""
        try:
            return get_entity_names()
        except Exception as e:
            handle_error(logger, e, "entity names access")
            return []

    def get_entity_primary_key_config(self, entity_name: str) -> Optional[str]:
        """Pure access to entity primary key"""
        try:
            return get_entity_primary_key(entity_name)
        except Exception as e:
            handle_error(logger, e, f"primary key access for {entity_name}")
            return None

    # Field Mapping Configuration Access

    def get_field_mappings_config(self) -> Dict[str, Any]:
        """Pure access to field mappings configuration"""
        try:
            return get_mappings()
        except Exception as e:
            handle_error(logger, e, "field mappings configuration access")
            return {}

    def get_entity_mappings(self) -> Dict[str, Any]:
        """Pure access to entity field mappings"""
        try:
            mappings = get_mappings()
            return mappings.get("entity_mappings", {})
        except Exception as e:
            handle_error(logger, e, "entity mappings access")
            return {}

    def get_field_categories(self) -> Dict[str, List[str]]:
        """Pure access to field categories"""
        try:
            mappings = get_mappings()
            return mappings.get("field_categories", {})
        except Exception as e:
            handle_error(logger, e, "field categories access")
            return {}

    def get_cascade_labeling_config(self) -> Dict[str, Any]:
        """Pure access to cascade labeling configuration"""
        try:
            mappings = get_mappings()
            return mappings.get("cascade_labeling", {})
        except Exception as e:
            handle_error(logger, e, "cascade labeling configuration access")
            return {}

    # Workflow Configuration Access

    def get_workflow_stages_config(self) -> Dict[str, Any]:
        """Pure access to workflow stages configuration"""
        try:
            return get_workflow_stages_config()
        except Exception as e:
            handle_error(logger, e, "workflow stages configuration access")
            return {}

    def get_workflow_display_config(self) -> Dict[str, Any]:
        """Pure access to workflow display configuration"""
        try:
            workflow_config = get_workflow_stages_config()
            return workflow_config.get("display_config", {})
        except Exception as e:
            handle_error(logger, e, "workflow display configuration access")
            return {}

    def get_entity_classification_config(self) -> Dict[str, Any]:
        """Pure access to entity classification configuration"""
        try:
            return get_entity_classification()
        except Exception as e:
            handle_error(logger, e, "entity classification configuration access")
            return {}

    def get_entity_connections_config(self) -> Dict[str, Any]:
        """Pure access to entity connections configuration"""
        try:
            return get_entity_connections()
        except Exception as e:
            handle_error(logger, e, "entity connections configuration access")
            return {}

    # Dashboard Configuration Access

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Pure access to dashboard configuration"""
        try:
            return get_dashboard_config()
        except Exception as e:
            handle_error(logger, e, "dashboard configuration access")
            return {}

    def get_styling_config(self) -> Dict[str, Any]:
        """Pure access to dashboard styling configuration"""
        try:
            return get_dashboard_styling_config()
        except Exception as e:
            handle_error(logger, e, "styling configuration access")
            return {
                "primary_color": "#4A90E2",
                "chart_colors": ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"],
                "background_light": "#FFFFFF",
                "text_primary": "#333333",
            }

    def get_dashboard_chart_config(self) -> Dict[str, Any]:
        """Pure access to dashboard chart configuration"""
        try:
            return get_dashboard_chart_config()
        except Exception as e:
            handle_error(logger, e, "chart configuration access")
            return {
                "font_family": "Arial, sans-serif",
                "default_height": 400,
                "title_font_size": 18,
            }

    def get_server_config(self) -> Dict[str, Any]:
        """Pure access to server configuration"""
        try:
            dashboard_config = get_dashboard_config()
            return dashboard_config.get("server", {})
        except Exception as e:
            handle_error(logger, e, "server configuration access")
            return {"default_host": "127.0.0.1", "default_port": 8050}

    def get_performance_config(self) -> Dict[str, Any]:
        """Pure access to performance configuration"""
        try:
            dashboard_config = get_dashboard_config()
            return dashboard_config.get("performance", {})
        except Exception as e:
            handle_error(logger, e, "performance configuration access")
            return {"query_timeout_warning": 5.0, "cache_ttl_seconds": 300}

    # Field Analysis Configuration Access

    def get_field_analysis_config(self) -> Dict[str, Any]:
        """Pure access to field analysis configuration"""
        try:
            return get_field_analysis_config()
        except Exception as e:
            handle_error(logger, e, "field analysis configuration access")
            return {}

    def get_completion_thresholds(self) -> Dict[str, int]:
        """Pure access to completion thresholds"""
        try:
            field_config = get_field_analysis_config()
            return field_config.get("completion_thresholds", {})
        except Exception as e:
            handle_error(logger, e, "completion thresholds access")
            return {"very_low": 20, "low": 40, "medium": 60, "good": 80, "high": 100}

    def get_completion_colors(self) -> Dict[str, str]:
        """Pure access to completion colors"""
        try:
            field_config = get_field_analysis_config()
            return field_config.get("completion_colors", {})
        except Exception as e:
            handle_error(logger, e, "completion colors access")
            return {
                "very_low": "#D32F2F",
                "low": "#F57C00",
                "medium": "#FFA000",
                "good": "#7CB342",
                "high": "#388E3C",
            }

    def get_chart_display_config(self) -> Dict[str, Any]:
        """Pure access to chart display configuration"""
        try:
            field_config = get_field_analysis_config()
            return field_config.get("chart_config", {})
        except Exception as e:
            handle_error(logger, e, "chart display configuration access")
            return {"row_height": 25, "min_height": 400, "max_completion": 100}

    # System Configuration Access

    def get_system_constants(self) -> Dict[str, Any]:
        """Pure access to system constants"""
        try:
            return get_system_constants()
        except Exception as e:
            handle_error(logger, e, "system constants access")
            return {}

    def get_database_config(self) -> Dict[str, Any]:
        """Pure access to database configuration"""
        try:
            constants = get_system_constants()
            return constants.get("database", {})
        except Exception as e:
            handle_error(logger, e, "database configuration access")
            return {}

    def get_processing_config(self) -> Dict[str, Any]:
        """Pure access to processing configuration"""
        try:
            constants = get_system_constants()
            return constants.get("processing", {})
        except Exception as e:
            handle_error(logger, e, "processing configuration access")
            return {}

    def get_relationships_config(self) -> Dict[str, Any]:
        """Pure access to relationships configuration"""
        try:
            constants = get_system_constants()
            return constants.get("relationships", {})
        except Exception as e:
            handle_error(logger, e, "relationships configuration access")
            return {}

    # Comprehensive Configuration Access

    def get_complete_config(self) -> Dict[str, Any]:
        """Pure access to all configuration data"""
        try:
            return get_all_config()
        except Exception as e:
            handle_error(logger, e, "complete configuration access")
            return {}

    def validate_config_availability(self) -> Dict[str, bool]:
        """Pure validation of configuration file availability"""
        try:
            validation_status = {}

            # Test each configuration source
            validation_status["schema"] = bool(self.get_schema_config())
            validation_status["mappings"] = bool(self.get_field_mappings_config())
            validation_status["workflow_stages"] = bool(self.get_workflow_stages_config())
            validation_status["dashboard"] = bool(self.get_dashboard_config())
            validation_status["entity_classification"] = bool(
                self.get_entity_classification_config()
            )
            validation_status["entity_connections"] = bool(self.get_entity_connections_config())
            validation_status["field_analysis"] = bool(self.get_field_analysis_config())
            validation_status["system_constants"] = bool(self.get_system_constants())

            return validation_status

        except Exception as e:
            handle_error(logger, e, "configuration validation")
            return {}

    # Specialized Access Methods

    def get_dashboard_metric_card_styling(self) -> Dict[str, Any]:
        """Pure access to metric card styling configuration"""
        try:
            styling = self.get_styling_config()
            chart = self.get_dashboard_chart_config()

            return {
                "primary_color": styling.get("primary_color", "#4A90E2"),
                "text_light": styling.get("text_light", "#FFFFFF"),
                "card_height": chart.get("metric_card_height", 120),
                "card_width": chart.get("metric_card_width", 220),
            }
        except Exception as e:
            handle_error(logger, e, "metric card styling access")
            return {}

    def get_dashboard_chart_styling_template(self) -> Dict[str, Any]:
        """Pure access to chart styling template"""
        try:
            styling = self.get_styling_config()
            chart = self.get_dashboard_chart_config()

            return {
                "colors": styling.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
                "font_family": chart.get("font_family", "Arial, sans-serif"),
                "title_font_size": chart.get("title_font_size", 18),
                "height": chart.get("default_height", 400),
                "background": styling.get("background_light", "#FFFFFF"),
            }
        except Exception as e:
            handle_error(logger, e, "chart styling template access")
            return {}


# Singleton pattern
_config_adapter = None


def get_config_adapter() -> ConfigAdapter:
    """Get singleton configuration adapter instance"""
    global _config_adapter
    if _config_adapter is None:
        _config_adapter = ConfigAdapter()
    return _config_adapter


def reset_config_adapter():
    """Reset configuration adapter instance"""
    global _config_adapter
    if _config_adapter:
        logger.info("Resetting configuration adapter")
        _config_adapter = None
