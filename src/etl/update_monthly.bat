@echo off
echo =======================================================
echo    Mora BCRA - Actualizacion Mensual Automatizada
echo =======================================================
echo.

cd /d "%~dp0"
cd ..\..\..

echo [1/3] Ejecutando ETL (Extraccion, Transformacion y Carga DWH)...
.\.venv\Scripts\python.exe src\etl\run_pipeline_v2.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Falló la ejecución del ETL. Abortando.
    pause
    exit /b %ERRORLEVEL%
)
echo.

echo [2/3] Generando Data Mart Web Agregado (datamart_bancos.parquet)...
.\.venv\Scripts\python.exe c:\tmp\export_datamart_web.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Falló la creación del Data Mart. Abortando.
    pause
    exit /b %ERRORLEVEL%
)
echo.

echo [3/3] Subiendo cambios a GitHub...
git add data/dwh/datamart_bancos.parquet
git add data/dwh/datamart_fechas_origen.parquet
git commit -m "data: actualiza Data Mart de Mora BCRA con ultima informacion mensual"
git push

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Hubo un problema al subir a GitHub (verifica si hay cambios o si el repo esta conectado).
) else (
    echo [OK] Cambios publicados. Tu Dashboard en Streamlit Cloud se actualizara en breve.
)

echo.
echo =======================================================
echo      Actualizacion Completada Exitosamente
echo =======================================================
pause
