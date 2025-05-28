import pandas as pd
from datetime import datetime, timedelta

# CSV dosyasını oku
df = pd.read_csv("data/generated_logs.csv")

# Zaman sütununu datetime formatına çevir
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Parametreler
FAIL_LIMIT = 3
TIME_WINDOW = timedelta(minutes=5)

# IP bazında başarısız girişimleri takip et
fail_attempts = {}

# Label sütunu için boş liste
labels = []

for index, row in df.iterrows():
    ip = row["ip"]
    status_code = row["status_code"]
    timestamp = row["timestamp"]

    if ip not in fail_attempts:
        fail_attempts[ip] = []

    # 5 dakika içindeki başarısız girişimleri filtrele
    fail_attempts[ip] = [t for t in fail_attempts[ip] if timestamp - t <= TIME_WINDOW]

    if status_code == 401:
        fail_attempts[ip].append(timestamp)

    # Label: 1 = saldırı (fail sayısı eşik veya üstü), 0 = normal
    if len(fail_attempts[ip]) >= FAIL_LIMIT:
        labels.append(1)
    else:
        labels.append(0)

# Label sütununu DataFrame'e ekle
df["label"] = labels

# Yeni CSV olarak kaydet
df.to_csv("data/labeled_logs.csv", index=False)

print("Label oluşturma tamamlandı, 'data/labeled_logs.csv' dosyası oluşturuldu.")
