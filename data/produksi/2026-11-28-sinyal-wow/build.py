#!/usr/bin/env python3
"""Bangun paket teks Short Sinyal Wow! dari satu sumber. Pakai: python build.py [cuts.json]"""
import json, math, os, sys

STYLE = ("detailed 2D animated feature-film illustration, clean line art, soft cel shading with painterly "
         "detail, rich harmonious colors (deep midnight navy, warm amber, crimson accent, cream, teal), "
         "highly detailed layered background with depth, vertical 9:16, main subject centered, keep top 10% "
         "and bottom 18% free of important details, no text, no letters, no numbers, no captions, no logo, no watermark")
CHARS = {
 "CHAR_RAKA": "friendly young Indonesian office worker guide, 25 years old, short tousled black hair, round dark eyes, warm brown skin, cream shirt with loosened crimson tie, navy jacket, dark trousers, white sneakers, expressive face",
 "CHAR_ASTRO": "fictional 1970s radio astronomer (not a portrait of any real person), middle-aged man, wavy light brown hair, square brown glasses, mustard knitted vest, cream collared shirt, brown trousers, red pen in his pocket",
 "CHAR_BIGEAR": "environment reference: huge Kraus-type radio telescope on a flat grassy field, a wide flat metal ground plane, a tall tilting flat mesh reflector at one end, a tall curved parabolic mesh reflector at the other end, and a small hut with two horn-shaped receivers",
}
NEG = ("Negative: no morphing, no warping, no melting lines, no extra limbs or fingers, no duplicated characters, "
       "no new characters or objects, no face change, no style change, no 3D or photorealism, no flicker, no sudden "
       "zoom, no spinning camera, no scene transition, no dissolve, no crossfade, no double exposure, no text, no "
       "letters, no numbers, no subtitles, no logo, no watermark.")
