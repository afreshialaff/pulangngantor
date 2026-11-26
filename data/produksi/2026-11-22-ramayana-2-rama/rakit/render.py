import json,subprocess,os
T=json.load(open('timeline.json'));A=json.load(open('align.json'));S=T['scenes'];X=T['X'];FPS=24
os.makedirs('seg',exist_ok=True);os.makedirs('part',exist_ok=True)
ENC=['-c:v','libx264','-preset','veryfast','-crf','13','-pix_fmt','yuv420p','-r','24','-video_track_timescale','12288','-an']
NORM="scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
def run(a): subprocess.check_call(['ffmpeg','-v','error','-y']+a)
def frames(p): return int(subprocess.check_output(['ffprobe','-v','error','-count_packets','-select_streams','v','-show_entries','stream=nb_read_packets','-of','csv=p=0',p]).decode().strip().strip(','))
for s in S:
    out=f"seg/{s['id']}.mp4";L=s['L']
    if os.path.exists(out) and frames(out)==L: continue
    if s['id']=='S31':
        # tahan bingkai pertama (zoom pelan) sampai narasi 'patah', lalu ledakan busur
        w=[w for w in A['S31']['words'] if w[0].startswith('patah')][0]
        wb=[w for w in A['S31']['words'] if w[0]=='Busur'][0]
        tb=(s['vo_at']-s['t0'])+(wb[1]-s['vo_start'])+0.35
        n1=int(round(tb*FPS));n2=L-n1;use=6.4;f=max(1.0,n2/FPS/use)
        fc=(f"[0:v]select='eq(n,0)',scale=3840:2160,zoompan=z='1+0.07*on/{n1}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n1}:s=1920x1080:fps=24,format=yuv420p,setsar=1[a];"
            f"[1:v]trim=0:{use},setpts=(PTS-STARTPTS)*{f},minterpolate=fps=24:mi_mode=blend,{NORM},trim=end_frame={n2},setpts=PTS-STARTPTS[b];"
            f"[a][b]concat=n=2:v=1:a=0,tpad=stop_mode=clone:stop_duration=2[v]")
        run(['-i',s['clip'],'-i',s['clip'],'-filter_complex',fc,'-map','[v]','-frames:v',str(L)]+ENC+[out])
        s2=tb
    else:
        vf=NORM
        if s['stretch']>1.001: vf=f"setpts=PTS*{s['stretch']},"+("minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1," if s['stretch']>1.08 else "")+vf
        vf+=",fps=24,tpad=stop_mode=clone:stop_duration=2"
        run(['-i',s['clip'],'-vf',vf,'-frames:v',str(L)]+ENC+[out])
    assert frames(out)==L,(s['id'],frames(out),L)
    print(s['id'],L,flush=True)
# bagian: badan tiap adegan + transisi antar adegan
lst=[]
for i,s in enumerate(S):
    head=0 if i==0 else X;mid_end=s['sf'];p=f"part/{i:02d}a.mp4"
    run(['-i',f"seg/{s['id']}.mp4",'-vf',f"trim=start_frame={head}:end_frame={mid_end},setpts=PTS-STARTPTS"]+ENC+[p]);lst.append(p);assert frames(p)==mid_end-head
    if i<len(S)-1:
        n=S[i+1];p=f"part/{i:02d}b.mp4";tr=s['trans'][0]
        fc=(f"[0:v]trim=start_frame={s['sf']}:end_frame={s['L']},setpts=PTS-STARTPTS,settb=1/24[a];"
            f"[1:v]trim=start_frame=0:end_frame={X},setpts=PTS-STARTPTS,settb=1/24[b];"
            f"[a][b]xfade=transition={tr}:duration={(X-0.5)/24:.5f}:offset=0[v]")
        run(['-i',f"seg/{s['id']}.mp4",'-i',f"seg/{n['id']}.mp4",'-filter_complex',fc,'-map','[v]','-frames:v',str(X)]+ENC+[p]);lst.append(p);assert frames(p)==X,(p,frames(p))
open('concat.txt','w').write(''.join(f"file '{p}'\n" for p in lst))
run(['-f','concat','-safe','0','-i','concat.txt','-c','copy','body.mp4'])
print('body frames',frames('body.mp4'),T['frames'])
