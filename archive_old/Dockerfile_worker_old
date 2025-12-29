# --- ETAPA 1: Constructor (Heavy) ---
FROM python:3.9-slim AS builder
WORKDIR /app

# Instalamos el compilador (pesado) solo para construir
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

COPY requirements.txt .
# Instalamos las librerías en una carpeta temporal (/install)
RUN pip install --prefix=/install -r requirements.txt

# --- ETAPA 2: Ejecutor (Lightweight) ---
FROM python:3.9-slim

WORKDIR /app

# Aquí solo instalamos la librería ligera para ejecutar (runtime)
# ¡Sin gcc ni herramientas de compilación!
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiamos SOLO las librerías ya cocinadas de la etapa anterior
COPY --from=builder /install /usr/local

# Copiamos tu código
COPY . .

CMD ["python", "main.py"]