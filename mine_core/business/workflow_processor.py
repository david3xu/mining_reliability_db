#!/usr/bin/env python3
"""
Core Workflow Processing Engine - Business Logic Authority
Centralized workflow intelligence with schema-driven stage analysis.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from configs.environment import (
    get_entity_classification,
    get_entity_connections,
    get_entity_names,
    get_mappings,
    get_schema,
    get_workflow_stages_config,
)
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


@dataclass
class WorkflowStage:
    """Workflow stage data container"""

    stage_number: int
    entity_name: str
    title: str
    field_count: int
    completion_rate: float
    business_fields: List[str]
    complexity_level: str


@dataclass
class WorkflowAnalysis:
    """Complete workflow analysis result"""

    workflow_stages: List[WorkflowStage]
    supporting_entities: List[Dict[str, Any]]
    completion_summary: Dict[str, Any]
    metadata: Dict[str, Any]


class WorkflowProcessor:
    """Core workflow intelligence and stage analysis engine"""

    def __init__(self):
        self.query_manager = get_query_manager()
        self.schema = get_schema()
        self.mappings = get_mappings()

    def analyze_workflow_schema(self) -> Dict[str, Any]:
        """Analyze workflow schema structure and relationships"""
        try:
            entity_names = get_entity_names()
            entity_mappings = self.mappings.get("entity_mappings", {})

            # Calculate unique field coverage
            unique_fields = set()
            for field_mapping in entity_mappings.values():
                unique_fields.update(field_mapping.values())

            # Analyze workflow entities
            workflow_entities = self._build_workflow_entities()

            # Extract analytical dimensions
            analytical_dimensions = self.schema.get("analytical_dimensions", {})
            field_categories = self.mappings.get("field_categories", {})

            return {
                "workflow_entities": workflow_entities,
                "total_entities": len(entity_names),
                "total_fields": len(unique_fields),
                "analytical_dimensions": len(analytical_dimensions),
                "field_categories": len(field_categories),
                "entity_complexity": self._analyze_entity_complexity(workflow_entities),
            }

        except Exception as e:
            handle_error(logger, e, "workflow schema analysis")
            return {}

    def analyze_entity_field_distribution(self) -> Dict[str, Any]:
        """Analyze field distribution across workflow entities"""
        try:
            entities = self.schema.get("entities", [])

            if not entities:
                return {}

            entity_names = []
            field_counts = []

            for entity in entities:
                entity_name = entity["name"]
                properties = entity.get("properties", {})
                field_count = len(properties)

                entity_names.append(entity_name)
                field_counts.append(field_count)

            return {
                "entity_names": entity_names,
                "field_counts": field_counts,
                "total_entities": len(entities),
                "field_distribution": self._analyze_field_distribution_patterns(field_counts),
            }

        except Exception as e:
            handle_error(logger, e, "entity field distribution analysis")
            return {}

    def analyze_field_mappings(self) -> Dict[str, Any]:
        """Analyze field mapping patterns and categorization"""
        try:
            entity_mappings = self.mappings.get("entity_mappings", {})
            field_categories = self.mappings.get("field_categories", {})

            if not entity_mappings:
                return {}

            # Build category lookup
            category_lookup = self._build_category_lookup(field_categories)

            # Analyze all mappings
            mapping_analysis = []
            for entity_name, field_mapping in entity_mappings.items():
                for target_field, source_field in field_mapping.items():
                    mapping_info = self._analyze_single_mapping(
                        entity_name, target_field, source_field, category_lookup
                    )
                    mapping_analysis.append(mapping_info)

            return {
                "mappings": mapping_analysis,
                "total_mappings": len(mapping_analysis),
                "entities_covered": len(entity_mappings),
                "categories_found": len(set(m["category"] for m in mapping_analysis)),
                "critical_fields": sum(1 for m in mapping_analysis if m["critical"]),
                "mapping_patterns": self._analyze_mapping_patterns(mapping_analysis),
            }

        except Exception as e:
            handle_error(logger, e, "field mapping analysis")
            return {}

    def process_workflow_business_analysis(self) -> WorkflowAnalysis:
        """Process complete workflow business analysis with Neo4j completion rates"""
        try:
            # Get workflow configuration
            workflow_config = get_workflow_stages_config()
            entity_completion_data = self._get_entity_completion_rates()

            # Process workflow stages
            workflow_stages = self._process_workflow_stages(workflow_config, entity_completion_data)

            # Process supporting entities
            supporting_entities = self._process_supporting_entities()

            # Generate completion summary
            completion_summary = self._generate_completion_summary(entity_completion_data)

            return WorkflowAnalysis(
                workflow_stages=workflow_stages,
                supporting_entities=supporting_entities,
                completion_summary=completion_summary,
                metadata={
                    "stage_count": len(workflow_stages),
                    "supporting_count": len(supporting_entities),
                    "analysis_type": "neo4j_driven",
                },
            )

        except Exception as e:
            handle_error(logger, e, "workflow business analysis")
            return WorkflowAnalysis([], [], {}, {"error": str(e)})

    def calculate_field_mapping_counts(self) -> Dict[str, Any]:
        """Calculate field mapping statistics for workflow metrics"""
        try:
            entity_mappings = self.mappings.get("entity_mappings", {})

            # Extract all source fields
            source_fields = []
            for entity_name, mapping in entity_mappings.items():
                source_fields.extend(mapping.values())

            # Calculate unique count
            unique_source_fields = list(set(source_fields))

            return {
                "total_fields": len(unique_source_fields),
                "entity_mappings": entity_mappings,
                "source_fields": unique_source_fields,
                "mapping_coverage": self._calculate_mapping_coverage(entity_mappings),
            }

        except Exception as e:
            handle_error(logger, e, "field mapping counts calculation")
            return {"total_fields": 0, "entity_mappings": {}, "source_fields": []}

    def process_complete_workflow_visualization(self) -> Dict[str, Any]:
        """Process data for complete workflow visualization with supporting entities"""
        try:
            # Get main workflow stages
            workflow_analysis = self.process_workflow_business_analysis()

            # Get entity classification for supporting entities
            entity_classification = get_entity_classification()
            entity_connections = get_entity_connections()

            # Process supporting entities with connections
            supporting_entities = self._process_supporting_with_connections(
                entity_classification, entity_connections
            )

            # Get layout configuration
            layout_config = entity_classification.get("layout_config", {})

            return {
                "workflow_stages": [
                    self._stage_to_dict(stage) for stage in workflow_analysis.workflow_stages
                ],
                "supporting_entities": supporting_entities,
                "layout_config": layout_config,
                "connection_config": entity_connections.get("connection_display", {}),
                "display_config": get_workflow_stages_config().get("display_config", {}),
            }

        except Exception as e:
            handle_error(logger, e, "complete workflow visualization processing")
            return {}

    # Private processing methods

    def _build_workflow_entities(self) -> List[Dict[str, Any]]:
        """Build enhanced workflow entity definitions"""
        # Core workflow entities in business order
        workflow_order = ["ActionRequest", "Problem", "RootCause", "ActionPlan", "Verification"]

        entities = self.schema.get("entities", [])
        entity_dict = {e["name"]: e for e in entities}

        workflow_entities = []
        for i, entity_name in enumerate(workflow_order, 1):
            if entity_name in entity_dict:
                entity_def = entity_dict[entity_name]
                enhanced_entity = self._enhance_entity_definition(entity_def, i)
                workflow_entities.append(enhanced_entity)

        return workflow_entities

    def _enhance_entity_definition(
        self, entity_def: Dict[str, Any], stage_number: int
    ) -> Dict[str, Any]:
        """Enhance entity definition with workflow context"""
        entity_name = entity_def["name"]
        properties = entity_def.get("properties", {})
        field_count = len(properties)

        # Calculate business field count (exclude technical fields)
        business_field_count = sum(
            1
            for prop_name, prop_info in properties.items()
            if not self._is_technical_field(prop_name, prop_info)
        )

        # Determine complexity
        complexity_level = (
            "complex" if field_count >= 8 else "moderate" if field_count >= 5 else "simple"
        )

        return {
            "stage_number": stage_number,
            "entity_name": entity_name,
            "title": self._get_business_title(entity_name),
            "field_count": field_count,
            "business_field_count": business_field_count,
            "properties": properties,
            "complexity_level": complexity_level,
        }

    def _process_workflow_stages(
        self, workflow_config: Dict, completion_data: Dict
    ) -> List[WorkflowStage]:
        """Process workflow stages with completion rates"""
        stage_configs = workflow_config.get("workflow_stages", [])

        stages = []
        for stage_config in stage_configs:
            entity_name = stage_config.get("entity_name", "")

            # Get completion rate from Neo4j data
            completion_rate = 0.0
            if entity_name in completion_data:
                completion_rate = completion_data[entity_name].get("completion_rate", 0.0)

            # Calculate complexity
            field_count = len(stage_config.get("business_fields", []))
            complexity = (
                "complex" if field_count >= 6 else "moderate" if field_count >= 3 else "simple"
            )

            stage = WorkflowStage(
                stage_number=stage_config.get("stage_number", 1),
                entity_name=entity_name,
                title=stage_config.get("title", entity_name),
                field_count=field_count,
                completion_rate=completion_rate,
                business_fields=stage_config.get("business_fields", []),
                complexity_level=complexity,
            )

            stages.append(stage)

        return stages

    def _process_supporting_entities(self) -> List[Dict[str, Any]]:
        """Process supporting entities for workflow context"""
        entity_classification = get_entity_classification()
        supporting_entities = (
            entity_classification.get("entity_types", {})
            .get("supporting_entities", {})
            .get("entities", [])
        )

        processed_entities = []
        for entity_name in supporting_entities:
            entity_info = self._get_entity_info_for_support(entity_name)
            processed_entities.append(entity_info)

        return processed_entities

    def _process_supporting_with_connections(
        self, entity_classification: Dict, entity_connections: Dict
    ) -> List[Dict[str, Any]]:
        """Process supporting entities with connection information"""
        supporting_entities = (
            entity_classification.get("entity_types", {})
            .get("supporting_entities", {})
            .get("entities", [])
        )
        connections = entity_connections.get("supporting_connections", {})

        processed = []
        for entity_name in supporting_entities:
            entity_info = self._get_entity_info_for_support(entity_name)
            entity_info["connects_to"] = connections.get(entity_name, "Unknown")
            entity_info["color"] = "#6C757D"  # Default supporting entity color
            processed.append(entity_info)

        return processed

    def _get_entity_completion_rates(self) -> Dict[str, Any]:
        """Get entity completion rates (simplified for core layer)"""
        # This would normally come from query_manager, simplified for core logic
        entity_names = get_entity_names()
        completion_data = {}

        for entity_name in entity_names:
            count = self.query_manager.get_entity_count(entity_name)
            # Simplified completion rate calculation
            completion_rate = min(100.0, (count / 10) * 100) if count > 0 else 0.0

            completion_data[entity_name] = {
                "total_count": count,
                "completion_rate": completion_rate,
                "completed_fields": count * 2,  # Simplified calculation
                "total_fields": count * 3,  # Simplified calculation
            }

        return completion_data

    # Helper methods

    def _analyze_entity_complexity(self, workflow_entities: List[Dict]) -> Dict[str, Any]:
        """Analyze complexity distribution across entities"""
        complexity_counts = {}
        for entity in workflow_entities:
            complexity = entity.get("complexity_level", "simple")
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1

        return {
            "complexity_distribution": complexity_counts,
            "average_fields": sum(e.get("field_count", 0) for e in workflow_entities)
            / len(workflow_entities),
            "most_complex": max(workflow_entities, key=lambda e: e.get("field_count", 0))[
                "entity_name"
            ],
        }

    def _analyze_field_distribution_patterns(self, field_counts: List[int]) -> Dict[str, Any]:
        """Analyze field distribution patterns"""
        if not field_counts:
            return {}

        return {
            "min_fields": min(field_counts),
            "max_fields": max(field_counts),
            "average_fields": sum(field_counts) / len(field_counts),
            "field_variance": max(field_counts) - min(field_counts),
            "balanced_distribution": max(field_counts) / min(field_counts) < 3
            if min(field_counts) > 0
            else False,
        }

    def _build_category_lookup(self, field_categories: Dict) -> Dict[str, str]:
        """Build field category lookup table"""
        category_lookup = {}
        for category, fields in field_categories.items():
            clean_category = category.replace("_fields", "").title()
            for field in fields:
                category_lookup[field] = clean_category
        return category_lookup

    def _analyze_single_mapping(
        self, entity_name: str, target_field: str, source_field: str, category_lookup: Dict
    ) -> Dict[str, Any]:
        """Analyze single field mapping"""
        # Determine category
        field_category = category_lookup.get(source_field, "General")

        # Determine criticality
        critical_patterns = ["number", "id", "cause", "plan", "date"]
        is_critical = any(pattern in target_field.lower() for pattern in critical_patterns)

        return {
            "entity": entity_name,
            "target_field": target_field,
            "source_field": source_field,
            "category": field_category,
            "critical": is_critical,
        }

    def _analyze_mapping_patterns(self, mappings: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in field mappings"""
        entity_counts = {}
        category_counts = {}

        for mapping in mappings:
            entity = mapping["entity"]
            category = mapping["category"]

            entity_counts[entity] = entity_counts.get(entity, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1

        return {
            "entity_distribution": entity_counts,
            "category_distribution": category_counts,
            "most_mapped_entity": max(entity_counts, key=entity_counts.get)
            if entity_counts
            else None,
            "dominant_category": max(category_counts, key=category_counts.get)
            if category_counts
            else None,
        }

    def _generate_completion_summary(self, completion_data: Dict) -> Dict[str, Any]:
        """Generate workflow completion summary"""
        if not completion_data:
            return {}

        rates = [data.get("completion_rate", 0) for data in completion_data.values()]

        return {
            "average_completion": sum(rates) / len(rates) if rates else 0,
            "highest_completion": max(rates) if rates else 0,
            "lowest_completion": min(rates) if rates else 0,
            "entities_analyzed": len(completion_data),
        }

    def _calculate_mapping_coverage(self, entity_mappings: Dict) -> Dict[str, Any]:
        """Calculate mapping coverage statistics"""
        total_entities = len(get_entity_names())
        mapped_entities = len(entity_mappings)

        return {
            "coverage_ratio": mapped_entities / total_entities if total_entities > 0 else 0,
            "mapped_entities": mapped_entities,
            "total_entities": total_entities,
            "unmapped_entities": total_entities - mapped_entities,
        }

    def _is_technical_field(self, prop_name: str, prop_info: Dict) -> bool:
        """Check if field is technical (primary/foreign key)"""
        is_primary_key = prop_info.get("primary_key", False)
        is_foreign_key = prop_name.endswith("_id") and not is_primary_key
        return is_primary_key or is_foreign_key

    def _get_business_title(self, entity_name: str) -> str:
        """Get business-friendly title for entity"""
        title_mapping = {
            "ActionRequest": "Incident Reporting",
            "Problem": "Problem Definition",
            "RootCause": "Causal Analysis",
            "ActionPlan": "Resolution Planning",
            "Verification": "Effectiveness Check",
        }
        return title_mapping.get(entity_name, entity_name)

    def _get_entity_info_for_support(self, entity_name: str) -> Dict[str, Any]:
        """Get entity information for supporting entity processing"""
        count = self.query_manager.get_entity_count(entity_name)
        completion_rate = min(100.0, (count / 5) * 100) if count > 0 else 0.0

        # Get field count from schema
        entities = self.schema.get("entities", [])
        entity_def = next((e for e in entities if e["name"] == entity_name), {})
        field_count = len(entity_def.get("properties", {}))

        return {
            "entity_name": entity_name,
            "field_count": field_count,
            "completion_rate": completion_rate,
            "entity_count": count,
            "card_height": 120,  # Standard supporting entity height
        }

    def _stage_to_dict(self, stage: WorkflowStage) -> Dict[str, Any]:
        """Convert WorkflowStage to dictionary"""
        return {
            "stage_number": stage.stage_number,
            "entity_name": stage.entity_name,
            "title": stage.title,
            "field_count": stage.field_count,
            "completion_rate": stage.completion_rate,
            "source_fields": stage.business_fields,
            "complexity_level": stage.complexity_level,
        }


# Singleton pattern
_workflow_processor = None


def get_workflow_processor() -> WorkflowProcessor:
    """Get singleton workflow processor instance"""
    global _workflow_processor
    if _workflow_processor is None:
        _workflow_processor = WorkflowProcessor()
    return _workflow_processor
