# Dockerfile para Railway (alternativa se Nixpacks não funcionar)
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Expõe porta
EXPOSE 5000

# Comando para iniciar (porta fixa 5000 para alinhar com Railway Target Port)
CMD gunicorn backend.api.server_flask:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120

