import json, re, subprocess, numpy as np, librosa
from chunks import TEXT
W='.'; PROD='/home/claude/pulangngantor/data/produksi/2026-11-28-sinyal-wow'
VO='/mnt/user-data/uploads/Downloads/SINYAL-WOW/VO_sinyal_wow.wav'; SR=16000
def forms(c):
    return re.sub(r'\{(.*?)=(.*?)\}', r'\1', c), re.sub(r'\{(.*?)=(.*?)\}', r'\2', c).replace('*','')
def feat(y):
    m=librosa.feature.mfcc(y=y,sr=SR,n_mfcc=20,n_fft=512,hop_length=160)[1:]
    f=np.vstack([m,librosa.feature.delta(m)])
    return (f-f.mean(1,keepdims=True))/(f.std(1,keepdims=True)+1e-6)
def tts(s):
    subprocess.run(['espeak-ng','-v','id','-s','165','-w','e.wav',s],check=True)
    y,_=librosa.load('e.wav',sr=SR); return librosa.effects.trim(y,top_db=35)[0]
vo,_=librosa.load(VO,sr=SR)
log=subprocess.run(['ffmpeg','-hide_banner','-i',VO,'-af','silencedetect=n=-38dB:d=0.1','-f','null','-'],capture_output=True,text=True).stderr
sil=list(zip(map(float,re.findall(r'silence_start: (-?[\d.]+)',log)),map(float,re.findall(r'silence_end: ([\d.]+)',log))))
norm=lambda s:re.sub(r'[^a-z]+','',s.lower())
nas=json.load(open(PROD+'/naskah.json'))['bagian']
flat=[]
for i,t in enumerate(TEXT):
    ch=t.split('|')
    assert norm(' '.join(forms(c)[1] for c in ch))==norm(nas[i]['vo']),i+1
    flat+=[(i,c) for c in ch]
parts,marks,n=[],[],0
for i,c in flat:
    e=tts(forms(c)[1]); p=re.sub(r'[*}]','',c)[-1]
    gap=np.zeros(int((0.35 if p in '.!?:' else 0.12)*SR),np.float32)
    marks.append((n,n+len(e))); parts+=[e,gap]; n+=len(e)+len(gap)
ref=np.concatenate(parts)
D,wp=librosa.sequence.dtw(feat(ref),feat(vo),metric='cosine'); wp=wp[::-1]
g=[]
for m,_ in marks:
    g.append(wp[wp[:,0]>=m//160][0,1]*0.01)
cuts=json.load(open(PROD+'/cuts.json'))
json.dump({'sil':sil,'flat':flat,'g':g,'dur':[(b-a)/SR for a,b in marks]},open('align.json','w'))
print('silences >=0.25s:')
print('  '.join(f'{s:.2f}-{e:.2f}' for s,e in sil if e-s>=0.25))
prev=None
for k,(i,c) in enumerate(flat):
    if i!=prev: print(f'== S{i+1:02d} cut {cuts[i]:.2f}'); prev=i
    near=min(sil,key=lambda x:abs(x[1]-g[k]))
    print(f'  g {g[k]:7.2f}  sil_end {near[1]:7.2f} ({near[1]-near[0]:.2f})  {forms(c)[0]}')
