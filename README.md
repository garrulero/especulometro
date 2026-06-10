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

## 🧠 El Motor Predictivo: Suite Tri-Modular en Cascada

Para abordar un problema complejo y multivariable como la gentrificación, el sistema huye de los modelos predictivos planos y utiliza una arquitectura de inferencia en cascada mediante *Meta-Features*:

1. **Módulo 1: El Especulómetro (Clasificador RF):** Analiza el vector de entrada y clasifica si el anuncio pertenece a un particular o a un Gran Tenedor / Fondo Comercial.
2. **Módulo 2: El Cazapiratas (Clasificador XGBoost):** Evalúa el riesgo conductual y administrativo, detectando fraudes como el camuflaje del número de Catastro en los campos de Licencia Turística.
3. **Módulo 3: El Oráculo Urbano (Regresor RF):** El modelo maestro. Recibe el vector original y se le inyectan dinámicamente las probabilidades continuas de los Módulos 1 y 2 (*meta-features*). Esto le permite predecir con extrema precisión el impacto inflacionista exacto (+€/m²) en los contratos de alquiler de los residentes del barrio.

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
git clone [https://github.com/tu-usuario/especulometro.git](https://github.com/tu-usuario/especulometro.git)
cd especulometro
