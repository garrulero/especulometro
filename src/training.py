import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_DATA = os.path.join(BASE_DIR, "data")
DIR_MODELS = os.path.join(BASE_DIR, "models")

def run_training():
    print("🌲 Iniciando entrenamiento de la Suite en Cascada...")
    df_ml = pd.read_csv(os.path.join(DIR_DATA, "processed", "df_processed.csv"))
    
    features_maestras = [
        'price_clean', 'availability_365', 'eustat_renta_media_hogar', 
        'osm_densidad_ocio_500m', 'osm_distancia_costa_monumento_m'
    ]
    
    X = df_ml[features_maestras]
    y_m1 = df_ml['y_especulador']
    y_m2 = df_ml['y_fraude_administrativo']
    
    # 1. Partición Train/Test y guardado
    X_train, X_test, y_train_m1, y_test_m1 = train_test_split(X, y_m1, test_size=0.2, random_state=42)
    _, _, y_train_m2, y_test_m2 = train_test_split(X, y_m2, test_size=0.2, random_state=42)
    
    X_train.to_csv(os.path.join(DIR_DATA, "train", "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(DIR_DATA, "test", "X_test.csv"), index=False)
    
    # 2. Instanciación y Entrenamiento Base (M1 y M2)
    m_rf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    m_xgb = XGBClassifier(n_estimators=80, max_depth=6, learning_rate=0.1, random_state=42)
    
    m_rf.fit(X, y_m1)
    m_xgb.fit(X, y_m2)
    
    # 3. Entrenamiento Regresor en Cascada (M3)
    df_ml['prob_m1'] = m_rf.predict_proba(X)[:, 1]
    df_ml['prob_m2'] = m_xgb.predict_proba(X)[:, 1]
    
    X_reg = df_ml[features_maestras + ['prob_m1', 'prob_m2']]
    y_reg = df_ml['price_clean'] * 0.15 
    
    m_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    m_reg.fit(X_reg, y_reg)
    
    # 4. Persistencia en /models/
    os.makedirs(DIR_MODELS, exist_ok=True)
    joblib.dump(m_rf, os.path.join(DIR_MODELS, "trained_model_1.pkl"))
    joblib.dump(m_xgb, os.path.join(DIR_MODELS, "trained_model_2.pkl"))
    joblib.dump(m_reg, os.path.join(DIR_MODELS, "final_model.pkl"))
    joblib.dump(features_maestras, os.path.join(DIR_MODELS, "features_maestras.joblib"))
    
    print("✅ Entrenamiento completado. Binarios exportados a /models/")

if __name__ == "__main__":
    run_training()