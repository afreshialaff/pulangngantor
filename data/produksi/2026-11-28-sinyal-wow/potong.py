#!/usr/bin/env python3
"""Cari batas scene dari jeda VO. Pakai: python potong.py VO.wav  -> cuts.json"""
import json, re, subprocess, sys
wav = sys.argv[1]
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",wav]))
log = subprocess.run(["ffmpeg","-i",wav,"-af","silencedetect=noise=-35dB:d=0.2","-f","null","-"],capture_output=True,text=True).stderr
a = [float(x) for x in re.findall(r"silence_start: ([\d.]+)",log)]
b = [float(x) for x in re.findall(r"silence_end: ([\d.]+)",log)]
sil = [((s+e)/2, e-s) for s,e in zip(a,b) if s>0.3 and e<dur-0.3]
teks = open("vo_satu_take.txt",encoding="utf-8").read().strip().split("\n\n")
bobot = [len(re.findall(r"[aeiouAEIOU]",t)) + 2*len(re.findall(r"[.!?:]",t)) for t in teks]
target = [dur*sum(bobot[:i])/sum(bobot) for i in range(1,len(teks))]
# DP: pilih 13 jeda berurutan, dekat target dan panjang
INF = 1e18; n, m = len(sil), len(target)
best = [[(INF,None)]*n for _ in range(m)]
for i in range(m):
    for j,(t,p) in enumerate(sil):
        c = (t-target[i])**2/4 - 12*p
        if i == 0: best[i][j] = (c,None)
        elif j:
            k = min(range(j), key=lambda k: best[i-1][k][0]); best[i][j] = (best[i-1][k][0]+c, k)
j = min(range(n), key=lambda j: best[-1][j][0]); pick = []
for i in range(m-1,-1,-1):
    pick.append(sil[j]); j = best[i][j][1]
pick.reverse()
cuts = [0.0] + [round(t,2) for t,_ in pick] + [round(dur,2)]
for i,(t,p) in enumerate(pick): print(f"S{i+1:02d}|S{i+2:02d} {t:7.2f} jeda {p:.2f} target {target[i]:.1f}")
print("durasi scene", [round(y-x,2) for x,y in zip(cuts,cuts[1:])])
print("jeda terpanjang lain", sorted([(round(t,2),round(p,2)) for t,p in sil if (t,p) not in pick], key=lambda x:-x[1])[:6])
json.dump(cuts, open("cuts.json","w"))
