#!/usr/bin/env python3
"""
Core Workflow Processing Engine - Business Logic Authority
Centralized workflow intelligence with schema-driven stage analysis.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from configs.environment import (
    get_entity_classification,
    get_entity_connections,
    get_entity_names,
    get_mappings,
    get_schema,
    get_workflow_stages_config,
)
from mine_core.database.query_manager import QueryManager, get_query_manager
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

    def __init__(self, query_manager: QueryManager):
        self.query_manager = query_manager
        self.mappings = get_mappings()
        self.schema = get_schema()

    def analyze_workflow_schema(self) -> Dict[str, Any]:
        """Fixed workflow schema analysis with proper entity counting"""
        try:
            # Get actual entity counts from database
            workflow_entities_order = [
                "ActionRequest",
                "Problem",
                "RootCause",
                "ActionPlan",
                "Verification",
            ]
            entity_analysis = []

            for i, entity_name in enumerate(workflow_entities_order, 1):
                entity_def = self._get_entity_definition(entity_name)
                if entity_def:
                    enhanced_entity = self._enhance_entity_definition(entity_def, i)
                    count = self.query_manager.get_entity_count(entity_name)
                    enhanced_entity["record_count"] = count  # Add record count
                    entity_analysis.append(enhanced_entity)

            # Recalculate total_fields based on enhanced entities
            total_fields = sum(e["field_count"] for e in entity_analysis)

            return {
                "workflow_entities": entity_analysis,
                "total_entities": len(entity_analysis),
                "total_fields": total_fields,
                "analytical_dimensions": 4,  # Based on field categories
                "field_categories": 5,  # From field_mappings.json
                "entity_complexity": self._calculate_complexity(entity_analysis),
            }
        except Exception as e:
            logger.error(f"Workflow schema analysis failed: {e}")
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

            # Get total ActionRequest count as the universal base for supporting entity completeness
            total_action_requests_for_support = self.query_manager.get_entity_count("ActionRequest")
            if total_action_requests_for_support == 0:
                logger.warning(
                    "WorkflowProcessor: No ActionRequest records found for supporting entities completion. Defaulting to 0."
                )

            # Process supporting entities, passing the total ActionRequest count
            supporting_entities = self._process_supporting_entities(
                total_action_requests_for_support
            )

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

            # Get total ActionRequest count as the universal base for supporting entity completeness
            total_action_requests_for_visualization = self.query_manager.get_entity_count(
                "ActionRequest"
            )
            if total_action_requests_for_visualization == 0:
                logger.warning(
                    "WorkflowProcessor: No ActionRequest records found for supporting entities visualization. Defaulting to 0."
                )

            # Get entity classification for supporting entities
            entity_classification = get_entity_classification()
            entity_connections = get_entity_connections()

            # Process supporting entities with connections
            supporting_entities = self._process_supporting_with_connections(
                entity_classification, entity_connections, total_action_requests_for_visualization
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

    def get_all_entity_fields(self, entity_name: str) -> List[str]:
        """Extract all internal field names for entity from field_mappings.json"""
        entity_mappings = self.mappings.get("entity_mappings", {})
        entity_fields = entity_mappings.get(entity_name, {})
        return list(entity_fields.keys())

    def calculate_comprehensive_field_completion(
        self, entity_name: str, total_action_requests: int
    ) -> Dict[str, Any]:
        """Calculate completion rate for every field in entity"""
        try:
            all_fields = self.get_all_entity_fields(entity_name)

            # For ActionRequest itself, set its completeness to 100% if records exist
            if entity_name == "ActionRequest":
                ar_total_count = self.query_manager.get_entity_count("ActionRequest")
                return {
                    "entity_name": entity_name,
                    "completion_rate": 100.0 if ar_total_count > 0 else 0.0,
                    "field_count": len(all_fields),
                    "field_details": [
                        {
                            "field_name": "Action Request Number",
                            "valid_count": ar_total_count,
                            "total_count": ar_total_count,
                            "completion_rate": 100.0 if ar_total_count > 0 else 0.0,
                        }
                    ],
                    "total_records": ar_total_count,
                }

            # For other entities, count how many instances are connected to an ActionRequest and have essential fields
            # The total_count for these entities will now be total_action_requests.
            if total_action_requests == 0 or not all_fields:
                return {
                    "entity_name": entity_name,
                    "completion_rate": 0.0,
                    "field_details": [],
                    "total_records": total_action_requests,
                }

            field_details = []
            completion_rates = []

            for field in all_fields:
                # Query to count entities (e.g., Problem, RootCause) that are connected to an ActionRequest
                # AND have the current 'field' populated.
                query = f"""
                MATCH (ar:ActionRequest)
                WHERE NOT '_SchemaTemplate' IN labels(ar)
                OPTIONAL MATCH (ar)-[*0..]->(n:{entity_name})
                WHERE n.{field} IS NOT NULL
                  AND toString(n.{field}) <> ''
                  AND toString(n.{field}) <> 'DATA_NOT_AVAILABLE'
                  AND toString(n.{field}) <> 'null'
                  AND toString(n.{field}) <> 'None'
                  AND toString(n.{field}) <> 'N/A'
                  AND toString(n.{field}) <> 'TBD'
                RETURN count(DISTINCT n) AS valid_count
                """

                result = self.query_manager.execute_query(query)
                valid_count = result.data[0]["valid_count"] if result.success else 0

                # Calculate field rate against total_action_requests
                field_rate = (valid_count / total_action_requests) * 100

                field_details.append(
                    {
                        "field_name": field,
                        "valid_count": valid_count,
                        "total_count": total_action_requests,  # Base is total ActionRequests
                        "completion_rate": field_rate,
                    }
                )
                completion_rates.append(field_rate)

            # Calculate overall rate as average of field rates
            overall_rate = (
                sum(completion_rates) / len(completion_rates) if completion_rates else 0.0
            )

            return {
                "entity_name": entity_name,
                "completion_rate": overall_rate,
                "field_count": len(all_fields),
                "field_details": field_details,
                "total_records": total_action_requests,  # Base is total ActionRequests
            }

        except Exception as e:
            handle_error(logger, e, f"comprehensive completion for {entity_name}")
            return {
                "entity_name": entity_name,
                "completion_rate": 0.0,
                "field_details": [],
                "total_records": 0,
            }

    def analyze_all_entity_completions(self) -> Dict[str, Any]:
        """Calculate comprehensive completion for all workflow entities and supporting entities using field-level averaging from workflow stages"""
        entity_names = ["ActionRequest", "Problem", "RootCause", "ActionPlan", "Verification"]
        supporting_entities = [
            "Facility",
            "Department",
            "Asset",
            "RecurringStatus",
            "AmountOfLoss",
            "Review",
            "EquipmentStrategy",
        ]

        workflow_completions = {}
        supporting_completions = {}

        # Get all 41 raw field completion rates (already based on ActionRequest count)
        raw_field_completion_rates = self.calculate_raw_field_completion_rates()
        if not raw_field_completion_rates:
            logger.warning(
                "WorkflowProcessor: No raw field completion rates available. Cannot calculate entity completion rates."
            )
            return {"workflow_entities": {}, "supporting_entities": {}}

        total_action_requests = self.query_manager.get_entity_count("ActionRequest")
        if total_action_requests == 0:
            logger.warning(
                "WorkflowProcessor: No ActionRequest records found. Cannot calculate entity completion rates based on total ActionRequests."
            )
            return {"workflow_entities": {}, "supporting_entities": {}}

        # Get workflow stages configuration to use business fields for consistency with frontend
        workflow_config = get_workflow_stages_config()
        stage_configs = workflow_config.get("workflow_stages", [])

        # Helper to get raw field names for a given entity
        def _get_raw_fields_for_entity(entity_name_to_map: str) -> List[str]:
            entity_raw_fields = []
            entity_mappings = self.mappings.get("entity_mappings", {}).get(entity_name_to_map, {})
            for internal_field, raw_field in entity_mappings.items():
                if raw_field != "root_cause_tail_extraction":  # Ensure derived field is skipped
                    entity_raw_fields.append(raw_field)
            return entity_raw_fields

        # Calculate completeness for workflow entities using the same logic as _process_workflow_stages
        for entity in entity_names:
            # Find the stage configuration for this entity
            stage_config = next((stage for stage in stage_configs if stage.get("entity_name") == entity), None)

            if entity == "ActionRequest":
                # Use the same field-level completion calculation as _process_workflow_stages for consistency
                ar_count = self.query_manager.get_entity_count("ActionRequest")

                if stage_config:
                    business_fields = stage_config.get("business_fields", [])
                    completion_rate = self._calculate_stage_field_completion(
                        entity, business_fields, raw_field_completion_rates
                    )
                    total_fields = len(business_fields)
                else:
                    # Fallback to raw field averaging if no stage config found
                    entity_raw_fields = _get_raw_fields_for_entity(entity)
                    relevant_field_rates = [
                        raw_field_completion_rates.get(field, 0.0)
                        for field in entity_raw_fields
                    ]
                    completion_rate = (
                        sum(relevant_field_rates) / len(relevant_field_rates)
                        if relevant_field_rates
                        else 0.0
                    )
                    total_fields = len(entity_raw_fields)

                workflow_completions[entity] = {
                    "entity_name": entity,
                    "completion_rate": round(completion_rate, 1),
                    "field_count": total_fields,
                    "total_records": ar_count,
                }
            else:
                # Use the same field-level completion calculation as _process_workflow_stages
                if stage_config:
                    business_fields = stage_config.get("business_fields", [])
                    completion_rate = self._calculate_stage_field_completion(
                        entity, business_fields, raw_field_completion_rates
                    )
                    total_fields = len(business_fields)
                else:
                    # Fallback to raw field averaging if no stage config found
                    entity_raw_fields = _get_raw_fields_for_entity(entity)
                    relevant_field_rates = [
                        raw_field_completion_rates.get(field, 0.0)
                        for field in entity_raw_fields
                    ]
                    completion_rate = (
                        sum(relevant_field_rates) / len(relevant_field_rates)
                        if relevant_field_rates
                        else 0.0
                    )
                    total_fields = len(entity_raw_fields)

                workflow_completions[entity] = {
                    "entity_name": entity,
                    "completion_rate": round(completion_rate, 1),
                    "field_count": total_fields,
                    "total_records": total_action_requests,  # Base is always total ActionRequests
                }

        # Calculate completeness for supporting entities
        for entity in supporting_entities:
            entity_raw_fields = _get_raw_fields_for_entity(entity)
            relevant_field_rates = [
                raw_field_completion_rates.get(field, 0.0)  # Get rate from 41-field analysis
                for field in entity_raw_fields
            ]
            completion_rate = (
                sum(relevant_field_rates) / len(relevant_field_rates)
                if relevant_field_rates
                else 0.0
            )
            total_fields = len(entity_raw_fields)
            supporting_completions[entity] = {
                "entity_name": entity,
                "completion_rate": round(completion_rate, 1),
                "field_count": total_fields,
                "total_records": total_action_requests,  # Base is always total ActionRequests
            }

        return {
            "workflow_entities": workflow_completions,
            "supporting_entities": supporting_completions,
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def get_all_raw_field_names(self) -> List[str]:
        """Extract all 41 raw field names from field_mappings.json"""
        entity_mappings = self.mappings.get("entity_mappings", {})
        all_raw_fields = []

        for entity_name, field_mapping in entity_mappings.items():
            # Get raw field names (values in mapping)
            raw_fields = list(field_mapping.values())
            all_raw_fields.extend(raw_fields)

        return all_raw_fields

    def calculate_raw_field_completion_rates(self) -> Dict[str, float]:
        """Calculate completion for each raw field name"""
        try:
            entity_mappings = self.mappings.get("entity_mappings", {})
            field_completion_rates = {}

            logger.info(
                f"WorkflowProcessor: Starting raw field completion calculation. Loaded entity mappings for {len(entity_mappings)} entities."
            )

            # Get total ActionRequest count as the universal base for completeness
            total_action_requests = self.query_manager.get_entity_count("ActionRequest")
            if total_action_requests == 0:
                logger.warning(
                    "WorkflowProcessor: No ActionRequest records found. Cannot calculate raw field completion rates."
                )
                return {}

            logger.info(
                f"WorkflowProcessor: Total ActionRequest count (base for completeness): {total_action_requests}"
            )

            # Process each entity's field mappings
            for entity_name, field_mapping in entity_mappings.items():
                if entity_name == "Facility":
                    logger.info(
                        "WorkflowProcessor: Skipping 'Facility' entity for raw field completion calculation."
                    )
                    continue

                # Use total_action_requests as the base for all calculations
                # The assumption is that all fields, regardless of entity, are assessed against the total ActionRequest count
                # This aligns with the "41 base is the count of action request number" requirement.

                for internal_field, raw_field in field_mapping.items():
                    # Exclude 'root_cause_tail_extraction' which is a derived field and not a raw field for completeness analysis
                    if internal_field == "root_cause_tail_extraction":
                        logger.info(
                            f"WorkflowProcessor: Skipping derived field '{internal_field}' from raw field completion calculation."
                        )
                        continue
                    query = f"""
                    MATCH (n:{entity_name})
                    WHERE n.{internal_field} IS NOT NULL
                      AND toString(n.{internal_field}) <> ''
                      AND toString(n.{internal_field}) <> 'DATA_NOT_AVAILABLE'
                      AND toString(n.{internal_field}) <> 'null'
                      AND toString(n.{internal_field}) <> 'None'
                      AND toString(n.{internal_field}) <> 'N/A'
                    RETURN count(n) AS valid_count
                    """

                    result = self.query_manager.execute_query(query)
                    valid_count = result.data[0]["valid_count"] if result.success else 0

                    # Calculate completion rate against total_action_requests
                    completion_rate = (valid_count / total_action_requests) * 100

                    field_completion_rates[raw_field] = completion_rate
                    logger.info(
                        f"WorkflowProcessor: Calculated completion for raw field '{raw_field}' (internal: {internal_field}) in entity '{entity_name}': {completion_rate:.2f}%"
                    )

            logger.info(
                f"WorkflowProcessor: Finished raw field completion calculation. Total unique raw fields with rates: {len(field_completion_rates)}"
            )
            return field_completion_rates

        except Exception as e:
            handle_error(logger, e, "raw field completion calculation")
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
        """Process workflow stages with completion rates calculated by averaging field completion rates"""
        stage_configs = workflow_config.get("workflow_stages", [])

        # Get raw field completion rates from the accurate 41-field calculation
        raw_field_completion_rates = self.calculate_raw_field_completion_rates()

        stages = []
        for stage_config in stage_configs:
            entity_name = stage_config.get("entity_name", "")
            business_fields = stage_config.get("business_fields", [])

            # Calculate stage completion by averaging the completion rates of fields belonging to this stage
            completion_rate = self._calculate_stage_field_completion(
                entity_name, business_fields, raw_field_completion_rates
            )

            # Calculate complexity
            field_count = len(business_fields)
            complexity = (
                "complex" if field_count >= 6 else "moderate" if field_count >= 3 else "simple"
            )

            stage = WorkflowStage(
                stage_number=stage_config.get("stage_number", 1),
                entity_name=entity_name,
                title=stage_config.get("title", entity_name),
                field_count=field_count,
                completion_rate=completion_rate,
                business_fields=business_fields,
                complexity_level=complexity,
            )

            stages.append(stage)

        return stages

    def _process_supporting_entities(self, total_action_requests: int) -> List[Dict[str, Any]]:
        """Process supporting entities for workflow context"""
        entity_classification = get_entity_classification()
        supporting_entities = (
            entity_classification.get("entity_types", {})
            .get("supporting_entities", {})
            .get("entities", [])
        )

        processed_entities = []
        for entity_name in supporting_entities:
            entity_info = self._get_entity_info_for_support(entity_name, total_action_requests)
            processed_entities.append(entity_info)

        return processed_entities

    def _process_supporting_with_connections(
        self, entity_classification: Dict, entity_connections: Dict, total_action_requests: int
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
            entity_info = self._get_entity_info_for_support(entity_name, total_action_requests)
            entity_info["connects_to"] = connections.get(entity_name, "Unknown")
            entity_info["color"] = "#6C757D"  # Default supporting entity color
            processed.append(entity_info)

        return processed

    def _get_entity_completion_rates(self) -> Dict[str, Any]:
        """Retrieve pre-calculated completion rates for workflow entities"""
        try:
            # Get comprehensive analysis which now calculates all entity completions
            all_entity_completions = self.analyze_all_entity_completions()
            return all_entity_completions.get("workflow_entities", {})
        except Exception as e:
            handle_error(logger, e, "retrieving workflow entity completion rates")
            return {}

    def _get_essential_fields_config(self, entity_name: str) -> List[str]:
        """Get essential fields from a centralized configuration (workflow_stages.json)"""
        workflow_config = get_workflow_stages_config()
        for stage in workflow_config.get("workflow_stages", []):
            if stage.get("entity_name") == entity_name:
                return stage.get("business_fields", [])
        return []

    def _resolve_business_fields(
        self, entity_name: str, business_fields_display: List[str]
    ) -> List[str]:
        """Resolve business field display names to actual database fields"""
        entity_mappings = self.mappings.get("entity_mappings", {}).get(entity_name, {})
        reversed_mappings = {
            v: k for k, v in entity_mappings.items()
        }  # display name -> internal name

        resolved_fields = []
        for display_name in business_fields_display:
            internal_name = reversed_mappings.get(display_name)
            if internal_name:
                resolved_fields.append(internal_name)
            else:
                logger.warning(
                    f"Business field display name '{display_name}' not found in field_mappings for entity '{entity_name}'."
                )
        return resolved_fields

    def _count_complete_records(self, entity_name: str, internal_fields: List[str]) -> int:
        """Count records where all specified internal fields are not null"""
        if not internal_fields:
            return 0

        where_clauses = [f"n.{field} IS NOT NULL" for field in internal_fields]
        where_clause_str = " AND ".join(where_clauses)

        # Exclude template nodes from the count
        template_exclude_clause = "WHERE NOT '_SchemaTemplate' IN labels(n)"
        final_where_clause = f"{template_exclude_clause} AND {where_clause_str}"

        query = f"MATCH (n:{entity_name}) {final_where_clause} RETURN count(n) AS count"

        result = self.query_manager.execute_query(query)
        return result.data[0]["count"] if result.success and result.data else 0

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

    def _get_entity_info_for_support(
        self, entity_name: str, total_action_requests: int
    ) -> Dict[str, Any]:
        """Retrieve pre-calculated entity information for supporting entities"""
        try:
            # Get comprehensive analysis which now calculates all entity completions
            all_entity_completions = self.analyze_all_entity_completions()
            supporting_completions = all_entity_completions.get("supporting_entities", {})

            entity_info = supporting_completions.get(entity_name, {})

            # Ensure it has all required fields even if the entity was not found in completions
            if not entity_info:
                # Get field count from schema for accurate completion rate (for cases where entity might not have records)
                entities = self.schema.get("entities", [])
                entity_def = next((e for e in entities if e["name"] == entity_name), {})
                field_count = len(entity_def.get("properties", {}))

                entity_info = {
                    "entity_name": entity_name,
                    "field_count": field_count,
                    "completion_rate": 0.0,
                    "entity_count": total_action_requests,  # Base is total ActionRequests
                    "card_height": 120,  # Standard supporting entity height
                }

            return entity_info

        except Exception as e:
            handle_error(logger, e, f"retrieving supporting entity info for {entity_name}")
            return {
                "entity_name": entity_name,
                "field_count": 0,
                "completion_rate": 0.0,
                "entity_count": 0,
                "card_height": 120,
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

    def _get_entity_definition(self, entity_type: str) -> Dict[str, Any]:
        """Get entity definition from schema with caching for WorkflowProcessor use"""
        # This cache is specific to WorkflowProcessor to avoid re-parsing schema
        if not hasattr(self, "_entity_def_cache"):
            self._entity_def_cache = {}

        if entity_type not in self._entity_def_cache:
            entities = self.schema.get("entities", [])
            entity_def = next((e for e in entities if e["name"] == entity_type), {})
            self._entity_def_cache[entity_type] = entity_def

        return self._entity_def_cache[entity_type]

    def _calculate_complexity(self, workflow_entities: List[Dict]) -> Dict[str, Any]:
        """Analyze complexity distribution across entities"""
        complexity_levels = {"complex": 0, "moderate": 0, "simple": 0}
        total_entities = len(workflow_entities)

        for entity in workflow_entities:
            complexity_level = entity["complexity_level"]
            complexity_levels[complexity_level] += 1

        return {
            "complexity_distribution": {
                "complex": complexity_levels["complex"] / total_entities
                if total_entities > 0
                else 0,
                "moderate": complexity_levels["moderate"] / total_entities
                if total_entities > 0
                else 0,
                "simple": complexity_levels["simple"] / total_entities if total_entities > 0 else 0,
            },
            "total_entities": total_entities,
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

    def _calculate_real_completion_rate(self, entity_name: str) -> float:
        """Calculate completion based on essential field validation"""
        try:
            # Get total entity count
            total_count = self.query_manager.get_entity_count(entity_name)
            if total_count == 0:
                return 0.0

            # Essential field validation queries per entity
            essential_field_queries = {
                "ActionRequest": "n.title IS NOT NULL AND n.categories IS NOT NULL",
                "Problem": "n.what_happened IS NOT NULL",
                "RootCause": "n.root_cause IS NOT NULL",
                "ActionPlan": "n.action_plan IS NOT NULL",
                "Verification": "n.is_action_plan_effective IS NOT NULL",
            }

            essential_condition = essential_field_queries.get(entity_name, "true")

            query = f"""
            MATCH (n:{entity_name})
            WHERE {essential_condition}
            RETURN count(n) AS completed_count
            """

            result = self.query_manager.execute_query(query)
            completed_count = result.data[0]["completed_count"] if result.success else 0

            return (completed_count / total_count) * 100

        except Exception as e:
            handle_error(logger, e, f"completion calculation for {entity_name}")
            return 0.0

    def _calculate_stage_field_completion(
        self, entity_name: str, business_fields: List[str], raw_field_completion_rates: Dict[str, float]
    ) -> float:
        """Calculate stage completion by averaging completion rates of fields belonging to the stage"""
        try:
            if not business_fields or not raw_field_completion_rates:
                return 0.0

            # Map business fields to raw field names using field mappings
            entity_mappings = self.mappings.get("entity_mappings", {}).get(entity_name, {})

            # Create reverse mapping: raw field name -> internal field name
            reverse_mapping = {raw_field: internal_field for internal_field, raw_field in entity_mappings.items()}

            # Find completion rates for stage fields
            stage_field_rates = []

            for business_field in business_fields:
                # Try to find the raw field completion rate
                # First try direct lookup (business field == raw field)
                if business_field in raw_field_completion_rates:
                    stage_field_rates.append(raw_field_completion_rates[business_field])
                else:
                    # Try to find through entity mappings
                    # Look for internal field that matches business field name pattern
                    internal_field = None
                    for internal, raw in entity_mappings.items():
                        if raw == business_field or internal == business_field:
                            internal_field = internal
                            break

                    if internal_field:
                        # Get the raw field name and its completion rate
                        raw_field = entity_mappings.get(internal_field)
                        if raw_field and raw_field in raw_field_completion_rates:
                            stage_field_rates.append(raw_field_completion_rates[raw_field])
                        else:
                            logger.warning(
                                f"Raw field '{raw_field}' for business field '{business_field}' not found in completion rates for entity '{entity_name}'"
                            )
                    else:
                        logger.warning(
                            f"Could not map business field '{business_field}' to raw field for entity '{entity_name}'"
                        )

            # Calculate average completion rate for the stage
            if stage_field_rates:
                average_completion = sum(stage_field_rates) / len(stage_field_rates)
                logger.info(
                    f"Stage completion for '{entity_name}': {average_completion:.1f}% (averaged from {len(stage_field_rates)} fields)"
                )
                return round(average_completion, 1)
            else:
                logger.warning(
                    f"No valid field completion rates found for stage '{entity_name}' with {len(business_fields)} business fields"
                )
                return 0.0

        except Exception as e:
            handle_error(logger, e, f"stage field completion calculation for {entity_name}")
            return 0.0


# Singleton pattern
_workflow_processor = None


def get_workflow_processor() -> WorkflowProcessor:
    """Get singleton workflow processor instance"""
    global _workflow_processor
    if _workflow_processor is None:
        _workflow_processor = WorkflowProcessor(get_query_manager())
    return _workflow_processor
