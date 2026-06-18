"""FunSearch-style program evolution -- the agent evolves a small function.

This is the genuine FunSearch mechanism, with the *driving agent* playing the
role of the LLM. A project that wants it exports an `EVOLVE` spec from its
`project.py`; this module then maintains an island-structured database of
candidate programs (each a single evolvable function) on disk, and a rigorous
evaluator that scores any candidate by *running it* and auditing the result.

The loop, agent-driven:

    lab.py evolve status            # islands + champion scores per dimension
    lab.py evolve sample --k 2      # show high-scoring PARENT programs to learn from
    #   ... agent writes a new, improved program file ...
    lab.py evolve eval prog.py      # rigorous score; registered iff it runs + is valid
    lab.py evolve best              # current champion program + scores

The evaluator is the un-gameable spine: for cap_set, every construction is
audited by `is_cap`, so a program cannot score by cheating -- only by actually
building a larger valid cap. Programs that run and validate are kept (clustered
into islands for diversity, FunSearch-style); the per-dimension champion is what
feeds the frontier (promote it with a one-line experiment + `lab.py record`).

A project's EVOLVE spec (dict) must provide:
    signature : str                      # e.g. "def priority(v, n) -> float"
    entry     : str                      # the function name to extract, e.g. "priority"
    evaluate  : Callable[[Callable], dict]   # -> {"valid","scores","fitness",
                                              #     "per_dim_metric": {dim: (track,metric,value)}}
    seed      : str                      # source of a trivial starter program
    islands   : int = 4                  # number of islands
    cluster   : list                     # dims/instances evaluated (for display)
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import os
import random
import time
from typing import Callable, Optional

from harness import project as P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _spec() -> dict:
    cfg = importlib.import_module(P.PKG + ".project")
    spec = getattr(cfg, "EVOLVE", None)
    if spec is None:
        raise SystemExit(f"project {P.NAME!r} defines no EVOLVE spec; "
                         f"`lab.py evolve` is only for FunSearch-style projects.")
    spec.setdefault("islands", 4)
    spec.setdefault("entry", "priority")
    return spec


def _dirs(spec: dict) -> tuple[str, str, str]:
    base = P.path("state", "evolve", spec.get("name", spec["entry"]))
    progs = os.path.join(base, "programs")
    db = os.path.join(base, "db.json")
    os.makedirs(progs, exist_ok=True)
    return base, progs, db


def _load_db(db_path: str) -> list[dict]:
    if not os.path.exists(db_path):
        return []
    with open(db_path) as f:
        return json.load(f)


def _save_db(db_path: str, rows: list[dict]) -> None:
    tmp = db_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(rows, f, indent=2)
    os.replace(tmp, db_path)


def _load_callable(program_path: str, entry: str) -> Callable:
    """Import a program file and return its evolvable function."""
    spec = importlib.util.spec_from_file_location("_evolve_candidate", program_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {program_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, entry, None)
    if not callable(fn):
        raise ValueError(f"{program_path} must define a callable {entry!r} "
                         f"({_spec_one_line()})")
    return fn


def _spec_one_line() -> str:
    try:
        return _spec()["signature"]
    except SystemExit:
        return "the EVOLVE signature"


def _ensure_seed(spec: dict, progs: str, db_path: str) -> list[dict]:
    """If the DB is empty, plant the trivial seed program so `sample` has parents."""
    rows = _load_db(db_path)
    if rows:
        return rows
    seed_path = os.path.join(progs, "prog_0000_seed.py")
    if not os.path.exists(seed_path):
        with open(seed_path, "w") as f:
            f.write(spec["seed"])
    fn = _load_callable(seed_path, spec["entry"])
    ev = spec["evaluate"](fn)
    rows = [_row(0, seed_path, ev, island=0, parents=[])]
    _save_db(db_path, rows)
    return rows


def _row(pid: int, path: str, ev: dict, island: int, parents: list[int]) -> dict:
    return {
        "id": pid,
        "path": os.path.relpath(path, ROOT),
        "island": island,
        "valid": bool(ev["valid"]),
        "fitness": float(ev["fitness"]),
        "scores": ev["scores"],
        "parents": parents,
        "created_at": time.time(),
    }


# --------------------------------------------------------------------------- #
# Public operations
# --------------------------------------------------------------------------- #
def status() -> str:
    spec = _spec()
    _, progs, db_path = _dirs(spec)
    rows = _ensure_seed(spec, progs, db_path)
    out = [f"EVOLVE target: {spec.get('name', spec['entry'])}  "
           f"({spec['signature']})",
           f"cluster: {spec.get('cluster')}   islands: {spec['islands']}   "
           f"programs: {len(rows)}", ""]
    # champion per dim
    champ = _champions(rows)
    out.append("CHAMPION cap per dimension (best valid program):")
    for dim in sorted(champ):
        pid, size = champ[dim]
        out.append(f"  dim {dim}: {size}  (prog {pid})")
    out.append("")
    out.append("ISLANDS (count, best fitness):")
    for isl in range(spec["islands"]):
        members = [r for r in rows if r["island"] == isl and r["valid"]]
        best = max((r["fitness"] for r in members), default=0.0)
        out.append(f"  island {isl}: {len(members)} programs, best fitness {best:g}")
    return "\n".join(out)


def _champions(rows: list[dict]) -> dict[int, tuple[int, float]]:
    champ: dict[int, tuple[int, float]] = {}
    for r in rows:
        if not r["valid"]:
            continue
        for dim, size in r["scores"].items():
            d = int(dim)
            if d not in champ or size > champ[d][1]:
                champ[d] = (r["id"], size)
    return champ


def sample(k: int = 2, island: Optional[int] = None, seed: Optional[int] = None) -> str:
    """Show k high-scoring parent programs (best-shot prompt material)."""
    spec = _spec()
    _, progs, db_path = _dirs(spec)
    rows = _ensure_seed(spec, progs, db_path)
    rng = random.Random(seed if seed is not None else time.time_ns())
    if island is None:
        islands = sorted({r["island"] for r in rows if r["valid"]})
        island = rng.choice(islands) if islands else 0
    members = sorted((r for r in rows if r["island"] == island and r["valid"]),
                     key=lambda r: r["fitness"], reverse=True)
    if not members:
        members = sorted((r for r in rows if r["valid"]),
                         key=lambda r: r["fitness"], reverse=True)
    chosen = members[:k]
    out = [f"# {len(chosen)} parent program(s) from island {island} "
           f"(fitness = sum of cap sizes over {spec.get('cluster')}).",
           f"# Write a NEW, improved program with the same interface: "
           f"{spec['signature']}.",
           f"# Read prompts/evolve.md. Save it, then: lab.py evolve eval <file>.", ""]
    for r in chosen:
        out.append(f"# ---- prog {r['id']}  fitness={r['fitness']:g}  scores={r['scores']} ----")
        with open(os.path.join(ROOT, r["path"])) as f:
            out.append(f.read().rstrip())
        out.append("")
    return "\n".join(out)


def evaluate(program_path: str) -> str:
    """Rigorously score a candidate program; register it iff valid."""
    spec = _spec()
    _, progs, db_path = _dirs(spec)
    rows = _ensure_seed(spec, progs, db_path)
    fn = _load_callable(program_path, spec["entry"])
    ev = spec["evaluate"](fn)

    champ_before = _champions(rows)
    lines = [f"scores: {ev['scores']}   fitness: {ev['fitness']:g}   valid: {ev['valid']}"]
    if not ev["valid"]:
        lines.append("INVALID -- a construction failed the rigorous audit; NOT registered.")
        if ev.get("audit"):
            lines.append(f"audit: {ev['audit']}")
        return "\n".join(lines)

    # Assign to the least-populated island for diversity; copy the source in.
    counts = {i: 0 for i in range(spec["islands"])}
    for r in rows:
        counts[r["island"]] = counts.get(r["island"], 0) + 1
    island = min(counts, key=counts.get)
    pid = (max((r["id"] for r in rows), default=-1)) + 1
    dest = os.path.join(progs, f"prog_{pid:04d}.py")
    with open(program_path) as src, open(dest, "w") as dst:
        dst.write(src.read())
    rows.append(_row(pid, dest, ev, island=island, parents=[]))
    _save_db(db_path, rows)

    lines.append(f"REGISTERED as prog {pid} on island {island} -> {os.path.relpath(dest, ROOT)}")
    improved = []
    for dim, size in ev["scores"].items():
        d = int(dim)
        before = champ_before.get(d, (None, -1))[1]
        if size > before:
            improved.append(f"dim {d}: {before if before >= 0 else '-'} -> {size}")
    if improved:
        lines.append("NEW CHAMPION(S): " + "; ".join(improved))
        lines.append("Promote into the frontier: write a one-line experiment that "
                     "runs this program for that dimension and `lab.py record` it.")
    else:
        lines.append("No per-dimension champion improved (kept for island diversity).")
    return "\n".join(lines)


def best() -> str:
    spec = _spec()
    _, progs, db_path = _dirs(spec)
    rows = _ensure_seed(spec, progs, db_path)
    champ = _champions(rows)
    out = ["CHAMPION program per dimension:"]
    for dim in sorted(champ):
        pid, size = champ[dim]
        path = next((r["path"] for r in rows if r["id"] == pid), "?")
        out.append(f"  dim {dim}: size {size}  -> prog {pid}  ({path})")
    return "\n".join(out)


def champion_priority(dim: int) -> Callable:
    """Return the champion evolvable function for a given dimension (for use by a
    promotion experiment). Raises if no valid program covers that dimension."""
    spec = _spec()
    _, progs, db_path = _dirs(spec)
    rows = _ensure_seed(spec, progs, db_path)
    champ = _champions(rows)
    if dim not in champ:
        raise ValueError(f"no champion program for dim {dim}")
    pid = champ[dim][0]
    path = next(r["path"] for r in rows if r["id"] == pid)
    return _load_callable(os.path.join(ROOT, path), spec["entry"])


def cli(args) -> int:
    if args.action == "status":
        print(status())
    elif args.action == "best":
        print(best())
    elif args.action == "sample":
        print(sample(k=args.k, island=args.island))
    elif args.action == "eval":
        if not args.program:
            print("usage: lab.py evolve eval <program.py>")
            return 2
        print(evaluate(args.program))
    return 0
