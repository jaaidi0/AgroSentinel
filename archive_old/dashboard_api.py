import os
import time
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# ---- Logging limpio ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("agrosentinel-api")
logging.getLogger("werkzeug").setLevel(logging.WARNING)  # menos ruido

# ---- Rutas absolutas ----
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# ---- Conexión DB (Azure/Postgres) ----
def get_engine():
    user_raw = os.getenv("AZURE_DB_USER") or ""
    user = user_raw.split("@")[0]  # limpia sufijo flexible server
    password = os.getenv("AZURE_DB_PASSWORD")
    host = os.getenv("AZURE_DB_HOST")
    port = os.getenv("AZURE_DB_PORT")
    dbname = os.getenv("AZURE_DB_NAME")
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={'sslmode': 'require'}
    )

engine = get_engine()

# ---- Caché simple 3s ----
CACHE = {"ts": 0.0, "data": None}
CACHE_TTL = 3.0

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "healthy", "db": "connected", "server": "Dos Hermanas"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.get("/api/latest")
def api_latest():
    now = time.time()
    if CACHE["data"] and (now - CACHE["ts"] < CACHE_TTL):
        return jsonify(CACHE["data"])
    try:
        with engine.connect() as conn:
            q = text("""
                SELECT * FROM (
                  SELECT ts, device_id, temperature_c, humidity_pct, vpd_kpa
                  FROM agro_telemetry
                  ORDER BY ts DESC LIMIT 30
                ) sub ORDER BY ts ASC
            """)
            rows = [dict(r._mapping) for r in conn.execute(q)]
        for r in rows:
            ts = r.get("ts")
            if hasattr(ts, "isoformat"):
                r["ts"] = ts.isoformat()
        payload = {"ok": True, "data": rows, "count": len(rows)}
        CACHE["ts"], CACHE["data"] = now, payload
        return jsonify(payload), 200
    except Exception as e:
        log.error(f"Error /api/latest: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# ---- Rutas del dashboard ----
@app.get("/")
def index():
    return send_from_directory(STATIC_DIR, "agro_dashboard.html")

@app.get("/styles.css")
def styles():
    return send_from_directory(STATIC_DIR, "styles.css")

@app.get("/favicon.ico")
def favicon():
    icon = os.path.join(STATIC_DIR, "favicon.ico")
    if os.path.exists(icon):
        return send_from_directory(STATIC_DIR, "favicon.ico")
    return ("", 204)

if __name__ == "__main__":
    # En producción real: Gunicorn/Waitress. Esto es dev server.
    app.run(host="0.0.0.0", port=5001)
