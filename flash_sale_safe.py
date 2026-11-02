import threading
import time

stok_barang = 10
terjual = 0
mutex = threading.Lock() # Pengaman Critical Section (Mutex)

def beli_barang_aman(id_pembeli):
    global stok_barang, terjual

    # Mengunci area kritis (Critical Section)
    with mutex:
        if stok_barang > 0:
            time.sleep(0.001)
            stok_barang -= 1
            terjual += 1
            print(f"Pembeli {id_pembeli} BERHASIL membeli. Sisa stok: {stok_barang}")
        else:
            print(f"Pembeli {id_pembeli} GAGAL. Stok habis.")

threads = []
for i in range(1, 21):
    t = threading.Thread(target=beli_barang_aman, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\n--- HASIL DENGAN MUTEX (AMAN) ---")
print(f"Total barang terjual: {terjual}, Sisa stok akhir: {stok_barang}")
