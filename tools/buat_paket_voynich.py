#!/usr/bin/env python3
"""Membangun naskah/storyboard/prompt video Voynich dari satu sumber data (SCENES).
Pakai: python tools/buat_paket_voynich.py data/produksi/2026-11-17
"""
import json, os, sys

GAYA = ("cinematic noir still, 35mm film grain, low-key lighting, warm amber lamp light against deep midnight navy "
        "and black shadows, archival paper texture, single clear focal subject, high contrast, 16:9, no text, no watermark")
NEG_IMG = "bright colors, cartoon, cheerful, flat lighting, text overlay, watermark, logo, real person's face, readable letters, extra fingers"
NEG_VID = ("fast cuts, shaky camera, morphing faces, warping text, glitch, flicker, subtitles, watermark, logo, "
           "cartoon, bright saturated colors, jump cut, zoom burst")

SRC = {
 "wiki": ("Wikipedia: Voynich manuscript (merangkum literatur primer)", "https://en.wikipedia.org/wiki/Voynich_manuscript"),
 "nu": ("voynich.nu: Ownership history (R. Zandbergen)", "https://www.voynich.nu/history.html"),
 "brit": ("Encyclopaedia Britannica: Voynich manuscript", "https://www.britannica.com/print/article/2059077"),
 "plos": ("Montemurro & Zanette 2013, PLoS ONE 8(6): e66344", "https://pmc.ncbi.nlm.nih.gov/articles/PMC3689824"),
 "bristol": ("Shropshire Star / PA, 17 Mei 2019: universitas menarik klaim Cheshire", "https://www.shropshirestar.com/news/uk-news/2019/05/17/university-backtracks-over-voynich-manuscript-translation-claims"),
 "ia": ("Internet Archive: voynich_MS_408 (Public Domain Mark, sumber Beinecke)", "https://archive.org/details/voynich_MS_408/mode/2up"),
}

# id, bagian, kelas, keyakinan, sumber, vo, on_screen, kamera, sfx, subjek_flow, aksi_video, scan_asli
S = []
def sc(*a): S.append(a)

sc("S01","Cold open","fakta",None,["wiki","brit"],
 "Bayangin kamu menemukan sebuah buku tua. Isinya gambar tanaman yang aneh sekali, ditulis dengan huruf yang tidak dikenal siapa pun. Ini bukan film. Bukunya nyata, tersimpan di Yale, dan sampai sekarang belum ada yang bisa membacanya.",
 "BUKU YANG TAK BISA DIBACA","slow push-in","drone rendah, detak jam jauh",
 "an old leather-bound medieval codex lying open on a lone office desk at night, a single amber desk lamp, empty dark office behind, the open pages show invented herbal drawings with an unreadable made-up script",
 "0-5s: kamera dolly masuk perlahan ke buku di meja; 5-10s: debu melayang di cahaya lampu amber, lampu berkedip halus sekali; 10-15s: kamera berhenti di halaman terbuka, bayangan jendela kantor bergeser pelan.",
 None)
sc("S02","Pengenalan","fakta",None,["wiki","brit"],
 "Namanya Naskah Voynich. Di Yale kodenya Beinecke MS empat ratus delapan. Ukurannya seperti buku catatan, sekitar dua puluh tiga kali enam belas sentimeter. Sekitar dua ratus empat puluh halaman bertahan, padahal aslinya setidaknya dua ratus tujuh puluh dua.",
 "BEINECKE MS 408","static, lalu geser kiri","kertas dibalik pelan",
 "a closed small thick medieval codex with worn vellum cover beside a ruler on a dark archive table, warm amber lamp rim light, shallow depth of field",
 "0-5s: close-up sampul tua, kamera diam; 5-10s: tangan bersarung putih (tanpa wajah) membuka sampul pelan; 10-15s: kamera geser kiri menyusuri tepi halaman yang tebal.",
 "scan sampul/halaman Beinecke sebagai inset")
