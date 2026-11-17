# Rakit video HEXA per segmen (dipakai pertama kali untuk Voynich, 17 Nov 2026)

Urutan (jalankan dari folder kerja yang berisi VO.wav dan klip S1..S26.mp4; path masih tertulis di skrip):
1. `align.py` lalu `align2.py`: cari jeda (silencedetect) dan petakan tiap kalimat naskah ke jeda (jumlah suku kata). Hasil: sent.json. Tanpa ASR (Hugging Face diblokir di sandbox).
2. `timeline.py`: slot per adegan = durasi VO + 1 dtk; klip diregang/dipercepat (0,88-1,22x), tidak ada bagian klip yang dipotong. Transisi: fadeblack antarbagian, smoothleft di kronologi, dissolve/zoomin di dalam bagian.
3. `seg.py`: render + QC tiap segmen langsung (durasi, 1920x1080, blackdetect, frame contoh). Label adegan (Montserrat + Bebas Neue, palet brand).
4. `audio.py`: VO per paragraf ditempatkan di timeline, bed drone sintetis (bebas lisensi) + whoosh di transisi, ducking, loudnorm -14 LUFS.
5. `subs.py` + `ass.py`: subtitle dari teks naskah (angka -> digit, tahun tanpa titik ribuan), ASS untuk burn-in dan SRT untuk YouTube.
6. `final.py`: intro + 26 segmen (xfade) + outro + subtitle, satu kali encode.
Font: npm @fontsource/bebas-neue dan @fontsource/montserrat (woff2 -> ttf dengan fontTools).
