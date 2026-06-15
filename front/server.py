import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Especulometro")

app = FastAPI(title="Especulómetro Vasco API")

# Habilitar CORS para conectar con Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 🧠 1. CARGA GLOBAL DE LOS MODELOS DE INTELIGENCIA ARTIFICIAL
# ==============================================================================
# Obtener la ruta raiz del proyecto de forma dinamica (padre del directorio 'front' donde esta este server.py)
PATH_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_MODELO_NLP = os.path.join(PATH_RAIZ, "models", "trained_model_1_nlp.pkl")

print("Cargando el motor Transformer Multilingue en memoria...")
encoder_transformer = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

print("Cargando el clasificador semantico lineal (.pkl)...")
modelo_m1_nlp = joblib.load(PATH_MODELO_NLP)

print("Cargando el generador LLM Qwen2.5-0.5B en memoria (puede tardar un poco)...")
from transformers import pipeline
try:
    llm_generator = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", device="cpu")
except Exception as e:
    print(f"Error al cargar Qwen: {e}. Se usará un fallback.")
    llm_generator = None


# ==============================================================================
# 📋 2. DEFINICIÓN DE SCHEMAS
# ==============================================================================
class PredictInput(BaseModel):
    municipio: str
    precio_por_noche: float
    disponibilidad: int
    description: str | None = ""
    host_about: str | None = ""

class UrlInput(BaseModel):
    url: str

# ==============================================================================
# 🚀 3. LÓGICA DE PREDICCIÓN Y ADAPTACIÓN DE RESPUESTA
# ==============================================================================
def procesar_texto_y_predecir(description: str, host_about: str):
    texto_para_ia = f"{description} {host_about}".strip()
    if not texto_para_ia:
        texto_para_ia = "Apartment for rent standard vacation stay."
        
    vector_semantico = encoder_transformer.encode([texto_para_ia])
    prob_especulacion = float(modelo_m1_nlp.predict_proba(vector_semantico)[0][1])
    return prob_especulacion

def generar_informe_llm(ratio_especulacion: float, ratio_explotacion: float, municipio: str, alquiler_residencial: float, poblacion_joven: float, desertizacion: float):
    if not llm_generator:
        return "El modelo generador (Qwen) no está disponible en este momento."
    
    prompt = f"<|im_start|>system\nEres un analista experto en sociología urbana y mercado inmobiliario del País Vasco. Redacta un diagnóstico muy breve y formal.<|im_end|>\n<|im_start|>user\nGenera un diagnóstico forense de máximo 2 frases para un alojamiento en {municipio}. Indica de forma contundente si se trata de un caso de especulación teniendo en cuenta que su probabilidad de pertenecer a un gran tenedor/especulador es del {ratio_especulacion:.1f}%. Argumenta la conclusión mencionando que es {ratio_explotacion:.1f} veces más rentable que un alquiler residencial (renta media {alquiler_residencial:.0f}€) y cómo esto fomenta la pérdida del {poblacion_joven:.1f}% de población joven (Eustat) y una desertización del {desertizacion:.1f}%. No saludes.<|im_end|>\n<|im_start|>assistant\n"
    try:
        resultado = llm_generator(prompt, max_new_tokens=150, do_sample=True, temperature=0.3)
        texto_generado = resultado[0]['generated_text']
        informe = texto_generado.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
        
        # Evitar cortes a medias si llega al límite de tokens
        if not informe.endswith('.'):
            ultimo_punto = informe.rfind('.')
            if ultimo_punto != -1:
                informe = informe[:ultimo_punto+1]
                
        return informe
    except Exception as e:
        logger.error(f"Error en LLM: {str(e)}")
        return "No se pudo generar el informe narrativo en este momento."

