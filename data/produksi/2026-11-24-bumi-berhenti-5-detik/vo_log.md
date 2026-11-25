# Log VO: Bumi berhenti 5 detik
- Mesin: Google AI Studio, Gemini 3.8 Flash TTS (gemini-3.8-flash-tts). Suara: Bodi ('Quiet and intimate', nada rendah). Satu speech block, naskah utuh 208 kata.
- Take 1: gaya 'tenang, ±150 kata/menit, jeda sebelum fakta mengejutkan' = 1:36 (96 dtk). Dibuang karena melewati batas Short (95 dtk).
- Take 2 (dipakai): gaya 'tenang, hangat, sedikit misterius, ±165 kata/menit, jeda singkat' = 93,32 dtk. File: vo_bodi_take2.wav (WAV mono 24 kHz, 4,48 MB; nama asli unduhan 'Generated Audio November 24, 2026 - 10_12PM.wav' di Downloads).
- Catatan: tombol download sempat tertekan di posisi yang salah (mengenai tombol suka) sebelum unduhan benar; tidak berdampak pada audio.
- Loudness mentah: -24,8 LUFS integrated, true peak -2,5 dBFS. Perlu dinormalkan ke -14 LUFS (±1,5) saat rakit; true peak target <= -1 dBTP.
- Durasi 93,32 dtk: di atas toleransi 87-93, di bawah batas keras 95 dtk. Jendela scene dihitung total 93,0 dtk (awal 0,3 dtk dan ekor ±0,2 dtk dipotong).
- Cara mengukur: silencedetect (noise -38 dB, 0,28 dtk) memberi jeda antar kalimat. Batas scene dipasang di tengah jeda. Batas S06/S07 jatuh di tengah kalimat tanpa jeda panjang; dipasang di celah sunyi 46,1-46,9 dtk (±0,3 dtk). ASR tidak tersedia di sandbox (Hugging Face diblokir), jadi pemetaan kalimat memakai jumlah suku kata + jeda dan perlu didengar sekali oleh pemilik. Pelafalan belum didengar langsung oleh Hexa.
- Pelafalan yang perlu dicek telinga: 'Zimbelman', 'Subscribe', 'khatulistiwa', angka terbaca penuh ('seribu enam ratus tujuh puluh', 'dua koma tiga', 'empat puluh tujuh', 'satu koma tujuh').

## Tabel jendela scene (untuk rakit)
| Scene | Mulai (dtk) | Selesai (dtk) | Jendela (dtk) | VO |
|---|---|---|---|---|
| S01 | 0.00 | 11.70 | 11.7 | Bayangin Bumi berhenti berputar. Cuma lima detik. Kedengaran... |
| S02 | 11.70 | 17.40 | 5.7 | Dan alasannya bukan lamanya. Alasannya ada di kecepatan yang... |
| S03 | 17.40 | 23.90 | 6.5 | Saat ini kamu sedang melaju sekitar seribu enam ratus tujuh ... |
| S04 | 23.90 | 32.20 | 8.3 | Itu hasil keliling Bumi dibagi waktu satu putaran. Kita tida... |
| S05 | 32.20 | 40.20 | 8.0 | Sekarang Bumi mendadak berhenti. Tapi udara, laut, dan semua... |
| S06 | 40.20 | 46.50 | 6.3 | lebih dari seribu enam ratus kilometer per jam. Dalam lima d... |
| S07 | 46.50 | 52.30 | 5.8 | Hasilnya angin sekitar empat sampai lima kali rekor angin te... |
| S08 | 52.30 | 62.20 | 9.9 | Bangunan roboh, pohon tercabut, dan laut menyapu daratan sep... |
| S09 | 62.20 | 70.00 | 7.8 | Jadi yang berbahaya bukan lima detiknya, tapi berhentinya ya... |
| S10 | 70.00 | 78.20 | 8.2 | Satu sumber memperkirakan sekitar empat puluh tujuh kali gra... |
| S11 | 78.20 | 85.10 | 6.9 | Tenang, ini cuma pengandaian. Menurut geolog James Zimbelman... |
| S12 | 85.10 | 93.00 | 7.9 | Yang nyata justru pelan: hari memanjang sekitar satu koma tu... |
