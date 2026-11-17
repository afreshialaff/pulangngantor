# Log VO (Google AI Studio, Gemini 3.8 Flash TTS, suara Bodi) — 17 Nov 2026
Style: "Bahasa Indonesia santai seperti teman bercerita malam hari: hangat, tenang, sedikit misterius. Tempo mengalir natural sekitar 160 kata per menit, tanpa jeda panjang di awal atau akhir. Tidak teatrikal, bukan penyiar berita."
Catatan kalibrasi: tempo mengikuti angka di style (150 kpm -> 18 dtk untuk 37 kata; 175 kpm -> 11 dtk untuk 31 kata; 160 kpm -> ~12-15 dtk).

Durasi terukur (detik, dari pemutar AI Studio):
S01 15 | S02 13 | S03 15 | S04 13 | S05 13 | S06 14 | S07 14 | S08 13 | S09 13 | S10 13 | S11 14 | S12 12 | S13 15
S14 12 | S15 15 | S16 15 | S17 14 | S18 14 | S19 17 (KEPANJANGAN) | S20 12 | S21 15 | S22 17 (KEPANJANGAN) | S23 13 | S24 13
S25 15 | S26 15 (digenerate setelah kuota pulih sebentar)
S19 dan S22 versi pangkas: belum terukur (kuota kena batas lagi).
Jumlah S01-S24 = 327 dtk. Audio belum diunduh/disimpan (hanya diputar di pemutar AI Studio).
Perbaikan naskah: S19 dan S22 dipangkas jadi <=34 kata sebelum generate ulang.

## VO final (dipakai di video) — satu kali generate, akun kedua
Berkas: VO.wav (24 kHz mono, 399,8 dtk), dari pemilik di Downloads\VONYCH\VID. Dipotong per paragraf dengan penjajaran kalimat ke jeda (silencedetect + jumlah suku kata), 83 kalimat terpetakan.
Durasi VO per adegan (dtk) | slot di video | faktor regang klip (tidak ada bagian klip yang dipotong):
- S01: VO 16.5 | slot 17.5 | klip x1.218
- S02: VO 16.2 | slot 17.2 | klip x1.185
- S03: VO 16.3 | slot 17.3 | klip x1.189
- S04: VO 15.6 | slot 16.6 | klip x1.156
- S05: VO 13.6 | slot 14.6 | klip x1.008
- S06: VO 15.6 | slot 16.6 | klip x1.156
- S07: VO 14.1 | slot 15.1 | klip x1.038
- S08: VO 13.7 | slot 14.7 | klip x1.014
- S09: VO 13.9 | slot 14.9 | klip x1.026
- S10: VO 14.4 | slot 15.4 | klip x1.057
- S11: VO 14.7 | slot 15.7 | klip x1.080
- S12: VO 13.5 | slot 14.5 | klip x1.015
- S13: VO 14.8 | slot 15.8 | klip x1.089
- S14: VO 14.4 | slot 15.4 | klip x1.063
- S15: VO 16.2 | slot 17.2 | klip x1.184
- S16: VO 15.2 | slot 16.2 | klip x1.120
- S17: VO 15.7 | slot 16.7 | klip x1.152
- S18: VO 15.5 | slot 16.5 | klip x1.137
- S19: VO 13.9 | slot 14.9 | klip x1.029
- S20: VO 12.5 | slot 13.5 | klip x0.935
- S21: VO 14.1 | slot 15.1 | klip x1.059
- S22: VO 13.9 | slot 14.9 | klip x1.031
- S23: VO 14.3 | slot 15.3 | klip x1.059
- S24: VO 12.9 | slot 13.9 | klip x0.962
- S25: VO 16.5 | slot 17.5 | klip x1.219
- S26: VO 16.6 | slot 17.6 | klip x1.169
Isi video (tanpa intro/outro): 409.6 dtk.
