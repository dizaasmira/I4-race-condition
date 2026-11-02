# I-4: Analisis Race Condition dan Sinkronisasi

Sistem Operasi (USA-WP2260110), Kelas D, Universitas Sebelas April. Tema: Cloud dan Layanan Digital UMKM.
Nama: Diza Asmiranda Subianto · Kepingan puzzle #6 (Level 4 Puzzle UTS)

Kasus: **overselling** pada flash sale. 20 pembeli (thread) berebut stok awal 10 unit pada variabel bersama. Program awal memperlihatkan race condition; program kedua memperbaikinya dengan **mutex** (`threading.Lock`).

## Isi folder

| Berkas | Fungsi |
|---|---|
| `flash_sale_race.py` | Versi **sebelum** perbaikan: baca stok, jeda `time.sleep(0.001)`, cek, tulis, tanpa sinkronisasi |
| `flash_sale_safe.py` | Versi **sesudah** perbaikan: seluruh cek, kurangi, dan catat terjual dibungkus `with mutex:` |
| `ulangi.py` | Menjalankan kedua skrip N kali (`subprocess`), mengambil ringkasan, mengukur waktu, dan memeriksa konsistensi |
| `log/` | Keluaran satu kali eksekusi tiap skrip (sesuai Gambar 4.2 dan 4.3 laporan) |

## Cara menjalankan

Butuh Python 3 saja.

```bash
python3 flash_sale_race.py     # tanpa mutex: terjadi overselling
python3 flash_sale_safe.py     # dengan mutex: konsisten
python3 ulangi.py 10           # eksekusi berulang 10 kali untuk kedua skrip
```

Karena race condition bersifat non-deterministik, angka pada percobaan Anda bisa berbeda dari tabel di bawah. Itu wajar.

## Ringkasan hasil (VM praktik, 10 kali eksekusi)

Skenario: 20 pembeli, stok awal 10. Status KONSISTEN bila terjual tidak melebihi stok awal, sisa stok tidak negatif, dan terjual + sisa sama dengan stok awal.

| Versi | Run anomali | Terjual (min sampai maks) | Rata-rata waktu |
|---|---|---|---|
| Tanpa mutex (`flash_sale_race.py`) | 10 dari 10 | 14 sampai 20 | 159,4 ms |
| Dengan mutex (`flash_sale_safe.py`) | 0 dari 10 | selalu 10 | 178,5 ms |

Waktu mencakup start interpreter Python, jadi hanya cocok untuk perbandingan relatif. Versi dengan mutex sedikit lebih lambat karena critical section berjalan berurutan.

- Mutex dalam satu proses hanya melindungi thread di proses itu. Untuk toko yang dilayani beberapa server, atomisitas perlu dijamin di tingkat database.
- Penggunaan AI generatif diungkapkan pada Lampiran B laporan.
