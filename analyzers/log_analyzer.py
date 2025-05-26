import pandas as pd
import matplotlib.pyplot as plt

def analyze_log(file_path, keyword='error', time_unit='hour', save_fig=False, fig_name='log_analysis.png'):
    try:
        # Log dosyasını oku
        df = pd.read_csv(file_path, sep=' - ', engine='python', header=None, names=['TarihSaat', 'Mesaj'])
        
        # TarihSaat sütununu datetime tipine dönüştür
        df['TarihSaat'] = pd.to_datetime(df['TarihSaat'])
        
        # keyword içeren satırları filtrele (büyük/küçük harf duyarsız)
        filtered = df[df['Mesaj'].str.contains(keyword, case=False, na=False)]
        
        if filtered.empty:
            print(f"🔍 '{keyword}' içeren satır bulunamadı.")
            return
        
        # Zaman bazında grupla (hour/day/minute)
        if time_unit == 'hour':
            grouped = filtered.groupby(filtered['TarihSaat'].dt.hour).size()
            xlabel = 'Saat'
        elif time_unit == 'day':
            grouped = filtered.groupby(filtered['TarihSaat'].dt.date).size()
            xlabel = 'Gün'
        elif time_unit == 'minute':
            grouped = filtered.groupby(filtered['TarihSaat'].dt.strftime('%Y-%m-%d %H:%M')).size()
            xlabel = 'Dakika'
        else:
            print("❌ Desteklenmeyen zaman birimi. hour, day veya minute seçebilirsiniz.")
            return
        
        # Grafik çizimi
        grouped.plot(kind='bar', color='red')
        plt.title(f"Zaman Bazında '{keyword}' Sayısı ({time_unit})")
        plt.xlabel(xlabel)
        plt.ylabel('Sayısı')
        plt.tight_layout()
        
        if save_fig:
            plt.savefig(fig_name)
            print(f"📊 Grafik '{fig_name}' olarak kaydedildi.")
        else:
            plt.show()
        
    except FileNotFoundError:
        print(f"❌ '{file_path}' dosyası bulunamadı.")
    except Exception as e:
        print(f"⚠️ Bir hata oluştu: {e}")

# Örnek kullanım
if __name__ == "__main__":
    analyze_log('ornek2.log', keyword='error', time_unit='hour')
