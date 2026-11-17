import json,subprocess,sys,os
TL=json.load(open('timeline.json'))['scenes']
VID='/mnt/user-data/uploads/VONYCH/VID'
BEB=os.path.expanduser('~/.fonts/BebasNeue-Regular.ttf');MON=os.path.expanduser('~/.fonts/Montserrat-700.ttf')
def qc(path,L):
    o=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,r_frame_rate,pix_fmt','-of','json',path]))
    d=float(o['format']['duration']);st=o['streams'][0]
    bd=subprocess.run(['ffmpeg','-v','info','-i',path,'-vf','blackdetect=d=0.3:pix_th=0.06','-an','-f','null','-'],capture_output=True,text=True).stderr
    blacks=[l for l in bd.splitlines() if 'black_start' in l]
    ok=abs(d-L)<0.1 and st['width']==1920 and st['height']==1080 and not blacks
    return dict(dur=round(d,3),want=L,size=f"{st['width']}x{st['height']}",fps=st['r_frame_rate'],black=len(blacks),ok=ok)
res={}
for s in TL:
    if len(sys.argv)>1 and s['id'] not in sys.argv[1:]: continue
    n=int(s['id'][1:]);src=f'{VID}/S{n}.mp4'
    open(f'seg/{s["id"]}_k.txt','w').write(s['bagian'].upper())
    open(f'seg/{s["id"]}_l.txt','w').write(s['label'])
    a0,a1=0.9,5.2
    al=f"if(lt(t,{a0}),0,if(lt(t,{a0+0.35}),(t-{a0})/0.35,if(lt(t,{a1-0.4}),1,if(lt(t,{a1}),({a1}-t)/0.4,0))))"
    xs=f"(110-40*(1-min(1,max(0,(t-{a0})/0.35))))"
    vf=(f"setpts=PTS*{s['stretch']},fps=24,scale=1920:1080:flags=lanczos,setsar=1,"
        f"eq=contrast=1.05:saturation=0.94:gamma=0.98,vignette=angle=PI/5,"
        f"drawbox=x=78:y=78:w=8:h=128:color=0x8B1E1E@1:t=fill:enable='between(t,{a0},{a1})',"
        f"drawtext=fontfile={MON}:textfile=seg/{s['id']}_k.txt:fontsize=26:fontcolor=0xF4A259:alpha='{al}':x='{xs}':y=86:shadowcolor=black@0.7:shadowx=2:shadowy=2,"
        f"drawtext=fontfile={BEB}:textfile=seg/{s['id']}_l.txt:fontsize=92:fontcolor=0xE9D9C5:alpha='{al}':x='{xs}':y=118:shadowcolor=black@0.75:shadowx=3:shadowy=3,"
        f"noise=alls=4:allf=t,format=yuv420p")
    out=f'seg/{s["id"]}.mp4'
    subprocess.check_call(['ffmpeg','-v','error','-y','-i',src,'-an','-vf',vf,'-t',str(s['seg_len']),'-c:v','libx264','-crf','14','-preset','fast','-r','24',out])
    subprocess.check_call(['ffmpeg','-v','error','-y','-ss','2.4','-i',out,'-frames:v','1','-vf','scale=640:-1',f'seg/{s["id"]}_qc.jpg'])
    r=qc(out,s['seg_len']);res[s['id']]=r;print(s['id'],r,flush=True)
    json.dump(res,open(f'seg/{s["id"]}_qc.json','w'))
