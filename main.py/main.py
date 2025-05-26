# main.py
import os
from analyzers.bruteForceDetector import detect_brute_force
from analyzers.grafik import plot_error_counts

def main():
    log_file = 'ornek2.log'  # Log dosyanızın adını burada belirtiyorsunuz

    # Dosya var mı kontrol et
    if not os.path.exists(log_file):
        print(f"❌ HATA: '{log_file}' adlı log dosyası bulunamadı.")
        print("📁 Lütfen dosyanın doğru dizinde olduğundan ve isminin doğru yazıldığından emin olun.")
        return

    print(f"🔍 '{log_file}' dosyası analiz ediliyor...")

    # Brute force saldırılarını kontrol et
    alerts = detect_brute_force(log_file)
    if alerts:
        print("\n🚨 Brute force saldırısı tespit edildi! Şüpheli IP adresleri:")
        for ip, count in alerts.items():
            print(f"🔸 {ip} - {count} başarısız giriş denemesi")
    else:
        print("✅ Brute force saldırısı tespit edilmedi.")

    # Hata mesajlarını grafikle göster
    print("\n📊 Hata mesajları analizi yapılıyor...")
    plot_error_counts(log_file)

if __name__ == "__main__":
    main()
