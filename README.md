# TIF Análisis Mora BCRA

Proyecto de integración final (TIF) enfocado en el procesamiento masivo de datos (Out-of-Core) del Banco Central de la República Argentina (BCRA) empleando DuckDB.

## Arquitectura y Componentes
- **Local Data Warehouse (DuckDB)**: Construcción de esquemas dimensionales limpios desde los archivos TXT crudos del BCRA.
- **EDA Automatizado (`eda-pro`)**: Herramienta de escaneo de tablas e informe de nulos/correlaciones (`scripts/run_eda.py`).
- **Dashboard Interactivo**: UI en Streamlit para visualizar la mora, dividiendo el impacto en Personas (Endeudamiento Familiar) vs Empresas (Personas Jurídicas).

## Workflows Disponibles (Antigravity Skills)

Este repositorio utiliza el framework de agentes `.agents` con diversas habilidades (`Skills`) para gestionar pipelines:

- `/run-eda data/dwh/bcra_dwh.duckdb`: Ejectuta diagnóstico sobre los datos cargados.
- `/doc-gen`: Actualiza esta misma documentación y los docstrings.
- `/clean-notebook`: Purgador de jupyter notebooks antes de commits.
- `/ingest-to-duckdb`: (Work-In-Progress)
- `/build-credit-report`: Pipeline para actualizar el Star Schema.
- `/deploy-streamlit`: Levanta el Dashboard analítico.
- `/render-report`: Publica Quarto notebooks.

## Uso

1. Activa tu entorno virtual (`.venv\Scripts\activate`)
2. Ingesta los datos: `python src/etl/pipeline.py`
3. Visualiza la herramienta ejecutando la tarea de deploy.
