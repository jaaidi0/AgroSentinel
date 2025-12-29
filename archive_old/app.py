# app.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", static_url_path='')
CORS(app)  # Permite peticiones desde cualquier origen

# --- API Endpoints ---

@app.get("/health")
def health():
    return jsonify({"ok": True, "status": "healthy"}), 200

@app.get("/api/latest")
def latest():
    # Simulación de datos para el dashboard
    return jsonify({
        "ok": True,
        "data": [
            {
                "device_id": "ESP32_INVERNADERO_01",
                "temperature_c": 24.6,
                "humidity_pct": 60.4,
                "vpd_kpa": 1.22,
                "ts": "2025-12-28T00:22:08+00:00"
            },
            {
                "device_id": "ESP32_EXTERIOR_01",
                "temperature_c": 24.43,
                "humidity_pct": 63.7,
                "vpd_kpa": 1.11,
                "ts": "2025-12-28T00:22:08+00:00"
            }
        ]
    }), 200

# --- Servir Dashboard HTML ---
@app.get("/")
def dashboard():
    return send_from_directory('static', 'agro_dashboard.html')

# --- Servir cualquier otro archivo estático (CSS, JS, etc.) ---
@app.get("/<path:filename>")
def static_files(filename):
    path = os.path.join(app.static_folder, filename)
    if os.path.exists(path):
        return send_from_directory(app.static_folder, filename)
    return "File not found", 404

# --- Run ---
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
