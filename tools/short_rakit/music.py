"""Backsound orisinal (disusun lewat MIDI, dirender FluidSynth + FluidR3 GM)."""
import pretty_midi as pm, subprocess, random

W = '/tmp/claude-0/-home-claude/14405b17-3b3d-5944-b753-5a30887fc6d7/scratchpad'
random.seed(7)
mid = pm.PrettyMIDI(initial_tempo=96)
BEAT = 60 / 96


def inst(program, vol, pan=64, drum=False):
    i = pm.Instrument(program=program, is_drum=drum)
    i.control_changes += [pm.ControlChange(7, vol, 0), pm.ControlChange(10, pan, 0), pm.ControlChange(91, 70, 0)]
    mid.instruments.append(i)
    return i


pad = inst(89, 62)          # warm pad
strg = inst(48, 55, 54)     # strings
trem = inst(44, 50, 74)     # tremolo strings
pizz = inst(45, 80, 56)     # pizzicato
mar = inst(12, 58, 82)      # marimba
cel = inst(8, 55, 45)       # celesta
box = inst(10, 50, 70)      # music box
bass = inst(32, 68)         # acoustic bass
kal = inst(108, 62, 60)     # kalimba
gtr = inst(24, 56, 50)      # nylon guitar
glk = inst(9, 40, 80)       # glockenspiel
timp = inst(47, 60)         # timpani
drm = inst(0, 55, drum=True)


def note(i, p, t, d, v=70):
    i.notes.append(pm.Note(int(max(1, min(127, v + random.randint(-4, 4)))), p, max(0, t), t + d))


def chord(i, ps, t, d, v=55):
    for p in ps:
        note(i, p, t, d, v)


def bars(a, b, prog, beats=4):
    t, k = a, 0
    while t < b - 0.05:
        d = min(beats * BEAT, b - t)
        yield t, d, prog[k % len(prog)], k
        t += d
        k += 1


Dm = (38, [62, 65, 69]); Bb = (34, [58, 62, 65]); Gm = (31, [55, 58, 62]); A = (33, [57, 61, 64])
F = (41, [60, 65, 69]); C = (36, [60, 64, 67])

# 1) 0-9 misteri tengah malam
chord(pad, [50, 57, 62], 0, 9.0, 50)
chord(trem, [62, 65], 0.1, 4.0, 40)
chord(trem, [61, 64], 4.1, 4.6, 46)
for t, p in [(0.1, 86), (0.75, 81), (1.4, 77), (2.3, 82), (4.1, 86), (4.75, 81), (5.4, 76), (6.4, 73), (7.7, 74)]:
    note(cel, p, t, 0.9, 62)
note(timp, 38, 0.05, 1.5, 75)
for k in range(8):
    note(bass, 38, 3.9 + k * BEAT, 0.25, 52 + k * 3)

# 2) 9-67 rasa ingin tahu: pizzicato + marimba ringan
for t, d, (r, ch), k in bars(9.0, 67.0, [Dm, Bb, Gm, A]):
    chord(pad, ch, t, d, 38)
    for j, p in enumerate([r + 12, r + 19, r + 12, r + 17]):
        if j * BEAT < d - 0.1:
            note(pizz, p, t + j * BEAT, 0.3, 66 if j == 0 else 52)
    pat = [0, 2, 1, 2, 0, 2, 1, 2]
    if k % 4 != 3:
        for j in range(8):
            if j * BEAT / 2 < d - 0.1 and j not in (3, 7):
                note(mar, ch[pat[j]] + 12, t + j * BEAT / 2, 0.22, 46)
    else:
        for j, p in enumerate([ch[2] + 12, ch[1] + 12, ch[0] + 12]):
            note(cel, p, t + (1 + j) * BEAT, 0.6, 50)
    note(bass, r, t, min(d, 1.2), 55)
    if t >= 29:
        for j in range(4):
            if j * BEAT < d - 0.1:
                note(drm, 42, t + j * BEAT + BEAT / 2, 0.1, 28)
note(timp, 45, 38.0, 1.0, 62)
for k in range(10):  # detak cepat saat jantung "lari maraton" (S05)
    note(drm, 36, 42.0 + k * 0.3, 0.1, 58)

# 3) 67-85 hutan: kalimba + perkusi kayu
for t, d, (r, ch), k in bars(67.0, 85.0, [Dm, C, Bb, C]):
    chord(strg, ch, t, d, 38)
    note(bass, r, t, 0.5, 65)
    note(bass, r + 7, t + 2.5 * BEAT, 0.4, 55)
    for j, s in enumerate([0, 1, 2, 1, 0, 2]):
        o = [0, 0.75, 1.5, 2, 2.75, 3.25][j] * BEAT
        if o < d - 0.1:
            note(kal, ch[s] + 12, t + o, 0.4, 58)
    for j in range(8):
        if j * BEAT / 2 < d - 0.05:
            note(drm, [64, 70, 63, 70, 64, 76, 63, 70][j], t + j * BEAT / 2, 0.1, 40 if j % 2 == 0 else 26)

# 4) 85-115 malam: cermin, ketindihan, sosok di belakang
for t, d, (r, ch), k in bars(85.0, 115.0, [Dm, Gm, Bb, A], beats=8):
    chord(pad, [r + 12] + ch, t, d, 46)
    chord(trem, [ch[1] + 12], t + d / 2, d / 2, 30)
    for j, s in enumerate([2, 1, 0, 1, 2, 0]):
        o = (j * 1.25 + 0.25) * BEAT
        if o < d - 0.2:
            note(box, ch[s] + 12, t + o, 1.0, 50)
t = 96.2
while t < 105.5:  # detak jantung pelan
    note(drm, 36, t, 0.12, 52)
    note(drm, 36, t + 0.28, 0.12, 38)
    t += 1.25
note(timp, 38, 106.0, 1.5, 55)
chord(trem, [61, 64], 112.3, 2.6, 45)

# 5) 115-132 lega dan ceria (F mayor)
for t, d, (r, ch), k in bars(115.0, 129.5, [F, C, Bb, C]):
    chord(pad, ch, t, d, 36)
    note(bass, r, t, 0.6, 64)
    note(bass, r + 7, t + 2 * BEAT, 0.5, 54)
    for j, s in enumerate([0, 1, 2, 1, 0, 1, 2, 1]):
        if j * BEAT / 2 < d - 0.05:
            note(gtr, ch[s], t + j * BEAT / 2, 0.35, 56)
    note(glk, ch[2] + 12, t + 2 * BEAT, 0.8, 48)
    if d > 2 * BEAT:
        note(drm, 70, t + BEAT, 0.1, 30)
        note(drm, 70, t + 3 * BEAT, 0.1, 30) if d > 3 * BEAT else None
chord(pad, [53, 60, 65, 69], 129.5, 2.4, 45)
chord(gtr, [53, 60, 65, 69], 129.5, 2.4, 60)
for j, p in enumerate([77, 81, 84, 89]):
    note(glk, p, 130.0 + j * 0.22, 1.2, 52)

mid.write(f'{W}/music.mid')
subprocess.run(['fluidsynth', '-ni', '-g', '0.7', '-r', '48000', '-F', f'{W}/music_raw.wav',
                '/usr/share/sounds/sf2/FluidR3_GM.sf2', f'{W}/music.mid'], check=True, capture_output=True)
