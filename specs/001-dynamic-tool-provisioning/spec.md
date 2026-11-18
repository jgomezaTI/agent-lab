# Feature Specification: Repository-Guided Dynamic Tool Provisioning

**Feature Branch**: `001-dynamic-tool-provisioning`

**Created**: 2026-11-18

**Status**: Foundation implemented — pending architectural review

**Input**: User description: "Permitir que una skill conectada a un repositorio analice el alcance relevante de una aplicación, construya un grafo y ayude a un agente a proponer, probar y publicar herramientas MCP para que otros agentes puedan consumirlas contra los sistemas autorizados de un cliente."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mapear una aplicación con alcance controlado (Priority: P1)

Como responsable de producto o plataforma, quiero conectar un repositorio y declarar qué partes de la aplicación son relevantes para que un agente pueda analizar su estructura sin recorrer componentes genéricos o irrelevantes.

**Why this priority**: El grafo es la base de toda la provisión de herramientas. Sin un mapa acotado, el agente puede interpretar incorrectamente la aplicación y generar integraciones innecesarias.

**Independent Test**: Dado un repositorio de ejemplo con módulos incluidos y excluidos, ejecutar la skill y comprobar que produce un grafo reproducible con los módulos incluidos, sus relaciones y la razón de exclusión de los demás.

**Acceptance Scenarios**:

1. **Given** un repositorio con rutas incluidas y excluidas, **When** se ejecuta el mapper, **Then** el resultado contiene únicamente el alcance autorizado y registra la configuración utilizada.
2. **Given** un repositorio con endpoints, modelos, dependencias y tests, **When** se genera el grafo, **Then** cada nodo conserva su ruta de origen y cada relación identifica su tipo.
3. **Given** una segunda ejecución sobre el mismo commit y configuración, **When** se compara el resultado, **Then** el grafo y sus identificadores son reproducibles.

---

### User Story 2 - Proponer una herramienta a partir de una necesidad (Priority: P1)

Como responsable de plataforma, quiero convertir una necesidad expresada en lenguaje natural en una especificación de herramienta para que el agente constructor pueda generar una implementación verificable.

**Why this priority**: La especificación intermedia evita que el agente pase directamente de una petición ambigua a código ejecutable.

**Independent Test**: Dado un grafo y la petición "consultar las notas del usuario autenticado por curso", comprobar que se crea una especificación con nombre, descripción, entradas, salida, permisos, fuentes de datos, riesgo y referencias al grafo.

**Acceptance Scenarios**:

1. **Given** una necesidad compatible con capacidades conocidas, **When** el agente constructor analiza el grafo, **Then** propone una herramienta con contrato de entrada y salida explícito.
2. **Given** una necesidad sin suficiente evidencia en el grafo, **When** se solicita la herramienta, **Then** el sistema marca la propuesta como incompleta y solicita información adicional en lugar de inventar una integración.
3. **Given** una propuesta de herramienta de solo lectura, **When** se valida, **Then** su riesgo, permisos y origen quedan registrados antes de generar código.

---

### User Story 3 - Probar y publicar una herramienta versionada (Priority: P1)

Como responsable de operaciones, quiero que una herramienta generada pase por validaciones y aprobación antes de publicarse en un runtime MCP del cliente.

**Why this priority**: La publicación es el límite entre una propuesta generada y una capacidad que puede tocar datos reales.

**Independent Test**: Dada una herramienta válida y un entorno de pruebas, ejecutar el pipeline y comprobar que solo una versión aprobada aparece como publicable, con trazabilidad del commit, grafo y especificación.

**Acceptance Scenarios**:

1. **Given** una herramienta generada, **When** falla la validación de contrato o seguridad, **Then** no puede publicarse y conserva los errores asociados.
2. **Given** una herramienta que supera las validaciones, **When** un responsable la aprueba, **Then** se crea un artefacto versionado con metadatos de procedencia.
3. **Given** una herramienta publicada, **When** cambia el contrato de origen, **Then** el sistema puede marcarla como potencialmente obsoleta y evitar su publicación automática.

---

### User Story 4 - Descubrir y consumir la herramienta desde un agente (Priority: P1)

