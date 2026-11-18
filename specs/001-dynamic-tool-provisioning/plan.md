# Implementation Plan: Repository-Guided Dynamic Tool Provisioning

**Branch**: `001-dynamic-tool-provisioning` | **Date**: 2026-11-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-dynamic-tool-provisioning/spec.md`

## Summary

AgentLab will gain a repository-mapping and dynamic-tool-provisioning foundation. A portable
agent skill will let Codex, Cursor, Claude, or another compatible agent configure an analysis
scope, inspect a connected repository, and produce a deterministic application graph. A
separate capability workflow will turn a graph-backed request into a tool proposal with
schemas, permissions, provenance, and validation state. Runtime publication will be modeled
as a versioned artifact and registry operation; it will not execute generated code directly
inside an end-user request.

The initial implementation is intentionally local and provider-neutral. It will generate
JSON graph/proposal artifacts, validate them, and provide a mock runtime contract. Customer
connectors, actual MCP transports, model providers, and production deployment remain behind
interfaces so they can be added without coupling the repository mapper to a particular host.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Python standard library for the mapper core; Pydantic v2 for
contracts when the backend is introduced; FastAPI and an MCP SDK are deferred behind ports.

**Storage**: Versioned JSON artifacts for the foundation; PostgreSQL, object storage, and
search indexes are runtime integration targets, not required by the mapper MVP.

**Testing**: pytest for Python components, contract fixtures for graph/proposal schemas, and
CLI smoke tests using synthetic repositories.

**Target Platform**: Linux/macOS/Windows development environments and Linux runtime services.

**Project Type**: Python monorepo foundation containing a reusable CLI/library, agent skills,
architecture contracts, and future web services.

**Performance Goals**: Analyze a small-to-medium pilot repository deterministically with a
bounded file set; avoid network calls and model calls in the mapper core.

**Constraints**: Never scan excluded paths; never execute repository code; never access
customer credentials; fail closed on invalid scope or malformed artifacts; preserve source
provenance; remain usable from a connected agent terminal.

**Scale/Scope**: One pilot repository, one product scope, one read-only capability, and
synthetic fixtures for the first vertical slice. The design must support multiple products
and customer runtimes later.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Contract-first: PASS. Graph, proposal, artifact, and registry records are explicit JSON
  contracts before runtime adapters are introduced.
- Repository evidence boundary: PASS. The mapper only produces design-time artifacts; the
  runtime contract references approved customer data interfaces.
- Least privilege and isolation: PASS. The first slice is local, read-only, synthetic, and
  has no customer credential access.
- Human-governed publication: PASS. Publication is represented as an explicit lifecycle and
  approval gate; no direct production deployment is implemented.
- Defensive boundaries: PASS. Repository content is treated as data, excluded paths are
  enforced, and repository code is never executed by the mapper.
- Traceability: PASS. Commit, scope hash, analyzer version, graph ID, and proposal ID are
  required provenance fields.
- Incremental delivery: PASS. The feature begins with one bounded repository and a CLI
  vertical slice.

## Project Structure

### Documentation (this feature)

```text
specs/001-dynamic-tool-provisioning/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
agent-lab/
├── AGENTS.md                         # Portable instructions for coding agents
├── agent-instructions/               # Host-specific integration guidance
│   ├── README.md
│   ├── codex.md
│   ├── claude.md
│   └── cursor.md
├── skills/
│   └── repository-mapper/
│       ├── SKILL.md
│       └── references/
├── backend/
│   ├── app/
│   │   ├── capabilities/
│   │   ├── graphs/
│   │   ├── mcp/
│   │   ├── policies/
│   │   ├── provisioning/
│   │   ├── schemas/
│   │   └── services/
│   └── tests/
│       ├── contract/
│       ├── integration/
│       └── unit/
├── packages/
│   └── repository-mapper/
│       ├── src/repository_mapper/
│       └── tests/
├── contracts/
│   ├── repository-scope.schema.json
│   ├── application-graph.schema.json
│   ├── tool-proposal.schema.json
│   └── capability-registry.schema.json
├── configs/
│   └── repository-scope.example.toml
├── examples/
│   └── repository-mapper/
├── evals/
│   ├── datasets/
│   └── reports/
├── docs/
│   ├── architecture/
│   └── adr/
└── specs/
    └── 001-dynamic-tool-provisioning/
```

**Structure Decision**: Use a small Python package for deterministic repository analysis and
separate backend ports for graph, provisioning, policy, and MCP concerns. Agent instructions
and the repository-mapper skill are kept outside the runtime package so different coding
agents can reuse the same workflow. JSON schemas are first-class contracts shared by the
CLI, future API, tests, and generated artifacts.

## Research Decisions

- The mapper uses a configurable scope and does not execute repository code.
- The first graph format is JSON because it is portable across Codex, Cursor, Claude,
  pipelines, and future graph stores.
- The first repository scope format is TOML because Python 3.12 reads it without an extra
  parser dependency.
- MCP is represented through ports and contracts in the foundation. A real remote MCP
  transport is added after identity, policy, and customer connector contracts are tested.
- Runtime tools are versioned artifacts independent from repository availability, with source
  commit and graph provenance retained for drift detection.
- Drift is evaluated before promotion by comparing the current graph identity and source
  commit with proposal provenance; a signal blocks automatic publication but does not mutate
  customer runtimes.

## Complexity Tracking

No constitution violations identified. The package/backend split is a boundary between a
portable analysis library and future runtime services, not a commitment to deploy many
microservices.
