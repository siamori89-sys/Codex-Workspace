#!/usr/bin/env python3
"""Deterministic persistence utilities for the repository-local TRADEPAL workflow."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STATE = ROOT / "tradepal" / "state"
ARCHIVE = ROOT / "tradepal" / "sage" / "archive"
SIM = ROOT / "tradepal" / "simulations"
STATE_FILES = {
    "current-specification.md": "# Current specification\n\nNo product requirements have been supplied. TRADEPAL is inactive until `START TRADEPAL`.\n",
    "current-contract.md": "# Current contract\n\nStatus: **NOT PROPOSED**. No MQL5 implementation is authorized.\n",
    "current-version.md": "# Current version\n\n`NONE` — no TRADEPAL executable source version exists.\n",
    "open-questions.md": "# Open questions\n\n- No active project questions.\n",
    "feedback-log.md": "# Feedback log\n\nNo project feedback recorded.\n",
    "version-ledger.md": "# Version ledger\n\nNo executable TRADEPAL version exists. Exact future source is preserved in Git.\n",
    "research-notes.md": "# Research notes\n\nNo research recorded.\n",
}
SAGE_FILES = {
    "analytical-memory.md": "# SAGE analytical memory\n\n## Project status\n- OBSERVED: TRADEPAL is installed but inactive; no Indicator or EA has been designed.\n",
    "insight-journal.md": "# SAGE experiment / insight journal\n\nNo project experiments or insights recorded.\n",
}

def stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")

def initialize() -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    SIM.mkdir(parents=True, exist_ok=True)
    for name, content in STATE_FILES.items():
        (STATE / name).touch(exist_ok=True)
        if not (STATE / name).read_text().strip():
            (STATE / name).write_text(content)
    for name, content in SAGE_FILES.items():
        path = ROOT / "tradepal" / "sage" / name
        path.touch(exist_ok=True)
        if not path.read_text().strip():
            path.write_text(content)
    chunk = ARCHIVE / "0001.jsonl"
    chunk.touch(exist_ok=True)

def append_event(role: str, text: str, simulation: bool = False) -> dict:
    initialize()
    target = (SIM / "archive.jsonl") if simulation else (ARCHIVE / "0001.jsonl")
    event = {"id": f"{target.stem}-{stamp()}", "timestamp": stamp(), "role": role.upper(), "text": text}
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event

def search(query: str, simulation: bool = False) -> int:
    folder = SIM if simulation else ARCHIVE
    hits = 0
    for path in sorted(folder.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            if query.casefold() in event["text"].casefold():
                print(f"{path.relative_to(ROOT)}:{event['id']}:{event['role']}: {event['text']}")
                hits += 1
    return hits

def validate() -> int:
    initialize()
    required_skills = ["tradepal", "tradepal-requirements", "tradepal-product-decision", "tradepal-impact-analysis", "tradepal-contracting", "tradepal-mql5-engineering", "tradepal-validation", "tradepal-versioning", "tradepal-research"]
    missing = [name for name in required_skills if not (ROOT / ".agents" / "skills" / name / "SKILL.md").is_file()]
    required_roles = ["ARCHITECT", "ENGINEER", "AUDITOR", "SAGE"]
    workflow = (ROOT / ".agents" / "skills" / "tradepal" / "references" / "workflow.md").read_text()
    absent_roles = [role for role in required_roles if role not in workflow]
    absent_state = [name for name in STATE_FILES if not (STATE / name).is_file()]
    archive_ok = (ARCHIVE / "0001.jsonl").is_file()
    compiler = next((shutil.which(name) for name in ("metaeditor64", "metaeditor", "MetaEditor64.exe", "MetaEditor.exe", "mql5compiler") if shutil.which(name)), None)
    report = {
        "skills": not missing, "roles": not absent_roles, "state": not absent_state,
        "archive": archive_ok, "mql5_compiler": compiler, "multi_agent_execution": True,
        "single_process_role_emulation": True,
    }
    print(json.dumps(report, indent=2))
    return 1 if missing or absent_roles or absent_state or not archive_ok else 0

def simulate() -> int:
    initialize()
    for path in SIM.glob("*"):
        path.unlink()
    append_event("USER", "I want arrows showing a moving-average crossover.", True)
    append_event("ARCHITECT", "Discovery: visualization suggests an Indicator; contract awaits approval.", True)
    append_event("USER", "I approve the indicator contract.", True)
    append_event("ENGINEER", "Simulated build: crossover indicator version sim-v1.", True)
    append_event("AUDITOR", "Simulated validation: static checks passed; real compilation unavailable.", True)
    append_event("USER", "The arrows are too noisy; add a trend filter.", True)
    append_event("SAGE", "OBSERVED: user values signal selectivity over unfiltered crossover frequency.", True)
    append_event("ARCHITECT", "Impact: PATCH; updated contract awaits approval for trend filter.", True)
    append_event("USER", "I approve the updated contract.", True)
    append_event("ENGINEER", "Simulated build: trend-filtered version sim-v2.", True)
    append_event("AUDITOR", "Simulated validation: complete-program static review passed; real compilation unavailable.", True)
    (SIM / "sim-v1.mq5").write_text("// simulated historical source v1\n")
    (SIM / "sim-v2.mq5").write_text("// simulated current source v2\n")
    (SIM / "version-ledger.md").write_text("# Simulation ledger\n\n- sim-v1: approved initial Indicator build.\n- sim-v2: PATCH trend filter after feedback.\n")
    (SIM / "current-version.md").write_text("sim-v2\n")
    checks = [
        search("too noisy", True) == 1,
        "sim-v2" in (SIM / "current-version.md").read_text(),
        "sim-v1" in (SIM / "version-ledger.md").read_text(),
        (SIM / "sim-v1.mq5").is_file(),
        "awaits approval" in (SIM / "archive.jsonl").read_text(),
    ]
    print(json.dumps({"simulation_checks": checks, "passed": all(checks)}))
    return 0 if all(checks) else 1

def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    add = sub.add_parser("append")
    add.add_argument("--role", required=True, choices=["user", "architect", "engineer", "auditor", "sage", "assistant"])
    add.add_argument("--text", required=True)
    find = sub.add_parser("search")
    find.add_argument("--query", required=True)
    sub.add_parser("status")
    sub.add_parser("validate")
    sub.add_parser("simulate")
    args = parser.parse_args()
    if args.command == "init": initialize(); return 0
    if args.command == "append": print(json.dumps(append_event(args.role, args.text))); return 0
    if args.command == "search": return 0 if search(args.query) else 1
    if args.command == "validate": return validate()
    if args.command == "simulate": return simulate()
    initialize()
    print((STATE / "current-version.md").read_text().strip())
    print((STATE / "current-contract.md").read_text().strip())
    return 0

if __name__ == "__main__":
    sys.exit(main())
