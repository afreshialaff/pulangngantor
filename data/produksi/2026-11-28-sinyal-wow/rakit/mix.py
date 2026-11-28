import subprocess, re
VO='/mnt/user-data/uploads/Downloads/SINYAL-WOW/VO_sinyal_wow.wav'; T=115.2
def ff(*a): return subprocess.run(['ffmpeg','-hide_banner','-y',*a],check=True,capture_output=True,text=True).stderr
def lufs(f):
    s=ff('-i',f,'-af','ebur128=peak=true','-f','null','-').split('Summary:')[-1]
    return float(re.search(r'I:\s+(-?[\d.]+)',s)[1]), float(re.search(r'Peak:\s+(-?[\d.]+)',s)[1])
ff('-i','music_raw.wav','-af',f'highpass=f=40,equalizer=f=2200:t=q:w=1:g=-4,acompressor=threshold=0.1:ratio=2:attack=30:release=400,apad,atrim=0:{T},afade=t=in:d=0.2,afade=t=out:st={T-1.6}:d=1.6','-ar','48000','music.wav')
ff('-i',VO,'-af',f'aresample=48000:resampler=swr,highpass=f=70,acompressor=threshold=0.2:ratio=2:attack=8:release=120,apad,atrim=0:{T},pan=stereo|c0=c0|c1=c0','-c:a','pcm_f32le','vo48.wav')
gain=-26.5-lufs('music.wav')[0]+(lufs('vo48.wav')[0]+17.8)
ff('-i','vo48.wav','-i','music.wav','-filter_complex',
 '[0:a]asplit=2[vo][sc];'f'[1:a]volume={gain:.2f}dB[m];[m][sc]sidechaincompress=threshold=0.05:ratio=2.5:attack=25:release=450[md];'
 '[md]asplit=2[md1][stem];[vo][md1]amix=inputs=2:normalize=0[o]','-map','[o]','-c:a','pcm_f32le','premix.wav','-map','[stem]','-c:a','pcm_f32le','music_ducked.wav')
g=-14.2-lufs('premix.wav')[0]
for _ in range(3):
    ff('-i','premix.wav','-af',f'aresample=192000,volume={g:.2f}dB,alimiter=limit=0.79:level=false:attack=5:release=60,aresample=48000','-c:a','pcm_s16le','mix.wav')
    I,P=lufs('mix.wav')
    if abs(I+14.2)<0.25: break
    g+=-14.2-I
v=lufs('vo48.wav')[0]; m=lufs('music_ducked.wav')[0]
print('mix',(I,P),'VO',v,'musik',m,'selisih',round(v-m,1))
