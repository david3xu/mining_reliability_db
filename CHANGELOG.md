# Changelog

All notable changes to the Mining Reliability DB project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project structure
- Neo4j graph database schema creation
- Data import pipeline for facility incident records
- Basic query functionality
- Documentation

## [0.1.0] - YYYY-MM-DD

### Added

- Core entity model based on 12-entity design
- ETL pipeline for raw reliability data
- Schema creation and database reset utilities
- Test framework

### Changed

- Refactored from original SQL model to Neo4j graph representation
- Implemented hierarchical chain pattern instead of hub-and-spoke
