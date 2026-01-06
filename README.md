# 🌿 AgroSentinel v1.3 | Climate Intelligence System

<p align="center">
  <img src="static/dashboard.png" alt="AgroSentinel Dashboard" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.3_Madrid-7289da?style=for-the-badge&logo=github" alt="Release">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Cloud-Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="GCP">
  <img src="https://img.shields.io/badge/IA-Gemini_Flash-orange?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini">
</p>

---

## 🛰️ Visión General
**AgroSentinel** no es solo una estación meteorológica; es una herramienta de **Inteligencia Biológica**. Fusiono la fisiología vegetal con la ingeniería de datos para prevenir el estrés hídrico en tiempo real mediante el cálculo preciso del **VPD (Vapor Pressure Deficit)**.

> "Del microscopio al teclado: ciencia convertida en sistemas inteligentes para la agricultura."

---

## ✨ Características Destacadas (v1.3)

| Funcionalidad | Descripción Técnica | Impacto |
| :--- | :--- | :--- |
| **🎬 Video Reports** | Renderizado automático con **FFmpeg** y lógica Python. | Visualización instantánea del estado del cultivo. |
| **🧠 Gemini IA** | Diagnóstico avanzado de salud vegetal (Google Gemini 1.5). | Traducción de datos crudos a lenguaje agronómico. |
| **🌍 Cloud Native** | Arquitectura distribuida desplegada en **GCP Madrid**. | Resiliencia total y latencia mínima para el sur de Europa. |
| **🤖 n8n Workflows** | Orquestación de eventos y alertas en **Microsoft Teams**. | Automatización total de la cadena de decisión. |

---

## 🏗️ Arquitectura de Datos



1. **Captura:** Nodos IoT (ESP32) enviando telemetría vía API.
2. **Procesamiento:** Motor de cálculo VPD (Tetens Equation) en contenedores **Docker**.
3. **Análisis:** Evaluación de estrés hídrico por modelos de IA.
4. **Output:** Generación de video con locución y dashboards dinámicos en **Grafana Cloud**.

---

## 🔬 El Corazón del Sistema: Control de VPD
Entendemos que la temperatura no lo es todo. El **VPD** es el motor de la transpiración:

* 🔵 **0.4 - 0.8 kPa:** Bajo riesgo (Humedad alta, riesgo fúngico).
* 🟢 **0.8 - 1.2 kPa:** Zona óptima de crecimiento.
* 🟡 **1.2 - 1.6 kPa:** Transpiración elevada.
* 🔴 **> 1.6 kPa:** **ALERTA AGROSENTINEL**. Generación automática de video-reporte.

---

## 🛠️ Stack Tecnológico

| Área | Tecnologías |
| :--- | :--- |
| **Lenguaje** | `Python 3.11`, `FastAPI` |
| **IA & Automatización** | `Google Gemini 1.5`, `n8n` |
| **Infraestructura** | `Docker`, `Docker Compose`, `GCP (Madrid)` |
| **Multimedia** | `FFmpeg`, `Gunicorn` |
| **Visualización** | `Grafana Cloud`, `PostgreSQL` |

---

## 🚀 Despliegue en 3 minutos

```bash
# Clonar el ecosistema
git clone [https://github.com/jaaidi0/AgroSentinel.git](https://github.com/jaaidi0/AgroSentinel.git)

# Levantar microservicios
docker compose up -d --build
