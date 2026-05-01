# Bitácora del TIF

## Sesión 001 — Constitución del centro de control y decisión fundacional

**Fecha:** 2026-05-01
**Chat:** 00 — Control de avance y protocolo del TIF
**Tipo de sesión:** planificación / gobierno metodológico
**Duración estimada:** 1 h
**Duración real:** 1 h 15 min

### Objetivo

Constituir el chat de control del TIF, ordenar el alcance inicial y registrar la decisión fundacional del trabajo.

### Decisiones tomadas

1. Este chat queda definido como “00 — Control de avance y protocolo del TIF”.
2. El TIF se enfocará en el análisis temporal de la mora crediticia en Argentina.
3. Se trabajará con datos públicos sensibles.
4. El aporte principal será metodológico y analítico.
5. Las herramientas de IA se utilizarán como soporte de desarrollo, trazabilidad y documentación.
6. Las herramientas de IA no serán el objeto central del TIF.
7. Las definiciones finas dependerán de la estructura real de los datos.
8. El próximo chat especializado será “01 — Auditoría estratégica del repositorio y estructura de datos”.

### Decisión metodológica pendiente de validación por datos

El objetivo marco del TIF se mantiene orientado al análisis de patrones de mora y comportamiento crediticio en Argentina con datos públicos sensibles.

Sin embargo, se reconoce que el alcance temporal originalmente planteado puede depender fuertemente de la estructura efectiva de los datos disponibles.

Se definen dos rutas metodológicas posibles:

1. **Ruta A — Análisis temporal de mora:** viable si los datos permiten reconstruir trayectorias por unidad de análisis a lo largo del tiempo.
2. **Ruta B — Segmentación o clasificación no supervisada de deudores/clientes:** alternativa viable si los datos permiten construir perfiles crediticios robustos, pero no trayectorias temporales confiables.

La auditoría estratégica del repositorio y de la estructura de datos deberá determinar cuál ruta es metodológicamente defendible para el TIF.

### Riesgos identificados

1. Definir metodología antes de auditar datos.
2. Sobredimensionar el rol de IA y agentes.
3. Convertir el TIF en un proyecto de ingeniería demasiado amplio.
4. No tratar adecuadamente datos públicos sensibles.
5. Construir backlog detallado antes de conocer el estado real del repositorio.

### Próximo paso

Preparar los insumos mínimos para abrir el chat:

**01 — Auditoría estratégica del repositorio y estructura de datos**.

### Pendientes

- Reunir árbol de carpetas del repositorio.
- Reunir README y archivos de configuración.
- Identificar notebooks y scripts principales.
- Describir la estructura de datos sin exponer registros sensibles.
- Registrar rango temporal, periodicidad y variables disponibles.

### Observaciones de control

Durante la sesión se detectó una incidencia técnica local vinculada a Git y VSCode: existencia de un repositorio Git anidado accidental. La incidencia fue priorizada antes de avanzar a la auditoría estratégica, porque podía afectar la trazabilidad del proyecto.

La resolución de esta incidencia consumió tiempo adicional no previsto, pero fue necesaria para asegurar que el repositorio quedara en condiciones mínimas de control antes de abrir la auditoría.

## Sesión 002 — Auditoría estratégica del repositorio y estructura de datos

**Fecha:** 2026-05-01
**Chat:** 01 — Auditoría estratégica del repositorio y estructura de datos
**Tipo de sesión:** auditoría técnica / metodológica / privacidad
**Duración estimada:** [2:30]
**Duración real:** [completar]

### Objetivo

Retomar la auditoría estratégica del repositorio y de la estructura de datos del TIF para determinar si los datos permiten sostener la Ruta A — análisis temporal de mora — o si corresponde reformular hacia la Ruta B — segmentación no supervisada de perfiles crediticios.

### Contexto

El TIF se enfoca en el análisis de patrones de mora y comportamiento crediticio en Argentina utilizando datos públicos sensibles. El aporte principal será metodológico y analítico. Las herramientas de IA se utilizan como soporte de desarrollo, trazabilidad, revisión y documentación, pero no constituyen el objeto central del TIF.

