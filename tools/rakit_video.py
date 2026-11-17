#!/usr/bin/env python3
"""Rakit video final: INTRO + isi + OUTRO (wajib untuk semua video Pulang ngantor).

python tools/rakit_video.py --body out/isi.mp4 --out out/video.mp4 [--xfade 0.4]

Semua bagian dinormalkan ke 1920x1080, 24 fps, AAC 48 kHz stereo, lalu digabung.
Isi (tanpa intro/outro) harus >= config.yaml video.min_isi_detik (default 360).
Intro/outro: assets/INTRO_PULANG_NGANTOR_1080p.mp4 dan assets/OUTRO_PULANG_NGANTOR_1080p.mp4.
"""
import argparse
import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml"), encoding="utf-8"))
V = cfg.get("video", {})


def durasi(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path])
    return float(json.loads(out)["format"]["duration"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--body", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--intro", default=os.path.join(ROOT, V.get("intro", "assets/INTRO_PULANG_NGANTOR_1080p.mp4")))
    ap.add_argument("--outro", default=os.path.join(ROOT, V.get("outro", "assets/OUTRO_PULANG_NGANTOR_1080p.mp4")))
    ap.add_argument("--xfade", type=float, default=0.0, help="detik crossfade (0 = potong langsung)")
    ap.add_argument("--allow-short", action="store_true", help="hanya untuk uji teknis; jangan dipakai untuk video rilis")
    a = ap.parse_args()

    for p in (a.body, a.intro, a.outro):
        if not os.path.exists(p):
            sys.exit(f"GAGAL: berkas tidak ada: {p}")
    d_body, d_in, d_out = durasi(a.body), durasi(a.intro), durasi(a.outro)
    minimal = V.get("min_isi_detik", 360)
    if d_body < minimal and not a.allow_short:
        sys.exit(f"GAGAL: isi video {d_body:.0f} dtk < minimal {minimal} dtk (6 menit). Tambah materi, jangan mengulur.")

    norm = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p"
    anorm = "aformat=sample_rates=48000:channel_layouts=stereo"
    x = a.xfade
    if x > 0:
        fc = (f"[0:v]{norm}[v0];[1:v]{norm}[v1];[2:v]{norm}[v2];"
              f"[0:a]{anorm}[a0];[1:a]{anorm}[a1];[2:a]{anorm}[a2];"
              f"[v0][v1]xfade=transition=fade:duration={x}:offset={d_in - x:.3f}[vx];"
              f"[vx][v2]xfade=transition=fade:duration={x}:offset={d_in + d_body - 2 * x:.3f}[v];"
              f"[a0][a1]acrossfade=d={x}[ax];[ax][a2]acrossfade=d={x}[a]")
    else:
        fc = (f"[0:v]{norm}[v0];[1:v]{norm}[v1];[2:v]{norm}[v2];"
              f"[0:a]{anorm}[a0];[1:a]{anorm}[a1];[2:a]{anorm}[a2];"
              f"[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-y", "-i", a.intro, "-i", a.body, "-i", a.outro, "-filter_complex", fc,
           "-map", "[v]", "-map", "[a]", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
    subprocess.check_call(cmd)
    total = durasi(a.out)
    print(f"OK {a.out}: intro {d_in:.1f}s + isi {d_body:.1f}s + outro {d_out:.1f}s = {total:.1f}s")
    print(json.dumps({"durasi_detik": round(total), "isi_detik": round(d_body)}))


if __name__ == "__main__":
    main()