sc("S03","Pengenalan","fakta",None,["wiki","brit"],
 "Menurut para peneliti, isinya terbagi enam bagian. Bagian tumbuhan paling tebal, sekitar seratus dua puluh enam halaman. Lalu ada diagram bintang, perempuan telanjang di antara kolam dan pipa, gambar botol obat, dan bagian yang mirip daftar resep.",
 "6 BAGIAN","pan horizontal lambat","gesekan kertas",
 "a cinematic spread of six invented medieval-style illustration cards laid on a dark desk: plants, star diagram, bathing pools with pipes, jars, recipe lines; all drawings are original inventions with unreadable glyphs, amber lamp light",
 "0-5s: kamera pan lambat melewati kartu tumbuhan; 5-10s: lanjut ke diagram bintang dan kolam; 10-15s: berhenti di botol dan baris resep, cahaya amber menguat sedikit.",
 "scan halaman herbal, astronomi, balneologi dari Beinecke")
sc("S04","Pengenalan","fakta",None,["wiki","plos"],
 "Tulisannya yang paling bikin pusing. Sekitar dua puluh sampai dua puluh lima karakter menyusun sebagian besar teks, mengalir dari kiri ke kanan, hampir tanpa tanda baca. Totalnya sekitar tiga puluh delapan ribu kata, tak satu pun kita tahu artinya.",
 "38.000 KATA, 0 ARTI","extreme macro","goresan pena",
 "extreme macro of lines of invented unreadable script in dark brown ink on aged vellum, warm amber raking light, visible parchment grain, shallow focus",
 "0-5s: macro baris tulisan, kamera diam; 5-10s: fokus bergeser dari kata ke kata dari kiri ke kanan; 10-15s: kamera mundur perlahan, memperlihatkan seluruh paragraf.",
 "scan halaman teks murni")
sc("S05","Latar belakang","fakta",None,["wiki","brit"],
 "Lalu kapan ditulis? Tahun dua ribu sembilan, Universitas Arizona menguji umur kulitnya dengan radiokarbon. Hasilnya antara tahun seribu empat ratus empat dan seribu empat ratus tiga puluh delapan. Jadi ini memang naskah abad kelima belas.",
 "1404-1438","slow tilt up","dengung laboratorium halus",
 "a small vellum sample in a dim laboratory under a warm amber lamp, scientific instruments blurred in the dark background, no readable screens",
 "0-5s: tilt up dari meja lab ke sampel perkamen; 5-10s: titik cahaya amber berdenyut pelan di instrumen buram; 10-15s: kamera mendekat ke tekstur perkamen.",
 None)
sc("S06","Latar belakang","fakta",None,["wiki","brit"],
 "Satu catatan penting: yang diuji kulitnya, bukan tintanya. Tapi pemindaian multispektral tidak menemukan tulisan lama di bawahnya, jadi ini bukan kulit bekas. Dan hasil ini mematahkan dugaan lama bahwa penulisnya Roger Bacon, ilmuwan abad ketiga belas.",
 "BUKAN ROGER BACON","static, rack focus","bisikan angin",
 "a dark study with a stack of old scholarly books and a silhouette-less empty chair, an amber lamp, a glowing ultraviolet-blue line sweeping across a page, restrained",
 "0-5s: rack focus dari tumpukan buku ke halaman; 5-10s: garis cahaya biru tipis menyapu halaman sekali; 10-15s: cahaya padam, tinggal lampu amber.",
 None)
sc("S07","Kronologi","fakta","kuat",["wiki","nu"],
 "Jejak pertamanya baru muncul hampir dua abad kemudian, di kota Praha. Ada tanda tangan samar di halaman pertama: Jacobus Horčický de Tepenec, yang diangkat jadi bangsawan kecil. Siapa pemilik sebelum dia? Tidak ada yang tahu pasti.",
 "PRAHA, ABAD 17","slow dolly","lonceng jauh",
 "a 17th-century Prague alchemist's study at night, candle and amber light, shelves of jars and books, a faint erased signature glowing on an old page, no faces",
 "0-5s: dolly lambat melewati rak botol alkemis; 5-10s: cahaya lilin bergoyang; 10-15s: kamera berhenti pada tanda tangan pudar di halaman.",
 None)
