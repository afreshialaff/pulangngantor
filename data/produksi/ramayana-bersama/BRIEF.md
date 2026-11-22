# BRIEF bersama: Ramayana 4 part (Pulang ngantor)

Pemilik: Thea. Tanggal kerja: 22 Nov 2026. Bahasa kerja dan naskah: Indonesia, bercerita santai (master brand bagian 2). Baca dulu: `CLAUDE.md`, `docs/MASTER-BRAND.md` (bagian 2, 4, 9, 10), `agen/hexa/SKILL.md` (Modul B, C, D, aturan retensi), `docs/referensi/audit-jagad-mandala.md` (pelajaran: janji judul dibayar terlambat, beban nama/istilah, kritik sumber, "catatan kepercayaan" untuk mitos).

## Seri
| Part | Folder | Cakupan (kata pemilik) |
|---|---|---|
| 1 | `2026-11-22-ramayana-1-rahwana` | Rahwana: dari remaja, balas dendam ke dewa, sampai jadi raja para raksasa dan menguasai beberapa daerah |
| 2 | `2026-11-22-ramayana-2-rama` | Rama lahir sebagai awatara Wisnu, masa kecil dan remaja, menikah, kebijaksanaan dan kekuatannya |
| 3 | `2026-11-22-ramayana-3-pengasingan-perang` | Inti Ramayana: pengasingan karena intrik istana dan perebutan kuasa (Rama menerima dharma), berpindah dari hutan ke hutan, konflik dengan Rahwana, Sinta diculik, Rama bertemu Hanoman, perang Rama-Rahwana, Sinta kembali |
| 4 | `2026-11-22-ramayana-4-moksa` | Setelah bertahun-tahun kerajaan aman, Rama menuntaskan dharma dan wafat/moksa, pengabdian terakhir Hanoman |

Durasi isi (tanpa intro 4,3 dtk dan outro 7,9 dtk): Part 1, 2, 4 = 26 scene (±6:30); Part 3 = 40 scene (±10:00) karena inti cerita. Minimal 360 detik isi per part, tanpa mengulur.

