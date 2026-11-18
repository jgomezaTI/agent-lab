<!--
Sync Impact Report
Version change: template → 1.0.0
Modified principles: all scaffold placeholders replaced with project principles.
Added sections: Security and governance controls for repository mapping, generated tools,
MCP runtimes, customer isolation, and human approval.
Removed sections: none; the initial scaffold was replaced with the adopted constitution.
Follow-up TODOs: validate the controls against the company's legal, privacy, and security
requirements before production deployment.
-->

# AgentLab Constitution

## Core Principles

### I. Contract-First and Library-First Design

Every capability MUST begin with an explicit contract that defines its inputs, outputs,
permissions, failure modes, and provenance. Domain capabilities SHOULD be implemented as
independently testable modules before they are connected to an agent workflow. MCP, REST,
and internal adapters MUST converge on stable internal contracts so agents are not coupled
to a specific transport or vendor.

Rationale: explicit contracts prevent agents, generated tools, and customer integrations from
becoming inseparable implementations.

### II. Repository Analysis Is Evidence, Not Runtime Authority

Repository mapping, application graphs, and generated code MUST be treated as design-time
evidence. Runtime tools MUST execute against explicitly configured customer APIs, views,
stored procedures, or other approved data interfaces. A production agent MUST NOT depend on
the availability of a source repository in order to answer a request or execute an approved
tool.

Generated artifacts MUST retain source commit, graph version, tool specification, and build
metadata so that runtime behavior remains traceable to its design evidence.

Rationale: repositories describe how a system is built; they are not automatically safe or
authorized runtime data sources.

### III. Least Privilege and Customer Isolation

Every agent, MCP server, tool, connector, and data source MUST have an explicit identity and
minimal permissions. Access MUST be denied by default and evaluated using the authenticated
caller, customer or tenant, product, environment, data classification, and requested action.

Customer data, credentials, indexes, generated artifacts, and audit records MUST remain
isolated unless an explicit cross-customer policy permits sharing. Runtime tools MUST use
parameterized access through approved interfaces and MUST NOT expose arbitrary SQL, file
system access, shell execution, or unrestricted network requests.

Rationale: the tool layer is a security boundary, not only an integration convenience.

### IV. Human-Governed Generation and Publication

An agent MAY propose a new tool, but generated code MUST pass schema validation, automated
tests, security checks, and provenance checks before publication. Tools that write data,
change configuration, access sensitive information, or affect production MUST require an
explicit approval policy and, where configured, human approval.

The runtime support agent MUST NOT directly generate and deploy code in response to an
ordinary end-user request. Provisioning MUST be an observable workflow with draft, review,
approved, published, deprecated, and rejected states.

Rationale: generation speed must not bypass change control or make production behavior
unreviewable.

### V. Untrusted Content and Defensive Agent Boundaries

Repository files, manuals, MCP metadata, API responses, database content, and retrieved
documents MUST be treated as untrusted data. Their content MUST NOT override system
instructions, authorization decisions, safety policies, or approval requirements.

Agent workflows MUST enforce bounded steps, timeouts, retries, budgets, tool allowlists, and
network policies. Tool descriptions and retrieved content MUST be tested for prompt
injection, confused-deputy behavior, data exfiltration, and cross-tool privilege escalation.

Rationale: a trusted connector can still transport hostile or misleading content.

### VI. Traceability, Evaluation, and Reproducibility

Every execution MUST have a trace identifier and record the caller, agent, workflow, tool or
resource, customer, product, input classification, outcome, latency, cost, approvals, and
errors. Secrets and sensitive payloads MUST be redacted according to policy.

Every generated or retrieved capability MUST be testable using reproducible fixtures,
contract tests, evaluation datasets, and security scenarios. Changes to models, prompts,
schemas, connectors, graphs, or policies MUST be attributable to a versioned artifact.

Rationale: an agent system cannot be operated safely if its decisions and data access cannot
be reconstructed.

### VII. Incremental Delivery and Operational Simplicity

The project MUST start with one product, one bounded support workflow, read-only access,
synthetic or sanitized test data, and a complete vertical slice. Additional products,
write actions, multi-agent workflows, and independent MCP servers MUST be added only after
the preceding slice meets its functional, security, and operational acceptance criteria.

The architecture SHOULD prefer a modular monolith and a small number of explicit trust
boundaries until scale, ownership, deployment, or isolation requirements justify further
service separation.

Rationale: a narrow, verifiable slice exposes integration and governance problems before
they multiply across products and customers.

## Security, Data, and Compliance Requirements

- Remote MCP transports MUST use authenticated and authorized connections with audience-
  bound tokens or an equivalent control approved by security.
- Secrets MUST be stored outside source code, generated artifacts, prompts, and ordinary
  logs.
- Customer data MUST be encrypted in transit and at rest according to organizational policy.
- Document and tool access MUST support retention, deletion, versioning, and audit evidence.
- New MCP servers and generated tool packages MUST undergo dependency, provenance, and
  configuration review before being trusted by a runtime host.
- Production actions MUST have rollback or compensating procedures where technically
  possible.
- The implementation MUST maintain a compliance mapping for applicable privacy, security,
  contractual, and sector-specific obligations. This constitution provides engineering
  controls; it does not by itself certify legal or regulatory compliance.

## Development Workflow and Quality Gates

1. Describe the user outcome and boundaries in a feature specification.
2. Record architecture decisions, security assumptions, and integration contracts.
3. Define data models and evaluation scenarios before implementation.
4. Implement the smallest vertical slice with tests and observability.
5. Run unit, contract, integration, security, and evaluation checks appropriate to the
   affected trust boundary.
6. Review generated code and tool permissions before publication.
7. Update documentation, provenance, runbooks, and rollback procedures with the change.

Pull requests and agent-generated changes MUST identify affected products, data classes,
tools, policies, and operational risks. A change that cannot explain its authorization and
audit behavior is not ready for production.

## Governance

This constitution is the highest-level project governance document. Feature specifications,
plans, tasks, code, and generated artifacts MUST conform to it. A lower-level document may
add stricter controls but may not weaken these principles without an explicit amendment.

Amendments require:

1. A written rationale and impact analysis.
2. Review by the project maintainers and the relevant security or privacy owner.
3. Updates to affected templates, specifications, plans, tests, and operational documents.
4. A version increment according to semantic versioning.
5. A migration or rollback plan when existing behavior is affected.

Constitution compliance MUST be reviewed at feature planning, pre-publication, and periodic
operational review points. Emergency changes may use an expedited review, but the rationale,
scope, and retrospective review MUST still be recorded.

**Version**: 1.0.0 | **Ratified**: 2026-11-18 | **Last Amended**: 2026-11-18
