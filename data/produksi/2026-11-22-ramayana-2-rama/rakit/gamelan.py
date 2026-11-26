# Sintesis gamelan Jawa (slendro/pelog) buatan sendiri: bebas lisensi. Intensitas mengikuti mood adegan.
import json,numpy as np,wave,sys
from scipy.signal import fftconvolve
SR=48000
rng=np.random.default_rng(7)
TL=json.load(open('timeline.json'));SC=TL['scenes'];BODY=TL['body']
N=int((BODY+6)*SR)
L=np.zeros(N,np.float32);R=np.zeros(N,np.float32)
TL_=np.zeros(N,np.float32);TR_=np.zeros(N,np.float32)
SLENDRO=[0,231,474,716,955];PELOG=[0,120,258,539,675,785,943]
def hz(base,cents,octv=0): return base*2**((cents)/1200)*2**octv
def put(buf_pan,sig,t,pan=0.0,g=1.0):
    i=int(t*SR)
    if i<0 or i>=N: return
    n=min(len(sig),N-i)
    gl=g*np.cos((pan+1)*np.pi/4);gr=g*np.sin((pan+1)*np.pi/4)
    L[i:i+n]+=sig[:n]*gl;R[i:i+n]+=sig[:n]*gr
def env(n,tau): return np.exp(-np.arange(n)/SR/tau)
def bar(f,dur=2.5,vel=1.0,tau=1.3,ombak=1.004):
    n=int(dur*SR);t=np.arange(n)/SR
    y=np.zeros(n)
    for r,a,k in ((1,1,1.0),(2.76,.32,.45),(5.4,.14,.2),(8.93,.05,.1)):
        y+=a*np.sin(2*np.pi*f*r*t)*np.exp(-t/(tau*k))
        y+=a*.8*np.sin(2*np.pi*f*r*ombak*t+1)*np.exp(-t/(tau*k))
    a_=np.minimum(1,t/0.002)
    return y*a_*vel*0.5
def gong(f=52,dur=9,vel=1.0):
    n=int(dur*SR);t=np.arange(n)/SR;y=np.zeros(n)
    for r,a,tau in ((1,1,5.5),(1.003,.9,5.0),(2.0,.45,4),(2.71,.28,2.5),(4.1,.14,1.5),(5.9,.07,1.0)):
        y+=a*np.sin(2*np.pi*f*r*t+0.3*np.sin(2*np.pi*0.4*t))*np.exp(-t/tau)
    nz=rng.standard_normal(n)*np.exp(-t/0.05)*0.25
    y+=nz
    return y*np.minimum(1,t/0.006)*vel*0.55
def kettle(f,dur=1.2,vel=1.0):
    n=int(dur*SR);t=np.arange(n)/SR;y=np.zeros(n)
    for r,a,tau in ((1,1,.7),(2.0,.4,.45),(3.1,.2,.25),(4.3,.1,.15)):
        y+=a*np.sin(2*np.pi*f*r*t)*np.exp(-t/tau)
    return y*np.minimum(1,t/0.003)*vel*0.35
def kendang(kind,vel=1.0):
    n=int(0.5*SR);t=np.arange(n)/SR
    if kind=='dung':
        f=150*np.exp(-t*7)+70;ph=2*np.pi*np.cumsum(f)/SR
        y=np.sin(ph)*np.exp(-t/0.16)+0.15*rng.standard_normal(n)*np.exp(-t/0.01)
    elif kind=='tak':
        y=rng.standard_normal(n)*np.exp(-t/0.03);
        from scipy.signal import butter,lfilter
        b,a=butter(2,[1800/(SR/2),5200/(SR/2)],'band');y=lfilter(b,a,y)*2.2
    else:
        y=rng.standard_normal(n)*np.exp(-t/0.012);
        from scipy.signal import butter,lfilter
        b,a=butter(2,[700/(SR/2),2500/(SR/2)],'band');y=lfilter(b,a,y)*1.6+0.4*np.sin(2*np.pi*230*t)*np.exp(-t/0.05)
    return y*vel*0.8
def pad(f,dur,vel):
    n=int(dur*SR);t=np.arange(n)/SR
    y=np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*1.5*t+0.7)+0.25*np.sin(2*np.pi*f*2.0*t)
    e=np.minimum(1,t/2.0)*np.minimum(1,(dur-t)/2.0)
    return y*e*vel*0.12
