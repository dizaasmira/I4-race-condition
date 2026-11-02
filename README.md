# I-4: Analisis Race Condition dan Sinkronisasi

Sistem Operasi (USA-WP2260110), Kelas D, Universitas Sebelas April. Tema: Cloud dan Layanan Digital UMKM.
Nama: Diza Asmiranda Subianto · NIM: 250660121024 · Kepingan puzzle #6 (Level 4 Puzzle UTS)

Kasus: **overselling** pada flash sale. 20 pembeli (thread) berebut stok awal 10 unit pada variabel bersama. Program awal memperlihatkan race condition; program kedua memperbaikinya dengan **mutex** (`threading.Lock`).

## Isi folder

| Berkas | Fungsi |
|---|---|
| `flash_sale_race.py` | Versi **sebelum** perbaikan: baca stok, jeda `time.sleep(0.001)`, cek, tulis, tanpa sinkronisasi |
| `flash_sale_safe.py` | Versi **sesudah** perbaikan: seluruh cek, kurangi, dan catat terjual dibungkus `with mutex:` |
| `ulangi.py` | Menjalankan kedua skrip N kali (`subprocess`), mengambil ringkasan, mengukur waktu, dan memeriksa konsistensi |
| `log/` | Keluaran satu kali eksekusi tiap skrip (sesuai Gambar 4.2 dan 4.3 laporan) |
| `bukti/` | Tangkapan layar dari VM (identitas VM, hasil eksekusi, eksekusi berulang, kode di editor nano) |

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

## Critical section

Critical section adalah bagian yang menyentuh variabel bersama `stok_barang` dan `terjual`: membaca stok, mengecek `> 0`, mengurangi stok, dan mencatat terjual. Pengecekan harus berada di dalam critical section yang sama dengan pengurangan, karena kalau tidak, thread tetap bisa lolos cek dengan nilai stok yang sudah basi (pola check-then-act).

## Bukti

Lihat folder `bukti/`:

| Berkas | Isi |
|---|---|
| `4.1_identitas_vm.jpg` | Hostname, kernel, versi Python, dan folder kerja |
| `4.2_hasil_tanpa_mutex.jpg` | 20 pembeli berhasil dari stok 10, sisa stok akhir 5 |
| `4.3_hasil_mutex.jpg` | Tepat 10 berhasil, 10 gagal, sisa 0 |
| `4.4_eksekusi_berulang_10run.jpg` | Hasil per-run `ulangi.py 10` |
| `A.1_kode_race_di_nano.jpg`, `A.2_kode_safe_di_nano.jpg` | Kode di editor nano pada VM |

## Catatan

- Semaphore dibahas pada laporan sebagai alternatif, tidak diimplementasikan.
- Mutex dalam satu proses hanya melindungi thread di proses itu. Untuk toko yang dilayani beberapa server, atomisitas perlu dijamin di tingkat database.
- Penggunaan AI generatif diungkapkan pada Lampiran B laporan.
