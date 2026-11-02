import threading
import time

# Simulasi stok awal flash sale
stok_barang = 10
terjual = 0

def beli_barang(id_pembeli):
    global stok_barang, terjual
    # Proses membaca stok dan jeda waktu untuk memicu race condition
    stok_sekarang = stok_barang
    time.sleep(0.001)

    if stok_sekarang > 0:
        stok_barang = stok_sekarang - 1
        terjual += 1
        print(f"Pembeli {id_pembeli} BERHASIL membeli. Sisa stok: {stok_barang}")
    else:
        print(f"Pembeli {id_pembeli} GAGAL. Stok habis.")

# Membuat 20 thread pembeli yang menyerbu secara bersamaan
threads = []
for i in range(1, 21):
    t = threading.Thread(target=beli_barang, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\n--- HASIL TANPA SINKRONISASI ---")
print(f"Total barang terjual: {terjual}, Sisa stok akhir: {stok_barang}")
