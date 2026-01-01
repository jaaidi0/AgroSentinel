import os
import time
import random
import math
import requests
from colorama import Fore, init

init(autoreset=True)

# 1. Priorizamos la variable de entorno, si no existe usamos la IP de Madrid
# Línea 11 aproximadamente
API_URL = "http://34.175.53.215:5000/ingest"
SLEEP_S = 10

def run_simulation():
    # 2. Usamos API_URL que es la que tiene la dirección correcta
    print(f"{Fore.CYAN}🚀 AgroSentinel Sim v2.0 | Enviando a: {API_URL}")

    while True:
        temp = round(25.0 + 5 * math.sin(time.time()/3600), 2)
        hum = round(50.0 + random.uniform(-5, 5), 1)
        soil = round(30.0 + random.uniform(-2, 2), 1)

        payload = {
            "deviceid": "ESP32_UJI_PRO",
            "temperaturec": temp,
            "humiditypct": hum,
            "soilpct": soil,
            "source": "sim-prod"
        }

        try:
            # 3. La petición ahora va a la IP de la VM en Madrid
            r = requests.post(API_URL, json=payload, timeout=30)
            if r.status_code in [200, 201]: # Aceptamos ambos códigos de éxito
                res = r.json()
                # Ajustamos las claves según lo que devuelva tu API
                status = res.get('status', 'ok')
                vpd = res.get('vpd', 'N/A')
                ia = res.get('ia_advice', 'Procesando...')
                
                color = Fore.GREEN if status == 'stored' else Fore.YELLOW
                print(f"{color}✅ DB: {status} | VPD: {vpd} | IA: {ia}")
            else:
                print(f"{Fore.RED}⚠️ Error API: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"{Fore.RED}❌ Fallo de conexión: {e}")

        time.sleep(SLEEP_S)

if __name__ == "__main__":
    run_simulation()