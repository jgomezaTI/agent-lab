# Roadmap de AgentLab

## Objetivo

Convertir AgentLab en una plataforma segura y escalable para centralizar el conocimiento de múltiples productos y permitir consultas, autogestión y operaciones controladas mediante MCP, REST y herramientas internas.

El roadmap prioriza un piloto sobre un LMS basado en Moodle. El piloto comenzará con soporte documental y evolucionará hacia acciones operacionales acotadas, sin habilitar automatizaciones de alto riesgo. Las plataformas internas de gestión del desempeño, capacitación y talento (SGDP) se abordarán posteriormente, debido a su mayor nivel de personalización.

## Principios de ejecución

- Empezar con un solo producto y un caso de uso medible.
- Separar conocimiento de acciones operacionales.
- Mantener el conocimiento versionado y con referencias.
- Centralizar identidad, políticas y auditoría.
- Usar MCP como contrato de integración, no como sustituto del gobierno de seguridad.
- Mantener REST y MCP detrás de una abstracción común.
- Usar Python para la orquestación y Rust para integraciones operacionales que requieran un servicio independiente.
- Introducir acciones operacionales de forma gradual: consulta, autogestión, operación asistida y automatización supervisada.
- Validar calidad y seguridad antes de ampliar el número de productos.

## Fase 0 — Descubrimiento, alcance y riesgo

### Objetivo

Definir el primer caso de uso, las fuentes documentales y el modelo de acceso.

### Trabajo

- [ ] Confirmar un LMS basado en Moodle como producto piloto.
- [ ] Seleccionar un flujo de soporte y una operación controlada para evaluar.
- [ ] Distinguir necesidades del usuario final, del cliente o administrador y del operador.
- [ ] Confirmar que las mallas curriculares y sus actividades viven en Moodle.
- [ ] Definir la finalización de un módulo: una actividad con el checkbox de finalización sin marcar se considera pendiente.
- [ ] Confirmar los tipos de actividades del piloto: recursos, archivos, enlaces, cuestionarios y otros módulos utilizados por la malla.
- [ ] Definir Slack como canal inicial del bot.
- [ ] Excluir la convalidación automática del MVP inicial.
- [ ] Inventariar manuales y fuentes existentes.
- [ ] Inventariar las capacidades de integración disponibles en Moodle, como API o web services.
- [ ] Confirmar formatos: Markdown, PDF, HTML, wiki u otros.
- [ ] Identificar propietarios de la documentación.
- [ ] Clasificar información pública, interna, confidencial y restringida.
- [ ] Definir usuarios, equipos, tenants y roles.
- [ ] Elaborar un threat model inicial.
- [ ] Identificar países, sectores y requisitos contractuales aplicables.

### Resultado esperado

Una especificación del piloto con fuentes, usuarios autorizados, riesgos, criterios de éxito y límites explícitos.

## Fase 1 — Contrato documental y gobierno de conocimiento

### Objetivo

Crear un modelo común que no dependa del formato original de los manuales.

### Trabajo

- [ ] Definir `Document`, `DocumentVersion`, `Section` y `Citation`.
- [ ] Definir `product_id`, `product_version`, `tenant_id` y `locale`.
- [ ] Definir estados de publicación y retirada.
- [ ] Definir clasificación y políticas de retención.
- [ ] Definir reglas de ownership y revisión.
- [ ] Definir cómo se propagan las actualizaciones y eliminaciones.

### Criterio de salida

Un documento Markdown y uno PDF pueden representarse con el mismo contrato, conservar su origen y producir referencias reproducibles.

## Fase 2 — Ingestion e indexación

### Objetivo

Transformar las fuentes en conocimiento consultable y versionado.

### Trabajo

- [ ] Implementar adaptador para Markdown.
- [ ] Implementar adaptador para PDF.
- [ ] Añadir OCR para PDF escaneado si es necesario.
- [ ] Guardar el original en object storage.
- [ ] Registrar metadatos en PostgreSQL.
- [ ] Dividir el contenido por títulos y secciones.
- [ ] Crear índice de texto completo.
- [ ] Añadir búsqueda semántica con `pgvector` u otra tecnología aprobada.
- [ ] Implementar reindexación incremental.
- [ ] Probar eliminación y actualización de documentos.

### Criterio de salida

El sistema puede ingerir, versionar, buscar y retirar documentación sin perder el vínculo con el documento original.

## Fase 3 — Knowledge Service y Knowledge MCP

### Objetivo

Exponer el conocimiento mediante una interfaz segura y estable.

### Trabajo

