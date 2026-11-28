exec(open('align.py').read().split("norm=lambda")[0])
CUTS=[0.0,12.04,19.86,26.89,35.95,43.55,52.55,61.44,68.72,75.46,83.47,88.77,98.93,106.95,113.96]
G=json.load(open('align.json'))['g']
cues=[]; k0=0
for i in range(14):
    ch=TEXT[i].split('|'); a,b=CUTS[i],CUTS[i+1]
    y=vo[int(a*SR):int(b*SR)]
    _,(s0,s1)=librosa.effects.trim(y,top_db=35); on,off=a+s0/SR,a+s1/SR; y=y[s0:s1]
    parts,marks,n=[],[],0
    for c in ch:
        e=tts(forms(c)[1]); p=re.sub(r'[*}]','',c)[-1]
        gap=np.zeros(int((0.3 if p in '.!?:' else 0.1)*SR),np.float32)
        marks.append(n); parts+=[e,gap]; n+=len(e)+len(gap)
    ref=np.concatenate(parts)
    _,wp=librosa.sequence.dtw(feat(ref),feat(y),metric='cosine'); wp=wp[::-1]
    starts=[on]
    for k,m in enumerate(marks[1:],1):
        t=on+wp[wp[:,0]>=m//160][0,1]*0.01; loc=t; gl=G[k0+k]
        if abs(gl-t)>0.35: t=(t+gl)/2
        near=[(0 if s<=t<=e else min(abs(e-t),abs(s-t)),e,e-s) for s,e in sil if on<e<off]
        near=[x for x in near if x[0]<=0.4 and x[1]>starts[-1]+0.3]
        if near: t=min(near,key=lambda x:x[0]-0.6*x[2])[1]
        starts.append(max(t,starts[-1]+0.45))
        print(f'   S{i+1:02d} lokal {loc:7.2f} global {gl:7.2f} pakai {starts[-1]:7.2f}  {forms(ch[k])[0]}')
    for k,c in enumerate(ch):
        snapped=any(abs(e-starts[k])<0.02 for s,e in sil) or k==0
        cues.append({'scene':i+1,'on':starts[k],'t':forms(c)[0],'jeda':snapped,'off':off,'b':b})
    k0+=len(ch)
json.dump(cues,open('cues_raw.json','w'),ensure_ascii=False)
print(len(cues),'cue;',sum(c['jeda'] for c in cues),'menempel pada jeda')
