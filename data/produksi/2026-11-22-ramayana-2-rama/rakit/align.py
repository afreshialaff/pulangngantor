import numpy as np,subprocess,re,json,wave,io,sys
from scipy.fftpack import dct
from vo import VO
SR=16000;HOP=160;WIN=400
D="/mnt/user-data/uploads/RAMAYANA PART 2/VO/"
def load(p):
    r=subprocess.check_output(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','s16le','-'])
    return np.frombuffer(r,'<i2').astype(np.float32)/32768
def mel():
    f=lambda h:2595*np.log10(1+h/700);g=lambda m:700*(10**(m/2595)-1)
    pts=g(np.linspace(f(80),f(7600),28));b=np.floor(513*pts/SR).astype(int);F=np.zeros((26,257))
    for i in range(26):
        a,c,d=b[i],b[i+1],b[i+2]
        for k in range(a,c):F[i,k]=(k-a)/max(1,c-a)
        for k in range(c,d):F[i,k]=(d-k)/max(1,d-c)
    return F
FB=mel()
def feats(x):
    x=np.append(x[0],x[1:]-0.97*x[:-1]);x=np.pad(x,(0,WIN))
    n=(len(x)-WIN)//HOP+1;fr=np.stack([x[i*HOP:i*HOP+WIN] for i in range(n)])*np.hamming(WIN)
    P=np.abs(np.fft.rfft(fr,512))**2
    db=10*np.log10(P.sum(1)+1e-10)
    c=dct(np.log(P@FB.T+1e-8),norm='ortho',axis=1)[:,1:13]
    return c,db
def norm(c):
    c=(c-c.mean(0))/(c.std(0)+1e-6);d=np.gradient(c,axis=0)*2
    v=np.hstack([c,d]);return v/(np.linalg.norm(v,axis=1,keepdims=True)+1e-9)
def tts(w):
    r=subprocess.check_output(['espeak-ng','-v','id','-s','165','--stdout',w])
    open('/tmp/_w.wav','wb').write(r);x=load('/tmp/_w.wav')
    nz=np.where(np.abs(x)>0.01)[0]
    return x[max(0,nz[0]-80):nz[-1]+80]
def dtw(A,B):
    C=1-A@B.T;n,m=C.shape;acc=np.full((n+1,m+1),np.inf);acc[0,0]=0
    bt=np.zeros((n,m),np.int8)
    for i in range(1,n+1):
        prev=acc[i-1];cur=acc[i];c=C[i-1]
        for j in range(1,m+1):
            a=prev[j-1]+2*c[j-1];b=prev[j]+c[j-1];d=cur[j-1]+c[j-1]
            if a<=b and a<=d:cur[j]=a;bt[i-1,j-1]=0
            elif b<=d:cur[j]=b;bt[i-1,j-1]=1
            else:cur[j]=d;bt[i-1,j-1]=2
    i,j=n-1,m-1;path=[]
    while i>=0 and j>=0:
        path.append((i,j));k=bt[i,j]
        if k==0:i-=1;j-=1
        elif k==1:i-=1
        else:j-=1
    return path[::-1],acc[n,m]/(n+m)
out={}
for sid,bag,kl,text in VO:
    x=load(D+sid+'_VO.mp3');c,db=feats(x)
    thr=np.percentile(db,95)-32
    sp=db>thr
    # tutup celah sangat pendek (<90 ms)
    i=0
    while i<len(sp):
        if not sp[i]:
            j=i
            while j<len(sp) and not sp[j]:j+=1
            if j-i<9 and i>0 and j<len(sp):sp[i:j]=True
            i=j
        else:i+=1
    idx=np.where(sp)[0]
    words=text.split()
    segs=[tts(re.sub(r'[^\w\- ]','',w) or w) for w in words]
    y=np.concatenate(segs);c2,db2=feats(y)
    keep=db2>np.percentile(db2,95)-35;idx2=np.where(keep)[0]
    A=norm(c[idx]);B=norm(c2[idx2])
    path,cost=dtw(A,B)
    j2i={}
    for i,j in path:j2i.setdefault(j,[]).append(i)
    bounds=np.cumsum([0]+[len(s) for s in segs])/HOP
    W=[]
    for k,w in enumerate(words):
        js=np.where((idx2>=bounds[k])&(idx2<bounds[k+1]))[0]
        ii=[i for j in js for i in j2i.get(j,[])]
        W.append([w,round(idx[min(ii)]*0.01,2),round(idx[max(ii)]*0.01+0.025,2)])
    # jeda nyata di audio
    gaps=[];i=0
    while i<len(sp):
        if not sp[i]:
            j=i
            while j<len(sp) and not sp[j]:j+=1
            if j-i>=14:gaps.append((i*0.01,j*0.01))
            i=j
        else:i+=1
    out[sid]=dict(dur=len(x)/SR,words=W,gaps=gaps,cost=float(cost),speech=[idx[0]*0.01,idx[-1]*0.01+0.025])
    # validasi: akhir kalimat harus dekat jeda
    res=[]
    for k,(w,a,b) in enumerate(W[:-1]):
        if w[-1] in '.?!:':
            nb=W[k+1][1]
            d=min([0 if g0-0.05<=(b+nb)/2<=g1+0.05 else min(abs(g0-b),abs(g1-nb)) for g0,g1 in gaps] or [9])
            res.append((w,round(d,2)))
    print(sid,round(float(cost),3),res,flush=True)
json.dump(out,open('align.json','w'),indent=0)
