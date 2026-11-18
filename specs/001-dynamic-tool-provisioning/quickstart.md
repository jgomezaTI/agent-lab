# Quickstart: Repository-Guided Dynamic Tool Provisioning

This guide validates the first foundation without customer credentials, external MCP
servers, or production data.

## Prerequisites

- Python 3.12 or newer.
- Git.
- A checkout of this repository.

## 1. Configure a repository scope

Copy `configs/repository-scope.example.toml` to a local file and point it at a synthetic
fixture or a local pilot repository. Keep generated output outside the source tree or under
an ignored directory.

The scope must include the product identity and at least one path. Excluded paths take
precedence over included paths.

## 2. Run the repository mapper

Run the mapper CLI from the repository root:

```bash
PYTHONPATH=packages/repository-mapper/src \
python -m repository_mapper scan \
  --scope configs/repository-scope.example.toml \
  --repository . \
  --output .agentlab/graph.json
```

Validate and explain it:

```bash
PYTHONPATH=packages/repository-mapper/src python -m repository_mapper validate .agentlab/graph.json
PYTHONPATH=packages/repository-mapper/src python -m repository_mapper explain .agentlab/graph.json
```

The command emits an application graph JSON artifact containing:

- Scope and configuration hash.
- Source commit when available.
- Nodes for discovered files and supported structural entities.
- Relationships between discovered entities.
- Analyzer version and generation timestamp.

The command must not execute files from the inspected repository.

## 3. Validate the graph contract

Validate the generated JSON against
`specs/001-dynamic-tool-provisioning/contracts/application-graph.schema.json`.

The validation must fail if required provenance, node IDs, relationship IDs, or scope fields
are missing. The canonical schemas are under `specs/001-dynamic-tool-provisioning/contracts/`
and their stable runtime copies are under `contracts/`.

## 4. Create a tool proposal fixture

Create a proposal for a read-only capability such as `get_course_grades`. The proposal must
reference graph node IDs, declare an input and output schema, declare permissions, and set
the lifecycle state to `draft` or `review`.

Validate it against
`specs/001-dynamic-tool-provisioning/contracts/tool-proposal.schema.json`.

## 5. Validate registry isolation

Create registry fixtures for two customers using the same tool name but different artifacts.
The registry contract must preserve customer, product, environment, permissions, graph ID,
and source commit. A discovery test must return only the entry matching the caller context.

## 6. Run the agent integration workflow

Open the repository with a compatible coding agent and follow:

- [AGENTS.md](../../AGENTS.md)
- [repository-mapper skill](../../skills/repository-mapper/SKILL.md)
- Host-specific guidance in `agent-instructions/`.

The agent should be able to inspect the repository, apply the configured scope, run the
mapper, explain the resulting graph, and propose the next capability without manually
constructing the graph file.

## Expected boundary

The quickstart intentionally stops before real customer deployment. A future integration
quickstart must add identity, policy, secret management, a mock customer API, a runtime MCP
server, contract tests, and an approval step before any production connector is enabled.
