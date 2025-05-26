# bruteForceDetector.py
import re
from collections import defaultdict

def detect_brute_force(log_file, threshold=5, window_minutes=10):
    """
    Log dosyasını okuyup, belirli bir zaman aralığında ardışık başarısız girişimleri tespit eder.
    """
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - Failed login from (\d+\.\d+\.\d+\.\d+)')
    failed_logins = defaultdict(list)

    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                timestamp_str, ip = match.groups()
                from datetime import datetime, timedelta
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                failed_logins[ip].append(timestamp)

    alerts = {}
    for ip, times in failed_logins.items():
        times.sort()
        for i in range(len(times)):
            window_start = times[i]
            count = 1
            for j in range(i+1, len(times)):
                if times[j] - window_start <= timedelta(minutes=window_minutes):
                    count += 1
                else:
                    break
            if count >= threshold:
                alerts[ip] = count
                break

    return alerts

# 🌐 Canlı takip için ek fonksiyon
def detect_line(line):
    """
    Canlı log takibi için tek satır brute force tespiti.
    """
    if "failed" in line.lower():
        print(f"⚠️ Brute force şüphesi: {line}")

# Test için
if __name__ == "__main__":
    log_path = 'ornek.log'
    alerts = detect_brute_force(log_path)
    if alerts:
        print("Brute force attack detected from these IPs:")
        for ip, count in alerts.items():
            print(f"{ip} with {count} failed attempts.")
    else:
        print("No brute force attempts detected.")
