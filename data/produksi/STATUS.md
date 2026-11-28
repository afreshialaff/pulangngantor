# Status produksi Pulang ngantor (diperbarui tiap run HEXA)

## Antrean pemilik (diisi pemilik; run POSA membaca bagian ini lebih dulu)
- Topik berikutnya: (kosong)
- Format (panjang / short_90): (kosong)
- Voynich ("perbaiki dan unggah ulang" / "terima apa adanya"): (kosong)

| Folder | Tahap tercapai | Berikutnya |
|---|---|---|
| 2026-11-17 (Voynich) | Terunggah PRIVATE; cek ulang 26 Nov **GAGAL**: true peak +0,2 dBTP (batas -1,0) | Pemilik: pilih perbaiki audio lalu unggah ulang (ID video baru), atau terima apa adanya dan publikasikan manual di Studio. Perbaikan audio saja sudah diuji lolos (lihat run 26 Nov malam) |
| 2026-11-22-ramayana-1-rahwana | **SUDAH TAYANG** (konfirmasi pemilik 26 Nov 2026; yOu1JLVvU-g) | Selesai. Jangan dicek, diunggah, atau dijadwalkan ulang |
| 2026-11-24-bumi-berhenti-5-detik (Short) | **SUDAH TAYANG** publik 26 Nov 2026 (X-e9THx36F8), masuk playlist | Selesai. Jangan diunggah ulang. Subtitle sudah terbakar di video |
| 2026-11-22-ramayana-2-rama | **SUDAH TERUPLOAD** (konfirmasi pemilik 27 Nov 2026; 1r8pRi2lhck). upload.json masih mencatat private dan subtitle API gagal | Jangan diunggah atau dijadwalkan ulang. Belum dipastikan: status publik dan subtitle manual |
| 2026-11-27-pareidolia-hantu (Short) | Tahap 4, **menunggu klip pemilik**: VO (2:07), 14 gambar 2K, prompt video, paket teks dilengkapi; klip di ASUS baru S01 (1/14) | Pemilik: lengkapi S02-S14 di `PAREIDOLIA-HANTU/VIDEO/` (atau lanjutkan Nexabot lewat sesi interaktif; ditunda pemilik 28 Nov), dan putuskan durasi 127 dtk |
| 2026-11-22-ramayana-3-pengasingan-perang | riset, scenes.json, pelafalan | prompt_video, gambar |
| 2026-11-22-ramayana-4-moksa | riset, scenes.json, pelafalan | prompt_video, gambar |

Run tanpa topik: baca tabel ini, jangan menebak; minta pemilik memilih part/topik.

Catatan run 25 Nov 2026: Part 1 tidak perlu estimasi kredit baru (gambar, klip, VO sudah jadi). Video tidak ada di repo; sumber: Downloads/RAMAYANA PART 1/OUTPUT/. Upload tidak dipicu oleh run terjadwal.

## Run terjadwal 25 Nov 2026 (malam)
- Tahap tercapai: tidak ada topik di tabel yang dimajukan. Voynich dan Ramayana 1 sudah terunggah private; Ramayana 2-4 menunggu instruksi pemilik (HANDOFF-RAMAYANA-HEXA.md, 24 Nov). Modul A dijalankan: `data/produksi/USULAN-TOPIK.md`.
- Voynich dan Ramayana 1: menunggu hari dan jam tayang dari pemilik (sudah diunggah private menurut upload.json; jangan unggah ulang).
- Catatan: Downloads/bumi-berhenti-5-detik/ berisi Short final (93,0 dtk, QC dan teks upload ada, log menyebut Hexa). Tidak ada di tabel ini dan tidak disentuh.
- Kredit dipakai run ini: 0 (Flow dan AI Studio tidak dibuka).
- Dibutuhkan dari pemilik: (1) pilih topik + format; (2) hari/jam tayang; (3) beri akses push repo ke tugas terjadwal.