- [ ] Implementar `search_product_knowledge`.
- [ ] Implementar `get_document_section`.
- [ ] Implementar `list_supported_products`.
- [ ] Implementar `get_product_versions`.
- [ ] Exigir filtros explícitos de producto y versión.
- [ ] Aplicar permisos antes de devolver resultados.
- [ ] Devolver citas, páginas, secciones y versiones.
- [ ] Deshabilitar herramientas de escritura en el primer MVP.
- [ ] Documentar el contrato MCP.
- [ ] Añadir pruebas de compatibilidad MCP.

### Criterio de salida

Un cliente MCP autorizado puede consultar únicamente la información que le corresponde y recibe resultados trazables.

## Fase 4 — MCP Gateway y Tool Registry de AgentLab

### Objetivo

Hacer que los agentes consuman capacidades sin conocer la implementación concreta.

### Trabajo

- [ ] Añadir cliente MCP al Tool Registry.
- [ ] Añadir descubrimiento controlado de servidores.
- [ ] Mantener una allowlist de servidores y herramientas.
- [ ] Añadir adaptadores REST y MCP bajo la misma interfaz.
- [ ] Validar esquemas de entrada y salida con Pydantic.
- [ ] Definir el contrato entre AgentLab y los bridges operacionales.
- [ ] Aplicar timeouts y circuit breakers.
- [ ] Añadir cuotas y límites por agente, usuario y tenant.
- [ ] Registrar cada invocación con `trace_id`.

### Criterio de salida

El mismo agente puede consumir una capacidad mediante MCP, REST o Python sin modificar su lógica de negocio.

Los adaptadores operacionales podrán implementarse como servicios independientes. El primer caso será un Moodle Bridge en Rust, consumido por AgentLab mediante REST o MCP.

## Fase 5 — Identidad, políticas y seguridad

### Objetivo

Convertir el acceso a conocimiento y herramientas en una decisión explícita y auditable.

### Trabajo

- [ ] Integrar un proveedor OIDC/OAuth.
- [ ] Propagar la identidad del usuario hasta la recuperación.
- [ ] Definir scopes y políticas por producto y versión.
- [ ] Resolver permisos mediante roles y capabilities de Moodle en su contexto, no mediante la tabla `mdl_user` por sí sola.
- [ ] Implementar denegación por defecto.
- [ ] Validar audiencias de tokens MCP.
- [ ] Evitar token passthrough no controlado.
- [ ] Añadir almacenamiento seguro de secretos.
- [ ] Redactar secretos y datos personales en logs.
- [ ] Añadir límites de egress y dominios permitidos.
- [ ] Definir política de retención de auditoría.
- [ ] Revisar seguridad de dependencias y servidores MCP.

### Criterio de salida

Una consulta no autorizada es rechazada antes de recuperar datos y existe evidencia suficiente para reconstruir una ejecución.

## Fase 6 — Piloto AgentLab + Moodle

### Objetivo

Validar el valor de negocio con un flujo limitado y verificable sobre un LMS basado en Moodle.

### Trabajo

- [ ] Crear el agente de soporte en Python dentro de AgentLab.
- [ ] Implementar el Moodle Bridge como servicio independiente en Rust.
- [ ] Permitir consultas sobre un único LMS y sus manuales asociados.
- [ ] Consultar el estado de matrícula de un usuario.
- [ ] Consultar la fecha de matrícula y el curso o programa asociado.
- [ ] Consultar las notas o calificaciones disponibles.
- [ ] Identificar cursos o módulos pendientes según la malla correspondiente.
- [ ] Probar la interacción del bot mediante Slack.
- [ ] Permitir que un usuario consulte y edite únicamente la información de su propio perfil.
- [ ] Permitir la consulta de notas o datos personales de terceros solo cuando el rol y las capacidades de Moodle lo autoricen.
- [ ] Recuperar información usando Knowledge MCP.
- [ ] Exigir respuesta con citas.
- [ ] Responder explícitamente cuando no exista evidencia suficiente.
- [ ] Añadir una capacidad de autogestión de bajo riesgo para usuarios o clientes.
- [ ] Añadir una operación controlada para el cliente o el operador, como validar y matricular usuarios.
- [ ] Permitir solicitudes masivas mediante un archivo solo después de validar su estructura y contenido.
- [ ] Mostrar una previsualización y solicitar confirmación antes de modificar Moodle.
- [ ] Mantener fuera del MVP la aplicación automática de reglas de convalidación.
- [ ] Registrar permisos, validaciones, cambios, errores y excepciones.
- [ ] Registrar las fuentes usadas.
- [ ] Añadir interfaz API y, opcionalmente, una UI mínima.
- [ ] Prohibir operaciones arbitrarias o acciones irreversibles.

### Criterio de salida

El agente resuelve un conjunto de preguntas reales con respuestas fundamentadas y ejecuta una operación acotada sobre Moodle con permisos, confirmación y auditoría.

## Fase 7 — Evaluación y seguridad adversarial

### Objetivo

Medir si el sistema es útil, seguro y reproducible antes de escalarlo.

