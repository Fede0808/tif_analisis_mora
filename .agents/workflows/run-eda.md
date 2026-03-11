---
description: Genera un reporte rápido de la estructura de los datos (nulos, distribuciones, correlaciones) con eda-pro.
---

# Ejecución de EDA

Conducido por `eda-pro`. Toma un dataset crudo (CSV o Parquet) y realiza un diagnóstico automático.

1.  Lee la base de datos DuckDB de destino (ej: `data/dwh/bcra_dwh.duckdb`) o el archivo procesado que indique el usuario.
2.  Importa una muestra representativa de los datos usando `pandas` (o lee parciales para no saturar la RAM si es muy grande).
3.  Calcula métricas: Cantidad de nulos por columna, tipos de datos anómalos, estadísticos descriptivos rápidos.
4.  Identifica variables altamente correlacionadas (correlación > 0.8 o < -0.8).
5.  Escribe el resumen de los hallazgos en un archivo markown (ej: `reporte_eda.md`) en la carpeta de documentación o notebooks.
