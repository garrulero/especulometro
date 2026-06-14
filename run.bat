@echo off
title Especulometro - Iniciar Proyecto
echo ===================================================
echo   Iniciando Especulometro Vasco (Back + Front)
echo ===================================================

:: Cambiar al directorio del script
cd /d "%~dp0"

:: Iniciar el backend de FastAPI
echo [1/2] Iniciando Backend en puerto 8000...
start "Especulometro - Backend API" cmd /k "cd front && python server.py"

:: Iniciar el frontend de Next.js
echo [2/2] Iniciando Frontend en puerto 3000...
start "Especulometro - Frontend App" cmd /k "cd front && if not exist node_modules (echo Instalando dependencias, esto puede tardar un poco... && npm install) && npm run dev"

echo ===================================================
echo   Ambos servicios se han lanzado en ventanas nuevas.
echo ===================================================
pause
