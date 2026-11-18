# ADR 0001: Separar plano de control y plano de ejecución

## Estado

Aceptada — 2026-11-18

## Contexto

El equipo necesita inspeccionar repositorios de productos específicos, proponer nuevas
herramientas y permitir que agentes de soporte las consuman. Conectar el agente de soporte
directamente al repositorio o generar/desplegar código durante una petición mezclaría
análisis de diseño con acceso operacional y dificultaría el aislamiento por cliente.

## Decisión

Se adoptan dos planos:

- control: scope, grafo, propuestas, validación, aprobación y publicación;
- ejecución: registro, políticas, adaptadores MCP/REST y conectores de datos aprobados.

El grafo aporta evidencia y contexto estructural, pero no es una fuente de datos de
negocio. El runtime consume artefactos publicados y no importa el mapper.

## Consecuencias

Se puede regenerar una capacidad cuando cambia el repositorio sin exponer el repositorio
en producción. A cambio, se necesita un pipeline de promoción, versionado, revisión y
revocación. El vertical slice inicial usa implementaciones en memoria para probar los
contratos antes de incorporar infraestructura real.