## Aturan inti (tidak boleh dilonggarkan)
1. **Mitos = catatan kepercayaan, bukan fakta sejarah.** Banyak umat Hindu (di Indonesia terutama di Bali) memuliakan Rama sebagai awatara Wisnu dan Ramayana sebagai kitab suci. Tulis hormat, tanpa mengolok, tanpa meremehkan, tanpa mengklaim "ini terbukti terjadi". Pakai frasa seperti "menurut Walmiki", "dalam kisahnya", "diyakini". Fakta yang boleh dinyatakan tegas hanya fakta filologi/sejarah (naskah, tanggal, relief, kakawin, siapa menulis, penelitian).
2. **Kelas tiap scene** (isi `kelas`): `fakta` (fakta sejarah/filologi yang bisa diverifikasi), `kisah` (isi kitab/tradisi, catatan kepercayaan), `versi` (perbedaan antar tradisi, mis. Walmiki, Kakawin Ramayana, wayang Jawa, Ramakien, Ramayana Bali), `dugaan` (hipotesis ilmuwan). `dugaan` wajib `keyakinan` ("terbukti" / "didukung" / "spekulatif"); lainnya `null`.
3. **Sumber:** tiap scene ≥1 id sumber, tiap klaim penting ≥2 sumber kredibel (kitab primer + sumber sekunder akademik/ensiklopedia). Catat kanda/sarga/bab bila dari Walmiki Ramayana (mis. "Uttarakanda 9-10"). Hormati catatan penting: **Balakanda dan Uttarakanda dianggap tambahan belakangan oleh banyak sarjana** (verifikasi sendiri ke sumber; tulis jujur: bagian Rahwana muda dan akhir hidup Rama bergantung pada Uttarakanda). Kakawin Ramayana (Jawa Kuno, abad ke-9) beda di beberapa bagian dari Walmiki: catat bedanya.
4. **Ejaan Indonesia** (Rama, Sinta, Rahwana, Hanoman, Laksmana, Bharata/Barata?, Satrugna, Dasarata, Kaikeyi, Kausalya, Sumitra, Wibisana, Kumbakarna, Indrajit/Megananda, Marica, Subali/Sugriwa, Jatayu, Ayodhya, Mithila, Alengka/Lanka, Dandaka, Panchawati). Pilih satu ejaan, pakai konsisten di satu part, daftarkan di `pelafalan.md` dengan cara baca untuk TTS.
5. **Bahasa:** santai bercerita, kalimat ≤20 kata, satu fakta per kalimat. Setiap nama/istilah baru dijelaskan dengan satu klausa. **Maksimal ±3 nama/istilah baru per 30 detik** (Ramayana penuh nama; mulai dari satu orang dan satu kejadian, bukan daftar nama). Analogi dunia kerja/kantor boleh dipakai sesekali, bila pas dan tidak merendahkan kisah sucinya (mis. intrik jabatan, "janji tertulis"), tanpa memaksa.
6. **Angka dan tahun di VO ditulis dengan kata penuh** ("sepuluh kepala", "seribu tahun"), supaya TTS membaca benar. Di `on_screen` boleh angka.
7. **Satu scene = satu gambar Flow = satu klip 15 detik.** VO per scene **30 sampai 34 kata (maksimal 35)** agar sekitar 14-15 dtk pada tempo 160 kata/menit. Jangan lebih. Jumlah scene sesuai tabel di atas. VO tiap scene boleh berisi 2-3 kalimat pendek.
8. **Retensi (aturan HEXA, wajib di tiap part):** VO dimulai langsung dengan hook ≤15 dtk (pertanyaan atau klaim yang membalik anggapan umum); `peta_3_poin` (3 kalimat) ≤45 dtk; **momen jawaban ≤90 dtk** (janji judul/thumbnail dibayar konkret di scene S01-S06); catat `momen_jawaban_detik`. Tanpa cliffhanger palsu. Penutup tiap part menyisakan satu pertanyaan untuk komentar dan (kecuali Part 4) mengarah ke part berikutnya tanpa CTA keras (CTA ada di outro resmi).
9. Part 1-3 menyambung ke part berikutnya secara naratif; Part 2-4 membuka dengan satu kalimat pengingat singkat (tanpa rekap panjang).
10. Tanpa konten kekerasan eksplisit/gore dan tanpa nuansa SARA. Tokoh jahat tidak dikarikaturkan; Rahwana digambarkan kompleks (terpelajar, taat tapa, sekaligus angkuh), sebagaimana teks.
11. Jangan menyalin kalimat dari terjemahan/buku modern (hak cipta). Parafrase dengan kata sendiri; kutipan ≤15 kata, bertanda, dengan atribusi, dan hanya dari terjemahan yang berstatus domain publik (mis. Griffith, 1870-74) atau naskah kuno.

## Bahasa visual (Flow, semua part)
Konsep: **arsip noir** brand + tradisi visual Nusantara yang dikenal penonton Indonesia: bayangan **wayang kulit** di balik kelir yang diterangi blencong (lampu minyak), **relief candi** batu andesit (gaya Prambanan/Borobudur, lahir dari kisah ini) disorot obor amber, **lontar** (daun palem berukir aksara tak terbaca), dan pemandangan alam/arsitektur bernuansa noir. Alasan: konsistensi tokoh antar scene, penghormatan (tidak membuat potret wajah dewa), dan menghindari tiruan desain film/komik tertentu.

