# Status produksi Pulang ngantor (diperbarui tiap run HEXA)

| Folder | Tahap tercapai | Berikutnya |
|---|---|---|
| 2026-11-17 (Voynich) | Terunggah PRIVATE; cek ulang 26 Nov **GAGAL**: true peak +0,2 dBTP (batas -1,0) | Pemilik: pilih perbaiki audio lalu unggah ulang (ID video baru), atau terima apa adanya dan publikasikan manual di Studio. Perbaikan audio saja sudah diuji lolos (lihat run 26 Nov malam) |
| 2026-11-22-ramayana-1-rahwana | **SUDAH TAYANG** (konfirmasi pemilik 26 Nov 2026; yOu1JLVvU-g) | Selesai. Jangan dicek, diunggah, atau dijadwalkan ulang |
| 2026-11-24-bumi-berhenti-5-detik (Short) | **SUDAH TAYANG** publik 26 Nov 2026 (X-e9THx36F8), masuk playlist | Selesai. Jangan diunggah ulang. Subtitle sudah terbakar di video |
| 2026-11-22-ramayana-2-rama | Video final dirakit (8:39) di Downloads/RAMAYANA PART 2/OUTPUT (27 Nov); belum diunggah | Pemilik tonton, lalu tentukan hari/jam tayang; thumbnail dan upload private |
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
