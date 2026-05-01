# AGENTS.md

## Propósito

Este repositorio corresponde a un Trabajo Integrador Final de Posgrado en Ciencia de Datos.

El proyecto busca analizar patrones de mora y comportamiento crediticio en Argentina utilizando datos públicos sensibles, con foco en rigor metodológico, reproducibilidad, trazabilidad y viabilidad académica.

Las herramientas de IA pueden asistir en planificación, auditoría, implementación, revisión y documentación, pero no constituyen el objeto central del TIF.

## Reglas generales para agentes

Todo agente que trabaje sobre este repositorio debe:

1. priorizar cambios pequeños, revisables y trazables;
2. explicar supuestos antes de implementar;
3. indicar archivos que modificará antes de hacer cambios;
4. no modificar datos crudos;
5. no exponer identificadores sensibles;
6. no introducir dependencias nuevas sin justificación;
7. no proponer modelos complejos sin validar la estructura de datos;
8. no asumir que existe longitudinalidad suficiente sin evidencia;
9. mantener separación entre exploración, implementación y documentación;
10. respetar el alcance metodológico del TIF.

## Privacidad

Los datos pueden ser públicos, pero deben tratarse como sensibles.

El agente no debe:

- imprimir registros individuales innecesarios;
- copiar identificadores sensibles en respuestas;
- subir datos crudos a servicios externos;
- agregar datos crudos al repositorio;
- generar documentación con ejemplos reales sensibles.

Debe preferir:

- esquemas;
- agregados;
- muestras sintéticas;
- diccionarios de variables;
- estadísticas descriptivas no identificatorias.

## Antes de implementar

El agente debe informar:

1. interpretación de la tarea;
2. archivos que espera modificar;
3. supuestos;
4. riesgos;
5. validaciones previstas.

## Después de implementar

El agente debe informar:

1. archivos modificados;
2. resumen de cambios;
3. validaciones ejecutadas;
4. validaciones pendientes;
5. riesgos remanentes;
6. mensaje de commit sugerido.

## Reglas metodológicas

Antes de proponer análisis temporal de mora, validar:

- unidad de análisis;
- identificador persistente;
- variable temporal;
- periodicidad;
- cantidad de períodos disponibles;
- variable de situación crediticia, mora o deterioro;
- continuidad suficiente para reconstruir trayectorias;
- riesgo de leakage.

Si no hay evidencia suficiente para análisis temporal, considerar una ruta alternativa basada en segmentación no supervisada de perfiles crediticios.

## Rutas metodológicas posibles

### Ruta A — Análisis temporal de mora

Viable si existen datos longitudinales confiables.

Métodos posibles:

- matrices de transición;
- análisis de deterioro, permanencia y mejora;
- modelos de tiempo discreto o supervivencia, si el alcance lo permite.

### Ruta B — Segmentación no supervisada

Viable si no hay longitudinalidad suficiente, pero sí estructura transversal rica.

Métodos posibles:

- K-Means;
- clustering jerárquico;
- Gaussian Mixture Models;
- reducción dimensional exploratoria;
- validación con métricas internas e interpretación de perfiles.

## Tareas adecuadas para agentes

Los agentes pueden ayudar con:

- auditoría del repositorio;
- revisión de estructura de datos;
- redacción de issues;
- refactorización puntual;
- documentación técnica;
- revisión de privacidad;
- validaciones;
- mejora de README;
- organización de notebooks;
- generación de funciones auxiliares.

## Tareas no adecuadas para agentes sin supervisión

Los agentes no deben realizar de forma autónoma:

- cambios masivos de arquitectura;
- eliminación de archivos;
- modificación de datos;
- selección definitiva de metodología;
- interpretación final de resultados;
- redacción final sin revisión humana;
- publicación de información sensible.

## Criterio de terminado

Una tarea realizada por un agente solo se considera terminada si:

1. cumple el objetivo definido;
2. los cambios son mínimos y revisables;
3. no introduce riesgos de privacidad;
4. incluye validaciones o indica claramente cuáles faltan;
5. mantiene coherencia con el objetivo académico del TIF;
6. deja trazabilidad suficiente para revisión.