Como usuario final, quiero pedir información de un producto y que el agente utilice una herramienta autorizada del cliente sin conocer cómo fue implementada.

**Why this priority**: Este es el valor visible de la plataforma: resolver necesidades de soporte usando herramientas estables y gobernadas.

**Independent Test**: Dado un runtime MCP de pruebas con una herramienta publicada, solicitar una consulta de soporte y comprobar que el agente descubre la capacidad, la invoca con el esquema correcto y devuelve una respuesta trazable.

**Acceptance Scenarios**:

1. **Given** una herramienta publicada y autorizada, **When** el usuario realiza una petición compatible, **Then** el agente selecciona la herramienta y devuelve el resultado con su origen.
2. **Given** una herramienta inexistente, **When** el usuario realiza una petición, **Then** el agente no genera ni despliega código durante la interacción y crea una solicitud de provisión pendiente.
3. **Given** un usuario sin permiso sobre un producto, **When** intenta consultar sus datos, **Then** la herramienta no aparece o la invocación es rechazada antes de acceder a la fuente.

---

### User Story 5 - Operar con aislamiento y trazabilidad (Priority: P1)

Como responsable de seguridad, quiero identificar quién, qué agente, qué cliente, qué herramienta y qué fuente participaron en cada ejecución para poder auditar y responder ante incidentes.

**Why this priority**: Sin aislamiento, autorización y auditoría, la generación dinámica de herramientas no es adecuada para datos de clientes.

**Independent Test**: Ejecutar una consulta autorizada y otra no autorizada en un entorno multi-cliente y comprobar que los datos quedan aislados y que ambos resultados generan eventos auditables sin exponer secretos.

**Acceptance Scenarios**:

1. **Given** dos clientes con datos similares, **When** un agente consulta uno de ellos, **Then** el resultado no contiene información del otro.
2. **Given** una herramienta con permisos insuficientes, **When** se intenta invocar, **Then** la política la rechaza antes de acceder a la fuente.
3. **Given** una ejecución completada, **When** se consulta su traza, **Then** se pueden reconstruir actor, agente, herramienta, versión, fuente, resultado, latencia y aprobación.

### Edge Cases

- El repositorio no contiene las rutas declaradas en el alcance.
- El repositorio contiene código generado, dependencias vendorizadas o un monorepo con varios productos.
- El grafo no tiene evidencia suficiente para construir una herramienta solicitada.
- El contrato de una fuente cambia después de publicar una herramienta.
- El documento o código recuperado contiene instrucciones que intentan alterar las políticas del agente.
- La herramienta MCP está disponible pero la identidad del usuario no tiene permisos sobre el cliente o producto.
- Una publicación se interrumpe después de crear el artefacto y antes de actualizar el registro.
- El runtime del cliente no está disponible o responde parcialmente.
- La herramienta devuelve datos personales o sensibles que no deben llegar al modelo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow an authorized operator to define repository roots, inclusion patterns, exclusion patterns, product identity, environment, and analysis configuration.
- **FR-002**: System MUST generate a versioned application graph from the authorized repository scope.
- **FR-003**: System MUST preserve source paths, commit identifier, analyzer version, configuration hash, and graph identifier for every generated graph.
- **FR-004**: System MUST represent relevant modules, endpoints, data models, dependencies, permissions, tests, and typed relationships when evidence is available.
- **FR-005**: System MUST allow an agent to create a tool proposal from a natural-language capability request and an application graph.
- **FR-006**: Every tool proposal MUST include a stable name, description, input schema, output schema, permissions, data sources, risk level, graph references, and unresolved assumptions.
- **FR-007**: System MUST refuse to generate a publishable tool when required evidence, permissions, or data-source contracts are missing.
- **FR-008**: System MUST execute generated tools in an isolated validation environment before publication.
- **FR-009**: System MUST validate tool schemas, authorization metadata, dependency provenance, and security policy before publication.
- **FR-010**: System MUST model tool lifecycle states including draft, validation_failed, review, approved, published, deprecated, and rejected.
- **FR-011**: System MUST publish approved tools as versioned artifacts to a customer or domain runtime without requiring the source repository during normal runtime execution.
- **FR-012**: System MUST maintain a capability registry that records tool versions, customer scope, permissions, source graph, source commit, deployment status, and deprecation state.
- **FR-013**: System MUST allow runtime agents to discover only tools permitted by their identity, customer, product, environment, and policy context.
- **FR-014**: System MUST prevent runtime agents from generating or deploying code directly during an ordinary end-user request.
- **FR-015**: System MUST expose generated tools through a controlled MCP or REST adapter while preserving a transport-neutral internal contract.
- **FR-016**: Runtime data access MUST use approved APIs, read-only views, stored procedures, or parameterized repositories; arbitrary SQL, unrestricted filesystem access, and unrestricted network access MUST NOT be exposed.
- **FR-017**: System MUST propagate the authenticated caller and customer context to every tool invocation.
- **FR-018**: System MUST record an audit event for repository analysis, graph generation, proposal, validation, approval, publication, discovery, invocation, denial, failure, and deprecation.
- **FR-019**: System MUST redact secrets and sensitive payloads according to configured data-handling policy.
- **FR-020**: System MUST detect or flag possible graph and tool drift when source commits, schemas, permissions, or contracts change.
- **FR-021**: System MUST provide a portable agent instruction entry point that can guide Codex, Cursor, Claude, or another compatible coding agent through repository mapping and tool provisioning.
- **FR-022**: System SHOULD support a local mock customer runtime and synthetic fixtures so the full provisioning flow can be validated without production data.

