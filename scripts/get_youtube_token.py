#!/usr/bin/env python3
"""Jalankan SEKALI di laptop untuk mendapatkan YT_REFRESH_TOKEN.

1. Unduh OAuth client (Desktop app) dari Google Cloud Console -> simpan sebagai
   scripts/client_secret.json (sudah di .gitignore, jangan diupload).
2. pip install google-auth-oauthlib google-api-python-client
3. python scripts/get_youtube_token.py
4. Browser terbuka -> login dengan akun Google yang MEMEGANG channel "Pulang ngantor"
   (di layar pilih akun/brand account, pilih channel Pulang ngantor, BUKAN channel lama).
5. Salin nilai yang dicetak ke GitHub Secrets. Jangan bagikan ke siapa pun, termasuk ke chat.
"""
import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
here = os.path.dirname(os.path.abspath(__file__))
path = next(p for p in (os.path.join(here, "client_secret.json"), "client_secret.json") if os.path.exists(p))

flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
info = json.load(open(path))
info = info.get("installed") or info.get("web")

yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
ch = yt.channels().list(part="snippet", mine=True).execute().get("items", [{}])[0]

print("\nChannel yang terhubung :", ch.get("snippet", {}).get("title"), f"({ch.get('snippet', {}).get('customUrl', '-')})")
print("Pastikan itu 'Pulang ngantor'. Kalau bukan, JANGAN dipakai; ulangi dan pilih channel yang benar.\n")
print("=== Salin ke GitHub -> Settings -> Secrets and variables -> Actions ===")
print("YT_CLIENT_ID            =", info["client_id"])
print("YT_CLIENT_SECRET        =", info["client_secret"])
print("YT_REFRESH_TOKEN        =", creds.refresh_token)
print("YT_EXPECTED_CHANNEL_ID  =", ch.get("id"))
