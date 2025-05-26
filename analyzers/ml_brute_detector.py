# analyzers/ml_brute_detector.py

import joblib
import pandas as pd
from analyzers.feature_extractor import parse_logs, prepare_features

def detect_brute_force(log_lines):
    # Logları işle ve özellikleri hazırla
    df = parse_logs(log_lines)
    df = prepare_features(df)
    df.dropna(inplace=True)

    # Gerekli sütunları al
    X = df[["fail_count_last_5min", "time_since_last_fail", "total_failures"]]

    # Eğitilmiş modeli yükle
    model = joblib.load("analyzers/ml_model.pkl")

    # Tahmin yap
    df["prediction"] = model.predict(X)

    # Brute force olarak tahmin edilen IP'leri filtrele
    detected_ips = df[df["prediction"] == 1]["ip"].unique().tolist()

    return detected_ips

# Örnek kullanım
if __name__ == "__main__":
    logs = [
        "192.168.1.10 - POST /login - 401 - 2025-05-15 10:01:03",
        "192.168.1.10 - POST /login - 401 - 2025-05-15 10:03:00",
        "192.168.1.10 - POST /login - 401 - 2025-05-15 10:04:00",
        "192.168.1.10 - POST /login - 401 - 2025-05-15 10:09:00",
        "192.168.1.12 - POST /login - 401 - 2025-05-15 10:06:00",
        "192.168.1.12 - POST /login - 401 - 2025-05-15 10:07:00",
        "192.168.1.12 - POST /login - 401 - 2025-05-15 10:09:00",
    ]

    result = detect_brute_force(logs)
    print("🚨 Tespit edilen brute force IP'leri:", result)