sc("S08","Kronologi","klaim","spekulatif",["wiki","nu"],
 "Menurut surat tahun seribu enam ratus enam puluh lima, Kaisar Rudolf II pernah membelinya seharga enam ratus dukat emas. Tapi itu kabar turunan. Istana memang mencatat pembelian buku tahun seribu lima ratus sembilan puluh sembilan, belum terbukti itu naskah ini.",
 "600 DUKAT?","slow push-in","denting koin",
 "a Renaissance imperial court treasury at night, a small pile of gold ducats on a dark table, a wax-sealed letter, amber candlelight, no faces",
 "0-5s: close-up koin emas di meja; 5-10s: kamera bergeser ke surat bersegel; 10-15s: cahaya lilin meredup sebagian, koin tetap berkilau.",
 None)
sc("S09","Kronologi","fakta","kuat",["wiki","nu"],
 "Pemilik pertama yang pasti terdokumentasi adalah Georg Baresch, seorang alkemis di Praha. Tahun seribu enam ratus tiga puluh sembilan ia menulis surat kepada Athanasius Kircher di Roma dan mengirim contoh tulisan dari buku itu.",
 "SURAT 1639","side tracking","goresan pena, kertas",
 "a 17th-century desk with a quill, an inkwell and a handwritten letter being folded, a hand only, amber candle light, dark room",
 "0-5s: tangan menulis surat (tanpa wajah); 5-10s: surat dilipat dan disegel lilin; 10-15s: kamera mengikuti surat yang ditaruh di tumpukan pengiriman.",
 None)
sc("S10","Kronologi","fakta","kuat",["wiki","nu"],
 "Setelah Baresch wafat, bukunya diwariskan ke Johannes Marcus Marci, yang mengirimnya ke Kircher lewat surat tahun seribu enam ratus enam puluh lima. Dari surat itulah kisah Rudolf dan Roger Bacon bermula, dan Marci sendiri tidak menjaminnya.",
 "SURAT 1665","slow pan","kertas, derap kuda jauh",
 "a courier's saddlebag with a wrapped package and a sealed letter on a stone ledge, moonlit cobblestone street leading toward distant Rome rooftops, amber lantern",
 "0-5s: bungkusan dimasukkan ke tas pelana; 5-10s: kamera pan mengikuti jalan batu yang basah; 10-15s: lampu lentera mengecil di kejauhan.",
 None)
sc("S11","Kronologi","fakta","kuat",["wiki","nu"],
 "Naskah itu tersimpan di perpustakaan Jesuit di Roma selama berabad-abad, sampai harta mereka disita tahun seribu delapan ratus tujuh puluh tiga. Tahun seribu sembilan ratus dua belas, pedagang buku langka Wilfrid Voynich membelinya, dan namanya melekat sampai sekarang.",
 "1912: VOYNICH","slow dolly","gema perpustakaan",
 "a vast dim Jesuit library corridor with towering bookshelves and a lone amber lantern, dust in the air, a rare-book dealer's trunk in the foreground, no faces",
 "0-5s: dolly menyusuri lorong rak buku; 5-10s: kamera menemukan peti buku di sudut; 10-15s: peti dibuka sedikit, cahaya amber keluar dari dalam.",
 None)
sc("S12","Kronologi","fakta","kuat",["wiki","nu"],
 "Setelah Voynich meninggal, bukunya akhirnya dibeli pedagang buku Hans Kraus tahun seribu sembilan ratus enam puluh satu seharga dua puluh empat ribu lima ratus dolar. Delapan tahun kemudian, ia menyumbangkannya ke Perpustakaan Beinecke di Yale.",
 "1969: YALE","static, lalu tilt up","langkah di marmer",
 "a modern university rare-book library at night, a glass reading room with a single amber lamp, a sealed archival box on a table, long shadows",
 "0-5s: kotak arsip di meja; 5-10s: kamera tilt up ke jendela kaca besar perpustakaan; 10-15s: lampu amber menyala satu per satu di ruangan.",
 None)
