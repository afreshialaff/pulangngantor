# Pelajaran HEXA

## 2026-11-17 (3) — Voynich: aturan klip 15 detik
1. Aturan lama 'adegan ≤6 dtk' bentrok dengan generator klip pemilik (15 dtk); sekarang 1 adegan = 1 klip 15 dtk, VO ±35-38 kata.
2. Penomoran gambar wajib S01..Sxx sejak awal.
3. Flow bisa tertahan persetujuan privasi/onboarding; cek akses Flow di awal sesi, sebelum menulis prompt gambar.
**Perbaikan diterapkan:** agen/hexa/SKILL.md langkah 2 diperbarui; tools/buat_paket_voynich.py menghasilkan tabel durasi per scene.

Dibaca di awal setiap sesi. Tambahkan entri baru di atas. Format: tanggal, 3 hal yang bisa diperbaiki, perbaikan yang diterapkan.

## 2026-11-22 — Upgrade dari audit Jagad Mandala
Sumber: `docs/referensi/audit-jagad-mandala.md` (auditor tidak bisa mendengar audio, hanya 2 transkrip, tanpa Analytics).
**3 hal yang bisa diperbaiki**
1. Skill belum menjamin awal video yang kuat: tidak ada batas untuk jeda kosong, opener basa-basi, atau kapan janji judul dibayar (di Jagad Mandala jawaban inti muncul di menit 9-15).
2. Tidak ada kontrol variasi thumbnail, kata kunci judul di 50 karakter pertama, jadwal tetap, dan konsistensi format/seri.
3. Audio hanya dinilai "terdengar natural"; loudness tidak pernah diukur.
**Perbaikan yang diterapkan:** SKILL.md v2.2 (bagian "Aturan retensi & konsistensi", kerangka kritik sumber, subtitle krem/amber, baris keterangan AI, tabel keputusan audit vs brand); `tools/qc_lint.py` kini memeriksa momen jawaban ≤90 dtk, peta 3 poin, kata kunci di 50 karakter pertama, thumbnail_objek vs 3 video terakhir, baris AI di deskripsi, dan loudness via `--video`. Ketat untuk folder bertanggal ≥2026-11-22; video lama hanya mendapat PERINGATAN.
**Perlu diuji di Analytics:** apakah momen jawaban ≤90 dtk dan peta 3 poin menaikkan retensi 30 detik pertama; batas ±3 istilah baru per 30 dtk adalah heuristik Hexa, bukan data audit.

## 2026-11-17 (2) — Durasi ≥6 menit + intro/outro wajib
**3 hal yang bisa diperbaiki**
1. Aturan durasi hanya di prompt/brand (8-15 menit, Shorts 30-60 dtk) dan tidak ditegakkan; video bisa lolos terlalu pendek.
2. Intro/outro belum punya berkas resmi; perakitan ffmpeg ditulis ulang tiap sesi, rawan beda format (resolusi, fps, audio).
3. Timestamp subtitle/chapter bisa meleset setelah intro ditambahkan.

**Perbaikan yang diterapkan:** `tools/rakit_video.py` (normalisasi + tolak isi <360 dtk), `assets/` intro 4,3 dtk dan outro 7,9 dtk, `config.yaml: video`, cek durasi/kata/intro-outro di `tools/qc_lint.py`, aturan geser timestamp di SKILL.md.
**Konflik yang menunggu keputusan pemilik:** master brand bagian 9/12 dan `config.yaml shorts_per_week` masih menyebut Shorts 30-60 dtk; Hexa tidak memproduksi Shorts sampai diputuskan.

## 2026-11-17 — Upgrade skill dari audit Sisi Terang (belum ada video diproduksi)
Sumber: `docs/referensi/audit-sisi-terang.md`.

**3 hal yang bisa diperbaiki**
1. Skill Hexa sebelumnya hanya berupa prompt tanpa modul rinci. Pemilihan topik, struktur naskah, judul, dan deskripsi tidak punya aturan terukur, sehingga mudah melebar menjadi klaim berlebihan atau berita-ish.
2. QC hanya checklist manual. Kesalahan yang terlihat di audit (judul melebihi bukti, tanpa chapter, label berita palsu, salah dengar TTS, angka tanpa atribusi) belum ada pemeriksaan otomatisnya.
3. Belum ada cara menjaga audit tetap jujur: data audit hanya angka publik, sebagian bertanda INFERENSI/TIDAK DIVERIFIKASI, dan satu kanal contoh adalah gaya yang bertentangan dengan brand.

**Perbaikan yang diterapkan**
- `agen/hexa/SKILL.md` v2: modul A-G (topik, naskah, visual, audio, judul, deskripsi, QC) + tabel keputusan saat audit bertentangan dengan master brand (master brand menang).
- `tools/qc_lint.py`: memeriksa panjang judul, label berita/LANGSUNG, sumber di deskripsi, chapter untuk video ≥5 menit, atribusi per bagian naskah, tingkat keyakinan untuk dugaan/klaim/konspirasi, tag artefak di subtitle, duplikasi judul.
- Aturan memakai audit: hormati penanda keyakinan, jangan menyalin judul/kalimat, data Analytics Pulang ngantor sendiri mengalahkan audit.

**Untuk run berikutnya (diuji, bukan diasumsikan)**
- Ukur dulu apakah chapter + atribusi sumber menaikkan retensi di Analytics channel ini; audit tidak bisa membuktikannya.
- Uji apakah batas judul ≤70 karakter lebih baik daripada ≤100 pada channel ini (A/B judul bila YouTube mengizinkan).
- Tambahkan contoh `naskah.json` nyata ke `samples/` setelah video pertama selesai.

## 2026-11-17 (4) — Voynich: perakitan per segmen
- VO sekali generate (399,8 dtk) dipetakan per kalimat ke jeda tanpa ASR; 83/83 kalimat pas. Hugging Face dan unduhan model Whisper diblokir di sandbox, jadi jangan bergantung pada ASR.
- QC berjalan per segmen saat render (bukan menunggu semua), plus QC independen subagen: menemukan "1.438" (tahun diberi titik ribuan) di subtitle. Diperbaiki di subs.py dan ditambal di video tanpa render ulang penuh.
- Noise/grain + CRF 14/18 membuat master 27 Mbps (1,45 GB). Untuk kirim: 2-pass 6,8 Mbps. File >100 MB disimpan sebagai potongan .part-* dan digabung di workflow upload.
Tiga perbaikan berikutnya:
1. (DITERAPKAN) Aturan angka subtitle: tahun 1000-2099 setelah "tahun"/"dan" tanpa titik ribuan; workflow upload menggabung potongan video.
2. Kurangi kekuatan grain atau terapkan grain hanya di encode akhir agar segmen antara tidak 80 Mbps dan render lebih cepat.
3. Watermark ✦ dari Flow/Veo tidak dihapus (penanda konten AI); kalau ingin video bersih, generate klip dengan paket yang tanpa watermark terlihat.
