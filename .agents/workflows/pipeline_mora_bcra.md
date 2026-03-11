---
description: Pipeline End-to-End Estudio de Mora BCRA
---

Este workflow orquesta la ejecución del pipeline completo de ingesta, visualización y preparación del entorno para el modelado de mora del BCRA. Requiere autorización explícita para modificaciones de sistema.

## 0. Verificar Entorno
```bash
py scripts\check_environment.py
```

## 1. Instalar Dependencias
Instalación de las librerías base necesarias para el proyecto.
```bash
pip install pandas numpy selenium streamlit torch lifelines scikit-learn matplotlib plotly python-dotenv
```

## 2. Ingesta de Datos Automatizada (Selenium)
Ejecuta el scraper para descargar los datos `Cheques y Deudores` al directorio `data/raw/` de manera autenticada.
```bash
py src\data\ingest_bcra.py
```

## 3. Lanzar Dashboard Interactivo (Streamlit)
Levanta el dashboard post-EDA para previsualizar filtros e insights anonimizados.
```bash
streamlit run src\dashboard\app.py
```
*(Nota: Para ingresar utiliza el usuario `admin` y clave `bcra2026`).*

## 4. Ejecutar Modelos TraCeR / Hazard
Ejecuta y compila el Jupyter Notebook final con los datos limpios.
```bash
jupyter lab notebooks\final_report.ipynb
```
