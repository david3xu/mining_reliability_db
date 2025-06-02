#!/usr/bin/env python3
"""
Core Database Query Manager - Centralized Database Operations
Single authority for all Neo4j database interactions with schema-driven design.
"""

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from configs.environment import get_entity_primary_key, get_schema
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

    def get_entity_count(self, entity_type: str, filters: Dict[str, Any] = None) -> int:
        """Get count of entities with optional filtering"""
        try:
            filter_clause = self._build_filter_clause(filters) if filters else ""
            query = f"MATCH (n:{entity_type}) {filter_clause} RETURN count(n) AS count"

            result = self.execute_query(query, filters or {})
            return result.data[0]["count"] if result.success and result.data else 0

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
            {facility_filter}
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
        """Get completion rates for workflow entities"""
        try:
            query = """
            MATCH (ar:ActionRequest)
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

            return self.execute_query(query)

        except Exception as e:
            handle_error(logger, e, "workflow completion rates")
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
                 rc.root_cause_tail AS secondary_cause,
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
            MATCH (n:{entity_type})
            WHERE n.{date_field} IS NOT NULL
            WITH substring(n.{date_field}, 0, 4) AS year, count(n) AS count
            WHERE year IS NOT NULL
            RETURN year, count
            ORDER BY year
            """

            return self.execute_query(query)

        except Exception as e:
            handle_error(logger, e, f"temporal analysis for {entity_type}")
            return QueryResult(data=[], count=0, success=False, metadata={"error": str(e)})

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
            if isinstance(value, str):
                conditions.append(f"n.{key} = ${key}")
            elif isinstance(value, list):
                conditions.append(f"n.{key} IN ${key}")
            else:
                conditions.append(f"n.{key} = ${key}")

        return f"WHERE {' AND '.join(conditions)}" if conditions else ""


# Singleton pattern
_query_manager = None


def get_query_manager() -> QueryManager:
    """Get singleton query manager instance"""
    global _query_manager
    if _query_manager is None:
        _query_manager = QueryManager()
    return _query_manager
