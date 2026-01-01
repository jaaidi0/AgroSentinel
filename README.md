# 🌿 AgroSentinel v1.3: Inteligencia Climática IoT (Madrid Release)

![AgroSentinel Architecture](static/dashboard.png)

> **Estado:** 🟢 Estable (Cloud Ready - 2026)
> **Infraestructura:** Google Cloud Platform (Región: europe-southwest1, Madrid)
> **Stack:** Python 3.11 + Docker + Google Cloud SQL + n8n + Gemini IA
> **Misión:** Monitoreo de VPD y prevención de Estrés Hídrico en cultivos de Dos Hermanas.

## 🚀 Arquitectura de Microservicios
* **🧠 AgroBot (Python/Flask):** API de ingestión con **Google Gemini 1.5 Flash** para análisis biológico en tiempo real.
* **☁️ Google Cloud SQL:** Persistencia PostgreSQL gestionada para alta disponibilidad de datos críticos.
* **🤖 n8n Automator:** Orquestación de alertas dinámicas enviadas a Microsoft Teams.
* **📊 Grafana Cloud:** Visualización avanzada de métricas (VPD, Humedad del suelo y Temperatura).

## 💡 ¿Por qué este proyecto?
AgroSentinel no solo mide datos; **entiende la planta**. Utilizando el cálculo de **Déficit de Presión de Vapor (VPD)**, el sistema identifica el momento exacto en que la planta cierra sus estomas para evitar la deshidratación, permitiendo un riego de precisión que ahorra agua y mejora la producción.

## 🛠️ Instalación y Despliegue
```bash
# Clonar y levantar en segundos
git clone [https://github.com/jaaidi0/AgroSentinel.git](https://github.com/jaaidi0/AgroSentinel.git)
cd AgroSentinel
docker compose up -d --build