### Key Entities

- **Repository Scope**: Authorized roots, inclusion and exclusion patterns, product identity, environment, and analysis configuration.
- **Application Graph**: Versioned representation of modules, endpoints, models, dependencies, permissions, tests, and their relationships.
- **Capability Request**: A natural-language request for a missing or existing capability, including requester, customer, product, and desired outcome.
- **Tool Proposal**: A proposed capability contract with schemas, permissions, sources, risk, assumptions, and graph references.
- **Generated Artifact**: A tested and versioned implementation package with source commit, graph, specification, dependencies, and validation results.
- **Runtime Deployment**: Publication of an approved artifact to a customer or domain MCP/REST runtime.
- **Capability Registry Entry**: The discoverable record of a tool, its lifecycle, versions, scope, permissions, and deployment status.
- **Audit Event**: An immutable or append-only record of an actor, action, resource, outcome, and trace context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An authorized agent can configure and analyze a scoped repository without manually enumerating every relevant module.
- **SC-002**: For a supported sample repository, repeated analysis of the same commit and scope produces identical graph identifiers and equivalent relationships.
- **SC-003**: At least 90% of tool proposals in the pilot include complete name, schemas, permissions, source references, and unresolved-assumption fields without manual reconstruction.
- **SC-004**: No tool can reach a published runtime before passing validation and an explicit publication gate.
- **SC-005**: A runtime agent can discover and invoke an approved read-only tool for the pilot product without importing repository-specific implementation code.
- **SC-006**: Unauthorized cross-customer and cross-product queries are rejected in all security test scenarios.
- **SC-007**: 100% of pilot executions have traceable actor, customer, agent, tool version, source reference, outcome, and approval metadata.
- **SC-008**: A repository or source-contract change can be detected and associated with affected graph or tool versions before the next automatic publication.
- **SC-009**: The first pilot tool can be provisioned from request to approved artifact using a documented workflow that does not require manually editing the repository structure for each new tool.

## Assumptions

- The first vertical slice targets one product and one read-only support capability.
- The customer exposes an approved API, read-only database view, stored procedure, or equivalent data interface.
- Production credentials are supplied through an external secret-management mechanism.
- Human approval is required before publication to a customer runtime during the initial release.
- The repository mapper initially supports common source-code and configuration formats; unsupported formats are reported rather than silently ignored.
- The initial implementation may use mock runtimes and synthetic data instead of connecting to a real customer environment.
- Legal, privacy, and security owners will validate the final control mapping for each deployment jurisdiction and sector.

## Out of Scope for the Initial Release

- Automatic deployment to production without approval.
- Arbitrary SQL generation and execution.
- Write operations against customer systems.
- Full semantic understanding of every framework or programming language.
- Replacing the customer's source-control, CI/CD, IAM, or secrets-management systems.
- Guaranteeing legal or regulatory compliance without organization-specific review.
