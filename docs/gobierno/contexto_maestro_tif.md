# Contexto maestro del TIF

**Última actualización:** 2026-05-01
**Estado:** vigente
**Chat de origen:** 00 — Control de avance y protocolo del TIF

## 1. Rol de este Project

Este Project se utiliza como espacio de tutoría metodológica, técnica y de gobierno para el Trabajo Integrador Final de Posgrado en Ciencia de Datos.

El objetivo del Project no es solo generar texto o código, sino ayudar a terminar el TIF con orden, trazabilidad, rigor metodológico y viabilidad operativa.

## 2. Decisión fundacional

El TIF se enfocará en el análisis de patrones de mora y comportamiento crediticio en Argentina utilizando datos públicos sensibles.

El aporte principal será metodológico y analítico.

Las herramientas de IA se utilizarán como soporte de desarrollo, trazabilidad, revisión y documentación, pero no serán el objeto central del TIF.

## 3. Alcance actual

El alcance original se orienta al análisis temporal de la mora crediticia en Argentina.

Sin embargo, se reconoce que este objetivo depende de la estructura efectiva de los datos disponibles. En particular, depende de contar con identificadores persistentes, variable temporal confiable, variable de situación crediticia o mora, y continuidad suficiente para reconstruir trayectorias.

Por lo tanto, el alcance definitivo deberá validarse mediante una auditoría estratégica del repositorio y de la estructura de datos.

## 4. Hipótesis metodológica vigente

El TIF buscará construir un pipeline reproducible para analizar patrones crediticios y de mora con datos públicos sensibles.

Si los datos permiten reconstruir trayectorias temporales confiables, se priorizará un análisis temporal de mora mediante matrices de transición, deterioro, permanencia o mejora crediticia.

Si los datos no permiten sostener trayectorias temporales defendibles, el TIF podrá reformularse hacia una segmentación no supervisada de clientes, deudores o unidades crediticias mediante algoritmos de clusterización, como hito metodológico previo a una futura etapa temporal.

## 5. Rutas metodológicas posibles

### Ruta A — Análisis temporal de mora

Viable si existen:

- unidad de análisis persistente;
- variable temporal confiable;
- variable de situación crediticia o mora;
- varios períodos observables;
- continuidad suficiente;
- posibilidad de construir transiciones.

Posibles métodos:

- matrices de transición;
- análisis de deterioro, permanencia y mejora;
- modelos de tiempo discreto o supervivencia, si el alcance lo permite.

### Ruta B — Segmentación no supervisada de perfiles crediticios

Viable si no hay longitudinalidad suficiente, pero sí existe una estructura transversal rica.

Posibles métodos:

- K-Means;
- clustering jerárquico;
- Gaussian Mixture Models;
- DBSCAN o HDBSCAN, si corresponde;
- reducción dimensional para exploración;
- validación mediante métricas internas e interpretación de perfiles.

Esta ruta no debe presentarse como simple comparación de algoritmos, sino como identificación metodológica e interpretativa de perfiles crediticios.

## 6. Reglas de privacidad

Los datos son públicos, pero sensibles.

Reglas mínimas:

- no exponer datos crudos innecesariamente;
- no subir identificadores sensibles a herramientas cloud;
- trabajar con esquemas, agregados, muestras sintéticas o perfiles de datos;
- separar datos de código;
- excluir datos sensibles del repositorio;
- documentar decisiones de minimización y privacidad.

## 7. Rol de herramientas de IA

ChatGPT se usará para:

- tutoría metodológica;
- planificación;
- revisión crítica;
- documentación;
- preparación de prompts;
- control de alcance;
- revisión de decisiones.

GitHub Copilot o Codex en VSCode se usarán para:

- diagnóstico local;
- implementación guiada;
- refactorización;
- revisión de código;
- generación controlada de scripts;
- tareas técnicas acotadas.

Regla general:

Las herramientas de IA pueden asistir, pero no reemplazan la responsabilidad metodológica, analítica ni decisional del autor.

## 8. Mapa de conversaciones

### 00 — Control de avance y protocolo del TIF

Chat actual de gobierno del proyecto.

Uso permitido:

- registrar decisiones;
- controlar avance;
- mantener mapa de conversaciones;
- decidir próximos chats;
- detectar desvíos;
- definir criterios de avance.

No usar para:

- depuración extensa;
- implementación detallada;
- revisión completa de notebooks;
- redacción final extensa.

### 01 — Auditoría estratégica del repositorio y estructura de datos

Próximo chat especializado.

Objetivo:

Auditar el repositorio y la estructura de datos para determinar si el TIF debe sostener la Ruta A, temporal, o reformularse hacia la Ruta B, segmentación no supervisada.

## 9. Estado del repositorio

Repositorio remoto:

`Fede0808/tif_analisis_mora`

Repositorio local esperado:

`C:\Users\Federico\Dev\GitHub\tif_analisis_mora`

Incidencia resuelta:

Se detectó y eliminó un repositorio Git anidado accidental dentro de la carpeta raíz. La incidencia quedó resuelta cuando VSCode Source Control volvió a mostrar un solo repositorio.

## 10. Próximo paso operativo

Abrir el chat:

`01 — Auditoría estratégica del repositorio y estructura de datos`

Objetivo del próximo chat:

Determinar, a partir del estado real del repositorio y de los datos, qué alcance metodológico es viable para el TIF.

## 11. Reglas para nuevos chats

Cada nuevo chat debe:

1. respetar que el aporte principal del TIF es metodológico y analítico;
2. no convertir las herramientas de IA en el objeto central del trabajo;
3. distinguir decisiones cerradas, hipótesis y pendientes;
4. considerar la privacidad de datos públicos sensibles;
5. evitar implementación sin diagnóstico;
6. separar lo imprescindible, lo deseable y lo accesorio;
7. devolver próximos pasos concretos y defendibles.
