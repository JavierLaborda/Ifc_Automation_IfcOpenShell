@echo off
:: Establece la ruta a Python Portable
set PYTHON_PORTABLE=python_portable\python.exe

:: Verifica si Python Portable existe
if not exist %PYTHON_PORTABLE% (
    echo Python Portable no encontrado. Por favor, verifica la carpeta python_portable.
    pause
    exit /b
)

:: Ejecuta el script Python usando Python Portable
%PYTHON_PORTABLE% script.py

:: Pausa para ver los resultados
pause