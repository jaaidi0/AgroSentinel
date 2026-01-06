FROM python:3.11-slim

WORKDIR /app

# Instalamos dependencias del sistema, FFmpeg y FUENTES para el texto del video
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    ffmpeg \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Gunicorn al final
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "python_worker.main:app"]