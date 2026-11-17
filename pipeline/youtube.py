"""Koneksi GitHub -> YouTube Data API v3 untuk channel Pulang ngantor.

Secret yang dibutuhkan (GitHub Actions secrets / env lokal):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Opsional tapi sangat disarankan:
  YT_EXPECTED_CHANNEL_ID  -> upload ditolak kalau token ternyata milik channel lain.
"""
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]


def service():
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        raise RuntimeError(f"Secret YouTube belum lengkap: {', '.join(missing)} (lihat README langkah 3-5).")
    creds = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def my_channel(yt):
    """Channel yang dimiliki token ini."""
    items = yt.channels().list(part="snippet,statistics", mine=True).execute().get("items", [])
    if not items:
        raise RuntimeError("Token ini tidak punya channel YouTube.")
    return items[0]


def guarded_service():
    """service() + pengaman: pastikan token milik channel Pulang ngantor, bukan channel lain."""
    yt = service()
    expected = os.environ.get("YT_EXPECTED_CHANNEL_ID", "").strip()
    ch = my_channel(yt)
    if expected and ch["id"] != expected:
        raise RuntimeError(
            f"Token milik channel '{ch['snippet']['title']}' ({ch['id']}), "
            f"bukan channel yang diharapkan ({expected}). Upload dibatalkan."
        )
    if not expected:
        print(f"PERINGATAN: YT_EXPECTED_CHANNEL_ID belum diisi. Upload akan ke '{ch['snippet']['title']}' ({ch['id']}).")
    return yt
