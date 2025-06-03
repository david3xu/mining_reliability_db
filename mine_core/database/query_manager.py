#!/usr/bin/env python3
"""
Core Database Query Manager - Centralized Database Operations
Single authority for all Neo4j database interactions with schema-driven design.
"""

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from configs.environment import get_entity_primary_key, get_schema, get_mappings, get_entity_connections
from mine_core.database.db import get_database
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


@dataclass
class QueryResult:
    """Standardized query result container"""

    data: List[Dict[str, Any]]
    count: int
    success: bool
    metadata: Dict[str, Any]


class QueryManager:
    """Centralized database query management with schema integration"""

    def __init__(self):
        self.db = get_database()
        self.schema = get_schema()
        self._entity_cache = {}

    def execute_query(self, query: str, params: Dict[str, Any] = None) -> QueryResult:
        """Execute raw query with standardized result handling"""
        try:
            results = self.db.execute_query(query, **(params or {}))
            return QueryResult(
                data=results,
                count=len(results),
                success=True,
                metadata={"query_type": "raw", "params": params},
            )
        except Exception as e:
            handle_error(logger, e, "query execution")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_entity_count(self, entity_type: str) -> int:
        """Return integer count, not QueryResult object"""
        try:
            filter_clause = "WHERE NOT '_SchemaTemplate' IN labels(n)"
            query = f"MATCH (n:{entity_type}) {filter_clause} RETURN count(n) AS count"

            result = self.execute_query(query)
            if result.success and result.data:
                return result.data[0]["count"]  # Extract integer from QueryResult
            return 0
        except Exception as e:
            handle_error(logger, e, f"entity count for {entity_type}")
            return 0

    def get_entities_by_type(
        self, entity_type: str, limit: int = 1000, filters: Dict[str, Any] = None
    ) -> QueryResult:
        """Get entities by type with schema-driven property selection"""
        try:
            # Get properties from schema
            entity_def = self._get_entity_definition(entity_type)
            if not entity_def:
                return QueryResult(
                    data=[],
                    count=0,
                    success=False,
                    metadata={"error": f"Unknown entity type: {entity_type}"},
                )

            properties = list(entity_def.get("properties", {}).keys())
            property_list = ", ".join([f"n.{prop} AS {prop}" for prop in properties])

            filter_clause = self._build_filter_clause(filters) if filters else ""
            query = f"""
            MATCH (n:{entity_type})
            {filter_clause}
            RETURN {property_list}
            LIMIT $limit
            """

            params = {"limit": limit}
            if filters:
                params.update(filters)

            return self.execute_query(query, params)

        except Exception as e:
            handle_error(logger, e, f"entities retrieval for {entity_type}")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_relationship_data(
        self, from_type: str, rel_type: str, to_type: str, limit: int = 1000
    ) -> QueryResult:
        """Get relationship data between entity types"""
        try:
            from_pk = get_entity_primary_key(from_type)
            to_pk = get_entity_primary_key(to_type)

            if not from_pk or not to_pk:
                return QueryResult(
                    data=[], count=0, success=False, metadata={"error": "Missing primary keys"}
                )

            query = f"""
            MATCH (from:{from_type})-[r:{rel_type}]->(to:{to_type})
            RETURN from.{from_pk} AS from_id, to.{to_pk} AS to_id,
                   properties(r) AS relationship_props
            LIMIT $limit
            """

            return self.execute_query(query, {"limit": limit})

        except Exception as e:
            handle_error(logger, e, f"relationship data {from_type}-{rel_type}-{to_type}")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_facility_metrics(self, facility_id: str = None) -> QueryResult:
        """Get facility-specific metrics with optional facility filtering"""
        try:
            facility_filter = "WHERE f.facility_id = $facility_id" if facility_id else ""
            params = {"facility_id": facility_id} if facility_id else {}

            query = f"""
            MATCH (f:Facility)
            WHERE NOT '_SchemaTemplate' IN labels(f) {facility_filter}
            OPTIONAL MATCH (f)<-[:BELONGS_TO]-(ar:ActionRequest)
            WITH f, count(ar) AS incident_count
            RETURN f.facility_id AS facility_id,
                   f.facility_name AS facility_name,
                   f.active AS active,
                   incident_count
            ORDER BY f.facility_name
            """

            return self.execute_query(query, params)

        except Exception as e:
            handle_error(logger, e, "facility metrics retrieval")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_workflow_completion_rates(self) -> QueryResult:
        """Enhanced workflow completion rates with proper validation"""
        try:
            query = """
            MATCH (ar:ActionRequest)
            WHERE NOT '_SchemaTemplate' IN labels(ar)
            OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
            OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
            OPTIONAL MATCH (rc)<-[:RESOLVES]-(ap:ActionPlan)
            OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)

            RETURN count(ar) AS total_requests,
                   count(p) AS problems_defined,
                   count(rc) AS causes_analyzed,
                   count(ap) AS plans_developed,
                   count(v) AS plans_verified
            """

            result = self.execute_query(query)
            if result.success and result.data:
                logger.info(f"Workflow completion query successful: {result.data[0]}")
                return result
            else:
                logger.warning("Workflow completion query returned no data")
                return QueryResult(
                    data=[
                        {
                            "total_requests": 0,
                            "problems_defined": 0,
                            "causes_analyzed": 0,
                            "plans_developed": 0,
                            "plans_verified": 0,
                        }
                    ],
                    count=1,
                    success=True,
                    metadata={"fallback": True},
                )

        except Exception as e:
            handle_error(logger, e, "workflow completion rates query")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_causal_intelligence_data(self, facility_id: str = None) -> QueryResult:
        """Get causal intelligence patterns"""
        try:
            facility_filter = "WHERE f.facility_id = $facility_id" if facility_id else ""
            params = {"facility_id": facility_id} if facility_id else {}

            query = f"""
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            {facility_filter}
            MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
            WHERE rc.root_cause IS NOT NULL AND rc.root_cause <> 'DATA_NOT_AVAILABLE'
            WITH rc.root_cause AS primary_cause,
                 rc.root_cause_tail_extraction AS secondary_cause,
                 ar.categories AS category,
                 count(*) AS frequency
            RETURN primary_cause, secondary_cause, category, frequency
            ORDER BY frequency DESC
            LIMIT 20
            """

            return self.execute_query(query, params)

        except Exception as e:
            handle_error(logger, e, "causal intelligence data")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_temporal_analysis_data(self, entity_type: str = "ActionRequest") -> QueryResult:
        """Get temporal analysis data for entities"""
        try:
            # Get date field from schema
            entity_def = self._get_entity_definition(entity_type)
            date_fields = [
                prop
                for prop, config in entity_def.get("properties", {}).items()
                if config.get("type") == "date"
            ]

            if not date_fields:
                return QueryResult(
                    data=[], count=0, success=False, metadata={"error": "No date fields found"}
                )

            date_field = date_fields[0]  # Use first date field

            query = f"""
            MATCH (n:{entity_type})-[:BELONGS_TO]->(f:Facility)
            WHERE n.{date_field} IS NOT NULL AND f.facility_id IS NOT NULL AND NOT '_SchemaTemplate' IN labels(n)
            WITH f.facility_id AS facility_id,
                 CASE
                     WHEN n.{date_field} =~ '^\\d{{4}}-\\d{{2}}-\\d{{2}}.*' THEN substring(n.{date_field}, 0, 4)
                     WHEN n.{date_field} =~ '^\\d{{4}}' THEN substring(n.{date_field}, 0, 4)
                     ELSE NULL
                 END AS year,
                 count(n) AS incident_count
            WHERE year IS NOT NULL AND year =~ '^\\d{{4}}$'
            RETURN facility_id, year, incident_count
            ORDER BY year, facility_id
            """

            return self.execute_query(query)

        except Exception as e:
            handle_error(logger, e, f"temporal analysis for {entity_type}")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def discover_search_data_structure(self) -> QueryResult:
        """Discover actual database structure for search functionality"""
        try:
            structure_query = """
            // Check what relationships actually exist between Problem and RootCause
            MATCH (p:Problem)-[r]-(rc:RootCause)
            WITH type(r) AS relationship_type, count(*) AS count
            RETURN "relationships" AS discovery_type,
                   collect({type: relationship_type, count: count}) AS findings

            UNION ALL

            // Check actual properties on RootCause nodes
            MATCH (rc:RootCause)
            WITH keys(rc) AS rc_properties LIMIT 1
            RETURN "rootcause_properties" AS discovery_type, rc_properties AS findings

            UNION ALL

            // Check actual properties on Problem nodes
            MATCH (p:Problem)
            WITH keys(p) AS p_properties LIMIT 1
            RETURN "problem_properties" AS discovery_type, p_properties AS findings

            UNION ALL

            // Sample actual data to verify content
            MATCH (p:Problem)-[r]-(rc:RootCause)
            RETURN "sample_data" AS discovery_type,
                   {problem_props: properties(p),
                    relationship: type(r),
                    rootcause_props: properties(rc)} AS findings
            LIMIT 3
            """

            return self.execute_query(structure_query)

        except Exception as e:
            handle_error(logger, e, "search data structure discovery")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def get_core_workflow_labels(self) -> QueryResult:
        """Get only the 5 core workflow node labels"""
        try:
            core_labels_query = """
            CALL db.labels() YIELD label
            WHERE label IN ['ActionRequest', 'Problem', 'RootCause', 'ActionPlan', 'Verification', 'Facility']
            RETURN label
            ORDER BY
                CASE label
                    WHEN 'ActionRequest' THEN 1
                    WHEN 'Problem' THEN 2
                    WHEN 'RootCause' THEN 3
                    WHEN 'ActionPlan' THEN 4
                    WHEN 'Verification' THEN 5
                    WHEN 'Facility' THEN 6
                END
            """

            return self.execute_query(core_labels_query)

        except Exception as e:
            handle_error(logger, e, "core workflow labels discovery")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def search_incident_patterns(self, search_text: str) -> QueryResult:
        """Fixed search with correct relationship pattern"""
        try:
            # Test multiple relationship patterns
            corrected_query = """
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
            OPTIONAL MATCH (p)-[r]-(rc:RootCause)
            WHERE toLower(toString(p.name)) CONTAINS toLower($search_text)
               OR toLower(toString(ar.name)) CONTAINS toLower($search_text)

            RETURN ar.action_request_number AS request_number,
                   ar.name AS title,
                   ar.initiation_date AS initiation_date,
                   p.name AS problem_description,
                   coalesce(rc.name, 'No root cause analysis') AS root_cause,
                   f.facility_id AS facility_id,
                   coalesce(ar.stage, 'Unknown') AS status
            ORDER BY ar.initiation_date DESC
            LIMIT 20
            """

            # Correct parameter syntax
            return self.execute_query(corrected_query, {"search_text": search_text})

        except Exception as e:
            handle_error(logger, e, f"search execution for '{search_text}'")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def search_using_schema_configuration(self, search_text: str) -> QueryResult:
        """Schema-driven search using field_mappings.json"""
        try:
            # Get actual field mappings
            # NOTE: We need the schema to get the *internal* Neo4j property names, not just display names
            schema_config = get_schema()
            connections_config = get_entity_connections()

            # Extract search properties using their actual internal Neo4j names
            problem_search_field = "what_happened"
            ar_search_field = "title"
            rc_result_field = "root_cause"

            # Get relationship types from schema
            problem_to_ar = self._get_relationship_type(connections_config, "Problem", "ActionRequest", "IDENTIFIED_IN")
            rc_to_problem = self._get_relationship_type(connections_config, "RootCause", "Problem", "ANALYZES")

            # Build schema-driven query using internal property names (no backticks needed)
            schema_query = f"""
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            MATCH (p:Problem)-[:{problem_to_ar}]->(ar)
            MATCH (rc:RootCause)-[r]-(p:Problem)
            WHERE toLower(toString(p.{problem_search_field})) CONTAINS toLower($search_text)
               OR toLower(toString(ar.{ar_search_field})) CONTAINS toLower($search_text)

            RETURN ar.action_request_number AS request_number,
                   ar.{ar_search_field} AS title,
                   ar.initiation_date AS initiation_date,
                   p.problem_id AS problem_id,
                   p.{problem_search_field} AS problem_description,
                   coalesce(rc.root_cause, 'No analysis') AS root_cause,
                   f.facility_id AS facility_id,
                   coalesce(ar.stage, 'Unknown') AS status
            ORDER BY ar.initiation_date DESC
            LIMIT 20
            """

            query_result = self.execute_query(query=schema_query, params={"search_text": search_text})
            logger.info(f"Raw schema search results: {query_result.data}")
            return query_result

        except Exception as e:
            handle_error(logger, e, f"schema-driven search for '{search_text}'")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

    def _get_relationship_type(self, connections_config: Dict[str, Any], from_entity: str, to_entity: str, default_relation: str) -> str:
        """Helper to get relationship type from connections_config"""
        for conn in connections_config.get("workflow_connections", {}).get("primary_workflow_flow", []):
            if conn.get("from") == from_entity and conn.get("to") == to_entity:
                return conn.get("relationship", default_relation)
        return default_relation

    def _get_entity_definition(self, entity_type: str) -> Dict[str, Any]:
        """Get entity definition from schema with caching"""
        if entity_type not in self._entity_cache:
            entities = self.schema.get("entities", [])
            entity_def = next((e for e in entities if e["name"] == entity_type), {})
            self._entity_cache[entity_type] = entity_def

        return self._entity_cache[entity_type]

    def _build_filter_clause(self, filters: Dict[str, Any]) -> str:
        """Build WHERE clause from filters"""
        if not filters:
            return ""

        conditions = []
        for key, value in filters.items():
            if value == "__IS_NOT_NULL__":
                conditions.append(f"n.{key} IS NOT NULL")
            elif isinstance(value, str):
                conditions.append(f"n.{key} = ${key}")
            elif isinstance(value, list):
                conditions.append(f"n.{key} IN ${key}")
            else:
                conditions.append(f"n.{key} = ${key}")

        return f"WHERE {' AND '.join(conditions)}" if conditions else ""

    def test_workflow_entities(self):
        """Tests the existence and count of core workflow entities in Neo4j."""
        entities = ["ActionRequest", "Problem", "RootCause", "ActionPlan", "Verification"]
        logger.info("--- Testing Workflow Entities --- ")
        for entity in entities:
            count = self.get_entity_count(entity)
            logger.info(f"{entity}: {count} records")
        logger.info("--- Workflow Entity Test Complete ---")


# Singleton pattern
_query_manager = None


def get_query_manager() -> QueryManager:
    """Get singleton query manager instance"""
    global _query_manager
    if _query_manager is None:
        _query_manager = QueryManager()
    return _query_manager
