# 🌾 AgroSentinel v1.3: Sistema de Inteligencia Climática & IoT

> **Estado:** 🟢 Estable (Release v1.3 - Cloud Ready)
> **Stack:** Python + Docker + Azure PostgreSQL + n8n + Teams
> **Ciencia:** Cálculo de VPD (Fórmula de Tetens) & Punto de Rocío
> **Desarrollador:** El Mostapha Jaidi | Agro-Tech Developer & Biólogo

---

## 💡 ¿Qué es AgroSentinel?
**AgroSentinel** es un ecosistema de monitorización agrícola diseñado para **transformar datos climáticos en decisiones biológicas**. A diferencia de estaciones meteorológicas simples, diagnostica el estrés hídrico real de la planta en Dos Hermanas.

### 🧬 Lógica Agronómica
El sistema procesa variables crudas y calcula:
1.  **💧 VPD (Déficit de Presión de Vapor):** Mide la capacidad de transpiración.
    * **0.8 - 1.2 kPa:** Zona Óptima de Crecimiento.
2.  **🌫️ Punto de Rocío:** Alerta temprana de condensación y riesgo fúngico.

---

## 🚀 Arquitectura Híbrida (Edge + Cloud)
* **🧠 AgroBot (Python/Flask):** API de ingestión y control de riego alojada en Azure.
* **☁️ Azure PostgreSQL:** Persistencia de datos en la región de España (Madrid).
* **🤖 n8n Orquestador:** Vigilancia de umbrales y envío de Adaptive Cards a Teams.
* **🐳 Docker:** Despliegue profesional mediante contenedores.

---

## 🛠️ Instalación y Despliegue

### 1. Preparación Local
```bash
git clone [https://github.com/jaaidi0/AgroSentinel.git](https://github.com/jaaidi0/AgroSentinel.git)
cd AgroSentinel
cp .env.example .env