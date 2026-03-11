import sys
import os
import pandas as pd
import numpy as np

def run_eda(file_path):
    """
    Ejecuta un Análisis Exploratorio de Datos (EDA) sobre un archivo o base de datos DuckDB.
    
    Toma la ruta del archivo y mediante pandas genera estadísticas descriptivas, detecta nulos, y 
    variables correlacionadas, resumiendo los hallazgos en `notebooks/reporte_eda.md`.
    
    Args:
        file_path (str): Ruta al archivo de datos a analizar o base de datos .duckdb local.
    """
    print(f"Iniciando EDA para: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no existe.")
        return
        
    # Inferir tipo de archivo y leer
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.txt'):
            # Intento de lectura para TXT delimitado
            # (El usuario puede tener separadores especiales, pruebo con tabulador o coma)
            with open(file_path, 'r') as f:
                first_line = f.readline()
                sep = '\t' if '\t' in first_line else ','
            df = pd.read_csv(file_path, sep=sep)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        elif file_path.endswith('.duckdb') or file_path.endswith('.db'):
            import duckdb
            conn = duckdb.connect(file_path, read_only=True)
            tables = conn.execute("SHOW TABLES").df()
            if tables.empty:
                print("La base de datos DuckDB no contiene tablas.")
                return
            
            dataframes = {}
            for table_name in tables.iloc[:, 0]:
                print(f"Base de datos de DuckDB: Analizando la tabla {table_name}...")
                df_table = conn.execute(f"SELECT * FROM {table_name} LIMIT 1000000").df()
                dataframes[table_name] = df_table
            conn.close()
        else:
            print("Formato de archivo no soportado nativamente en este script genérico.")
            return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Preparar el archivo de reporte
    report_path = "notebooks/reporte_eda.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    # Manejamos si dataframes no está definido (caso csv, parquet, etc)
    if 'dataframes' not in locals():
        dataframes = {os.path.basename(file_path): df}
        
    with open(report_path, "w", encoding='utf-8') as f:
        f.write(f"# Reporte EDA Automático\n\n")
        f.write(f"**Archivo analizado:** `{file_path}`\n\n")
        
        for table_name, df_actual in dataframes.items():
            f.write(f"---\n\n## Análisis de: {table_name}\n\n")
            
            # 1. Dimensiones basicas
            f.write("### 1. Visión General\n")
            f.write(f"- **Número de filas (vista):** {df_actual.shape[0]}\n")
            f.write(f"- **Número de columnas:** {df_actual.shape[1]}\n\n")

            # 2. Tipos de datos y nulos
            f.write("### 2. Tipos de Datos y Valores Nulos\n")
            f.write("| Columna | Tipo de Dato | Nulos | % Nulos |\n")
            f.write("|---------|--------------|-------|----------|\n")
            
            for col in df_actual.columns:
                null_count = df_actual[col].isnull().sum()
                null_pct = (null_count / len(df_actual)) * 100 if len(df_actual) > 0 else 0
                dtype = str(df_actual[col].dtype)
                f.write(f"| {col} | {dtype} | {null_count} | {null_pct:.2f}% |\n")
            f.write("\n")
            
            # 3. Estadísticos descriptivos rápidos
            f.write("### 3. Estadísticas Descriptivas (Variables Numéricas)\n")
            num_df = df_actual.select_dtypes(include=[np.number])
            if not num_df.empty:
                stats = num_df.describe().T
                f.write("```text\n")
                f.write(stats.to_string())
                f.write("\n```\n\n")
            else:
                f.write("*No hay variables numéricas para calcular estadísticas.*\n\n")
                
            # 4. Correlaciones Altas
            f.write("### 4. Variables Altamente Correlacionadas\n")
            if not num_df.empty and num_df.shape[1] > 1:
                corr_matrix = num_df.corr().abs()
                upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                
                high_corr = []
                for col in upper_tri.columns:
                    for idx, val in upper_tri[col].items():
                        if val > 0.8:
                            high_corr.append((idx, col, val))
                            
                if high_corr:
                    f.write("Se encontraron las siguientes correlaciones mayores o iguales a 0.8:\n")
                    f.write("| Variable 1 | Variable 2 | Correlación Absoluta |\n")
                    f.write("|------------|------------|----------------------|\n")
                    for var1, var2, val in high_corr:
                        f.write(f"| {var1} | {var2} | {val:.4f} |\n")
                else:
                    f.write("*No se encontraron correlaciones absolutas mayores a 0.8 entre variables numéricas.*\n")
            else:
                f.write("*No hay suficientes variables numéricas para calcular correlaciones.*\n")

        print(f"Reporte EDA generado exitosamente en: {report_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python run_eda.py <ruta_al_archivo>")
    else:
        file_path = sys.argv[1]
        run_eda(file_path)
