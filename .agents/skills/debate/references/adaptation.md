# Runtime adaptation

This Codex environment can run named roles as sequential, tool-mediated responsibilities, but it does not expose a runtime control that binds a project custom-agent definition to an individual model invocation or changes model reasoning effort per turn. The project agent definitions therefore preserve role prompts and the controller maps DIRECT/LIGHT/STANDARD/DEEP/MAX to processing depth. The persistent level state, routing classifier, append-only record, retrieval, and validation are executable locally.

Project skills are stored in `.agents/skills/`, the repository-scoped convention used by this workspace. Their `agents/openai.yaml` metadata permits discovery by skill-aware Codex surfaces. The supplied validation script confirms the files and metadata; the currently installed shell does not provide the `codex` CLI, so CLI discovery cannot be tested here.
