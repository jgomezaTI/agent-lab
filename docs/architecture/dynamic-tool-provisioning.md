# Arquitectura de provisión dinámica de herramientas

## Decisión central

AgentLab separa dos planos que no deben mezclarse:

```text
Plano de control / diseño
Repositorio → scope → grafo → propuesta → validación → aprobación → publicación

Plano de ejecución / runtime
Agente de soporte → gateway MCP/REST → registro → políticas → conector aprobado → datos del cliente
```

El repositorio sirve como evidencia técnica para entender estructura, dependencias y
relaciones. No es la fuente de datos del cliente y no debe quedar en el camino de una
consulta de usuario final.

## Flujo completo

1. El host de IA carga `AGENTS.md`, la instrucción de su proveedor y
   `skills/repository-mapper/SKILL.md`.
2. El agente configura un scope por producto. El scope incluye únicamente el portal o
   módulo relevante y excluye el core genérico, tests pesados o carpetas no pertinentes.
3. `repository-mapper scan` inspecciona archivos de forma estática. No importa ni ejecuta
   el código inspeccionado.
4. El mapper emite un `application-graph` con IDs deterministas, commit, hash de
   configuración, nodos, relaciones y evidencia de origen.
5. Un agente constructor recibe una solicitud como “buscar mis notas de curso”, consulta
   el grafo y genera una `tool-proposal` con esquema, permiso, fuente de datos,
   referencias del grafo y supuestos pendientes.
6. Validadores contractuales, de seguridad y de pruebas revisan la propuesta y el
   artefacto generado en un entorno aislado.
7. Una persona o política aprobadora acepta el artefacto. Solo entonces el publicador lo
   registra en el runtime del cliente.
8. El runtime expone la capacidad mediante MCP y, cuando convenga por compatibilidad,
   REST. Ambos adaptadores apuntan al mismo contrato y servicio de políticas.
9. El agente de soporte descubre solamente las herramientas que corresponden a su
   `customer_id`, `product_id`, `environment` y permisos.
10. La invocación usa una interfaz aprobada —API del producto, vista de solo lectura o
    servicio interno— y genera un evento auditable con `trace_id`.

## Qué se genera y qué no

Se generan artefactos versionables: scope, grafo, propuesta, manifiesto, digest,
resultado de validaciones, registro de capacidad y evidencia de aprobación.

No se permite en este vertical slice:

- ejecutar código arbitrario del repositorio;
- crear consultas SQL libres a la base del cliente;
- desplegar directamente en producción;
- usar el código del repositorio como base de conocimiento operacional;
- crear capacidades de escritura sin un flujo adicional de riesgo y aprobación.

## MCP y REST

MCP es el adaptador natural para descubrimiento de herramientas por agentes. REST es un
adaptador de interoperabilidad para clientes, jobs o sistemas que no tengan MCP. La
capacidad se define una sola vez en el registro; los adaptadores no deben duplicar la
lógica de permisos ni de aislamiento.

## Handoff entre agentes

El agente constructor y el agente de soporte tienen responsabilidades distintas:

| Agente | Puede hacer | No debe hacer |
|---|---|---|
| Mapper/constructor | Leer scope, crear grafo, proponer código/artefacto y abrir revisión | Consultar datos productivos o publicar sin aprobación |
| Soporte/runtime | Descubrir y usar capacidades publicadas | Generar, instalar o desplegar código durante una consulta |
| Aprobador | Revisar evidencia, riesgo y cambios | Omitir validaciones o aceptar referencias sin trazabilidad |

## Estado actual del repositorio

La implementación local cubre el vertical slice con un runtime y datos sintéticos. Los
conectores reales, el SDK MCP remoto, identidad corporativa, secretos, persistencia y
despliegue son siguientes incrementos deliberados, no supuestos ocultos.
