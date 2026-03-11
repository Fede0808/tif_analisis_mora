---
description: Configura el entorno y lanza el dashboard interactivo (streamlit-dev)
---
# Flujo de Trabajo: Deploy Streamlit

Responsable: `streamlit-dev`

Este workflow asegura que el entorno de visualización esté listo y despliega la aplicación local.

1. Instalar requerimientos (si no están ya instalados).
```powershell
pip install -r requirements.txt
```

2. Ejecutar la aplicación de análisis de mora.
// turbo
```powershell
streamlit run src/dashboard/app.py
```
