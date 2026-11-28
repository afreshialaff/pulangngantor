"""Paskan VO ke durasi klip: potong di jeda antar scene, tambah hening (tanpa ubah tempo)."""
import json, subprocess, wave

SRC = '/mnt/user-data/uploads/Downloads/PAREIDOLIA-HANTU/VIDEO/VO_pareidolia.wav'
OUT = '/mnt/user-data/outputs/VO_pareidolia_pas_klip.wav'
PROD = '/home/claude/pulangngantor/data/produksi/2026-11-27-pareidolia-hantu'
RAW = '/tmp/claude-0/-home-claude/14405b17-3b3d-5944-b753-5a30887fc6d7/scratchpad/vo_fit_raw.wav'
CLIPS = [9, 11, 9, 9, 7, 13, 9, 10, 8, 11, 10, 9, 9, 8]

cuts = json.load(open(PROD + '/cuts.json'))
w = wave.open(SRC)
rate, params = w.getframerate(), w.getparams()
assert params.nchannels == 1 and params.sampwidth == 2
data = w.readframes(w.getnframes())
total = len(data) // 2
fade = int(0.005 * rate)
out, rows, start = bytearray(), [], 0.0
for i, clip in enumerate(CLIPS):
    a = round(cuts[i] * rate)
    b = total if i == len(CLIPS) - 1 else round(cuts[i + 1] * rate)
    seg = memoryview(bytearray(data[a * 2:b * 2])).cast('h')
    for k in range(fade):
        if i:
            seg[k] = int(seg[k] * k / fade)
        seg[-1 - k] = int(seg[-1 - k] * k / fade)
    extra = clip * rate - len(seg)
    assert extra >= 0, f'S{i+1:02d}: VO lebih panjang dari klip'
    lead = 0 if i == 0 else min(int(extra * 0.4), int(0.3 * rate))
    out += bytes(lead * 2) + seg.tobytes() + bytes((extra - lead) * 2)
    rows.append({'scene': f'S{i+1:02d}', 'mulai': start, 'selesai': start + clip,
                 'vo_asli_dtk': round(len(seg) / rate, 2),
                 'hening_awal': round(lead / rate, 2),
                 'hening_akhir': round((extra - lead) / rate, 2)})
    start += clip
r = wave.open(RAW, 'wb')
r.setparams(params)
r.writeframes(bytes(out))
r.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', RAW, '-af',
                'aresample=192000,volume=2.5dB,alimiter=limit=0.794:level=false:attack=5:release=50,aresample=48000',
                '-c:a', 'pcm_s16le', OUT], check=True)
json.dump({'catatan': 'Timing final: VO dipaskan ke durasi klip (permintaan pemilik 28 Nov). cuts.json = VO asli.',
           'vo': 'VIDEO/VO_pareidolia_pas_klip.wav', 'durasi_detik': start, 'scene': rows},
          open(PROD + '/cuts_klip.json', 'w'), ensure_ascii=False, indent=1)
for x in rows:
    print(x)
print('total', start)
