import numpy as np,subprocess,json,sys,os,cv2
exec(open('rm.py').read())
X0,Y0,S=1660,820,160;W,H=1920,1080
T=json.load(open('../asm/timeline.json'))
todo=[s for s in T['scenes']][int(sys.argv[1])::2]
for s in todo:
    out=f"clean/{s['id']}.mp4"
    if os.path.exists(out): continue
    dec=subprocess.Popen(['ffmpeg','-v','error','-i',s['clip'],'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    fps=subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=r_frame_rate','-of','csv=p=0',s['clip']]).decode().strip()
    enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',fps,'-i','-','-i',s['clip'],'-map','0:v','-map','1:a?',
        '-c:v','libx264','-preset','veryfast','-crf','12','-pix_fmt','yuv420p','-c:a','copy',out+'.tmp.mp4'],stdin=subprocess.PIPE)
    n=0
    while True:
        b=dec.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        f=np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
        f[Y0:Y0+S,X0:X0+S]=clean(f[Y0:Y0+S,X0:X0+S]);enc.stdin.write(f.tobytes());n+=1
    enc.stdin.close();enc.wait();dec.wait();os.rename(out+'.tmp.mp4',out);print(s['id'],n,flush=True)
