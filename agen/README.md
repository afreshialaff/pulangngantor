# Agen Pulang ngantor

Agen produksi: **HEXA**. Skill lengkap: [`agen/hexa/SKILL.md`](hexa/SKILL.md) (v2.1: audit Sisi Terang, isi ≥6 menit, intro/outro wajib dari `assets/`).
Rakit video: `python tools/rakit_video.py --body out/isi.mp4 --out out/video.mp4`.

Bacaan wajib tiap sesi: `docs/MASTER-BRAND.md`, `docs/PELAJARAN-HEXA.md`, `docs/referensi/audit-sisi-terang.md`.
QC otomatis: `python tools/qc_lint.py data/produksi/<YYYY-MM-DD>`.

Aturan dasar (dari `docs/MASTER-BRAND.md`, bagian 16):
1. Pertahankan identitas Dark Mystery dan after-work storytelling; nama, tagline, konsep tidak diubah tanpa persetujuan pemilik.
2. Jangan mengubah atau menghapus channel lama tanpa izin eksplisit.
3. Bedakan fakta terbukti, dugaan, klaim, dan teori konspirasi; jangan sajikan spekulasi sebagai fakta.
4. Login, password, dan pembayaran selalu oleh pemilik.
5. Upload awal private sampai QC (checklist di master brand bagian 13) selesai.
6. Voice-over: Google AI Studio (Gemini TTS).
