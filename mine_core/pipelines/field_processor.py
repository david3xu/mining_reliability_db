#!/usr/bin/env python3
"""
Complex Field Processing Engine for Mining Reliability Database
Handles advanced field transformation patterns and context preservation.
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from mine_core.shared.constants import (
    TEMPORAL_PATTERNS, MULTI_VALUE_PROCESSING, FIELD_NORMALIZATION,
    ANALYTICS_CATEGORIES, VALIDATION_RULES
)
from mine_core.shared.field_utils import (
    has_real_value, get_missing_indicator, clean_label, process_list_field
)

logger = logging.getLogger(__name__)

class FieldProcessor:
    """Advanced field processing for complex transformation patterns"""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize with processing configuration"""
        self.config = config or {}
        self.temporal_patterns = TEMPORAL_PATTERNS
        self.multi_value_config = MULTI_VALUE_PROCESSING
        self.normalization_rules = FIELD_NORMALIZATION

    def process_temporal_sequences(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect and process temporal field sequences"""
        temporal_entities = []
        temporal_fields = self._extract_temporal_fields(record)

        if len(temporal_fields) < 2:
            return temporal_entities

        # Sort by date value
        sorted_temporal = self._sort_temporal_fields(temporal_fields)

        # Create sequence entities
        for i, (field_name, date_value) in enumerate(sorted_temporal):
            entity = {
                "temporal_id": f"temporal_{i}_{clean_label(field_name)}",
                "field_name": field_name,
                "date_value": date_value,
                "sequence_position": i,
                "total_sequence_length": len(sorted_temporal)
            }
            temporal_entities.append(entity)

        return temporal_entities

    def _extract_temporal_fields(self, record: Dict[str, Any]) -> List[Tuple[str, str]]:
        """Extract temporal fields from record"""
        temporal_fields = []

        for field_name, value in record.items():
            if self._is_temporal_field(field_name, value):
                normalized_date = self._normalize_date_value(value)
                if normalized_date:
                    temporal_fields.append((field_name, normalized_date))

        return temporal_fields

    def _is_temporal_field(self, field_name: str, value: Any) -> bool:
        """Check if field represents temporal data"""
        if not has_real_value(value):
            return False

        field_lower = field_name.lower()
        temporal_indicators = self.temporal_patterns["sequence_indicators"]

        # Check field name for temporal indicators
        if any(indicator in field_lower for indicator in temporal_indicators):
            return True

        # Check value pattern for date-like content
        if isinstance(value, str):
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{1,2}-\w{3}-\d{4}' # DD-MMM-YYYY
            ]
            return any(re.search(pattern, value) for pattern in date_patterns)

        return False

    def _normalize_date_value(self, value: Any) -> Optional[str]:
        """Normalize date value to standard format"""
        if not has_real_value(value):
            return None

        str_value = str(value).strip()

        # Try common date formats
        date_formats = [
            "%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%Y-%m-%d %H:%M:%S"
        ]

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(str_value, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # Return original if no parsing successful
        return str_value

    def _sort_temporal_fields(self, temporal_fields: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Sort temporal fields by date value"""
        def date_sort_key(temporal_tuple):
            field_name, date_value = temporal_tuple
            try:
                return datetime.strptime(date_value, "%Y-%m-%d")
            except:
                return datetime.min

        return sorted(temporal_fields, key=date_sort_key)

    def process_cross_field_context(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process relationships between related fields"""
        context_entities = []

        # Process cause-evidence relationships
        context_entities.extend(self._process_cause_evidence_pairs(record))

        # Process action-outcome relationships
        context_entities.extend(self._process_action_outcome_pairs(record))

        # Process department flow relationships
        context_entities.extend(self._process_department_flow(record))

        return context_entities

    def _process_cause_evidence_pairs(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process cause and evidence field relationships"""
        pairs = []

        cause_field = "Root Cause"
        evidence_field = "Obj. Evidence"

        cause_value = record.get(cause_field)
        evidence_value = record.get(evidence_field)

        if has_real_value(cause_value) and has_real_value(evidence_value):
            # Process multiple causes and evidence
            causes = process_list_field(cause_value)
            evidences = process_list_field(evidence_value)

            for i, cause in enumerate(causes):
                for j, evidence in enumerate(evidences):
                    pair = {
                        "context_id": f"cause_evidence_{i}_{j}",
                        "cause_text": cause,
                        "evidence_text": evidence,
                        "relationship_type": "CAUSE_EVIDENCE",
                        "confidence": self._calculate_relationship_confidence(cause, evidence)
                    }
                    pairs.append(pair)

        return pairs

    def _process_action_outcome_pairs(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process action and outcome field relationships"""
        pairs = []

        action_outcome_mappings = [
            ("Action Plan", "Complete"),
            ("Recom.Action", "IsActionPlanEffective"),
            ("Action Plan", "Action Plan Eval Comment")
        ]

        for action_field, outcome_field in action_outcome_mappings:
            action_value = record.get(action_field)
            outcome_value = record.get(outcome_field)

            if has_real_value(action_value) and has_real_value(outcome_value):
                pair = {
                    "context_id": f"action_outcome_{clean_label(action_field)}_{clean_label(outcome_field)}",
                    "action_text": str(action_value),
                    "outcome_text": str(outcome_value),
                    "relationship_type": "ACTION_OUTCOME",
                    "action_field": action_field,
                    "outcome_field": outcome_field
                }
                pairs.append(pair)

        return pairs

    def _process_department_flow(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process department workflow relationships"""
        flows = []

        init_dept = record.get("Init. Dept.")
        rec_dept = record.get("Rec. Dept.")

        if has_real_value(init_dept) and has_real_value(rec_dept):
            if str(init_dept) != str(rec_dept):  # Only if different departments
                flow = {
                    "context_id": f"dept_flow_{clean_label(str(init_dept))}_{clean_label(str(rec_dept))}",
                    "from_department": str(init_dept),
                    "to_department": str(rec_dept),
                    "relationship_type": "DEPARTMENT_FLOW",
                    "transfer_type": "ESCALATION" if "safety" in str(rec_dept).lower() else "ASSIGNMENT"
                }
                flows.append(flow)

        return flows

    def _calculate_relationship_confidence(self, text1: str, text2: str) -> float:
        """Calculate confidence score for field relationship"""
        if not text1 or not text2:
            return 0.0

        # Simple word overlap confidence
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.1

        overlap = len(words1.intersection(words2))
        total_words = len(words1.union(words2))

        return min(1.0, overlap / total_words * 2)  # Scale to reasonable confidence

    def validate_field_dependencies(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate field dependency rules"""
        violations = []

        dependency_rules = VALIDATION_RULES["field_dependency_rules"]

        for trigger_field, trigger_value, dependent_field, requirement in dependency_rules:
            trigger_val = record.get(trigger_field)
            dependent_val = record.get(dependent_field)

            if self._check_trigger_condition(trigger_val, trigger_value):
                if requirement == "required" and not has_real_value(dependent_val):
                    violation = {
                        "violation_id": f"dep_{clean_label(trigger_field)}_{clean_label(dependent_field)}",
                        "trigger_field": trigger_field,
                        "trigger_value": str(trigger_val),
                        "dependent_field": dependent_field,
                        "requirement": requirement,
                        "violation_type": "MISSING_DEPENDENT_FIELD"
                    }
                    violations.append(violation)

        return violations

    def _check_trigger_condition(self, actual_value: Any, expected_value: str) -> bool:
        """Check if trigger condition is met"""
        if not has_real_value(actual_value):
            return False

        actual_str = str(actual_value).lower().strip()
        expected_str = expected_value.lower().strip()

        # Handle boolean-like values
        if expected_str == "true":
            return actual_str in self.normalization_rules["boolean_true_values"]
        elif expected_str == "false":
            return actual_str in self.normalization_rules["boolean_false_values"]
        else:
            return actual_str == expected_str

    def extract_field_patterns(self, record: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract patterns from field values for analytics"""
        patterns = {
            "categories": [],
            "identifiers": [],
            "statuses": [],
            "quantitative": []
        }

        for field_name, value in record.items():
            if not has_real_value(value):
                continue

            str_value = str(value)

            # Category patterns
            if field_name in ["Categories", "Action Types", "Operating Centre"]:
                patterns["categories"].append(str_value)

            # Identifier patterns
            elif re.match(r'^[A-Z]{2,3}-\d{3,4}', str_value):
                patterns["identifiers"].append(str_value)

            # Status patterns
            elif any(status in str_value.lower() for status in ["open", "closed", "pending", "complete"]):
                patterns["statuses"].append(str_value)

            # Quantitative patterns
            elif re.match(r'^\d+(\.\d+)?$', str_value):
                patterns["quantitative"].append(str_value)

        return patterns

    def create_field_analytics_entities(self, record: Dict[str, Any], base_id: str) -> List[Dict[str, Any]]:
        """Create entities for field-level analytics"""
        analytics_entities = []

        # Performance indicators
        for field_name in ANALYTICS_CATEGORIES["performance_indicators"]:
            value = record.get(field_name)
            if has_real_value(value):
                entity = {
                    "analytics_id": f"perf_{base_id}_{clean_label(field_name)}",
                    "base_record_id": base_id,
                    "category": "performance",
                    "field_name": field_name,
                    "field_value": str(value),
                    "analytical_dimension": "operational_efficiency"
                }
                analytics_entities.append(entity)

        # Classification dimensions
        for field_name in ANALYTICS_CATEGORIES["classification_dimensions"]:
            value = record.get(field_name)
            if has_real_value(value):
                entity = {
                    "analytics_id": f"class_{base_id}_{clean_label(field_name)}",
                    "base_record_id": base_id,
                    "category": "classification",
                    "field_name": field_name,
                    "field_value": str(value),
                    "analytical_dimension": "categorical_analysis"
                }
                analytics_entities.append(entity)

        return analytics_entities