# pola balungan (indeks nada)
CALM=[1,2,3,2,1,5,3,2, 3,5,3,2,1,2,5,3]      # slendro, lamban
TENSE=[0,2,1,0,3,2,1,0, 4,3,2,0,1,2,0,6]     # pelog
FAST=[2,3,5,3,2,3,5,6, 5,3,2,3,5,3,2,1]
def scene_music(s,t0,dur):
    m=s['mood'];T=t0
    if m==0:
        beat=1.5;sc=SLENDRO;base=hz(293.7,0)
        k=0;t=T
        while t<T+dur:
            n=CALM[k%16];put(0,bar(hz(base,sc[n%5]),3,0.55,tau=1.6),t+rng.normal(0,.01),pan=-0.15,g=0.9)
            if k%2==0: put(0,bar(hz(base,sc[CALM[(k+1)%16]%5],-1),3.5,0.5,tau=2.0),t+beat/2,pan=0.2,g=0.7)   # slenthem rendah
            if k%4==3: put(0,kettle(hz(base,sc[2],-1)),t,pan=0.35,g=0.5)
            if k%8==0: put(0,gong(55,9,0.7),t,pan=0)
            if k%4==2: put(0,kettle(hz(base,sc[4],-1)*1.0,1.5),t,pan=-0.4,g=0.35)
            # gender: arpeggio halus
            if k%2==1:
                for j in range(4):
                    put(0,bar(hz(base,sc[(CALM[(k+j)%16]+j)%5],1),1.6,0.28,tau=0.8),t+j*beat/4,pan=0.4-0.2*j,g=0.8)
            k+=1;t+=beat
    elif m==1:
        beat=2.0;sc=PELOG;base=hz(261.6,0)
        k=0;t=T
        put(0,pad(hz(base,0,-3),dur+2,1.0),T,g=1.0)
        while t<T+dur:
            n=TENSE[k%16];put(0,bar(hz(base,sc[n],-1),3.5,0.6,tau=2.0),t,pan=-0.1,g=0.9)
            if k%3==0: put(0,bar(hz(base,sc[TENSE[(k+2)%16]],-2),4,0.5,tau=2.5),t+beat*0.5,pan=0.15,g=0.7)
            if k%6==0: put(0,gong(46,10,0.9),t)
            if k%3==1: put(0,kettle(hz(base,sc[5],-1),1.6),t,pan=0.4,g=0.4)
            if k%4==3: put(0,kendang('dung'),t,g=0.5)
            k+=1;t+=beat
    elif m==2:
        beat=0.7;sc=PELOG;base=hz(261.6,0)
        k=0;t=T
        put(0,pad(hz(base,0,-3),dur+2,1.2),T)
        while t<T+dur:
            n=FAST[k%16]%7;put(0,bar(hz(base,sc[n],0),1.8,0.8,tau=0.9),t,pan=-0.1,g=0.9)
            put(0,kettle(hz(base,sc[FAST[(k+1)%16]%7],1),0.9),t+beat/2,pan=0.3,g=0.5)
            if k%2==0: put(0,kettle(hz(base,sc[FAST[k%16]%7],0),1.0),t,pan=-0.35,g=0.5)
            put(0,kendang('dung' if k%4==0 else 'tak'),t,g=0.7 if k%4==0 else 0.5)
            if k%2==1: put(0,kendang('tak'),t+beat*0.5,g=0.35)
            if k%8==0: put(0,gong(50,9,0.95),t)
            if k%4==2: put(0,bar(hz(base,sc[FAST[k%16]%7],-1),2.5,0.6,tau=1.4),t,pan=0.2,g=0.6)
            k+=1;t+=beat
    else:
        beat=0.375;sc=PELOG;base=hz(277.2,0)
        k=0;t=T
        put(0,pad(hz(base,0,-3),dur+2,1.6),T)
        while t<T+dur:
            n=FAST[k%16]%7;put(0,bar(hz(base,sc[n],0),1.2,0.9,tau=0.6),t,pan=-0.15,g=1.0)
            put(0,kettle(hz(base,sc[FAST[(k+3)%16]%7],1),0.7),t+beat/2,pan=0.35,g=0.55)
            put(0,kettle(hz(base,sc[FAST[(k+5)%16]%7],0),0.7),t+beat/4,pan=-0.4,g=0.45)
            put(0,kendang('dung' if k%4==0 else 'tak'),t,g=0.8 if k%4==0 else 0.55)
            put(0,kendang('tak'),t+beat/2,g=0.4)
            if k%2==0: put(0,kendang('tak'),t+beat/4,g=0.3)
            if k%8==0: put(0,gong(48,8,1.0),t)
            if k%4==0: put(0,gong(98,5,0.5),t+0.01) if False else None
            if k%4==2: put(0,bar(hz(base,sc[FAST[k%16]%7],-1),2.0,0.8,tau=1.0),t,pan=0.1,g=0.7)
            k+=1;t+=beat
def window(buf,t0,t1,fi,fo):
    pass
# render per scene dengan crossfade antar adegan
for s in SC:
    t0=s['t0'];dur=s['slot']+1.5
    L[:]=0;R[:]=0
    scene_music(s,t0,dur)
    # jendela dengan fade-in 0.8 dan fade-out 1.6 (energi menyatu di transisi)
    w=np.zeros(N,np.float32);a=int(max(0,t0-0.8)*SR);b=int(min(N,(t0+s['slot']+0.8)*SR))
    w[a:b]=1
    fi=int(0.9*SR);fo=int(1.7*SR)
    w[a:a+fi]=np.linspace(0,1,min(fi,b-a))**1.5;w[b-fo:b]=np.linspace(1,0,fo)**1.5
    w=w*{0:1.26,1:1.26,2:0.77,3:0.66}[s['mood']]
    TL_+=L*w;TR_+=R*w
    L[:]=0;R[:]=0
L=TL_;R=TR_
# reverb ruang gamelan
def ir(sec,seed):
    r=np.random.default_rng(seed);n=int(sec*SR);t=np.arange(n)/SR
    return (r.standard_normal(n)*np.exp(-t/0.55)*np.minimum(1,t/0.01)).astype(np.float32)
irl=ir(2.2,1);irr=ir(2.2,2)
wl=fftconvolve(L,irl)[:N];wr=fftconvolve(R,irr)[:N]
wl/=np.abs(wl).max()+1e-9;wr/=np.abs(wr).max()+1e-9
pk=max(np.abs(L).max(),np.abs(R).max())
Lw=0.80*L/pk+0.22*wl*0.8;Rw=0.80*R/pk+0.22*wr*0.8
out=np.stack([Lw,Rw],1)
out=(out/np.abs(out).max()*0.8).astype(np.float32)
D=int(BODY*SR);out=out[:D]
# fade in/out keseluruhan
f=int(2.5*SR);out[:f]*=np.linspace(0,1,f)[:,None];out[-f*2:]*=np.linspace(1,0,f*2)[:,None]
with wave.open('gamelan.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
print('ok',BODY)
