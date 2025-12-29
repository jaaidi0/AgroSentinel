import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def create_infrastructure():
    # 1. Limpieza de credenciales (El truco que funcionó)
    raw_user = os.getenv("AZURE_DB_USER")
    user = raw_user.split('@')[0] if raw_user and '@' in raw_user else raw_user
    password = os.getenv("AZURE_DB_PASSWORD")
    host = os.getenv("AZURE_DB_HOST")
    port = os.getenv("AZURE_DB_PORT")
    dbname = os.getenv("AZURE_DB_NAME")

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(db_url, connect_args={'sslmode': 'require'})

    # 2. El Plano de la Tabla (SQL)
    # Incluimos vpd_kpa para tus cálculos de Tetens y vpd_client para auditoría
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS agro_telemetry (
        id BIGSERIAL PRIMARY KEY,
        ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        device_id TEXT NOT NULL,
        temperature_c REAL NOT NULL,
        humidity_pct REAL NOT NULL,
        soil_pct REAL NOT NULL,
        vpd_kpa REAL NOT NULL,
        vpd_client REAL NULL,
        source TEXT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_agro_ts ON agro_telemetry(ts);
    """

    try:
        with engine.begin() as conn:
            print(f"🏗️ Construyendo tabla en {host}...")
            conn.execute(text(create_table_sql))
            print("✅ TABLA 'agro_telemetry' CREADA O YA EXISTENTE.")
            
            # Verificación final
            res = conn.execute(text("SELECT count(*) FROM information_schema.tables WHERE table_name = 'agro_telemetry'")).scalar()
            if res:
                print("🚀 Sistema listo para recibir el registro #419.")
    except Exception as e:
        print(f"❌ Error al crear infraestructura: {e}")

if __name__ == "__main__":
    create_infrastructure()