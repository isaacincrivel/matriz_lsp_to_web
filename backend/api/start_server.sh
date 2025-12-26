#!/bin/bash
echo "================================================================================"
echo "Iniciando servidor Flask API..."
echo "================================================================================"
echo ""

cd "$(dirname "$0")/../.."

python3 backend/api/server_flask.py

if [ $? -ne 0 ]; then
    echo ""
    echo "================================================================================"
    echo "ERRO ao iniciar o servidor!"
    echo "================================================================================"
    echo ""
    echo "Verifique se as dependências estão instaladas:"
    echo "  pip install flask flask-cors pandas"
    echo ""
    read -p "Pressione Enter para continuar..."
fi

