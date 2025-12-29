# 🌾 AgroSentinel v1.3: Sistema de Inteligencia Climática & IoT

![AgroSentinel Architecture](dashboard.png)

> **Estado:** 🟢 Estable (Release v1.3 - Cloud Ready)
> **Stack:** Python + Docker + Azure PostgreSQL + n8n + Teams
> **Ciencia:** Cálculo de VPD (Fórmula de Tetens) & Punto de Rocío
> **Desarrollador:** El Mostapha Jaidi | Agro-Tech Developer & Biólogo

---

## 💡 ¿Qué es AgroSentinel?
**AgroSentinel** es un ecosistema de monitorización agrícola diseñado para **transformar datos climáticos en decisiones biológicas**. No es solo una estación meteorológica; es una herramienta de diagnóstico que mide el estrés hídrico real de la planta en Dos Hermanas mediante el cálculo del **Déficit de Presión de Vapor (VPD)**.

### 🧬 Inteligencia Biológica Aplicada
El sistema no solo lee sensores; aplica lógica agronómica en tiempo real:
1.  **💧 VPD (Déficit de Presión de Vapor):** Mide la capacidad de transpiración.
    * **0.8 - 1.2 kPa:** Zona Óptima de Crecimiento.
2.  **🌫️ Punto de Rocío:** Alerta temprana de condensación y riesgo fúngico para prevenir plagas antes de que aparezcan.

---

## 🚀 Arquitectura Híbrida (Edge + Cloud)
* **🧠 AgroBot (Python/Flask):** API de ingestión y control alojada en **Azure App Service**.
* **☁️ Azure PostgreSQL:** Persistencia de datos profesional en la región de España (Madrid).
* **🤖 n8n Orquestador:** Vigilancia activa de umbrales y envío de **Adaptive Cards** interactivas.
* **🐳 Docker:** Despliegue profesional mediante contenedores multi-etapa para máxima eficiencia.

---

## 🛠️ Instalación y Despliegue

### 1. Preparación Local
```bash
git clone [https://github.com/jaaidi0/AgroSentinel.git](https://github.com/jaaidi0/AgroSentinel.git)
cd AgroSentinel
cp .env.example .env