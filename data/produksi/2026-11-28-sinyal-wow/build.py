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
 "Tahun seribu sembilan ratus tujuh puluh tujuh, sebuah teleskop menangkap sinyal aneh dari langit. Saking kagetnya, seorang astronom menulis satu kata: Wow!",
 "Starry night over CHAR_BIGEAR. A thin glowing amber beam of radio waves descends from one bright point in the sky onto the telescope. In the foreground CHAR_ASTRO holds a long continuous paper printout, eyes wide and mouth open in amazement.",
 "Slow push-in from the wide sky toward the astronomer",
 ["stars twinkle and the amber wave rings travel down the beam toward the telescope","the astronomer lifts the printout and his eyes widen","his glasses catch an amber glint and he holds an amazed pose"],"fakta",["ehman"]),
("S02","Big Ear",["CHAR_RAKA","CHAR_BIGEAR"],
 "Teleskopnya bernama Big Ear, alias Telinga Raksasa, di Ohio, Amerika. Ia nggak melihat bintang. Ia mendengarkan gelombang radio.",
 "Golden dusk over CHAR_BIGEAR seen from a gentle high angle, tiny figures of CHAR_RAKA in the foreground cupping a hand behind his ear. Soft concentric teal wave arcs flow from the sky into the tall curved reflector.",
 "Smooth sideways glide across the telescope field",
 ["clouds drift slowly and grass sways","teal wave arcs flow from the sky into the curved reflector","Raka cups his ear, smiles and nods while the first stars appear"],"fakta",["ehman"]),
("S03","Cetakan",["CHAR_ASTRO"],
 "Malam lima belas Agustus, komputer mencatat semuanya di kertas. Beberapa hari kemudian, Jerry Ehman memeriksa tumpukan cetakan itu.",
 "Cozy 1970s study room. CHAR_ASTRO sits at a wooden desk reading a tall stack of folded continuous printer paper with perforated edges, covered only with tiny abstract dots. Green desk lamp, coffee mug, reel-to-reel tape computer cabinets and a window with night sky behind.",
 "Gentle push-in over the desk",
 ["the desk lamp glows and steam rises from the mug","he slides one sheet of paper aside and follows a row with his finger","he leans closer and adjusts his glasses"],"fakta",["ehman"]),
("S04","Lingkaran merah",["CHAR_ASTRO"],
 "Matanya berhenti di kode: enam, E, Q, U, J, lima. Dilingkari pena merah, lalu ditulis: Wow!",
 "Close-up top view of a continuous printout on a desk with a wide blank cream area in the center and tiny abstract dots around it. The hand of CHAR_ASTRO holds a red pen and has just drawn a bold empty red oval around the blank area. Warm lamp light.",
 "Very slow top-down push-in toward the red oval",
 ["the hand hovers with the red pen above the paper","the pen traces softly along the existing red oval","the pen lifts and the hand taps the paper once"],"fakta",["ehman"]),
("S05","Kekuatan",["CHAR_RAKA"],
 "Itu bukan pesan rahasia. Huruf dan angka itu ukuran kekuatan sinyal. Puncaknya sekitar tiga puluh kali lebih kuat dari bising latar.",
 "CHAR_RAKA stands beside a giant glowing bar chart made of plain colored blocks without labels: many tiny grey blocks and one set of six blocks rising and falling like a mountain, the tallest bright amber. He points up at the tallest block. Dark teal studio with soft particles.",
 "Slow vertical tilt from the small blocks up to the tallest amber block",
 ["tiny grey blocks flicker gently","the six colored blocks glow one after another from left to right","Raka points at the tallest block, impressed, as it pulses"],"fakta",["ehman"]),
("S06","Saluran hidrogen",["CHAR_RAKA"],
 "Frekuensinya dekat seribu empat ratus dua puluh megahertz, nada alami atom hidrogen. Ilmuwan pernah mengusulkan: alien mungkin memilih saluran ini untuk menyapa.",
 "Deep space scene with a large stylized glowing hydrogen atom, one small electron on a ring, emitting soft concentric teal waves. CHAR_RAKA floats beside it holding a vintage radio and turning its knob. Nebula clouds and many stars.",
 "Slow arc from the atom toward Raka and the radio",
 ["the electron circles slowly and waves pulse outward","Raka turns the radio knob and its amber dial light brightens","he tilts his head, listening, with a curious smile"],"fakta",["ehman","cocconi"]),
("S07","72 detik",["CHAR_BIGEAR"],
 "Sinyalnya naik lalu turun selama tujuh puluh dua detik. Pas dengan sapuan teleskop saat Bumi berputar. Artinya, sumbernya tampak ikut bergerak bersama langit.",
 "Beautiful view of the curved edge of Earth at night with CHAR_BIGEAR small on its surface, projecting a soft teal listening beam into the starry sky. The beam passes across one bright amber point. A glowing smooth bell-shaped curve of light floats in the sky.",
 "Slow pull-back revealing the curve of the Earth",
 ["the beam begins to approach the amber point as the Earth turns slightly","the beam crosses the point and the point shines brightest","the beam moves past and the point dims gently"],"fakta",["ehman"]),