sc("S13","Bukti & analisis","fakta",None,["wiki","brit"],
 "Tentu banyak yang mencoba membacanya. Di abad kedua puluh, para pemecah sandi terbaik, termasuk tim William Friedman, ikut mengerjakannya. Pendekatan utamanya menganggap ini sandi huruf biasa, yang diacak dengan aturan tertentu. Semuanya gagal.",
 "SEMUA GAGAL","slow push-in","ketikan mesin sandi",
 "a mid-20th-century codebreaking office at night, stacks of papers with invented cipher tables, a vintage cipher machine, amber desk lamp, silhouette-less",
 "0-5s: tumpukan kertas sandi di meja; 5-10s: roda mesin sandi berputar pelan; 10-15s: kamera mendekat ke kertas penuh coretan merah, lalu diam.",
 None)
sc("S14","Bukti & analisis","fakta","kuat",["wiki","plos"],
 "Anehnya, teksnya tidak terlihat ngawur. Pola kata-katanya mirip bahasa asli lewat hukum Zipf: kata paling sering muncul sekitar dua kali lebih sering dari kata kedua, dan tiga kali dari kata ketiga. Itu pola yang sulit ditiru asal-asalan.",
 "POLA BAHASA?","static macro","detak halus",
 "a dark desk with a hand-drawn bar chart of descending frequencies on aged paper, red pencil circles, amber lamp, shallow focus",
 "0-5s: grafik batang tulisan tangan; 5-10s: lingkaran merah tergambar pada batang pertama dan kedua; 10-15s: lingkaran ketiga, kamera diam.",
 None)
sc("S15","Bukti & analisis","fakta","kuat",["plos","wiki"],
 "Tahun dua ribu tiga belas, Marcelo Montemurro dan Damián Zanette menemukan kata-kata kunci naskah ini mengelompok mengikuti topik, dan bagian bertanaman berbagi kosakata. Mereka menyimpulkan ada struktur layaknya bahasa. Tapi itu bukan pembacaan, kata mereka sendiri.",
 "ADA STRUKTUR","slow pan","dengung data",
 "an investigation board wall in a dark office with red string connecting index cards and invented plant sketches, amber lamp, no readable text",
 "0-5s: papan investigasi, benang merah; 5-10s: kamera pan mengikuti benang antar kartu; 10-15s: berhenti di satu kartu kosong.",
 None)
sc("S16","Bukti & analisis","fakta","didukung",["wiki","plos"],
 "Tapi ada sisi yang janggal juga. Keteraturan huruf demi huruf, yang disebut entropi kondisional, hanya sekitar dua, sedangkan bahasa alami umumnya tiga sampai empat. Hurufnya terlalu mudah ditebak, dan itu membuat sebagian peneliti ragu ini bahasa biasa.",
 "TERLALU TERATUR","rack focus","denging tipis",
 "two aged paper strips of different pattern density side by side under an amber lamp, one chaotic and one overly regular, dark desk, macro",
 "0-5s: dua strip kertas berdampingan; 5-10s: fokus bergeser dari yang acak ke yang teratur; 10-15s: lampu meredup sedikit.",
 "scan halaman teks sebagai pembanding")
sc("S17","Bukti & analisis","dugaan","diperdebatkan",["wiki","plos"],
 "Teori pertama: tipuan. Tahun dua ribu tiga, Gordon Rugg menunjukkan teks yang mirip bisa dibuat dengan tabel suku kata dan kartu berlubang Cardan grille. Tapi mirip belum tentu sama, dan Montemurro menilai bukti strukturnya membatasi kemungkinan tipuan.",
 "TEORI 1: TIPUAN","slow push-in","klik mekanis",
 "a medieval Cardan grille, a perforated card laid over a table of syllables on parchment, amber lamp, dark workshop",
 "0-5s: tabel suku kata di perkamen; 5-10s: kartu berlubang diturunkan menutupi tabel; 10-15s: potongan kata terlihat lewat lubang, kamera diam.",
 None)
