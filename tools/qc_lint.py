#!/usr/bin/env python3
"""Linter QC otomatis untuk satu folder produksi (pelajaran dari audit Sisi Terang).

python tools/qc_lint.py data/produksi/<YYYY-MM-DD>

Mengeluarkan GAGAL (harus diperbaiki) / PERINGATAN (periksa) / OK. Exit 1 bila ada GAGAL.
Hanya memeriksa berkas yang ada; berkas yang belum dibuat dilaporkan sebagai PERINGATAN.
"""
import json
import os
import re
import sys

LABEL_BERITA = re.compile(r"(?i:berita\s+terkini|breaking\s+news)|\bLANGSUNG\b|\bLIVE\b")
ARTEFAK = re.compile(r"\[\s*(musik|music|tepuk tangan|applause)\s*\]", re.I)
CHAPTER = re.compile(r"^\s*(\d{1,2}:)?\d{1,2}:\d{2}\s+\S", re.M)


def baca_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def main(folder):
    hasil = []

    def add(level, msg):
        hasil.append((level, msg))

    meta = baca_json(os.path.join(folder, "metadata.json"))
    naskah = baca_json(os.path.join(folder, "naskah.json"))

    if meta is None:
        add("PERINGATAN", "metadata.json belum ada")
    else:
        judul = meta.get("judul", "")
        deskripsi = meta.get("deskripsi", "")
        if len(judul) > 100:
            add("GAGAL", f"judul {len(judul)} karakter (>100)")
        elif len(judul) > 70:
            add("PERINGATAN", f"judul {len(judul)} karakter (target <=70)")
        if "—" in judul:
            add("PERINGATAN", "judul memakai tanda pisah panjang (kesan terjemahan/AI)")
        if re.search(r"baru saja", judul, re.I):
            add("PERINGATAN", "'Baru Saja' hanya untuk berita <=7 hari; konfirmasi")
        if sum(1 for w in re.findall(r"\b[A-Z]{3,}\b", judul)) > 1:
            add("PERINGATAN", "lebih dari satu kata KAPITAL di judul")
        if LABEL_BERITA.search(judul):
            add("GAGAL", "judul memuat label berita/LANGSUNG; hanya boleh untuk siaran live")
        if "Sumber dan referensi" not in deskripsi:
            add("GAGAL", "deskripsi tanpa blok 'Sumber dan referensi'")
        elif len(re.findall(r"https?://", deskripsi.split("Sumber dan referensi", 1)[1])) < 2:
            add("GAGAL", "kurang dari 2 URL sumber di deskripsi")
        if "[DAFTAR SUMBER]" in deskripsi:
            add("GAGAL", "placeholder [DAFTAR SUMBER] belum diganti")
        if len(meta.get("tag", [])) > 15:
            add("GAGAL", "tag lebih dari 15")
        durasi = (meta.get("durasi_detik") or (naskah or {}).get("durasi_detik") or 0)
        if durasi >= 300 and len(CHAPTER.findall(deskripsi)) < 3:
            add("GAGAL", "semua video (>=6 menit) wajib punya >=3 chapter (PENANDA WAKTU, mulai 0:00)")
        if durasi >= 300 and not re.search(r"^\s*0:00\b", deskripsi, re.M):
            add("GAGAL", "chapter pertama harus 0:00")
        isi = meta.get("isi_detik") or (naskah or {}).get("isi_detik") or 0
        if durasi and durasi < 372:
            add("GAGAL", f"durasi total {durasi} dtk; isi harus >=360 dtk + intro/outro (~372 dtk)")
        if isi and isi < 360:
            add("GAGAL", f"isi video {isi} dtk < 360 dtk (6 menit)")
        if not durasi:
            add("PERINGATAN", "durasi_detik belum dicatat di metadata.json (hasil tools/rakit_video.py)")
        if len(meta.get("judul_varian", [])) < 3:
            add("PERINGATAN", "simpan 3 varian judul di metadata.json (judul_varian)")

    if naskah is None:
        add("PERINGATAN", "naskah.json belum ada")
    else:
        kata = sum(len(b.get("vo", "").split()) for b in naskah.get("bagian", []))
        if kata and kata < 900:
            add("GAGAL", f"naskah {kata} kata; butuh >=~950 kata untuk isi 6 menit")
        for b in naskah.get("bagian", []):
            if not b.get("sumber"):
                add("GAGAL", f"bagian '{b.get('id')}' tanpa sumber/atribusi")
            if not b.get("kelas"):
                add("PERINGATAN", f"bagian '{b.get('id')}' tanpa kelas (fakta/dugaan/klaim/konspirasi)")
            if b.get("kelas") in ("dugaan", "klaim", "konspirasi") and not b.get("tingkat_keyakinan"):
                add("GAGAL", f"bagian '{b.get('id')}' berkelas {b['kelas']} tanpa tingkat_keyakinan")
            for kalimat in re.split(r"(?<=[.!?])\s+", b.get("vo", "")):
                if len(kalimat.split()) > 20:
                    add("PERINGATAN", f"kalimat >20 kata di '{b.get('id')}': {kalimat[:50]}...")

    srt = os.path.join(folder, "subtitle.srt")
    if os.path.exists(srt):
        if ARTEFAK.search(open(srt, encoding="utf-8").read()):
            add("GAGAL", "subtitle.srt memuat tag artefak seperti [musik]")
    else:
        add("PERINGATAN", "subtitle.srt belum ada")

    for nama in ("INTRO", "OUTRO"):
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", f"{nama}_PULANG_NGANTOR_1080p.mp4")):
            add("GAGAL", f"assets/{nama}_PULANG_NGANTOR_1080p.mp4 tidak ada")
    if not os.path.exists(os.path.join(folder, "pelafalan.md")):
        add("PERINGATAN", "pelafalan.md belum ada (QC pelafalan TTS)")
    if not os.path.exists(os.path.join(folder, "thumbnail.jpg")):
        add("PERINGATAN", "thumbnail.jpg belum ada")

    # duplikat topik 60 hari: bandingkan judul dengan folder produksi lain
    induk = os.path.dirname(os.path.abspath(folder))
    if meta:
        kata = set(re.findall(r"\w{5,}", meta.get("judul", "").lower()))
        for nama in sorted(os.listdir(induk)):
            lain = os.path.join(induk, nama, "metadata.json")
            if nama == os.path.basename(os.path.abspath(folder)) or not os.path.exists(lain):
                continue
            kata2 = set(re.findall(r"\w{5,}", baca_json(lain).get("judul", "").lower()))
            if kata and len(kata & kata2) / max(len(kata), 1) >= 0.6:
                add("PERINGATAN", f"judul mirip dengan {nama}; cek duplikasi 60 hari")

    if not any(l == "GAGAL" for l, _ in hasil) and not hasil:
        add("OK", "tidak ada temuan")
    for level, msg in hasil:
        print(f"[{level}] {msg}")
    sys.exit(1 if any(l == "GAGAL" for l, _ in hasil) else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
