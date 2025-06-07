#!/usr/bin/env python3
"""
Core Business Intelligence Engine - Coordination Layer
Delegates to specialized intelligence engines for focused analysis.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from configs.environment import (
    get_entity_connections,
    get_entity_names,
    get_entity_primary_key,
)
from mine_core.business.intelligence_models import IntelligenceResult
from mine_core.business.portfolio_intelligence import PortfolioIntelligence
from mine_core.business.quality_intelligence import QualityIntelligence
from mine_core.business.search_intelligence import SearchIntelligence
from mine_core.database.query_manager import QueryResult, get_query_manager
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


class IntelligenceEngine:
    """Core intelligence coordination - delegates to specialized engines"""

    def __init__(self):
        self.query_manager = get_query_manager()

        # Specialized intelligence engines
        self.portfolio_intelligence = PortfolioIntelligence()
        self.search_intelligence = SearchIntelligence()
        self.quality_intelligence = QualityIntelligence()

    # Portfolio Analysis Delegation
    def analyze_portfolio_metrics(self) -> IntelligenceResult:
        """Delegate to portfolio intelligence engine"""
        return self.portfolio_intelligence.analyze_metrics()

    def analyze_facility_distribution(self) -> IntelligenceResult:
        """Delegate to portfolio intelligence engine"""
        return self.portfolio_intelligence.analyze_facility_distribution()

    def analyze_field_type_distribution(self) -> IntelligenceResult:
        """Delegate to portfolio intelligence engine"""
        return self.portfolio_intelligence.analyze_field_type_distribution()

    def analyze_temporal_timeline(self) -> IntelligenceResult:
        """Delegate to portfolio intelligence engine"""
        return self.portfolio_intelligence.analyze_temporal_timeline()

    # Search Intelligence Delegation
    def execute_comprehensive_incident_search(self, search_terms: str) -> IntelligenceResult:
        """Delegate to search intelligence engine"""
        return self.search_intelligence.execute_comprehensive_search(search_terms)

    def analyze_incident_intelligence(self, search_terms: str) -> IntelligenceResult:
        """Delegate to search intelligence engine for stakeholder intelligence"""
        return self.search_intelligence.analyze_incident_intelligence(search_terms)

    # Quality Analysis Delegation
    def analyze_data_quality(self) -> IntelligenceResult:
        """Delegate to quality intelligence engine"""
        return self.quality_intelligence.analyze_data_quality()

    def analyze_facility_completeness(self, facility_id: str = None) -> IntelligenceResult:
        """Delegate to quality intelligence engine"""
        return self.quality_intelligence.analyze_facility_completeness(facility_id)

    def get_missing_data_impact(self) -> IntelligenceResult:
        """Delegate to quality intelligence engine"""
        return self.quality_intelligence.get_missing_data_impact()

    def analyze_action_request_facility_statistics(self) -> IntelligenceResult:
        """Delegate to quality intelligence engine"""
        return self.quality_intelligence.analyze_action_request_facility_statistics()

    # Direct Query Execution (Core Functionality)
    def execute_cypher_query(
        self, query_template: str, parameters: Dict[str, Any] = None
    ) -> IntelligenceResult:
        """Execute schema-driven cypher query with template substitution"""
        try:
            logger.info("Intelligence Engine: Executing cypher query template")

            # Get schema information for template substitution
            entity_names = get_entity_names()
            entity_connections = get_entity_connections()

            # Template substitution - replace schema placeholders
            formatted_query = query_template

            # Replace entity names
            for entity_type, entity_name in entity_names.items():
                formatted_query = formatted_query.replace(
                    f"{{{entity_type.lower()}_entity}}", entity_name
                )

            # Replace relationship connections
            for connection_key, connection_name in entity_connections.items():
                formatted_query = formatted_query.replace(
                    f"{{{connection_key.lower()}}}", connection_name
                )

            # Replace field mappings (basic primary keys)
            for entity_type in entity_names.keys():
                primary_key = get_entity_primary_key(entity_type)
                if primary_key:
                    formatted_query = formatted_query.replace(
                        f"{{{entity_type.lower()}_primary_key}}", primary_key
                    )

            # Execute the formatted query
            result = self.query_manager.execute_query(formatted_query, **(parameters or {}))

            if not result.success:
                return IntelligenceResult(
                    analysis_type="cypher_query_execution",
                    data=[],
                    metadata={
                        "error": "Query execution failed",
                        "template_used": query_template[:100],
                    },
                    quality_score=0.0,
                    generated_at=datetime.now().isoformat(),
                )

            return IntelligenceResult(
                analysis_type="cypher_query_execution",
                data=result.data,
                metadata={
                    "query_executed": formatted_query[:200] + "...",
                    "parameters_used": list((parameters or {}).keys()),
                    "records_returned": len(result.data) if result.data else 0,
                },
                quality_score=1.0 if result.data else 0.5,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, f"cypher query execution: {query_template[:50]}...")
            return IntelligenceResult(
                analysis_type="cypher_query_execution",
                data=[],
                metadata={"error": str(e), "template_used": query_template[:100]},
                quality_score=0.0,
                generated_at=datetime.now().isoformat(),
            )

    def execute_raw_cypher_query(self, query: str) -> Optional[list]:
        """Execute raw Cypher query with safety checks"""
        try:
            logger.info("Intelligence Engine: Executing raw Cypher query")
            results = self.query_manager.execute_query(query)

            if results is not None:
                logger.info(f"Raw query returned {len(results) if hasattr(results, '__len__') else 'unknown'} results")
                return results
            else:
                logger.warning("Raw query returned no results")
                return []

        except Exception as e:
            handle_error(logger, e, "raw cypher query execution")
            return None

    # Legacy compatibility methods
    def analyze_causal_intelligence(self, facility_id: str = None) -> IntelligenceResult:
        """Legacy causal analysis - delegate to search intelligence"""
        return self.search_intelligence.analyze_causal_intelligence(facility_id)


# Singleton pattern
_intelligence_engine = None


def get_intelligence_engine() -> IntelligenceEngine:
    """Get singleton intelligence engine instance"""
    global _intelligence_engine
    if _intelligence_engine is None:
        _intelligence_engine = IntelligenceEngine()
    return _intelligence_engine
