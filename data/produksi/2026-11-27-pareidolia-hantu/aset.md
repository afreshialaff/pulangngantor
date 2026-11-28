# Aset lokal (ASUS, Downloads/PAREIDOLIA-HANTU)

- VO_pareidolia.wav (127,11 dtk; salinan identik di VIDEO/)
- PICTURE/S01..S14 *_2K.jpg (14 gambar)
- VIDEO/S01..S14.mp4 (1080x1920, 24 fps; lengkap 28 Nov)
- VIDEO/S12_v2.mp4 (pengganti S12 yang disarankan)

Belum ada: S04-S14 (cek 28 Nov ±19.05 WIB; S02 11,03 dtk dan S03 9,02 dtk sudah ada).

Sumber aset: gambar Google Flow, VO Google AI Studio, klip Nexabot. Musik/SFX belum ada.

## Cek 28 Nov (run terjadwal)
- S01: lembar kontak 1 fps (9 frame): karakter, jam, selimut, dan jemuran konsisten; logo bintang kecil di kanan bawah terlihat.
- VO asli: -16,5 LUFS, true peak +1,1 dBTP (di luar batas -15,5..-12,5 LUFS dan <= -1 dBTP). Berkas asli tidak diubah.
- Uji sementara (hasil tidak disimpan): `-af "aresample=192000,volume=2.5dB,alimiter=limit=0.794:level=false:attack=5:release=50,aresample=48000"` memberi -15,1 LUFS; true peak -2,0 dBTP, durasi tetap 127,11 dtk. Pakai rantai ini (atau setara) saat rakit, lalu ukur ulang video akhir.
- Cek ±19.05 WIB: S02 ada dissolve sekitar detik 8,7-10,8 (lembar kontak 6 fps dari detik 7); S03 konsisten pada lembar kontak 1 fps.
