import json,sys
off=float(sys.argv[1]) if len(sys.argv)>1 else 0.0
C=json.load(open('cues.json'))
def ts(t):
    h=int(t//3600);m=int(t%3600//60);s=t%60;return f"{h}:{m:02d}:{s:05.2f}"
def srt(t):
    ms=int(round(t*1000));return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Montserrat Thin,56,&H00EEF4F7,&H000000FF,&H00101010,&H96000000,-1,0,0,0,100,100,0.5,0,1,3.2,1.6,2,200,200,72,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open('subs.ass','w') as f:
    f.write(hdr)
    for a,b,t,_ in C:
        f.write(f"Dialogue: 0,{ts(a+off)},{ts(b+off)},Sub,,0,0,0,,{{\\fad(120,120)}}{t}\n")
with open('subtitle.srt','w') as f:
    for i,(a,b,t,_) in enumerate(C,1):
        f.write(f"{i}\n{srt(a+off)} --> {srt(b+off)}\n{t.replace(chr(92)+'N',chr(10))}\n\n")
print(len(C))
