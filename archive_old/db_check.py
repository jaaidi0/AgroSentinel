import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def check_cloud():
    # 1. Limpiamos el usuario programáticamente (evita el error del @)
    raw_user = os.getenv("AZURE_DB_USER")
    user = raw_user.split('@')[0] if raw_user and '@' in raw_user else raw_user
    
    password = os.getenv("AZURE_DB_PASSWORD")
    host = os.getenv("AZURE_DB_HOST")
    port = os.getenv("AZURE_DB_PORT")
    dbname = os.getenv("AZURE_DB_NAME")

    # 2. Construcción de URL limpia
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    
    print(f"📡 Intentando conectar como usuario: {user}")
    
    engine = create_engine(db_url, connect_args={'sslmode': 'require'})

    try:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT version();")).scalar()
            print(f"✅ ¡CONEXIÓN EXITOSA!")
            print(f"🖥️ {res[:50]}")
    except Exception as e:
        print(f"❌ Fallo exacto: {e}")

if __name__ == "__main__":
    check_cloud()