Aturan gambar:
- Tokoh muncul sebagai **siluet wayang kulit berlubang (perforated leather puppet) di kelir**, **figur relief batu**, atau hanya tangan/bayangan. **Tanpa potret wajah realistis.** Mahkota, panah, busur, ukuran, dan sepuluh kepala (Rahwana) boleh jadi penanda tokoh.
- Satu subjek dominan per gambar, komposisi sederhana, tanpa teks terbaca, tanpa logo/watermark.
- Cahaya: satu sumber amber hangat di lingkungan biru-hitam gelap, kontras tinggi, grain film 35mm. Aksen merah tua (#8B1E1E) boleh untuk simbol bahaya (Rahwana/perang), krem (#E9D9C5) untuk kelir/lontar.
- Variasikan jenis gambar antar scene agar tidak monoton: (a) tablo wayang di kelir, (b) close-up relief batu, (c) lontar/naskah, (d) lanskap/arsitektur (hutan Dandaka, laut dan jembatan, kota Alengka, gunung), (e) objek (busur, panah, anting, cincin, perhiasan di tanah, api).
- Dilarang: meniru desain film/komik/anime/serial Ramayana tertentu, meniru lukisan tertentu, orang nyata, kekerasan eksplisit, telanjang, simbol/aksara terbaca.

`GAYA` (kalimat penutup tiap prompt gambar, jangan diubah oleh penulis scene; generator menambahkannya):
`cinematic noir still in the visual language of Javanese wayang kulit and candi relief, backlit perforated leather shadow-puppet silhouettes on a glowing oil-lamp screen OR deeply carved volcanic-stone temple relief lit by raking amber torchlight OR palm-leaf lontar texture, deep midnight navy and black shadows, single warm amber light source, subtle crimson accent, 35mm film grain, high contrast, single clear focal subject, 16:9, no text, no watermark`

## Skema `scenes.json` (satu file per part, di folder part)
```json
{
 "meta": {
  "part": 1,
  "judul_kerja": "…",
  "judul_varian": ["3 varian, ≤70 karakter, kata kunci kuat di 50 karakter pertama, tanpa '|' dan tanpa 'Baru Saja'"],
  "pilar": "…",
  "playlist": "salah satu dari config.yaml (jangan buat nama seri baru)",
  "peta_3_poin": ["…","…","…"],
  "momen_jawaban_detik": 0,
  "analogi": ["…"],
  "thumbnail_teks": "3-6 kata",
  "thumbnail_objek": "satu kata benda (siluet wayang/relief/dll)",
  "kata_kunci_utama": "…"
 },
 "sumber": {
  "walmiki_bk": {"atribusi": "…", "tahun": 0, "url": "…", "jenis": "primer|sekunder", "catatan": "…"}
 },
 "scenes": [
  {
   "id": "S01",
   "bagian": "Cold open | Latar belakang | Kronologi | Bukti & analisis | Kesimpulan | Closing (atau nama bab sesuai cerita)",
   "kelas": "fakta|kisah|versi|dugaan",
   "keyakinan": null,
   "sumber": ["walmiki_bk"],
   "rujukan": "mis. Uttarakanda sarga 9-10 (bila Walmiki)",
   "vo": "30-34 kata, Indonesia santai, angka dieja",
   "on_screen": "≤5 KATA KAPITAL",
   "sfx": "ambience/SFX singkat (Indonesia)",
   "kamera": "slow push-in (Indonesia/Inggris singkat)",
   "flow_subject": "English. ONE clear subject, concrete objects, lighting, composition. NO style suffix (generator adds GAYA). Must say figures are wayang-kulit silhouettes / relief figures / hands only.",
   "cam_en": "English camera move for the 15 s video, one direction, slow",
   "beat1": "English action 0-5 s",
   "beat2": "English action 5-10 s",
   "beat3": "English action 10-15 s (calm, stable last second)",
   "scan_asli": "id aset open-source (dari aset.md) atau null"
  }
 ]
}
```
Panjang `flow_subject` 25-60 kata, konkret, tanpa kata "photorealistic" dan tanpa nama merek/film. Beat video: gerak halus saja (nyala lampu bergoyang, debu, kain/siluet bergerak sedikit, kamera dolly/pan/tilt lambat), tidak ada perubahan bentuk drastis.

## File keluaran per part (folder part)
1. `riset.md`: riset mendalam, sangat detail, Indonesia: kronologi lengkap per kejadian dengan rujukan kanda/sarga, tokoh dan hubungan, **perbedaan versi** (Walmiki vs Kakawin Ramayana vs wayang Jawa vs Ramakien/lainnya) berlabel, **kontroversi/catatan filologi**, hal yang sengaja tidak dimasukkan ke video dan alasannya, daftar sumber (URL) dengan jenis primer/sekunder, dan "yang belum terverifikasi".
2. `scenes.json` sesuai skema di atas (hanya isi kreatif; generator memproses ke naskah, storyboard, prompt Flow, prompt video).
3. `pelafalan.md`: nama dan istilah + cara baca TTS (gaya: `- Rahwana: "RAH-wa-na"`).
4. Tulis hasil langsung ke folder part (path absolut ada di prompt tugasmu). Jangan menyentuh folder lain, `config.yaml`, atau master brand. Jangan commit/push.

## Format laporan akhir subagen (singkat)
Path file yang dibuat, jumlah scene dan jumlah kata VO total, `momen_jawaban_detik`, 5 temuan riset paling penting, daftar hal yang kamu ragukan atau tidak bisa diverifikasi (dengan alasan), dan setiap sumber yang tidak bisa dibuka.
