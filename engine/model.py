from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    relation: str
    weight: float
    confidence: str
    confidence_weight: float
    causal_status: str
    mechanism: str
    contexts: Dict[str, float] = field(default_factory=dict)

@dataclass
class ReasoningCase:
    seeds: Dict[str, float]
    context: Dict[str, float] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)
    notes: Optional[str] = None

@dataclass
class EdgeContribution:
    edge_id: str
    source: str
    target: str
    relation: str
    raw_source_activation: float
    signed_weight: float
    confidence_weight: float
    context_multiplier: float
    contribution: float
    mechanism: str
    causal_status: str

@dataclass
class ReasoningResult:
    activations: Dict[str, float]
    confidence: Dict[str, float]
    support: Dict[str, float]
    inhibition: Dict[str, float]
    trace: List[EdgeContribution]
    iterations: int
    converged: bool
    dominant_nodes: List[str]
    tensions: List[Dict[str, Any]]
