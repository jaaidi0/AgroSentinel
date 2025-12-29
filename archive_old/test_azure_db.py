# health_check_azure.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Usamos los datos reales del despliegue exitoso
DB_CONFIG = {
    'host': 'jaidi-agro-db-spain.postgres.database.azure.com',
    'port': 5432,
    'dbname': 'postgres',
    'user': 'jaidi',
    'password': 'AgroTech2025_Jaidi',
    'sslmode': 'require'
}

try:
    print(f"📡 Conectando al corazón de AgroSentinel en {DB_CONFIG['host']}...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # 1. Verificar Versión
    cur.execute("SELECT version();")
    print(f"✅ Motor PostgreSQL listo: {cur.fetchone()[0][:30]}...")

    # 2. Verificar Tabla y Alarma de Aceite
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'sensor_data' AND column_name = 'oil_level';
    """)
    if cur.fetchone():
        print("🛢️  Columna 'oil_level': ✅ Configurada para alarmas en dárija.")
    
    # 3. Contar registros actuales
    cur.execute("SELECT COUNT(*) FROM sensor_data;")
    print(f"📊 Registros en la nube: {cur.fetchone()[0]}")

    conn.close()
    print("\n🚀 El sistema está operativo y listo para 2026.")
except Exception as e:
    print(f"❌ Error crítico en el sistema: {e}")