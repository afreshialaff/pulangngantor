"""Backsound orisinal tema misteri angkasa (MIDI -> FluidSynth + FluidR3 GM)."""
import pretty_midi as pm, subprocess, random
random.seed(1977)
T=115.2; BPM=80; B=60/BPM
mid=pm.PrettyMIDI(initial_tempo=BPM)
def inst(program, vol, pan=64, drum=False, rev=90):
    i=pm.Instrument(program=program,is_drum=drum)
    i.control_changes+=[pm.ControlChange(7,vol,0),pm.ControlChange(10,pan,0),pm.ControlChange(91,rev,0)]
    mid.instruments.append(i); return i
pad=inst(89,60); halo=inst(94,48,50); space=inst(91,50,78); strg=inst(48,50,60); cello=inst(42,52,48)
cel=inst(8,55,40); vib=inst(11,52,84); box=inst(10,46,70); glk=inst(9,48,80); harp=inst(46,56,52)
bass=inst(38,52,64,rev=40); sub=inst(39,48,64,rev=30); beep=inst(80,30,90); timp=inst(47,70)
piano=inst(0,62,58); drm=inst(0,50,drum=True,rev=50); rise=inst(119,55)
def note(i,p,t,d,v=70):
    if t>=T: return
    i.notes.append(pm.Note(int(max(1,min(127,v+random.randint(-3,3)))),p,max(0,t),min(T,t+d)))
def chord(i,ps,t,d,v=50):
    for p in ps: note(i,p,t,d,v)
def signal(t,v=50,p=86):   # motif "sinyal": titik-titik radio
    for k,(o,d) in enumerate([(0,.09),(.18,.09),(.36,.22),(.74,.09),(.92,.32)]):
        note(beep,p if k!=4 else p+5,t+o,d,v-k*2)
def bars(a,b,prog,beats=4):
    t,k=a,0
    while t<b-0.1:
        d=min(beats*B,b-t); yield t,d,prog[k%len(prog)],k; t+=d; k+=1
Am=(33,[57,60,64,71]); F=(29,[53,57,60,64]); Dm=(26,[50,53,57,64]); E=(28,[52,56,59,64]); C=(36,[55,60,64,67]); G=(31,[55,59,62,69]); Bb=(34,[53,58,62,65])
def hit(t,v=80,root=33):
    note(timp,root+12,t,1.8,v); chord(glk,[81,88,93],t,1.4,v-18); chord(harp,[57,64,69,76],t,1.6,v-14)

# 1) S01 0-12: hook, dengung + sinyal, puncak di "Wow!" 11.37
chord(pad,[33,45,52,57],0,12.0,54); chord(space,[64,71],0.2,5.8,40); chord(space,[65,72],6.1,5.2,44)
signal(0.15,58); signal(3.0,42); signal(6.2,52,88)
for t,p in [(1.4,76),(2.2,81),(4.4,83),(5.2,79),(7.6,76),(8.4,81),(9.2,84),(10.0,88)]: note(cel,p,t,1.2,52)
t=6.0; k=0
while t<10.9:
    note(sub,33,t,0.22,40+k*3); t+=B/2; k+=1
note(rise,60,9.8,1.5,60); hit(11.37,88)

# 2) S02-S03 12-26.9: penasaran, arpeggio ringan
for t,d,(r,ch),k in bars(12.0,26.89,[Am,F,Dm,E]):
    chord(pad,ch[:3],t,d,36); note(bass,r+12,t,0.5,56); note(bass,r+12,t+2.5*B,0.3,44)
    for j,s in enumerate([0,1,2,3,2,1,2,1]):
        if j*B/2<d-0.1: note(harp,ch[s]+12,t+j*B/2,0.35,44 if j%2 else 54)
    if k%2: note(vib,ch[3]+12,t+2*B,1.2,40)
    for j in range(8):
        if j*B/2<d-0.05: note(drm,42,t+j*B/2,0.06,18 if j%2==0 else 12)

