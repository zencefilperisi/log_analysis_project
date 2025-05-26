import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Veriyi oku
df = pd.read_csv("data/labeled_logs.csv")

# Özellikler ve etiket
X = df[["failed_attempts", "unique_fail_times"]]
y = df["label"]

# Veriyi eğitim ve test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Tahmin ve değerlendirme
y_pred = model.predict(X_test)
print("✅ Model başarıyla eğitildi.")
print("🔍 Doğruluk Oranı:", accuracy_score(y_test, y_pred))
print("\n🧪 Detaylı Sonuç:\n", classification_report(y_test, y_pred))

# Eğitilen modeli kaydet
joblib.dump(model, "models/brute_model.pkl")
print("\n💾 Model 'models/brute_model.pkl' olarak kaydedildi.")