### Trabajo

- [ ] Crear dataset de preguntas reales y sintéticas.
- [ ] Medir precisión de recuperación.
- [ ] Medir corrección de citas.
- [ ] Medir respuestas sin evidencia.
- [ ] Probar documentos con prompt injection.
- [ ] Probar acceso cruzado entre productos y tenants.
- [ ] Probar documentos retirados y versiones antiguas.
- [ ] Medir latencia, coste y número de llamadas.
- [ ] Ejecutar pruebas de carga sobre Knowledge MCP.
- [ ] Probar validación de archivos y operaciones masivas controladas.
- [ ] Medir tasa de operaciones exitosas, rechazadas y derivadas a un operador.
- [ ] Medir reducción del trabajo operativo en el flujo piloto.
- [ ] Registrar resultados por modelo y configuración.

### Criterio de salida

Existe un informe reproducible de calidad, seguridad, coste y rendimiento, con riesgos conocidos y decisiones de aceptación.

## Fase 8 — Escalado y extensión a sistemas personalizados

### Objetivo

Ampliar la plataforma sin perder aislamiento ni control.

### Trabajo

- [ ] Incorporar más productos mediante conectores.
- [ ] Definir cuándo un producto requiere un MCP independiente.
- [ ] Separar Knowledge MCP de Product Operations MCP.
- [ ] Añadir herramientas operacionales de solo lectura.
- [ ] Incorporar acciones con aprobación humana.
- [ ] Extender el enfoque a sistemas SGDP mediante adaptadores específicos.
- [ ] Documentar diferencias de permisos, datos y workflows entre Moodle y cada SGDP.
- [ ] Añadir workflows multiagente.
- [ ] Añadir despliegue horizontal e ingestion asíncrona.
- [ ] Integrar alertas y SIEM.
- [ ] Crear reportes de cumplimiento y auditoría.

### Criterio de salida

Los nuevos productos pueden integrarse mediante configuración y conectores sin duplicar agentes, políticas ni mecanismos de auditoría.

## Vertical slice recomendado

El primer entregable debería ser pequeño pero completo:

```text
1 LMS basado en Moodle
1 conjunto de manuales del LMS
1 Knowledge MCP
1 agente de soporte en Python
1 Moodle Bridge en Rust
1 API FastAPI
1 modelo de permisos
1 sistema de citas
Consultas de matrícula, fechas, notas y módulos pendientes
1 operación controlada con confirmación
1 conjunto de evaluaciones
```

No se deberían añadir todavía acciones arbitrarias, operaciones irreversibles, convalidación automática ni integraciones con SGDP altamente personalizados.

## Métricas de éxito

- Precisión de recuperación.
- Porcentaje de respuestas con citas correctas.
- Tasa de respuestas sin evidencia.
- Tasa de filtrado correcto por permisos.
- Tasa de fuga entre productos o tenants.
- Latencia de recuperación y de respuesta total.
- Coste estimado por interacción.
- Número de llamadas a herramientas por tarea.
- Porcentaje de ejecuciones auditables.
- Tiempo necesario para incorporar un nuevo producto.
- Porcentaje de operaciones ejecutadas correctamente.
- Porcentaje de solicitudes derivadas a un operador.
- Tiempo operativo ahorrado en el flujo piloto.

## Riesgos principales

| Riesgo | Mitigación |
|---|---|
| Documentación desactualizada | Versionado, ownership y fecha de vigencia |
| Fuga entre productos | Filtrado por identidad y políticas server-side |
| Prompt injection en manuales | Tratar documentos como datos no confiables y probar contenido adversarial |
| Exceso de servidores MCP | Gateway, catálogo y criterios de separación |
| Herramientas demasiado poderosas | Contratos estrechos, allowlist y solo lectura inicial |
| Costes impredecibles | Límites de tokens, pasos, tiempo y presupuesto |
| Falta de evidencia | Auditoría, trazas y citas obligatorias |
| Operaciones incorrectas sobre Moodle | Bridge con contratos estrechos, validación, previsualización y confirmación |
| Integraciones SGDP demasiado personalizadas | Adaptadores específicos y extensión posterior al piloto |
| Incumplimiento normativo | Matriz legal por país, sector y tipo de dato |

## Definición de listo para producción

La plataforma no debería considerarse lista para producción hasta contar, como mínimo, con:

- Modelo de identidad y autorización probado.
- Aislamiento verificado entre productos y tenants.
- Gestión de documentos retirados y versiones antiguas.
- Auditoría completa y redacción de datos sensibles.
- Evaluaciones de calidad y seguridad automatizadas.
- Límites de ejecución y control de costes.
- Gestión de secretos y dependencias.
- Procedimiento de incidentes y recuperación.
- Revisión de seguridad, privacidad y cumplimiento.
- Documentación operativa y de soporte.
