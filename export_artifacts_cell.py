# Notebook'ta model eğitiminden sonra çalıştır:
import os
import joblib
from sklearn.preprocessing import LabelEncoder

os.makedirs("artifacts", exist_ok=True)

# 1) XGBoost modeli
joblib.dump(model, "artifacts/xgb_price_model.joblib")

# 2) LabelEncoder'ları tekrar düzgün şekilde kaydet
cat_cols = ["manufacturer", "model", "condition", "fuel", "title_status", "transmission", "type"]
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    le.fit(df[col].astype(str))
    label_encoders[col] = le
joblib.dump(label_encoders, "artifacts/label_encoders.joblib")

# 3) TF-IDF vectorizer
joblib.dump(tfidf, "artifacts/tfidf_vectorizer.joblib")

# 4) Feature kolon sırası
joblib.dump(FEATURE_COLS, "artifacts/feature_cols.joblib")

print("Artifacts kaydedildi:")
print("- artifacts/xgb_price_model.joblib")
print("- artifacts/label_encoders.joblib")
print("- artifacts/tfidf_vectorizer.joblib")
print("- artifacts/feature_cols.joblib")
