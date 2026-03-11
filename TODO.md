# Pipeline de Tareas Pendientes (Backlog)

## 📌 Habilitar MCP GitHub
**Objetivo**: Integrar el Model Context Protocol para que Antigravity interactúe fluidamente con GitHub (PRs, issues, etc.).
* **¿Cómo obtener el GitHub Token?**
  1. Ingresa a tu cuenta en [GitHub.com](https://github.com/).
  2. Ve a **Settings (Configuración)** (haz clic en tu foto de perfil arriba a la derecha).
  3. Desplázate hasta abajo a la izquierda y selecciona **Developer settings** (Configuración de desarrollador).
  4. Haz clic en **Personal access tokens** -> **Tokens (classic)**.
  5. Clic en **Generate new token (classic)**.
  6. Escribe un nombre descriptivo en "Note" (ej: `antigravity-mcp-token`).
  7. Marca los permisos necesarios, usualmente el scope **`repo`** (para acceso completo a repositorios privados) y **`read:user`**.re
  8. Clic en **Generate token**. ¡Cópialo inmediatamente porque no lo volverás a ver! 

## 📌 Configurar Antigravity Custom Rules
**Objetivo**: Asegurar que las reglas de comportamiento del agente (Idioma y Rol de Mentor/Lead Data Scientist) persistirán en cualquier nuevo chat.
* **Aclaración Comercial/Técnica**: En algunas versiones y distribuciones recientes de la interfaz de Antigravity (o el IDE que estés usando, como VS Code con la extensión Gemini), la ruta *"Settings > Custom Rules"* puede variar o no estar habilitada explícitamente en la GUI. 
* **Solución transitoria**: Como buena práctica arquitectónica, ya hemos mitigado esto a nivel local. El archivo que creamos antes (`.agents/project_rules.md`) funcionará como la fuente de verdad ("single source of truth") de la configuración en este proyecto específico. Seguiremos iterando sobre los flujos de trabajo locales.

## 📌 Entorno Virtual e Instalación de Dependencias
- [x] Crear el entorno virtual (`.venv`).
- [x] Listar las dependencias extraídas deductivamente del código fuente (duckdb, streamlit, pandas, selenium, etc.).
- [x] Ejecutar instalación (`pip install -r requirements.txt`).

## 📌 Gobernanza y Calidad del DWH (Nuevas Tareas)
- [x] Implementar aserciones básicas al final del pipeline (validar conteos, ceros, negativos, dominios como `tipo_persona`).
- [x] Generar un Contrato de Datos Lógico ligero (Data Dictionary en YAML), útil para que el Dashboard o las variables sigan una definición documentada.

## 🔒 Anonimización Previa a Publicación Web *(Pendiente — Bloqueante para Deploy)*

> **Contexto**: El ETL mantiene temporalmente el `nro_identificacion` (CUIT/CUIL/CDI) en DuckDB para
> posibilitar el join entre la Central de Deudores del BCRA y el Padrón ARCA.
> **Antes de exponer el dataset en cualquier entorno web o público**, se deben completar los
> siguientes pasos de anonimización:

- [ ] **Aplicar hash SHA-256 con salt** al campo `nro_identificacion` para generar el `hash_id` definitivo.
  - El salt debe ser un secreto almacenado en `.env` (fuera del repositorio).
  - Usar `sha256(salt + cuit)` en DuckDB: `sha256(concat('$SALT', nro_identificacion))`.
- [ ] **Eliminar columnas con PII** del dataset exportado a Parquet de producción:
  - `nro_identificacion` (CUIT/CUIL en crudo).
  - `denominacion` (nombre/razón social).
  - `fecha_nac_contrato` y `fecha_fallecimiento` (datos sensibles individuales).
  - `cuit_reemplazo`.
- [ ] **Verificar** que ningún Parquet del directorio `data/dwh/parquet/` contenga CUITs en texto plano antes del deploy.
  - Script de validación: `assert 'nro_identificacion' not in parquet_df.columns`.
- [ ] **Documentar el proceso** en `CONTRIBUTING.md` como paso obligatorio previo a publicación.
- [ ] Revisión legal/ética del dataset final (contrastarlo con Ley 25.326 de Protección de Datos Personales).

---

## 📋 Estado del Proyecto al 2026-03-09 — Continuar Mañana

### ✅ Completado hoy
- **Bug de montos NaN resuelto**: los montos usaban coma decimal (`88,0`). Fix: `replace(',', '.')` antes del `CAST` en DuckDB. Verificado con 39.4M registros (avg $4.17M, max $678B).
- **DWH v2 reconstruido limpio**: `bcra_dwh_v2.duckdb` con datos correctos. Parquet exportados.
- **Dashboard actualizdo a schema v2**: `views.py` + `filters.py` + `app.py` reescritos. Streamlit corriendo en `localhost:8501`.
- **Diagnóstico de `dim_persona` vacía**: causa identificada → `load_padron_arca()` estaba comentado en el script de ejecución. Los widths del padrón son correctos (220 chars).
- **Verificación de `dias_atraso`**: ✅ correcto. El 97.86% en cero es metodológicamente válido (el BCRA permite clasificación cualitativa de riesgo sin mora acumulada).
- **Enriquecimiento postal investigado**: API `georef.datos.gob.ar` + CSV OpenDataCordoba disponibles para mapear código postal → localidad, provincia y coordenadas.

### 🔜 Próximos pasos (en orden de prioridad)

1. **🔴 Cargar Padrón ARCA** (`Padron_ARCA.txt`, 14 GB, ~30-60 min) — descomentar `load_padron_arca()` en `run_pipeline_v2.py` y lanzar en background. Esto pobla `dim_persona` y habilita el mapa.
2. **🟡 Descargar CSV códigos postales** de [OpenDataCordoba](https://github.com/OpenDataCordoba/codigo-postal-argentino) → cargar como `dim_codigo_postal` en el ETL → enriquece `dim_persona` con localidad, partido, latitud y longitud.
3. **🟡 Instalar `plotly`** en `.venv` y agregar a `requirements.txt`.
4. **🟡 Implementar 6 mejoras al dashboard** (aprobadas pendientes):
   - Eliminar tablas de registros individuales (clientes)
   - Histograma apilado por situación crediticia por banco (top 20 entidades)
   - Top 20 / Tail 20 por volumen de deuda (barras horizontales)
   - Mirada temporal: distribución `dias_atraso` + antigüedad en situación normal
   - Mapa de Argentina por provincia (`dim_persona` + `dim_codigo_postal`)
   - Scatter 3D entidades: ejes = tasa irregular / ratio previsiones / log(deuda)

### 📂 Archivos clave modificados hoy
- `src/etl/pipeline.py` — fix coma decimal en montos
- `src/dashboard/components/views.py` — reescritura completa, schema v2
- `src/dashboard/components/filters.py` — reescritura completa, schema v2
- `src/dashboard/app.py` — reescritura completa, schema v2
- `data/dwh/bcra_dwh_v2.duckdb` — reconstruido limpio con montos correctos
- `data/dwh/parquet/` — Parquet actualizados

### 📌 Notas metodológicas para el dashboard
- `dias_atraso = 0` en situaciones 3-5 es válido: el BCRA permite clasificación por análisis de riesgo
- Montos expresados en **miles de pesos con 1 decimal**
- `dim_persona` vacía hasta que se cargue el Padrón ARCA (14 GB)


### ✅ Completado hoy
- **ETL `pipeline.py` rediseñado** desde cero: 11 tablas, 22 campos en `fact_deuda_mensual`, autodescubrimiento de archivos, compatibilidad pandas ≥ 2.0.
- **Catálogo de datos** generado con todas las tablas y campos del LEAME DEUDORES + LEAME PADRON.
- **Pipeline v2 ejecutado** exitosamente: `bcra_dwh_v2.duckdb` con **39.4M registros** en `fact_deuda_mensual`.
- **Nota metodológica** agregada al dashboard (`app.py`).
- **Issue de anonimización** formalizado en `TODO.md`.

### 🔜 Próximos pasos (en orden de prioridad)
1. **Corregir montos NaN** en `fact_deuda_mensual` — los campos monetarios se están parseando como NULL. Revisar el offset posicional del campo de precio en `deudores.txt` (el separador `\0` puede no aplicar; probar con `read_fwf` de pandas con los `DEUDORES_WIDTHS`).
2. **Apuntar Streamlit al DWH v2** — actualizar la ruta en `src/dashboard/components/views.py` de `bcra_dwh.duckdb` → `bcra_dwh_v2.duckdb`.
3. **Implementar nuevas características en el dashboard** (ver propuestas en `walkthrough.md`):
   - Vista Deudores: flags de refinanciación, proceso judicial, antigüedad en situación normal, N° de entidades acreedoras.
   - Vista Entidades: tasa de cartera irregular, ratio previsiones/deuda, garantías preferidas A/B.
4. **Cargar Padrón ARCA** (`Padron_ARCA.txt`, 14 GB) — necesario para características geográficas, etarias y de actividad. Ejecutar `load_padron_arca()` en background con tiempo (puede tardar 30-60 min).
5. **Inicializar git** en el proyecto y hacer commit del estado actual.

### 📂 Archivos clave modificados hoy
- `src/etl/pipeline.py` — ETL completo rediseñado
- `src/dashboard/app.py` — nota metodológica
- `data/dwh/bcra_dwh_v2.duckdb` — nuevo DWH con esquema completo
- `data/dwh/parquet/` — todos los Parquet del nuevo esquema exportados


