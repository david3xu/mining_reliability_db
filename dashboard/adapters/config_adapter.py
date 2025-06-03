#!/usr/bin/env python3
"""
Configuration Adapter - Pure Configuration Access Layer
Central configuration adapter with caching and validation.
"""

import logging
from typing import Any, Dict, List, Optional

# Pure configuration imports
from configs.environment import (
    get_all_config,
    get_batch_size,
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
    get_mappings,
    get_max_retries,
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
]

logger = logging.getLogger(__name__)


def handle_error_utility(logger: logging.Logger, error: Exception, context: str) -> None:
    """Unified error handling utility for adapters"""
    handle_error(logger, error, context)


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

    # Dashboard Configuration Access

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Pure access to dashboard configuration"""
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
            return {
                "font_family": "Arial, sans-serif",
                "title_font_size": 18,
                "default_height": 400,
            }

    def get_styling_config(self) -> Dict[str, Any]:
        """Pure access to dashboard styling configuration"""
        try:
            return get_dashboard_styling_config()
        except Exception as e:
            handle_error_utility(logger, e, "styling configuration access")
            return {
                "primary_color": "#4A90E2",
                "chart_colors": ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"],
                "background_light": "#FFFFFF",
                "text_primary": "#333333",
            }

    def get_server_config(self) -> Dict[str, Any]:
        """Pure access to server configuration"""
        try:
            dashboard_config = self.get_dashboard_config()
            return dashboard_config.get("server", {})
        except Exception as e:
            handle_error_utility(logger, e, "server configuration access")
            return {"default_host": "127.0.0.1", "default_port": 8050}

    def get_performance_config(self) -> Dict[str, Any]:
        """Pure access to performance configuration"""
        try:
            dashboard_config = self.get_dashboard_config()
            return dashboard_config.get("performance", {})
        except Exception as e:
            handle_error_utility(logger, e, "performance configuration access")
            return {"query_timeout_warning": 5.0, "cache_ttl_seconds": 300}

    def get_dashboard_metric_card_styling(self) -> Dict[str, Any]:
        """Get metric card styling configuration for adapters"""
        try:
            styling = self.get_styling_config()
            micro_styles = styling.get("micro_component_styles", {})
            metric_card = micro_styles.get("metric_card", {})

            return {
                "primary_color": styling.get("primary_color", "#4A90E2"),
                "text_light": styling.get("text_light", "#FFFFFF"),
                "card_height": metric_card.get("default_dimensions", {})
                .get("height", "120px")
                .replace("px", ""),
                "card_width": metric_card.get("default_dimensions", {})
                .get("width", "220px")
                .replace("px", ""),
            }
        except Exception as e:
            handle_error_utility(logger, e, "metric card styling configuration access")
            return {}

    def get_dashboard_chart_styling_template(self) -> Dict[str, Any]:
        """Get dashboard chart styling template for adapters"""
        try:
            styling = self.get_styling_config()
            charts = self.get_dashboard_chart_config()

            return {
                "colors": styling.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
                "font_family": charts.get("font_family", "Arial, sans-serif"),
                "title_font_size": charts.get("title_font_size", 18),
                "height": charts.get("default_height", 400),
                "background": styling.get("background_light", "#FFFFFF"),
            }
        except Exception as e:
            handle_error_utility(logger, e, "chart styling template access")
            return {}

    # Field Analysis Configuration Access

    def get_field_analysis_config(self) -> Dict[str, Any]:
        """Pure access to field analysis configuration"""
        try:
            return get_field_analysis_config()
        except Exception as e:
            handle_error_utility(logger, e, "field analysis configuration access")
            return {}

    def get_field_category_display_mapping(self) -> Dict[str, Any]:
        """Pure access to field category display mapping"""
        try:
            return get_field_category_display_mapping()
        except Exception as e:
            handle_error_utility(logger, e, "field category display mapping access")
            return {}

    def get_completion_thresholds(self) -> Dict[str, int]:
        """Pure access to completion thresholds"""
        try:
            field_config = self.get_field_analysis_config()
            return field_config.get("completion_thresholds", {})
        except Exception as e:
            handle_error_utility(logger, e, "completion thresholds access")
            return {"very_low": 20, "low": 40, "medium": 60, "good": 80, "high": 100}

    def get_completion_colors(self) -> Dict[str, str]:
        """Pure access to completion colors"""
        try:
            field_config = self.get_field_analysis_config()
            return field_config.get("completion_colors", {})
        except Exception as e:
            handle_error_utility(logger, e, "completion colors access")
            return {
                "very_low": "#D32F2F",
                "low": "#F57C00",
                "medium": "#FFA000",
                "good": "#7CB342",
                "high": "#388E3C",
            }

    def get_chart_display_config(self) -> Dict[str, Any]:
        """Get chart display configuration from field analysis"""
        try:
            field_config = self.get_field_analysis_config()
            return field_config.get(
                "chart_config", {"row_height": 25, "min_height": 400, "max_completion": 100}
            )
        except Exception as e:
            handle_error_utility(logger, e, "chart display configuration access")
            return {}

    # System Configuration Access

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
            handle_error_utility(logger, e, "database configuration access")
            return {}

    def get_processing_config(self) -> Dict[str, Any]:
        """Pure access to processing configuration"""
        try:
            return {
                "batch_size": get_batch_size(),
                "connection_timeout": get_connection_timeout(),
                "max_retries": get_max_retries(),
            }
        except Exception as e:
            handle_error_utility(logger, e, "processing configuration access")
            return {}

    def get_relationships_config(self) -> Dict[str, Any]:
        """Pure access to relationships configuration based on schema"""
        try:
            return {
                "relationships": get_schema().get("relationships", []),
                "entity_connections": self.get_entity_connections_config(),
            }
        except Exception as e:
            handle_error_utility(logger, e, "relationships configuration access")
            return {}

    def get_complete_config(self) -> Dict[str, Any]:
        """Comprehensive configuration summary for debugging"""
        try:
            return get_all_config()
        except Exception as e:
            handle_error_utility(logger, e, "complete configuration access")
            return {}

    def validate_config_availability(self) -> Dict[str, bool]:
        """Validate availability of core configuration files"""
        availability = {
            "schema_available": bool(self.get_schema_config()),
            "mappings_available": bool(self.get_field_mappings_config()),
            "dashboard_available": bool(self.get_dashboard_config()),
            "workflow_stages_available": bool(self.get_workflow_stages_config()),
            "styling_available": bool(self.get_styling_config()),
            "charts_available": bool(self.get_dashboard_chart_config()),
            "system_constants_available": bool(self.get_system_constants()),
            "field_analysis_available": bool(self.get_field_analysis_config()),
            "entity_classification_available": bool(self.get_entity_classification_config()),
            "entity_connections_available": bool(self.get_entity_connections_config()),
        }
        if not all(availability.values()):
            handle_error_utility(
                logger, ValueError("Some configs not available"), "config availability validation"
            )
        return availability

    # Convenience methods for workflow_adapter compatibility
    def get_mappings(self) -> Dict[str, Any]:
        """Get full mappings configuration (convenience method)"""
        return self.get_field_mappings_config()

    def get_schema(self) -> Dict[str, Any]:
        """Get schema configuration (convenience method)"""
        return self.get_schema_config()

    def get_entity_classification(self) -> Dict[str, Any]:
        """Get entity classification configuration (convenience method for workflow analysis)"""
        return self.get_entity_classification_config()


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
