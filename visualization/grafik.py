# grafik.py
import matplotlib.pyplot as plt
import datetime

def plot_error_counts(log_file):
    error_counts = {}
    with open(log_file, 'r') as f:
        for line in f:
            if 'error' in line.lower():
                date_str = line.split(' - ')[0]
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                day = date.date()
                error_counts[day] = error_counts.get(day, 0) + 1

    days = sorted(error_counts.keys())
    counts = [error_counts[day] for day in days]

    plt.plot(days, counts, marker='o')
    plt.title('Daily Error Counts')
    plt.xlabel('Date')
    plt.ylabel('Number of Errors')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_error_counts('ornek.log')
