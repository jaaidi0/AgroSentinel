import os
import math
import logging
import datetime as dt
import google.generativeai as genai
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# --- CONFIGURACIÓN PROFESIONAL ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- IA CONFIG (SOLUCIÓN DEFINITIVA ERROR 404) ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
# Nombre limpio para evitar conflictos de URL en v1beta
MODEL_NAME = 'gemini-1.5-flash' 

genai.configure(api_key=GEMINI_KEY)

try:
    if GEMINI_KEY:
        ai_model = genai.GenerativeModel(model_name=MODEL_NAME)
        logger.info(f"🧠 IA vinculada con éxito: {MODEL_NAME}")
    else:
        ai_model = None
except Exception as e:
    logger.error(f"❌ Error al inicializar IA: {e}")
    ai_model = None

# --- PERSISTENCIA ROBUSTA ---
def get_engine():
    user = os.getenv("DB_USER", "postgres")
    pw = os.getenv("DB_PASSWORD", "AgroUJI2025")
    db = os.getenv("DB_NAME", "agrodata")
    host = os.getenv("DB_HOST", "database") # Sincronizado con docker-compose
    url = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
    return create_engine(url, pool_size=15, max_overflow=20, pool_pre_ping=True)

engine = get_engine()

@app.route('/')
def home():
    current_ip = request.host.split(':')[0]
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8"><title>AgroSentinel PRO</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; border-top: 8px solid #2e7d32; width: 380px; }}
            .status {{ color: #2e7d32; font-weight: bold; margin: 1.5rem 0; font-size: 1.2rem; }}
            .btn {{ display: block; padding: 14px; margin: 10px 0; border-radius: 10px; text-decoration: none; font-weight: 600; color: white; transition: 0.3s; }}
            .btn-grafana {{ background: #ef6c00; }}
            .btn-n8n {{ background: #1976d2; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌱 AgroSentinel v1.5</h1>
            <div class="status">🟢 NODO MADRID ONLINE</div>
            <a href="http://{current_ip}:3000" class="btn btn-grafana">📊 Panel de Control</a>
            <a href="http://{current_ip}:5678" class="btn btn-n8n">🤖 Automatización n8n</a>
        </div>
    </body>
    </html>
    """, 200

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json(silent=True) or {}
    try:
        t = float(data.get("temperaturec", 25))
        rh = float(data.get("humiditypct", 50))
        soil = float(data.get("soilpct", 30))
        
        # Cálculo de VPD
        es = 0.6108 * math.exp((17.27 * t) / (t + 237.3))
        vpd = round(es * (1.0 - rh / 100.0), 3)
        
        # IA con Fallback Silencioso
        advice = "Revisar transpiración."
        if ai_model:
            try:
                prompt = f"Como agrónomo experto: T{t}C, H{rh}%, VPD{vpd}kPa, Suelo{soil}%. Da un consejo técnico de 8 palabras."
                advice = ai_model.generate_content(prompt).text.strip()
            except:
                advice = "IA analizando datos bióticos..."

        # Guardado en DB
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO agro_telemetry (ts, device_id, temperature_c, humidity_pct, soil_pct, vpd_kpa, source, ia_analysis) 
                VALUES (:ts, :id, :t, :rh, :s, :v, :src, :ia)"""),
                {"ts": dt.datetime.now(dt.timezone.utc), "id": data.get("deviceid", "ESP32_UJI"), "t": t, "rh": rh, "s": soil, "v": vpd, "src": "madrid-prod", "ia": advice})
        
        return jsonify({"status": "stored", "vpd": vpd, "ia_advice": advice}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)