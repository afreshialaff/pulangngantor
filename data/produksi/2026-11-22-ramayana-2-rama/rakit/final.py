import json,subprocess
R='/home/claude/pulangngantor/assets';I=f'{R}/INTRO_PULANG_NGANTOR_1080p.mp4';O=f'{R}/OUTRO_PULANG_NGANTOR_1080p.mp4'
def dur(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
T=json.load(open('timeline.json'));body=T['body'];di=103/24;do=dur(O);XI=0.5
bs=di-XI;os_=bs+body-XI;total=os_+do
norm="scale=1920:1080,setsar=1,fps=24,format=yuv420p,settb=1/24,setpts=PTS-STARTPTS"
fc=(f"[0:v]{norm}[in];[1:v]{norm}[b];[2:v]{norm}[out];"
 f"[in][b]xfade=transition=fade:duration={XI}:offset={bs:.5f}[ib];"
 f"[ib][out]xfade=transition=fadeblack:duration={XI}:offset={os_:.5f}[x];"
 f"[x]ass=subs.ass:fontsdir=/usr/share/fonts/truetype/google-fonts,format=yuv420p[v];"
 f"[0:a]loudnorm=I=-16:TP=-1.5,aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={bs:.3f}:d={XI}[ai];"
 f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st={body-XI:.3f}:d={XI},adelay={int(bs*1000)}|{int(bs*1000)}[am];"
 f"[2:a]loudnorm=I=-16:TP=-1.5,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={XI},adelay={int(os_*1000)}|{int(os_*1000)}[ao];"
 f"[ai][am][ao]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.84:level=false,aresample=48000[a]")
subprocess.check_call(['ffmpeg','-v','warning','-y','-i',I,'-i','body.mp4','-i',O,'-i','mix.wav','-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{total:.3f}',
 '-c:v','libx264','-preset','medium','-crf','20','-maxrate','5200k','-bufsize','10400k','-profile:v','high','-r','24','-g','48',
 '-c:a','aac','-b:a','192k','-movflags','+faststart','RAMAYANA_PART2_final.mp4'])
json.dump(dict(intro=di,outro=do,body=body,body_start=bs,outro_start=os_,total=total,
 chapters=[(s['id'],s['bagian'],round(bs+s['t0'],2)) for s in T['scenes']]),open('final_meta.json','w'),indent=1)
print('done',total)
