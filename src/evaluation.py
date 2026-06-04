import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_evaluation():
    print("📊 Ejecutando evaluación forense de los modelos guardados...")
    
    # 1. Cargar datos de test y variables objetivo reales
    X_test = pd.read_csv(os.path.join(BASE_DIR, "data", "test", "X_test.csv"))
    df_ml = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "df_processed.csv"))
    
    # Reconstrucción de los targets de prueba para validar
    test_indices = X_test.index
    y_test_m1 = df_ml.loc[test_indices, 'y_especulador']
    y_test_m2 = df_ml.loc[test_indices, 'y_fraude_administrativo']
    y_test_m3 = df_ml.loc[test_indices, 'price_clean'] * 0.15
    
    # 2. Cargar modelos desde /models/
    dir_models = os.path.join(BASE_DIR, "models")
    m_rf = joblib.load(os.path.join(dir_models, "trained_model_1.pkl"))
    m_xgb = joblib.load(os.path.join(dir_models, "trained_model_2.pkl"))
    m_reg = joblib.load(os.path.join(dir_models, "final_model.pkl"))
    
    # 3. Predicciones y Métricas
    preds_m1 = m_rf.predict(X_test)
    preds_m2 = m_xgb.predict(X_test)
    
    X_test_reg = X_test.copy()
    X_test_reg['prob_m1'] = m_rf.predict_proba(X_test)[:, 1]
    X_test_reg['prob_m2'] = m_xgb.predict_proba(X_test)[:, 1]
    preds_m3 = m_reg.predict(X_test_reg)
    
    # 4. Reporte en consola
    print("\n" + "="*60)
    print("🚀 REPORTE DE MÉTRICAS EN PRODUCCIÓN (TEST SET)")
    print("="*60)
    print(f"🎯 MÓDULO 1 (Especulómetro - Random Forest):")
    print(f"   · Accuracy : {accuracy_score(y_test_m1, preds_m1):.4f}")
    print(f"   · Precision: {precision_score(y_test_m1, preds_m1, zero_division=0):.4f}\n")
    
    print(f"🏴‍☠️ MÓDULO 2 (Cazapiratas - XGBoost):")
    print(f"   · Accuracy : {accuracy_score(y_test_m2, preds_m2):.4f}\n")
    
    print(f"🔮 MÓDULO 3 (Oráculo Urbano - Regresión en Cascada):")
    print(f"   · R² Score : {r2_score(y_test_m3, preds_m3):.4f}")
    print("="*60)

if __name__ == "__main__":
    run_evaluation()