## Run terjadwal 25 Nov 2026 (susulan, 23.52 WIB)
- Tahap tercapai: sama dengan run sebelumnya, tidak ada topik yang dimajukan. USULAN-TOPIK.md dari run sebelumnya dipakai ulang (tidak dibuat ganda).
- Push masih ditolak (403, `git push --dry-run`): sesi terjadwal tidak diberi repo afreshialaff/pulangngantor. Perubahan ada sebagai patch di Downloads/POSA-run-2026-11-25-b/.
- Kredit dipakai: 0 (Flow dan AI Studio tidak dibuka).
- Dibutuhkan dari pemilik: (1) buat ulang tugas terjadwal POSA dari chat baru di claude.ai yang diberi repo pulangngantor dan folder Downloads; (2) pilih topik + format (atau izinkan Ramayana 2); (3) hari/jam tayang Voynich dan Ramayana 1.

## Run terjadwal 26 Nov 2026 (00.04 WIB)
- Run terjadwal: tidak ada topik yang bisa dimajukan (Ramayana 2-4 masih menunggu instruksi pemilik). USULAN-TOPIK.md 25 Nov masih berlaku, tidak dibuat ulang.
- Pesan pemilik di tengah run: (1) Ramayana 1 sudah tayang, dicatat; (2) posting Short Bumi berhenti 5 detik: tayang publik, https://youtu.be/X-e9THx36F8, playlist berhasil pada percobaan kedua (tahap publish).
- Belum diverifikasi pada Short: pelafalan VO dan sumber/klaim. Subtitle API gagal (token tanpa scope youtube.force-ssl).
- Kredit Flow/AI Studio dipakai: 0.
- Dibutuhkan dari pemilik: (1) pilih topik + format (atau izinkan Ramayana 2); (2) keputusan Voynich.

## Run terjadwal 26 Nov 2026 (malam, sekitar 20.00 WIB)
- ASUS terhubung (Downloads diizinkan saat run), `git push --dry-run` lolos.
- Tahap tercapai: tidak ada topik yang bisa dimajukan (Ramayana 2-4 ditahan menurut HANDOFF 24 Nov; Voynich menunggu keputusan; Ramayana 1 dan Short Bumi sudah tayang). Tidak ada produksi baru.
- Modul A: USULAN-TOPIK.md 25 Nov dipakai ulang (MKUltra 24, Kantor kosong 23, Waktu terasa cepat 21); tidak ada folder produksi baru yang menduplikasi ketiganya. Sumber tidak dibaca ulang.
- Voynich, uji di ruang kerja sementara (berkas hasil TIDAK disimpan, repo/Downloads/YouTube tidak diubah): limiter audio saja memberi -14,2 LUFS, true peak -1,3 dBTP (asli -13,8 LUFS, +0,2 dBTP); stream video identik (MD5 sama), durasi 420,79 dtk. Perintah: `ffmpeg -i asli.mp4 -map 0:v -map 0:a -c:v copy -af "aresample=192000,alimiter=limit=0.794:level=false:attack=5:release=50,aresample=48000" -c:a aac -b:a 192k -movflags +faststart baru.mp4`. Audio belum didengarkan.
- `tools/qc_lint.py --format short` ditambahkan; Short Bumi: 0 GAGAL (peringatan: naskah.json dan pelafalan.md tidak ada di folder, hook/VO awal dicek manual).
- Kredit Flow/AI Studio dipakai: 0.
- Dibutuhkan dari pemilik: (1) pilih topik + format, atau izinkan Ramayana 2; (2) Voynich: "perbaiki dan unggah ulang" atau "terima apa adanya"; (3) bila Voynich diunggah ulang, tentukan juga hari dan jam tayangnya.

## Run terjadwal 27 Nov 2026 (siang, sekitar 14.15 WIB)
- ASUS terhubung (Downloads diizinkan saat run). Clone berhasil, tetapi push ditolak (403: repo tidak masuk daftar repo yang diizinkan untuk sesi ini). Hasil run ada di Downloads/POSA-run-2026-11-27/.
- Pesan pemilik di tengah run: Ramayana Part 2 sudah terupload.
- QC sebagian Part 2 (video dari repo, 518,6 dtk, 1920x1080, 24 fps): qc_lint 0 GAGAL, 2 peringatan (jadwal_tayang kosong, naskah.json tidak ada); -14,6 LUFS, true peak -1,1 dBTP; pemindaian layar hitam, gambar beku, dan senyap tanpa temuan. Belum diperiksa: lembar kontak, keutuhan intro/outro, pelafalan VO, pemeriksa terpisah. review.json tidak ditulis.
- Pemeriksaan lanjutan (lembar kontak, banding intro/outro, pemasangan alat transkripsi) ditolak pengaman izin otomatis dan tidak dicoba lagi.
- Tidak ada topik lain yang dimajukan: Ramayana 3-4 menunggu instruksi (HANDOFF 24 Nov), Voynich menunggu keputusan. USULAN-TOPIK.md 25 Nov masih dipakai.
- Kredit Flow/AI Studio dipakai: 0.
- Dibutuhkan dari pemilik: (1) topik + format berikutnya, atau izinkan Ramayana 3; (2) keputusan Voynich; (3) tugas terjadwal dibuat ulang dengan akses repo.

