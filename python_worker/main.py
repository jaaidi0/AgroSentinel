import os
import logging
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from datetime import datetime

# --- 1. CONFIGURACIÓN (Mantenemos tu lógica original) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Variables de entorno
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'agro_db')
DB_USER = os.getenv('DB_USER', 'jaidi')
DB_PASS = os.getenv('DB_PASSWORD', 'password_segura_123')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# Motor de BD global
engine = create_engine(DATABASE_URL)

# --- 2. TU LÓGICA DE NEGOCIO (¡Intacta!) ---
def diagnostico_agronomo(temp, hum):
    """Tu algoritmo original para determinar riesgos."""
    if hum > 85 and temp > 20:
        return "PELIGRO CRÍTICO: Riesgo fúngico alto"
    elif hum > 70:
        return "ALERTA: Humedad excesiva"
    if temp > 35:
        return "ALERTA: Estrés térmico (Calor)"
    if temp < 5:
        return "PELIGRO: Riesgo de Helada"
    return "OPTIMO: Crecimiento Activo"

# --- 3. NUEVA API (La puerta para el ESP32) ---
@app.route('/api/sensor', methods=['POST'])
def recibir_datos():
    try:
        # 1. Recibir JSON del ESP32
        data = request.json
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # 2. Extraer valores (con valores por defecto por seguridad)
        sensor_id = data.get('sensor_id', 'unknown_esp32')
        temp = float(data.get('temperature', 0))
        hum = float(data.get('humidity', 0))

        # 3. Aplicar tu inteligencia agronómica
        estado_salud = diagnostico_agronomo(temp, hum)

        # 4. Guardar en Base de Datos
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO mediciones_clima (time, sensor_id, temperatura, humedad, riesgo_hongo) VALUES (NOW(), :s, :t, :h, :r)"),
                {"s": sensor_id, "t": temp, "h": hum, "r": estado_salud}
            )

        logger.info(f"📡 DATO RECIBIDO [{sensor_id}]: {temp}ºC | {hum}% -> {estado_salud}")
        return jsonify({"status": "success", "diagnosis": estado_salud}), 201

    except Exception as e:
        logger.error(f"❌ Error procesando dato: {e}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "AgroBot Online", "location": "Dos Hermanas"}), 200

# --- 4. ARRANQUE DEL SERVIDOR ---
if __name__ == "__main__":
    # Inicialización de tablas (solo al arrancar)
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS mediciones_clima (
                    time TIMESTAMPTZ NOT NULL,
                    sensor_id TEXT NOT NULL,
                    temperatura FLOAT,
                    humedad FLOAT,
                    riesgo_hongo TEXT
                );
            """))
            # Intentar activar TimescaleDB (si falla, ignora)
            try:
                conn.execute(text("SELECT create_hypertable('mediciones_clima', 'time', if_not_exists => TRUE);"))
            except:
                pass
        logger.info("✅ DB Inicializada.")
    except Exception as e:
        logger.error(f"⚠️ Error init DB: {e}")

    # ¡IMPORTANTE! host='0.0.0.0' permite conexiones desde fuera del contenedor
    logger.info("🚀 Servidor escuchando en puerto 5000...")
app.run(host='0.0.0.0', port=5000)