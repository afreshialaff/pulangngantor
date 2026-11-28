"""Selaraskan potongan subtitle dengan VO final: espeak-ng + DTW per scene, lalu tempel ke jeda."""
import json, re, subprocess, numpy as np, librosa

W = '/tmp/claude-0/-home-claude/14405b17-3b3d-5944-b753-5a30887fc6d7/scratchpad'
PROD = '/home/claude/pulangngantor/data/produksi/2026-11-27-pareidolia-hantu'
VO = '/mnt/user-data/outputs/VO_pareidolia_pas_klip.wav'
SR = 16000

# *kata* = disorot amber; {tampil=ucapan} untuk angka
TEXT = [
 "Jam dua belas malam.|Ada *sosok putih* melambai|di pojok kamar!|Jantungmu langsung joget.|Itu *hantu*...|atau cuma *jemuran*?",
 "Tenang, otakmu nggak rusak.|Namanya *pareidolia*:|melihat *wajah*|di benda acak.|Stopkontak kaget,|mobil senyum, awan melotot.",
 "Di otakmu ada area|yang sibuk banget ngurusin *wajah*.|Namanya *fusiform face area*.|Anggap aja *satpam*|khusus pengecek muka.",
 "Studi tahun {2020=dua ribu dua puluh}|merekam otak orang.|Sekitar *seperlima detik* pertama,|benda mirip wajah|diproses mirip *wajah beneran*.",
 "Sekejap kemudian, otak *meralat*:|eh, ternyata cuma benda!|Masalahnya, *jantungmu*|keburu lari maraton.",
 "Di eksperimen lain,|orang diminta mencari *wajah*|di gambar bintik acak.|Katanya, separuhnya berisi wajah.|Padahal *kosong semua*!|Tapi di sekitar|{*34 persen*=tiga puluh empat persen} percobaan,|mereka bilang: *ada*!",
 "Jadi *harapan*|ikut menyetir matamu.|Kalau sudah mikir,|rumah ini *angker*,|bayangan biasa gampang|naik pangkat jadi *penampakan*.",
 "Kenapa begitu?|Dugaan ilmuwan,|salah alarm itu *lebih murah*.|Mengira semak itu *harimau*|cuma bikin malu.|Kalau kebalik, bisa gawat.",
 "Dan bukan cuma manusia.|*Monyet rhesus* juga|menatap lebih lama|benda yang mirip wajah.|Radar muka ini|sepertinya *warisan lama*.",
 "*Cahaya redup*|bikin makin seru.|Menatap *cermin* lama-lama,|sebagian orang melihat|*wajah asing*.|Satu tinjauan mencatat|{*58 persen*=lima puluh delapan persen},|walau mutu studinya beragam.",
 "Terus, *ketindihan*!|Badan terkunci,|pikiran setengah bangun,|kadang muncul *sosok*.|Di populasi umum,|sekitar {*8 dari 100* orang=delapan dari seratus orang}|pernah *lumpuh tidur*.",
 "Rasa *diikuti* dari belakang|pun pernah dibuat di lab.|*Robot* menyentuh punggung peserta|dengan jeda singkat.|Sebagian merasa|ada *sosok tak terlihat*!",
 "Jadi kalau lihat sosok:|*nyalakan lampu*,|geser sudut pandang,|lalu *cukup tidur*.|Kalau sering dan bikin tersiksa,|ngobrol ke *dokter*, ya.",
 "Rasanya bisa sangat nyata,|tapi belum tentu ada *tamunya*.|Benda apa di kamarmu|yang paling mirip *wajah*?|Tulis di *komentar*!",
]


def forms(c):
    show = re.sub(r'\{(.*?)=(.*?)\}', r'\1', c)
    say = re.sub(r'\{(.*?)=(.*?)\}', r'\2', c).replace('*', '')
    return show, say


def feat(y):
    m = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20, n_fft=512, hop_length=160)[1:]
    d = librosa.feature.delta(m)
    f = np.vstack([m, d])
    return (f - f.mean(1, keepdims=True)) / (f.std(1, keepdims=True) + 1e-6)


def tts(s):
    subprocess.run(['espeak-ng', '-v', 'id', '-s', '165', '-w', f'{W}/e.wav', s], check=True)
    y, _ = librosa.load(f'{W}/e.wav', sr=SR)
    return librosa.effects.trim(y, top_db=35)[0]


vo, _ = librosa.load(VO, sr=SR)
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', VO, '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
sil = list(zip(map(float, re.findall(r'silence_start: ([\d.]+)', log)),
               map(float, re.findall(r'silence_end: ([\d.]+)', log))))
scenes = json.load(open(PROD + '/cuts_klip.json'))['scene']
naskah = json.load(open(PROD + '/naskah.json'))['bagian']
cues = []
for i, sc in enumerate(scenes):
    chunks = TEXT[i].split('|')
    norm = lambda s: re.sub(r'[^a-z]+', '', s.lower())
    assert norm(' '.join(forms(c)[1] for c in chunks)) == norm(naskah[i]['vo']), (i + 1, 'teks beda dari naskah')
    # batas ucapan dalam scene
    a, b = sc['mulai'], sc['selesai']
    y = vo[int(a * SR):int(b * SR)]
    _, (s0, s1) = librosa.effects.trim(y, top_db=35)
    on, off = a + s0 / SR, a + s1 / SR
    y = y[s0:s1]
    parts, marks, n = [], [], 0
    for c in chunks:
        e = tts(forms(c)[1])
        marks.append(n)
        gap = np.zeros(int(0.12 * SR), np.float32)
        parts += [e, gap]
        n += len(e) + len(gap)
    ref = np.concatenate(parts)
    _, wp = librosa.sequence.dtw(feat(ref), feat(y), metric='cosine')
    wp = wp[::-1]
    starts = [on]
    for m in marks[1:]:
        j = wp[wp[:, 0] >= m // 160][0, 1]
        t = on + j * 0.01
        # tempel ke akhir jeda terdekat bila ada
        near = [(abs(e - t) if not (s <= t <= e) else 0, e, e - s) for s, e in sil if on < e < off]
        near = [x for x in near if x[0] <= 0.45]
        if near:
            best = min(near, key=lambda x: x[0] - 0.5 * x[2])
            t = best[1]
        starts.append(max(t, starts[-1] + 0.45))
    for k, c in enumerate(chunks):
        st = starts[k] - 0.05 if k else starts[k]
        en = starts[k + 1] - 0.05 if k + 1 < len(chunks) else min(off + 0.2, b - 0.02)
        snapped = any(abs(e - starts[k]) < 0.02 for s, e in sil)
        cues.append({'scene': i + 1, 'a': round(max(st, a), 3), 'b': round(en, 3), 't': forms(c)[0], 'jeda': snapped or k == 0})
json.dump(cues, open(f'{W}/cues.json', 'w'), ensure_ascii=False, indent=0)
for c in cues:
    print(c['scene'], f"{c['a']:7.2f} {c['b']:7.2f} {c['b']-c['a']:5.2f} {'|' if c['jeda'] else '?'} {c['t']}")
print(len(cues), 'cue;', sum(c['jeda'] for c in cues), 'menempel pada jeda')
