---
description: Crea el esquema y carga datos crudos a una base local .duckdb usando duckdb-engineer.
---

# Ingesta hacia DuckDB

El `duckdb-engineer` toma las riendas para optimizar los datos locales.

1.  Localiza los archivos fuente indicados (ej. múltiples CSVs en `data/raw/`).
2.  Formula consultas SQL nativas (`CREATE TABLE ... AS SELECT * FROM read_csv_auto(...)`).
3.  Ejecuta la inyección hacia un único archivo de base de datos `.db` o `.duckdb` (en `data/processed/`).
4.  Paralelamente, aprovecha el momento para limpiar nombres de columnas (snake_case) y normalizar tipos (str a numéricos/fechas).
5.  Muestra los primeros registros del almacén de datos ya curado como verificación.
