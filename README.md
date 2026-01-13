# 🌿 AgroSentinel

[![Release](https://img.shields.io/github/v/release/jaaidi0/AgroSentinel?color=green)](https://github.com/jaaidi0/AgroSentinel/releases)
[![License](https://img.shields.io/github/license/jaaidi0/AgroSentinel)](LICENSE)
[![Stars](https://img.shields.io/github/stars/jaaidi0/AgroSentinel? style=social)](https://github.com/jaaidi0/AgroSentinel/stargazers)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

> Sistema IoT Multi-Cloud de monitoreo agrícola con predicción de riesgo fúngico y optimización de riego mediante IA

**AgroSentinel** es una plataforma open-source de agricultura de precisión que combina IoT, Machine Learning y arquitectura distribuida para proporcionar decisiones automatizadas en sanidad vegetal y gestión hídrica.

---

## 🚀 Características Principales

### 🌡️ **Monitoreo VPD (Déficit de Presión de Vapor)**
- Cálculo en tiempo real basado en la ecuación de Tetens
- Alertas predictivas de estrés hídrico
- Optimización automática de programas de riego

### 🍄 **Predicción de Riesgo Fúngico**
- Modelos específicos para *Botrytis cinerea* y Mildiu
- Predicción con **72h de antelación**
- Integración con estaciones meteorológicas

### 🤖 **IA Generativa**
- Informes automáticos en video (Gemini 2.5 Flash)
- Análisis de tendencias climáticas
- Recomendaciones por cultivo

### ☁️ **Arquitectura Multi-Cloud**
- **Telemetría:** GCP Madrid (baja latencia Europa)
- **Procesamiento:** DigitalOcean Frankfurt
- **Sincronización bidireccional** de datos

---

## 🛠️ Stack Tecnológico

```
Backend:          Python 3.11 │ FastAPI
Base de Datos:   TimescaleDB │ PostgreSQL optimizado
Visualización:   Grafana Cloud
Containers:      Docker │ Docker Compose
IA/ML:           Google Gemini 2.5 Flash API
Automatización:   n8n Workflow Engine
Cloud:           GCP │ DigitalOcean
```

---

## 📦 Instalación Rápida

### **Requisitos**
- Docker 24.0+
- Docker Compose 2.20+
- Credenciales API (GCP, Gemini)

### **Comandos**

```bash
# Clonar repositorio
git clone https://github.com/jaaidi0/AgroSentinel.git
cd AgroSentinel

# Configurar entorno
cp .env.example . env
nano .env  # Editar credenciales

# Levantar infraestructura
docker-compose up -d

# Verificar servicios
docker-compose ps

# Acceder a Grafana
# http://localhost:3000
# Usuario: admin | Password: (ver .env)
```

---

## 🎯 Casos de Uso

| Sector | Aplicación | Beneficio |
|--------|-----------|-----------|
| 🍇 **Viticultura** | Predicción Botrytis | Reducción 40% uso fungicidas |
| 🍅 **Invernaderos** | Monitoreo VPD continuo | +25% producción tomate |
| 🌾 **Investigación** | Pipeline datos climáticos | Análisis históricos 10 años |

---

## 📊 Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────┐
│              SENSORES IoT CAMPO                      │
│  Temp │ Humedad │ Mojado Foliar │ Radiación          │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│         CAPA INGESTA (GCP Madrid)                    │
│    FastAPI │ TimescaleDB │ Pub/Sub                   │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│    PROCESAMIENTO IA (DigitalOcean Frankfurt)         │
│  Python ML │ Gemini 2.5 │ n8n Workflows              │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│         VISUALIZACIÓN & ALERTAS                      │
│    Grafana Dashboards │ Webhooks │ Notificaciones    │
└──────────────────────────────────────────────────────┘
```

---

## 🔬 Roadmap

### **v1.5.0** (Febrero 2026)
- [ ] API REST pública con OpenAPI
- [ ] Integración sensores LoRaWAN
- [ ] Módulo fertilización basado en IA

### **v2.0.0** (Q2 2026)
- [ ] Multi-tenant para cooperativas
- [ ] App móvil (React Native)
- [ ] Marketplace modelos ML

---

## 📥 Últimas Versiones

**[v1.4.0 - The Frankfurt Update](https://github.com/jaaidi0/AgroSentinel/releases/tag/v1.4.0)** (2026-01-13)
- ✅ Arquitectura Multi-Cloud
- ✅ IA generativa con Gemini 2.5
- ✅ Motor VPD Intelligence
- ✅ Automatización n8n

---

## 🤝 Contribuir

Las contribuciones son bienvenidas: 

1. Fork del proyecto
2. Crea rama feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit (`git commit -m 'Add:  nueva funcionalidad'`)
4. Push (`git push origin feature/NuevaFuncionalidad`)
5. Abre Pull Request

---

## 📄 Licencia

MIT License - Uso libre para investigación y producción. 

Ver [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos

- **CSIC** - Inspiración en investigación agroclimática
- **Comunidad AgriTech** - Conocimiento open-source compartido
- **Universidad de Granada** - Formación en sistemas informáticos

---

## 👤 Autor

**El Mostapha Jaaidi**  
🌱 Agro-Tech & Data Engineer  
🎓 Biólogo + Developer | Python, IoT & Agricultura de Precisión

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-0077B5?logo=linkedin)](https://linkedin.com/in/el-mostapha-jaaidi)
[![GitHub](https://img.shields.io/badge/GitHub-Seguir-181717?logo=github)](https://github.com/jaaidi0)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella**

**Desarrollado con 🌱 desde Granada, España**

</div>
