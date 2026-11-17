# Pelajaran HEXA

Dibaca di awal setiap sesi. Tambahkan entri baru di atas. Format: tanggal, 3 hal yang bisa diperbaiki, perbaikan yang diterapkan.

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
