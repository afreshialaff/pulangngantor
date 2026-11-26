import json,re
T=json.load(open('timeline.json'));A=json.load(open('align.json'));MAX=40
def bal(ws):
    t=' '.join(ws)
    if len(t)<=MAX: return t
    c=[]
    for k in range(1,len(ws)):
        a=' '.join(ws[:k]);b=' '.join(ws[k:])
        c.append((max(len(a),len(b))>MAX+4, abs(len(a)-len(b))-(8 if a[-1] in ',.:?!' else 0),k))
    k=min(c)[2];return ' '.join(ws[:k])+'\n'+' '.join(ws[k:])
def split(idx,W):
    t=' '.join(W[i] for i in idx)
    if len(t)<=2*MAX-4: return [idx]
    c=[]
    for k in range(2,len(idx)-1):
        a=len(' '.join(W[i] for i in idx[:k]));b=len(t)-a-1
        c.append((abs(a-b)-(30 if W[idx[k-1]][-1] in ',:;' else 0),k))
    k=min(c)[1];return split(idx[:k],W)+split(idx[k:],W)
cues=[]
for s in T['scenes']:
    a=A[s['id']];words=a['words'];W=[w[0] for w in words]
    assert ' '.join(W)==' '.join(s['text'].split())
    sents=[];cur=[]
    for i,w in enumerate(W):
        cur.append(i)
        if w[-1] in '.?!': sents.append(cur);cur=[]
    if cur: sents.append(cur)
    chunks=[c for x in sents for c in split(x,W)]
    # gabung potongan sangat pendek
    i=0
    while i<len(chunks):
        t=' '.join(W[j] for j in chunks[i])
        if len(t)<14:
            for nb in ([i+1] if i+1<len(chunks) else [])+([i-1] if i else []):
                m=sorted(chunks[i]+chunks[nb])
                if len(' '.join(W[j] for j in m))<=2*MAX-6:
                    lo=min(i,nb);chunks[lo:lo+2]=[m];i=lo;break
        i+=1
    gaps=a['gaps'];s0,s1=a['speech']
    B=[[s0,None]]
    for k in range(len(chunks)-1):
        e=words[chunks[k][-1]][2];b=words[chunks[k+1][0]][1];m=(e+b)/2
        punct=W[chunks[k][-1]][-1] in '.?!:,'
        win=0.75 if punct else 0.3
        cand=[(max(g0-m,m-g1,0)-0.6*(g1-g0),g0,g1) for g0,g1 in gaps if max(g0-m,m-g1,0)<=win and g0>B[-1][0]+0.3]
        if cand: _,g0,g1=min(cand);B[-1][1]=g0+0.12;B.append([g1-0.08,None])
        else: B[-1][1]=m;B.append([m,None])
    B[-1][1]=s1+0.2
    off=s['vo_at']-s0
    for c,(x,y) in zip(chunks,B): cues.append([x+off-0.05,y+off,bal([W[j] for j in c]),s['id']])
for i in range(len(cues)-1):
    g=cues[i+1][0]-cues[i][1]
    if g<0.5: cues[i][1]=cues[i+1][0]-0.02
json.dump(cues,open('cues.json','w'),ensure_ascii=False,indent=0)
def srt(t):
    ms=int(round(t*1000));return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
def ts(t):
    c=int(round(t*100));return f"{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}"
INTRO=103/24;XI=12/24;off=INTRO-XI
with open('subtitle.srt','w') as f:
    for i,(a,b,t,_) in enumerate(cues,1): f.write(f"{i}\n{srt(a+off)} --> {srt(b+off)}\n{t}\n\n")
KEY=r"\b(Dewa Wisnu|Wisnu|Rama Nawami|Rama|Sinta|Siwa|Dasarata|Laksmana|Parasurama|Wiswamitra|Wasista|Tataka|Marica|Subahu|Ahalya|Ayodhya|Mithila|Janaka|Walmiki|Rahwana|Kausalya|Bharata|Kaikeyi|Sumitra|Satrugna|Tulsidas|Prambanan|Resyasringa|Sarayu|Atibala|Bala)\b"
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Poppins Medium,60,&H00C5D9E9,&H000000FF,&H00101014,&H96000000,0,0,0,0,100,100,0,0,1,3.6,1.8,2,160,160,58,1
Style: Kicker,Poppins Medium,38,&H0059A2F4,&H000000FF,&H00101014,&H96000000,0,0,0,0,100,100,6,0,1,2.5,1.5,8,100,100,70,1
Style: Title,Poppins,82,&H00C5D9E9,&H000000FF,&H00101014,&H96000000,1,0,0,0,100,100,1,0,1,4,2.5,8,100,100,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open('subs.ass','w') as f:
    f.write(hdr)
    f.write(f"Dialogue: 1,{ts(off+0.7)},{ts(off+6.2)},Kicker,,0,0,0,,{{\\fad(500,600)}}RAMAYANA · BAGIAN 2\n")
    f.write(f"Dialogue: 1,{ts(off+0.9)},{ts(off+6.2)},Title,,0,0,0,,{{\\fad(600,600)}}Rama, Dewa yang Memilih Jadi Manusia\n")
    for a,b,t,_ in cues:
        t=re.sub(KEY,lambda m:'{\\c&H59A2F4&}'+m.group(1)+'{\\c&HC5D9E9&}',t).replace('\n','\\N')
        f.write(f"Dialogue: 0,{ts(a+off)},{ts(b+off)},Sub,,0,0,0,,{{\\fad(90,90)}}{t}\n")
cps=[len(c[2])/(c[1]-c[0]) for c in cues]
print(len(cues),'cues; max cps',round(max(cps),1),'min dur',round(min(c[1]-c[0] for c in cues),2),'max line',max(len(l) for c in cues for l in c[2].split('\n')))
for c in cues[:8]: print(c[3],round(c[0],2),round(c[1],2),repr(c[2]))
