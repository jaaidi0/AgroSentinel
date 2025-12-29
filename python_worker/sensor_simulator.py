import os
import time
import random
import math
import requests
from colorama import Fore, init

init(autoreset=True)

# Configuración desde el .env (o valores por defecto)
API_URL = os.getenv("AGRO_API_URL", "http://localhost:5000/ingest")
SLEEP_S = int(os.getenv("SIM_INTERVAL_S", "10"))

SENSORS = [
    {'id': 'ESP32_INVERNADERO_01', 'type': 'interior'},
    {'id': 'ESP32_EXTERIOR_01', 'type': 'exterior'}
]

def saturation_vapor_pressure(t_c):
    return 0.6108 * math.exp((17.27 * t_c) / (t_c + 237.3))

def calculate_vpd(t_c, rh_pct):
    return round(saturation_vapor_pressure(t_c) * (1.0 - rh_pct / 100.0), 3)

def run_simulation():
    print(f"{Fore.CYAN}🚀 Iniciando Sensores de AgroSentinel...")
    print(f"{Fore.YELLOW}📡 Enviando datos a: {API_URL}")

    while True:
        for sensor in SENSORS:
            # Simulación física realista para Dos Hermanas
            temp = round(22.0 + 3 * math.sin(time.time()/3600) + random.uniform(-0.5, 0.5), 2)
            hum = round(60.0 + random.uniform(-5, 5), 1)
            soil = round(45.0 + random.uniform(-2, 2), 1)
            vpd = calculate_vpd(temp, hum)

            # Preparamos el JSON para la API
            payload = {
                "deviceid": sensor['id'],
                "temperaturec": temp,
                "humiditypct": hum,
                "soilpct": soil,
                "vpdkpa": vpd,
                "source": "sim-wokwi"
            }

            try:
                # El momento del envío: Sensor -> Flask -> Azure
                r = requests.post(API_URL, json=payload, timeout=5)
                if r.status_code == 201:
                    print(f"{Fore.GREEN}✅ {sensor['id']} -> Enviado OK | VPD: {vpd} kPa")
                else:
                    print(f"{Fore.RED}⚠️ Error {r.status_code}: {r.text}")
            except Exception as e:
                print(f"{Fore.RED}❌ Fallo de conexión con la API: {e}")

        time.sleep(SLEEP_S)

if __name__ == "__main__":
    run_simulation()