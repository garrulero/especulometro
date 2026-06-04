import os
import pandas as pd
import numpy as np
import re

# Configuración de rutas relativas al directorio raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_RAW = os.path.join(BASE_DIR, "data", "raw", "df_fuentes_unidas.csv")
PATH_PROCESSED = os.path.join(BASE_DIR, "data", "processed", "df_processed.csv")

def auditar_campo_licencia(texto):
    if not isinstance(texto, str) or texto.strip() == "" or texto.upper() == 'SIN_REGISTRO':
        return "ILEGAL_SIN_REGISTRO"
    cadena = texto.strip().upper()
    if "ESFCTU" in cadena or len(cadena) > 30:
        match = re.search(r'(EBI\d+|ESS\d+|LSS\d+)', cadena)
        return f"CORREGIDA_{match.group(1)}" if match else "FRAUDE_FORMATO_CATASTRO"
    return f"OK_{cadena}"

def run_pipeline():
    print(f"🔄 Iniciando pipeline de procesamiento de datos...")
    
    if not os.path.exists(PATH_RAW):
        raise FileNotFoundError(f"No se encuentra el dataset crudo en: {PATH_RAW}")

    df = pd.read_csv(PATH_RAW)
    
    # 1. Auditoría Forense de Licencias
    df['estado_licencia_auditada'] = df['license'].apply(auditar_campo_licencia)
    df['y_fraude_administrativo'] = df['estado_licencia_auditada'].str.contains('FRAUDE|ILEGAL').astype(int)
    
    # 2. Inyección Exógena (Simulación Booking y Eustat)
    df['indice_rotacion_booking'] = (df['availability_365'] * 0.25 + np.random.normal(5, 2, len(df))).round(1)
    poblacion_impacto = {"Bilbao": -3.2, "Donostia-San Sebastián": -5.4, "Vitoria-Gasteiz": -1.1}
    df['eustat_variacion_poblacion_5anos'] = df['neighbourhood_cleansed'].map(poblacion_impacto) - (df['price_clean'] * 0.01).round(2)
    
    df = df.drop_duplicates(subset=['id'])
    
    # 3. Feature Engineering de Negocio
    df['ingreso_mensual_turistico'] = df['price_clean'] * 22.0
    df['ingreso_mensual_tradicional'] = df['catastro_m2_real'] * df['idealista_m2_mes']
    df['ratio_especulacion_real'] = (df['ingreso_mensual_turistico'] / df['ingreso_mensual_tradicional']).round(2)
    df['indice_desertizacion_comercial'] = ((df['osm_densidad_ocio_500m'] * 1.5) + (df['availability_365'] * 0.1)).round(1)
    df['indice_desplazamiento_vecinal'] = ((df['dias_ocupados_reales'] / 365) * 100).round(1)
    df['y_especulador'] = (df['ratio_especulacion_real'] > 2.5).astype(int)
    
    # Exportación
    os.makedirs(os.path.dirname(PATH_PROCESSED), exist_ok=True)
    df.to_csv(PATH_PROCESSED, index=False)
    print(f"✅ Pipeline exitoso. Dataset procesado guardado en: {PATH_PROCESSED}")

if __name__ == "__main__":
    run_pipeline()