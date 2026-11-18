# Evaluation report: Repository-Guided Dynamic Tool Provisioning

Date: 2026-11-18

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| Scoped mapper scan | PASS | `graph_94e1147fac50da67`, 7 nodes, 7 relationships |
| Graph CLI validation | PASS | `valid` |
| Graph explanation | PASS | 7 nodes, 7 relationships, no errors |
| Mapper unit/integration suite | PASS | 6 tests with `unittest` |
| Backend contract/unit/integration suite | PASS | 18 tests with `unittest` |
| Python compilation | PASS | `compileall-ok` |
| JSON parsing | PASS | Runtime contracts and proposal fixture loaded successfully |
| JSON Schema validation | PASS | Graph and proposal validated with a local schema registry |
| Repository hygiene | PASS | `git diff --check` returned no errors |
| Pytest command | NOT RUN | `pytest` is declared as an optional dependency but is not installed in this environment |

## Observed behavior

- The sample scope includes the product fixture and excludes `framework-core/**`.
- The mapper does not import or execute inspected source files.
- A Spanish request for “notas de curso” resolves to the synthetic `get_course_grades`
  proposal through explicit query aliases; unresolved requests retain assumptions.
- Failed validation prevents approval and unapproved artifacts cannot be published.
- Runtime discovery filters customer, product, environment, active state, and permissions.
- Runtime handlers receive the authenticated `RequestContext`, including the customer ID.
- Audit metadata redacts token/password/authorization-style keys.
- Graph and source-commit mismatches are reported as drift signals.

## Known limits before customer integration

The current slice uses in-memory registry, publisher, runtime, audit sink, and synthetic
data. It does not yet provide a remote MCP SDK adapter, REST server, corporate identity,
secret manager, persistent storage, CI sandbox, or production deployment. Those must be
implemented and security-reviewed before any customer runtime is enabled.
