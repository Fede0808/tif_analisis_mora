---
description: Escanea el proyecto y actualiza toda la documentación pendiente usando doc-architect.
---

# Generar y Actualizar Documentación

Este workflow utiliza el agente `doc-architect` para escanear y generar documentación.

1.  Analiza la estructura del proyecto explorando las carpetas principales (ej: `src/`, `data/`).
2.  Busca archivos que no tengan docstrings (en Python) o JSDoc (en JS/TS).
3.  Autogenera y añade estos docstrings.
4.  Revisa el `README.md` de la raíz del proyecto y actualiza su contenido basándose en las últimas modificaciones del código.
5.  Revisa la carpeta `docs/` o similares y crea o actualiza diagramas (mermaid) si hay cambios arquitectónicos.
