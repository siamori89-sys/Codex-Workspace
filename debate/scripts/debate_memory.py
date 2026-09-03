#!/usr/bin/env python3
"""Persistent storage and deterministic routing helpers for the DEBATE workflow."""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / "debate" / "memory"
FULL = MEMORY / "full-record"
STRUCTURED = MEMORY / "structured"
STATE = STRUCTURED / "state.json"
INDEX = STRUCTURED / "index.jsonl"

MAX_PATTERNS = ("proof", "argument", "therefore", "because", "objection", "object", "disagree", "contradict", "counterexample", "assumption", "previous conclusion", "does not follow")
LEVELS = ("DIRECT", "LIGHT", "STANDARD", "DEEP", "MAX")

def now(): return datetime.now(timezone.utc).isoformat()
def init():
    FULL.mkdir(parents=True, exist_ok=True); STRUCTURED.mkdir(parents=True, exist_ok=True)
    if not STATE.exists(): STATE.write_text(json.dumps({"active": False, "persistent_level": None}, indent=2) + "\n")
def state(): init(); return json.loads(STATE.read_text())
def save_state(value): init(); STATE.write_text(json.dumps(value, indent=2) + "\n")
def tokens(text): return set(re.findall(r"[a-z0-9][a-z0-9-]*", text.lower()))
def next_id(prefix, path):
    count = sum(1 for _ in path.open()) if path.exists() else 0
    return f"{prefix}-{count + 1:06d}"
def append(kind, text, role, metadata):
    init(); day = datetime.now(timezone.utc).strftime("%Y-%m")
    path = FULL / f"{day}.jsonl"; event_id = next_id("EV", path)
    item = {"id": event_id, "timestamp": now(), "kind": kind, "role": role, "text": text, "metadata": metadata}
    with path.open("a") as f: f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return item
def index_item(item_type, summary, event_id, tags):
    init(); item = {"id": next_id("MEM", INDEX), "timestamp": now(), "type": item_type, "summary": summary, "event_id": event_id, "tags": tags}
    with INDEX.open("a") as f: f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return item
def route(text):
    lower = text.lower()
    override = re.search(r"\b(?:use|think at|think with)\s+(direct|light|standard|deep|max)\b|\b(max)\s+thinking\b|\bthink harder\b|\bmaximum reasoning\b", lower)
    requested = (override.group(1) or override.group(2) or ("max" if override else None)) if override else None
    persistent = bool(re.search(r"\b(until i say otherwise|for the rest of (?:this )?discussion|remain active)\b", lower))
    if requested: return {"level": requested.upper(), "source": "user_override", "persistent": persistent}
    if any(p in lower for p in MAX_PATTERNS): return {"level": "MAX", "source": "automatic_max", "persistent": False}
    if re.fullmatch(r"\s*(hi|hello|thanks|thank you|continue|ok|okay)[!. ]*\s*", lower) or "format" in lower: return {"level": "DIRECT", "source": "automatic", "persistent": False}
    if any(p in lower for p in ("define", "definition", "simple example", "clarify")): return {"level": "LIGHT", "source": "automatic", "persistent": False}
    if any(p in lower for p in ("compare", "interpret", "why does", "connect", "relationship")): return {"level": "STANDARD", "source": "automatic", "persistent": False}
    return {"level": "DEEP", "source": "automatic", "persistent": False}
def retrieve(query, limit):
    query_tokens = tokens(query); results=[]
    if not INDEX.exists(): return results
    for line in INDEX.read_text().splitlines():
        item=json.loads(line); hay=tokens(item["summary"] + " " + " ".join(item.get("tags", [])))
        score=len(query_tokens & hay)
        if score: results.append((score,item))
    return [item for _,item in sorted(results, key=lambda x:(-x[0], x[1]["id"]))[:limit]]
def cmd_init(_): init(); print(json.dumps(state()))
def cmd_activate(args): s=state(); s["active"]=args.active; save_state(s); print(json.dumps(s))
def cmd_level(args): s=state(); s["persistent_level"]=None if args.level == "CANCEL" else args.level; save_state(s); print(json.dumps(s))
def cmd_record(args):
    item=append(args.kind,args.text,args.role,{"substantive":args.substantive}); print(json.dumps(item))
def cmd_index(args): print(json.dumps(index_item(args.type,args.summary,args.event_id,args.tag)))
def cmd_retrieve(args): print(json.dumps(retrieve(args.query,args.limit), ensure_ascii=False))
def cmd_route(args):
    decision=route(args.text); s=state()
    if not decision["source"] == "user_override" and s.get("persistent_level"): decision={"level":s["persistent_level"],"source":"persistent_user_override","persistent":True}
    if decision["source"] == "user_override" and decision["persistent"]: s["persistent_level"]=decision["level"]; save_state(s)
    print(json.dumps(decision))
def parser():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(required=True)
    x=sub.add_parser("init"); x.set_defaults(func=cmd_init)
    x=sub.add_parser("activate"); x.add_argument("active", type=lambda v:v.lower()=="true"); x.set_defaults(func=cmd_activate)
    x=sub.add_parser("level"); x.add_argument("level", choices=(*LEVELS,"CANCEL")); x.set_defaults(func=cmd_level)
    x=sub.add_parser("record"); x.add_argument("kind", choices=("user","assistant")); x.add_argument("text"); x.add_argument("--role", default="TYPIST"); x.add_argument("--substantive", action="store_true"); x.set_defaults(func=cmd_record)
    x=sub.add_parser("index"); x.add_argument("type"); x.add_argument("summary"); x.add_argument("event_id"); x.add_argument("--tag", action="append", default=[]); x.set_defaults(func=cmd_index)
    x=sub.add_parser("retrieve"); x.add_argument("query"); x.add_argument("--limit", type=int, default=8); x.set_defaults(func=cmd_retrieve)
    x=sub.add_parser("route"); x.add_argument("text"); x.set_defaults(func=cmd_route)
    return p
if __name__ == "__main__":
    args=parser().parse_args(); args.func(args)
