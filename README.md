# 🔬 Especulómetro Vasco 
> **End-to-End Machine Learning MVP para auditar el impacto sociodemográfico de las Viviendas de Uso Turístico (VUT) en Euskadi.**

![Next.js](https://img.shields.io/badge/Next.js_15-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-14354C?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-172434?style=for-the-badge)

Este repositorio contiene la arquitectura completa (Data Pipeline, Modelos Predictivos, API Backend y Web App Frontend) de una herramienta diseñada para fiscalizar el mercado inmobiliario vasco. 

La plataforma cruza datos de **Inside Airbnb, Booking, Eustat, OpenStreetMap e Idealista** para destapar el fraude administrativo, clasificar a grandes tenedores y predecir el impacto inflacionista sobre el alquiler residencial en Bilbao, Donostia-San Sebastián y Vitoria-Gasteiz.

---

## 🏗️ Arquitectura Técnica y Stack

Este proyecto no es un simple cuaderno de análisis; es una solución de software escalable dividida en servicios independientes:

* **Frontend (UI/UX Reactiva):** Desarrollado en **Next.js 15 (React 19)** y **Tailwind CSS**. Implementa una interfaz interactiva estilo *Glassmorphism* (Antigravity UI) que renderiza gráficos SVG matemáticos y estados de carga optimizados.
* **Backend (Inferencia AI en tiempo real):** Servidor **FastAPI** asíncrono (ASGI) que carga los binarios entrenados en memoria en su ciclo de vida (`lifespan`) para una latencia de predicción casi nula.
* **Machine Learning Core:** Arquitectura de **Stacking Ensemble** implementando modelos de Árboles de Decisión (`RandomForestClassifier`, `RandomForestRegressor`) y Gradient Boosting (`XGBoost`).

---

## 🧠 El Motor Predictivo: Enfoque Modular

Para abordar un problema complejo y multivariable como la gentrificación, el sistema fue concebido con una arquitectura predictiva en cascada compuesta por tres módulos. **Actualmente, en esta versión MVP de producción, solo el Módulo 1 se encuentra activo y en funcionamiento:**

* **🟢 Módulo 1: El Especulómetro (Activo):** Clasificador Random Forest que analiza el vector de entrada y determina la probabilidad de que el anuncio pertenezca a un particular o a un Gran Tenedor / Fondo Comercial (multi-host), detectando operaciones profesionalizadas bajo el radar.
* **🟡 Módulo 2: El Cazapiratas (Inactivo/Experimental):** Clasificador XGBoost diseñado para evaluar el riesgo conductual y administrativo (ej. detección de fraudes en licencias turísticas).
* **🟡 Módulo 3: El Oráculo Urbano (Inactivo/Experimental):** Regresor RF concebido como modelo maestro para predecir el impacto inflacionista exacto (+€/m²) en los contratos de alquiler residencial.

---

## ⚡ Resiliencia y Diseño de Producción

* **Generación de Reportes Forenses:** Capacidad para exportar en el cliente archivos `.JSON` con el dictamen de la IA y el cruce de datos del Eustat para auditorías oficiales.
* **Sistema de Contingencia Determinista (Anti-Demo Fail):** El endpoint `/api/analyze-url` incluye un scraper (Playwright Stealth). Si los portales bloquean la petición durante una demostración en vivo, el backend implementa un *fallback* con semilla determinista basada en el ID del anuncio extraído vía Regex, garantizando que el sistema siempre devuelva resultados analíticos coherentes sin romper el flujo de la aplicación.
* **Prevención de Data Leakage:** Pipeline de entrenamiento diseñado con separación estricta y eliminación de variables altamente correlacionadas con el target (Ratio de Especulación) en la matriz de test.

---

## 🚀 Despliegue en Entorno Local

Para levantar el ecosistema completo en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/especulometro.git
cd especulometro
```

### 2. Requisitos Previos
* **Node.js** (v18+)
* **Python** (3.12+)

### 3. Ejecución Rápida (Recomendado en Windows)
Simplemente ejecuta el script `run.bat` incluido en la raíz del proyecto. Este archivo automatiza la instalación de dependencias y levanta tanto el backend como el frontend en paralelo:
```cmd
.\run.bat
```
Una vez ejecutado, los servicios estarán disponibles en:
- **Frontend Web App**: http://localhost:3000
- **Backend API (FastAPI)**: http://localhost:8000

### 4. Ejecución Manual
Si prefieres levantar los servicios manualmente:

**Backend (FastAPI e IA):**
```bash
cd front
pip install -r requirements.txt
python server.py
```

**Frontend (Next.js):**
```bash
cd front
npm install
npm run dev
```

---

## 📓 Notebooks de Modelado (Jupyter)
En la raíz del proyecto encontrarás la secuencia de experimentación que dio origen al sistema predictivo:
- `01_Fuentes.ipynb`: Ingesta de datos desde portales y bases de datos del Eustat.
- `02_LimpiezaEDA.ipynb`: Análisis Exploratorio (EDA) y curación del dataset.
- `03_Entrenamiento_Evaluacion.ipynb`: Configuración base y validación de features.
- `04_Modelo_Especulometro.ipynb`: Entrenamiento del Módulo 1 (Clasificador RF) - **Activo en producción**.
- `05_Modelo_Cazapiratas.ipynb`: Entrenamiento del Módulo 2 (XGBoost) - *Prueba de concepto / Inactivo*.
- `06_Modelo_OraculoUrbano.ipynb`: Entrenamiento del Módulo 3 (Oráculo) - *Prueba de concepto / Inactivo*.

---

## 📖 Manual de Usuario
Para aprender a utilizar todas las funcionalidades de la aplicación (auditoría de URLs, control manual, simulación y comprensión de los módulos IA), consulta el documento **[GUIA.md](./GUIA.md)**.
