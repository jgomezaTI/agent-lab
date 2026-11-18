# Data Model: Repository-Guided Dynamic Tool Provisioning

## RepositoryScope

Defines the part of a repository that an agent may inspect.

| Field | Type | Rules |
|---|---|---|
| `scope_id` | string | Stable identifier for the scope configuration |
| `repository_root` | string | Absolute path at execution time; never serialized as a secret |
| `product_id` | string | Required product identifier |
| `environment` | enum | `local`, `sandbox`, `staging`, or `production` |
| `include` | array[string] | At least one effective include root is required |
| `exclude` | array[string] | Exclusions take precedence over inclusions |
| `languages` | array[string] | Optional analysis hints |
| `ignore_hidden` | boolean | Defaults to `true` |
| `analyzer_version` | string | Required provenance field |
| `configuration_hash` | string | Hash of normalized scope configuration |

## ApplicationGraph

Versioned design-time representation of the scoped application.

| Field | Type | Rules |
|---|---|---|
| `graph_id` | string | Deterministic for the same commit, scope, and analyzer version |
| `repository` | object | Contains repository identity and source commit |
| `scope` | object | References `RepositoryScope` |
| `nodes` | array | Must contain unique node IDs and source paths |
| `relationships` | array | Must reference existing node IDs |
| `generated_at` | datetime | Required UTC timestamp |
| `analyzer` | object | Version and capabilities used |

Node kinds initially include `repository`, `module`, `file`, `endpoint`, `model`, `schema`,
`dependency`, `permission`, `test`, and `configuration`.

Relationship kinds initially include `contains`, `imports`, `calls`, `exposes`, `reads`,
`writes`, `depends_on`, `authorized_by`, `tested_by`, and `configures`.

## CapabilityRequest

User or operator request for a capability.

| Field | Type | Rules |
|---|---|---|
| `request_id` | string | Stable identifier |
| `requested_by` | string | Authenticated actor or agent identity |
| `customer_id` | string | Required runtime scope |
| `product_id` | string | Required product scope |
| `text` | string | Natural-language need; must not be empty |
| `requested_at` | datetime | Required UTC timestamp |
| `status` | enum | `new`, `matched`, `provisioning`, `blocked`, or `fulfilled` |

## ToolProposal

Intermediate contract between a capability request and generated code.

| Field | Type | Rules |
|---|---|---|
| `proposal_id` | string | Stable identifier |
| `name` | string | Lowercase stable tool name; no spaces |
| `description` | string | Must describe scope and side effects |
| `input_schema` | object | JSON Schema object |
| `output_schema` | object | JSON Schema object |
| `permissions` | array[string] | At least one explicit permission |
| `data_sources` | array[object] | Approved API, view, procedure, or repository reference |
| `risk_level` | enum | `read_only`, `sensitive_read`, `write`, or `irreversible` |
| `graph_references` | array[string] | Existing graph node IDs |
| `assumptions` | array[string] | Unresolved assumptions must be visible |
| `lifecycle_state` | enum | `draft`, `validation_failed`, `review`, `approved`, `published`, `deprecated`, or `rejected` |

## GeneratedArtifact

Immutable output of the generation and validation pipeline.

| Field | Type | Rules |
|---|---|---|
| `artifact_id` | string | Stable identifier |
| `artifact_version` | string | Semantic version or equivalent immutable version |
| `proposal_id` | string | Required parent proposal |
| `source_commit` | string | Required repository provenance |
| `graph_id` | string | Required graph provenance |
| `checks` | array[object] | Each check has name, status, and evidence |
| `package_digest` | string | Digest of generated package |
| `approved_by` | string | Required before publication |
| `approved_at` | datetime | Required before publication |

## RuntimeDeployment

Publication of an artifact to a customer or domain runtime.

| Field | Type | Rules |
|---|---|---|
| `deployment_id` | string | Stable identifier |
| `artifact_id` | string | Must reference an approved artifact |
| `customer_id` | string | Required isolation scope |
| `runtime_id` | string | Target runtime identifier |
| `transport` | enum | `mcp` or `rest` |
| `status` | enum | `pending`, `active`, `failed`, `revoked`, or `deprecated` |
| `published_at` | datetime | Required when active |

## CapabilityRegistryEntry

Discoverable record used by runtime agents and policy checks.

It references the active artifact, allowed customer/product scope, permissions, transport,
and deprecation status. Discovery MUST filter entries using caller identity and policy.

## AuditEvent

Append-only event for provisioning and runtime actions.

Required attributes are `event_id`, `trace_id`, `timestamp`, `actor`, `customer_id`,
`product_id`, `action`, `resource_type`, `resource_id`, `outcome`, and a redacted `metadata`
object. Secret values and unrestricted raw customer payloads MUST NOT be stored in metadata.

## State transitions

```text
CapabilityRequest:
new → matched → fulfilled
new → provisioning → fulfilled
new → blocked

ToolProposal:
draft → validation_failed → draft
draft → review → approved → published → deprecated
review → rejected
published → deprecated

RuntimeDeployment:
pending → active
pending → failed
active → revoked
active → deprecated
```
