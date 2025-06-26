#!/usr/bin/env python3
"""
Data Adapter - Minimal Search-Only Version
Provides only the search-related data access for the search-algorithms-only branch.
"""

from mine_core.database.query_manager import get_query_manager

class DataAdapter:
    """Minimal data adapter for executing Cypher queries via the query manager."""
    def __init__(self):
        self.query_manager = get_query_manager()

    def execute_cypher_query(self, query, parameters=None):
        """Execute a Cypher query using the core query manager."""
        try:
            return self.query_manager.execute_cypher_query(query, parameters=parameters)
        except Exception as e:
            # Optionally log or handle error here
            return None

    def execute_comprehensive_graph_search(self, search_params):
        """Execute comprehensive graph search combining all search query types and templates."""
        try:
            # Handle both string and dict search parameters
            if isinstance(search_params, str):
                search_term = search_params
            elif isinstance(search_params, dict):
                search_term = search_params.get("search_term", "")
            else:
                search_term = str(search_params)

            if not search_term:
                return {"nodes": [], "relationships": [], "summary": "No search term provided"}

            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Starting comprehensive search for: '{search_term}'")

            all_results = []
            category_results = {}

            # Phase 1: Execute pre-built query templates first (highest priority)
            template_results = self._execute_query_templates(search_term)
            if template_results:
                all_results.extend(template_results)
                category_results["Query Templates"] = len(template_results)
                logger.info(f"Query templates returned {len(template_results)} results")

            # Phase 2: Execute graph configuration queries
            from dashboard.adapters import get_config_adapter
            config = get_config_adapter()
            graph_config = config.get_graph_search_config()

            # Execute all configured search query categories
            search_categories = [
                ("direct_field_matches", "Direct field matches"),
                ("equipment_patterns", "Equipment patterns"),
                ("causal_chains", "Causal analysis"),
                ("cross_facility_patterns", "Cross-facility insights"),
                ("temporal_patterns", "Timeline analysis"),
                ("recurring_sequences", "Recurring patterns"),
                ("solution_effectiveness", "Proven solutions")
            ]

            for category_key, category_name in search_categories:
                if category_key in graph_config.get("search_queries", {}):
                    category_config = graph_config["search_queries"][category_key]
                    category_count = 0

                    # Execute all queries in this category
                    for query_key, query in category_config.items():
                        if query_key != "description" and isinstance(query, str):
                            try:
                                results = self.query_manager.execute_cypher_query(
                                    query,
                                    parameters={"search_term": search_term}
                                )

                                if results and results.get("success", False):
                                    data = results.get("data", [])
                                    for record in data:
                                        record["search_category"] = category_key
                                        record["search_subcategory"] = query_key
                                        record["category_description"] = category_name

                                    all_results.extend(data)
                                    category_count += len(data)

                            except Exception as e:
                                logger.warning(f"Failed to execute {category_key}.{query_key}: {e}")
                                continue

                    if category_count > 0:
                        category_results[category_name] = category_count

            # Phase 3: Execute comprehensive single queries
            comprehensive_queries = [
                ("comprehensive_incident_search", "Incident search"),
                ("equipment_facility_network", "Equipment network"),
                ("solution_effectiveness_graph", "Solution effectiveness")
            ]

            for query_key, query_name in comprehensive_queries:
                if query_key in graph_config.get("search_queries", {}):
                    try:
                        query = graph_config["search_queries"][query_key]
                        results = self.query_manager.execute_cypher_query(
                            query,
                            parameters={"search_term": search_term}
                        )

                        if results and results.get("success", False):
                            data = results.get("data", [])
                            for record in data:
                                record["search_category"] = query_key
                                record["category_description"] = query_name

                            all_results.extend(data)
                            if data:
                                category_results[query_name] = len(data)

                    except Exception as e:
                        logger.warning(f"Failed to execute {query_key}: {e}")
                        continue

            # Process results
            if all_results:
                # Remove duplicates and limit results
                unique_results = []
                seen_incidents = set()

                for result in all_results:
                    # Try to extract incident identifier for deduplication
                    incident_id = None
                    if isinstance(result, dict):
                        if "ar" in result and isinstance(result["ar"], dict):
                            incident_id = result["ar"].get("properties", {}).get("action_request_number")
                        elif "action_request_number" in result:
                            incident_id = result["action_request_number"]

                    if incident_id and incident_id not in seen_incidents:
                        seen_incidents.add(incident_id)
                        unique_results.append(result)
                    elif not incident_id:
                        unique_results.append(result)

                # Limit to top 100 results for performance
                limited_results = unique_results[:100]

                # Create comprehensive summary
                summary_parts = [
                    f"Found {len(all_results)} results ({len(limited_results)} unique) for '{search_term}'"
                ]

                if category_results:
                    category_summary = ", ".join([f"{name}: {count}" for name, count in category_results.items()])
                    summary_parts.append(f"Categories: {category_summary}")

                return {
                    "nodes": limited_results,
                    "relationships": [],
                    "summary": " | ".join(summary_parts),
                    "search_metadata": {
                        "total_results": len(all_results),
                        "unique_results": len(unique_results),
                        "displayed_results": len(limited_results),
                        "categories": category_results,
                        "search_term": search_term
                    }
                }
            else:
                return {
                    "nodes": [],
                    "relationships": [],
                    "summary": f"No results found for '{search_term}' across all search categories",
                    "search_metadata": {
                        "total_results": 0,
                        "search_term": search_term,
                        "categories_attempted": len(search_categories) + len(comprehensive_queries)
                    }
                }

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in comprehensive graph search: {e}")
            return {
                "nodes": [],
                "relationships": [],
                "summary": f"Search error: {str(e)}",
                "search_metadata": {"error": str(e)}
            }

    def _execute_query_templates(self, search_term):
        """Execute pre-built query templates from configs/queries/ directory."""
        import os
        import logging
        logger = logging.getLogger(__name__)

        queries_dir = "/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries"
        all_results = []

        # Define filter clause for search term
        filter_clause = f"""toLower(p.what_happened) CONTAINS toLower('{search_term}')
           OR toLower(ar.categories) CONTAINS toLower('{search_term}')
           OR toLower(rc.root_cause) CONTAINS toLower('{search_term}')
           OR toLower(ap.action_plan) CONTAINS toLower('{search_term}') """

        # Get all available query templates
        try:
            template_files = [f for f in os.listdir(queries_dir) if f.endswith('.cypher')]

            # Priority templates executed first for better results ordering
            priority_templates = [
                "why_did_this_happen.cypher",
                "proven_solutions.cypher",
                "potential_root_causes.cypher",
                "effective_actions.cypher",
                "who_can_help_me.cypher"
            ]

            # Execute priority templates first
            executed_templates = set()
            for template_file in priority_templates:
                if template_file in template_files:
                    results = self._execute_single_template(template_file, queries_dir, filter_clause)
                    if results:
                        all_results.extend(results)
                        executed_templates.add(template_file)
                        logger.info(f"Priority template {template_file} returned {len(results)} results")

            # Then execute remaining templates
            remaining_templates = [t for t in template_files if t not in executed_templates]
            for template_file in remaining_templates:
                results = self._execute_single_template(template_file, queries_dir, filter_clause)
                if results:
                    all_results.extend(results)
                    logger.info(f"Template {template_file} returned {len(results)} results")

        except Exception as e:
            logger.error(f"Error accessing query templates directory: {e}")

        return all_results

    def _execute_single_template(self, template_file, queries_dir, filter_clause):
        """Execute a single query template file."""
        import os
        import logging
        logger = logging.getLogger(__name__)

        query_file = os.path.join(queries_dir, template_file)
        results = []

        try:
            with open(query_file, 'r') as f:
                query_template = f.read()

            # Replace the filter clause placeholder
            query = query_template.replace("{filter_clause}", filter_clause)

            # Execute the query
            query_results = self.query_manager.execute_cypher_query(query)

            if query_results and query_results.get("success", False):
                data = query_results.get("data", [])
                for record in data:
                    record["query_template"] = template_file
                    record["search_category"] = "template_query"
                    record["template_name"] = template_file.replace('.cypher', '').replace('_', ' ').title()

                results = data

        except Exception as e:
            logger.warning(f"Failed to execute template {template_file}: {e}")

        return results

    def execute_organized_comprehensive_search(self, search_params):
        """Execute comprehensive search and return results organized by search category."""
        # Get the comprehensive results first
        comprehensive_results = self.execute_comprehensive_graph_search(search_params)

        if not comprehensive_results.get("nodes"):
            return comprehensive_results

        # Organize results by category
        organized_results = {
            "template_queries": [],
            "direct_matches": [],
            "equipment_patterns": [],
            "causal_analysis": [],
            "cross_facility": [],
            "temporal_patterns": [],
            "recurring_patterns": [],
            "proven_solutions": [],
            "other": []
        }

        category_mapping = {
            "template_query": "template_queries",
            "direct_field_matches": "direct_matches",
            "equipment_patterns": "equipment_patterns",
            "causal_chains": "causal_analysis",
            "cross_facility_patterns": "cross_facility",
            "temporal_patterns": "temporal_patterns",
            "recurring_sequences": "recurring_patterns",
            "solution_effectiveness": "proven_solutions"
        }

        # Categorize results
        for result in comprehensive_results["nodes"]:
            category = result.get("search_category", "other")
            target_category = category_mapping.get(category, "other")
            organized_results[target_category].append(result)

        # Add metadata
        organized_results["metadata"] = comprehensive_results.get("search_metadata", {})
        organized_results["summary"] = comprehensive_results.get("summary", "")

        return organized_results

# Singleton instance
_data_adapter = None

def get_data_adapter():
    """Get singleton data adapter instance."""
    global _data_adapter
    if _data_adapter is None:
        _data_adapter = DataAdapter()
    return _data_adapter
