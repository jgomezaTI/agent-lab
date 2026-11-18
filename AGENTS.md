# AgentLab instructions

AgentLab is building a repository-guided capability provisioning platform. Treat the
repository mapper as a design-time analysis tool and the MCP/customer runtime as a separate
execution boundary.

## Before changing code

1. Read the relevant feature specification under `specs/`.
2. Read `.specify/memory/constitution.md`.
3. Inspect `docs/marco-teorico.md` and `docs/roadmap.md` when working on architecture.
4. Preserve customer isolation, provenance, deny-by-default policy, and human publication
   gates.

## Repository mapping

Use the portable skill in `skills/repository-mapper/SKILL.md`. Start from a scoped
configuration and run the mapper without executing code from the inspected repository:

```bash
PYTHONPATH=packages/repository-mapper/src \
python -m repository_mapper scan \
  --scope configs/repository-scope.example.toml \
  --repository . \
  --output .agentlab/graph.json
```

Never remove exclusions merely to increase graph coverage. Explain any scope change in the
resulting artifact or feature plan.

## Generated tools

Generated tools are proposals until they pass contract, security, provenance, and approval
checks. Do not add arbitrary SQL, unrestricted filesystem access, shell execution, or
production credentials to generated code. Runtime tools must use approved customer APIs,
read-only views, stored procedures, or parameterized repositories.

## Agent host compatibility

The canonical workflow is documented in `agent-instructions/`. Keep instructions portable so
Codex, Cursor, Claude, and other agents can follow the same repository scope and artifact
contracts.
