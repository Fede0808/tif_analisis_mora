import sys
import subprocess
import platform
import importlib.util

def check_command(command, name):
    try:
        result = subprocess.run([command, '--version'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"[OK] {name} encontrado: {result.stdout.strip()}")
            return True
        else:
            print(f"[MISSING] {name} no responde como se esperaba. Salida: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
         print(f"[MISSING] {name} NO está instalado en el PATH.")
         return False

def check_package(package_name, display_name=None):
    if display_name is None:
        display_name = package_name
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"[OK] Paquete Python {display_name} instalado.")
        return True
    else:
        print(f"[MISSING] Paquete Python {display_name} NO está instalado.")
        return False

if __name__ == "__main__":
    print(f"--- Análisis del Entorno para Estudio de Mora BCRA ---")
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Versión de Python: {sys.version}")
    print("\n--- Herramientas del Sistema ---")
    
    check_command('git', 'Git')
    check_command('node', 'Node.js (Opcional, útil para herramientas frontend/MCP)')
    check_command('gh', 'GitHub CLI (Útil para automatización)')
    
    print("\n--- Bibliotecas Python Base (Costo $0) ---")
    req_packages = {
        'pandas': 'Pandas (Estructura de Datos)',
        'numpy': 'NumPy (Manejo matricial)',
        'selenium': 'Selenium (Sub-agente/Ingesta)',
        'streamlit': 'Streamlit (Dashboard)',
        'torch': 'PyTorch (Motor TraCeR)',
        'lifelines': 'Lifelines (Modelos de Supervivencia Clasicos)',
        'sklearn': 'Scikit-Learn (Métricas pre/post modelado)',
        'matplotlib': 'Matplotlib (Visualizaciones estáticas base)',
        'plotly': 'Plotly (Visualizaciones Streamlit interactivas)',
        'dotenv': 'python-dotenv (Manejo de credenciales/variables)'
    }
    
    missing_py = []
    for pkg, name in req_packages.items():
        if not check_package(pkg, name):
            missing_py.append(pkg)
            
    print("\n--- Resumen de Acciones Necesarias ---")
    if missing_py:
        print("Falta instalar las siguientes bibliotecas Python:")
        print(f" pip install {' '.join(missing_py)}")
    
    print("\nRecursos sugeridos a solicitar de GitHub (TraCeR architecture reference):")
    print(" - Implementación de PyTorch original de TraCeR (arXiv). Se deberá proveer/descargar o implementar desde paper.")
    
    print("\n[INFO] Todas las dependencias listadas son de código abierto y no representan costo económico.")