sc("S18","Bukti & analisis","dugaan","spekulatif",["wiki","brit"],
 "Teori kedua: ini bahasa sungguhan, atau mungkin bahasa buatan dengan aksara khusus. Usulannya banyak, dari Nahuatl, Ibrani, sampai Turki kuno. Masalahnya, tiap usulan diuji peneliti lain dan sampai sekarang belum ada satu pun yang diterima luas.",
 "TEORI 2: BAHASA","slow dolly","bisik banyak suara samar",
 "a dark room with many floating invented scripts projected faintly on walls, a lone desk and amber lamp, no readable letters, moody",
 "0-5s: aksara samar muncul di dinding gelap; 5-10s: kamera dolly melewati meja kosong; 10-15s: satu aksara menyala amber lalu memudar.",
 None)
sc("S19","Bukti & analisis","klaim","ditolak ahli",["bristol","wiki"],
 "Tahun dua ribu sembilan belas, Gerard Cheshire dari Universitas Bristol mengaku memecahkannya dalam dua minggu: bahasa proto-Romance. Universitas segera menarik beritanya, karena ada kekhawatiran soal validitas penelitiannya. Paleograf Lisa Fagin Davis menyebut terjemahannya melingkar dan membenarkan dirinya sendiri.",
 "KLAIM DITARIK","static, lalu zoom out","bunyi surat kabar jatuh",
 "a university press office at night, a newspaper being pulled from a corkboard, a pinned page torn halfway, amber desk lamp, no faces or readable headlines",
 "0-5s: koran terpasang di papan; 5-10s: koran ditarik lepas; 10-15s: paku kosong, kamera zoom out.",
 None)
sc("S20","Bukti & analisis","klaim","spekulatif",["wiki","brit"],
 "Ada juga klaim yang lebih hati-hati. Stephen Bax, tahun dua ribu empat belas, mengusulkan pembacaan sebagian: sepuluh nama diri dan empat belas karakter. Itu masih usulan, belum terbukti, dan Bax wafat tahun dua ribu tujuh belas.",
 "BACAAN SEBAGIAN","slow push-in","denting piano tunggal",
 "a researcher's desk with index cards of ten invented plant labels and a magnifying glass, an empty chair, amber lamp, dim study",
 "0-5s: kartu label tanaman di meja; 5-10s: kaca pembesar bergerak di atas kartu; 10-15s: kursi kosong mengisi bingkai, lampu meredup perlahan.",
 None)
sc("S21","Bukti & analisis","klaim","didukung sebagian",["wiki","brit"],
 "Pertanyaan lain yang menarik: berapa orang menulisnya? Lisa Fagin Davis, lewat analisis tulisan tangan digital tahun dua ribu dua puluh, berpendapat naskah ini dikerjakan beberapa penulis dalam satu komunitas. Kalau benar, ini bukan coretan satu orang iseng.",
 "SIAPA PENULISNYA?","slow tilt","goresan pena bergantian",
 "a medieval scriptorium at night with several empty writing desks each lit by a small amber lamp, no faces, shadows of hands only",
 "0-5s: deretan meja penulis kosong; 5-10s: bayangan tangan menulis di dinding; 10-15s: lampu menyala satu per satu.",
 None)
sc("S22","Kesimpulan","fakta",None,["wiki","nu","plos"],
 "Cara menimbang semua ini? Anggap papan investigasi di kantor: ada bukti keras, ada dugaan, ada tebakan. Yang keras: umur kulitnya, jalur kepemilikan sejak sekitar seribu enam ratus, dan pola statistik teksnya. Sisanya, termasuk soal isinya, masih dugaan.",
 "BUKTI vs DUGAAN","slow pan","detak jam",
 "an office investigation board split into three zones with index cards, solid red-string connections on one side and loose cards on the other, amber lamp, no readable text",
 "0-5s: papan terbagi tiga zona; 5-10s: benang merah mengencang di sisi bukti keras; 10-15s: kartu di sisi dugaan bergoyang pelan.",
 None)
