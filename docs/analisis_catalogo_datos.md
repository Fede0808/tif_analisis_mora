# Catálogo de Datos: Análisis y Propuesta

## 1. El Diagnóstico (El Caso de Uso)
El problema que acabamos de resolver (la ausencia de la columna `tipo_persona` y la extracción incorrecta de posiciones fijas) es un síntoma clásico de "deriva estructural" (Schema Drift). 

En el TIF:
- El ETL asumía un diseño de registro.
- El Dashboard asumía que el Data Warehouse exponía ciertas variables.
- Al no haber un "contrato firme" en el medio, ambos componentes se desincronizaron en tiempo de ejecución.

## 2. ¿Es necesario un Catálogo de Datos para este proyecto?

**Respuesta Técnica Corta:** *Sí y No.*

- **NO es estrictamente necesario implementar un catálogo corporativo pesado** (como Apache Atlas, Amundsen o DataHub). Al ser un proyecto individual o académico (TIF), levantar un contenedor Docker extra sólo para catalogación añadirá complejidad operativa y consumo de RAM sin retorno de inversión inmediato.

- **SÍ es absolutamente necesario un catálogo lógico "ligero" (Data Contract).** Hay que documentar de forma estructurada qué entra al DWH y qué sale. Este contrato es el que nos permitió hoy darnos cuenta de que la columna exigida por `app.py` no coincidía con el DWH real.

## 3. Implementación Propuesta (Ligera y Escalable)

Te propongo tres acciones proporcionales a un Lead Data Scientist resolviendo este escenario en un proyecto ágil:

### a) Definir un `schema.yml` (El Contrato Lógico)
Crear un archivo en `data/dwh/schema.yml` que defina explícitamente las tablas de DuckDB, las columnas y sus tipos. Herramientas analíticas modernas (como dbt o Cube.js) se basan en este principio.

### b) Agregar aserciones de calidad al ETL (Data Quality Checks)
Al final de `pipeline.py`, el proceso no solo debería decir "exporté Parquet", sino ejecutar checks. Por ejemplo:
- Validar que los montos no sean negativos.
- Validar que `tipo_persona` solo tenga valores esperados ("Física", "Jurídica", "Otra/Desconocida").

### c) Centralizar el diccionario de metadatos en Markdown
El `README.md` tiene arquitectura, pero no diccionario. Aprovechando que tenés una "Skill" llamada `doc-architect`, ese agente puede usar el archivo `.yml` para generar un diccionario de datos legible para humanos y guardarlo en `docs/data_dictionary.md`.

## 4. Beneficios concretos para el Dashboard
Teniendo el catálogo en YAML, el dashboard podría inicializarse leyendo ese esquema. Si la columna no está, Streamlit lanzaría un banner amistoso ("Falta la variable tipo_persona en el schema actual") en vez de crashear con una excepción críptica de DuckDB de `Binder Error`.
