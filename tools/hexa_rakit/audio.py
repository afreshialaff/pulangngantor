import json,subprocess
T=json.load(open('timeline.json'));S=T['scenes'];body=T['body']
VO='/mnt/user-data/uploads/VONYCH/VID/VO.wav'
n=len(S)
fc=f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit={n}"+''.join(f'[v{i}]' for i in range(n))+';'
for i,s in enumerate(S):
    a=max(0,s['vo_start']-0.08);b=s['vo_end']+0.22;d=int(round((s['vo_at']-0.08)*1000))
    fc+=f"[v{i}]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.06:.3f}:d=0.06,adelay={d}|{d}[w{i}];"
fc+=''.join(f'[w{i}]' for i in range(n))+f"amix=inputs={n}:normalize=0:duration=longest,apad,atrim=0:{body:.3f}[vo]"
subprocess.check_call(['ffmpeg','-v','error','-y','-i',VO,'-filter_complex',fc,'-map','[vo]','-c:a','pcm_s16le','vo_track.wav'])
# bed
D=body
ev=("0.42*sin(2*PI*55*t)*(0.65+0.35*sin(2*PI*0.06*t))+0.30*sin(2*PI*82.41*t)*(0.6+0.4*sin(2*PI*0.045*t+1.3))"
    "+0.12*sin(2*PI*110.2*t)*(0.5+0.5*sin(2*PI*0.031*t+2))+0.06*sin(2*PI*164.8*t)*(0.5+0.5*sin(2*PI*0.023*t))")
fb=f"aevalsrc='{ev}|{ev}':s=48000:d={D:.3f}[dr];anoisesrc=color=brown:amplitude=0.5:sample_rate=48000:duration={D:.3f},lowpass=f=350,pan=stereo|c0=c0|c1=c0,volume=0.5[nz];"
fb+=f"[dr][nz]amix=inputs=2:normalize=0,lowpass=f=700,highpass=f=35,afade=t=in:d=3,afade=t=out:st={D-4:.3f}:d=4,volume=0.16[bed0];"
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
             f"afade=t=in:d=0.6:curve=exp,afade=t=out:st=0.7:d=0.7,volume=0.22,pan=stereo|c0=c0|c1=c0,adelay={dms}|{dms}[h{k}];"); parts.append(f'[h{k}]');k+=1
        fb+=(f"aevalsrc='0.9*sin(2*PI*48*t)*exp(-3.2*t)|0.9*sin(2*PI*48*t)*exp(-3.2*t)':s=48000:d=1.6,volume=0.35,adelay={dms+700}|{dms+700}[h{k}];"); parts.append(f'[h{k}]');k+=1
    else:
        fb+=(f"anoisesrc=color=pink:amplitude=0.5:sample_rate=48000:duration=0.8,bandpass=f=1400:w=1.5,"
             f"afade=t=in:d=0.35:curve=exp,afade=t=out:st=0.4:d=0.4,volume=0.07,pan=stereo|c0=c0|c1=c0,adelay={dms}|{dms}[h{k}];"); parts.append(f'[h{k}]');k+=1
fb+=f"[bed0]{''.join(parts)}amix=inputs={1+len(parts)}:normalize=0:duration=first,atrim=0:{D:.3f}[bed]"
subprocess.check_call(['ffmpeg','-v','error','-y','-filter_complex',fb,'-map','[bed]','-c:a','pcm_s16le','bed.wav'])
# duck bed under VO and mix, loudness
mix=("[0:a]asplit=2[vo][sc];[1:a][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[bd];"
     "[vo][bd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]")
subprocess.check_call(['ffmpeg','-v','error','-y','-i','vo_track.wav','-i','bed.wav','-filter_complex',mix,'-map','[o]','-ar','48000','-c:a','pcm_s16le','mix.wav'])
print('ok')
