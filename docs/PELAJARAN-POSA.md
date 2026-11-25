# Pelajaran POSA

(Diisi tiap run: 3 perbaikan, minimal satu diterapkan, dengan angka sebelum/sesudah.)

## 2026-11-25 (run terjadwal, Ramayana Part 1)
1. STATUS.md tertinggal dari kenyataan: tertulis "prompt_video", padahal di Downloads sudah ada 26 gambar, 26 klip, VO, dan video final 426 dtk. Terapkan: tiap run mulai dengan membaca isi Downloads/<topik>/ sebelum memilih tahap (dilakukan; menghemat tahap 2-5).
2. QC menangkap true peak -0.2 dBTP (batas -1,0) dan loudness -13,0 LUFS; perbaikan cukup di audio, tanpa render ulang video. Tambahkan limiter (alimiter/loudnorm TP=-1.5) di akhir rakit.
3. metadata.json dari alur lama belum punya kata_kunci_utama; samakan templat metadata dengan syarat qc_lint.
