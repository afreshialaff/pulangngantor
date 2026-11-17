# Pulang ngantor — Divisi YouTube

> *Kerja boleh selesai. Rasa penasaran jangan.*

Repo produksi channel YouTube **Pulang ngantor** (horror, mystery, konspirasi, psikologi, trivia, dark history). Dibangun dengan pola yang sama seperti repo Titi World, tetapi **master brand-nya adalah [`docs/MASTER-BRAND.md`](docs/MASTER-BRAND.md)** (Dark Mystery / Cinematic Noir / After-Work Storytelling). Repo ini khusus YouTube.

## Struktur
| Folder | Isi |
|---|---|
| `docs/MASTER-BRAND.md` | Master brand guideline (sumber kebenaran, jangan diubah tanpa persetujuan pemilik) |
| `brand/` | Aset: foto profil 800×800, banner 2560×1440 (lihat `brand/README.md`) |
| `config.yaml` | Pengaturan channel, jadwal, mode upload |
| `pipeline/youtube.py` | Koneksi YouTube Data API v3 + pengaman channel |
| `tools/cek_youtube.py`, `tools/upload.py` | Uji koneksi, unggah video |
| `scripts/get_youtube_token.py` | Ambil refresh token (sekali, di laptop) |
| `.github/workflows/` | `cek-youtube.yml` (uji koneksi), `upload.yml` (upload manual) |
| `data/produksi/<YYYY-MM-DD>/` | Naskah, metadata, thumbnail, hasil upload per video |
| `agen/` | Aturan kerja agen (menyusul, mengikuti pola Titi World) |

## Setup koneksi GitHub ↔ YouTube (sekali saja)

> Penting: akun Google di laptopmu punya channel lama ("Leo Faurizal Fatoni"). Channel Pulang ngantor harus **channel terpisah**, dan token harus diambil untuk channel itu.

### 1. Buat channel Pulang ngantor
Di YouTube: foto profil → **Buat channel** (sebaiknya sebagai *Brand Account* baru bernama "Pulang ngantor"). Cek handle `@pulangngantor`; kalau sudah terpakai, pilih varian dan beri tahu agar `config.yaml` diperbarui. Detail checklist: `docs/MASTER-BRAND.md` bagian 14.

### 2. Google Cloud: aktifkan API
1. https://console.cloud.google.com → buat project `pulang-ngantor`.
2. **APIs & Services → Library** → aktifkan **YouTube Data API v3**.
3. **OAuth consent screen** → External → isi nama app & email → tambahkan akunmu sebagai **Test user** → lalu **Publish app** (supaya refresh token tidak kedaluwarsa tiap 7 hari).
4. **Credentials → Create credentials → OAuth client ID → Desktop app** → unduh JSON → simpan sebagai `scripts/client_secret.json` (di `.gitignore`, jangan diupload).

### 3. Ambil refresh token (di laptop)
```bash
pip install -r requirements.txt
python scripts/get_youtube_token.py
```
Saat browser terbuka, login dan **pilih channel Pulang ngantor** (bukan channel lama). Skrip mencetak nama channel yang terhubung, lalu empat nilai.

### 4. Masukkan ke GitHub Secrets
Repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Nilai |
|---|---|
| `YT_CLIENT_ID` | dari skrip |
| `YT_CLIENT_SECRET` | dari skrip |
| `YT_REFRESH_TOKEN` | dari skrip |
| `YT_EXPECTED_CHANNEL_ID` | ID channel Pulang ngantor (dari skrip). Pengaman: upload ditolak kalau token milik channel lain |

Jangan tempel nilai-nilai ini di chat atau file repo.

### 5. Uji koneksi
Repo → **Actions → Pulang ngantor — cek koneksi YouTube → Run workflow**. Log harus menampilkan `OK terhubung ke: Pulang ngantor`.

### 6. Upload pertama
Taruh `metadata.json` (+ `thumbnail.jpg`, `subtitle.srt`) di `data/produksi/<tgl>/` dan videonya di repo, lalu jalankan workflow **upload ke YouTube**. Default **private** sampai QC selesai (aturan master brand).

Contoh `metadata.json`:
```json
{"judul": "Kenapa Kantor Kosong Terasa Menyeramkan?",
 "deskripsi": "Selamat datang di Pulang ngantor...\n\nSumber dan referensi:\n- ...",
 "tag": ["pulang ngantor", "cerita misteri", "psikologi manusia"],
 "playlist": {"judul": "Misteri Setelah Jam Kerja"}}
```

## Catatan YouTube API
- Project API yang belum diaudit: video unggahan API bisa dikunci **private**. Untuk publik/terjadwal otomatis, ajukan *YouTube API Services – Audit and Quota Extension*, lalu ubah `upload.mode` di `config.yaml`.
- Thumbnail custom butuh channel terverifikasi nomor HP (youtube.com/verify).
- Kuota default 10.000 unit/hari; satu upload ≈ 1.600 unit.