### Actividades realizadas

1. Se retomó el Chat 01 luego de una bifurcación operativa destinada a incorporar instrucciones y prompts para el uso controlado de asistentes de IA en el repositorio.
2. Se confirmó que se agregó y publicó una capa mínima de gobierno de agentes:
   - `.github/copilot-instructions.md`
   - `.github/prompts/repo-audit.prompt.md`
   - `.github/prompts/data-structure-audit.prompt.md`
   - `.github/prompts/privacy-review.prompt.md`
   - `.github/prompts/issue-writer.prompt.md`
   - `.github/prompts/implementation-task.prompt.md`
   - `.github/prompts/methodology-review.prompt.md`
   - `docs/ai-workflow/uso_agentes_tif.md`
   - `docs/ai-workflow/matriz_herramientas_ia.md`
   - `AGENTS.md`
3. Se registró el commit publicado:
   - `d0068d1 chore: add agent instructions and AI workflow prompts`
4. Se validó que:
   - `main` local quedó sincronizada con `origin/main`;
   - el working tree quedó limpio;
   - no se modificaron datos;
   - no se modificaron notebooks analíticos;
   - no se agregaron dependencias;
   - no se cambió el alcance metodológico del TIF.
5. Se actualizó el contexto con documentación normativa de la Central de Deudores del BCRA.
6. Se revisó la conveniencia de ejecutar la auditoría de estructura de datos usando Copilot Agent o Codex en VSCode con instrucciones específicas.
7. Se recibió un primer informe de auditoría local generado por el agente.

### Hallazgos principales

1. La estructura técnica del repositorio ya contiene elementos compatibles con una auditoría temporal:
   - `hash_id`;
   - `periodo_yyyymm`;
   - `fact_deuda_mensual`;
   - `fact_historial_24`;
   - `id_situacion`;
   - `dias_atraso`;
   - tablas dimensionales y parquets derivados.
2. El informe del agente clasifica preliminarmente la Ruta A como “viable con restricciones”.
3. La viabilidad de Ruta A todavía no está cerrada porque falta verificar empíricamente:
   - cantidad real de períodos distintos;
   - continuidad de `hash_id` entre períodos;
   - cantidad de unidades con más de una observación temporal;
   - duplicados por claves candidatas;
   - posibilidad efectiva de construir transiciones;
   - mapeo correcto de `mes_n` a `periodo_yyyymm` en `fact_historial_24`.
4. La Ruta B sigue vigente como alternativa si no se confirma continuidad temporal suficiente.
5. Persisten riesgos de privacidad que deben mantenerse bajo control:
   - presencia de datos crudos locales;
   - posible PII en parquets detallados;
   - uso de `nro_identificacion` y `denominacion` en algunas capas internas;
   - necesidad de validar datamarts publicables.

### Decisiones tomadas

1. No avanzar todavía a implementación.
2. No construir backlog operativo hasta cerrar la evidencia mínima de viabilidad metodológica.
3. Usar Copilot Agent o Codex solo como auditor operativo local, no como decisor metodológico.
4. Mantener ChatGPT como tutor metodológico para interpretar los resultados y decidir Ruta A o Ruta B.
5. Incorporar la documentación normativa de BCRA como marco de referencia, no como sustituto de la auditoría empírica de datos.

### Decisión metodológica pendiente

Determinar si el TIF sostiene:

- **Ruta A — análisis temporal de mora**, si se confirma continuidad longitudinal suficiente; o
- **Ruta B — segmentación no supervisada de perfiles crediticios**, si los datos no permiten reconstruir trayectorias defendibles.

### Próximo paso

Ejecutar localmente, sin modificar archivos ni exponer datos sensibles, las consultas de verificación mínima sobre DuckDB o parquets:

1. conteo de filas de `fact_deuda_mensual`;
2. mínimo, máximo y cantidad de períodos distintos;
3. cantidad de `hash_id` únicos;
4. cantidad y porcentaje de `hash_id` con más de un período;
5. duplicados por `hash_id + periodo_yyyymm`;
6. duplicados por `hash_id + cod_entidad + periodo_yyyymm`;
7. distribución agregada de `id_situacion` por período;
8. estado de `fact_historial_24`;
9. presencia de columnas sensibles en parquets;
10. evaluación preliminar de posibilidad de construir transiciones.

