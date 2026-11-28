"""Rakit Short Sinyal Wow!: hapus bintang, retime, transisi halus, teks layar, subtitle, audio."""
import json, re, subprocess, sys, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
import dewm
V='/mnt/user-data/outputs/SINYAL-WOW/VIDEO'; O='/mnt/user-data/outputs/SINYAL-WOW/FINAL'; os.makedirs(O,exist_ok=True)
OUT=f'{O}/sinyal_wow_pulang_ngantor.mp4'; SRT=f'{O}/subtitle_sinyal_wow.srt'
FPS,WD,HT,T=24,1080,1920,115.2
CUTS=[0.0,12.04,19.86,26.89,36.10,43.55,52.55,61.44,68.72,75.46,83.47,88.77,98.93,106.95,T]
S=[int(round(c*FPS)) for c in CUTS]; N=S[-1]
SECTION={6,10,12}
H=[0]+[10 if j in SECTION else (5 if j==4 else 8) for j in range(1,14)]+[0]

def read(path):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',path,'-an','-vf','scale=in_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,format=bgr24','-f','rawvideo','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(WD*HT*3)
        if len(b)<WD*HT*3: break
        yield np.frombuffer(b,np.uint8).reshape(HT,WD,3).copy()
    assert p.wait()==0

def prep(i):
    L=(S[i+1]+H[i+1])-(S[i]-H[i])
    fr=[dewm.clean(f) for f in read(f'{V}/S{i+1:02d}.mp4')]
    D=len(fr); mode='asli'
    if D<L-3 or D>L*1.2:   # perlu retime halus dengan interpolasi gerak
        mode=f'retime x{D/L:.2f}'
        e=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{WD}x{HT}','-r',str(FPS),'-i','-','-c:v','ffv1',f'c{i}.mkv'],stdin=subprocess.PIPE)
        for f in fr: e.stdin.write(f.tobytes())
        e.stdin.close(); assert e.wait()==0
        subprocess.run(['ffmpeg','-v','error','-y','-i',f'c{i}.mkv','-vf',f'setpts=PTS*{(L+1)/D:.6f},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop_duration=1,format=bgr0','-c:v','ffv1',f'r{i}.mkv'],check=True)
        fr=list(read(f'r{i}.mkv')); os.remove(f'c{i}.mkv'); os.remove(f'r{i}.mkv')
    while len(fr)<L: fr.append(fr[-1])
    print(f'S{i+1:02d} klip {D} frame, dipakai {L}, {mode}',flush=True)
    return fr[:L]

