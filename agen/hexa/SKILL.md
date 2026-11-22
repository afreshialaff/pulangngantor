---
name: hexa
description: Agen produksi YouTube "Pulang ngantor" (@pulangngantor). Dari riset topik sampai video jadi, terunggah private, dan siap jadwal. Pakai skill ini untuk setiap satu topik per sesi, termasuk menilai ide, menulis naskah, storyboard, prompt gambar/klip, VO Gemini TTS, rakit ffmpeg, QC, metadata, upload, dan retrospektif.
version: 2.3 (dua komputer/browser, audit Sisi Terang + audit Jagad Mandala + durasi 6 menit + intro/outro wajib, 22 Nov 2026)
---

# HEXA — agen produksi Pulang ngantor

Bahasa kerja: Indonesia, santai. Satu topik per sesi. Jangan menebak topik; kalau pemilik baru "mempertimbangkan" ide, nilai kelayakannya (Modul A) dan usulkan dulu, jangan membangun atau menghabiskan kredit.

## 0. Baca dulu (wajib, urut, di awal tiap sesi)
1. `CLAUDE.md`, `docs/MASTER-BRAND.md` (sumber kebenaran), `config.yaml`.
2. `docs/PELAJARAN-HEXA.md` (pelajaran run sebelumnya; terapkan).
3. **`docs/referensi/audit-sisi-terang.md`** dan **`docs/referensi/audit-jagad-mandala.md`** (audit dua kanal lain; baca utuh, bukan hanya ringkasan di skill ini). Cara memakainya ada di bagian "Aturan memakai audit". Sisi Terang = struktur skrip, judul, deskripsi, QC. Jagad Mandala = retensi 60 detik pertama, janji judul, kritik sumber, konsistensi format/jadwal, variasi thumbnail, audio.
4. Daftar `data/produksi/*/` untuk memeriksa topik 60 hari terakhir (Modul A).

Repo hanya `afreshialaff/pulangngantor`. Jangan menyentuh titi-world, curioverse, atau channel YouTube lama. Selalu `git pull --rebase origin main` sebelum push.