### Riesgos abiertos

1. Definir Ruta A sin evidencia empírica suficiente.
2. Subestimar la diferencia entre tener una variable temporal y tener verdadera longitudinalidad.
3. Exponer datos públicos sensibles o PII en archivos derivados.
4. Construir backlog antes de cerrar la decisión metodológica.
5. Sobredimensionar el rol de agentes o herramientas de IA.

### Estado al cierre de la sesión

La auditoría estratégica queda en curso.
La hipótesis vigente es: **Ruta A viable con restricciones**, pendiente de validación empírica mediante consultas agregadas sobre la estructura real de datos.

## Incidencias técnicas

### Incidencia 001 — Repositorio Git anidado accidental

**Fecha de detección:** 2026-05-01
**Estado:** resuelta
**Severidad:** media
**Tipo:** configuración local de repositorio / control de versiones
**Herramientas usadas:** VSCode, Git, Codex, ChatGPT

#### Descripción

Durante el commit inicial de la bitácora, VSCode Source Control mostró dos repositorios llamados `tif_analisis_mora`.

El diagnóstico confirmó que existía un repositorio Git anidado accidental en:

`C:\Users\Federico\Dev\GitHub\tif_analisis_mora\tif_analisis_mora`

Ese repositorio interno apuntaba al mismo remoto que el repositorio principal:

`https://github.com/Fede0808/tif_analisis_mora.git`

#### Evidencia técnica

Se verificó que existían dos carpetas `.git`:

1. `C:\Users\Federico\Dev\GitHub\tif_analisis_mora\.git`
2. `C:\Users\Federico\Dev\GitHub\tif_analisis_mora\tif_analisis_mora\.git`

El repositorio correcto era la raíz:

`C:\Users\Federico\Dev\GitHub\tif_analisis_mora`

La carpeta interna solo contenía:

- `.git`
- `.gitattributes`

No contenía archivos útiles del TIF ni la bitácora.

#### Riesgos

- Commits en el repositorio equivocado.
- Confusión visual en VSCode Source Control.
- Sincronización incorrecta con GitHub.
- Duplicación accidental de estructura.
- Pérdida de trazabilidad durante la auditoría del repositorio.

#### Acciones realizadas

1. Se verificó la raíz Git efectiva del repositorio principal.
2. Se confirmó que el remoto correcto era `Fede0808/tif_analisis_mora`.
3. Se inspeccionó el repositorio anidado.
4. Se desactivó el `.git` interno renombrándolo como `.git.disabled`.
5. Se revalidó que solo quedara un `.git` real.
6. Se eliminó la carpeta duplicada interna al confirmar que no contenía información útil.
7. Se verificó que VSCode Source Control ya no mostrara el repositorio duplicado.

#### Validación posterior

Resultado esperado y confirmado:

- Existe un único `.git` real en la raíz del repositorio.
- VSCode Source Control muestra un solo repositorio.
- El repositorio raíz está vinculado al remoto correcto.
- La carpeta duplicada ya no aparece como elemento no trackeado.
- El commit de la bitácora quedó realizado en el repositorio correcto.

#### Causa probable

Inicialización o clonación accidental de un repositorio dentro de la carpeta raíz del mismo repositorio.

#### Aprendizaje operativo

Antes de iniciar una auditoría metodológica o técnica del repositorio, debe validarse que:

1. VSCode tenga abierta la carpeta correcta.
2. Git detecte una única raíz.
3. No existan repositorios anidados accidentales.
4. El remoto corresponda al repositorio esperado.
5. `git status` esté limpio o los cambios pendientes estén justificados.

#### Tiempo insumido

**Tiempo estimado:** 20 min
**Tiempo real:** 20 min
**Evidencia temporal complementaria:** commit inicial de bitácora `216228e`, registrado el 2026-05-01 a las 11:27:57 -0300.
