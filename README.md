# 🌿 AgroSentinel v1.3: Inteligencia Climática IoT (Madrid Release)

**Estado:** 🟢 Estable (Cloud Ready - 2026)  
**Infraestructura:** Google Cloud Platform (Región: `europe-southwest1`, Madrid)  
**Stack:** Python 3.11 + Docker + Google Cloud SQL + n8n + Gemini IA  
**Misión:** Monitoreo de VPD y prevención de Estrés Hídrico en cultivos de Dos Hermanas.

## 🚀 Arquitectura de Microservicios Cloud-Native

Este ecosistema ha sido diseñado para la resiliencia y la baja latencia, migrando con éxito de Azure a GCP para optimizar el servicio en el sur de España.

* **🧠 AgroBot (Python/Flask):** API de ingestión que integra **Google Gemini 1.5 Flash** para generar diagnósticos biológicos automatizados.
* **☁️ Google Cloud SQL:** Persistencia PostgreSQL gestionada para garantizar la integridad de la telemetría histórica.
* **🤖 n8n Automator:** Orquestador de flujos de trabajo que transforma datos crudos en alertas de Microsoft Teams.
* **📊 Grafana Cloud:** Centro de visualización avanzada para métricas de VPD y humedad del suelo.

## 🔬 Ciencia Aplicada: El VPD (Déficit de Presión de Vapor)

AgroSentinel no solo mide datos; **entiende la planta**. Mediante el cálculo del VPD, el sistema identifica el estrés hídrico antes de que sea visible:
* **VPD > 2.0 kPa:** Riesgo crítico. La planta cierra estomas para evitar la deshidratación.
* **Detección Automática:** El sistema ha registrado picos de **2.183 kPa**, disparando alertas inmediatas de riego.

## 🛠️ Despliegue Rápido
```bash
git clone [https://github.com/jaaidi0/AgroSentinel.git](https://github.com/jaaidi0/AgroSentinel.git)
cd AgroSentinel
docker compose up -d --build
