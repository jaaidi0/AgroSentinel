# 🌿 AgroSentinel v1.3: Inteligencia Climática IoT (Madrid Release)

![AgroSentinel Architecture](static/dashboard.png)

> **Estado:** 🟢 Estable (Cloud Ready - 2026)
> **Stack:** Python 3.11 + Docker + Google Cloud SQL + n8n + Gemini IA
> **Biología:** Monitoreo de VPD y Alerta de Estrés Hídrico en Dos Hermanas.

## 🚀 Arquitectura de Microservicios
* **🧠 AgroBot (Python/Flask):** API de ingestión que integra **Google Gemini 1.5 Flash** (v1beta) para análisis agronómico.
* **☁️ Google Cloud SQL:** Persistencia en PostgreSQL (Región Madrid).
* **🤖 n8n Automator:** Orquestación de alertas basadas en telemetría real enviadas a Teams.
* **📊 Grafana:** Dashboard dinámico para visualización de VPD y Humedad del Suelo.

## 🛠️ Despliegue
\`\`\`bash
docker compose up -d --build
\`\`\`
