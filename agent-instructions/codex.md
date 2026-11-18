# Codex workflow

From the repository root, ask Codex to:

```text
Read AGENTS.md and the active feature specification. Inspect the configured repository scope,
run the repository-mapper skill, validate the graph, and explain which graph nodes support the
requested capability. Do not execute inspected repository code or publish a runtime tool.
```

Use the skill at `skills/repository-mapper/SKILL.md` and preserve all generated
artifacts under `.agentlab/` or another ignored directory.
