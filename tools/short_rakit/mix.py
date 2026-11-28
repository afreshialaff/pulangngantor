"""Mix VO + musik (ducking), loudness akhir sekitar -14 LUFS, true peak <= -1 dBTP."""
import subprocess, re, json

W = '/tmp/claude-0/-home-claude/14405b17-3b3d-5944-b753-5a30887fc6d7/scratchpad'
VO = '/mnt/user-data/outputs/VO_pareidolia_pas_klip.wav'


def ff(*a):
    return subprocess.run(['ffmpeg', '-hide_banner', '-y', *a], check=True, capture_output=True, text=True).stderr


def lufs(f):
    s = ff('-i', f, '-af', 'ebur128=peak=true', '-f', 'null', '-').split('Summary:')[-1]
    return float(re.search(r'I:\s+(-?[\d.]+)', s)[1]), float(re.search(r'Peak:\s+(-?[\d.]+)', s)[1])


# musik: potong 132 dtk, ratakan dinamika, setel ke -27 LUFS sebelum ducking
ff('-i', f'{W}/music_raw.wav', '-af',
   'highpass=f=45,equalizer=f=2200:t=q:w=1:g=-4,acompressor=threshold=0.08:ratio=2.5:attack=30:release=400,'
   'apad,atrim=0:132,afade=t=in:d=0.15,afade=t=out:st=130.2:d=1.8', '-ar', '48000', f'{W}/music.wav')
gain = -23.8 - lufs(f'{W}/music.wav')[0]
ff('-i', VO, '-i', f'{W}/music.wav', '-filter_complex',
   '[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[vo][sc];'
   f'[1:a]volume={gain:.2f}dB[m];[m][sc]sidechaincompress=threshold=0.05:ratio=2.5:attack=30:release=500[md];'
   '[md]asplit=2[md1][stem];[vo][md1]amix=inputs=2:normalize=0[o]',
   '-map', '[o]', '-c:a', 'pcm_f32le', f'{W}/premix.wav', '-map', '[stem]', f'{W}/music_ducked.wav')
g = -14.2 - lufs(f'{W}/premix.wav')[0]
ff('-i', f'{W}/premix.wav', '-af',
   f'aresample=192000,volume={g:.2f}dB,alimiter=limit=0.79:level=false:attack=5:release=60,aresample=48000',
   '-c:a', 'pcm_s16le', f'{W}/mix.wav')
vo_i = lufs(VO)[0]
mu_i = lufs(f'{W}/music_ducked.wav')[0]
print('mix', lufs(f'{W}/mix.wav'), 'VO', vo_i, 'musik setelah ducking', mu_i, 'selisih', round(vo_i - mu_i, 1))
