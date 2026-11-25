# Status produksi Pulang ngantor (diperbarui tiap run HEXA)

| Folder | Tahap tercapai | Berikutnya |
|---|---|---|
| 2026-11-17 (Voynich) | Terunggah PRIVATE (upload.json ada) | Pemilik: cek thumbnail di YouTube Studio, putuskan jadwal tayang |
| 2026-11-22-ramayana-1-rahwana | Terunggah PRIVATE 25 Nov 2026 (upload.json: yOu1JLVvU-g), thumbnail ok | Pemilik: unggah subtitle.srt dan masukkan ke playlist secara manual di Studio (API gagal), lalu tentukan hari/jam tayang |
| 2026-11-22-ramayana-2-rama | riset, scenes.json, pelafalan | prompt_video, gambar |
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