sc("S23","Kesimpulan","fakta",None,["wiki","plos"],
 "Bayangin ruang arsip kantor penuh map berlabel kode yang kamusnya tidak ada. Kamu bisa melihat polanya: map mana yang mirip, mana yang berkelompok. Tapi tanpa kamus, kamu tidak tahu isinya. Itulah posisi para peneliti Voynich sampai sekarang.",
 "TANPA KAMUS","slow dolly","kertas, hening kantor",
 "an empty night office archive room with rows of filing cabinets labelled with invented symbols, a single amber lamp at the far end, long perspective",
 "0-5s: dolly menyusuri lorong lemari arsip; 5-10s: kamera melewati satu map yang menyembul; 10-15s: berhenti di lampu amber di ujung lorong.",
 None)
sc("S24","Kesimpulan","fakta","kuat",["wiki","plos"],
 "Kenapa susah? Ada sekitar seribu label yang menempel pada gambar, tapi jarang berulang, jadi sulit dipakai sebagai kunci. Dan sampai hari ini, belum ada pembacaan yang diterima luas oleh para ahli, sekeras apa pun mereka mencoba.",
 "BELUM ADA KUNCI","static macro","dengung halus",
 "macro of a medieval illustration with small invented labels next to a plant drawing, aged parchment, amber raking light, shallow focus, unreadable glyphs",
 "0-5s: macro satu gambar tumbuhan dengan label; 5-10s: fokus berpindah antar label; 10-15s: kamera mundur memperlihatkan banyak label.",
 "scan halaman herbal berlabel")
sc("S25","Kesimpulan","fakta","kuat",["wiki","brit","plos"],
 "Jadi apa yang kita tahu? Ini buku asli abad kelima belas, ditulis dengan aksara unik, dan menurut sebagian peneliti teksnya terlalu berstruktur untuk sekadar tipuan, tapi juga tidak sepenuhnya seperti bahasa biasa. Sisanya, jujur saja, masih gelap.",
 "YANG KITA TAHU","slow push-in","drone naik",
 "the open codex on the lone desk again in a dark office, amber lamp, the window now showing a distant night city, calm, high contrast",
 "0-5s: buku terbuka di meja; 5-10s: kamera mendekat pelan; 10-15s: lampu amber menerangi satu halaman, sisanya gelap.",
 None)
sc("S26","Closing","fakta",None,["wiki"],
 "Mungkin suatu hari ada yang menemukan kuncinya. Mungkin juga tidak. Tapi buku ini sudah lama menemani orang-orang yang lembur dengan pertanyaan yang sama, dan mungkin masih lama. Menurutmu ini bahasa, sandi, atau tipuan? Tulis di kolom komentar.",
 "BAHASA, SANDI, ATAU TIPUAN?","slow pull-back","drone memudar, satu detak jam",
 "a lone desk lamp turning off in a dark office, the codex a faint silhouette, city lights through the window, quiet and warm amber fading to navy",
 "0-5s: lampu amber redup perlahan; 5-10s: kamera menarik mundur memperlihatkan kantor kosong; 10-15s: gelap, hanya lampu kota jauh.",
 None)

_f = os.path.join(os.path.dirname(__file__), 'vo_30kata.json')
VO_OVR = json.load(open(_f)) if os.path.exists(_f) else {}
WPS = 2.05  # kata/detik perkiraan TTS Indonesia (dikalibrasi ulang dari audio asli)

