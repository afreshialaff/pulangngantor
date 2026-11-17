import json,subprocess
R='/home/claude/pulangngantor'
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
T=json.load(open('timeline.json'));S=T['scenes']
# actual offsets
o=0.0
for i,s in enumerate(S):
    s['seg_actual']=dur(f'seg/{s["id"]}.mp4'); s['t0']=round(o,3); s['vo_at']=round(o+T['LEAD'],3)
    if i<25: o+=s['seg_actual']-s['trans'][1]
body=o+S[-1]['seg_actual'];T['body']=body
json.dump(T,open('timeline.json','w'),ensure_ascii=False,indent=1)
print('body',body)
subprocess.check_call(['python3','audio.py']); subprocess.check_call(['python3','subs.py'],stdout=subprocess.DEVNULL)
INTRO=f'{R}/assets/INTRO_PULANG_NGANTOR_1080p.mp4';OUTRO=f'{R}/assets/OUTRO_PULANG_NGANTOR_1080p.mp4'
di,do=dur(INTRO),dur(OUTRO);XI=0.5
bstart=di-XI; ostart=bstart+body-XI
subprocess.check_call(['python3','ass.py',str(bstart)])
norm="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p,settb=1/24"
ins=['-i',INTRO]+sum([['-i',f'seg/{s["id"]}.mp4'] for s in S],[])+['-i',OUTRO,'-i','mix.wav']
fc=f"[0:v]{norm}[in];[27:v]{norm}[out];"
for i in range(26): fc+=f"[{i+1}:v]settb=1/24,setpts=PTS-STARTPTS[s{i}];"
prev='s0'
for i in range(25):
    tr,X=S[i]['trans'];off=S[i+1]['t0']
    fc+=f"[{prev}][s{i+1}]xfade=transition={tr}:duration={X}:offset={off:.4f}[b{i}];";prev=f'b{i}'
fc+=f"[in][{prev}]xfade=transition=fade:duration={XI}:offset={di-XI:.4f}[ib];"
fc+=f"[ib][out]xfade=transition=fadeblack:duration={XI}:offset={ostart:.4f}[full];"
fc+=f"[full]ass=subs.ass:fontsdir=/root/.fonts,format=yuv420p[v];"
fc+=(f"[0:a]loudnorm=I=-16:TP=-1.5,aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st={di-XI:.3f}:d={XI}[ai];"
     f"[28:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.3,adelay={int(bstart*1000)}|{int(bstart*1000)}[am];"
     f"[27:a]loudnorm=I=-16:TP=-1.5,aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d={XI},adelay={int(ostart*1000)}|{int(ostart*1000)}[ao];"
     f"[ai][am][ao]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.89[a]")
open('fc.txt','w').write(fc)
total=ostart+do
cmd=['ffmpeg','-v','warning','-stats_period','30','-y']+ins+['-filter_complex_script','fc.txt','-map','[v]','-map','[a]','-t',f'{total:.3f}',
     '-c:v','libx264','-preset','medium','-crf','18','-tune','film','-profile:v','high','-pix_fmt','yuv420p','-r','24','-g','48',
     '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','out_video.mp4']
print(' '.join(cmd))
subprocess.check_call(cmd)
json.dump(dict(intro=di,outro=do,body=body,body_start=bstart,outro_start=ostart,total=total,
  chapters=[(s['id'],round(bstart+s['t0'],2),s['bagian'],s['label']) for s in S]),open('final_meta.json','w'),indent=1)
print('done',total)