# id, judul, refs, vo, gambar, kamera, aksi (3 tahap), kelas, sumber
S = [
("S01","Hook",["CHAR_ASTRO","CHAR_BIGEAR"],
 "Katanya, ada sinyal luar angkasa yang artinya Wow. Eits, salah! Tahun seribu sembilan ratus tujuh puluh tujuh, sinyal aneh tertangkap, dan astronom yang kaget mencoret kertasnya: Wow!",
 "Starry night over CHAR_BIGEAR. A thin glowing amber beam of radio waves descends from one bright point in the sky onto the telescope. In the foreground CHAR_ASTRO holds a long continuous paper printout, eyes wide and mouth open in amazement.",
 "Slow gentle push-in from the wide sky toward the astronomer",
 ["stars twinkle softly and one small pulse of light glides down the existing amber beam to its lower end","the astronomer raises the printout a little as its long paper tail sways, his eyes widen and he blinks","a soft amber glint crosses his glasses and he holds the same amazed pose"],"fakta",["ehman"]),
("S02","Big Ear",["CHAR_RAKA","CHAR_BIGEAR"],
 "Teleskopnya bernama Big Ear, alias Telinga Raksasa, di Ohio, Amerika. Ia nggak melihat bintang. Ia mendengarkan gelombang radio.",
 "Golden dusk over CHAR_BIGEAR seen from a gentle high angle, tiny figures of CHAR_RAKA in the foreground cupping a hand behind his ear. Soft concentric teal wave arcs flow from the sky into the tall curved reflector.",
 "Smooth gentle sideways glide with a slight push-in",
 ["grass sways, clouds drift slowly and the teal wave arcs ripple gently","the existing teal wave arcs flow one after another into the tall curved reflector on the right","Raka keeps one hand cupped at his ear, tilts his head, smiles wider and nods once while stars twinkle"],"fakta",["ehman"]),
("S03","Cetakan",["CHAR_ASTRO"],
 "Malam lima belas Agustus, komputer mencatat semuanya di kertas. Beberapa hari kemudian, Jerry Ehman memeriksa tumpukan cetakan itu.",
 "Cozy 1970s study room. CHAR_ASTRO sits at a wooden desk reading a tall stack of folded continuous printer paper with perforated edges, covered only with tiny abstract dots. Green desk lamp, coffee mug, reel-to-reel tape computer cabinets and a window with night sky behind.",
 "Gentle push-in toward the astronomer and his printout",
 ["the lamp light glows warmly and he draws the continuous paper slowly through both hands, reading","his eyes move across one line from left to right and the paper folds sway slightly","he leans a little closer to the paper, narrows his eyes with focus and holds"],"fakta",["ehman"]),
("S04","Lingkaran merah",["CHAR_ASTRO"],
 "Matanya berhenti di kode: enam, E, Q, U, J, lima. Dilingkari pena merah, lalu ditulis: Wow!",
 "Close-up top view of a continuous printout on a desk with a wide blank cream area in the center and tiny abstract dots around it. The hand of CHAR_ASTRO holds a red pen and has just drawn a bold empty red oval around the blank area. Warm lamp light.",
 "Very slow push-in toward the red oval",
 ["the hand with the red pen rests near the top of the existing red oval while lamp light glows","the pen tip glides slowly a short way along the existing red line, adding no new marks","the hand lifts the pen slightly off the paper and holds still; the inside of the oval stays completely blank"],"fakta",["ehman"]),
("S05","Kekuatan",["CHAR_RAKA"],
 "Itu bukan pesan rahasia. Huruf dan angka itu ukuran kekuatan sinyal. Puncaknya sekitar tiga puluh kali lebih kuat dari bising latar.",
 "CHAR_RAKA stands beside a giant glowing bar chart made of plain colored blocks without labels: many tiny grey blocks and one set of six blocks rising and falling like a mountain, the tallest bright amber. He points up at the tallest block. Dark teal studio with soft particles.",
 "Slow gentle vertical tilt from the small grey blocks up to the tallest amber block",
 ["the small grey blocks shimmer softly while background particles float; every block keeps its size and position","the colored blocks brighten softly one after another from left to right","the tallest amber block glows a little brighter in a steady soft way with no burst, no explosion, no glowing orb, no lightning and no flying sparks; Raka keeps pointing at it, glances up and smiles impressed"],"fakta",["ehman"]),
("S06","Saluran hidrogen",["CHAR_RAKA"],
 "Frekuensinya dekat seribu empat ratus dua puluh megahertz, nada alami atom hidrogen. Ilmuwan pernah mengusulkan: alien mungkin memilih saluran ini untuk menyapa.",
 "Deep space scene with a large stylized glowing hydrogen atom, one small electron on a ring, emitting soft concentric teal waves. CHAR_RAKA floats beside it holding a vintage radio and turning its knob. Nebula clouds and many stars.",
 "Slow gentle drift and slight push-in from the atom toward Raka and the radio",
 ["the single electron travels slowly along its existing ring and the teal waves pulse outward","Raka floats gently and turns the radio knob with small finger movements as the radio dial glows amber","he tilts his head slightly, listening with a curious smile, tie floating softly"],"fakta",["ehman","cocconi"]),
("S07","72 detik",["CHAR_BIGEAR"],
 "Sinyalnya naik lalu turun selama tujuh puluh dua detik. Pas dengan sapuan teleskop saat Bumi berputar. Artinya, sumbernya tampak ikut bergerak bersama langit.",
 "Beautiful view of the curved edge of Earth at night with CHAR_BIGEAR small on its surface, projecting a soft teal listening beam into the starry sky. The beam passes across one bright amber point. A glowing smooth bell-shaped curve of light floats in the sky.",
 "Very slight slow pull-back over the curve of the Earth",
 ["the teal beam sweeps slowly toward the bright amber star as the Earth rotates very slightly","the beam passes across the star, the star grows only a little brighter and the bell-shaped curve of light brightens softly at its peak, with no burst, no explosion and no lens flare","the beam moves just past the star and both star and curve dim gently"],"fakta",["ehman"]),
("S08","Dua corong",["CHAR_RAKA"],
 "Anehnya, Big Ear punya dua corong penerima. Kalau sumbernya terus menyala, harusnya tertangkap dua kali. Ternyata cuma sekali.",
 "Inside the receiver hut: two large metal horn-shaped receivers side by side. The left horn glows with a bright amber wave entering it, the right horn is completely dark and quiet. CHAR_RAKA stands between them scratching his head, puzzled.",
 "Very slight smooth pan from the left horn toward the right horn",
 ["amber light waves swirl continuously into the left horn only","the right horn stays completely dark, empty and silent while Raka glances from the left horn to the right","Raka slowly scratches his head, raises his eyebrows and gives a small puzzled shrug; the amber light stays only on the left"],"fakta",["ehman"]),
("S09","Sagitarius",["CHAR_ASTRO","CHAR_BIGEAR"],
 "Arahnya dari rasi Sagitarius. Big Ear mengecek lokasi itu lebih dari lima puluh kali. Hasilnya? Sunyi.",
 "Rich Milky Way core sky with a subtle constellation drawn as thin glowing lines shaped like a teapot, one empty soft circle marking a spot beside it. Below, CHAR_ASTRO with headphones sits on the grass near CHAR_BIGEAR, looking disappointed.",
 "Slow gentle tilt from the seated astronomer up to the constellation",
 ["the seated astronomer stays still with his headphones, blinks and tilts his head slightly, listening","the existing constellation lines glow softly one after another; the shape does not change","the single marked circle stays empty and dim while the astronomer lowers his eyes, disappointed"],"fakta",["ehman","gray_wiki"]),
("S10","Perburuan",["CHAR_RAKA"],
 "Peneliti lain ikut berburu, pakai teleskop di Amerika dan Australia. Tahun dua ribu dua puluh dua, satu bintang kandidat ikut disimak. Tetap kosong.",
 "Wide night landscape with several large white dish radio antennas on desert hills all pointing at one small warm yellow star. CHAR_RAKA in the foreground looks through binoculars. Colorful twilight horizon.",
 "Gentle slow push-in toward Raka with soft parallax between hills and dishes",
 ["the dishes stay in place while the small yellow star twinkles; Raka holds the binoculars to his eyes","Raka turns the binoculars very slightly left and then right, searching","he holds still, the smile fades into a small disappointed sigh and his shoulders drop a little; the binoculars stay over his eyes"],"fakta",["gray","bl2022"]),
("S11","Komet?",["CHAR_RAKA"],
 "Ada yang menduga komet. Tapi sejumlah astronom menolak: posisi dan perilakunya dinilai nggak cocok.",
 "A glowing icy comet with a long teal tail crossing a starry sky. CHAR_RAKA stands on a hill holding up two crossed arms in an X gesture with a friendly skeptical face. Silhouette of pine trees.",
 "Slow gentle push-in toward Raka with the comet drifting behind him",
 ["the comet glides slowly across the sky and its tail shimmers","Raka keeps his arms crossed in an X, glances toward the comet and raises one eyebrow","he looks back at the viewer and shakes his head gently with a small skeptical smile"],"klaim",["comet"]),
("S12","Awan hidrogen",["CHAR_RAKA"],
 "Hipotesis baru tahun dua ribu dua puluh empat: awan hidrogen dingin mendadak terang akibat semburan magnetar, bintang supermagnet. Menarik, tapi belum terbukti.",
 "Spectacular deep space: a small dense star with curved magnetic field lines sends a burst of light toward a soft blue hydrogen cloud, which glows brightly and sends a narrow amber ray toward a tiny distant Earth. CHAR_RAKA floats in a corner holding a magnifying glass.",
 "Slow gentle pan from the magnetic star toward the glowing cloud with a slight push-in",
 ["the magnetic star pulses and its field lines shimmer as light streams along the existing burst","the blue cloud brightens softly from within","one pulse of light travels along the existing amber ray to the tiny Earth while Raka floats gently, glances up and keeps holding his magnifying glass"],"dugaan",["arecibo1","arecibo2"]),
("S13","Belum pasti",["CHAR_RAKA","CHAR_ASTRO"],
 "Jadi, alien? Belum ada buktinya. Sebab alami? Juga belum pasti. Ehman sendiri bilang, datanya terlalu sedikit.",
 "A balanced scale in a warm observatory room: on one side a small cute generic glowing flying saucer toy, on the other a small glowing blue cloud. CHAR_RAKA and CHAR_ASTRO stand on either side thinking with hands on chins.",
 "Gentle slow push-in toward the balanced scale",
 ["the scale tips only a few millimeters toward the saucer toy; chains stay straight and attached","it tips only a few millimeters toward the cloud while both characters follow it with their eyes","it settles level; both keep hands on chins, raise their eyebrows and tilt their heads thoughtfully"],"fakta",["ehman"]),
("S14","Penutup",["CHAR_RAKA","CHAR_BIGEAR"],
 "Tujuh puluh dua detik, lalu hening hampir lima puluh tahun. Menurutmu itu apa? Tulis tebakanmu di komentar!",
 "CHAR_RAKA sits on a hill under a magnificent starry sky wearing headphones, smiling at the viewer and pointing upward. CHAR_BIGEAR silhouette in the distance, one bright amber star above.",
 "Very slight slow pull-back from Raka toward the whole sky",
 ["he sits relaxed with headphones, blinks and nods softly while small stars twinkle","the amber star twinkles a little brighter and settles, with no burst","he smiles warmly at the viewer, keeps pointing upward and holds the pose"],"narasi",["ehman"]),
]
SUMBER = {
 "ehman":("Jerry R. Ehman, laporan 30 tahun, Big Ear (rev. 2010)","https://www.bigear.org/Wow30th/wow30th.htm"),
 "cocconi":("Cocconi & Morrison (1959), Searching for Interstellar Communications, salinan di Big Ear","https://www.bigear.org/vol1no1/interste.htm"),
 "gray":("Seth Shostak (2002) tentang pencarian Gray, salinan di Big Ear","https://bigear.org/shostak_wow_20021205.htm"),
 "gray_wiki":("Planetary Society (2012), ulasan buku Robert Gray","https://www.planetary.org/articles/3346"),
 "bl2022":("Breakthrough Listen (2022)","https://seti.berkeley.edu/wow"),
 "comet":("PHL UPR Arecibo, keberatan atas hipotesis komet","https://phl.upr.edu/wow/comet"),
 "arecibo1":("Méndez dkk. (2024), Arecibo Wow! I, pracetak","https://arxiv.org/pdf/2408.08513"),
 "arecibo2":("Méndez dkk. (2025), Arecibo Wow! II, draf pracetak","https://arxiv.org/pdf/2508.10657"),
}
YAKIN = {"fakta":"didukung","dugaan":"spekulatif","klaim":"diperdebatkan","narasi":"-"}

