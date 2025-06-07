from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class IntelligenceResult:
    """Standardized intelligence analysis result"""

    analysis_type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    quality_score: float
    generated_at: str