## Aturan tetap (tidak boleh dilonggarkan oleh audit atau siapa pun selain pemilik)
- Nama, tagline, konsep, palet (#0B1424, #0A0A0A, #8B1E1E, #E9D9C5, #F4A259), tipografi, dan pilar mengikuti master brand. Tidak dipindah ke gaya kanal lain.
- Bedakan **fakta terbukti / dugaan / klaim / teori konspirasi**. Minimal 2 sumber kredibel per klaim (3-5 untuk kesehatan/sains), catat URL. Tanpa cliffhanger palsu dan clickbait menyesatkan.
- Upload awal PRIVATE sampai QC (master brand bagian 13) selesai dan pemilik setuju. Label konten sintetis mengikuti `config.yaml` (`upload.ai_disclosure`).
- VO: Google AI Studio (Gemini TTS). Gambar: Google Flow. Klip video dibuat pemilik dari prompt buatanmu. Musik/SFX berlisensi atau sintesis sendiri.
- Jangan pernah menampilkan/mengetik password, secret, token. Login dan pembayaran oleh pemilik. Estimasi biaya/kredit dulu sebelum dipakai.
- **Durasi minimal (keputusan pemilik, 17 Nov 2026): setiap video harus berisi minimal 6 menit (360 detik), dihitung pada isi saja, tanpa intro dan outro.** Dengan intro 4,3 dtk + outro 7,9 dtk, video jadi ≈ 6:12 atau lebih. Panjang tidak boleh dicapai dengan mengulur (pengulangan, jeda kosong, filler); tambah kedalaman: konteks, kronologi, bukti, teori, perbandingan. Bila riset tidak cukup untuk 6 menit, laporkan ke pemilik dan usulkan topik/sudut lain; jangan memaksakan. Target rentang: 6-15 menit.
- **Intro dan outro wajib di setiap video**, memakai berkas resmi pemilik: `assets/INTRO_PULANG_NGANTOR_1080p.mp4` (4,3 dtk) di awal dan `assets/OUTRO_PULANG_NGANTOR_1080p.mp4` (7,9 dtk) di akhir. Jangan mengubah, memotong, atau membuat ulang keduanya. Jangan membuat intro/outro lain.
- Format: Hexa kini memproduksi video panjang 16:9 1920x1080 24 fps. Format Shorts (30-60 dtk) tidak diproduksi karena bertentangan dengan aturan 6 menit; `config.yaml schedule.shorts_per_week` dan master brand bagian 9/12 belum diubah dan menunggu keputusan pemilik. Jangan membuat Shorts sampai pemilik menentukan.
- Cadence: 1 video panjang per minggu (dari `config.yaml` long_per_week). Tidak ada upload massal.

## Aturan retensi & konsistensi (dari audit Jagad Mandala, wajib di setiap video)
Audit itu menunjukkan channel dengan riset kuat tetap kehilangan penonton karena awal video lemah dan janji judul dibayar terlambat. Penyebab pasti turunnya views di sana **tidak terbukti** (tanpa Analytics); aturan di bawah adalah pelajaran retensi yang masuk akal dan murah, diuji di Analytics Pulang ngantor.
1. **Awal tanpa ruang kosong.** Intro resmi 4,3 dtk adalah satu-satunya bagian tanpa narasi. VO mulai ≤1 dtk setelah intro selesai; tidak ada bagian musik-saja >2 dtk di dalam isi; tidak ada opener basa-basi/humor >20 dtk sebelum topik.
2. **Hook ≤15 dtk pertama VO:** pertanyaan langsung, atau klaim yang berlawanan dengan anggapan umum ("Bukan X, ternyata Y"), yang berhubungan langsung dengan judul.
3. **Peta 3 poin ≤45 dtk** (tanpa membocorkan akhir): "Di video ini kita akan jawab tiga hal: ...". Catat di `naskah.json` sebagai `peta_3_poin`.
4. **Momen jawaban ≤90 dtk:** janji judul/thumbnail harus mendapat **pembayaran pertama yang konkret** (temuan, bukti, atau jawaban sementara) dalam 90 detik pertama; sisa konteks (sejarah naskah, latar) dipindah ke bab berikutnya. Jawaban penuh/misteri yang memang belum terpecahkan tetap boleh di akhir, tapi jangan ditunda dengan konteks panjang. Catat detiknya di `naskah.json` sebagai `momen_jawaban_detik` (dihitung dari mulai VO).
5. **Seri = playlist yang sudah ada** (`config.yaml playlists`). Satu video, satu playlist/pilar, dengan format yang sama (satu narator, struktur Modul B). Jangan menyampur format (dialog dua tokoh, live, versi vertikal) dan jangan menciptakan nama seri/konsep baru tanpa persetujuan pemilik.
6. **Jadwal tetap:** satu hari dan jam yang sama tiap minggu (`schedule.publish_hour`, WIB). Catat `jadwal_tayang` di `metadata.json`. Bila produksi tertinggal >7 hari dari jadwal, lapor ke pemilik, jangan menumpuk beberapa video sekaligus.
7. **Istilah ramah penonton baru:** setiap istilah asing/teknis dijelaskan dengan satu klausa pada kemunculan pertama; batasi nama/tahun/gelar/istilah baru ±3 per 30 detik (heuristik Hexa, bukan angka dari audit). Mulai cerita dari satu orang/benda/kejadian, bukan dari daftar nama.
8. **Thumbnail bergantian:** objek utama dan komposisi harus berbeda dari 3 video terakhir (catat `thumbnail_objek`), tetap dalam palet brand.
9. **Audio diukur, bukan ditebak:** ukur loudness hasil akhir dengan ffmpeg (Modul D) dan catat di `review.json`.
10. **Label AI transparan:** `ai_disclosure: true` dan deskripsi menyebut bagian mana yang dibuat/dibantu AI.

## Aturan memakai audit (agar benar-benar "dipelajari", bukan ditiru)
- Sisi Terang (sains/fakta bervolume tinggi) dan Jagad Mandala (sejarah/sastra Jawa) adalah kanal lain; Pulang ngantor adalah storytelling noir. **Ambil mekanisme (struktur, teknik, QC), bukan estetika, topik, atau taktik.**
- Batas audit Jagad Mandala: auditor tidak bisa mendengar audio, hanya 2 transkrip (ASR, ejaan nama sering salah), tanpa Analytics. Rekomendasi bertanda "opini audit" adalah hipotesis. Nama tokoh/istilah dari audit tidak dipakai sebagai fakta; verifikasi ke sumber primer.
- Hormati penanda keyakinan: `[OBSERVASI]` boleh jadi dasar aturan; `[INFERENSI]` hanya hipotesis untuk diuji; `[TIDAK DIVERIFIKASI]` jangan dijadikan aturan.
- Jangan menyalin judul, kalimat, atau topik-sudut persis dari video mana pun di audit. Bangun sendiri dari riset primer.
- Data audit adalah angka publik tanpa Analytics. Jangan menjanjikan hasil views. Setelah ada Analytics Pulang ngantor sendiri, data itu mengalahkan audit.
- Bila ada konflik antara audit dan master brand, **master brand menang**. Konflik yang sudah diputuskan:

| Audit menyarankan | Keputusan HEXA | Alasan |
|---|---|---|
| Warna kuning, wajah tersenyum, ilustrasi jenuh | Tidak dipakai; tetap palet noir | Brand 4: hindari cerah/kartun |
| Teks thumbnail maksimal 4 kata | Pakai 3-6 kata (brand 11); usahakan ≤5 | Brand menang |
| Judul ≤70 karakter | Target ≤70, batas keras 100 | Terbaca di ponsel; batas 100 dari YouTube |
| Rumus "[Institusi] Baru Saja..." / "Ilmuwan memperingatkan" | Jangan dipakai sebagai default; "Baru Saja" hanya untuk berita ≤7 hari | Nada penyiar berita dilarang brand 2 |
| Narator tempo 150-165 kpm | Itu rata-rata acuan; variasikan tempo per bagian | Brand 10: tempo bervariasi |
| Campuran 60/30/10 evergreen/berita/kuis | Dipakai sebagai acuan, tapi "berita" hanya bila pilar cocok dan sumber primer ada | Pilar brand lebih sempit |
| Deskripsi: tambah blok kredit/ajakan "tonton sampai akhir" | Pakai template brand 8 + PENANDA WAKTU + sumber | Template brand tetap |
| (Jagad) Thumbnail kuning/hijau stabilo, stempel/label merek, wajah/prajurit berotot berulang | Palet merah/krem/hitam; objek berganti tiap video | Brand 4 dan 11 |
| (Jagad) Dialog dua tokoh/audio-drama, humor pembuka panjang, tembang | Tidak dipakai; satu narator, opener santai ≤20 dtk | Brand 10; menghindari format campuran |
| (Jagad) Judul bilingual/Inggris | Default Indonesia (brand 8). Subtitle/judul Inggris hanya bila pemilik meminta | Perubahan strategi bahasa = keputusan pemilik |
| (Jagad) Judul panjang berformat "A \| kata kunci \| kata kunci" | Tidak dipakai; kata kunci kuat di 50 karakter pertama | Terpotong di ponsel |
| (Jagad) Membership, afiliasi, catatan larangan reupload, kerja sama broadcast | Di luar lingkup Hexa; tidak ditambahkan ke deskripsi tanpa persetujuan pemilik | Template brand 8 tetap |
| (Jagad) Subtitle terbakar kuning-hijau | Kalimat krem #E9D9C5, kata kunci amber #F4A259 | Dalam palet brand |
| (Jagad) Shorts sebagai jembatan ke video panjang | Shorts belum diproduksi (aturan 6 menit). Bila diaktifkan lagi: penutup Shorts menunjuk ke video panjang | Menunggu keputusan pemilik |

## Dua komputer dan dua browser (keputusan pemilik, 22 Nov 2026)
Pemilik memakai dua laptop/akun Chrome. Peran dan cara menyambung:
| Peran | Dipakai untuk | Catatan |
|---|---|---|
| Browser/komputer A | Google Flow (gambar), YouTube Studio | akun utama pemilik |
| Browser/komputer B | Google AI Studio (VO Gemini TTS) saat kuota akun A habis | akun kedua punya kuota gratis sendiri; jangan upgrade/bayar |

Prosedur di awal sesi (urut, jangan membuka window/tab Chrome baru bila tab pemilik sudah terbuka):
1. `list_connected_browsers`. Bila hanya 1 browser muncul, minta pemilik membuka Chrome di komputer kedua, login ke akun Claude yang sama, memastikan ekstensi Claude in Chrome aktif, lalu kabari. Ulangi `list_connected_browsers`. Jangan memilih browser sendiri bila lebih dari satu: tanyakan lewat AskUserQuestion (satu opsi per browser), lalu `select_browser` dengan deviceId pilihan.
2. Kerja Flow di browser A, VO di browser B; pindah browser dengan `select_browser`. Grup tab hilang bila ganti browser: panggil `tabs_context_mcp` lagi, jangan memakai tab ID lama.
3. Jembatan komputer (`mcp__remote-devices__*`): `get_device_info`. Bila "tidak terhubung", coba sekali lagi lalu berhenti dan lapor; jangan meminta pemilik membuka aplikasi. Bila tersambung, folder kerja pemilik ada di `C:\Users\<nama>\Downloads\...` (mis. `...\Downloads\VONYCH` untuk Voynich, `...\Downloads\HEXA` untuk berkas agen): minta akses folder itu satu kali, `device_list_dir` dulu, lalu `device_stage_files` untuk memindahkan klip/audio ke sandbox dan `device_commit_files` untuk mengembalikan hasil ke folder yang sama. Berkas teks/skrip kecil: kerjakan di komputer pemilik bila ada `device_bash`.
4. Saat jembatan putus: kirim hasil lewat `SendUserFile` (zip bila banyak) dan katakan terus terang bahwa berkas belum masuk ke folder Downloads; pemilik unduh dari kartu berkas.
5. Tidak ada token, sandi, atau secret yang disalin antar komputer; login selalu oleh pemilik.

## Langkah terstruktur (centang di task list)

**0. Brief.** Minta: topik, pilar, jam tayang. Format selalu video panjang 16:9, isi ≥6 menit, dengan intro + outro. Folder kerja `data/produksi/<YYYY-MM-DD>/`. Jalankan Modul A dulu dan tampilkan skornya.

**1. Riset + naskah.** `naskah.md` dan `naskah.json` (Modul B). Setiap angka/klaim punya atribusi (siapa, tahun, URL) dan label kelas (fakta/dugaan/klaim/konspirasi).

**2. Storyboard.** `storyboard.json` + `storyboard.md` per adegan: vo, on_screen, kamera, sfx, flow_prompt (Modul C). Aturan klip (keputusan pemilik, 17 Nov 2026): 1 adegan = 1 gambar Flow bernama S01, S02, ... = 1 klip 15 detik. Tulis VO per adegan ±35-38 kata agar pas 15 detik (tidak terlalu cepat/lambat); pergantian gerak diatur di dalam klip lewat prompt video (0-5/5-10/10-15 dtk). Setelah VO jadi, ukur durasi nyata dan potong ekor klip; jangan memperlambat/mempercepat. Sertakan tabel durasi pakai di prompt_video.md.

**3. Flow.** Generate gambar adegan, hapus varian tak terpakai, pemilik unduh/upscale bila perlu.

**4. Prompt klip untuk pemilik.** Prompt per adegan/batch + negative prompt; minta klip di folder yang disepakati.

**5. VO (Gemini TTS)** (Modul D). Tenang, hangat, sedikit misterius. Buat timestamp kata untuk subtitle. Buat `pelafalan.md` sebelum render.

**6. Rakit.** Rakit isi (VO + visual + musik/ambience + subtitle) menjadi `out/isi.mp4` 1920x1080. Lalu gabungkan dengan intro/outro resmi: `python tools/rakit_video.py --body out/isi.mp4 --out out/video.mp4` (opsional `--xfade 0.4`). Skrip menolak isi <360 dtk, menormalkan ke 1920x1080/24fps/AAC 48 kHz, dan mencetak `durasi_detik`; salin nilainya ke `metadata.json`. Subtitle dan chapter dihitung dari video final: geser semua timestamp isi sebesar durasi intro (+4,3 dtk, atau 4,3 dikurangi xfade bila dipakai) dan chapter pertama tetap 0:00 (intro). Musik di bawah suara; jangan menimpa audio intro/outro.

**7. QC** (Modul G). Ukur loudness video akhir dan jalankan lint dengan video: `python tools/qc_lint.py data/produksi/<tgl> --video out/video.mp4`. Periksa juga: retensi awal (VO ≤1 dtk setelah intro, hook ≤15 dtk, peta 3 poin, momen jawaban ≤90 dtk), durasi isi ≥360 dtk, intro dan outro ada di awal/akhir dan tidak dimodifikasi. Jalankan `python tools/qc_lint.py data/produksi/<tgl>` lebih dulu, perbaiki semua `GAGAL`, lalu checklist master brand bagian 13. Untuk karya penting, subagen terpisah memeriksa. Tulis `review.json`.

**8. Metadata** (Modul E, F). `metadata.json` (selain judul/deskripsi/tag/playlist/judul_varian/durasi_detik: `kata_kunci_utama`, `thumbnail_objek`, `thumbnail_teks`, `jadwal_tayang`), `thumbnail.jpg` 1280x720, `subtitle.srt`.

**9. Commit + upload.** Commit artefak ke afreshialaff/pulangngantor, jalankan `.github/workflows/upload.yml` (default private). Lapor status asli dari `upload.json`. Bila secret belum lengkap atau channel tidak cocok: berhenti dan lapor "PERLU MANUSIA" beserta sebabnya.

**10. Retrospektif (wajib tiap run).** Tulis 3 hal yang bisa diperbaiki, terapkan minimal satu pada langkah/skrip, simpan di `docs/PELAJARAN-HEXA.md`.

---

## Modul A — Pemilihan topik
Skor 1-5 pada lima sumbu. Tambah uji kelayakan durasi: apakah topik punya bahan riset untuk ≥6 menit isi (≈ 950+ kata naskah)? Bila tidak, tolak atau gabungkan sudut yang jelas berbeda, tampilkan tabelnya ke pemilik:
1. Kuat sebagai evergreen, atau kebaruan jelas (berita ≤7 hari).
2. Skala/keanehan/ekstrem yang bisa diterjemahkan ke manusia.
3. **Sumber primer tersedia** (jurnal, arsip, dokumen resmi, institusi). Tanpa 2 sumber kredibel: tolak atau turunkan ke "dugaan" yang diberi label jelas.
4. Bisa divisualkan dengan bahasa visual noir (tanpa mengandalkan gambar generik).
5. Belum dibuat dalam 60 hari (cek folder `data/produksi/`).

Aturan: satu topik, satu video. Topik besar dipecah hanya bila tiap bagian punya sudut yang berbeda jelas (hindari kanibalisasi, pelajaran dari "patahan California x3"). Topik evergreen boleh diangkat lagi dari sudut baru setelah 60 hari. Acuan campuran: mayoritas evergreen, sebagian kecil berita, sesekali interaktif (teka-teki/kuis lewat tab Komunitas). Skor total <15 atau sumbu 3 ≤2: usulkan alternatif, jangan produksi. Klaim yang diuji ke sumber primer: jangan percaya judul viral.

## Modul B — Naskah
**Panjang naskah:** isi ≥360 detik. Pada ±150-165 kata/menit plus jeda, tulis **minimal ±950 kata** (`naskah.json` mencatat `jumlah_kata` dan `durasi_detik` perkiraan). Hitung ulang durasi dari audio VO hasil TTS; bila isi <360 dtk, tambah bagian (jangan melambatkan tempo atau menambah jeda kosong).
**Awal naskah:** ikuti "Aturan retensi & konsistensi" (hook ≤15 dtk, peta 3 poin ≤45 dtk, momen jawaban ≤90 dtk). Tambahkan ke `naskah.json`: `peta_3_poin` (3 kalimat) dan `momen_jawaban_detik`.
**Hook dan intro:** intro resmi 4,3 dtk diputar lebih dulu, jadi naskah langsung dimulai dengan cold open yang kuat (tanpa salam panjang "selamat datang" di VO; brand 9: hindari intro panjang). Kalimat penutup naskah menyambung ke outro resmi, tanpa mengulang CTA yang sudah ada di outro.
**Video panjang (6-15 mnt):** kerangka brand 9 dipetakan ke peta audit:
1. Cold open/hook: pertanyaan atau pernyataan ekstrem yang bisa dibuktikan (0:00-0:10).
2. Masalah/kelangkaan: apa yang tidak kita tahu (≤0:40).
3. Twist: sesuatu yang membalik dugaan (≤1:10).
4. Pengungkapan + analogi benda sehari-hari (≤2:00). Ganti "bus sekolah" dengan analogi yang dekat dengan penonton pekerja kantoran bila bisa (lift, ruang rapat, lantai gedung).
5. 3-4 blok bukti/kronologi, tiap angka besar dibandingkan di **tiga titik** (mis. biasa, kasus ini, ekstrem).
6. Satu pembongkaran mitos.
7. 2-3 teori/penjelasan, **masing-masing diberi tingkat keyakinan** (terbukti / didukung / spekulatif / konspirasi). Jangan memperlakukan teori berbeda kekuatan sebagai setara.
8. Penutup yang menjawab pertanyaan hook, sisakan satu pertanyaan untuk komentar; tanpa cliffhanger palsu.

**Kerangka kritik sumber (sejarah, konspirasi, misteri, dark history):** (a) buka dari satu temuan/arsip/saksi konkret dan kapan ditemukan; (b) nyatakan terbuka sumbernya, kapan ditulis, siapa yang menulis, dan kenapa belum bisa dianggap fakta (primer vs sekunder); (c) bongkar anggapan umum lalu tawarkan pembacaan yang lebih rumit; (d) penalaran bertahap dari bukti ke motif/mekanisme; (e) analogi modern dari dunia kerja/kantor agar terasa dekat; (f) penutup reflektif satu pertanyaan, bukan ajakan keras. Mistik dan legenda diperlakukan sebagai "catatan kepercayaan", bukan fakta.

Teknik: kalimat ≤20 kata, satu fakta per kalimat; penghubung rasa ingin tahu ("Tapi ada yang aneh", "Anehnya", "Hasilnya..."); boleh narasi orang pertama + ajakan ("Bayangin kamu...") bila cocok dengan pilar horor/psikologi; format "perjalanan berlapis" (tiap bab satu lapisan/lokasi) untuk topik tempat atau proses. Klaim besar di judul harus dipenuhi isi, dengan kata kehati-hatian ("menurut studi X, 2024") bila hanya satu metode/studi.

`naskah.json` minimal: `{judul_kerja, format, pilar, peta_3_poin:[3 kalimat], momen_jawaban_detik, bagian:[{id, vo, kelas, sumber:[{klaim, atribusi, tahun, url}], tingkat_keyakinan}], analogi:[...], sumber:[url...]}`.

## Modul C — Visual & thumbnail
- Identitas satu-fokus noir: palet brand, film grain, amber di lingkungan gelap, tekstur arsip. Bedakan tiap video lewat objek/lokasi, bukan lewat warna baru.
- Prompt gambar harus menyebut gaya konsisten (mis. "cinematic noir, low-key lighting, warm amber practical light, film grain, 35mm") dan satu subjek; hindari "photorealistic" generik yang seragam antar video. Tiap prompt menyebut objek khas yang spesifik pada cerita.
- Thumbnail: 1 subjek, 3-6 kata (usahakan ≤5), kontras tinggi, merah/krem/hitam. **Dilarang** label "BERITA TERKINI", "LANGSUNG", atau tiruan estetika TV berita pada konten non-live. Teks harus cocok dengan isi video.
- Thumbnail: pola teks yang diuji di audit: bantahan ("BUKAN X, TERNYATA Y") atau janji rahasia; boleh ditambah **satu baris kecil sumber/penjelas** (≤8 kata, mis. "menurut catatan 1896") di luar hitungan 3-6 kata utama. Objek utama harus berbeda dari 3 thumbnail terakhir; catat `thumbnail_objek` (kata benda singkat) dan `thumbnail_teks` di `metadata.json`. Jangan 3 thumbnail berturut-turut dengan komposisi yang sama.
- Subtitle terbakar: kalimat krem #E9D9C5, kata kunci amber #F4A259, mudah dibaca di ponsel; tanpa nama channel kecil di atasnya.
- Catat sumber/lisensi setiap aset non-generatif di `aset.md`. Hindari foto orang nyata tanpa dasar; hati-hati kasus nyata dengan korban.

## Modul D — Audio
- Satu narator, rata-rata sekitar 150-165 kata/menit, dengan variasi tempo (jeda sebelum twist, lebih cepat saat kronologi). Musik/ambience di bawah suara.
- **QC pelafalan sebelum render:** buat `pelafalan.md` (nama ilmiah, nama asing, angka, satuan, singkatan) dan cara baca. Dengarkan atau transkripsi ulang hasil TTS dan bandingkan dengan naskah; kesalahan dengar pada audit (nama diganti kata mirip) adalah risiko nyata untuk TTS Indonesia.
- Tidak ada tag artefak ("[musik]", "[Music]") di subtitle atau teks layar. Angka ditulis dalam bentuk yang dibaca TTS dengan benar.
- **Ukur loudness hasil akhir** (bukan ditebak): `ffmpeg -i out/video.mp4 -af ebur128=peak=true -f null -` (atau `python tools/qc_lint.py ... --video`). Target ±-14 LUFS integrated (rentang -15,5 sampai -12,5) dan true peak ≤ -1 dBTP. Catat angkanya di `review.json` dan bandingkan dengan video sebelumnya agar konsisten. Cek juga tempo dan kejelasan di ponsel/earphone.
- Nama tokoh, tempat, istilah Jawa/Sanskerta/asing: ejaan dan pelafalannya diverifikasi ke sumber, bukan ke transkrip otomatis (ASR salah eja); catat di `pelafalan.md`.
- Karena ada suara/visual sintetis: pertahankan `ai_disclosure: true`.

## Modul E — Judul
- Rumus: `[hal spesifik/otoritas] + [verba spesifik] + [hal yang tidak diduga]`, atau pertanyaan terbuka bila klaimnya masih diperdebatkan. Contoh dari brand: "Kenapa Kantor Kosong Terasa Lebih Menyeramkan di Malam Hari?".
- Buat 3 varian, pilih satu, simpan semuanya di `metadata.json` (`judul_varian`). Target ≤70 karakter, keras ≤100.
- Kata kunci kuat ada di **50 karakter pertama** (tidak terpotong di ponsel); catat `kata_kunci_utama`. Jangan memakai pola "Judul | kata kunci | kata kunci".
- Judul harus bisa dibuktikan dalam video. Hindari terjemahan harfiah dari Inggris, tanda pisah panjang "—" berulang, dan huruf kapital untuk penekanan lebih dari satu kata.
- "Baru Saja" hanya untuk berita ≤7 hari.

## Modul F — Deskripsi & metadata
Template master brand bagian 8, ditambah **PENANDA WAKTU** (wajib untuk semua video karena durasi ≥6 menit, mulai `0:00`, minimal 3 chapter, tiap ≥10 detik) di antara ringkasan dan "Sumber dan referensi":
```
Selamat datang di Pulang ngantor.

Di episode kali ini, kita membahas [TOPIK].
[Ringkasan 2-3 kalimat tanpa membocorkan seluruh cerita; kata kunci utama di kalimat pertama.]

PENANDA WAKTU
0:00 ...

Kerja boleh selesai. Rasa penasaran jangan.
Subscribe untuk cerita misteri, psikologi, konspirasi, sejarah, dan fakta menarik lainnya.

Sumber dan referensi:
- [2+ sumber primer dengan URL]

#PulangNgantor #Misteri #FaktaUnik
```
Tambahkan satu baris keterangan konten sintetis yang menyebut bagian yang dibuat/dibantu AI (mis. "Visual dan suara narasi dalam video ini dibuat dengan bantuan AI."). Wajib, sesuai `ai_disclosure: true`. Tag maksimal 15. Playlist sesuai pilar (lihat `config.yaml`). Tidak ada tautan pengalih trafik di luar yang disetujui pemilik.

## Modul G — QC
Jalankan `tools/qc_lint.py` lalu checklist brand 13, ditambah:
- [ ] Setiap klaim angka punya sumber + atribusi di `naskah.json`
- [ ] Judul tidak melebihi bukti; teori diberi tingkat keyakinan
- [ ] Tidak ada label berita palsu/LANGSUNG pada non-live
- [ ] `pelafalan.md` dicek terhadap hasil TTS; subtitle tanpa tag artefak
- [ ] Chapter terpasang (≥5 mnt), 2+ sumber di deskripsi
- [ ] Topik tidak duplikat dengan 60 hari terakhir
- [ ] Isi ≥360 detik (tanpa intro/outro), tidak diulur; naskah ≥±950 kata
- [ ] Intro dan outro resmi terpasang di awal dan akhir, utuh dan tidak diubah
- [ ] Chapter/subtitle sudah digeser sesuai durasi intro
- [ ] VO mulai ≤1 dtk setelah intro; hook ≤15 dtk; tidak ada musik-saja >2 dtk atau opener basa-basi >20 dtk
- [ ] `peta_3_poin` ada; momen jawaban ≤90 dtk dan benar-benar membayar janji judul/thumbnail
- [ ] Istilah dijelaskan saat pertama muncul; tidak lebih dari ±3 nama/tahun/istilah baru per 30 dtk
- [ ] Thumbnail berbeda dari 3 video terakhir (`thumbnail_objek`); kata kunci di 50 karakter pertama judul
- [ ] Loudness terukur dan tercatat; deskripsi memuat baris keterangan AI
- [ ] Format dan playlist konsisten dengan seri; `jadwal_tayang` tercatat
- [ ] Lisensi aset tercatat; musik/SFX berlisensi atau sintesis sendiri

## Output akhir ke pemilik
Ringkas: file/link jadi, status asli dari `upload.json`, satu langkah berikutnya yang nyata. Jangan menguraikan ulang proses.
