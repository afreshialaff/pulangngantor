import json,re,subprocess
from vo import VO
A=json.load(open('align.json'))
FPS=24;X=14   # frame crossfade
LEAD=12       # frame sebelum suara mulai dalam tiap adegan
U='/mnt/user-data/uploads/'
def clip(s):
    if s in('S23','S26'): return U+f'RAMAYANA PART 2/VID/{s}_RAMA2_fix.mp4'
    if s=='S14': return U+'Downloads/S14_RAMA2_v2.mp4'
    return U+f'Downloads/{s}_RAMA2.mp4'
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
MOOD=dict(zip([v[0] for v in VO],
 [0,1,0,0,0, 0,0,1,0,0, 0,1,1,1,0, 1,1,0,2,2, 3,2,3,1,0, 0,0,2,1,2, 3,0,2,2,0, 0,0,0,0,0, 0,0,1]))
sc=[];t=0
for k,(sid,bag,kl,text) in enumerate(VO):
    a=A[sid];s0,s1=a['speech'];sp=s1-s0
    C=dur(clip(sid));last=k==len(VO)-1
    need=sp+LEAD/FPS+0.35          # minimum sebelum transisi berikutnya
    maxi=sp+1.6
    slot=min(max(C-X/FPS,need),maxi)
    if last: slot=sp+LEAD/FPS+1.8
    sf=int(round(slot*FPS));L=sf+(0 if last else X)
    stretch=max(1.0,L/FPS/(C-0.02))
    if stretch>1.35: raise SystemExit(f'{sid} stretch {stretch}')
    sc.append(dict(id=sid,bagian=bag,text=text,mood=MOOD[sid],clip=clip(sid),clipdur=C,sf=sf,L=L,stretch=round(stretch,4),
      f0=t,t0=t/FPS,slot=sf/FPS,vo_at=t/FPS+LEAD/FPS,vo_start=s0,vo_end=s1))
    t+=sf
bag=[s['bagian'] for s in sc]
for i,s in enumerate(sc):
    s['trans']=None if i==len(sc)-1 else (['fadeblack',X/FPS] if bag[i]!=bag[i+1] else ['fade',X/FPS])
json.dump(dict(scenes=sc,body=t/FPS,frames=t,X=X),open('timeline.json','w'),ensure_ascii=False,indent=1)
print('body',t/FPS,'max stretch',max(s['stretch'] for s in sc))
print(' '.join(f"{s['id']}:{s['stretch']:.2f}/{s['L']/FPS-s['clipdur']:+.1f}" for s in sc))
