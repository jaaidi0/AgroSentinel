import asyncio
import os
import sys
import math
import logging
import datetime as dt
from google import genai  # Generative AI SDK 2026
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import time

# Path fix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- CONFIGURATION ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- IA CONFIGURATION ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = None

client = None
if GEMINI_KEY:
    try:
        # Initialize client
        client = genai.Client(api_key=GEMINI_KEY, http_options={'api_version': 'v1beta'})
        logger.info("🧠 IA GenAI vinculada con éxito")

        # Fetch and set the model
        models = client.models.list()
        for model in models:
            if 'gemini-2.5-flash' in model.name:
                MODEL_NAME = model.name
                logger.info(f"Usando modelo: {MODEL_NAME}")
                break

        if not MODEL_NAME:
            raise ValueError("No se encontró un modelo válido como 'gemini-2.5-flash'.")

    except Exception as e:
        logger.error(f"❌ Error al conectar con Gemini: {e}")
else:
    logger.error("Gemini API key no configurada. Por favor, verifica el archivo .env.")

# --- DATABASE CONFIGURATION ---
def get_engine():
    user = os.getenv("DB_USER", "postgres")
    pw = os.getenv("DB_PASSWORD", "AgroUJI2025")
    db = os.getenv("DB_NAME", "agrodata")
    host = os.getenv("DB_HOST", "database")
    url = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
    return create_engine(url, pool_size=15, max_overflow=20, pool_pre_ping=True)

engine = get_engine()

@app.route('/')
def home():
    return jsonify({"service": "AgroSentinel PRO", "status": "online"}), 200

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json(silent=True) or {}
    try:
        t = float(data.get("temperaturec", 25))
        rh = float(data.get("humiditypct", 50))
        soil = float(data.get("soilpct", 30))

        # Calculate VPD
        es = 0.6108 * math.exp((17.27 * t) / (t + 237.3))
        vpd = round(es * (1.0 - rh / 100.0), 3)

        prompt = (
            f"SISTEMA: AgroSentinel\n"
            f"DATOS: T:{t}°C | HR:{rh}% | VPD:{vpd}kPa | Suelo:{soil}%\n"
            f"TAREA: Diagnóstico técnico (máx 10 palabras)."
        )

        advice = "Diagnóstico por defecto: IA no disponible."
        if client and MODEL_NAME:
            for attempt in range(3):  # Retry up to 3 times for availability
                try:
                    logger.info(f"Intentando generar contenido IA (intento {attempt+1})...")
                    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                    advice = response.text.strip()
                    break
                except Exception as e:
                    logger.error(f"Error IA (intento {attempt+1}): {e}")
                    if "503" in str(e):
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        break  # Other errors should not retry

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO agro_telemetry (ts, device_id, temperature_c, humidity_pct, soil_pct, vpd_kpa, source, ia_analysis)
                VALUES (:ts, :id, :t, :rh, :s, :v, :src, :ia)"""),
                {
                    "ts": dt.datetime.now(dt.timezone.utc),
                    "id": data.get("deviceid", "ESP32_UJI"),
                    "t": t, "rh": rh, "s": soil, "v": vpd,
                    "src": "madrid-prod", "ia": advice
                })

        return jsonify({"status": "stored", "vpd": vpd, "ia_advice": advice}), 201
    except Exception as e:
        logger.error(f"Error en ingest: {e}")
        return jsonify({"error": str(e)}), 400

# Video module
try:
    from video import produce_video
    logger.info("✅ Módulo de video cargado")
except ImportError:
    produce_video = None

@app.route("/generate-video", methods=["POST"])
def generate_video():
    if produce_video is None:
        return jsonify({"error": "Módulo de video no disponible"}), 503
    data = request.get_json(silent=True) or {}
    try:
        archivo = asyncio.run(produce_video(data.get("text", "Reporte"), data.get("vpd", 0), data.get("temp", 0)))
        return jsonify({"status": "success", "video": archivo}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
