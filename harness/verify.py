"""Tier-1 verifier: the hard, un-gameable gate.

It runs an experiment module in a subprocess under a wall-clock budget and
returns a verdict derived purely from *executing code and reading numbers*.
No language model is involved at this tier. This is the analog of comparing
val_bpb in Karpathy autoresearch: cheap, automatic, and impossible to talk your
way past.

Verdicts
--------
    OK            : ran within budget, returned a valid Result.
    FALSIFICATION : ran fine AND reported falsified=True with evidence (jackpot).
    INVALID       : returned a Result that violates the contract.
    FAILED        : raised an exception.
    TIMEOUT       : exceeded the wall-clock budget.
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Verdict:
    status: str
    module: str
    elapsed_seconds: float = 0.0
    result: Optional[dict] = None
    manifest: Optional[dict] = None
    error: Optional[str] = None
    raw_stdout: str = ""
    raw_stderr: str = field(default="", repr=False)

    @property
    def ok(self) -> bool:
        return self.status in ("OK", "FALSIFICATION")

    def summary(self) -> str:
        if self.result:
            r = self.result
            return (
                f"[{self.status}] {self.module} :: {r['track']} :: "
                f"{r['frontier_metric']}={r['frontier_value']:g} :: {r['claim']}"
            )
        return f"[{self.status}] {self.module} :: {self.error or ''}"


def verify(module_name: str, budget_seconds: float = 300.0) -> Verdict:
    """Run `module_name`'s experiment and return a Verdict."""
    cmd = [sys.executable, "-m", "harness.run_experiment", module_name, str(budget_seconds)]
    try:
        # Hard timeout = budget + slack for import/startup (compilation excluded,
        # mirroring autoresearch's "wall clock, excluding startup").
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=budget_seconds + 60,
        )
    except subprocess.TimeoutExpired as e:
        return Verdict(
            status="TIMEOUT",
            module=module_name,
            elapsed_seconds=budget_seconds + 60,
            error=f"exceeded wall-clock budget of {budget_seconds}s",
            raw_stdout=(e.stdout or "") if isinstance(e.stdout, str) else "",
        )

    payload = _extract_payload(proc.stdout)
    if payload is None:
        return Verdict(
            status="FAILED",
            module=module_name,
            error="no __RESULT__ line in subprocess output",
            raw_stdout=proc.stdout,
            raw_stderr=proc.stderr,
        )

    status = payload.get("status", "FAILED")
    if status == "OK":
        res = payload["result"]
        final_status = "FALSIFICATION" if res.get("falsified") else "OK"
        return Verdict(
            status=final_status,
            module=module_name,
            elapsed_seconds=payload.get("elapsed_seconds", 0.0),
            result=res,
            manifest=payload.get("manifest"),
            raw_stdout=proc.stdout,
            raw_stderr=proc.stderr,
        )
    return Verdict(
        status=status,  # INVALID / FAILED
        module=module_name,
        elapsed_seconds=payload.get("elapsed_seconds", 0.0),
        error=payload.get("error"),
        raw_stdout=proc.stdout,
        raw_stderr=proc.stderr,
    )


def _extract_payload(stdout: str) -> Optional[dict]:
    for line in reversed(stdout.splitlines()):
        if line.startswith("__RESULT__"):
            try:
                return json.loads(line[len("__RESULT__"):])
            except json.JSONDecodeError:
                return None
    return None


if __name__ == "__main__":
    # CLI: python -m harness.verify experiments.exp_0001_critical_line [budget]
    mod = sys.argv[1]
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    v = verify(mod, budget)
    print(v.summary())
    if v.error:
        print(v.error)
