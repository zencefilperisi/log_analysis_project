import time
import os
import joblib
import pandas as pd
from analyzers.feature_extractor import parse_logs, prepare_features

def tail_f_ml(filepath, model):
    """
    Gerçek zamanlı log takibi + ML modeliyle brute force tahmini
    """
    if not os.path.exists(filepath):
        print(f"❌ Dosya bulunamadı: {filepath}")
        return

    with open(filepath, "r") as file:
        file.seek(0, 2)
        print(f"📡 Log izleniyor: {filepath}")
        buffer = []

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue

            buffer.append(line.strip())

            # Son 5 satırı al ve analiz et
            recent_logs = buffer[-5:]
            df = parse_logs(recent_logs)
            df = prepare_features(df)
            df.dropna(inplace=True)

            if df.empty:
                continue

            X = df[["fail_count_last_5min", "time_since_last_fail", "total_failures"]]
            predictions = model.predict(X)

            for ip, pred in zip(df["ip"], predictions):
                if pred == 1:
                    print(f"⚠️  AI Tespit: Brute force saldırısı! IP: {ip}")
                else:
                    print(f"✅  Güvenli: IP {ip}")

if __name__ == "__main__":
    log_path = "ornek2.log"  # İzlenecek log dosyası
    model_path = "analyzers/ml_model.pkl"  # Eğitilmiş modelin yolu

    if not os.path.exists(model_path):
        print("❌ Model dosyası bulunamadı. Lütfen önce model eğitimi yapın.")
    else:
        model = joblib.load(model_path)
        tail_f_ml(log_path, model)
