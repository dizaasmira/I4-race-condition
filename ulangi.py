# ulangi.py - menjalankan kedua skrip berulang kali dan merangkum hasilnya
import subprocess, re, sys, time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
STOK_AWAL = 10

def jalankan(skrip):
    mulai = time.perf_counter()
    out = subprocess.run(["python3", skrip], capture_output=True, text=True).stdout
    durasi = (time.perf_counter() - mulai) * 1000
    m = re.search(r"terjual: (\d+), Sisa stok akhir: (-?\d+)", out)
    return int(m.group(1)), int(m.group(2)), durasi

for skrip, label in (("flash_sale_race.py", "SEBELUM (tanpa mutex)"),
                     ("flash_sale_safe.py", "SESUDAH (dengan mutex)")):
    print(f"\n=== {label} - {skrip} ===")
    print(f"{'Run':>3} | {'Terjual':>7} | {'Sisa':>4} | {'Waktu(ms)':>9} | Status")
    anomali, total_ms = 0, 0
    for i in range(1, N + 1):
        t, s, ms = jalankan(skrip)
        total_ms += ms
        ok = (t <= STOK_AWAL) and (s >= 0) and (t + s == STOK_AWAL)
        anomali += (not ok)
        print(f"{i:>3} | {t:>7} | {s:>4} | {ms:>9.1f} | {'KONSISTEN' if ok else 'ANOMALI'}")
    print(f"Anomali: {anomali}/{N} run | rata-rata waktu: {total_ms/N:.1f} ms")
