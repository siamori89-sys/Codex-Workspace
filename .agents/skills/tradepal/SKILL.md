---
name: tradepal
description: Run TRADEPAL, a persistent staged workflow for collaboratively discovering, contracting, building, validating, versioning, and evolving MQL5 MetaTrader 5 indicators and expert advisors. Use only after the user says START TRADEPAL or clearly invokes the workflow; end it on STOP TRADEPAL.
---

# TRADEPAL

Use this workflow only for the active TRADEPAL project; never apply its state or rules to unrelated work. Read `references/workflow.md` and `references/roles.md` at activation and use `scripts/tradepal_state.py` for all persistent state, transcript, and validation operations.

## Turn protocol

1. Append each TRADEPAL user turn losslessly before substantive work, and append each substantive final reply before ending the turn.
2. **ARCHITECT** owns discovery, requirement statuses, product decision, impact analysis, and contracts. Do not write executable MQL5 before an explicitly approved initial contract.
3. **ENGINEER** changes only the current version and only an approved contract or a correction restoring approved behavior.
4. **AUDITOR** independently executes all validation stages on the complete program after every executable-code modification. Say exactly `COMPILATION NOT YET VERIFIED BY A REAL MQL5 COMPILER` unless a real compiler completed successfully.
5. **SAGE** updates analytical memory and the insight journal after meaningful turns; distinguish OBSERVED, INFERRED, and HYPOTHESIS. Retrieve exact archive text when wording/history matters.
6. For each meaningful change, ARCHITECT records impact analysis and explicitly selects PATCH, REFACTOR, or REBUILD before implementation. Obtain the user's agreement for material behavior or architecture changes.

Use the concise response formats in the workflow reference. Consult the named modular skills below for their specialty.

## State and recovery

- Project state is under `tradepal/`; Git commits are the canonical exact-source history.
- Run `python3 .agents/skills/tradepal/scripts/tradepal_state.py status` to identify the current version and contract state.
- Run `... search --query 'text'` before making claims about past wording when retrieval is needed.
- Record a meaningful executable version only after validation by updating the current-version pointer and ledger, then commit its source.

## Modular TRADEPAL skills

- `../tradepal-requirements/SKILL.md`
- `../tradepal-product-decision/SKILL.md`
- `../tradepal-impact-analysis/SKILL.md`
- `../tradepal-contracting/SKILL.md`
- `../tradepal-mql5-engineering/SKILL.md`
- `../tradepal-validation/SKILL.md`
- `../tradepal-versioning/SKILL.md`
- `../tradepal-research/SKILL.md`
