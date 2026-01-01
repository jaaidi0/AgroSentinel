import os
import math
import logging
import datetime as dt
import google.generativeai as genai
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Configuración de Logs y Entorno
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 2. Configuración de Inteligencia Artificial (Gemini)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Motor de Base de Datos Optimizado
def get_engine():
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASSWORD")
    db = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST", "35.195.59.72")
    try:
        # Usamos pool_pre_ping para evitar desconexiones tras periodos de inactividad
        url = f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{db}"
        return create_engine(url, pool_size=10, max_overflow=20, pool_pre_ping=True)
    except Exception as e:
        logger.error(f"❌ Error al conectar con Cloud SQL: {e}")
        return None

engine = get_engine()

# 4. Lógica de Análisis Agronómico (IA)
def generar_analisis_ia(t, rh, vpd, soil):
    try:
        prompt = (
            f"Como experto agrónomo, analiza: Temp {t}°C, Humedad {rh}%, VPD {vpd}kPa, Suelo {soil}%. "
            "Dame un consejo técnico de máximo 15 palabras para el agricultor."
        )
        response = ai_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.warning(f"⚠️ Fallo en Gemini: {e}")
        return "Análisis IA temporalmente no disponible"

# 5. Rutas de la API
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "AgroBot Online",
        "timestamp": dt.datetime.now().isoformat(),
        "db_connected": engine is not None
    }), 200

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json(silent=True) or {}
    try:
        # Extracción de datos con valores por defecto de seguridad
        t = float(data.get("temperaturec", 25))
        rh = float(data.get("humiditypct", 50))
        soil = float(data.get("soilpct", 30))
        device_id = data.get("deviceid", "ESP32_UJI_PRO")
        
        # Cálculo físico del VPD (Vapor Pressure Deficit)
        # Fórmula: VPsat - VPactual
        es = 0.6108 * math.exp((17.27 * t) / (t + 237.3))
        vpd = round(es * (1.0 - rh / 100.0), 3)
        
        # Obtener análisis de la IA
        ia_report = generar_analisis_ia(t, rh, vpd, soil)
        
        # Guardado atómico en PostgreSQL
        if engine:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO agro_telemetry (ts, device_id, temperature_c, humidity_pct, soil_pct, vpd_kpa, source, ia_analysis) 
                    VALUES (:ts, :device_id, :t, :rh, :s, :v, :src, :ia)
                """), {
                    "ts": dt.datetime.now(dt.timezone.utc),
                    "device_id": device_id,
                    "t": t, "rh": rh, "s": soil, "v": vpd, "src": "sim-prod",
                    "ia": ia_report
                })
        
        logger.info(f"✅ Registro Exitoso: {device_id} | VPD: {vpd} | IA: {ia_report}")
        return jsonify({"status": "stored", "vpd": vpd, "ia_advice": ia_report}), 201

    except Exception as e:
        logger.error(f"💥 Error crítico en ingesta: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 400

if __name__ == "__main__":
    # Puerto 5000 abierto en Firewall de GCP
    app.run(host='0.0.0.0', port=5000)