# 3) S04 26.9-36.1: tegang menuju "Wow!" 35.23
chord(pad,[33,45,52],26.89,8.3,48); chord(strg,[64,65],29.0,3.8,34); chord(strg,[65,68],32.8,2.4,44)
t=26.95; k=0
while t<34.9:
    note(sub,33,t,0.16,36+k); note(drm,37,t+B/2,0.05,14+k//2); t+=B; k+=1
for k,t in enumerate([29.02,29.77,31.07,31.65,32.34,32.7]): note(cel,[76,79,81,83,84,88][k],t,0.5,58)
note(rise,62,33.9,1.3,66); hit(35.23,98); chord(strg,[57,64,69,72],35.25,1.2,60)

# 4) S05-S07 36.1-61.4: penjelasan, mengalir
for t,d,(r,ch),k in bars(36.1,61.44,[Am,F,C,G]):
    chord(pad,ch,t,d,34); note(bass,r+12,t,0.7,58); note(bass,r+19,t+2*B,0.4,44); note(bass,r+12,t+3*B,0.4,40)
    for j,s in enumerate([0,2,1,3,2,0,3,1]):
        if j*B/2<d-0.1: note(vib if t<52.5 else harp,ch[s]+12,t+j*B/2,0.3,42 if j%2 else 52)
    note(drm,36,t,0.1,36); 
    for j in range(8):
        if j*B/2<d-0.05: note(drm,70,t+j*B/2,0.06,20 if j%2 else 12)
    if k%2==1: note(cel,ch[3]+12,t+3*B,0.8,42)
signal(43.7,38); signal(52.7,36,83)
chord(halo,[69,76],52.55,8.9,40)

# 5) S08-S10 61.4-83.5: sepi, mencari; hening di "Sunyi" 74.66
for t,d,(r,ch),k in bars(61.44,73.7,[Dm,Am,Bb,E],beats=4):
    chord(pad,ch[:3],t,d,36); note(cello,r+12,t,d*0.95,44)
    for j,s in enumerate([3,2,1]):
        if j*1.25*B<d-0.2: note(box,ch[s]+12,t+(0.25+j*1.25)*B,1.0,46)
    note(drm,75,t+2*B,0.05,22)
signal(67.4,34,81)
chord(pad,[45,52],73.7,1.0,26)
note(piano,76,74.75,1.2,34)
for t,d,(r,ch),k in bars(75.5,83.47,[Am,F,Dm,E]):
    chord(pad,ch[:3],t,d,34); note(bass,r+12,t,0.5,52)
    for j,s in enumerate([0,1,2,3,2,1]):
        if j*B/2<d-0.1: note(harp,ch[s]+12,t+j*B/2,0.35,44)
    for j in range(4):
        if j*B<d-0.05: note(drm,76 if j%2 else 77,t+j*B+B/2,0.06,22)

# 6) S11-S12 83.5-98.9: dugaan, berkilau lalu membesar
for t,d,(r,ch),k in bars(83.47,88.77,[Dm,E]):
    chord(pad,ch[:3],t,d,36); note(bass,r+12,t,0.4,50)
    for j in range(4):
        if j*B<d-0.1: note(vib,ch[(j*3)%4]+12,t+j*B,0.35,44)
for t,d,(r,ch),k in bars(88.77,98.93,[F,G,Am,E]):
    chord(halo,[p+12 for p in ch[1:]],t,d,36+k*5); chord(pad,ch,t,d,38); note(sub,r+12,t,1.4,48)
    for j,s in enumerate([0,1,2,3,0,1,2,3]):
        if j*B/2<d-0.1: note(cel,ch[s]+24,t+j*B/2,0.3,32+k*5)
note(rise,57,92.2,1.2,48); hit(92.6,58)

# 7) S13 98.9-107: renungan (piano)
for t,d,(r,ch),k in bars(98.93,106.95,[F,C,Dm,E]):
    chord(pad,ch[:3],t,d,30); note(piano,r+12,t,d,48)
    for j,s in enumerate([1,2,3]):
        if (j+1)*B<d: note(piano,ch[s]+12,t+(j+1)*B*0.9,1.0,44)

# 8) S14 107-115.2: kembali ke sinyal, penutup lapang
chord(pad,[33,45,52,59,64],106.95,8.25,48); chord(strg,[57,64,71],108.4,6.8,36); chord(halo,[72,76],110.9,4.3,40)
signal(107.0,44); signal(109.9,36,83)
for j,p in enumerate([69,72,76,83,81]): note(cel,p,110.9+j*0.45,1.4,48)
signal(113.95,50); hit(113.95,52)

mid.write('music.mid')
subprocess.run(['fluidsynth','-ni','-g','0.6','-r','48000','-F','music_raw.wav','/usr/share/sounds/sf2/FluidR3_GM.sf2','music.mid'],check=True,capture_output=True)
