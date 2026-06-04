# Meatzaritza Data Labs — Especulómetro Vasco 🔬 lsh
> **Suite Tri-Modular Multiplataforma de Contra-Auditoría Territorial y Predicción del Suelo Residencial en Euskadi**

---

## 🎯 1. Objetivo del Proyecto

El avance de las Viviendas de Uso Turístico (VUT) en las capitales de la Comunidad Autónoma Vasca ha generado tensiones en el mercado del alquiler tradicional. **Meatzaritza Data Labs — Especulómetro Vasco** nace como un ecosistema analítico de software libre y machine learning diseñado para fiscalizar de forma automatizada el suelo urbano residencial.

El objetivo central es auditar anuncios activos, cruzar plataformas opacas, identificar dinámicas de fraude administrativo y proyectar el impacto económico real (inflación y desplazamiento) sobre el derecho a la vivienda de los residentes locales en Bilbao, Donostia-San Sebastián y Vitoria-Gasteiz.

---

## 📊 2. Arquitectura de Fuentes y Cruce de Datos

Para evitar los sesgos de los conjuntos de datos genéricos, este proyecto implementa un modelo de enriquecimiento geoespacial multiplataforma cruzando cuatro grandes capas de información:

1. **Censo Turístico Base (Inside Airbnb):** Extracción de la matriz base del censo de perfiles de anfitriones, tarifas basales, identificadores únicos y el campo crítico de licencias oficiales (`listings.csv.gz`).
2. **Multiplataforma (Booking.com):** Inyección de vectores de control de fricción y rotación habitacional. Permite evaluar la duplicación de anuncios y la explotación comercial intensiva.
3. **Músculo Financiero (Eustat):** Vinculación de micro-datos socioeconómicos del País Vasco por sección censal (Renta Media por Hogar y tasa de variación demográfica/pérdida de población local a 5 años).
4. **Infraestructura Urbana (OpenStreetMap):** Extracción geoespacial de variables de entorno mediante un radio de influencia de 500 metros (densidad de locales de ocio nocturno, saturación de franquicias turísticas y distancias métricas a hitos costeros o monumentos).
5. **Presión del Suelo (Idealista + Catastro Foral):** Captura del precio basal del metro cuadrado residencial tradicional para computar las tasas de desviación y la rentabilidad del suelo.

---

## ⚙️ 3. Metodología e Ingeniería de Características (Feature Engineering)

El pipeline de datos sigue un flujo lineal e independiente dividido en fases estrictas para garantizar la reproducibilidad científica:

### A. Parser Forense de Strings (Regex)
Muchos grandes tenedores camuflan la explotación masiva incrustando los 18 dígitos del código catastral del edificio dentro del campo de la licencia turística individual de la plataforma para esquivar las inspecciones. Se implementa un parser basado en expresiones regulares (`Regex`) que audita las cadenas de texto, extrae la licencia real oculta y etiqueta de forma binaria el **Fraude de Formato Administrativo** (`y_fraude_administrativo`).

### B. Construcción de Índices de Daño Social
A partir de las variables exógenas unificadas, se computan tres métricas nucleares de negocio:
* **Ratio de Especulación Real:** Determina cuántas veces supera el rendimiento mensual estimado de la explotación turística frente al precio de mercado del alquiler residencial tradicional en el mismo barrio.
  $$\text{Ratio Especulación} = \frac{\text{Precio por Noche} \times 22}{\text{Metros Cuadrados Catastro} \times \text{Precio } m^2 \text{ Idealista}}$$
  Un ratio $> 2.5$ establece de forma matemática el *Ground Truth* de explotación comercial desmedida.
* **Índice de Desertización Comercial:** Ponderación basada en la desaparición del comercio de proximidad local por la proliferación de servicios orientados en exclusiva al visitante.
* **Índice de Desplazamiento Vecinal:** Porcentaje de saturación del inmueble que mide el bloqueo físico del suelo a los habitantes fijos de la localidad.

---

## 🤖 4. Modelado Predictivo: La Suite Tri-Modular en Cascada

En lugar de delegar la predicción en un único modelo plano, el core de inteligencia artificial se compone de una **arquitectura multimodelo en cascada** basada en algoritmos de ensamble (Árboles de Decisión):