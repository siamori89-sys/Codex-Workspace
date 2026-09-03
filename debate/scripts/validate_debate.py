#!/usr/bin/env python3
"""Validate DEBATE project artifacts and run isolated workflow simulations."""
from __future__ import annotations
import importlib.util, json, shutil, subprocess, sys, tempfile, tomllib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SKILLS = ["debate", "debate-reading", "debate-routing", "debate-thinking", "debate-memory", "debate-replying"]
AGENTS = ["typist", "dispatcher", "brain", "memo"]
VALIDATOR = Path("/opt/codex/skills/.system/skill-creator/scripts/quick_validate.py")

def ok(condition, label):
    if not condition: raise AssertionError(label)
    print(f"PASS {label}")
def main():
    for skill in SKILLS:
        folder=ROOT/".agents/skills"/skill
        result=subprocess.run([sys.executable, str(VALIDATOR), str(folder)], text=True, capture_output=True)
        ok(result.returncode == 0, f"skill valid: {skill}: {result.stdout.strip()}")
        ok((folder/"agents/openai.yaml").exists(), f"skill discoverability metadata: {skill}")
    for agent in AGENTS:
        data=tomllib.loads((ROOT/".codex/agents"/f"{agent}.toml").read_text())
        ok(data["name"] == agent.upper() and bool(data["developer_instructions"]), f"agent definition valid: {agent}")
    spec=importlib.util.spec_from_file_location("memory", ROOT/"debate/scripts/debate_memory.py")
    memory=importlib.util.module_from_spec(spec); spec.loader.exec_module(memory)
    with tempfile.TemporaryDirectory() as temp:
        old=(memory.MEMORY,memory.FULL,memory.STRUCTURED,memory.STATE,memory.INDEX)
        memory.MEMORY=Path(temp)/"memory"; memory.FULL=memory.MEMORY/"full-record"; memory.STRUCTURED=memory.MEMORY/"structured"; memory.STATE=memory.STRUCTURED/"state.json"; memory.INDEX=memory.STRUCTURED/"index.jsonl"
        memory.init()
        incoming=memory.append("user", "If P then Q. P. Therefore Q.", "TYPIST", {"substantive":True})
        indexed=memory.index_item("argument", "modus ponens proof", incoming["id"], ["P", "Q"])
        ok(memory.retrieve("proof P Q", 4)[0]["id"] == indexed["id"], "structured memory writes and retrieves")
        decision=memory.route("If P then Q. P. Therefore Q.")
        ok(decision["level"] == "MAX" and decision["source"] == "automatic_max", "automatic MAX for proof")
        for prompt in ["I object to the conclusion.", "I disagree because premise P is false.", "This contradicts definition D.", "Here is a counterexample.", "Your previous conclusion is wrong because it assumes P."]:
            ok(memory.route(prompt)["level"] == "MAX", f"automatic MAX: {prompt[:20]}")
        override=memory.route("USE MAX. Explain this definition.")
        ok(override["level"] == "MAX" and override["source"] == "user_override", "one-turn USE MAX override")
        persistent=memory.route("USE MAX UNTIL I SAY OTHERWISE")
        saved=memory.state()
        if persistent["persistent"]: saved["persistent_level"] = persistent["level"]; memory.save_state(saved)
        ok(persistent["persistent"] and memory.state()["persistent_level"] == "MAX", "persistent USE MAX override")
        routed=memory.route("Explain the definition.")
        if memory.state()["persistent_level"] and routed["source"] != "user_override": routed={"level":memory.state()["persistent_level"],"source":"persistent_user_override"}
        ok(routed["source"] == "persistent_user_override", "persistent override is respected")
        saved["persistent_level"] = None; memory.save_state(saved)
        # Simulated TYPIST -> DISPATCHER -> BRAIN -> MEMO -> BRAIN -> TYPIST.
        proposal={"conclusion":"Q follows if both stated premises are accepted.","premises":["If P then Q","P"],"confidence":10}
        objection="No objection: the conclusion is conditional on the supplied premises."
        reply="Answer: Q follows if both premises are accepted. BRAIN ↔ MEMO: no material objection. Basis: USER, REASONING. Confidence: 10/10."
        final=memory.append("assistant", reply, "TYPIST", {"simulation":True,"brain":proposal,"memo":objection})
        ok(final["role"] == "TYPIST" and "Confidence" in final["text"], "isolated full-record simulated workflow")
        memory.STATE=old[3]; memory.INDEX=old[4]; memory.MEMORY,memory.FULL,memory.STRUCTURED=old[:3]
    ok(not any((ROOT/"debate/memory/full-record").glob("*.jsonl")), "simulations did not pollute live full record")
    print("ALL DEBATE VALIDATION TESTS PASSED")
if __name__ == "__main__": main()
