from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

from reasoning.global_runtime import GlobalGrowthReasoner


@dataclass
class BenchmarkResult:
    scenario_id: str
    passed: bool
    failures: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GlobalAdversarialBenchmark:
    def __init__(self, reasoner: GlobalGrowthReasoner, suite: Dict[str, Any]):
        self.reasoner = reasoner
        self.suite = suite

    @classmethod
    def from_repo_root(cls, root: str | Path) -> "GlobalAdversarialBenchmark":
        root = Path(root)
        reasoner = GlobalGrowthReasoner.from_repo_root(root)
        suite = json.loads(
            (root / "benchmarks/global_adversarial_scenarios.json").read_text()
        )
        return cls(reasoner, suite)

    @staticmethod
    def _subset(required: List[str], actual: List[str]) -> bool:
        return set(required).issubset(set(actual))

    def run_scenario(self, scenario: Dict[str, Any]) -> BenchmarkResult:
        scenario_id = scenario["id"]
        failures: List[str] = []
        expected_error = scenario.get("expect_error")

        try:
            out = self.reasoner.reason(scenario["case"])
        except Exception as exc:
            if expected_error and exc.__class__.__name__ == expected_error:
                return BenchmarkResult(scenario_id, True, [])
            return BenchmarkResult(
                scenario_id,
                False,
                [f"unexpected error {exc.__class__.__name__}: {exc}"],
            )

        if expected_error:
            return BenchmarkResult(
                scenario_id,
                False,
                [f"expected {expected_error} but reasoning succeeded"],
            )

        expected = scenario.get("expect", {})
        if not self._subset(expected.get("rules", []), out.matched_rules):
            failures.append(
                f"missing rules: expected {expected.get('rules', [])}, "
                f"actual {out.matched_rules}"
            )

        actual_cores = [x.get("core") for x in out.bottleneck_candidates]
        if not self._subset(expected.get("cores", []), actual_cores):
            failures.append(
                f"missing cores: expected {expected.get('cores', [])}, "
                f"actual {actual_cores}"
            )

        if not self._subset(
            expected.get("forbidden", []),
            out.forbidden_inferences,
        ):
            failures.append(
                f"missing forbidden inferences: "
                f"expected {expected.get('forbidden', [])}, "
                f"actual {out.forbidden_inferences}"
            )

        expected_ceiling = expected.get("causal_ceiling")
        if expected_ceiling and out.causal_ceiling != expected_ceiling:
            failures.append(
                f"causal ceiling expected {expected_ceiling}, "
                f"actual {out.causal_ceiling}"
            )

        for target in expected.get("hpc_targets", []):
            if out.hpc_reasoning is None:
                failures.append("expected HPC reasoning but none was returned")
                break
            if target not in out.hpc_reasoning.get("conclusions", {}):
                failures.append(f"missing HPC target conclusion: {target}")

        return BenchmarkResult(scenario_id, not failures, failures)

    def run_all(self) -> List[BenchmarkResult]:
        return [
            self.run_scenario(s)
            for s in sorted(self.suite["scenarios"], key=lambda x: x["id"])
        ]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    benchmark = GlobalAdversarialBenchmark.from_repo_root(root)
    results = benchmark.run_all()
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{result.scenario_id}: {status}")
        for failure in result.failures:
            print(f"  - {failure}")
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
