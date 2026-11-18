# Agent host integration

AgentLab exposes a host-neutral workflow. The repository is the input to the mapper; the
generated graph and proposal artifacts are the handoff between a coding agent and the
AgentLab provisioning pipeline.

## Common workflow

1. Read `AGENTS.md` and the active feature specification.
2. Select or create a scope file under `configs/`.
3. Run the repository mapper.
4. Validate and explain the graph.
5. Use graph node IDs when proposing a capability.
6. Never publish generated code directly from an end-user interaction.

The host-specific files in this directory are prompts and operating guidance, not credentials
or runtime configuration. The reusable skill itself lives at `skills/repository-mapper/` so it
can be copied or registered by the host agent without depending on this repository's private
Codex installation.
