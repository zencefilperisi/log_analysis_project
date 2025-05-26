from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

def parse_logs(log_lines):
    """
    Log satırlarını alır, IP, durum kodu ve zaman bilgisini parse eder.
    Pandas DataFrame olarak döner.
    """
    data = []
    for entry in log_lines:
        try:
            ip, method_path, status, time_str = entry.split(" - ")
            status = status.strip()
            timestamp = datetime.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")
            data.append({"ip": ip, "status": status, "timestamp": timestamp})
        except ValueError:
            continue  # Hatalı satır varsa atla
    return pd.DataFrame(data)


def prepare_features(df, time_window_minutes=5):
    """
    Belirli bir zaman aralığında başarısız giriş denemelerine dair öznitelikler üretir:
      - fail_count_last_5min
      - time_since_last_fail
      - total_failures
      - is_brute_force_label (eğitim verisi için opsiyonel)
    """
    TIME_WINDOW = timedelta(minutes=time_window_minutes)
    fail_attempts = defaultdict(list)
    all_failures = defaultdict(int)

    fail_count_list = []
    time_delta_list = []
    total_fail_list = []
    brute_force_label = []

    for idx, row in df.iterrows():
        ip = row["ip"]
        ts = row["timestamp"]
        status = row["status"]

        if status == "401":
            # Başarısız denemeyi kaydet
            fail_attempts[ip].append(ts)
            all_failures[ip] += 1

            # Zaman aralığı içinde kalanları filtrele
            recent_fails = [t for t in fail_attempts[ip] if ts - t <= TIME_WINDOW]
            fail_attempts[ip] = recent_fails

            # Öznitelikler
            fail_count_list.append(len(recent_fails))
            total_fail_list.append(all_failures[ip])
            if len(recent_fails) > 1:
                delta = (ts - recent_fails[-2]).total_seconds()
            else:
                delta = None
            time_delta_list.append(delta)

            # Opsiyonel: brute force etiketi (örnekleme için)
            label = 1 if len(recent_fails) >= 3 else 0
            brute_force_label.append(label)

        else:
            # Başarılı giriş olursa reset
            fail_attempts[ip] = []
            fail_count_list.append(0)
            time_delta_list.append(None)
            total_fail_list.append(all_failures[ip])
            brute_force_label.append(0)

    df["fail_count_last_5min"] = fail_count_list
    df["time_since_last_fail"] = time_delta_list
    df["total_failures"] = total_fail_list
    df["is_brute_force"] = brute_force_label

    return df
