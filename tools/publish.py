#!/usr/bin/env python3
"""Ubah video yang sudah diunggah (upload.json) menjadi public tanpa mengunggah ulang.

python tools/publish.py data/produksi/<tgl> [--privacy public|unlisted|private]
Memakai pengaman channel (YT_EXPECTED_CHANNEL_ID) dan mencoba ulang playlist bila sebelumnya gagal.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.youtube import guarded_service  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    a = ap.parse_args()
    up = os.path.join(a.folder, "upload.json")
    out = json.load(open(up))
    vid = out["video_id"]
    yt = guarded_service()
    v = yt.videos().list(part="status", id=vid).execute()["items"][0]
    st = v["status"]
    st["privacyStatus"] = a.privacy
    r = yt.videos().update(part="status", body={"id": vid, "status": st}).execute()
    out["status"] = r["status"]["privacyStatus"]
    out["dipublikasikan"] = out["status"] == "public"
    pid = out.get("playlist")
    if not pid and out.get("playlist_error"):
        meta = json.load(open(os.path.join(a.folder, "metadata.json")))
        pl = (meta.get("playlist") or {}).get("judul")
        try:
            req = yt.playlists().list(part="snippet", mine=True, maxResults=50)
            while req is not None and not pid:
                rr = req.execute()
                for it in rr.get("items", []):
                    if it["snippet"]["title"].strip().lower() == (pl or "").strip().lower():
                        pid = it["id"]
                        break
                req = yt.playlists().list_next(req, rr)
            if pid:
                yt.playlistItems().insert(part="snippet", body={"snippet": {
                    "playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
                out["playlist"] = pid
                out.pop("playlist_error", None)
        except Exception as e:
            out["playlist_error"] = str(e)[:200]
    json.dump(out, open(up, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
