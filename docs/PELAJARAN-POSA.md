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


## 2026-11-25 (run terjadwal susulan, 23.52 WIB)
1. Dua run POSA berdempetan: berkas run sebelumnya ditulis sekitar 9 detik setelah run ini dipicu. Diterapkan: cek Downloads/POSA-run-*/ sebelum mulai; hasilnya diperiksa (`git apply --check` lolos) dan dipakai ulang, 0 usulan ganda.
2. Push ditolak di 2 dari 2 run malam ini (403), 0 commit sampai ke main; alat add_repo juga tidak tersedia di run ini. Tugas terjadwal perlu dibuat ulang dengan akses repo sebelum jadwal Senin-Jumat 08.17 WIB berikutnya.
3. QC Short "Bumi berhenti 5 detik" (produksi di luar tabel) mencatat logo bintang kanan bawah dihapus di S01-S12, padahal prompt tugas HEXA melarang menghapus tanda air AI Flow/Veo. Usul: pemilik memutuskan sebelum unggah; tambahkan cek ini ke QC.

## 2026-11-26 (run terjadwal 00.04 WIB, posting Short atas permintaan pemilik)
1. Templat jadwal selalu memicu tahap=upload, yang berhenti bila upload.json ada: video private yang dijadwalkan tidak akan pernah publik. Diterapkan: docs/templat/jadwal-posa.yml memilih tahap=publish bila upload.json ada (belum diuji lewat run jadwal).
2. Cek ulang Voynich: true peak +0,2 dBTP (batas -1,0), review.json tanpa status. Ukur true peak (ebur128 peak=true), jangan mengandalkan setelan limiter; ditandai gagal.
3. Playlist gagal 409 pada upload pertama (2 dari 2 upload POSA); menjalankan tahap=publish sesudahnya berhasil (1 dari 1, Short Bumi). Usul: upload.py mencoba ulang playlist dengan jeda; tambahkan juga --format short ke qc_lint.py (Short ini tayang tanpa lint otomatis).

## 2026-11-26 (run terjadwal malam, tanpa topik yang bisa dimajukan)
1. Short pertama tayang tanpa lint otomatis. Diterapkan: `tools/qc_lint.py --format short` (87-95 dtk, 1080x1920, momen jawaban <=30 dtk, tanpa chapter/intro/outro). Short Bumi: sebelum 1 GAGAL palsu (aturan 360 dtk), sesudah 0 GAGAL; keluaran mode panjang di 6 folder produksi tidak berubah. `rakit_video.py --format short` belum dibuat.
2. Voynich GAGAL hanya di audio: limiter dengan oversampling 192 kHz menurunkan true peak +0,2 menjadi -1,3 dBTP, loudness -13,8 menjadi -14,2 LUFS, video disalin tanpa render ulang. Usul: pakai rantai ini di akhir rakit.
3. STATUS.md kini mencatat 4 run terjadwal (25-26 Nov) tanpa produksi baru karena topik menunggu keputusan pemilik. Usul: pemilik menaruh satu baris "topik berikutnya + format" di STATUS.md, atau jadwal POSA dijeda sampai ada pilihan, supaya run tidak berulang tanpa produksi.

## 2026-11-26 (sesi pemilik, Ramayana Part 2 gambar dan VO)
1. Agen Flow salah saat rename/hapus massal (1 gambar benar terbuang, 4 judul tertukar). Diterapkan: verifikasi judul lewat teks footer tiap tile sesudahnya (sebelum 39/43 judul benar, sesudah 43/43). Hapus gambar secara manual.
2. VO satu take 10:46 pada permintaan 135 kata/menit; sesudah atempo 1,3 jadi 8:17. Usul: minta tempo lebih cepat di style prompt dan ukur sebelum membuat prompt klip.
3. Estimasi durasi klip dari kata (479 dtk) meleset dari ukuran VO (521 dtk). Diterapkan: build.py memakai durasi.json hasil penyelarasan jeda; 2 scene dipangkas ke batas 15 dtk.
- 27 Nov (klip Nexabot): jangan minta elemen samar (siluet wajah) "menjadi terang", wajahnya bisa berganti; minta tetap sama dari awal sampai akhir. Adegan "kalah tapi selamat" jangan memakai sinar/ledakan di akhir. QC tiap klip dengan contact sheet 1-2 fps; lompatan gambar di ujung bisa dibereskan dengan potong + perlambat tanpa generate ulang.
- 27 Nov (rakit Part 2): subtitle bisa disejajarkan akurat tanpa Whisper memakai espeak-ng + DTW per scene (akhir kalimat jatuh di jeda VO). Render transisi sebagai potongan kecil lalu concat, jauh lebih ringan daripada satu rantai xfade 43 input.
- 27 Nov: pemilik memutuskan logo Gemini yang terlihat boleh dihapus (Google juga menyediakan toggle Settings > Media Watermark sejak Agustus 2026). Untuk produksi berikutnya: matikan toggle itu di Flow sebelum generate gambar, supaya tidak perlu hapus logo di klip.
