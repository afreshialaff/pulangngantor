#!/usr/bin/env python3
"""Ganti thumbnail video yang sudah diunggah (video_id dari upload.json), tanpa mengunggah ulang video.

python tools/ganti_thumbnail.py data/produksi/<folder> [--thumb path.jpg]
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from googleapiclient.http import MediaFileUpload  # noqa: E402
from pipeline.youtube import guarded_service  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--thumb", default=None)
    a = ap.parse_args()
    up = os.path.join(a.folder, "upload.json")
    out = json.load(open(up))
    thumb = a.thumb or os.path.join(a.folder, "thumbnail.jpg")
    yt = guarded_service()
    yt.thumbnails().set(videoId=out["video_id"], media_body=MediaFileUpload(thumb)).execute()
    out["thumbnail"] = True
    out["thumbnail_diganti"] = dt.datetime.now(dt.timezone.utc).isoformat()
    json.dump(out, open(up, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