("S08","Dua corong",["CHAR_RAKA"],
 "Anehnya, Big Ear punya dua corong penerima. Kalau sumbernya terus menyala, harusnya tertangkap dua kali. Ternyata cuma sekali.",
 "Inside the receiver hut: two large metal horn-shaped receivers side by side. The left horn glows with a bright amber wave entering it, the right horn is completely dark and quiet. CHAR_RAKA stands between them scratching his head, puzzled.",
 "Smooth pan from the left horn to the right horn",
 ["amber waves pour into the left horn","the camera reaches the dark right horn and nothing arrives","Raka scratches his head and shrugs"],"fakta",["ehman"]),
("S09","Sagitarius",["CHAR_ASTRO","CHAR_BIGEAR"],
 "Arahnya dari rasi Sagitarius. Big Ear mengecek lokasi itu lebih dari lima puluh kali. Hasilnya? Sunyi.",
 "Rich Milky Way core sky with a subtle constellation drawn as thin glowing lines shaped like a teapot, one empty soft circle marking a spot beside it. Below, CHAR_ASTRO with headphones sits on the grass near CHAR_BIGEAR, looking disappointed.",
 "Slow tilt from the astronomer up to the constellation",
 ["the astronomer presses his headphones and waits","the constellation lines glow softly one by one","the marked circle stays empty and dim"],"fakta",["ehman","gray_wiki"]),
("S10","Perburuan",["CHAR_RAKA"],
 "Peneliti lain ikut berburu, pakai teleskop di Amerika dan Australia. Tahun dua ribu dua puluh dua, satu bintang kandidat ikut disimak. Tetap kosong.",
 "Wide night landscape with several large white dish radio antennas on desert hills all pointing at one small warm yellow star. CHAR_RAKA in the foreground looks through binoculars. Colorful twilight horizon.",
 "Gentle glide forward between the dishes",
 ["the dishes tilt very slightly toward the star","the small star twinkles while soft teal listening arcs reach toward it","Raka lowers the binoculars and sighs"],"fakta",["gray","bl2022"]),
("S11","Komet?",["CHAR_RAKA"],
 "Ada yang menduga komet. Tapi sejumlah astronom menolak: posisi dan perilakunya dinilai nggak cocok.",
 "A glowing icy comet with a long teal tail crossing a starry sky. CHAR_RAKA stands on a hill holding up two crossed arms in an X gesture with a friendly skeptical face. Silhouette of pine trees.",
 "Slow tracking shot following the comet, ending on Raka",
 ["the comet glides slowly and its tail shimmers","Raka watches and raises an eyebrow","he crosses his arms into an X and shakes his head gently"],"klaim",["comet"]),
("S12","Awan hidrogen",["CHAR_RAKA"],
 "Hipotesis baru tahun dua ribu dua puluh empat: awan hidrogen dingin mendadak terang akibat semburan magnetar, bintang supermagnet. Menarik, tapi belum terbukti.",
 "Spectacular deep space: a small dense star with curved magnetic field lines sends a burst of light toward a soft blue hydrogen cloud, which glows brightly and sends a narrow amber ray toward a tiny distant Earth. CHAR_RAKA floats in a corner holding a magnifying glass.",
 "Slow pan from the magnetic star to the glowing cloud",
 ["the magnetic star pulses and releases one burst of light","the blue cloud lights up from within","a narrow amber ray extends toward the tiny Earth while Raka studies it"],"dugaan",["arecibo1","arecibo2"]),
("S13","Belum pasti",["CHAR_RAKA","CHAR_ASTRO"],
 "Jadi, alien? Belum ada buktinya. Sebab alami? Juga belum pasti. Ehman sendiri bilang, datanya terlalu sedikit.",
 "A balanced scale in a warm observatory room: on one side a small cute generic glowing flying saucer toy, on the other a small glowing blue cloud. CHAR_RAKA and CHAR_ASTRO stand on either side thinking with hands on chins.",
 "Gentle push-in toward the balanced scale",
 ["the scale tips very slightly to the toy side","it tips slightly to the cloud side","it settles level and both characters shrug"],"fakta",["ehman"]),
("S14","Penutup",["CHAR_RAKA","CHAR_BIGEAR"],
 "Tujuh puluh dua detik, lalu hening hampir lima puluh tahun. Menurutmu itu apa? Tulis tebakanmu di komentar!",
 "CHAR_RAKA sits on a hill under a magnificent starry sky wearing headphones, smiling at the viewer and pointing upward. CHAR_BIGEAR silhouette in the distance, one bright amber star above.",
 "Slow pull-back from Raka to reveal the whole sky",
 ["he listens quietly while stars twinkle","the amber star flares softly once","he smiles at the viewer, points upward and holds the pose"],"narasi",["ehman"]),
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
    vid.append(f"## {sid} · {judul} · {klip} detik (VO {a:.2f}–{b:.2f} = {d:.2f} dtk)\n\nVO: {vo}\n\n```\n{sid} — Animate the provided start frame as a smooth 2D animated illustration, vertical 9:16, {klip} seconds, one continuous shot, no cuts. Keep every character, prop, color, line and background exactly as in the start frame. Camera: {cam}, with soft ease-in and ease-out. Action: 0-{t1}s {aksi[0]}. {t1}-{t2}s {aksi[1]}. {t2}-{klip}s {aksi[2]}. Motion is fluid and gentle with natural secondary motion, stable lighting, steady camera with no shake. Characters stay silent: no talking, no lip-sync, only facial expressions. Silent video, no voice, no music. {NEG}\n```\n")
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
