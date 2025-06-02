#!/usr/bin/env python3
"""
Workflow Adapter - Process Workflow Data Access Layer
Unified workflow data extraction with standardized interface.
"""

import logging
from typing import Any, Dict, List, Optional

from dashboard.adapters.interfaces import ComponentMetadata

# Pure core layer imports
from mine_core.business.workflow_processor import get_workflow_processor
from mine_core.shared.common import handle_error

__all__ = [
    "WorkflowAdapter",
    "get_workflow_adapter",
    "reset_workflow_adapter",
]

logger = logging.getLogger(__name__)


class WorkflowAdapter:
    """Pure workflow data access - calls core workflow processor only"""

    def __init__(self):
        """Initialize with core workflow processor connection"""
        self.workflow_processor = get_workflow_processor()

    def get_workflow_schema_analysis(self) -> Dict[str, Any]:
        """Pure data access for workflow schema structure"""
        try:
            logger.info("Workflow Adapter: Fetching schema analysis from core")

            # Call core business logic
            schema_analysis = self.workflow_processor.analyze_workflow_schema()

            if not schema_analysis:
                return {}

            # Pure data pass-through with metadata
            return {
                **schema_analysis,
                "metadata": ComponentMetadata(
                    source="core.workflow_processor",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if schema_analysis.get("total_entities", 0) > 0 else 0.0,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, "workflow schema analysis data access")
            return {}

    def get_entity_field_distribution(self) -> Dict[str, Any]:
        """Pure data access for entity field distribution"""
        try:
            logger.info("Workflow Adapter: Fetching entity field distribution from core")

            # Call core business logic
            distribution_data = self.workflow_processor.analyze_entity_field_distribution()

            if not distribution_data:
                return {}

            # Pure data pass-through
            return {
                **distribution_data,
                "metadata": ComponentMetadata(
                    source="core.workflow_processor",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if distribution_data.get("total_entities", 0) > 0 else 0.0,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, "entity field distribution data access")
            return {}

    def get_field_mapping_analysis(self) -> Dict[str, Any]:
        """Pure data access for field mapping patterns"""
        try:
            logger.info("Workflow Adapter: Fetching field mapping analysis from core")

            # Call core business logic
            mapping_data = self.workflow_processor.analyze_field_mappings()

            if not mapping_data:
                return {}

            # Pure data pass-through
            return {
                **mapping_data,
                "metadata": ComponentMetadata(
                    source="core.workflow_processor",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if mapping_data.get("total_mappings", 0) > 0 else 0.0,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, "field mapping analysis data access")
            return {}

    def get_workflow_business_analysis_neo4j(self) -> Dict[str, Any]:
        """Pure data access for Neo4j-driven workflow business analysis"""
        try:
            logger.info("Workflow Adapter: Fetching Neo4j workflow analysis from core")

            # Call core business logic
            workflow_analysis = self.workflow_processor.process_workflow_business_analysis()

            if not workflow_analysis.workflow_stages:
                return {}

            # Pure data transformation to dictionary format
            return {
                "workflow_stages": self._transform_workflow_stages(
                    workflow_analysis.workflow_stages
                ),
                "supporting_entities": workflow_analysis.supporting_entities,
                "completion_summary": workflow_analysis.completion_summary,
                "display_config": {},  # Would be populated from config adapter
                "metadata": ComponentMetadata(
                    source="core.workflow_processor.neo4j",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if workflow_analysis.workflow_stages else 0.0,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, "Neo4j workflow business analysis data access")
            return {}

    def get_field_mapping_counts(self) -> Dict[str, Any]:
        """Pure data access for field mapping statistics"""
        try:
            logger.info("Workflow Adapter: Fetching field mapping counts from core")

            # Call core business logic
            mapping_counts = self.workflow_processor.calculate_field_mapping_counts()

            # Pure data pass-through
            return mapping_counts

        except Exception as e:
            handle_error(logger, e, "field mapping counts data access")
            return {"total_fields": 0, "entity_mappings": {}, "source_fields": []}

    def get_complete_workflow_analysis(self) -> Dict[str, Any]:
        """Pure data access for complete workflow visualization data"""
        try:
            logger.info("Workflow Adapter: Fetching complete workflow visualization from core")

            # Call core business logic
            complete_data = self.workflow_processor.process_complete_workflow_visualization()

            if not complete_data:
                return {}

            # Pure data pass-through
            return {
                **complete_data,
                "metadata": ComponentMetadata(
                    source="core.workflow_processor.complete",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if complete_data.get("workflow_stages") else 0.0,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, "complete workflow analysis data access")
            return {}

    def validate_workflow_data(self) -> Dict[str, bool]:
        """Pure validation check for workflow data availability"""
        try:
            validation_status = {}

            # Test each workflow service
            schema_data = self.workflow_processor.analyze_workflow_schema()
            validation_status["workflow_schema"] = bool(schema_data.get("total_entities", 0) > 0)

            entity_data = self.workflow_processor.analyze_entity_field_distribution()
            validation_status["entity_distribution"] = bool(
                entity_data.get("total_entities", 0) > 0
            )

            mapping_data = self.workflow_processor.analyze_field_mappings()
            validation_status["field_mapping"] = bool(mapping_data.get("total_mappings", 0) > 0)

            workflow_analysis = self.workflow_processor.process_workflow_business_analysis()
            validation_status["workflow_business"] = bool(workflow_analysis.workflow_stages)

            return validation_status

        except Exception as e:
            handle_error(logger, e, "workflow data validation")
            return {"error": True, "message": str(e)}

    def _transform_workflow_stages(self, workflow_stages: List) -> List[Dict[str, Any]]:
        """Helper to transform workflow stages for dashboard display"""
        transformed_stages = []
        for stage in workflow_stages:
            transformed_stages.append(
                {
                    "name": stage.name,
                    "description": stage.description,
                    "status": stage.status,
                    "completion_rate": stage.completion_rate,
                    "metrics": stage.metrics,
                }
            )
        return transformed_stages

    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime

        return datetime.now().isoformat()


_workflow_adapter: Optional[WorkflowAdapter] = None


def get_workflow_adapter() -> WorkflowAdapter:
    """Singleton access to WorkflowAdapter instance"""
    global _workflow_adapter
    if _workflow_adapter is None:
        _workflow_adapter = WorkflowAdapter()
    return _workflow_adapter


def reset_workflow_adapter():
    """Reset the singleton adapter instance (for testing purposes)"""
    global _workflow_adapter
    if _workflow_adapter:
        logger.info("Resetting workflow adapter")
        _workflow_adapter = None
