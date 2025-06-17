# log_olustur.py

from datetime import datetime, timedelta
import random

# Örnek log mesajları
mesajlar = [
    "User login successful",
    "User logout",
    "Error: Failed to connect to database",
    "Error: Unauthorized access attempt",
    "File uploaded",
    "Password changed",
    "Error: Invalid user credentials",
    "Session expired",
    "New user registered"
]

# Şu anki zamandan başlayarak geçmişe doğru rastgele zamanlar üret
simdi = datetime.now()
log_satirlari = []

for i in range(100):
    zaman = simdi - timedelta(minutes=random.randint(1, 500))
    mesaj = random.choice(mesajlar)
    log_satirlari.append(f"{zaman.strftime('%Y-%m-%d %H:%M:%S')} - {mesaj}")

# Log dosyasını yaz
with open("data/ornek2.log", "w") as f:
    for satir in sorted(log_satirlari):
        f.write(satir + "\n")

print("✅ ornek2.log başarıyla oluşturuldu.")



# .