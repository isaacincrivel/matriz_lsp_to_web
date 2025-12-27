#!/bin/bash
# Script de start para Railway
# Este script inicia o servidor Flask usando Gunicorn

echo "🚀 Iniciando servidor Flask..."

# Verifica se a variável PORT está definida
if [ -z "$PORT" ]; then
    echo "⚠️  Variável PORT não definida, usando porta padrão 8000"
    export PORT=8000
fi

echo "📡 Iniciando servidor na porta $PORT..."

# Inicia o Gunicorn
exec gunicorn backend.api.server_flask:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