## Run terjadwal 27 Nov 2026 (sore, sekitar 14.26 WIB)
- ASUS (laptop-e7b7q717) terhubung, Downloads diizinkan saat run. `git push --dry-run` lolos sesudah branch main lokal diperbarui (percobaan pertama ditolak non-fast-forward karena salinan lokal tertinggal 28 commit, bukan soal akses).
- Catatan run siang (patch di Downloads/POSA-run-2026-11-27/) sudah dimasukkan ke repo; patch itu tidak perlu diterapkan lagi.
- Tahap tercapai: tidak ada topik yang bisa dimajukan. Tidak ada instruksi baru untuk Ramayana 3-4 atau Voynich di STATUS.md, handoff, dan isi Downloads yang dicek. Tidak ada produksi baru.
- Modul A: `USULAN-TOPIK.md` diperbarui (3 kandidat, sebagian sumber dibaca ulang).
- Kesiapan Ramayana 3 (hanya dibaca): 40 scene, 1.244 kata VO (30-34 per scene); 16 `flow_subject` masih menyebut wayang, padahal Part 1 disetujui bergaya animasi 3D. Perkiraan bila diizinkan: 40 gambar Flow di luar character lock, 40 klip 15 dtk (dibuat pemilik), 1 take VO sekitar 8-10 menit. Biaya kredit belum dicek di Flow/AI Studio.
- Ramayana 4 (hanya dibaca): 26 scene, 814 kata VO; S19 hanya 29 kata (minimal 30).
- Kredit Flow/AI Studio dipakai: 0 (browser tidak dibuka).
- Dibutuhkan dari pemilik: (1) isi "Antrean pemilik" di atas (topik + format, atau izinkan Ramayana 3); (2) keputusan Voynich; (3) Ramayana 2: pastikan status publik dan unggah subtitle.srt di Studio bila belum.

## Run terjadwal 28 Nov 2026 (sekitar 18.47 WIB)
- ASUS (laptop-e7b7q717) terhubung, Downloads terhubung; `git push --dry-run` lolos sesudah checkout main.
- Topik: Short pareidolia (paling maju). Tahap 4 belum lengkap: hanya `VIDEO/S01.mp4`. **Menunggu klip pemilik**; run ini tidak membuat klip dan tidak membuka browser.
- Dibuat: `naskah.json`, `pelafalan.md`, draf `metadata.json`, `aset.md`; sumber Haselton & Nettle 2006 (abstrak) ditambahkan untuk S08.
- QC S01 (lembar kontak 1 fps): 9,02 dtk, 1080x1920, 24 fps, visual konsisten; logo bintang kecil kanan bawah terlihat.
- VO: 127,11 dtk, -16,5 LUFS, true peak +1,1 dBTP (perlu diproses saat rakit; uji sementara -15,1 LUFS dan -2,0 dBTP). Pelafalan belum didengarkan.
- `qc_lint --format short`: GAGAL durasi 127,1 dtk (batas 87-95; permintaan pemilik 1,5-2,5 menit) dan S01, S13, S14 tanpa sumber (S01/S14 hook dan penutup; S13 saran praktis yang belum punya sumber). Peringatan: naskah 283 kata, jadwal kosong, subtitle dan thumbnail belum ada. review.json belum ditulis.
- `tools/rakit_video.py --format short` belum ada; perlu dibuat sebelum rakit.
- Kredit Flow/AI Studio dipakai: 0.
- Dibutuhkan dari pemilik: (1) klip S02-S14; (2) setujui durasi 127 dtk (aturan lint disesuaikan) atau pendekkan VO/naskah; (3) keputusan Voynich masih terbuka.

