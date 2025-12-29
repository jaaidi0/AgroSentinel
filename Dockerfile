# --- ETAPA 1: Constructor ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependencias de compilación
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requirements
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# --- ETAPA 2: Ejecutor (Producción) ---
FROM python:3.11-slim

WORKDIR /app

# Solo runtime de PostgreSQL (sin compiladores)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar librerías desde builder
COPY --from=builder /install /usr/local

# Copiar código de la aplicación
COPY python_worker ./python_worker

# Cambiar al directorio de trabajo
WORKDIR /app/python_worker

# Exponer puerto
EXPOSE 5000

# Variables de entorno (se sobrescribirán en Azure)
ENV PYTHONUNBUFFERED=1

# Comando de inicio con gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--timeout=600", "--workers=2", "main:app"]