# ---------- teks layar ----------
POP='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
def pill(text,size,cy,fg=(255,196,84)):
    f=ImageFont.truetype(POP,size); im=Image.new('RGBA',(WD,HT),(0,0,0,0)); d=ImageDraw.Draw(im)
    x0,y0,x1,y1=d.textbbox((0,0),text,font=f,anchor='mm'); px,py=int(size*.45),int(size*.28)
    box=(WD//2+x0-px,cy+y0-py,WD//2+x1+px,cy+y1+py)
    d.rounded_rectangle(box,radius=(box[3]-box[1])//2,fill=(10,16,34,205),outline=fg+(230,),width=4)
    d.text((WD//2,cy),text,font=f,fill=fg+(255,),anchor='mm')
    return np.array(im)[...,[2,1,0,3]]
BADGE=[(6.16,11.0,pill('1977',140,290)),(44.83,48.5,pill('±1420 MHz',104,270)),(54.24,58.0,pill('72 detik',118,260)),(89.05,98.55,pill('hipotesis, belum terbukti',54,175,(190,225,255)))]
def comp(frame,rgba,a):
    al=rgba[...,3]
    ys,xs=np.nonzero(al)
    if not len(ys) or a<=0: return frame
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    m=al[y0:y1,x0:x1,None].astype(np.float32)/255*a
    frame[y0:y1,x0:x1]=(frame[y0:y1,x0:x1]*(1-m)+rgba[y0:y1,x0:x1,:3]*m+0.5).astype(np.uint8)
    return frame
def env(t,a,b,d=0.25):
    return float(np.clip(min((t-a)/d,(b-t)/d),0,1))

# pelacakan lingkaran merah S04
def track(frames,ref_k=12):
    orb=cv2.ORB_create(4000); g=lambda f:cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    kr,dr=orb.detectAndCompute(g(frames[ref_k]),None); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    P=[]; cur=g(frames[ref_k])
    pts0=cv2.goodFeaturesToTrack(cur,600,0.01,12)
    P=[None]*len(frames)
    for rng in (range(ref_k,len(frames)),range(ref_k,-1,-1)):
        prev=cur; p0=pts0.copy(); pp=pts0.copy()
        for k in rng:
            gk=g(frames[k])
            nx,st,_=cv2.calcOpticalFlowPyrLK(prev,gk,pp,None,winSize=(31,31),maxLevel=4)
            ok=st.ravel()==1; p0,pp=p0[ok],nx[ok]; prev=gk
            M,inl=cv2.estimateAffinePartial2D(p0,pp,ransacReprojThreshold=2.0)
            P[k]=M
            keep=inl.ravel()==1
            if keep.sum()>60: p0,pp=p0[keep],pp[keep]
    A=np.array(P); w=5; pad=np.pad(A,((w,w),(0,0),(0,0)),mode='edge')
    return [pad[k:k+2*w+1].mean(0) for k in range(len(frames))]
def s04_layers(cx,cy):
    def layer(text,font,size,xy,fill,ang):
        f=ImageFont.truetype(font,size); im=Image.new('RGBA',(WD,HT),(0,0,0,0))
        ImageDraw.Draw(im).text(xy,text,font=f,fill=fill,anchor='mm')
        return np.array(im.rotate(ang,center=xy,resample=Image.BICUBIC))[...,[2,1,0,3]]
    return (layer('6EQUJ5','/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',80,(cx-5,cy-50),(38,32,40,245),8),
            layer('Wow!','/usr/share/fonts/truetype/google-fonts/ofl/comicrelief/ComicRelief-Bold.ttf',116,(cx+5,cy+68),(196,32,30,255),12))

# ---------- subtitle ----------
raw=json.load(open('cues_raw.json'))
MERGE={'yang kaget','penerima.','mengusulkan:','*terlalu sedikit*.','dan Australia.'}
cl=[]
for c in raw:
    if c['t'] in MERGE: cl[-1]['t']+=' '+c['t']
    else: cl.append(dict(c))
cues=[]
for k,c in enumerate(cl):
    a=max(c['on']-0.05,CUTS[c['scene']-1] if c['scene']!=5 else 36.12)
    nxt=cl[k+1] if k+1<len(cl) else None
    if nxt and nxt['scene']==c['scene']: b=nxt['on']-0.05
    else: b=min(c['off']+0.3,CUTS[c['scene']]-0.02)
    if c['scene']==4 and nxt['scene']==5: b=36.08
    if c['scene']==14 and not nxt: b=T-0.15
    cues.append((round(a,3),round(b,3),c['t']))
for x,y in zip(cues,cues[1:]): assert x[1]<=y[0]+1e-6 and x[1]-x[0]>=0.35,(x,y)
def at(t):
    c=int(round(t*100)); return f'{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}'
def st(t):
    m=int(round(t*1000)); return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Poppins,112,&H00C5D9E9,&H000000FF,&H00241410,&H80000000,-1,0,0,0,100,100,0,0,1,8,3,2,90,90,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open('subs.ass','w') as a, open(SRT,'w') as s:
    a.write(head)
    for k,(x,y,t) in enumerate(cues,1):
        mv=760 if 68.5<x<75.4 else 0   # S09: jangan menutup wajah astronom
        burn=not (t=='*Wow!*' and 35<x<36)   # sudah tampil besar di dalam lingkaran
        rich=re.sub(r'\*(.+?)\*',r'{\\c&H59A2F4&}\1{\\c&HC5D9E9&}',t)
        if burn: a.write(f"Dialogue: 0,{at(x)},{at(y)},Sub,,0,0,{mv},,{{\\fad(60,40)}}{rich}\n")
        s.write(f"{k}\n{st(x)} --> {st(y)}\n{t.replace('*','')}\n\n")
json.dump(cues,open('cues.json','w'),ensure_ascii=False)
print(len(cues),'cue')
if '--subs' in sys.argv: sys.exit()

ENC=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{WD}x{HT}','-r',str(FPS),'-i','-','-i','mix.wav',
 '-vf','ass=subs.ass,scale=out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p','-map','0:v','-map','1:a',
 '-c:v','libx264','-preset','slow','-crf','20','-tune','animation','-maxrate','10M','-bufsize','20M','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
 '-c:a','aac','-b:a','192k','-t',str(N/FPS),'-movflags','+faststart',OUT]
def write(path,frames):
    e=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{WD}x{HT}','-r',str(FPS),'-i','-','-c:v','ffv1','-pix_fmt','bgr0',path],stdin=subprocess.PIPE)
    for f in frames: e.stdin.write(f.tobytes())
    e.stdin.close(); assert e.wait()==0
for i in range(14):
    if os.path.exists(f'p{i}.mkv'): continue
    fr=prep(i)
    if i==3:
        M=track(fr); L6,LW=s04_layers(518,985)
        for k,f in enumerate(fr):
            t=(S[3]-H[3]+k)/FPS
            for lay,t0 in ((L6,29.0),(LW,35.2)):
                a=float(np.clip((t-t0)/0.2,0,1))
                if a>0: comp(f,cv2.warpAffine(lay,M[k],(WD,HT),flags=cv2.INTER_CUBIC),a)
        np.save('s04_M.npy',np.array(M))
    write(f'part.mkv',fr); os.rename('part.mkv',f'p{i}.mkv'); del fr
if '--prep' in sys.argv: sys.exit()
enc=subprocess.Popen(ENC,stdin=subprocess.PIPE)
cache={}
def frame(i,n):
    if i not in cache: cache[i]=[read(f'p{i}.mkv'),-1,None]
    c=cache[i]; k=max(0,n-(S[i]-H[i]))
    while c[1]<k:
        f=next(c[0],None)
        if f is None: break
        c[2]=f; c[1]+=1
    return c[2]
def zoom(f,s):
    if s<=1.0005: return f
    return cv2.warpAffine(f,cv2.getRotationMatrix2D((WD/2,HT/2),0,s),(WD,HT),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
i=0
for n in range(N):
    while n>=S[i+1]: i+=1
    out=None
    for j in (i,i+1):
        if 0<j<14 and S[j]-H[j]<=n<S[j]+H[j]:
            x=(n-(S[j]-H[j])+0.5)/(2*H[j]); e=x*x*(3-2*x); A,B=frame(j-1,n),frame(j,n)
            if j in SECTION: A,B=zoom(A,1+0.09*e),zoom(B,1+0.07*(1-e))
            out=cv2.addWeighted(A,1-e,B,e,0)
    if out is None: out=frame(i,n).copy()
    t=n/FPS
    for a,b,img in BADGE:
        if a<=t<b: comp(out,img,env(t,a,b))
    for old in [k for k in cache if k<i-1]: del cache[old]
    enc.stdin.write(out.tobytes())
enc.stdin.close(); assert enc.wait()==0
print('selesai',OUT)
