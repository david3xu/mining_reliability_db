#!/usr/bin/env python3
"""
Dashboard Data Adapter - Extended with Workflow Methods
Clean adapter pattern implementation for all dashboard data needs.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from dashboard.adapters.interfaces import (
    PortfolioData, FacilityData, FieldData, TimelineData,
    ComponentMetadata, ValidationResult
)

# Real data sources - existing infrastructure
from mine_core.database.queries import (
    get_facilities,
    get_operational_performance_dashboard,
    get_action_requests,
    get_root_cause_intelligence_summary,
    get_field_completion_statistics,
    get_entity_completion_rates,
    get_facility_action_statistics
)
from mine_core.shared.common import handle_error
from configs.environment import (
    get_mappings, get_schema, get_entity_names, get_workflow_stages_config,
    get_entity_classification, get_entity_connections, get_field_analysis_config
)

logger = logging.getLogger(__name__)

class DashboardDataAdapter:
    """
    Complete data access layer with workflow-specific methods.
    Single point of coupling to mine_core business logic.
    """

    def __init__(self):
        """Initialize adapter with caching support."""
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes
        self._last_refresh = {}

    # EXISTING METHODS (Keep unchanged - working real data)
    def get_portfolio_metrics(self) -> PortfolioData:
        """Get core portfolio metrics for dashboard header cards"""
        try:
            logger.info("Adapter: Generating portfolio metrics")

            facilities = get_facilities()
            all_requests = get_action_requests(limit=10000)
            mappings = get_mappings()

            total_records = len(all_requests)

            entity_mappings = mappings.get("entity_mappings", {})
            all_fields = set()
            for entity_type, field_mapping in entity_mappings.items():
                all_fields.update(field_mapping.values())
            total_fields = len(all_fields)

            total_facilities = len(facilities)

            years_found = set()
            for request in all_requests:
                date_str = request.get('date', '')
                if date_str and len(date_str) >= 4:
                    try:
                        year = int(date_str[:4])
                        years_found.add(year)
                    except Exception as e:
                        handle_error(logger, e, "Failed to parse year from date string", {"date_str": date_str})
                        continue

            year_coverage = len(years_found) if years_found else 0
            min_year = min(years_found) if years_found else None
            max_year = max(years_found) if years_found else None

            return PortfolioData(
                total_records=total_records,
                data_fields=total_fields,
                facilities=total_facilities,
                years_coverage=year_coverage,
                year_detail=f"{min_year}-{max_year}" if min_year and max_year else "Unknown",
                metadata=ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=self._calculate_quality_score(all_requests)
                )
            )

        except Exception as e:
            handle_error(logger, e, "portfolio metrics generation")
            return self._create_empty_portfolio_data()

    def get_facility_breakdown(self) -> FacilityData:
        """Get facility-wise record distribution for pie chart"""
        try:
            logger.info("Adapter: Generating facility breakdown")

            facilities = get_facilities()

            labels = []
            values = []
            total_records = 0

            for facility in facilities:
                facility_id = facility.get('id', 'Unknown')
                incident_count = facility.get('incident_count', 0)

                labels.append(facility_id)
                values.append(incident_count)
                total_records += incident_count

            percentages = []
            for count in values:
                percentage = round((count / total_records * 100), 1) if total_records > 0 else 0
                percentages.append(percentage)

            return FacilityData(
                labels=labels,
                values=values,
                percentages=percentages,
                total_records=total_records,
                metadata=ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if total_records > 0 else 0.0
                )
            )

        except Exception as e:
            handle_error(logger, e, "facility breakdown generation")
            return self._create_empty_facility_data()

    def get_field_distribution(self) -> FieldData:
        """Get field type distribution for bar chart visualization"""
        try:
            logger.info("Adapter: Analyzing field distribution")

            mappings = get_mappings()
            field_categories = mappings.get("field_categories", {})

            category_mapping = {
                "descriptive_fields": "Text/String (Unstructured)",
                "temporal_fields": "Date (Temporal)",
                "categorical_fields": "Categorical (Discrete)",
                "boolean_fields": "Boolean (Binary)",
                "identification_fields": "List (Multi-value)",
                "quantitative_fields": "Numeric (Quantitative)"
            }

            labels = []
            values = []
            total_fields = 0

            for category, display_name in category_mapping.items():
                field_count = len(field_categories.get(category, []))
                labels.append(display_name)
                values.append(field_count)
                total_fields += field_count

            percentages = []
            for count in values:
                percentage = round((count / total_fields) * 100, 1) if total_fields > 0 else 0
                percentages.append(percentage)

            return FieldData(
                labels=labels,
                values=values,
                percentages=percentages,
                total_fields=total_fields,
                metadata=ComponentMetadata(
                    source="configs.mappings",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if total_fields > 0 else 0.0
                )
            )

        except Exception as e:
            handle_error(logger, e, "field distribution analysis")
            return self._create_empty_field_data()

    def get_historical_timeline(self) -> TimelineData:
        """Get historical records timeline for table visualization"""
        try:
            logger.info("Adapter: Generating historical timeline")

            all_requests = get_action_requests(limit=10000)
            facilities = get_facilities()

            facility_names = [f.get('id', 'Unknown') for f in facilities]
            timeline_data = {}
            year_totals = {}
            facility_totals = {}

            for facility_id in facility_names:
                timeline_data[facility_id] = {}
                facility_totals[facility_id] = 0

            for request in all_requests:
                date_str = request.get('date', '')
                facility_id = request.get('facility_id', 'Unknown')

                if date_str and len(date_str) >= 4 and facility_id in facility_names:
                    try:
                        year = int(date_str[:4])

                        if year not in timeline_data[facility_id]:
                            timeline_data[facility_id][year] = 0
                        if year not in year_totals:
                            year_totals[year] = 0

                        timeline_data[facility_id][year] += 1
                        year_totals[year] += 1
                        facility_totals[facility_id] += 1
                    except Exception as e:
                        handle_error(logger, e, "Failed to parse year from action request date", {"date_str": date_str})
                        continue

            if year_totals:
                min_year = min(year_totals.keys())
                max_year = max(year_totals.keys())
                year_range = list(range(min_year, max_year + 1))
            else:
                year_range = []

            table_rows = []
            for facility_id in facility_names:
                row = {
                    "facility": facility_id,
                    "total": facility_totals[facility_id]
                }

                for year in year_range:
                    row[str(year)] = timeline_data[facility_id].get(year, 0)

                table_rows.append(row)

            totals_row = {"facility": "Total", "total": sum(facility_totals.values())}
            for year in year_range:
                totals_row[str(year)] = year_totals.get(year, 0)
            table_rows.append(totals_row)

            return TimelineData(
                columns=["facility"] + [str(year) for year in year_range] + ["total"],
                rows=table_rows,
                year_range=year_range,
                total_records=sum(facility_totals.values()),
                facilities_count=len(facility_names),
                metadata=ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if year_range else 0.0
                )
            )

        except Exception as e:
            handle_error(logger, e, "historical timeline generation")
            return self._create_empty_timeline_data()

    # EXISTING FACILITY-SPECIFIC METHODS
    def get_facility_performance_analysis(self, facility_id: str) -> Dict[str, Any]:
        """Get facility-specific performance analysis using real data"""
        try:
            logger.info(f"Adapter: Generating facility analysis for {facility_id}")

            # Real performance data for specific facility
            performance_data = get_operational_performance_dashboard(facility_id)

            # Real action requests for facility
            action_requests = get_action_requests(facility_id=facility_id, limit=10000)

            # Real causal intelligence for facility
            causal_data = get_root_cause_intelligence_summary(facility_id)

            # Process category distribution from real data
            category_distribution = {}
            for request in action_requests:
                category = request.get('categories', 'Unknown')
                if category not in category_distribution:
                    category_distribution[category] = 0
                category_distribution[category] += 1

            # Calculate percentages
            total_records = len(action_requests)
            category_percentages = {}
            for category, count in category_distribution.items():
                percentage = round((count / total_records * 100), 1) if total_records > 0 else 0
                category_percentages[category] = percentage

            return {
                "facility_id": facility_id,
                "total_records": total_records,
                "category_distribution": category_distribution,
                "category_percentages": category_percentages,
                "categories_count": len(category_distribution),
                "performance_metrics": performance_data,
                "causal_patterns": causal_data.get("causal_patterns", []),
                "temporal_trends": performance_data.get("temporal_trends", []),
                "workflow_efficiency": performance_data.get("workflow_efficiency", {}),
                "metadata": ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if total_records > 0 else 0.0
                )
            }

        except Exception as e:
            handle_error(logger, e, f"facility performance analysis for {facility_id}")
            return {}

    def get_facility_comparison_metrics(self, facility_id: str) -> Dict[str, Any]:
        """Compare facility performance against other facilities"""
        try:
            logger.info(f"Adapter: Generating facility comparison for {facility_id}")

            # Get data for target facility
            target_facility = self.get_facility_performance_analysis(facility_id)

            # Get data for all facilities for comparison
            all_facilities = get_facilities()
            facility_metrics = []

            for facility in all_facilities:
                other_facility_id = facility.get('id', 'Unknown')
                if other_facility_id != facility_id:
                    other_data = self.get_facility_performance_analysis(other_facility_id)
                    facility_metrics.append(other_data)

            # Calculate comparison metrics
            target_records = target_facility.get("total_records", 0)
            other_records = [f.get("total_records", 0) for f in facility_metrics]
            avg_other_records = sum(other_records) / len(other_records) if other_records else 0

            performance_rank = sum(1 for r in other_records if r < target_records) + 1
            total_facilities = len(other_records) + 1

            return {
                "facility_id": facility_id,
                "target_records": target_records,
                "average_other_records": avg_other_records,
                "performance_rank": performance_rank,
                "total_facilities": total_facilities,
                "percentile": round((performance_rank / total_facilities) * 100, 1),
                "vs_average": round(((target_records - avg_other_records) / avg_other_records * 100), 1) if avg_other_records > 0 else 0
            }

        except Exception as e:
            handle_error(logger, e, f"facility comparison for {facility_id}")
            return {}

    # NEW WORKFLOW METHODS - CLEAN ADAPTER PATTERN
    def get_workflow_schema_analysis(self) -> Dict[str, Any]:
        """Get workflow schema analysis for process flow visualization"""
        try:
            logger.info("Adapter: Generating workflow schema analysis")

            # Access configuration through adapter
            schema = get_schema()
            mappings = get_mappings()
            entity_names = get_entity_names()

            # Real schema data
            entity_mappings = mappings.get("entity_mappings", {})

            # Count unique field names across all entities (not field mappings per entity)
            unique_fields = set()
            for field_mapping in entity_mappings.values():
                unique_fields.update(field_mapping.values())
            total_fields = len(unique_fields)

            # Real entity count from schema
            entities_count = len(entity_names)

            # Real analytical dimensions
            analytical_dimensions = schema.get("analytical_dimensions", {})

            # Core workflow entities in business order
            workflow_entities = [
                {"name": "ActionRequest", "title": "Incident Reporting", "stage": 1},
                {"name": "Problem", "title": "Problem Definition", "stage": 2},
                {"name": "RootCause", "title": "Causal Analysis", "stage": 3},
                {"name": "ActionPlan", "title": "Resolution Planning", "stage": 4},
                {"name": "Verification", "title": "Effectiveness Check", "stage": 5}
            ]

            # Get real entity definitions from schema
            entities = schema.get("entities", [])
            entity_dict = {e["name"]: e for e in entities}

            # Enrich workflow entities with real data
            enriched_workflow = []
            for workflow_entity in workflow_entities:
                entity_name = workflow_entity["name"]
                entity_def = entity_dict.get(entity_name, {})

                # Real field count from schema
                properties = entity_def.get("properties", {})
                field_count = len(properties)

                # Business required fields (exclude primary keys and foreign keys)
                required_fields = 0
                for prop_name, prop_info in properties.items():
                    if prop_info.get("required", False):
                        # Skip primary keys and foreign keys - these are technical requirements
                        is_primary_key = prop_info.get("primary_key", False)
                        is_foreign_key = prop_name.endswith("_id") and not is_primary_key

                        # Only count business fields as required
                        if not is_primary_key and not is_foreign_key:
                            required_fields += 1

                # Enhanced entity data
                enriched_entity = {
                    **workflow_entity,
                    "field_count": field_count,
                    "required_fields": required_fields,
                    "properties": properties,
                    "complexity_level": "complex" if field_count >= 8 else "moderate" if field_count >= 5 else "simple"
                }

                enriched_workflow.append(enriched_entity)

            return {
                "workflow_entities": enriched_workflow,
                "total_entities": entities_count,
                "total_fields": total_fields,
                "analytical_dimensions": len(analytical_dimensions),
                "field_categories": len(mappings.get('field_categories', {})),
                "metadata": ComponentMetadata(
                    source="configs.schema",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if entities_count > 0 else 0.0
                )
            }

        except Exception as e:
            handle_error(logger, e, "workflow schema analysis")
            return {}

    def get_entity_field_distribution(self) -> Dict[str, Any]:
        """Get entity field distribution for bar chart visualization"""
        try:
            logger.info("Adapter: Generating entity field distribution")

            # Real schema data through adapter
            schema = get_schema()
            entities = schema.get("entities", [])

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
                "metadata": ComponentMetadata(
                    source="configs.schema",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if entities else 0.0
                )
            }

        except Exception as e:
            handle_error(logger, e, "entity field distribution")
            return {}

    def get_field_mapping_analysis(self) -> Dict[str, Any]:
        """Get field mapping analysis for detailed table"""
        try:
            logger.info("Adapter: Generating field mapping analysis")

            # Real field mappings through adapter
            mappings = get_mappings()
            entity_mappings = mappings.get("entity_mappings", {})
            field_categories = mappings.get("field_categories", {})

            if not entity_mappings:
                return {}

            # Build field category lookup
            category_lookup = {}
            for category, fields in field_categories.items():
                for field in fields:
                    category_lookup[field] = category.replace("_fields", "").title()

            # Analyze mappings
            mapping_analysis = []
            for entity_name, field_mapping in entity_mappings.items():
                for target_field, source_field in field_mapping.items():

                    # Determine field category
                    field_category = category_lookup.get(source_field, "General")

                    # Determine if critical based on field name patterns
                    critical_patterns = ["number", "id", "cause", "plan", "date"]
                    is_critical = any(pattern in target_field.lower()
                                    for pattern in critical_patterns)

                    mapping_analysis.append({
                        "entity": entity_name,
                        "target_field": target_field,
                        "source_field": source_field,
                        "category": field_category,
                        "critical": is_critical
                    })

            return {
                "mappings": mapping_analysis,
                "total_mappings": len(mapping_analysis),
                "entities_covered": len(entity_mappings),
                "categories_found": len(set(m["category"] for m in mapping_analysis)),
                "critical_fields": sum(1 for m in mapping_analysis if m["critical"]),
                "metadata": ComponentMetadata(
                    source="configs.mappings",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if mapping_analysis else 0.0
                )
            }

        except Exception as e:
            handle_error(logger, e, "field mapping analysis")
            return {}

    def get_field_mapping_counts(self) -> Dict[str, Any]:
        """Get field mapping counts for workflow metrics - encapsulates mapping access"""
        try:
            logger.info("Adapter: Analyzing field mapping counts")

            # Access configuration through adapter (not directly in component)
            mappings = get_mappings()
            entity_mappings = mappings.get("entity_mappings", {})

            # Count source fields
            raw_source_fields = []
            for entity_name, mapping in entity_mappings.items():
                raw_source_fields.extend(mapping.values())

            # Return total unique source fields
            total_fields = len(set(raw_source_fields))

            return {
                "total_fields": total_fields,
                "entity_mappings": entity_mappings,
                "source_fields": list(set(raw_source_fields))
            }

        except Exception as e:
            handle_error(logger, e, "field mapping counts analysis")
            return {
                "total_fields": 0,
                "entity_mappings": {},
                "source_fields": []
            }

    def validate_data_availability(self) -> ValidationResult:
        """Validate data availability for dashboard components"""
        try:
            validation_status = {
                "portfolio_metrics": False,
                "facility_breakdown": False,
                "field_distribution": False,
                "historical_timeline": False,
                "workflow_schema": False,
                "entity_distribution": False,
                "field_mapping": False
            }

            portfolio_data = self.get_portfolio_metrics()
            validation_status["portfolio_metrics"] = portfolio_data.total_records > 0

            facility_data = self.get_facility_breakdown()
            validation_status["facility_breakdown"] = facility_data.total_records > 0

            field_data = self.get_field_distribution()
            validation_status["field_distribution"] = field_data.total_fields > 0

            timeline_data = self.get_historical_timeline()
            validation_status["historical_timeline"] = timeline_data.total_records > 0

            # New workflow validations
            workflow_data = self.get_workflow_schema_analysis()
            validation_status["workflow_schema"] = bool(workflow_data.get("total_entities", 0) > 0)

            entity_data = self.get_entity_field_distribution()
            validation_status["entity_distribution"] = bool(entity_data.get("total_entities", 0) > 0)

            mapping_data = self.get_field_mapping_analysis()
            validation_status["field_mapping"] = bool(mapping_data.get("total_mappings", 0) > 0)

            all_valid = all(validation_status.values())

            return ValidationResult(
                is_valid=all_valid,
                component_status=validation_status,
                error_details=None if all_valid else "Some data components failed validation",
                data_quality_score=sum(validation_status.values()) / len(validation_status)
            )

        except Exception as e:
            handle_error(logger, e, "data validation")
            return ValidationResult(
                is_valid=False,
                component_status={},
                error_details=str(e),
                data_quality_score=0.0
            )

    # HELPER METHODS (Keep existing)
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        from datetime import datetime
        return datetime.now().isoformat()

    def _calculate_quality_score(self, data: List[Dict]) -> float:
        """Calculate data quality score based on completeness."""
        if not data:
            return 0.0
        return min(1.0, len(data) / 1000)

    def _create_empty_portfolio_data(self) -> PortfolioData:
        """Create empty portfolio data for error cases."""
        return PortfolioData(
            total_records=0, data_fields=0, facilities=0, years_coverage=0,
            year_detail="No data", metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_facility_data(self) -> FacilityData:
        """Create empty facility data for error cases."""
        return FacilityData(
            labels=[], values=[], percentages=[], total_records=0,
            metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_field_data(self) -> FieldData:
        """Create empty field data for error cases."""
        return FieldData(
            labels=[], values=[], percentages=[], total_fields=0,
            metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_timeline_data(self) -> TimelineData:
        """Create empty timeline data for error cases."""
        return TimelineData(
            columns=[], rows=[], year_range=[], total_records=0, facilities_count=0,
            metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    # NEO4J-DRIVEN ANALYTICS METHODS

    def get_entity_completion_analysis(self) -> Dict[str, Any]:
        """Get entity completion analysis using Neo4j data and configuration"""
        try:
            logger.info("Adapter: Getting Neo4j entity completion analysis")

            # Get Neo4j entity completion rates
            entity_data = get_entity_completion_rates()

            # Get entity classification config for ordering and display
            entity_config = get_entity_classification()
            entity_order = entity_config.get("entity_order", [])

            # Structure the response with configuration
            structured_entities = []
            for entity_name in entity_order:
                if entity_name in entity_data:
                    entity_info = entity_data[entity_name]
                    structured_entities.append({
                        "entity_name": entity_name,
                        "total_count": entity_info.get("total_count", 0),
                        "completion_rate": entity_info.get("completion_rate", 0.0),
                        "completed_fields": entity_info.get("completed_fields", 0),
                        "total_fields": entity_info.get("total_fields", 0)
                    })

            return {
                "entities": structured_entities,
                "entity_config": entity_config,
                "metadata": ComponentMetadata(
                    source="neo4j.entity_completion_rates",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if entity_data else 0.0
                )
            }

        except Exception as e:
            handle_error(logger, e, "Neo4j entity completion analysis")
            return {}

    def get_workflow_business_analysis_neo4j(self) -> Dict[str, Any]:
        """Get workflow business analysis using Neo4j entity completion rates"""
        try:
            logger.info("Adapter: Getting Neo4j workflow business analysis")

            # Get workflow stages configuration
            workflow_config = get_workflow_stages_config()

            # Get Neo4j entity completion rates
            entity_completion_data = get_entity_completion_rates()

            # Get entity classification for display configuration
            entity_classification = get_entity_classification()
            entity_order = entity_classification.get("entity_order", [])

            # Structure workflow stages with Neo4j completion rates
            workflow_stages = []
            stage_number = 1

            for entity_name in entity_order:
                if entity_name in workflow_config.get("stages", {}):
                    stage_config = workflow_config["stages"][entity_name]

                    # Get Neo4j completion rate for this entity
                    completion_rate = 0.0
                    entity_count = 0
                    if entity_name in entity_completion_data:
                        entity_info = entity_completion_data[entity_name]
                        completion_rate = entity_info.get("completion_rate", 0.0)
                        entity_count = entity_info.get("total_count", 0)

                    workflow_stages.append({
                        "stage_number": stage_number,
                        "entity_name": entity_name,
                        "title": stage_config.get("title", entity_name),
                        "description": stage_config.get("description", ""),
                        "completion_rate": completion_rate,
                        "entity_count": entity_count,
                        "source_fields": stage_config.get("source_fields", []),
                        "display_title": stage_config.get("display_title", entity_name),
                        "color": stage_config.get("color", "#4A90E2"),
                        "card_min_height": stage_config.get("card_min_height", "300px"),
                        "header_bg_opacity": stage_config.get("header_bg_opacity", 0.3),
                        "show_description": stage_config.get("show_description", False)
                    })
                    stage_number += 1

            # Get display configuration
            display_config = workflow_config.get("display_config", {})

            return {
                "workflow_stages": workflow_stages,
                "display_config": display_config,
                "entity_completion_summary": entity_completion_data,
                "metadata": ComponentMetadata(
                    source="neo4j.workflow_business_analysis",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if workflow_stages else 0.0
                )
            }

        except Exception as e:
            handle_error(logger, e, "Neo4j workflow business analysis")
            return {}

    def get_facility_statistics_analysis(self, facility_id: str = None) -> Dict[str, Any]:
        """Get facility statistics analysis using Neo4j aggregation"""
        try:
            logger.info(f"Adapter: Getting Neo4j facility statistics for {facility_id or 'all facilities'}")

            # Get Neo4j facility statistics
            facilities_data = get_facility_action_statistics(facility_id)

            if not facilities_data:
                return {}

            if facility_id:
                # Single facility analysis
                return {
                    "facility": facilities_data,
                    "analysis_type": "single_facility",
                    "metadata": ComponentMetadata(
                        source="neo4j.facility_action_statistics",
                        generated_at=self._get_timestamp(),
                        data_quality=1.0
                    )
                }
            else:
                # All facilities analysis
                facilities_list = facilities_data.get("facilities", [])
                aggregate_data = facilities_data.get("aggregate", {})

                # Calculate performance distributions
                completion_rates = [f.get("completion_rate", 0) for f in facilities_list]
                effectiveness_rates = [f.get("effectiveness_rate", 0) for f in facilities_list]

                avg_completion = sum(completion_rates) / len(completion_rates) if completion_rates else 0
                avg_effectiveness = sum(effectiveness_rates) / len(effectiveness_rates) if effectiveness_rates else 0

                total_facilities = len(facilities_list)
                total_incidents = aggregate_data.get("total_action_requests", 0)

                return {
                    "facilities": facilities_list,
                    "performance_summary": {
                        "average_completion_rate": round(avg_completion, 1),
                        "average_effectiveness_rate": round(avg_effectiveness, 1),
                        "completion_rate_distribution": completion_rates,
                        "effectiveness_rate_distribution": effectiveness_rates
                    },
                    "aggregate_metrics": {
                        "total_facilities": total_facilities,
                        "total_incidents": total_incidents,
                        "average_completion_rate": avg_completion,
                        "average_effectiveness_rate": avg_effectiveness
                    },
                    "metadata": ComponentMetadata(
                        source="neo4j.facility_action_statistics",
                        generated_at=self._get_timestamp(),
                        data_quality=1.0 if facilities_data else 0.0
                    )
                }

        except Exception as e:
            handle_error(logger, e, "Neo4j facility statistics analysis")
            return {}

    # DEPRECATED METHODS - TO BE REMOVED AFTER MIGRATION
    def get_workflow_business_analysis(self) -> Dict[str, Any]:
        """DEPRECATED: Use get_workflow_business_analysis_neo4j() instead"""
        logger.warning("Using deprecated Python-based workflow analysis. Migrating to Neo4j...")
        return self.get_workflow_business_analysis_neo4j()

    def _calculate_entity_completion_rate(self, entity_name: str, source_fields: List[str]) -> float:
        """DEPRECATED: Neo4j entity completion rates used instead"""
        logger.warning("Using deprecated Python completion rate calculation. Use Neo4j entity completion rates instead.")
        try:
            # Get action requests for completion rate calculation (reused calculation logic)
            action_requests = get_action_requests(limit=10000)

            if not source_fields or not action_requests:
                return 0.0

            # Count records with at least one value in fields
            records_with_data = 0
            for request in action_requests:
                has_data = False
                for field in source_fields:
                    if field in request and request[field]:
                        has_data = True
                        break
                if has_data:
                    records_with_data += 1

            # Calculate completion rate
            return round((records_with_data / len(action_requests) * 100), 1) if action_requests else 0

        except Exception as e:
            handle_error(logger, e, "entity completion rate calculation")
            return 0.0
