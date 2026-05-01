# Instrucciones para asistentes de IA en este repositorio

Este repositorio corresponde a un Trabajo Integrador Final de Posgrado en Ciencia de Datos.

## Objetivo del proyecto

El proyecto busca analizar patrones de mora y comportamiento crediticio en Argentina utilizando datos públicos sensibles, con foco en rigor metodológico, reproducibilidad, trazabilidad y viabilidad académica.

El aporte principal del TIF es metodológico y analítico. Las herramientas de IA se utilizan como soporte para desarrollo, revisión, documentación y trazabilidad, pero no constituyen el objeto central del trabajo.

## Reglas generales

- No exponer datos crudos ni identificadores sensibles.
- No modificar archivos de datos sin instrucción explícita.
- No asumir que el análisis temporal es viable sin evidencia de longitudinalidad.
- No introducir modelos complejos sin justificación metodológica.
- Priorizar cambios pequeños, revisables y trazables.
- Toda implementación debe incluir validaciones mínimas.
- Toda propuesta debe distinguir supuestos, riesgos y criterios de aceptación.
- Separar claramente lo imprescindible, lo deseable y lo accesorio.
- No convertir el uso de IA, agentes o automatizaciones en el foco del TIF.

## Reglas sobre privacidad

Los datos utilizados pueden ser públicos, pero deben tratarse como sensibles.

El asistente debe:

- evitar mostrar registros individuales;
- trabajar preferentemente con esquemas, agregados, muestras sintéticas o descripciones;
- no proponer subir datos sensibles a servicios externos;
- recomendar exclusión de datos crudos del repositorio;
- señalar riesgos de exposición de identificadores;
- proponer validaciones de minimización de datos cuando corresponda.

## Estilo técnico esperado

- Usar Python claro, mantenible y documentado.
- Separar notebooks exploratorios de código reutilizable.
- Preferir funciones pequeñas y testeables.
- Evitar sobreingeniería.
- Priorizar reproducibilidad.
- Documentar decisiones relevantes.
- Usar nombres descriptivos.
- Evitar cambios masivos no solicitados.

## Antes de modificar código

El asistente debe indicar:

1. objetivo del cambio;
2. archivos afectados;
3. supuestos;
4. riesgos;
5. validaciones propuestas.

## Después de modificar código

El asistente debe informar:

1. cambios realizados;
2. archivos modificados;
3. validaciones ejecutadas o pendientes;
4. riesgos remanentes;
5. próximo paso recomendado.

## Criterio metodológico

Antes de proponer modelos, el asistente debe validar o solicitar evidencia sobre:

- unidad de análisis;
- variable temporal;
- variable de situación crediticia o mora;
- cantidad de períodos disponibles;
- persistencia de identificadores;
- continuidad suficiente para reconstruir trayectorias;
- riesgo de leakage;
- interpretación financiera o crediticia de los resultados.

## Rutas metodológicas posibles

### Ruta A: análisis temporal de mora

Viable si existen identificadores persistentes, variable temporal confiable, variable de situación crediticia y continuidad suficiente.

Métodos posibles:

- matrices de transición;
- análisis de deterioro, permanencia y mejora;
- modelos de tiempo discreto o supervivencia, si el alcance lo permite.

### Ruta B: segmentación no supervisada

Viable si no hay longitudinalidad suficiente, pero sí una estructura transversal rica.

Métodos posibles:

- K-Means;
- clustering jerárquico;
- Gaussian Mixture Models;
- reducción dimensional exploratoria;
- validación con métricas internas e interpretación de perfiles.

## Regla de prudencia

Si una propuesta parece técnicamente atractiva pero aumenta demasiado el alcance, el asistente debe advertirlo.

Si una propuesta parece académicamente interesante pero inviable operativamente, el asistente también debe advertirlo.
