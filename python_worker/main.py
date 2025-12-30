import os
import math
import logging
import datetime as dt
import google.generativeai as genai
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Configuración de Logging Profesional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- CONFIGURACIÓN IA ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ai_model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
# --- MOTOR DE BASE DE DATOS MEJORADO ---
def get_engine():
    # Variables unificadas para máxima compatibilidad
    user = os.getenv("DB_USER") or os.getenv("AZURE_DB_USER")
    password = os.getenv("DB_PASSWORD") or os.getenv("AZURE_DB_PASSWORD")
    db_name = os.getenv("DB_NAME") or os.getenv("AZURE_DB_NAME")
    instance_connection = os.getenv("INSTANCE_CONNECTION_NAME")
    
    try:
        if instance_connection:
            # ✅ MODO GOOGLE CLOUD (Socket de Unix)
            db_url = f"postgresql+psycopg2://{user}:{password}@/{db_name}?host=/cloudsql/{instance_connection}"
            logger.info(f"🌐 Conectando a Cloud SQL via Socket: {instance_connection}")
            return create_engine(db_url, pool_pre_ping=True)
        else:
            # ✅ MODO LOCAL / AZURE (TCP)
            host = os.getenv("DB_HOST") or os.getenv("AZURE_DB_HOST") or "localhost"
            db_url = f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db_name}"
            # Solo forzar SSL si detectamos que es Azure
            ssl_args = {'sslmode': 'require'} if host and "azure" in host.lower() else {}
            return create_engine(db_url, connect_args=ssl_args, pool_pre_ping=True)
    except Exception as e:
        logger.error(f"❌ Error al configurar SQLAlchemy: {e}")
        return None

engine = get_engine()

def calculate_vpd(t, rh):
    es = 0.6108 * math.exp((17.27 * t) / (t + 237.3))
    return round(es * (1.0 - rh / 100.0), 3)

def pedir_consejo_ia(t, rh, soil, vpd):
    prompt = f"Como agrónomo experto de la UJI en Castellón, analiza: Temp {t}°C, HR {rh}%, Suelo {soil}%, VPD {vpd}kPa. Dame un consejo de riego breve (máximo 15 palabras)."
    try:
        response = ai_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.warning(f"⚠️ IA no disponible: {e}")
        return "IA analizando tendencias climáticas..."

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "AgroBot Online", "db_connected": engine is not None}), 200

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json(silent=True) or {}
    try:
        t = float(data.get("temperaturec", 25))
        rh = float(data.get("humiditypct", 50))
        soil = float(data.get("soilpct", 30))
        dev_id = data.get("deviceid", "ESP32_GENERIC")
        
        vpd = calculate_vpd(t, rh)
        consejo = pedir_consejo_ia(t, rh, soil, vpd)
        
        db_status = "skipped"
        if engine:
            try:
                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO agro_telemetry (ts, device_id, temperature_c, humidity_pct, soil_pct, vpd_kpa, source) 
                        VALUES (:ts, :device_id, :t, :rh, :s, :v, :src)
                    """), {
                        "ts": dt.datetime.now(dt.timezone.utc),
                        "device_id": dev_id, "t": t, "rh": rh, "s": soil, "v": vpd, "src": data.get("source", "sensor-network")
                    })
                db_status = "stored"
            except Exception as e:
                logger.error(f"🔥 Error en DB: {e}")
                db_status = "error"

        return jsonify({"status": db_status, "vpd": vpd, "ia_advice": consejo}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))