def main(out):
    os.makedirs(out, exist_ok=True)
    scenes = []
    t = 0.0
    for (sid, bagian, kelas, yakin, srcs, vo, onscr, kam, sfx, subjek, aksi, scan) in S:
        vo = VO_OVR.get(sid, vo)
        n = len(vo.split())
        est = round(n / WPS + 0.3, 1)
        pakai = min(15.0, est)
        scenes.append(dict(id=sid, bagian=bagian, kelas=kelas, tingkat_keyakinan=yakin,
            sumber=[dict(klaim=bagian + " " + sid, atribusi=SRC[k][0], tahun=None, url=SRC[k][1]) for k in srcs],
            vo=vo, jumlah_kata=n, durasi_vo_perkiraan=est, durasi_klip_generate=15, durasi_pakai=pakai,
            on_screen=onscr, kamera=kam, sfx=sfx,
            flow_prompt=f"{subjek}. Style: {GAYA}.", flow_negative=NEG_IMG,
            video_prompt=aksi, video_negative=NEG_VID, scan_asli_opsional=scan,
            mulai_perkiraan=round(t, 1)))
        t += pakai
    kata = sum(s["jumlah_kata"] for s in scenes)
    isi = round(t, 1)
    naskah = dict(judul_kerja="Naskah Voynich: Buku Abad ke-15 yang Belum Ada yang Bisa Membacanya",
        format="video panjang 16:9 1920x1080 24fps", pilar="Mystery & Unsolved Cases",
        jumlah_kata=kata, durasi_detik=isi, isi_detik=isi,
        bagian=[dict(id=s["id"], vo=s["vo"], kelas=s["kelas"], tingkat_keyakinan=s["tingkat_keyakinan"], sumber=s["sumber"]) for s in scenes],
        analogi=["papan investigasi kantor (S22)", "ruang arsip penuh map berkode tanpa kamus (S23)"],
        sumber=[v[1] for v in SRC.values()])
    json.dump(naskah, open(f"{out}/naskah.json", "w"), ensure_ascii=False, indent=1)
    json.dump(dict(gaya_global=GAYA, scenes=scenes), open(f"{out}/storyboard.json", "w"), ensure_ascii=False, indent=1)
    with open(f"{out}/naskah.md", "w") as f:
        f.write("# Naskah: Naskah Voynich\n\n_Kata: %d | perkiraan isi: %.0f dtk (kalibrasi ulang dari audio TTS)_\n\n" % (kata, isi))
        for s in scenes:
            f.write(f"**{s['id']} · {s['bagian']} · {s['kelas']}**  \n{s['vo']}\n\n")
        f.write("## Sumber\n" + "\n".join(f"- {v[0]}: {v[1]}" for v in SRC.values()) + "\n")
    with open(f"{out}/storyboard.md", "w") as f:
        f.write("# Storyboard Voynich (1 scene = 1 gambar Flow S## = 1 klip 15 dtk)\n\n")
        for s in scenes:
            f.write(f"## {s['id']} · {s['bagian']}\n- VO ({s['jumlah_kata']} kata, ~{s['durasi_vo_perkiraan']} dtk): {s['vo']}\n- On screen: {s['on_screen']}\n- Kamera: {s['kamera']}\n- SFX: {s['sfx']}\n- Flow prompt: {s['flow_prompt']}\n\n")
    with open(f"{out}/prompt_video.md", "w") as f:
        f.write("# Prompt video (Dreamina / generator pilihanmu) — tiap klip 15 detik, 16:9\n\n"
                "Aturan global: pakai gambar S## sebagai first frame; gerak lambat dan halus; tanpa teks di dalam video; pencahayaan amber tetap; satu subjek.\n"
                f"Negative prompt (semua klip): {NEG_VID}\n\n"
                "Tabel durasi: klip digenerate 15 dtk. 'Pakai' = durasi VO scene; potong ekor klip sesuai angka itu setelah VO final diukur (tidak diperlambat, tidak dipercepat).\n\n"
                "| Scene | Pakai (dtk) | Kata |\n|---|---|---|\n")
        for s in scenes:
            f.write(f"| {s['id']} | {s['durasi_pakai']} | {s['jumlah_kata']} |\n")
        f.write("\n")
        for s in scenes:
            f.write(f"### {s['id']} — 15 dtk (pakai ~{s['durasi_pakai']} dtk)\nFirst frame: gambar {s['id']}. Camera: {s['kamera']}. {s['video_prompt']}\nAmbience/SFX (tambah di edit): {s['sfx']}\n\n")
    print("kata", kata, "isi_detik", isi, "scenes", len(scenes))

if __name__ == "__main__":
    main(sys.argv[1])
