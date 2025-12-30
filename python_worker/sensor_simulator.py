import os
import time
import random
import math
import requests
from colorama import Fore, init

init(autoreset=True)

# URL final de tu servicio en Google Cloud
API_URL = "https://agrosentinel-api-1061445067646.europe-west1.run.app/ingest"
SLEEP_S = 10

def run_simulation():
    print(f"{Fore.CYAN}🚀 AgroSentinel Sim v2.0 | Enviando a: {API_URL}")

    while True:
        # Simulación de Dos Hermanas / Castellón
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
            r = requests.post(API_URL, json=payload, timeout=5)
            if r.status_code == 201:
                res = r.json()
                color = Fore.GREEN if res['status'] == 'stored' else Fore.YELLOW
                print(f"{color}✅ DB: {res['status']} | VPD: {res['vpd']} | IA: {res['ia_advice']}")
            else:
                print(f"{Fore.RED}⚠️ Error API: {r.status_code}")
        except Exception as e:
            print(f"{Fore.RED}❌ Fallo de conexión: {e}")

        time.sleep(SLEEP_S)

if __name__ == "__main__":
    run_simulation()