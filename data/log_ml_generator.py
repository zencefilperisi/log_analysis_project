import pandas as pd
from datetime import datetime

# Örnek log verileri (etiketli)
logs = [
    {"ip": "192.168.1.10", "status_code": 401, "timestamp": "2025-05-15 10:01:03", "label": 1},
    {"ip": "192.168.1.10", "status_code": 401, "timestamp": "2025-05-15 10:03:00", "label": 1},
    {"ip": "192.168.1.10", "status_code": 401, "timestamp": "2025-05-15 10:04:00", "label": 1},
    {"ip": "192.168.1.10", "status_code": 200, "timestamp": "2025-05-15 10:05:00", "label": 0},
    {"ip": "192.168.1.11", "status_code": 401, "timestamp": "2025-05-15 10:02:00", "label": 0},
    {"ip": "192.168.1.11", "status_code": 401, "timestamp": "2025-05-15 10:04:00", "label": 0},
    {"ip": "192.168.1.11", "status_code": 401, "timestamp": "2025-05-15 10:06:00", "label": 1},
    {"ip": "192.168.1.12", "status_code": 200, "timestamp": "2025-05-15 10:07:00", "label": 0},
    {"ip": "192.168.1.12", "status_code": 401, "timestamp": "2025-05-15 10:09:00", "label": 0},
]

# DataFrame'e çevir
df = pd.DataFrame(logs)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# CSV olarak kaydet
df.to_csv("data/generated_logs.csv", index=False)

print("✅ Etiketli log verisi başarıyla oluşturuldu: data/generated_logs.csv")
