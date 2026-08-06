@echo off
title DASH MEDIDORES

cd /d "%~dp0"

echo ==========================================
echo          DASH MEDIDORES
echo ==========================================
echo.
echo Iniciando processamento...
echo.

python main.py

echo.
echo ==========================================
echo Processo finalizado.
echo ==========================================
echo.

pause