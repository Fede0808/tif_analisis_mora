---
description: Procesa datos de deudores del BCRA y genera KPIs financieros (duckdb-engineer + finance-dashboard-agent)
---
# Flujo de Trabajo: Build Credit Report

Este flujo de trabajo es gestionado por la habilidad `finance-dashboard-agent`. 
Se encarga de tomar los datos crudos, pasarlos por el ETL de DuckDB y preparar el lanzamiento del dashboard de Streamlit separado por perfiles de riesgo crediticio (Personas vs Empresas).

## Pasos

1. Ejecutar el pipeline ETL de DuckDB para ingestar y dimensionar los datos del BCRA.
// turbo
```powershell
python src/etl/pipeline.py
```

2. Validar que los archivos Parquet se han generado en `data/dwh/parquet`.
// turbo
```powershell
ls data/dwh/parquet
```

3. Instalar dependencias si faltan (opcional, requiere `uv` o `pip`).
// turbo
```powershell
uv pip install -r requirements.txt
```

4. Lanzar el Dashboard de Streamlit.
```powershell
streamlit run src/dashboard/app.py
```
