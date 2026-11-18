# ADR 0002: Contrato único con adaptadores MCP y REST

## Estado

Aceptada — 2026-11-18

## Decisión

Cada capacidad se registra una sola vez con nombre, schemas, permisos, fuente de datos,
proveniencia y estado. MCP se usa para descubrimiento/invocación desde agentes y REST para
interoperabilidad. Ambos delegan en los mismos servicios de política, auditoría y
aislamiento.

## Consecuencia

La ausencia de MCP en un cliente no bloquea el producto, pero no se duplica la lógica de
negocio en dos integraciones. El contrato común debe probarse antes de habilitar un
conector real.
