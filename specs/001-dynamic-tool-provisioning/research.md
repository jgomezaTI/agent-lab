# Research: Repository-Guided Dynamic Tool Provisioning

## Decision 1: Separate design-time provisioning from runtime execution

**Decision**: The repository mapper, graph builder, proposal generator, validation pipeline,
and publication workflow are design-time/control-plane capabilities. Runtime agents consume
only approved, versioned tools from a customer or domain runtime.

**Rationale**: This preserves the constitution's boundary that repositories and generated
graphs are evidence, not runtime authority. It prevents an ordinary support request from
turning into an unreviewed production deployment.

**Alternatives considered**:

- Generate and deploy synchronously during the user request: rejected because it combines
  untrusted input, code generation, credentials, and production change control in one path.
- Run every tool directly from the source repository: rejected because runtime behavior would
  depend on repository availability and would bypass artifact provenance.

## Decision 2: Use a configurable repository scope

**Decision**: Repository analysis starts from a TOML scope file with explicit roots, include
patterns, exclude patterns, product metadata, and analysis options.

**Rationale**: A customer repository may contain frameworks, vendored code, generated files,
and unrelated products. Scope must be explicit, reviewable, reproducible, and usable by any
agent host.

**Alternatives considered**:

- Scan the complete repository: rejected because it creates noise and can expose unrelated
  or sensitive code.
- Ask the agent to decide the scope implicitly: rejected because the result would be harder
  to reproduce and review.

## Decision 3: Use portable JSON artifacts for the first graph and contracts

**Decision**: The first implementation emits JSON graph, proposal, artifact, registry, and
audit fixtures validated by JSON Schema. A graph database or search index can be introduced
behind a port later.

**Rationale**: JSON is portable across Codex, Cursor, Claude, CI jobs, and future services.
It also keeps the first vertical slice dependency-light and easy to inspect in a pull request.

**Alternatives considered**:

- Start with Neo4j or another graph database: deferred until graph queries and scale justify
  operational complexity.
- Store only prose documentation: rejected because agents and validators need stable node,
  relationship, and provenance identifiers.

## Decision 4: Keep MCP behind a transport-neutral gateway

**Decision**: AgentLab will expose a stable internal capability contract and later provide
MCP and REST adapters. The mapper core will not depend on a particular MCP SDK or customer
transport.

**Rationale**: The same capability may be consumed by different hosts and customers. A
transport-neutral boundary also keeps repository analysis usable offline.

The MCP specification defines tools that can be discovered and invoked by language models and
resources that can expose contextual data. The set of tools or resources may vary based on
the authorization presented for a request, so authorization belongs at the runtime boundary,
not only in the agent prompt.

**References**:

- [MCP specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/index.mdx)
- [MCP tools](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/tools.mdx)
- [MCP resources](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/resources.mdx)
- [MCP authorization security considerations](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/security-considerations.mdx)

## Decision 5: Use an explicit lifecycle for generated capabilities

**Decision**: A capability moves through `draft`, `validation_failed`, `review`, `approved`,
`published`, `deprecated`, or `rejected`. Publication requires validation and approval.

**Rationale**: The lifecycle gives humans and automation clear control points and lets the
registry prevent incomplete or stale tools from being discovered.

## Decision 6: Start with read-only synthetic validation

**Decision**: The first vertical slice supports a read-only capability against a mock or
sanitized runtime. Write operations and production connectors remain extension points.

**Rationale**: This follows the incremental-delivery principle and allows the complete
provisioning flow to be tested without customer credentials or irreversible actions.
