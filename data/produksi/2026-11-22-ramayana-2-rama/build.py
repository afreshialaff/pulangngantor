import json,math,sys
from vo import VO; from img import S,CHAR,STYLE; from motion import M
assert list(M)==[v[0] for v in VO]
dur_file=sys.argv[1] if len(sys.argv)>1 else None
D=json.load(open(dur_file)) if dur_file else None
def est(v): return min(15,max(4,math.ceil(len(v.split())/135*60+0.8)))
NEG=("Avoid: cuts, scene change, shaky camera, fast zoom, morphing, warping faces, changing costumes or hairstyle, extra or missing fingers or limbs, duplicated or new characters, objects appearing or vanishing without cause, lip-sync talking mouths, text, subtitles, letters, watermark, logo, photorealistic live-action look, 2D anime look, flicker, blur, gore, blood, modern objects.")
def clean(c):
    c=c.split(', gentle')[0]
    for a in [", wooden longbow and a quiver on his back",", bow and quiver",", a large iron battle axe, a great ancient bow"," and one peacock-free lotus ornament"]: c=c.replace(a,"")
    return c
out=["# Prompt video Ramayana Part 2 (Rama), Nexabot: Start Frame to Video, Landscape 16:9, 1080p",
 "Durasi "+("DIUKUR dari VO asli (dibulatkan ke atas)." if D else "SEMENTARA (perkiraan 135 kata/menit); akan diganti setelah VO diukur."),"",
 "| Scene | Durasi klip | VO |","|---|---|---|"]
tot=0; rows=[]; blocks=[]
for sid,bag,kls,vo in VO:
    d=D[sid]["klip"] if D else est(vo); tot+=d
    rows.append(f"| {sid} | {d} dtk | {vo} |")
    cam,a,b,c=M[sid]; chars,scene=S[sid]; t1=round(d/3,1); t2=round(2*d/3,1)
    chars=[] if sid in ("S13","S14") else chars
    look=" ".join(f"{k.replace('_KECIL',' (child)').title()}: {clean(CHAR[k])}." for k in chars)
    blocks.append(f"## {sid} ({d} dtk) · {bag}\n```\n{sid} RAMA PART 2. Image-to-video, exactly {d} seconds, 16:9 landscape, 1080p, 24 fps. The attached image is the exact first frame: keep every character, face, costume, prop, colour and background identical for the whole clip.\nScene: {scene}.\n"
      +(f"Character consistency (exactly as drawn in the first frame): {look}\n" if look else "")
      +f"Camera: {cam}. One continuous shot, smooth and stable.\n0 to {t1} s: {a}.\n{t1} to {t2} s: {b}.\n{t2} to {d} s: {c}.\nStyle: smooth stylized 3D animated feature film, soft natural motion at a calm storytelling pace, gentle secondary motion on hair, cloth, light and particles, rich warm gold and sapphire colours. Do not add any new character, weapon or object that is not already visible in the first frame; anything hand-held stays in the same hands with the same shape. Mouths stay closed or nearly still; no dialogue. Audio: soft ambient sound only, no speech, no singing.\n{NEG}\n```\n")
out+=rows+["",f"Total durasi klip: {tot} dtk ({tot//60} mnt {tot%60} dtk), {len(VO)} scene.",""]+blocks
open("prompt_video.md","w",encoding="utf-8").write("\n".join(out))
print(tot, max(len(x) for x in blocks))
