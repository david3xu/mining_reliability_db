#!/usr/bin/env python3
"""
Phase 1 Core Foundation Validation Script

Validates the implementation of Phase 1 Core Foundation including:
- Intelligence Engine with unified field resolution
- Workflow Processor with unified field resolution
- Enhanced QueryManager with business query capabilities
- Configuration consolidation and schema enhancements

This script ensures 100% compliance with the core layer → adapter → component workflow pattern.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def validate_configuration_consolidation():
    """Validate that configuration files have been properly consolidated"""
    logger.info("Validating configuration consolidation...")

    try:
        # Check model_schema.json enhancements
        config_path = Path("configs/model_schema.json")
        if not config_path.exists():
            return False, "model_schema.json not found"

        with open(config_path, "r") as f:
            schema = json.load(f)

        # Check for Phase 1 Core Foundation features
        required_features = [
            "schema_version",
            "architecture_compliance",
            "metadata",
            "core_foundation_framework",
            "phase_implementation",
        ]

        missing_features = []
        for feature in required_features:
            if feature not in schema:
                missing_features.append(feature)

        if missing_features:
            return False, f"Missing configuration features: {missing_features}"

        # Check version compliance
        if schema.get("schema_version") != "3.0.0":
            return (
                False,
                f"Schema version mismatch: expected 3.0.0, got {schema.get('schema_version')}",
            )

        # Check architecture compliance
        expected_compliance = "unified_field_reference_enhanced"
        if schema.get("architecture_compliance") != expected_compliance:
            return False, f"Architecture compliance mismatch: expected {expected_compliance}"

        # Check core foundation framework
        core_foundation = schema.get("core_foundation_framework", {})
        required_engines = ["intelligence_engine", "workflow_processor"]

        for engine in required_engines:
            if engine not in core_foundation:
                return False, f"Missing core foundation engine: {engine}"

        logger.info("✅ Configuration consolidation validation passed")
        return True, "Configuration consolidation successful"

    except Exception as e:
        return False, f"Configuration validation error: {str(e)}"


def validate_unified_field_resolution():
    """Validate unified field resolution system"""
    logger.info("Validating unified field resolution system...")

    try:
        # Import field mappings directly
        import json
        import os

        config_path = os.path.join(
            os.path.dirname(__file__), "..", "configs", "field_mappings.json"
        )
        with open(config_path, "r") as f:
            field_mappings = json.load(f)

        # Test field mapping access for key entities
        test_cases = [
            ("ActionRequest", "action_request_number"),
            ("Problem", "what_happened"),
            ("RootCause", "root_cause"),
            ("Facility", "facility_name"),
            ("ActionPlan", "action_plan"),
        ]

        failed_tests = []
        entity_mappings = field_mappings.get("entity_mappings", {})

        for entity, business_field in test_cases:
            try:
                entity_mapping = entity_mappings.get(entity, {})
                db_field = entity_mapping.get(business_field)

                if not db_field:
                    failed_tests.append(f"{entity}.{business_field} - no mapping found")
                else:
                    logger.debug(f"✓ {entity}.{business_field} -> {db_field}")

            except Exception as e:
                failed_tests.append(f"{entity}.{business_field}: {str(e)}")

        if failed_tests:
            return False, f"Field mapping access failures: {failed_tests}"

        # Validate field mappings structure
        required_sections = [
            "cascade_labeling",
            "entity_mappings",
            "field_categories",
            "adapter_optimization",
        ]
        for section in required_sections:
            if section not in field_mappings:
                return False, f"Missing required section: {section}"

        logger.info("✅ Direct field mapping access validation passed")
        return True, "Direct field mapping system working correctly"

    except ImportError as e:
        return False, f"Cannot import field resolver: {str(e)}"
    except Exception as e:
        return False, f"Field resolution validation error: {str(e)}"


def validate_intelligence_engine():
    """Validate Intelligence Engine integration"""
    logger.info("Validating Intelligence Engine...")

    try:
        # Import intelligence engine
        from mine_core.business.intelligence_engine import get_intelligence_engine

        intelligence_engine = get_intelligence_engine()

        # Test basic functionality
        if not hasattr(intelligence_engine, "field_mappings"):
            return False, "Intelligence Engine missing field_mappings attribute"

        if not hasattr(intelligence_engine, "core_foundation_config"):
            return False, "Intelligence Engine missing core_foundation_config attribute"

        # Test basic methods exist
        required_methods = [
            "analyze_causal_relationships",
            "calculate_performance_metrics",
            "generate_operational_insights",
            "validate_business_rules",
        ]

        missing_methods = []
        for method in required_methods:
            if not hasattr(intelligence_engine, method):
                missing_methods.append(method)

        if missing_methods:
            return False, f"Intelligence Engine missing methods: {missing_methods}"

        logger.info("✅ Intelligence Engine validation passed")
        return True, "Intelligence Engine integration successful"

    except ImportError as e:
        return False, f"Cannot import Intelligence Engine: {str(e)}"
    except Exception as e:
        return False, f"Intelligence Engine validation error: {str(e)}"


def validate_workflow_processor():
    """Validate Workflow Processor integration"""
    logger.info("Validating Workflow Processor...")

    try:
        # Import workflow processor
        from mine_core.business.workflow_processor import WorkflowProcessor

        workflow_processor = WorkflowProcessor()

        # Test integration attributes
        if not hasattr(workflow_processor, "field_mappings"):
            return False, "Workflow Processor missing field_mappings attribute"

        if not hasattr(workflow_processor, "core_foundation_config"):
            return False, "Workflow Processor missing core_foundation_config attribute"

        # Test that it has query manager integration
        if not hasattr(workflow_processor, "query_manager"):
            return False, "Workflow Processor missing query_manager attribute"

        logger.info("✅ Workflow Processor validation passed")
        return True, "Workflow Processor integration successful"

    except ImportError as e:
        return False, f"Cannot import Workflow Processor: {str(e)}"
    except Exception as e:
        return False, f"Workflow Processor validation error: {str(e)}"


def validate_query_manager_enhancement():
    """Validate QueryManager enhancements"""
    logger.info("Validating QueryManager enhancements...")

    try:
        # Import query manager
        from mine_core.database.query_manager import QueryType, get_query_manager

        query_manager = get_query_manager()

        # Test direct field mapping integration
        if not hasattr(query_manager, "field_mappings"):
            return False, "QueryManager missing field_mappings attribute"

        # Test new business query methods
        if not hasattr(query_manager, "execute_business_query"):
            return False, "QueryManager missing execute_business_query method"

        # Test QueryType enum
        required_query_types = ["CAUSAL_ANALYSIS", "PERFORMANCE_METRICS", "WORKFLOW_ANALYSIS"]
        missing_types = []

        for query_type in required_query_types:
            if not hasattr(QueryType, query_type):
                missing_types.append(query_type)

        if missing_types:
            return False, f"QueryType missing types: {missing_types}"

        logger.info("✅ QueryManager enhancement validation passed")
        return True, "QueryManager enhancements successful"

    except ImportError as e:
        return False, f"Cannot import QueryManager: {str(e)}"
    except Exception as e:
        return False, f"QueryManager validation error: {str(e)}"


def validate_architecture_compliance():
    """Validate overall architecture compliance"""
    logger.info("Validating architecture compliance...")

    try:
        # Test import dependencies follow clean architecture
        # Core layer should only import from shared and configs
        # Test that core business logic has no dashboard dependencies
        import inspect

        from configs import environment
        from mine_core.business import intelligence_engine, workflow_processor
        from mine_core.database import query_manager

        # Get source code of intelligence engine
        ie_source = inspect.getsource(intelligence_engine)
        if "dashboard" in ie_source.lower():
            return False, "Intelligence Engine has dashboard dependencies (architecture violation)"

        # Get source code of workflow processor
        wp_source = inspect.getsource(workflow_processor)
        if "dashboard" in wp_source.lower():
            return False, "Workflow Processor has dashboard dependencies (architecture violation)"

        logger.info("✅ Architecture compliance validation passed")
        return True, "Architecture compliance maintained"

    except Exception as e:
        return False, f"Architecture compliance validation error: {str(e)}"


def main():
    """Run Phase 1 Core Foundation validation"""
    logger.info("Starting Phase 1 Core Foundation Validation")
    logger.info("=" * 60)

    validation_results = []

    # Run all validations
    validations = [
        ("Configuration Consolidation", validate_configuration_consolidation),
        ("Unified Field Resolution", validate_unified_field_resolution),
        ("Intelligence Engine", validate_intelligence_engine),
        ("Workflow Processor", validate_workflow_processor),
        ("QueryManager Enhancement", validate_query_manager_enhancement),
        ("Architecture Compliance", validate_architecture_compliance),
    ]

    all_passed = True

    for name, validation_func in validations:
        logger.info(f"Running {name} validation...")
        try:
            success, message = validation_func()
            validation_results.append({"validation": name, "success": success, "message": message})

            if success:
                logger.info(f"✅ {name}: {message}")
            else:
                logger.error(f"❌ {name}: {message}")
                all_passed = False

        except Exception as e:
            logger.error(f"❌ {name}: Validation failed with exception: {str(e)}")
            validation_results.append(
                {"validation": name, "success": False, "message": f"Exception: {str(e)}"}
            )
            all_passed = False

    # Summary
    logger.info("=" * 60)
    if all_passed:
        logger.info("🎉 Phase 1 Core Foundation Validation: ALL TESTS PASSED")
        logger.info("✅ Ready to proceed to Phase 2: Adapter Purification")
        exit_code = 0
    else:
        logger.error("❌ Phase 1 Core Foundation Validation: SOME TESTS FAILED")
        logger.error("🔧 Please fix the issues before proceeding to Phase 2")
        exit_code = 1

    # Save validation results
    results_file = Path("validation_results_phase1.json")
    with open(results_file, "w") as f:
        json.dump(
            {
                "phase": "Phase 1 - Core Foundation",
                "timestamp": "2025-06-02",
                "overall_success": all_passed,
                "validation_results": validation_results,
            },
            f,
            indent=2,
        )

    logger.info(f"📊 Validation results saved to: {results_file}")

    return exit_code


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"❌ Validation script failed: {str(e)}")
        sys.exit(1)
