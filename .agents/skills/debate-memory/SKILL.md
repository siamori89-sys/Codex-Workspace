---
name: debate-memory
description: Maintain and selectively retrieve DEBATE's persistent append-only full record and structured intellectual index for a long-running book discussion.
---

# DEBATE MEMORY

Use `debate/scripts/debate_memory.py`. Record every substantive user message before extended work and every final reply after responding. The full record is append-only, chunked JSONL. The structured index is JSONL with stable IDs for definitions, claims, arguments, objections, conclusions, corrections, unresolved questions, sources, and relationships. Retrieve structured matches first; retrieve full-record excerpts only when exact wording or sequence matters. Never silently rewrite history; record corrections as new items.