def generar_respuesta(prob_especulacion: float, precio: float, disponibilidad: int, municipio: str):
    # Generar la estructura de respuesta que espera el frontend
    ratio_especulacion = prob_especulacion * 100
    indice_desplazamiento = 30 + (prob_especulacion * 50)
    impacto_economico = prob_especulacion * 12.5
    
    alquiler_residencial = 1100.0 if municipio == "Bilbao" else 1300.0
    dias_ocupados = 365 - disponibilidad
    ingreso_vut_anual = dias_ocupados * precio
    ingreso_vut_mensual = ingreso_vut_anual / 12 if ingreso_vut_anual > 0 else 0
    
    ratio_explotacion = ingreso_vut_mensual / alquiler_residencial if alquiler_residencial > 0 else 1
    
    informe_generado = generar_informe_llm(ratio_especulacion, ratio_explotacion, municipio, alquiler_residencial, 4.5, 14.2)
    
    return {
        "ratio_especulacion": ratio_especulacion,
        "indice_desplazamiento": indice_desplazamiento,
        "probabilidad_m1": prob_especulacion,
        "probabilidad_m2": prob_especulacion * 0.8,
        "impacto_economico": impacto_economico,
        "ratio_explotacion_comercial": round(ratio_explotacion, 1),
        "eustat_poblacion_joven": 4.5,
        "eustat_desertizacion_comercio": 14.2,
        "informe_llm": informe_generado,
        "detalles": {
            "renta_media_m2": 15.5,
            "alquiler_residencial_estimado": alquiler_residencial,
            "host_listings_count": 5 if prob_especulacion > 0.5 else 1,
            "dias_ocupados_proyectados": dias_ocupados,
            "ingreso_mensual_vut_estimado": ingreso_vut_mensual,
            "municipio_procesado": municipio
        }
    }

# ==============================================================================
# 🌐 4. ENDPOINTS
# ==============================================================================
@app.post("/api/predict")
async def predict(payload: PredictInput):
    logger.info(f"Recibida peticion POST a /api/predict para el municipio {payload.municipio}")
    try:
        prob = procesar_texto_y_predecir(payload.description, payload.host_about)
        logger.info(f"  -> Prediccion completada. Probabilidad M1: {prob*100:.2f}%")
        return generar_respuesta(prob, payload.precio_por_noche, payload.disponibilidad, payload.municipio)
    except Exception as err:
        logger.error(f"Error en /api/predict: {str(err)}")
        raise HTTPException(status_code=500, detail=f"Error en la inferencia NLP: {str(err)}")

import scratch_extract_final

@app.post("/api/analyze-url")
async def analyze_url(payload: UrlInput):
    logger.info(f"Recibida peticion POST a /api/analyze-url para la URL: {payload.url}")
    try:
        url = payload.url
        logger.info(f"  -> Iniciando scraper (Playwright) para {url}...")
        if "booking.com" in url.lower():
            scraped_data = await scratch_extract_final.extract_booking_data(url)
        else:
            scraped_data = await scratch_extract_final.extract_airbnb_data(url)
            
        logger.info(f"  -> Scraper finalizado. Datos base obtenidos. Titulo: {scraped_data.get('title')}")
        
        raw_text = scraped_data.get("raw_dom_data", {}).get("page_text", "")
        logger.info(f"  -> Texto DOM extraido: {len(raw_text)} caracteres.")
        
        # NLP Model takes the text
        texto_para_ia = raw_text[:5000] if raw_text else "Apartment for rent standard vacation stay."
        logger.info(f"  -> Pasando {len(texto_para_ia)} caracteres de texto al modelo Transformer...")
        
        vector_semantico = encoder_transformer.encode([texto_para_ia])
        prob_especulacion = float(modelo_m1_nlp.predict_proba(vector_semantico)[0][1])
        logger.info(f"  -> Analisis Semantico completado. Probabilidad de Especulacion: {prob_especulacion*100:.2f}%")
        
        analisis = generar_respuesta(
            prob_especulacion, 
            scraped_data.get("price", 100), 
            scraped_data.get("availability", 280), 
            scraped_data.get("municipio", "Bilbao")
        )
        
        logger.info("  -> Respuesta JSON generada correctamente y enviada al frontend.")
        return {
            "title": scraped_data.get("title", "Alojamiento"),
            "image": scraped_data.get("image", ""),
            "municipio": scraped_data.get("municipio", "Bilbao"),
            "host_name": scraped_data.get("host_name", "Desconocido"),
            "host_listings_count": scraped_data.get("host_listings_count", 1),
            "price": scraped_data.get("price", 100),
            "availability": scraped_data.get("availability", 280),
            "description_scraped": texto_para_ia,
            "analysis": analisis
        }
    except Exception as err:
        logger.error(f"Error en /api/analyze-url: {str(err)}")
        raise HTTPException(status_code=500, detail=f"Error analizando URL: {str(err)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)