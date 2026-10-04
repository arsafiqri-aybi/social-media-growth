from typing import Dict
from .model import ReasoningResult

def summarize(result: ReasoningResult, labels: Dict[str, str]) -> str:
    lines = []
    lines.append("Dominant activations:")
    for nid in result.dominant_nodes:
        lines.append(
            f"- {labels.get(nid, nid)}: activation={result.activations[nid]:.3f}, "
            f"evidence-signal={result.confidence[nid]:.3f}"
        )

    lines.append("\nStrongest propagated mechanisms:")
    for t in result.trace[:8]:
        lines.append(
            f"- {labels.get(t.source, t.source)} -> {labels.get(t.target, t.target)} "
            f"({t.relation}, contribution={t.contribution:.3f}): {t.mechanism}"
        )

    if result.tensions:
        lines.append("\nTensions:")
        for item in result.tensions:
            lines.append(
                f"- {labels.get(item['node'], item['node'])}: "
                f"support={item['support']}, inhibition={item['inhibition']}"
            )
    return "\n".join(lines)
