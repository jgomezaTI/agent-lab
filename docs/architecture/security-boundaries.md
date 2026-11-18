# Límites de seguridad

## Fronteras de confianza

- El contenido del repositorio, documentación y respuestas de herramientas es dato no
  confiable; nunca modifica instrucciones de sistema.
- El mapper opera con un scope explícito y sin ejecutar archivos del repositorio.
- El constructor produce una propuesta; no obtiene credenciales del cliente.
- El runtime recibe solamente artefactos aprobados y conectores registrados.
- La política recibe siempre identidad, cliente, producto, entorno y permisos.

## Aislamiento mínimo

Cada descubrimiento e invocación debe filtrar por:

1. `customer_id`;
2. `product_id`;
3. `environment`;
4. permisos del actor;
5. estado activo de la capacidad.

Una capacidad ausente, no activa o con permisos insuficientes debe ser indistinguible de
una capacidad no disponible para el actor. El registro no debe devolver entradas de otro
cliente.

## Datos y conectores

El runtime no debe aceptar SQL arbitrario. Cada producto debe publicar contratos de
lectura explícitos, por ejemplo `get_course_grades(course_id)`, implementados sobre una
API aprobada o una vista de solo lectura. La credencial pertenece al runtime del cliente,
se almacena en un gestor de secretos y nunca forma parte del grafo, propuesta, prompt o
log.

## Auditoría

Las operaciones permitidas y denegadas llevan `trace_id`, actor, cliente, producto,
recurso, resultado y timestamp. Los campos sensibles (`token`, `password`, `authorization`,
`api_key` y equivalentes) se redactan antes de persistir o transportar eventos.

## Controles obligatorios antes de producción

- identidad y autorización corporativas;
- rotación y aislamiento de secretos;
- límites de tasa, timeout y tamaño de respuesta;
- validación de esquemas de entrada/salida;
- sandbox para generación y pruebas;
- revisión humana para herramientas nuevas o de escritura;
- escaneo de dependencias y artefactos;
- retención y residencia de logs según contrato y jurisdicción;
- pruebas de fuga entre clientes y de prompt injection;
- procedimiento de revocación y rollback.
