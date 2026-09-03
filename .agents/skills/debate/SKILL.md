---
name: debate
description: Run the explicitly invoked DEBATE workflow for a long-running, difficult book discussion. Use only after the user says START DEBATE or otherwise explicitly invokes DEBATE; do not apply it to unrelated work.
---

# DEBATE controller

Activate on `START DEBATE` or an unmistakable explicit invocation; deactivate on `STOP DEBATE`. While active, use the component skills in this order: `$debate-reading`, `$debate-memory`, `$debate-routing`, `$debate-thinking`, `$debate-memory`, `$debate-replying`, `$debate-memory`.

Keep activation and persistent thinking-level state in `debate/memory/structured/state.json`. Use `debate/scripts/debate_memory.py` for records, retrieval, routing, and state changes. Read `references/workflow.md` for the complete contract and `references/adaptation.md` for runtime limitations.

Never begin a book discussion while setting up this system. Preserve incoming substantive text before extended work; keep the full record append-only; retrieve structured memory before full-record excerpts. Use named roles TYPIST, DISPATCHER, BRAIN, and MEMO even when one runtime agent emulates them sequentially.
