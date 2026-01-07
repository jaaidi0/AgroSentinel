# 🌿 AgroSentinel v1.4 | Multi-Cloud AI Intelligence

<p align="center">
  <img src="static/dashboard.png" alt="AgroSentinel Dashboard" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.4_Frankfurt-success?style=for-the-badge&logo=github" alt="Release">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Cloud-Hybrid_GCP_&_DigitalOcean-blue?style=for-the-badge&logo=digitalocean&logoColor=white" alt="Hybrid Cloud">
  <img src="https://img.shields.io/badge/IA-Gemini_2.5_Flash-orange?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini">
</p>

---

## 🛰️ Visión General
**AgroSentinel** ha evolucionado. De una estación local a una infraestructura **Multi-Cloud** distribuida. Fusiono la fisiología vegetal con la ingeniería de datos para prevenir el estrés hídrico en tiempo real mediante el cálculo preciso del **VPD (Vapor Pressure Deficit)** y diagnósticos generados por IA.

> "Del microscopio al teclado: ciencia convertida en sistemas inteligentes para la agricultura."

---

## ✨ Características v1.4 (The Frankfurt Update)

| Funcionalidad | Descripción Técnica | Impacto |
| :--- | :--- | :--- |
| **🎬 AI Video Reports** | Generación automática de vídeo con **FFmpeg**, **Edge-TTS** y lógica Python. | Reportes visuales inmediatos del estado del cultivo. |
| **🧠 Gemini 2.5 Flash** | Cerebro narrativo que interpreta datos biológicos complejos. | Diagnósticos expertos en lenguaje agronómico humano. |
| **🌍 Multi-Cloud Core** | Despliegue híbrido: **GCP (Madrid)** para telemetría y **DigitalOcean (Frankfurt)** para IA. | Resiliencia internacional y procesamiento distribuido. |
| **🤖 n8n Automation** | Orquestación total entre PostgreSQL, Gemini y sistemas de alerta. | Cero intervención humana en la cadena de decisión. |

---

## 🏗️ Arquitectura del Sistema

1. **Nodo Madrid (GCP):** Ingesta de datos IoT de baja latencia.
2. **Nodo Frankfurt (DigitalOcean):** Procesamiento pesado, Renderizado de vídeo y Orquestación n8n.
3. **Análisis:** Motor de cálculo VPD basado en la ecuación de Tetens.
4. **Visualización:** Dashboards en **Grafana Cloud** y reportes multimedia automáticos.

---

## 🔬 El Corazón del Sistema: Control de VPD
El **VPD** es el motor de la transpiración. AgroSentinel monitoriza estos rangos críticos:

* 🔵 **0.4 - 0.8 kPa:** Riesgo fúngico (Humedad excesiva).
* 🟢 **0.8 - 1.2 kPa:** **ZONA ÓPTIMA** de crecimiento.
* 🔴 **> 1.6 kPa:** **ALERTA CRÍTICA**. Activación del motor de IA y generación de vídeo-reporte.

---

## 🛠️ Stack Tecnológico

| Área | Tecnologías |
| :--- | :--- |
| **Backend** | `Python 3.11`, `FastAPI`, `Gunicorn` |
| **IA & Orquestación** | `Google Gemini 2.5 Flash`, `n8n` |
| **Infraestructura** | `Docker`, `Docker Compose`, `DigitalOcean`, `GCP` |
| **Multimedia** | `FFmpeg`, `Edge-TTS`, `Pexels API` |
| **Data** | `PostgreSQL`, `Grafana` |

---

## 🚀 Despliegue Rápido

```bash
# 1. Clonar el ecosistema
git clone [https://github.com/jaaidi0/AgroSentinel.git](https://github.com/jaaidi0/AgroSentinel.git)

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar la infraestructura Multi-Cloud
docker compose up -d --build