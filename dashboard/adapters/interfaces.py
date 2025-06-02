#!/usr/bin/env python3
"""
Adapter Data Interfaces - Type-Safe Data Contracts
Clean data structures for adapter-component communication.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ComponentMetadata:
    """Metadata for all dashboard data components"""

    source: str
    generated_at: str
    data_quality: float
    cache_hit: bool = False
    processing_time_ms: Optional[float] = None


@dataclass
class ValidationResult:
    """Validation status for data components"""

    is_valid: bool
    component_status: Dict[str, bool]
    error_details: Optional[str]
    data_quality_score: float


@dataclass
class PortfolioData:
    """Portfolio metrics for header cards"""

    total_records: int
    data_fields: int
    facilities: int
    years_coverage: int
    year_detail: str
    metadata: ComponentMetadata


@dataclass
class FacilityData:
    """Facility breakdown for pie chart visualization"""

    labels: List[str]
    values: List[int]
    percentages: List[float]
    total_records: int
    metadata: ComponentMetadata


@dataclass
class FieldData:
    """Field distribution for bar chart visualization"""

    labels: List[str]
    values: List[int]
    percentages: List[float]
    total_fields: int
    metadata: ComponentMetadata


@dataclass
class TimelineData:
    """Historical timeline for table visualization"""

    columns: List[str]
    rows: List[Dict[str, Any]]
    year_range: List[int]
    total_records: int
    facilities_count: int
    metadata: ComponentMetadata


@dataclass
class ChartConfig:
    """Configuration for chart components"""

    height: int
    width: Optional[int]
    colors: List[str]
    font_size: int
    show_legend: bool


@dataclass
class DashboardConfig:
    """Complete dashboard configuration"""

    server_host: str
    server_port: int
    auto_refresh_interval: int
    chart_config: ChartConfig
    performance_thresholds: Dict[str, float]


# Type aliases for common data structures
PlotlyData = Dict[str, Any]
ComponentResult = Dict[str, Any]
StyleConfig = Dict[str, Any]
