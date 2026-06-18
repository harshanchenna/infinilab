# CLAUDE.md

This project is driven from **AGENTS.md** — read it first. It is the single,
harness-neutral playbook for how an agent (Claude Code, Codex, or a human) runs
the infinilab research loop: read state, propose an experiment, verify (Tier-1),
scrutinise (Tier-2 skeptic), `record`, then commit and push.

You drive the deterministic `lab.py` CLI yourself with your own tools; nothing
shells out to an LLM. Quick reference:

```bash
python lab.py status         # frontier + recent ledger
python lab.py next           # next experiment filename/module
python lab.py verify <mod>   # Tier-1 verify (prints the numbers)
python lab.py record <mod> --skeptic sound   # apply keeping rules + journal/KB
python lab.py evolve sample  # FunSearch program evolution (cap_set)
```

Conventions for this repo: commit AND push every iteration to the working branch
with a detailed message; never edit `harness/` or a project's `lib/` to make a
result pass; set `novelty` honestly. Full details and invariants live in
AGENTS.md.
