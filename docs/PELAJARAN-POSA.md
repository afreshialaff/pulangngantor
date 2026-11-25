# Pelajaran POSA

(Diisi tiap run: 3 perbaikan, minimal satu diterapkan, dengan angka sebelum/sesudah.)

## 2026-11-25 (run terjadwal, Ramayana Part 1)
1. STATUS.md tertinggal dari kenyataan: tertulis "prompt_video", padahal di Downloads sudah ada 26 gambar, 26 klip, VO, dan video final 426 dtk. Terapkan: tiap run mulai dengan membaca isi Downloads/<topik>/ sebelum memilih tahap (dilakukan; menghemat tahap 2-5).
2. QC menangkap true peak -0.2 dBTP (batas -1,0) dan loudness -13,0 LUFS; perbaikan cukup di audio, tanpa render ulang video. Tambahkan limiter (alimiter/loudnorm TP=-1.5) di akhir rakit.
3. metadata.json dari alur lama belum punya kata_kunci_utama; samakan templat metadata dengan syarat qc_lint.
- Upload 25 Nov: video .part-* (4 potong, 90 MB) di repo berhasil; upload selesai ±70 dtk. Caption gagal (token tanpa scope youtube.force-ssl) dan playlist gagal (409); perlu token OAuth dengan scope caption.

## 2026-11-25 (run terjadwal malam, tanpa topik yang bisa dimajukan)
1. Push ditolak (403: repo tidak masuk daftar repo yang diizinkan untuk sesi terjadwal; 0 commit sampai ke main). Perbaikan: pemilik membuat ulang tugas terjadwal dari chat yang sudah menambahkan repo pulangngantor. Diterapkan di run ini: cek `git push --dry-run` di awal, hasil ditulis sebagai berkas baru + patch di Downloads.
2. STATUS.md tidak mencatat bahwa Ramayana 2-4 ditahan; informasinya hanya ada di HANDOFF di Downloads. Diterapkan: alasan tahan kini tercatat di STATUS.md (versi run ini).
3. Ada produksi di luar tabel (Short "Bumi berhenti 5 detik", 93,0 dtk, berkas bertanggal run yang sama). Usul: tiap sesi produksi, HEXA atau POSA, menambah barisnya di STATUS.md agar tidak ada kerja ganda.

