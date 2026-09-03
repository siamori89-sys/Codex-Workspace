# DEBATE workflow contract

## Activation and levels

DEBATE activates only after `START DEBATE` or an explicit DEBATE invocation and ends at `STOP DEBATE`. `USE DIRECT`, `USE LIGHT`, `USE STANDARD`, `USE DEEP`, `USE MAX`, and unmistakable equivalents override routing for the current turn. A command that says it persists (for example, `USE MAX UNTIL I SAY OTHERWISE`) is stored until changed or cancelled. Explicit lower levels are honored unless they prevent a safe or valid answer.

## Roles and turn order

1. **TYPIST / READING:** faithfully intake text and commands without substantive thought.
2. **MEMO / RECORD:** append substantive incoming text before extended processing.
3. **DISPATCHER / ROUTING:** select DIRECT, LIGHT, STANDARD, DEEP, or MAX; direct turns need no BRAIN work.
4. **MEMO / RETRIEVAL:** select relevant structured items, then exact full-record text if needed.
5. **BRAIN / THINKING:** work at the assigned level and use UPLOOKING before criticizing a user position.
6. **MEMO / DOWNLOOKING:** check the inspectable proposal against the user text, memory, book material, sources, assumptions, alternatives, and confidence.
7. **BRAIN ↔ MEMO:** resolve material objections: normally one brief pass for LIGHT/STANDARD; further passes only where material for DEEP/MAX.
8. **TYPIST / REPLYING:** send the shortest useful answer and concise audit.
9. **MEMO / UPDATE:** append the final reply and index new claims, objections, conclusions, corrections, agreements, disagreements, and unresolved matters.

## Routing rule

Automatic MAX is mandatory for substantive proofs, logical arguments, reasoned agreements, objections, disagreements, contradiction claims, counterexamples, challenges to assumptions or previous conclusions, important argument modifications, difficult entailment questions, and central interconnected arguments. When substantive logic makes two levels plausible, select the higher one.

## Memory model

`debate/memory/full-record/` holds chronological, append-only, chunked JSONL. `debate/memory/structured/` holds `index.jsonl` plus state. Every structured item references its full-record event ID. The memory command retrieves a bounded number of matching items before BRAIN work; full-record retrieval is explicit and targeted. Corrections are new events/items and never mutate old material.
