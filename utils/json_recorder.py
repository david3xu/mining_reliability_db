"""
JSON Recording Utility for Mining Reliability Dashboard
Handles saving search results to JSON files with timestamps and metadata.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class JSONRecorder:
    """Handles recording search results to JSON files"""

    def __init__(self, base_directory: str = None):
        """
        Initialize the JSON recorder

        Args:
            base_directory: Base directory for saving JSON files.
                          Defaults to project data/search_results directory.
        """
        if base_directory is None:
            # Default to project's search_results directory
            self.base_directory = Path(__file__).parent.parent / "data" / "search_results"
        else:
            self.base_directory = Path(base_directory)

        # Ensure directory exists
        self.base_directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"JSON Recorder initialized with directory: {self.base_directory}")

    def save_search_results(self,
                          search_term: str,
                          search_data: Dict[str, Any],
                          metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save search results to a JSON file with timestamp and metadata

        Args:
            search_term: The search term used
            search_data: The search results data from the intelligence engine
            metadata: Additional metadata to include

        Returns:
            str: Path to the saved JSON file
        """
        try:
            # Generate timestamp-based filename
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            # Clean search term for filename (replace spaces and special chars)
            clean_search_term = "".join(c for c in search_term if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_search_term = clean_search_term.replace(' ', '_')[:50]  # Limit length

            filename = f"search_{timestamp_str}_{clean_search_term}.json"
            filepath = self.base_directory / filename

            # Prepare complete JSON structure
            json_data = {
                "search_metadata": {
                    "search_term": search_term,
                    "timestamp": timestamp.isoformat(),
                    "timestamp_formatted": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "search_coverage": search_data.get("search_coverage", 0),
                    "total_dimensions": len([k for k in search_data.keys() if k != "search_coverage"]),
                },
                "search_results": search_data,
                "statistics": self._calculate_search_statistics(search_data),
            }

            # Add any additional metadata
            if metadata:
                json_data["search_metadata"].update(metadata)

            # Save to JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)

            logger.info(f"Search results saved to: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to save search results to JSON: {str(e)}")
            raise

    def _calculate_search_statistics(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate statistics about the search results

        Args:
            search_data: The search results data

        Returns:
            Dict containing various statistics
        """
        stats = {
            "total_results": 0,
            "dimensions_with_results": 0,
            "dimension_breakdown": {}
        }

        # Count results by dimension
        for key, value in search_data.items():
            if key == "search_coverage":
                continue

            if isinstance(value, list):
                result_count = len(value)
                stats["dimension_breakdown"][key] = result_count
                stats["total_results"] += result_count

                if result_count > 0:
                    stats["dimensions_with_results"] += 1

        return stats

    def load_search_results(self, filepath: str) -> Dict[str, Any]:
        """
        Load search results from a JSON file

        Args:
            filepath: Path to the JSON file

        Returns:
            Dict containing the loaded search data
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load search results from {filepath}: {str(e)}")
            raise

    def list_saved_searches(self, limit: Optional[int] = None) -> list:
        """
        List all saved search files, sorted by creation time (newest first)

        Args:
            limit: Maximum number of files to return

        Returns:
            List of file paths
        """
        try:
            json_files = list(self.base_directory.glob("search_*.json"))
            # Sort by modification time, newest first
            json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            if limit:
                json_files = json_files[:limit]

            return [str(f) for f in json_files]
        except Exception as e:
            logger.error(f"Failed to list saved searches: {str(e)}")
            return []

    def get_search_summary(self, filepath: str) -> Dict[str, Any]:
        """
        Get a summary of a saved search without loading full data

        Args:
            filepath: Path to the JSON file

        Returns:
            Dict containing search summary information
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "filepath": filepath,
                "search_term": data.get("search_metadata", {}).get("search_term", "Unknown"),
                "timestamp": data.get("search_metadata", {}).get("timestamp_formatted", "Unknown"),
                "total_results": data.get("statistics", {}).get("total_results", 0),
                "dimensions_with_results": data.get("statistics", {}).get("dimensions_with_results", 0),
                "search_coverage": data.get("search_metadata", {}).get("search_coverage", 0)
            }
        except Exception as e:
            logger.error(f"Failed to get search summary from {filepath}: {str(e)}")
            return {"filepath": filepath, "error": str(e)}