def tulis(n, t):
    open(n, "w", encoding="utf-8").write(t.rstrip() + "\n")

kata = sum(len(s[3].split()) for s in S)
if len(sys.argv) > 1:
    cuts = json.load(open(sys.argv[1])); sumber_durasi = "diukur dari VO"
else:
    cuts = [0.0]
    for s in S: cuts.append(round(cuts[-1] + len(s[3].split()) / 2.2, 2))
    sumber_durasi = "PERKIRAAN (2,2 kata/detik), belum diukur dari VO"
total = cuts[-1]
gam, vid, sb, md, bag = [], [], [], [], []
for i,(sid,judul,refs,vo,img,cam,aksi,kelas,src) in enumerate(S):
    a, b = cuts[i], cuts[i+1]; d = b - a; klip = max(3, min(15, math.ceil(d + 0.2)))
    t1, t2 = round(klip/3), round(klip*2/3)
    gam.append(f"## {sid} · {judul}\nReferensi: {', '.join(r for r in refs)}\n\n{img} Style: {STYLE}.\n")
    vid.append(f"## {sid} · {judul} · {klip} detik (VO {a:.2f}–{b:.2f} = {d:.2f} dtk)\n\nVO: {vo}\n\n```\n{sid} — Animate the provided start frame as a smooth 2D animated illustration, vertical 9:16, {klip} seconds, one continuous shot, no cuts. Keep every character, prop, color, line and background exactly as in the start frame. Camera: {cam}. It is one continuous, very smooth, slow cinematic move from the first frame to the last, easing in during the first second and settling softly in the final second, with subtle layered parallax and no jumps. Action: 0-{t1}s {aksi[0]}. {t1}-{t2}s {aksi[1]}. {t2}-{klip}s {aksi[2]}. Motion is fluid and gentle with natural secondary motion, stable lighting, steady camera with no shake. Characters stay silent: no talking, no lip-sync, only facial expressions. Silent video, no voice, no music. {NEG}\n```\n")
    sb.append(f"| {sid} | {a:.1f}–{b:.1f} | {klip} | {judul} | {cam} | {vo} |")
    md.append(f"## {sid} · {judul} ({kelas})\n{vo}\n")
    bag.append({"id":sid,"mulai":a,"selesai":b,"vo":vo,"kelas":kelas,"tingkat_keyakinan":YAKIN[kelas],
        "sumber":[{"klaim":vo,"atribusi":SUMBER[k][0],"url":SUMBER[k][1]} for k in src]})
