FROM python:3.11-slim
WORKDIR /app
# Instalamos dependencias para conectar con Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copiamos todo el proyecto
COPY . .
# Gunicorn buscará el objeto 'app' dentro de python_worker/main.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "python_worker.main:app"]