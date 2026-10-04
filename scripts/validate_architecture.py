import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "architecture" / "ontology.json"

ALLOWED_LEVELS = {"core","module","neuron","micro_neuron"}
ALLOWED_STATUS = {"candidate","under_review","accepted","provisional","deprecated","rejected"}

def validate_architecture(path=ARCH):
    data = json.loads(Path(path).read_text())
    errors = []

    required_top = [
        "architecture_id","version","layers","core_anchors","object_classes",
        "edge_relation_vocabulary","causal_status_vocabulary",
        "context_dimensions","uncertainty_channels","runtime_rule"
    ]
    for key in required_top:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    anchors = data.get("core_anchors", [])
    if len(anchors) != 8:
        errors.append(f"expected 8 current core anchors, got {len(anchors)}")
    if len(set(anchors)) != len(anchors):
        errors.append("duplicate core anchor")

    layers = data.get("layers", [])
    kinds = {x.get("kind") for x in layers}
    if kinds != ALLOWED_LEVELS:
        errors.append(f"layer kinds mismatch: {sorted(kinds)}")

    for field in [
        "object_classes","edge_relation_vocabulary","causal_status_vocabulary",
        "context_dimensions","uncertainty_channels","lifecycle"
    ]:
        values = data.get(field, [])
        if len(values) != len(set(values)):
            errors.append(f"duplicates in {field}")

    if len(data.get("uncertainty_channels", [])) < 5:
        errors.append("uncertainty model must preserve >=5 independent channels")

    if "runtime propagation weight" not in data.get("runtime_rule",""):
        errors.append("runtime/effect-size separation rule missing")

    return errors

if __name__ == "__main__":
    errors = validate_architecture()
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors))
        raise SystemExit(1)
    print("Architecture validation: PASS")
