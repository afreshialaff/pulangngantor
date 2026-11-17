#!/usr/bin/env python3
"""Unggah video ke YouTube (default PRIVATE sesuai brand guideline: private sampai QC selesai).

python tools/upload.py --video out/video.mp4 --meta data/produksi/<tgl>/metadata.json \
    --thumb data/produksi/<tgl>/thumbnail.jpg --result data/produksi/<tgl>/upload.json

metadata.json: {"judul": "...", "deskripsi": "...", "tag": ["..."], "playlist": {"judul": "..."}}
"""
import argparse
import datetime as dt
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from googleapiclient.http import MediaFileUpload  # noqa: E402
from pipeline.youtube import guarded_service  # noqa: E402

cfg = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.yaml"), encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--thumb", default=None)
    ap.add_argument("--result", required=True)
    ap.add_argument("--privacy", default=None, choices=["public", "private", "unlisted"])
    ap.add_argument("--captions", default=None)
    a = ap.parse_args()
    privacy = a.privacy or (cfg["upload"]["mode"] if cfg["upload"]["mode"] in ("public", "private", "unlisted") else "private")
    m = json.load(open(a.meta, encoding="utf-8"))
    body = {
        "snippet": {
            "title": m["judul"][:100],
            "description": m["deskripsi"][:4900],
            "tags": m.get("tag", [])[:15],
            "categoryId": str(m.get("category_id", cfg["channel"]["category_id"])),
            "defaultLanguage": cfg["channel"]["language"],
            "defaultAudioLanguage": cfg["channel"]["language"],
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": bool(cfg["upload"]["made_for_kids"]),
            "containsSyntheticMedia": bool(cfg["upload"]["ai_disclosure"]),
            "embeddable": True,
        },
    }
    yt = guarded_service()
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(a.video, chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        prog, resp = req.next_chunk()
        if prog:
            print(f"upload {int(prog.progress() * 100)}%", flush=True)
    vid = resp["id"]
    real = yt.videos().list(part="status", id=vid).execute()["items"][0]["status"]
    out = {"video_id": vid, "url": f"https://youtu.be/{vid}", "status": real.get("privacyStatus"),
           "diminta": privacy, "diunggah": dt.datetime.now(dt.timezone.utc).isoformat(), "thumbnail": False}
    if a.thumb and os.path.exists(a.thumb):
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(a.thumb)).execute()
            out["thumbnail"] = True
        except Exception as e:  # kanal belum verifikasi HP, dsb.
            out["thumbnail_error"] = str(e)[:200]
    if a.captions and os.path.exists(a.captions):
        try:
            yt.captions().insert(part="snippet", body={"snippet": {
                "videoId": vid, "language": "id", "name": "Bahasa Indonesia", "isDraft": False}},
                media_body=MediaFileUpload(a.captions, mimetype="application/octet-stream")).execute()
            out["captions"] = True
        except Exception as e:
            out["captions"] = False
            out["captions_error"] = str(e)[:200]
    pl = (m.get("playlist") or {}).get("judul")
    if pl:
        try:
            pid, req = None, yt.playlists().list(part="snippet", mine=True, maxResults=50)
            while req is not None and pid is None:
                r = req.execute()
                for it in r.get("items", []):
                    if it["snippet"]["title"].strip().lower() == pl.strip().lower():
                        pid = it["id"]
                        break
                req = yt.playlists().list_next(req, r)
            if pid is None:
                pid = yt.playlists().insert(part="snippet,status", body={
                    "snippet": {"title": pl[:150], "defaultLanguage": "id"},
                    "status": {"privacyStatus": "public"}}).execute()["id"]
            yt.playlistItems().insert(part="snippet", body={"snippet": {
                "playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
            out["playlist"] = pid
        except Exception as e:
            out["playlist_error"] = str(e)[:200]
    os.makedirs(os.path.dirname(a.result) or ".", exist_ok=True)
    json.dump(out, open(a.result, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
