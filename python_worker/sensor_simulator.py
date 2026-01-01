import time, random, math, requests
from colorama import Fore, init

init(autoreset=True)
API_URL = "http://127.0.0.1:5000/ingest"

def run_simulation():
    print(f"{Fore.CYAN}🚀 Desplegando telemetría en Nodo Madrid...")
    while True:
        payload = {
            "deviceid": "ESP32_UJI_PRO",
            "temperaturec": round(25 + 5 * math.sin(time.time()/3600), 2),
            "humiditypct": round(50 + random.uniform(-5, 5), 1),
            "soilpct": round(30 + random.uniform(-2, 2), 1)
        }
        try:
            r = requests.post(API_URL, json=payload, timeout=10)
            if r.status_code == 201:
                res = r.json()
                print(f"{Fore.GREEN}✅ DB: {res['status']} | VPD: {res['vpd']} | IA: {res['ia_advice']}")
            else:
                print(f"{Fore.RED}⚠️ Error {r.status_code}")
        except Exception as e:
            print(f"{Fore.RED}❌ Fallo: {e}")
        time.sleep(10)

if __name__ == "__main__":
    run_simulation()