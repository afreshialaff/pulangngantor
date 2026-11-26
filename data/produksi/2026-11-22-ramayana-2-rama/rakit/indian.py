# lapisan India buatan sendiri (bebas lisensi): dengung tanpura + suling bansuri
import json,numpy as np,wave
from scipy.signal import fftconvolve,butter,lfilter
SR=48000;rng=np.random.default_rng(11)
T=json.load(open('timeline.json'));S=T['scenes'];D=T['body'];N=int(D*SR)
SA=146.83
def add(b,sig,t,g=1.0):
    i=int(t*SR)
    if i<N:
        n=min(len(sig),N-i);b[i:i+n]+=sig[:n]*g
def pluck(f,dur=4.5):
    n=int(dur*SR);t=np.arange(n)/SR;y=np.zeros(n)
    for h in range(1,22):
        bloom=1+0.9*np.exp(-((t-0.25-h*0.07)/0.45)**2)
        y+=np.sin(2*np.pi*f*h*t*(1+0.00012*h)+rng.uniform(0,6))*bloom*np.exp(-t/(2.6/(1+0.08*h)))/h**1.15
    return y*np.minimum(1,t/0.03)
cyc=[pluck(SA*0.75),pluck(SA),pluck(SA*1.001),pluck(SA*0.5)]
drL=np.zeros(N);drR=np.zeros(N);t=0.0;k=0
while t<D:
    add(drL,cyc[k%4],t,0.8 if k%2 else 0.55);add(drR,cyc[k%4],t+0.012,0.55 if k%2 else 0.8);t+=1.25 if k%4<3 else 1.7;k+=1
# suling
R=[2**(c/12) for c in (0,2,4,7,9,12,14,16)]            # Bhupali
M=[2**(c/12) for c in (0,1,4,5,7,8,11,12)]             # Bhairav
def flute(freqs,durs):
    f=np.concatenate([np.full(int(d*SR),x) for x,d in zip(freqs,durs)])
    a=np.exp(-1/(0.07*SR));f=lfilter([1-a],[1,-a],f,zi=[f[0]*a])[0]   # meluncur antar nada
    n=len(f);t=np.arange(n)/SR
    vib=1+0.007*np.sin(2*np.pi*5.1*t)*np.clip((t%1.6-0.4)/0.6,0,1)
    ph=2*np.pi*np.cumsum(f*vib)/SR
    y=np.sin(ph)+0.22*np.sin(2*ph)+0.07*np.sin(3*ph)
    b,a_=butter(2,[900/(SR/2),3200/(SR/2)],'band');y+=lfilter(b,a_,rng.standard_normal(n))*0.09
    env=np.ones(n);i=0
    for d in durs:
        m=int(d*SR);r=min(int(0.12*SR),m//3)
        env[i:i+r]*=np.linspace(0.55,1,r);env[i+m-r:i+m]*=np.linspace(1,0.65,r);i+=m
    fi=int(0.5*SR);fo=int(1.2*SR);env[:fi]*=np.linspace(0,1,fi)**1.5;env[-fo:]*=np.linspace(1,0,fo)
    return y*env
fl=np.zeros(N)
warm={'S01':1.0,'S06':.7,'S08':.8,'S10':.9,'S11':.8,'S14':.8,'S15':.6,'S18':.6,'S24':.9,'S25':.9,'S26':1.0,'S27':1.0,'S30':.6,'S32':1.0,'S35':.8,'S36':.6,'S37':.7,'S39':.7,'S41':1.0,'S42':1.0,'S43':.9}
for s in S:
    if s['id'] not in warm: continue
    sc=M if s['mood']==1 else R
    t=s['t0']+0.3;end=s['t0']+s['slot']-0.2;pos=int(rng.integers(2,5))
    while end-t>3.0:
        freqs=[];durs=[];tot=0;L=min(end-t,rng.uniform(4,6.5))
        while tot<L-0.5:
            pos=int(np.clip(pos+rng.choice([-2,-1,-1,1,1,2]),0,7));d=float(min(L-tot,rng.choice([0.6,0.9,1.3,1.8])))
            freqs.append(SA*2*sc[pos]);durs.append(d);tot+=d
        freqs.append(SA*2*sc[int(rng.choice([0,3,5]))]);durs.append(1.7)
        add(fl,flute(freqs,durs),t,warm[s['id']]);t+=tot+1.7+rng.uniform(0.8,1.8)
def ir(sec,seed):
    r=np.random.default_rng(seed);n=int(sec*SR);t=np.arange(n)/SR
    return r.standard_normal(n)*np.exp(-t/0.7)*np.minimum(1,t/0.015)
nm=lambda x:x/(np.abs(x).max()+1e-9)
wl=nm(fftconvolve(fl,ir(2.8,3))[:N]);wr=nm(fftconvolve(fl,ir(2.8,4))[:N]);f=nm(fl)
dl=nm(drL);dr=nm(drR)
out=np.stack([0.17*dl+0.30*f*0.9+0.20*wl, 0.17*dr+0.30*f*0.75+0.20*wr],1)
fi=int(2*SR);fo=int(4*SR);out[:fi]*=np.linspace(0,1,fi)[:,None];out[-fo:]*=np.linspace(1,0,fo)[:,None]
with wave.open('indian.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
print('indian ok')
