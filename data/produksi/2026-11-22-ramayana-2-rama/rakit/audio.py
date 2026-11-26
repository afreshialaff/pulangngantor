import json,subprocess
T=json.load(open('timeline.json'));S=T['scenes'];body=T['body']
import numpy as np,wave
SR=48000
U='/mnt/user-data/uploads/RAMAYANA PART 2/VO/'
vo=np.zeros(int(body*SR),np.float32)
raw=[]
for s in S:
    x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',U+s['id']+'_VO.mp3','-ac','1','-ar',str(SR),'-f','f32le','-']),np.float32)
    a=int(max(0,s['vo_start']-0.1)*SR);b=int(min(len(x)/SR,s['vo_end']+0.22)*SR);y=x[a:b].copy()
    fr=y[:len(y)//2400*2400].reshape(-1,2400);e=np.sqrt((fr**2).mean(1));rms=np.sqrt((e[e>e.max()*0.08]**2).mean())
    raw.append((s,y,rms,s['vo_at']-(s['vo_start']-a/SR)))
tgt=np.median([r[2] for r in raw])
for s,y,rms,at in raw:
    y*=np.clip(tgt/rms,0.7,1.45)
    n=int(0.02*SR);y[:n]*=np.linspace(0,1,n);y[-n*2:]*=np.linspace(1,0,n*2)
    i=int(max(0,at)*SR);m=min(len(y),len(vo)-i);vo[i:i+m]+=y[:m]
st=np.clip(np.stack([vo,vo],1),-1,1)
with wave.open('vo_track.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype('<i2').tobytes())
D=body
fb="[0:a]aresample=48000,volume=0.85[gm];[1:a]aresample=48000,volume=0.9[ind];[gm][ind]amix=inputs=2:normalize=0[bed0];"
# transition hits
hits=[]
for i,s in enumerate(S[:-1]):
    tr,X=s['trans'];t=S[i+1]['t0']
    if tr=='fadeblack': hits.append((t+X/2-0.7,'big'))
    else: hits.append((t+X/2-0.4,'small'))
k=0;parts=[]
for (t,kind) in hits:
    dms=int(max(0,t)*1000)
    if kind=='big':
        fb+=(f"anoisesrc=color=pink:amplitude=0.6:sample_rate=48000:duration=1.4,bandpass=f=900:w=1.2,"
             f"afade=t=in:d=0.6:curve=exp,afade=t=out:st=0.7:d=0.7,volume=0.12,pan=stereo|c0=c0|c1=c0,adelay={dms}|{dms}[h{k}];"); parts.append(f'[h{k}]');k+=1
        fb+=(f"aevalsrc='0.9*sin(2*PI*48*t)*exp(-3.2*t)|0.9*sin(2*PI*48*t)*exp(-3.2*t)':s=48000:d=1.6,volume=0.2,adelay={dms+700}|{dms+700}[h{k}];"); parts.append(f'[h{k}]');k+=1
    else:
        fb+=(f"anoisesrc=color=pink:amplitude=0.5:sample_rate=48000:duration=0.8,bandpass=f=1400:w=1.5,"
             f"afade=t=in:d=0.35:curve=exp,afade=t=out:st=0.4:d=0.4,volume=0.04,pan=stereo|c0=c0|c1=c0,adelay={dms}|{dms}[h{k}];"); parts.append(f'[h{k}]');k+=1
A=json.load(open('align.json'));s31=[s for s in S if s['id']=='S31'][0]
wb=[w for w in A['S31']['words'] if w[0]=='Busur'][0]
d=int((s31['vo_at']+wb[1]-s31['vo_start']+0.35)*1000)
fb+=(f"anoisesrc=color=brown:amplitude=0.9:sample_rate=48000:duration=2.4,lowpass=f=500,afade=t=out:st=0.1:d=2.3:curve=exp,volume=0.55,pan=stereo|c0=c0|c1=c0,adelay={d}|{d}[q0];"
     f"anoisesrc=color=white:amplitude=0.7:sample_rate=48000:duration=0.18,highpass=f=1200,afade=t=out:st=0:d=0.18:curve=exp,volume=0.35,pan=stereo|c0=c0|c1=c0,adelay={d}|{d}[q1];"
     f"aevalsrc='sin(2*PI*44*t)*exp(-2.5*t)|sin(2*PI*44*t)*exp(-2.5*t)':s=48000:d=2,volume=0.4,adelay={d}|{d}[q2];")
parts+=['[q0]','[q1]','[q2]']
fb+=f"[bed0]{''.join(parts)}amix=inputs={1+len(parts)}:normalize=0:duration=first,atrim=0:{D:.3f}[bed]"
subprocess.check_call(['ffmpeg','-v','error','-y','-i','gamelan.wav','-i','indian.wav','-filter_complex',fb,'-map','[bed]','-c:a','pcm_s16le','bed.wav'])
# duck bed under VO and mix, loudness
mix=("[0:a]asplit=2[vo][sc];[1:a]volume=0.55[bq];[bq][sc]sidechaincompress=threshold=0.02:ratio=3:attack=60:release=1100:makeup=1[bd];"
     "[vo][bd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]")
subprocess.check_call(['ffmpeg','-v','error','-y','-i','vo_track.wav','-i','bed.wav','-filter_complex',mix,'-map','[o]','-ar','48000','-c:a','pcm_s16le','mix.wav'])
print('ok')