tulis("prompt_gambar.md", "# Prompt gambar Flow (9:16, 1 output per scene)\n\n## Character lock (buat dulu)\n\n" +
      "\n".join(f"### {k}\nCharacter reference sheet, plain soft background: {v}. Style: {STYLE}.\n" for k,v in CHARS.items()) + "\n" + "\n".join(gam))
tulis("prompt_video.md", f"# Prompt video Nexabot (Start Frame to Video, Portrait 9:16, 1080p)\n\nDurasi: {sumber_durasi}. Slider = angka di judul; potong ujung klip mengikuti waktu VO. Video tanpa suara.\nTeks \"6EQUJ5\" dan \"Wow!\" (S04) ditambahkan saat edit, bukan dari AI.\n\n" + "\n".join(vid))
tulis("storyboard.md", f"# Storyboard Short \"Sinyal Wow!\" ({total/60:.0f} mnt kurang lebih, {total:.1f} dtk; {sumber_durasi})\n\n| Scene | Waktu (dtk) | Klip (dtk) | Isi | Kamera | VO |\n|---|---|---|---|---|---|\n" + "\n".join(sb) +
      "\n\nTeks layar saat edit: S01 \"1977\"; S04 \"6EQUJ5\" + \"Wow!\"; S06 \"±1420 MHz\"; S07 \"72 detik\"; S12 \"hipotesis, belum terbukti\".")
tulis("naskah.md", f"# Naskah: Sinyal Wow!, 72 Detik yang Belum Terjawab\n\n{kata} kata.\n\n" + "\n".join(md))
tulis("vo_satu_take.txt", "\n\n".join(s[3] for s in S))
json.dump({"judul_kerja":"Sinyal Wow!","format":"short_90","catatan_format":"Pemilik meminta 1,5-2,5 menit (28 Nov); di luar rentang Short POSA 87-95 dtk.",
 "pilar":"Misteri","momen_jawaban_detik":cuts[3],"jumlah_kata":kata,"durasi_detik":total,"catatan_durasi":sumber_durasi,"bagian":bag,
 "sumber":[v[1] for v in SUMBER.values()]}, open("naskah.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(cuts, open("cuts.json","w"))
print(kata, "kata", round(total,1), "dtk", sumber_durasi)
