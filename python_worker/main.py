import os
import math
import logging
import datetime as dt
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Configuración de Logging profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- CONFIGURACIÓN DE CONEXIÓN ROBUSTA ---
def get_engine():
    # Usamos .get() con valores por defecto para evitar errores tipo 'None'
    host = os.getenv("AZURE_DB_HOST")
    dbname = os.getenv("AZURE_DB_NAME")
    raw_user = os.getenv("AZURE_DB_USER")
    password = os.getenv("AZURE_DB_PASSWORD")
    port = os.getenv("AZURE_DB_PORT", "5432")  # Por defecto 5432 si es None

    # Verificación de seguridad
    if not all([host, dbname, raw_user, password]):
        logger.error("❌ ERROR: Faltan variables de entorno (Host, User, Pass o DBName).")
        raise RuntimeError("Configuración de base de datos incompleta.")

    # Limpieza del @ para compatibilidad con Azure Flexible Server
    user = raw_user.split('@')[0] if '@' in raw_user else raw_user
    
    # Construcción de la URL de conexión
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    
    logger.info(f"📡 Intentando conectar a la DB en: {host}")
    
    return create_engine(
        db_url, 
        connect_args={'sslmode': 'require'}, 
        pool_pre_ping=True, 
        future=True
    )

# Inicializar motor de base de datos
try:
    engine = get_engine()
except Exception as e:
    logger.critical(f"🔥 No se pudo inicializar el motor de DB: {e}")
    engine = None

def calculate_vpd(t_c: float, rh_pct: float) -> float:
    """Calcula el Déficit de Presión de Vapor (VPD) usando la fórmula de Tetens."""
    es = 0.6108 * math.exp((17.27 * t_c) / (t_c + 237.3))
    return round(es * (1.0 - rh_pct / 100.0), 3)

# --- RUTAS DE LA API ---

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "AgroBot Online", 
        "location": "Dos Hermanas",
        "db_connected": engine is not None
    }), 200

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json(silent=True) or {}
    
    # Validación de datos de entrada (Telemetría básica)
    required = ["temperaturec", "humiditypct", "soilpct"]
    if not all(k in data for k in required):
        return jsonify({"error": "Datos incompletos", "required": required}), 400

    # Procesamiento Científico (VPD)
    try:
        t = float(data["temperaturec"])
        rh = float(data["humiditypct"])
        soil = float(data["soilpct"])
        vpd_server = calculate_vpd(t, rh)
    except ValueError:
        return jsonify({"error": "Formato de datos numéricos inválido"}), 400

    payload = {
        "ts": dt.datetime.now(dt.timezone.utc),
        "device_id": data.get("deviceid", "unknown"),
        "temperature_c": t,
        "humidity_pct": rh,
        "soil_pct": soil,
        "vpd_kpa": vpd_server,
        "vpd_client": data.get("vpdkpa"),
        "source": data.get("source", "sim-wokwi")
    }

    # Persistencia en Azure
    try:
        if engine is None: raise Exception("Motor de DB no disponible")
        
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO agro_telemetry 
                (ts, device_id, temperature_c, humidity_pct, soil_pct, vpd_kpa, vpd_client, source)
                VALUES (:ts, :device_id, :temperature_c, :humidity_pct, :soil_pct, :vpd_kpa, :vpd_client, :source)
            """), payload)
        
        logger.info(f"✅ Registro OK | Device: {payload['device_id']} | VPD: {vpd_server}")
        return jsonify({"status": "stored", "vpd": vpd_server}), 201

    except Exception as e:
        logger.error(f"❌ Error en persistencia: {e}")
        return jsonify({"error": "Fallo al guardar en la nube"}), 500

if __name__ == "__main__":
    # El puerto 5000 es el estándar para despliegues en Azure y Docker
    app.run(host='0.0.0.0', port=5000)