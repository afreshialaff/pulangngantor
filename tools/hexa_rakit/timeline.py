import json
S=json.load(open('sent.json'))
sb=json.load(open('/home/claude/pulangngantor/data/produksi/2026-11-17/storyboard.json'))['scenes']
CLIP=15.04; LEAD=0.45; TAIL=0.55
bag=[s['bagian'] for s in sb]
def trans(i):  # transition from scene i to i+1 (0-based)
    if bag[i]!=bag[i+1]: return ('fadeblack',0.8)
    if bag[i]=='Kronologi': return ('smoothleft',0.5)
    if i+1 in (3,14,24): return ('zoomin',0.6)
    return ('dissolve',0.6)
sc=[]
for k in range(26):
    ss=[x for x in S if x['para']==k]
    sc.append(dict(id=f'S{k+1:02d}',vo_start=ss[0]['start'],vo_end=ss[-1]['end'],sents=ss,bagian=bag[k],label=sb[k]['on_screen']))
t=0.0
for k,s in enumerate(sc):
    v=s['vo_end']-s['vo_start']; s['vo_dur']=round(v,3)
    X=trans(k)[1] if k<25 else 0.0
    s['trans']=trans(k) if k<25 else None
    # visible slot (time from this segment start to next segment start)
    slot=v+LEAD+TAIL
    L=slot+X
    f=L/CLIP
    if f<0.88: f=0.88; L=CLIP*f; slot=L-X
    if f>1.22: print('WARN stretch',s['id'],f)
    s.update(slot=round(slot,3),seg_len=round(L,3),stretch=round(f,4),t0=round(t,3),vo_at=round(t+LEAD,3))
    t+=slot
body=t
print('body',round(body,2))
for s in sc: print(s['id'],s['vo_dur'],s['slot'],s['seg_len'],s['stretch'],s['trans'])
json.dump(dict(scenes=sc,body=body,LEAD=LEAD),open('timeline.json','w'),ensure_ascii=False,indent=1)
