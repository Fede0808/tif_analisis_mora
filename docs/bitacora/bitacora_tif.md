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

## Sesión 002 — Inicio de auditoría estratégica

**Fecha:** 2026-05-01; 13:39:00 14_19 pare a comer 15:28
**Chat:** 01 — Auditoría estratégica del repositorio y estructura de datos
**Tipo de sesión:** auditoría / diagnóstico
**Duración estimada:** pendiente
**Duración real:** pendiente

### Objetivo

Iniciar la auditoría estratégica del repositorio y de la estructura de datos para determinar qué alcance metodológico es viable para el TIF.

### Contexto de inicio

La auditoría deberá evaluar si el TIF puede sostener la Ruta A, orientada al análisis temporal de mora, o si conviene reformularlo hacia la Ruta B, orientada a segmentación no supervisada de perfiles crediticios.

### Insumos iniciales previstos

- Árbol de carpetas del repositorio.
- README y archivos de configuración.
- Notebooks y scripts principales.
- Descripción segura de la estructura de datos.
- Rango temporal, periodicidad y variables disponibles.
- Identificación de riesgos técnicos, metodológicos y de privacidad.

### Próximo paso

Trabajar en el Chat 01 hasta obtener un diagnóstico inicial del repositorio y de los datos.

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
