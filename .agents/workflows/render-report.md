---
description: Renderiza reportes en Quarto para el proyecto (quarto-publisher)
---
# Flujo de Trabajo: Render Report

Responsable: `quarto-publisher`

Renderiza un análisis o dashboard a formato PDF o HTML listo para ser compartido con los "stakeholders" o legisladores.

1. Instalar dependencias necesarias para publicación (opcional).
```powershell
pip install quarto jupyter
```

2. Ejecutar la compilación del reporte en Quarto.
// turbo
```powershell
quarto render notebooks/analisis_exploratorio.qmd --to html
```
