#!/usr/bin/env python3
"""QC awal klip Short (tahap 4): kelengkapan, resolusi, fps, durasi vs slot VO, lembar kontak.

python tools/qc_klip.py data/produksi/<tgl> --klip <folder S01.mp4..> [--sheet <folder>]

Slot VO dibaca dari <folder produksi>/cuts.json (daftar batas detik). Lembar kontak tetap
harus dilihat mata: morphing, dissolve, atau wajah berubah tidak terdeteksi otomatis.
"""
import argparse
import json
import os
import subprocess
import sys


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate:format=duration", "-of", "json", path])
    d = json.loads(out)
    s = d["streams"][0]
    return s["width"], s["height"], s["r_frame_rate"], float(d["format"]["duration"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("produksi")
    ap.add_argument("--klip", required=True)
    ap.add_argument("--sheet", help="folder keluaran lembar kontak (4 frame per detik)")
    a = ap.parse_args()
    cuts = json.load(open(os.path.join(a.produksi, "cuts.json"), encoding="utf-8"))
    if a.sheet:
        os.makedirs(a.sheet, exist_ok=True)
    kurang, masalah = [], 0
    for i, (mulai, selesai) in enumerate(zip(cuts, cuts[1:]), 1):
        nama, slot = f"S{i:02d}", selesai - mulai
        path = os.path.join(a.klip, nama + ".mp4")
        if not os.path.exists(path):
            kurang.append(nama)
            continue
        w, h, fps, dur = probe(path)
        sebab = []
        if (w, h) != (1080, 1920):
            sebab.append(f"resolusi {w}x{h}")
        if fps != "24/1":
            sebab.append(f"fps {fps}")
        if dur + 0.001 < slot:
            sebab.append("lebih pendek dari slot VO")
        masalah += bool(sebab)
        print(f"{nama}: {dur:.2f} dtk / slot {slot:.2f} dtk, {w}x{h} {fps} -> {'; '.join(sebab) or 'OK teknis'}")
        if a.sheet:
            baris = int(dur * 4 // 8) + 1
            subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf",
                                   f"fps=4,scale=270:-1,tile=8x{baris}", "-frames:v", "1",
                                   os.path.join(a.sheet, nama + ".jpg")])
    print(f"Ada {len(cuts) - 1 - len(kurang)}/{len(cuts) - 1} klip; belum ada: {', '.join(kurang) or '-'}")
    sys.exit(1 if kurang or masalah else 0)


if __name__ == "__main__":
    main()
