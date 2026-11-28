"""Rakit Short: hapus watermark, perbaiki S02, transisi halus, subtitle terbakar, audio mix."""
import json, re, subprocess, numpy as np, cv2, sys
W = '/tmp/claude-0/-home-claude/14405b17-3b3d-5944-b753-5a30887fc6d7/scratchpad'
sys.path.insert(0, W)
import dewm

O = '/mnt/user-data/outputs'
OUT = f'{O}/pareidolia_pulang_ngantor.mp4'
FPS, WD, HT = 24, 1080, 1920
DUR = [9, 11, 9, 9, 7, 13, 9, 10, 8, 11, 10, 9, 9, 8]
FILES = [f'{O}/S{i:02d}.mp4' for i in range(1, 15)]
FILES[0] = '/mnt/user-data/uploads/Downloads/PAREIDOLIA-HANTU/VIDEO/S01.mp4'
FILES[11] = f'{O}/S12_v2.mp4'
SECTION = {7, 9, 12}  # pergantian bagian (awal S08, S10, S13): zoom-dissolve lebih panjang


def read(path, vf=''):
    chain = (vf + ',' if vf else '') + 'scale=in_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,format=bgr24'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', chain, '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(WD * HT * 3)
        if len(b) < WD * HT * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(HT, WD, 3).copy()
    assert p.wait() == 0


def load(i):
    n = DUR[i] * FPS
    if i == 1:  # S02: ghosting mulai ~8,5 dtk -> pakai 8,4 dtk, perlambat ke 11 dtk dengan interpolasi gerak
        tmp = f'{W}/s02_clean.mkv'
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{WD}x{HT}', '-r', str(FPS),
                                '-i', '-', '-c:v', 'ffv1', '-pix_fmt', 'bgr0', tmp], stdin=subprocess.PIPE)
        for k, f in enumerate(read(FILES[i])):
            if k < int(8.4 * FPS):
                enc.stdin.write(dewm.clean(f).tobytes())
        enc.stdin.close()
        assert enc.wait() == 0
        slow = f'{W}/s02_slow.mkv'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-vf',
                        f'setpts=PTS*{11 / 8.4:.6f},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,'
                        'tpad=stop_mode=clone:stop_duration=1,format=bgr0', '-c:v', 'ffv1', slow], check=True)
        fr = list(read(slow))[:n]
    else:
        fr = [dewm.clean(f) for f in read(FILES[i])][:n]
    assert len(fr) >= n - 1, (i + 1, len(fr), n)
    while len(fr) < n:
        fr.append(fr[-1])
    return fr


def zoom(f, s):
    if s <= 1.0005:
        return f
    M = cv2.getRotationMatrix2D((WD / 2, HT / 2), 0, s)
    return cv2.warpAffine(f, M, (WD, HT), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def ass_time(t):
    c = int(round(t * 100))
    return f'{c // 360000}:{c // 6000 % 60:02d}:{c // 100 % 60:02d}.{c % 100:02d}'


def srt_time(t):
    m = int(round(t * 1000))
    return f'{m // 3600000:02d}:{m // 60000 % 60:02d}:{m // 1000 % 60:02d},{m % 1000:03d}'


cues = json.load(open(f'{W}/cues.json'))
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Poppins,116,&H00C5D9E9,&H000000FF,&H00241410,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,90,90,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(f'{W}/subs.ass', 'w') as a, open(f'{O}/subtitle_pareidolia.srt', 'w') as s:
    a.write(head)
    for k, c in enumerate(cues, 1):
        rich = re.sub(r'\*(.+?)\*', r'{\\c&H59A2F4&}\1{\\c&HC5D9E9&}', c['t'])
        a.write(f"Dialogue: 0,{ass_time(c['a'])},{ass_time(c['b'])},Sub,,0,0,0,,{{\\fad(60,40)}}{rich}\n")
        s.write(f"{k}\n{srt_time(c['a'])} --> {srt_time(c['b'])}\n{c['t'].replace('*', '')}\n\n")

total = sum(DUR) * FPS
enc = subprocess.Popen(
    ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-',
     '-i', f'{W}/mix.wav', '-vf', f'ass={W}/subs.ass,scale=out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p',
     '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-tune', 'animation', '-maxrate', '10M', '-bufsize', '20M',
     '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
     '-c:a', 'aac', '-b:a', '192k', '-t', str(sum(DUR)), '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
start = np.cumsum([0] + DUR) * FPS
cache = {}


def frame(i, n):
    if i not in cache:
        cache[i] = load(i)
        print('muat S%02d' % (i + 1), flush=True)
    return cache[i][int(np.clip(n - start[i], 0, DUR[i] * FPS - 1))]


i = 0
for n in range(total):
    while n >= start[i + 1]:
        i += 1
    out = None
    for j in (i, i + 1):  # batas antara klip j-1 dan j
        if 0 < j < len(DUR):
            sec = j in SECTION
            half = 9 if sec else 6
            if start[j] - half <= n < start[j] + half:
                x = (n - (start[j] - half) + 0.5) / (2 * half)
                e = x * x * (3 - 2 * x)
                A, B = frame(j - 1, n), frame(j, n)
                if sec:
                    A, B = zoom(A, 1 + 0.09 * e), zoom(B, 1 + 0.07 * (1 - e))
                out = cv2.addWeighted(A, 1 - e, B, e, 0)
    if out is None:
        out = frame(i, n)
    for old in [k for k in cache if k < i - 1]:
        del cache[old]
    enc.stdin.write(out.tobytes())
enc.stdin.close()
assert enc.wait() == 0
print('selesai', OUT)
