import time
import threading
import psutil
import matplotlib.pyplot as plt

# Örnek bir sistem fonksiyonu (hesaplama işlemi)
def system_function(n):
    total = 0
    for i in range(n):
        total += i
    return total


# Stres testi fonksiyonu
def stress_test(duration, num_threads, workload, interval=1):
    end_time = time.time() + duration
    threads = []
    cpu_usage = []
    memory_usage = []
    timestamps = []

    def worker():
        while time.time() < end_time:
            system_function(workload)

    def monitor():
        while time.time() < end_time:
            cpu_usage.append(psutil.cpu_percent())
            memory_usage.append(psutil.virtual_memory().percent)
            timestamps.append(time.time())
            time.sleep(interval)

    # Belirtilen sayıda iş parçacığı oluştur ve başlat
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()

    # Tüm iş parçacıklarının tamamlanmasını bekle
    for thread in threads:
        thread.join()

    monitor_thread.join()

    return timestamps, cpu_usage, memory_usage


# Test parametreleri
test_duration = 60  # Test süresi (saniye)
num_threads = 10  # İş parçacığı sayısı
workload = 1000000  # İş yükü
interval = 1  # İzleme aralığı (saniye)

# Stres testini gerçekleştir ve metrikleri topla
timestamps, cpu_usage, memory_usage = stress_test(test_duration, num_threads, workload, interval)

print("Stres testi tamamlandı.")

# CPU ve bellek kullanımını görselleştirme
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(timestamps, cpu_usage, label='CPU Kullanımı (%)', color='blue')
plt.xlabel('Zaman (saniye)')
plt.ylabel('CPU Kullanımı (%)')
plt.title('CPU Kullanımı Zaman İçinde')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(timestamps, memory_usage, label='Bellek Kullanımı (%)', color='green')
plt.xlabel('Zaman (saniye)')
plt.ylabel('Bellek Kullanımı (%)')
plt.title('Bellek Kullanımı Zaman İçinde')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
