# Uso de asistentes y agentes de IA en el TIF

## Objetivo

Este documento define cómo se usarán herramientas de IA en el desarrollo del Trabajo Integrador Final.

Las herramientas de IA se utilizan como soporte para planificación, auditoría, implementación, revisión y documentación. No constituyen el objeto central del TIF.

## Principio general

Toda intervención de IA debe ser:

- trazable;
- revisable;
- acotada;
- metodológicamente justificada;
- compatible con la privacidad de datos públicos sensibles.

## Roles recomendados

### 1. Auditor del repositorio

Uso:

- revisar estructura del proyecto;
- detectar deuda técnica;
- identificar riesgos de reproducibilidad;
- revisar documentación;
- detectar riesgos de privacidad.

No debe:

- modificar archivos;
- refactorizar código;
- proponer modelos sin revisar datos.

### 2. Implementador prudente

Uso:

- ejecutar issues pequeños;
- crear scripts acotados;
- refactorizar funciones puntuales;
- agregar validaciones;
- mejorar documentación técnica.

No debe:

- cambiar el alcance del TIF;
- modificar datos sensibles;
- introducir dependencias innecesarias;
- hacer refactors masivos.

### 3. Revisor metodológico-técnico

Uso:

- revisar hipótesis;
- evaluar coherencia entre datos y método;
- detectar supuestos débiles;
- revisar resultados;
- preparar defensa.

No debe:

- reemplazar la decisión del autor;
- priorizar sofisticación técnica por encima de claridad académica.

## Flujo de trabajo recomendado

1. Definir objetivo de la sesión.
2. Seleccionar el prompt adecuado.
3. Pedir diagnóstico antes de implementar.
4. Ejecutar cambios pequeños.
5. Validar resultados.
6. Registrar decisiones relevantes.
7. Crear commit con mensaje claro.

## Reglas de privacidad

- No subir datos crudos sensibles a herramientas cloud.
- No compartir identificadores innecesarios.
- No incluir outputs con registros individuales en documentación.
- Usar agregados, esquemas o muestras sintéticas.
- Mantener datos fuera del repositorio salvo que sean públicos, necesarios y seguros.

## Criterio de uso

Usar IA cuando ayude a:

- ordenar;
- revisar;
- documentar;
- validar;
- implementar tareas acotadas.

No usar IA para:

- decidir metodología sin evidencia;
- automatizar cambios masivos;
- manipular datos sensibles sin control;
- reemplazar revisión humana.
