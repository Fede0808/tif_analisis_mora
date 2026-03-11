---
description: Elimina celdas vacías y salidas de error en notebooks antes de un commit usando notebook-master.
---

# Limpieza de Jupyter Notebooks

Este workflow es conducido por tu perfil `notebook-master`.

1.  Localiza los archivos con extensión `.ipynb` que se han modificado recientemente en la carpeta `notebooks/`.
2.  Lee el contenido JSON del `.ipynb`.
3.  Elimina las salidas (outputs) para aligerar el tamaño del archivo y prevenir subidas masivas de datos a git.
4.  Elimina celdas de tipo "code" que se encuentren completamente vacías.
5.  (Opcional) Si el usuario lo solicita, extrae el código en un script Python `.py` equivalente en la carpeta de scripts o src.
