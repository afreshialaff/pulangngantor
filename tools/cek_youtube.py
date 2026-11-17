#!/usr/bin/env python3
"""Uji koneksi GitHub -> YouTube (tanpa upload). Mencetak channel yang terhubung."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pipeline.youtube import guarded_service, my_channel  # noqa: E402

yt = guarded_service()
ch = my_channel(yt)
s = ch["snippet"]
print(f"OK terhubung ke: {s['title']} | id={ch['id']} | handle={s.get('customUrl', '-')}")
print(f"Subscriber: {ch['statistics'].get('subscriberCount', 'disembunyikan')} | Video: {ch['statistics'].get('videoCount')}")
