---
description: "Task list for repository-guided dynamic tool provisioning"
---

# Tasks: Repository-Guided Dynamic Tool Provisioning

**Input**: Design documents from `/specs/001-dynamic-tool-provisioning/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included because the constitution requires reproducible contract, security, and
integration validation for generated capabilities.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish a portable Python package, agent entry points, and repository layout.

- [x] T001 Create the Python monorepo structure in `packages/repository-mapper/`, `backend/app/`, `backend/tests/`, `configs/`, `contracts/`, `examples/repository-mapper/`, and `tests/`.
- [x] T002 [P] Add Python project metadata and developer commands in `pyproject.toml` with Python 3.12+, pytest, and an executable `repository-mapper` CLI entry point.
- [x] T003 [P] Add repository scope configuration in `configs/repository-scope.example.toml` with explicit include/exclude examples for a portal product and generic framework code.
- [x] T004 [P] Add portable agent guidance in `AGENTS.md`, `agent-instructions/README.md`, `agent-instructions/codex.md`, `agent-instructions/claude.md`, and `agent-instructions/cursor.md`.
- [x] T005 [P] Add the reusable repository mapper skill in `skills/repository-mapper/SKILL.md` and supporting references in `skills/repository-mapper/references/`.
- [x] T006 Verify `.gitignore` covers Python caches, virtual environments, generated graph artifacts, local scope files, secrets, and test output in `.gitignore`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define contracts and ports that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T007 [P] Add JSON Schema contracts for repository scope, application graph, tool proposal, and capability registry in `specs/001-dynamic-tool-provisioning/contracts/` and mirror stable runtime copies in `contracts/`.
- [x] T008 [P] Implement domain dataclasses and serialization helpers for scope and graph in `packages/repository-mapper/src/repository_mapper/models.py`, plus proposal, artifact, registry, and audit records in the backend domain modules.
- [x] T009 [P] Implement deterministic hashing and provenance helpers in `packages/repository-mapper/src/repository_mapper/provenance.py`.
- [x] T010 [P] Define transport-neutral capability and MCP gateway ports in `backend/app/mcp/ports.py` and `backend/app/capabilities/ports.py`.
- [x] T011 [P] Define lifecycle, policy, and audit service interfaces in `backend/app/provisioning/ports.py`, `backend/app/policies/ports.py`, and `backend/app/audit/ports.py`.
- [x] T012 Add package exports and test fixtures in `packages/repository-mapper/src/repository_mapper/__init__.py`, `packages/repository-mapper/tests/fixtures/`, and `backend/tests/fixtures/`.

**Checkpoint**: Contracts and ports are available without connecting to a customer system.

---

## Phase 3: User Story 1 - Scoped Application Mapping (Priority: P1) 🎯 MVP

**Goal**: Let a compatible coding agent configure a repository scope and produce a
deterministic application graph without executing repository code.

**Independent Test**: Run the CLI against the synthetic fixture and verify scope filtering,
provenance, deterministic IDs, and graph contract validation.

### Tests for User Story 1

- [x] T013 [P] [US1] Add scope loading and validation tests in `packages/repository-mapper/tests/test_scope.py` covering missing roots, exclusions, hidden files, symlinks, and malformed configuration.
- [x] T014 [P] [US1] Add deterministic provenance and graph contract tests in `packages/repository-mapper/tests/test_graph_contract.py`.
- [x] T015 [P] [US1] Add synthetic portal repository fixtures in `examples/repository-mapper/sample-repo/` and expected graph assertions in `packages/repository-mapper/tests/test_mapper_integration.py`.

### Implementation for User Story 1

- [x] T016 [US1] Implement TOML scope loading, default normalization, include/exclude matching, and fail-closed validation in `packages/repository-mapper/src/repository_mapper/scope.py`.
- [x] T017 [US1] Implement safe repository scanning without executing source files in `packages/repository-mapper/src/repository_mapper/scanner.py`.
- [x] T018 [US1] Implement file classification and lightweight structural extraction for modules, configurations, tests, dependencies, and endpoints in `packages/repository-mapper/src/repository_mapper/extractors.py`.
- [x] T019 [US1] Implement deterministic application graph construction and JSON serialization in `packages/repository-mapper/src/repository_mapper/graph.py`.
- [x] T020 [US1] Implement the `repository-mapper` CLI with `scan`, `validate`, and `explain` commands in `packages/repository-mapper/src/repository_mapper/cli.py`.
- [x] T021 [US1] Document the agent-driven mapping workflow and exclusion rules in `skills/repository-mapper/SKILL.md` and `agent-instructions/README.md`.

**Checkpoint**: A coding agent can run one command against a scoped repository and receive a
reproducible graph artifact without manual graph construction.

---

## Phase 4: User Story 2 - Graph-Backed Tool Proposals (Priority: P1)

**Goal**: Convert a capability request into a validated tool proposal with graph references,
permissions, data sources, and unresolved assumptions.

**Independent Test**: Given the MVP graph, create a read-only `get_course_grades` proposal,
validate it, and reject a proposal without graph evidence.

### Tests for User Story 2

- [x] T022 [P] [US2] Add tool proposal schema and lifecycle validation tests in `backend/tests/contract/test_tool_proposal.py`.
- [x] T023 [P] [US2] Add graph evidence matching tests in `backend/tests/unit/test_proposal_builder.py`.

### Implementation for User Story 2

- [x] T024 [US2] Implement proposal models, lifecycle states, and schema validation in `backend/app/provisioning/models.py`.
- [x] T025 [US2] Implement graph evidence lookup and capability proposal construction in `backend/app/provisioning/proposal_builder.py`.
- [x] T026 [US2] Implement missing-evidence and unresolved-assumption handling in `backend/app/provisioning/validation.py`.
- [x] T027 [US2] Add the `get_course_grades` synthetic proposal example in `examples/repository-mapper/tool-proposal.json`.

**Checkpoint**: The system can explain why a proposed tool is supported, incomplete, or
rejected before any code generation or runtime publication.

---

## Phase 5: User Story 3 - Validated and Versioned Publication (Priority: P1)

**Goal**: Model artifact validation, approval, publication, and deprecation without touching
production systems.

**Independent Test**: A valid synthetic artifact can move to approved/published in a mock
runtime, while an invalid or unapproved artifact cannot.

### Tests for User Story 3

- [x] T028 [P] [US3] Add artifact check and lifecycle tests in `backend/tests/unit/test_artifact_lifecycle.py`.
- [x] T029 [P] [US3] Add mock publication contract tests in `backend/tests/contract/test_publication.py`.

### Implementation for User Story 3

- [x] T030 [US3] Implement generated artifact manifests and validation results in `backend/app/provisioning/artifacts.py`.
- [x] T031 [US3] Implement an in-memory capability registry with customer/product/environment filtering in `backend/app/capabilities/registry.py`.
- [x] T032 [US3] Implement approval and publication transitions with fail-closed rules in `backend/app/provisioning/publisher.py`.
- [x] T033 [US3] Implement mock runtime deployment records in `backend/app/mcp/mock_runtime.py`.
- [x] T034 [US3] Add source commit, graph ID, proposal ID, package digest, lifecycle, and approval metadata to publication artifacts through `backend/app/provisioning/models.py` and `backend/app/provisioning/provenance.py`.

**Checkpoint**: Only approved, versioned artifacts are discoverable in the mock runtime.

---

## Phase 6: User Story 4 - Runtime Discovery and Consumption (Priority: P1)

**Goal**: Give a runtime agent a transport-neutral way to discover and invoke an authorized
tool while keeping repository code outside the runtime path.

**Independent Test**: An authorized request discovers and invokes a mock read-only capability;
an unauthorized request is filtered or rejected before data access.

### Tests for User Story 4

- [x] T035 [P] [US4] Add capability discovery filtering tests in `backend/tests/unit/test_capability_discovery.py`.
- [x] T036 [P] [US4] Add mock runtime invocation tests in `backend/tests/integration/test_runtime_invocation.py`.

### Implementation for User Story 4

- [x] T037 [US4] Implement capability discovery and invocation interfaces in `backend/app/capabilities/service.py`.
- [x] T038 [US4] Implement a policy-aware mock MCP gateway adapter in `backend/app/mcp/mock_gateway.py`.
- [x] T039 [US4] Implement synthetic customer data access through an approved read-only repository in `backend/app/services/synthetic_customer_data.py`.
- [x] T040 [US4] Add the runtime sequence and agent handoff documentation in `docs/architecture/dynamic-tool-provisioning.md`.

**Checkpoint**: Runtime consumption works from the registry and mock customer interface,
without importing the repository mapper into the support agent.

---

## Phase 7: User Story 5 - Isolation and Auditability (Priority: P1)

**Goal**: Enforce caller/customer context and produce redacted audit events for provisioning
and runtime actions.

**Independent Test**: Two customer contexts cannot read one another's registry or synthetic
data, and every allowed/denied invocation produces a traceable redacted audit event.

### Tests for User Story 5

- [x] T041 [P] [US5] Add customer/product/environment isolation tests in `backend/tests/unit/test_policy_isolation.py`.
- [x] T042 [P] [US5] Add redaction and audit event tests in `backend/tests/unit/test_audit.py`.

### Implementation for User Story 5

- [x] T043 [US5] Implement request context and deny-by-default policy evaluation in `backend/app/policies/context.py` and `backend/app/policies/engine.py`.
- [x] T044 [US5] Implement redacted audit event creation in `backend/app/audit/events.py`.
- [x] T045 [US5] Integrate policy and audit checks into proposal, publication, discovery, and invocation paths in `backend/app/services/guarded_operations.py` and `backend/app/services/audited_workflow.py`.
- [x] T046 [US5] Document the security boundary, trusted inputs, and non-goals in `docs/architecture/security-boundaries.md`.

**Checkpoint**: The foundation demonstrates isolation and traceability before any real
customer connector is introduced.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Make the foundation usable by other agents and maintainable by the project.

- [x] T047 [P] Update `README.md` with the new repository-mapper workflow, artifact locations, and quickstart links.
- [x] T048 [P] Add architecture decisions for scoped mapping, runtime separation, and generated artifact publication in `docs/adr/`.
- [x] T049 Run the validation flow from `specs/001-dynamic-tool-provisioning/quickstart.md` and record expected outputs in `evals/reports/001-dynamic-tool-provisioning.md`.
- [ ] T050 Run pytest, JSON Schema validation, CLI smoke tests, and repository hygiene checks; document results in `evals/reports/001-dynamic-tool-provisioning.md`.
- [x] T051 Review all generated artifacts and instructions for secrets, arbitrary SQL, unrestricted filesystem access, and direct production publication paths.
- [x] T052 [US3] Add drift detection for graph and source-commit changes before promotion in `backend/app/provisioning/drift.py`.

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks all user stories.
- **Phase 3 User Story 1**: Depends on Phase 2 and is the MVP mapping slice.
- **Phase 4 User Story 2**: Depends on the graph contract from US1, but proposal validation can be tested independently with fixtures.
- **Phase 5 User Story 3**: Depends on proposal contracts and registry contracts.
- **Phase 6 User Story 4**: Depends on the registry and mock runtime from US3.
- **Phase 7 User Story 5**: Cross-cuts US2-US4 and must be complete before real customer integration.
- **Phase 8 Polish**: Depends on all desired slices.

### User Story Dependencies

- **US1**: Starts after Phase 2; no story dependency.
- **US2**: Uses US1 graph artifacts; can use checked-in fixtures while US1 is under development.
- **US3**: Uses US2 proposal artifacts.
- **US4**: Uses US3 registry and deployment records.
- **US5**: Can be developed in parallel after Phase 2 but must gate runtime integration.

### Parallel Opportunities

- T002-T005 can run in parallel after the directory layout exists.
- T007-T011 can run in parallel because they create separate contracts and ports.
- T013-T015 can run in parallel before US1 implementation.
- T022-T023, T028-T029, T035-T036, and T041-T042 can each run in parallel.
- T047-T048 can run in parallel with the final validation phase.

## Implementation Strategy

### MVP First

1. Complete setup and contracts.
2. Implement the scoped mapper and deterministic graph CLI.
3. Validate the graph against the synthetic repository fixture.
4. Stop and review the graph shape before adding generated-tool publication.

### Incremental Delivery

1. Add graph-backed proposals.
2. Add versioned artifacts and mock publication.
3. Add runtime discovery and invocation.
4. Add policy isolation and audit.
5. Only then design real customer connectors and remote MCP transport.

### Completion Boundary

This feature is complete when the foundation supports a repeatable local flow from scoped
repository analysis to an approved mock runtime capability, with contracts, tests, agent
instructions, provenance, and audit behavior. Production deployment and customer credentials
remain intentionally outside this first implementation.
