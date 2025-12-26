@echo off
chcp 65001 >nul
echo ================================================================================
echo Iniciando servidor Flask API...
echo ================================================================================
echo.

cd /d "%~dp0\..\.."

python backend\api\server_flask.py

if errorlevel 1 (
    echo.
    echo ================================================================================
    echo ERRO ao iniciar o servidor!
    echo ================================================================================
    echo.
    echo Verifique se as dependências estão instaladas:
    echo   pip install flask flask-cors pandas
    echo.
    pause
)

