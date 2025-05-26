import pandas as pd
from datetime import datetime, timedelta
import random

ips = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
base_time = datetime(2025, 5, 20, 10, 0, 0)

logs = []

# Brute force yapan IP (saldırı örneği)
for i in range(5):
    logs.append({
        "ip": "192.168.1.10",
        "timestamp": base_time + timedelta(minutes=i),
        "path": "/login",
        "status_code": 401,
        "label": 1
    })

# Normal kullanıcı trafiği
for i in range(15):
    logs.append({
        "ip": random.choice(ips),
        "timestamp": base_time + timedelta(minutes=i+10),
        "path": "/login",
        "status_code": random.choice([200, 401]),
        "label": 0
    })

df = pd.DataFrame(logs)
df["timestamp"] = pd.to_datetime(df["timestamp"])
print(df.head())
