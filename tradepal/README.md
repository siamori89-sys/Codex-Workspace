# TRADEPAL persistent project area

This directory is exclusively the persistent state of the opt-in TRADEPAL MQL5 workflow. It is inactive until the user says `START TRADEPAL`.

- `state/` — current specification, contract, version pointer, ledger, questions, feedback, and research.
- `sage/archive/` — append-only full conversation archive, chunked JSONL.
- `sage/analytical-memory.md` and `sage/insight-journal.md` — long-term strategic record.
- `simulations/` — setup-only validation artifacts, never part of a user project.

Use `.agents/skills/tradepal/scripts/tradepal_state.py` to initialize, append, search, validate, and simulate the workflow.
