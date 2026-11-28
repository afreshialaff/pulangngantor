#!/usr/bin/env python3
"""Satu sumber untuk Ramayana Part 3. Pakai: python build.py [durasi.json]
Hasil: scenes.json, storyboard.md, prompt_gambar.md, vo_satu_take.txt, flow_blast.txt,
dan prompt_video.md (durasi dari durasi.json bila ada; kalau belum, perkiraan)."""
import json, math, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

STYLE = ("cinematic high-end 3D film render, lifelike realistic human faces and body proportions, smooth natural "
         "skin with fine detail, realistic hair strands, richly textured silk and gold jewellery, vibrant harmonious "
         "colours, soft volumetric golden light with deep sapphire shadows, extremely detailed layered background, "
         "ancient Indian epic setting, 16:9 widescreen, no text, no letters, no watermark, no logo, correct hands with five fingers")

CHARS = {
 "RAMA": "Rama, a handsome lean athletic prince about 25, dusky warm skin with a soft blue undertone, calm lotus-shaped dark eyes, shoulder-length wavy black hair tied in a loose top knot, forest-exile attire: saffron-ochre dhoti, deep green sash, simple wooden bead necklace, wooden longbow and quiver on his back, composed gentle expression",
 "SINTA": "Sinta, a graceful young woman about 22, golden warm skin, large gentle eyes, very long black braided hair with white jasmine, rose-pink sari with a thin gold border, a few delicate gold ornaments, dignified modest demeanour",
 "LAKSMANA": "Laksmana, a slim athletic young prince about 23, golden-fair skin, sharp alert eyes, black hair in a high knot, forest attire: deep blue dhoti, crimson sash, bead necklace, bow and quiver",
 "DASARATA": "King Dasarata, an elderly dignified king, long grey hair and grey beard, tall gold crown with rubies, maroon and gold royal robes, kind tired eyes",
 "KAIKEYI": "Queen Kaikeyi, a beautiful proud queen in her thirties, warm brown skin, sharp eyes, dark purple and gold sari, emerald jewellery, small gold tiara",
 "RAHWANA": "Rahwana, a powerful regal demon king about 45, bronze-red skin, strong jaw, thick black moustache, one clear human face with nine smaller crowned heads arranged symmetrically behind it, ornate black-gold armour and crimson cloak, intelligent proud eyes",
 "HANOMAN": "Hanoman, a noble anthropomorphic white-furred monkey warrior with a strong athletic body, expressive wise amber eyes, golden crown band, red dhoti with gold belt, golden mace, long curling tail",
 "SUGRIWA": "Sugriwa, a regal anthropomorphic monkey king with reddish-brown fur, small gold crown, emerald dhoti, gold armlets, thoughtful eyes",
 "SUBALI": "Subali, a very muscular anthropomorphic monkey king with dark golden-brown fur, larger than Sugriwa, heavy gold crown and necklace, purple dhoti, fierce eyes",
 "WIBISANA": "Wibisana, a gentle wise man about 38 of demon royal blood who looks human, warm brown skin, short neat beard, white and pale-gold robes, small crown, calm honest eyes",
 "KUMBAKARNA": "Kumbakarna, an enormous heavy-built giant warrior, earthy bronze skin, long dark hair and beard, small tusks, broad iron-and-bronze armour, tired but loyal eyes",
 "INDRAJIT": "Indrajit, a lean fierce young demon prince about 24, bronze skin, long black hair, silver-black armour, indigo cloak, an ornate dark bow",
 "BHARATA": "Bharata, a gentle prince about 23 resembling Rama but with golden-brown skin, long black hair in a simple knot, plain white and ivory cotton clothes, wooden bead necklace, sorrowful sincere eyes",
 "JATAYU": "Jatayu, a gigantic ancient vulture-eagle with silver-brown feathers, wise old golden eyes, powerful but aged wings",
}

# (id, bagian, kelas, sumber, judul layar, chars, vo, gambar, kamera, [aksi1, aksi2, aksi3], sfx)
S = []
def s(*a): S.append(a)

A = "walmiki_sd"; B = "britannica"; H = "hindutone"; W = "walmiki_wl"
s("S01","Cold open","kisah",[A,B],"HAMPIR JADI RAJA",["RAMA","DASARATA"],
 "Bayangin kamu hampir diangkat jadi raja. Tiba-tiba kamu disuruh pergi ke hutan, empat belas tahun. Pangeran Rama menyanggupi. Ia cuma heran, kenapa ayahnya tidak bicara sendiri.",
 "Grand royal throne hall of Ayodhya at dawn. RAMA (here in royal saffron silk with a gold circlet, no bow) stands calmly in the centre with folded hands, an empty golden coronation throne with garlands beside him, and in the shadowed background old DASARATA sits slumped on a couch, unable to look at his son.",
 "Slow dolly-in toward Rama",["marigold garlands sway gently and light grows through the arches","Rama lowers his folded hands and looks toward his father with calm surprise","he holds a serene steady gaze while dust motes drift"],"gamelan pelan, lonceng jauh")
s("S02","Peta","kisah",[B],"TIGA PERTANYAAN",["RAMA","SINTA","RAHWANA"],
 "Hari ini kita jawab tiga hal. Kenapa Rama menerima pengasingan itu? Bagaimana istrinya, Sinta, bisa diculik? Dan bagaimana ia direbut kembali lewat perang besar?",
 "Epic three-part composition in one frame: left, SINTA sitting by a forest cottage in morning light; centre, RAMA standing on a rock looking forward with his bow; right, the dark silhouette of RAHWANA above a red-lit island fortress across a stormy sea.",
 "Slow pull-back revealing all three",["morning light moves across the forest side","sea waves roll and clouds drift over the fortress","Rama holds his gaze as the wind moves his sash"],"genderang rendah")
s("S03","Intrik istana","kisah",[W,B],"BISIKAN DI ISTANA",["KAIKEYI"],
 "Menurut Walmiki, penyair kisah ini, semuanya bermula dari bisikan. Mantara, pelayan Ratu Kaikeyi, menghasut majikannya: kalau Rama jadi raja, putramu Bharata akan tersingkir.",
 "A lamp-lit palace chamber at night. An old hunch-backed maid with grey hair and a brown sari whispers into the ear of KAIKEYI, whose face shows growing worry; through a carved window the city of Ayodhya is decorated with festival lamps.",
 "Slow push-in on the two faces",["the oil lamp flickers and the maid leans closer","Kaikeyi's eyes narrow and she turns slightly away from the festive window","she clenches the edge of her sari and stays still"],"desis lampu minyak, bisik")
s("S04","Intrik istana","kisah",[A,B],"DUA JANJI DITAGIH",["KAIKEYI","DASARATA"],
 "Dulu Raja Dasarata pernah menjanjikan dua permintaan kepada Kaikeyi. Malam itu ia menagihnya: Bharata harus jadi raja, dan Rama harus diasingkan ke hutan empat belas tahun.",
 "Dim royal chamber of sorrow. KAIKEYI sits upright on the floor, ornaments scattered around her, holding up two fingers firmly, while DASARATA kneels facing her in shock, one hand on his chest, a single lamp between them.",
 "Slow arc from Kaikeyi toward Dasarata",["the lamp flame bends as Kaikeyi raises two fingers","Dasarata's shoulders sink and his eyes fill with grief","he lowers his head while she remains unmoved"],"petir jauh, nada rendah")
s("S05","Dharma","kisah",[A],"KENAPA DITERIMA?",["RAMA","KAIKEYI"],
 "Rama tidak melawan. Baginya, janji seorang ayah harus ditepati, dan membantu menepatinya adalah dharma, kewajiban luhur seorang anak. Takhta boleh lepas. Kehormatan kata-kata jangan.",
 "RAMA (royal saffron silk, gold circlet) bows respectfully with folded hands before KAIKEYI in a quiet palace corridor; he gently places his gold crown ornament on a silk cushion held by an attendant, warm light from behind him.",
 "Slow push-in on Rama's hands and face",["Rama lifts the circlet from his head","he sets it gently on the silk cushion","he folds his hands with a peaceful smile"],"suling lembut")
s("S06","Berangkat","kisah",[A],"SINTA MEMILIH IKUT",["RAMA","SINTA"],
 "Sinta menolak tinggal di istana yang nyaman. Menurutnya, tempat seorang istri ada di sisi suaminya, di mana pun. Rama sempat melarang, tetapi akhirnya luluh.",
 "A palace garden terrace at sunset. SINTA holds RAMA's hands firmly with a determined, loving expression; Rama looks at her tenderly; behind them lotus ponds, marble pillars and peacocks.",
 "Slow orbit around the couple",["the lotus pond ripples and a peacock turns","Sinta gently pulls his hands closer and nods","Rama's face softens and he smiles"],"air kolam, suling")
s("S07","Berangkat","kisah",[A],"TIGA ORANG KE HUTAN",["RAMA","SINTA","LAKSMANA"],
 "Laksmana, adik Rama, juga ikut. Rama meninggalkan busana kerajaan dan mengenakan pakaian pertapa. Rakyat Ayodhya menangis mengantar kereta mereka sampai ke gerbang kota.",
 "A chariot with two white horses leaves the great gate of Ayodhya at golden hour carrying RAMA, SINTA and LAKSMANA; a large crowd of townspeople reaches out sadly, flower petals falling, towering sandstone gate with carvings.",
 "Slow tracking move following the chariot",["the horses step forward and petals fall","townspeople raise their hands in farewell","the chariot moves under the gate as dust glows"],"derap kuda, isak jauh")
s("S08","Duka istana","kisah",[W],"RAJA WAFAT",["BHARATA"],
 "Kepergian itu terlalu berat bagi Dasarata. Tak lama kemudian, sang raja wafat karena duka. Bharata pulang dan terkejut: mahkota menunggunya, dengan harga yang tidak ia minta.",
 "A silent royal bedchamber at blue dawn: a covered royal bed with the gold crown resting on it, a young prince in white and gold (Bharata) standing at the doorway with a hand on the frame, devastated, lamps burning low, white curtains moving.",
 "Slow push-in from the doorway to the crown",["curtains drift in the cold breeze","Bharata steps one pace forward","he stops and looks down at the crown without touching it"],"angin, nada sedih")
s("S09","Sandal","kisah",[A],"SANDAL DI SINGGASANA",["RAMA","BHARATA"],
 "Bharata menyusul Rama ke hutan dan memohonnya pulang. Rama menolak, karena janji belum selesai. Bharata lalu meminta satu hal saja: sandal kakaknya.",
 "In a green forest clearing on Chitrakuta hill beside a leaf hut, Bharata, a young prince in simple white, kneels and receives a pair of golden-wood sandals from RAMA with both hands; royal elephants and soldiers wait far behind among the trees.",
 "Slow dolly-in on the sandals",["sunbeams shift through the leaves","Rama places the sandals into Bharata's hands","Bharata raises them to his forehead and closes his eyes"],"burung hutan")
s("S10","Sandal","kisah",[A],"MEMERINTAH ATAS NAMA SANDAL",["BHARATA"],
 "Sandal itu ia letakkan di singgasana. Bharata sendiri memerintah dari Nandigrama, desa di luar ibu kota, hidup sederhana, dan menunggu kakaknya pulang selama empat belas tahun.",
 "A humble village hall at Nandigrama: a pair of golden-wood sandals rest on a small throne under a white royal umbrella, Bharata, a young man with plain ascetic clothes and matted hair, sits on the floor beside it reading petitions with villagers, warm lamp light.",
 "Slow push-in on the sandals under the umbrella",["the tassels of the umbrella sway","Bharata bows toward the sandals","lamp light glows steadily on the sandals"],"suasana desa, lonceng kecil")
s("S11","Hutan","kisah",[A,H],"SEPULUH TAHUN BERPINDAH",["RAMA","SINTA","LAKSMANA"],
 "Rama, Sinta, dan Laksmana masuk makin dalam, ke rimba Dandaka. Sekitar sepuluh tahun mereka berpindah dari satu pertapaan ke pertapaan lain, melindungi para pertapa.",
 "RAMA, SINTA and LAKSMANA walk in single file along a path through a vast misty ancient forest with giant roots, waterfalls and shafts of light; in the distance a small hermitage with sages waving.",
 "Slow lateral tracking beside the walkers",["mist rolls between huge trunks","the three walk forward steadily","Rama pauses and greets the distant sages"],"serangga, air terjun")
s("S12","Hutan","kisah",[A,H],"PONDOK DI PANCHAWATI",["RAMA","SINTA","LAKSMANA"],
 "Akhirnya mereka membangun pondok di Panchawati, di tepi Sungai Godawari. Tempatnya indah dan tenang. Tak seorang pun menyangka, di sinilah badai dimulai.",
 "A charming thatched leaf cottage by a wide river with lotus flowers at golden sunrise; LAKSMANA ties bamboo on the roof, SINTA waters flowering plants, RAMA sits sharpening an arrow, deer in the background.",
 "Slow crane down from the river to the cottage",["the river sparkles and birds fly","Sinta pours water and Laksmana ties the bamboo","Rama looks up as a shadow of cloud passes"],"sungai, burung")
s("S13","Surpanakha","kisah",[A],"TAMU TAK DIUNDANG",["RAMA","SINTA","LAKSMANA"],
 "Datanglah Surpanakha, adik Rahwana, raja negeri Alengka. Ia jatuh hati pada Rama. Ditolak, ia menyerang Sinta, lalu Laksmana melukai wajahnya atas perintah Rama.",
 "Tense moment outside the cottage: a tall wild demoness with ash-brown skin, fiery eyes, dark red garments and long claws lunges toward SINTA; RAMA shields Sinta with his arm while LAKSMANA steps between with his sword raised, no blood.",
 "Quick but smooth push-in",["the demoness raises her claws and leaves swirl","Laksmana steps forward with sword raised and Rama pulls Sinta back","the demoness recoils, covering her face with her sleeve"],"geraman, angin kencang")
s("S14","Surpanakha","kisah",[A],"ADUAN KE ALENGKA",["RAHWANA"],
 "Surpanakha mencari balasan. Pasukan saudaranya dikalahkan Rama. Maka ia menghadap Rahwana di Alengka, dan menyebut satu hal yang memancing: kecantikan Sinta.",
 "Magnificent dark golden throne hall of Alengka with red braziers; RAHWANA sits on a huge throne leaning forward with interest, while the wild demoness in red kneels covering part of her face with her veil and gestures as if describing a vision of a beautiful woman in glowing smoke.",
 "Slow push-in toward Rahwana's face",["braziers flare and smoke curls into a woman's soft silhouette","Rahwana leans forward, eyes fixed on the smoke","a slow proud smile appears on his face"],"api, gong rendah")
s("S15","Rusa emas","kisah",[A],"RENCANA LICIK",["RAHWANA"],
 "Rahwana tidak mau berhadapan langsung. Ia mendatangi Marica, raksasa yang pandai berubah rupa. Marica sudah memperingatkan: jangan ganggu Rama. Tetapi Rahwana mengancam.",
 "A rocky seaside hermitage at dusk: a thin elderly shape-shifter demon with grey skin and simple dark robe raises both palms in warning, while RAHWANA towers over him pointing, his flying chariot resting behind.",
 "Slow low-angle push-in",["waves crash and the old demon shakes his head","Rahwana points sternly and his cloak billows","the old demon lowers his hands in defeat"],"ombak, genderang")
s("S16","Rusa emas","kisah",[A],"KIJANG EMAS",["SINTA"],
 "Marica terpaksa setuju. Ia menjelma menjadi kijang emas berbintik perak, lalu berkeliaran di depan pondok. Sinta terpikat dan meminta Rama menangkapnya.",
 "A dazzling golden deer with silver spots and jewel-like antlers stands in a sunlit flower meadow near the cottage; SINTA in the foreground holds flowers and looks at it with wonder.",
 "Slow push-in from Sinta toward the deer",["the deer lifts its head and its coat shimmers","Sinta steps forward and points with delight","the deer turns and takes a few graceful steps away"],"gemerincing halus")
s("S17","Rusa emas","kisah",[A],"LAKSMANA CURIGA",["RAMA","LAKSMANA","SINTA"],
 "Laksmana curiga itu tipuan. Rama tahu risikonya, tetapi tetap mengejar. Ia berpesan tegas kepada adiknya: jaga Sinta baik-baik, jangan sampai lengah.",
 "Beside the cottage LAKSMANA whispers a warning to RAMA while pointing to the distant golden deer; Rama holds his bow and places a firm hand on Laksmana's shoulder; SINTA watches from the doorway.",
 "Slow push-in on the two brothers",["Laksmana points toward the glittering deer","Rama places his hand on his brother's shoulder","Rama turns and takes his first step toward the forest"],"nada waspada")
s("S18","Rusa emas","kisah",[A],"JERITAN PALSU",["RAMA"],
 "Jauh di dalam hutan, panah Rama mengenai kijang itu. Sebelum tumbang, Marica kembali ke wujud asli dan menjerit meniru suara Rama: tolong aku, Laksmana!",
 "Deep dark forest: RAMA stands with his bow lowered after shooting; ahead the golden deer dissolves into golden light revealing the old grey shape-shifter demon falling to his knees with an open mouth crying out, no blood.",
 "Slow dolly from behind Rama",["golden particles swirl around the deer","the old demon appears in the light and cries out","Rama turns his head back sharply in alarm"],"gema jeritan, angin")
s("S19","Rusa emas","kisah",[A],"DESAKAN SINTA",["SINTA","LAKSMANA"],
 "Sinta panik dan mendesak Laksmana menolong. Laksmana menolak, sampai Sinta menuduhnya dengan kata-kata tajam. Dengan berat hati, ia pun pergi meninggalkan pondok.",
 "At the cottage door SINTA, frightened and tearful, points urgently toward the dark forest; LAKSMANA, hurt and reluctant, grips his bow and looks back at her.",
 "Slow push-in between the two faces",["Sinta points to the forest with trembling hand","Laksmana shakes his head, then his face fills with pain","he turns and walks away looking back once"],"detak genderang")
s("S20","Catatan","versi",["wikipedia_ramayana",A],"SOAL GARIS PELINDUNG",[],
 "Satu catatan penting. Banyak orang mengenal garis pelindung yang digambar Laksmana. Dalam kitab Walmiki, garis itu tidak ada. Ia muncul di versi yang jauh lebih muda.",
 "Close view of the cottage yard at twilight: a faint glowing golden line curves across the earth in front of the doorway like a legend, an old palm-leaf manuscript with abstract unreadable marks lies on a wooden stool in the foreground, oil lamp.",
 "Slow tilt from the manuscript up to the glowing line",["the lamp flickers over the manuscript","the golden line shimmers softly","the line slowly fades into plain earth"],"lembar daun, nada tenang")
s("S21","Penculikan","kisah",[A],"PERTAPA PALSU",["RAHWANA","SINTA"],
 "Saat Sinta sendirian, datang seorang pertapa tua meminta sedekah. Sinta menyambutnya dengan sopan. Tiba-tiba, sang tamu menampakkan wujud aslinya: Rahwana.",
 "At the cottage doorway SINTA offers a bowl of fruit to an old hooded ascetic with a staff; behind the ascetic his giant shadow on the wall and swirling red mist reveal the shape of RAHWANA with many crowned heads.",
 "Slow push-in with the shadow growing",["Sinta offers the bowl politely","the shadow behind the ascetic grows many heads","red mist swirls as Sinta steps back"],"desir gelap, gong")
s("S22","Penculikan","kisah",[A],"JEJAK PERHIASAN",["RAHWANA","SINTA"],
 "Rahwana membawa Sinta terbang. Dari udara, Sinta membungkus beberapa perhiasannya dengan kain, lalu menjatuhkannya ke sebuah bukit tempat para kera duduk.",
 "A majestic golden flying chariot high above clouds and forest hills; SINTA leans over the side dropping a small cloth bundle of gold ornaments, RAHWANA drives with cloak billowing; far below on a rocky hill five small monkeys look up.",
 "Slow tracking alongside the chariot",["clouds rush past and her veil streams","Sinta lets go of the cloth bundle","the bundle falls glinting toward the hill"],"angin, sayap")
s("S23","Jatayu","kisah",[A],"JATAYU MENGHADANG",["JATAYU","RAHWANA","SINTA"],
 "Di langit, Jatayu, burung tua sahabat Dasarata, melihat semuanya. Ia sudah renta, tetapi tetap menghadang. Ia melawan sekuat tenaga, sampai akhirnya jatuh terluka.",
 "Dramatic sky battle: huge JATAYU with spread silver-brown wings swoops in front of the golden flying chariot; RAHWANA raises his sword; SINTA reaches out toward the bird; sunset clouds, no blood.",
 "Slow dynamic orbit",["Jatayu beats his great wings and blocks the chariot","Rahwana swings his sword in a wide arc","Jatayu glides downward with loose feathers drifting"],"kepak sayap, pekik")
s("S24","Jatayu","kisah",[A],"PESAN TERAKHIR",["RAMA","LAKSMANA","JATAYU"],
 "Rama pulang dan mendapati pondok kosong. Dalam pencarian, ia menemukan Jatayu yang sekarat. Setelah memberi kabar, burung setia itu wafat, dan Rama sendiri memakamkannya.",
 "Forest hillside at dusk: RAMA kneels gently cradling the head of the great fallen JATAYU on a bed of leaves, feathers around, LAKSMANA stands behind with bowed head, warm last light.",
 "Slow push-in on Rama and the bird's eye",["Jatayu slowly opens his eye and Rama leans close","the bird rests his head in Rama's hands and closes his eyes","Rama bows his head while feathers drift"],"nada duka, angin")
s("S25","Petunjuk","kisah",[A],"PETUNJUK DARI KABANDHA",["RAMA","LAKSMANA"],
 "Perjalanan berlanjut. Mereka bertemu Kabandha, makhluk raksasa tanpa kepala. Setelah dibebaskan Rama, ia memberi petunjuk penting: carilah Sugriwa, raja kera yang terbuang.",
 "A giant headless forest creature with a single glowing eye on its chest and very long arms transforms into a radiant celestial being rising from golden fire, pointing toward distant mountains; RAMA and LAKSMANA watch below.",
 "Slow tilt up with the rising light",["golden fire swirls around the creature","a shining celestial figure rises from the glow","he points toward the far mountain"],"gemuruh, lonceng")
s("S26","Petunjuk","kisah",[A],"SAMBUTAN SABARI",["RAMA","LAKSMANA"],
 "Mereka juga singgah di pertapaan Sabari, perempuan tua yang saleh. Dengan tulus ia menyambut Rama dengan buah hutan. Lalu keduanya berjalan menuju gunung tempat Sugriwa.",
 "A tiny flower-covered hermitage by a lotus lake: an elderly saintly woman with white hair and bark-cloth sari, SABARI, offers forest berries on a leaf plate to RAMA, who accepts with a warm smile, LAKSMANA beside him.",
 "Slow push-in on the leaf plate and faces",["petals drift over the lake","Sabari raises the leaf plate with shaking hands","Rama takes a berry and smiles warmly"],"air, suling")
s("S27","Hanoman","kisah",[A,H],"HANOMAN DATANG",["HANOMAN","RAMA","LAKSMANA"],
 "Di bukit, Sugriwa melihat dua orang bersenjata dan mengutus Hanoman memeriksa. Hanoman, kera yang cerdas dan santun, menyapa mereka, lalu langsung percaya pada Rama.",
 "On a rocky mountain path with a deep valley behind, HANOMAN bows on one knee with folded hands before RAMA and LAKSMANA, golden sunlight, Rama extending a hand to lift him.",
 "Slow orbit around Hanoman and Rama",["Hanoman lands softly and kneels","he folds his hands and speaks with respect","Rama reaches out and helps him stand"],"angin gunung, musik hangat")
s("S28","Sekutu","kisah",[A],"SUMPAH DI DEPAN API",["RAMA","SUGRIWA","HANOMAN"],
 "Rama dan Sugriwa bersahabat dengan sumpah di depan api. Sugriwa lalu menunjukkan bungkusan perhiasan yang jatuh dari langit. Rama mengenalinya, dan air matanya menetes.",
 "Night camp in a mountain cave mouth with a sacred fire: RAMA holds an opened cloth with gold ornaments, eyes wet with tears, SUGRIWA sits facing him with a hand on his heart, HANOMAN tends the fire.",
 "Slow push-in on the ornaments in Rama's hands",["fire sparks rise as Sugriwa places his hand on his heart","Rama unfolds the cloth revealing the ornaments","Rama holds an earring close and closes his eyes"],"api unggun")
s("S29","Sekutu","kisah",[A],"SUGRIWA DAN SUBALI",["SUBALI","SUGRIWA"],
 "Sugriwa juga punya luka. Ia pernah dikira merebut takhta, lalu diusir kakaknya, Subali, dan istrinya direbut. Rama berjanji membantunya menghadapi sang kakak.",
 "At the gate of a monkey kingdom carved into red cliffs, powerful SUBALI points sternly outward from a high step with a crown, while SUGRIWA walks away downhill looking back sadly.",
 "Slow pull-back from the cliff gate",["Subali raises his arm and points away","Sugriwa walks down the steps","he pauses and looks back with sorrow"],"genderang suku")
s("S30","Sekutu","kisah",[A],"PANAH DARI BALIK POHON",["RAMA","SUBALI","SUGRIWA"],
 "Saat dua bersaudara itu berduel, Rama memanah Subali dari balik pohon. Subali menegurnya. Rama menjawab dengan hukum bagi raja. Sampai kini, pembaca masih memperdebatkannya.",
 "Forest arena: in the mid-ground SUBALI and SUGRIWA wrestle, in the foreground RAMA half hidden behind a huge tree draws his bow with a serious conflicted expression, no arrow impact, no blood.",
 "Slow rack focus from Rama to the duel",["the two monkey kings grapple and dust rises","Rama draws the bowstring slowly","he holds the aim, face troubled and still"],"benturan, tegang")
s("S31","Pencarian","kisah",[A],"CINCIN UNTUK HANOMAN",["RAMA","HANOMAN"],
 "Pasukan kera disebar ke empat arah. Kepada Hanoman, yang menuju selatan, Rama menitipkan cincinnya. Itu tanda, supaya Sinta tahu utusan ini benar-benar dari suaminya.",
 "Morning on a mountain ledge with thousands of monkey soldiers setting off in the valley: RAMA places a gold ring into HANOMAN's open palm, both looking at it solemnly.",
 "Slow macro push-in on the ring",["the army moves in the valley far below","Rama lays the ring into Hanoman's palm","Hanoman closes his fist over it against his chest"],"terompet kerang")
s("S32","Lautan","kisah",[A],"KEKUATAN YANG TERLUPA",["HANOMAN"],
 "Di pantai selatan, mereka buntu di depan lautan. Burung tua Sampati memberi tahu: Sinta ada di Alengka. Lalu tetua kera, Jambawan, mengingatkan Hanoman siapa dirinya.",
 "Wide dramatic seashore with enormous ocean: an old wise bear-like elder with grey fur places a paw on the shoulder of HANOMAN, who looks across the sea; on a cliff above an old vulture with burnt wings looks toward a faint island on the horizon.",
 "Slow push-in toward Hanoman looking at the sea",["waves roll and the old vulture lifts his head","the bear elder speaks with his paw on Hanoman's shoulder","Hanoman lifts his chin and his eyes brighten"],"ombak besar")
s("S33","Lautan","kisah",[A],"LOMPATAN HANOMAN",["HANOMAN"],
 "Hanoman membesarkan tubuhnya dan melompat melintasi lautan. Rintangan datang silih berganti. Dengan mengubah ukuran tubuh dan memakai akal, ia lolos, lalu tiba di Alengka.",
 "Colossal HANOMAN leaping high over a turquoise stormy ocean with the mountain behind him cracking, a huge sea serpent rising from the waves below, a golden island city glowing far ahead, tail streaming.",
 "Epic slow tracking with Hanoman in flight",["Hanoman soars forward with wind rippling his fur","the sea serpent rises below and he twists past","the golden island grows larger ahead"],"angin deras, gong")
s("S34","Alengka","kisah",[A],"BERTEMU SINTA",["HANOMAN","SINTA"],
 "Hanoman menemukan Sinta di taman asoka, sedih dan dijaga para raksasi. Diam-diam ia menyerahkan cincin Rama. Untuk pertama kalinya, Sinta kembali punya harapan.",
 "Moonlit ashoka garden full of orange blossoms: SINTA sits on the ground in a simple faded pink sari, a small HANOMAN on a low branch gently offers the gold ring; sleeping guard demonesses in the dim background.",
 "Slow push-in on the ring and Sinta's face",["blossoms fall in moonlight","Hanoman reaches down with the ring","Sinta takes it and her eyes fill with hope"],"malam, suling lirih")
s("S35","Alengka","kisah",[A],"BIAR RAMA YANG DATANG",["HANOMAN","SINTA"],
 "Hanoman menawarkan menggendongnya pulang. Sinta menolak. Ia tak ingin menyentuh lelaki lain, dan ia ingin Rama sendiri yang datang menjemput dengan terhormat.",
 "In the ashoka garden SINTA stands upright and dignified, gently raising her palm to decline, the ring on her finger, while HANOMAN kneels before her listening respectfully, dawn light beginning.",
 "Slow orbit around Sinta",["dawn light touches the blossoms","Sinta raises her palm gently","Hanoman bows his head with respect"],"nada anggun")
s("S36","Alengka","kisah",[A],"ALENGKA TERBAKAR",["HANOMAN"],
 "Hanoman sengaja membuat keributan sampai ditangkap. Ekornya dibakar. Justru dengan ekor menyala itu ia melompati atap demi atap, membakar Alengka, lalu pulang membawa kabar.",
 "HANOMAN leaping between golden palace rooftops of Alengka at night with the tip of his long tail blazing like a torch, roofs catching orange fire, smoke, no people harmed visible, sea in the background.",
 "Slow tracking following the leap",["flames dance at the tip of his tail","he springs from one roof to the next","he looks back at the glowing city against the night sea"],"api berkobar")
s("S37","Perang","kisah",[A],"WIBISANA MENYEBERANG",["WIBISANA","RAHWANA"],
 "Di Alengka, Wibisana, adik Rahwana, menasihati agar Sinta dikembalikan. Rahwana malah menghinanya. Wibisana memilih pergi, dan bergabung dengan pihak Rama.",
 "Throne hall council: WIBISANA stands with open palms speaking calmly while RAHWANA rises from the throne in anger pointing away; ministers look down.",
 "Slow push-in on Wibisana",["Wibisana speaks with open hands","Rahwana stands and points sharply","Wibisana bows, turns and walks toward the light of the doorway"],"gong, langkah")
s("S38","Perang","kisah",[A,"jurnal_bahastra"],"JEMBATAN DI LAUTAN",["RAMA","HANOMAN","SUGRIWA"],
 "Pasukan tiba di pantai. Dipimpin Nala, para kera membangun jembatan dari batu dan pohon. Orang Jawa mengenal kisah ini sebagai Rama Tambak, artinya Rama membendung laut.",
 "Spectacular sunrise over the ocean: thousands of monkey workers carrying boulders and trunks build a long stone bridge toward the island fortress; RAMA, HANOMAN and SUGRIWA watch from a rock in the foreground.",
 "Slow crane rise revealing the bridge",["monkeys pass boulders in a long line","splashes rise as stones are placed","the finished span glows toward the island"],"batu jatuh, sorak")
s("S39","Perang","kisah",[A],"RAHWANA DISURUH PULANG",["RAMA","RAHWANA"],
 "Perang pecah. Saat Rahwana turun sendiri, Rama menghancurkan kereta dan mahkotanya. Melihat musuhnya kelelahan, Rama menyuruhnya pulang, memulihkan tenaga, baru bertarung lagi.",
 "Battlefield at dusk: an exhausted RAHWANA kneels beside his broken chariot, his crown fallen on the ground; RAMA stands facing him with his bow lowered, gesturing calmly toward the city, banners and dust, no blood.",
 "Slow low-angle push-in",["dust settles around the broken chariot","Rama lowers his bow","Rama gestures toward the city as Rahwana lifts his eyes"],"angin medan, genderang pelan")
s("S40","Perang","kisah",[A],"KUMBAKARNA MAJU",["KUMBAKARNA","RAHWANA"],
 "Adik Rahwana yang lain, Kumbakarna, dibangunkan dari tidur panjang. Ia menegur kakaknya, tetapi tetap maju demi saudara dan negerinya. Ia pun gugur.",
 "Giant KUMBAKARNA rises from an enormous bed in a vast cavern-like hall, small drummers and attendants around him, RAHWANA standing at the foot of the bed; warm torchlight.",
 "Slow tilt up the giant",["drums are struck and the giant opens his eyes","he sits up and looks seriously at Rahwana","he places a hand on his armour with resolve"],"genderang besar, dengkur lalu hening")
s("S41","Perang","kisah",[A],"PANAH ULAR INDRAJIT",["INDRAJIT","RAMA","LAKSMANA"],
 "Putra Rahwana, Indrajit, melepaskan panah ular yang mengikat Rama dan Laksmana. Burung raksasa Garuda datang membebaskan mereka. Kelak, Indrajit gugur di tangan Laksmana.",
 "RAMA and LAKSMANA sit bound by glowing magical serpent coils of light on the battlefield; the golden eagle Garuda descends with huge wings as the serpents recoil; INDRAJIT watches from a cloud above.",
 "Slow push-in from above",["serpent coils of light tighten and glow","Garuda sweeps down with radiant wings","the coils burst into sparks and the brothers rise"],"desis, kepak agung")
s("S42","Puncak","kisah",[A],"DUEL TUJUH HARI",["RAMA","RAHWANA"],
 "Akhirnya Rama berhadapan dengan Rahwana. Menurut Walmiki, duel itu berlangsung berhari-hari. Setiap kepala Rahwana yang terlepas, tumbuh lagi. Senjata biasa tidak cukup.",
 "Epic duel between two flying war chariots at sunset: RAMA on a celestial golden chariot drawing his bow, RAHWANA on a dark chariot with all his crowned heads glowing, arrows of light crossing, storm clouds.",
 "Slow circling camera between the chariots",["arrows of light cross the sky","Rahwana's heads flare with red light","Rama steadies his bow and breathes"],"dentuman, paduan genderang")
s("S43","Puncak","kisah",[A],"PANAH BRAHMA",["RAMA","RAHWANA"],
 "Rama lalu melepaskan panah Brahma, senjata pemberian dewa pencipta. Panah itu menembus dada Rahwana. Raja Alengka gugur, dan hujan bunga turun ke kereta Rama.",
 "A blazing golden arrow of light flies from RAMA's bow toward the distant silhouette of RAHWANA; flower petals begin raining from golden clouds onto Rama's chariot, no wound visible, no blood.",
 "Slow push following the arrow of light",["Rama releases the glowing arrow","a bright burst of golden light fills the distance","flower petals shower down over Rama's chariot"],"desing panah, lonceng surgawi")
s("S44","Sesudah perang","kisah",[A],"PERMUSUHAN BERAKHIR",["RAMA","WIBISANA"],
 "Mandodari, istri Rahwana, meratap. Wibisana ragu mengurus jenazah kakaknya. Rama berkata, permusuhan selesai bersama kematian. Maka upacara penghormatan pun digelar dengan layak.",
 "Quiet twilight battlefield: RAMA places a hand on WIBISANA's shoulder; beyond them a grieving queen in white kneels beside a royal bier covered with a red-gold cloth and flowers, oil lamps.",
 "Slow push-in on the two men",["lamps flicker beside the covered bier","Rama rests his hand on Wibisana's shoulder","Wibisana bows his head and nods"],"nada hening")
s("S45","Ujian","kisah",[A],"KATA-KATA YANG MELUKAI",["RAMA","SINTA","HANOMAN"],
 "Sinta akhirnya dibawa menghadap. Namun di depan banyak orang, Rama meragukan kesuciannya, karena ia lama tinggal di istana Rahwana. Sinta sangat terluka.",
 "A wide open ground before the army: SINTA stands alone in the centre with tearful dignified face; RAMA stands apart looking away with a heavy conflicted expression; HANOMAN and soldiers look on in shock.",
 "Slow push-in on Sinta",["wind moves her veil","Rama turns his face aside","Sinta lifts her chin through her tears"],"angin sunyi")
s("S46","Ujian","kisah",[A],"UJIAN API",["SINTA","RAMA"],
 "Sinta meminta api dinyalakan. Ia bersumpah hatinya tidak pernah berpaling, lalu masuk ke dalamnya. Agni, dewa api, keluar membawanya utuh dan menyatakan ia suci.",
 "A great golden ceremonial fire; from its heart a radiant god of fire with a flaming halo gently leads SINTA out, completely unharmed and glowing, her garlands fresh; RAMA steps forward in awe.",
 "Slow push-in into the golden light",["flames rise in a soft golden swirl","the fire god emerges guiding Sinta forward unharmed","Rama steps toward her with relief"],"api, paduan suara lembut")
s("S47","Jawa","versi",["brin_prambanan","wikipedia_ramayana"],"VERSI YANG BERBEDA",[],
 "Tidak semua versi sama. Kakawin Ramayana dari Jawa Kuno, menurut kajian arkeologi, tidak memuat ujian api itu. Sementara di Prambanan, kisah penculikan Sinta dipahat di batu.",
 "Prambanan temple in Central Java at golden hour with its tall carved stone spires; in the foreground a close carved andesite relief panel showing a flying demon king carrying a woman while a great bird attacks.",
 "Slow pan from the relief to the temple",["golden light slides across the carved stone","the focus shifts from relief to the spires","birds cross the evening sky"],"gamelan Jawa pelan")
s("S48","Penutup","kisah",[A],"PULANG KE AYODHYA",["RAMA","SINTA","LAKSMANA","HANOMAN","BHARATA"],
 "Empat belas tahun genap. Rama, Sinta, dan Laksmana pulang. Bharata menyerahkan kembali kerajaan, dan Rama dinobatkan. Menurutmu, sudah adilkah Rama kepada Sinta? Tulis di komentar.",
 "Joyful coronation night in Ayodhya: RAMA and SINTA in magnificent royal attire seated on a golden throne, LAKSMANA holding a white umbrella, HANOMAN kneeling, Bharata presenting the sandals, thousands of oil lamps and fireworks over the city.",
 "Slow grand pull-back over the city",["thousands of lamps flicker","Bharata bows and presents the sandals","Sinta looks quietly toward the lamps with a thoughtful face"],"sorak, gamelan megah")

KATA = lambda t: len(t.split())
dur = {}
if len(sys.argv) > 1:
    dur = json.load(open(sys.argv[1]))
elif os.path.exists("durasi.json"):
    dur = json.load(open("durasi.json"))
IDS = [x[0] for x in S]
assert IDS == [f"S{i:02d}" for i in range(1, len(S)+1)]

ROYAL = {"S01","S05"}
def ref(chars): return ("Use character references: " + ", ".join(chars) + ". ") if chars else ""
def img(x): return f"{x[0]}. {ref(x[5])}{x[7]} {STYLE}."

NEG = ("Negative: no morphing, no warping, no melting, no face change, no identity change, no costume change, no "
       "extra limbs, heads or fingers, no duplicated characters, no new characters or objects appearing, no "
       "disappearing objects, no style change, no flicker, no sudden zoom, no shaky or spinning camera, no scene "
       "cut, no dissolve, no crossfade, no double exposure, no talking, no lip-sync, no blood, no gore, no text, "
       "no letters, no subtitles, no logo, no watermark.")
def klip(x):
    if x[0] in dur: return max(5, math.ceil(dur[x[0]] + 0.4)), dur[x[0]], True
    e = KATA(x[6]) / 2.3
    return max(5, math.ceil(e + 0.5)), round(e, 2), False

meta = {"part":3,"judul_kerja":"Ramayana inti: Rama terbuang, Sinta diculik, perang Alengka",
 "judul":"Kisah Rama dan Sinta: Dibuang, Diculik, Direbut Kembali",
 "judul_varian":["Kisah Rama dan Sinta: Dibuang, Diculik, Direbut Kembali",
   "Kenapa Rama Mau Dibuang 14 Tahun? Inti Kisah Ramayana",
   "Ramayana: Pengasingan Rama sampai Rahwana Gugur"],
 "format":"panjang","pilar":"Sejarah kelam & kisah kuno (mitologi sebagai catatan kepercayaan)","playlist":"Sejarah Sisi Gelap",
 "peta_3_poin":["Kenapa Rama menerima pengasingan.","Bagaimana Sinta diculik.","Bagaimana Sinta direbut kembali lewat perang."],
 "momen_jawaban_detik":55,"thumbnail_teks":"RAMA DIBUANG, SINTA DICULIK","thumbnail_objek":"kijang emas",
 "kata_kunci_utama":"Kisah Rama dan Sinta"}
old = json.load(open("scenes.json", encoding="utf-8"))
src = old["sumber"]
src.setdefault("jurnal_bahastra", {"atribusi":"Jurnal Bahastra UAD, Simbol Rama","tahun":0,"url":"https://pbsi.uad.ac.id/wp-content/uploads/SIMBOL-RAMA-JURNAL-BAHASTRA.pdf","jenis":"sekunder"})
scenes = []
for x in S:
    i,bag,kelas,sumber,layar,chars,vo,gbr,cam,aksi,sfx = x
    for k in sumber: assert k in src, (i,k)
    scenes.append({"id":i,"bagian":bag,"kelas":kelas,"keyakinan":None,"sumber":sumber,"vo":vo,"on_screen":layar,
        "sfx":sfx,"karakter":chars,"flow_subject":gbr,"cam_en":cam,"beat1":aksi[0],"beat2":aksi[1],"beat3":aksi[2]})
json.dump({"meta":meta,"sumber":src,"scenes":scenes}, open("scenes.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
open("vo_satu_take.txt","w",encoding="utf-8").write("\n\n".join(x[6] for x in S)+"\n")

pg = ["# Prompt gambar Flow, Ramayana Part 3 (16:9, Nano Banana)","","## Gaya (sudah menyatu di tiap prompt)",STYLE,"","## Character lock"]
for k,v in CHARS.items(): pg.append(f"- **{k}**: {v}")
pg += ["","## Scene"]
for x in S: pg += [f"### {x[0]} · {x[4]}", img(x), ""]
open("prompt_gambar.md","w",encoding="utf-8").write("\n".join(pg))

fb = ["Create CHARACTER LOCK reference images first, then immediately generate every scene without stopping to ask.",
      "Image model Nano Banana, aspect 16:9, exactly 1 image per prompt.",
      f"Step 1: generate one full-body reference sheet for each character below, on a plain soft backdrop, titled CHAR_<NAME>. Style for all: {STYLE}.", ""]
for k,v in CHARS.items(): fb.append(f"CHAR_{k}: {v}.")
fb += ["", f"Step 2: generate all {len(S)} scenes below in one batch, using the matching CHAR references as ingredients so faces and costumes stay identical. Title each image exactly with its code S01 to S{len(S):02d}.",
       f"Style appended to every scene: {STYLE}.", ""]
for x in S: fb.append(f"{x[0]}. {ref(x[5])}{x[7]}")
open("flow_blast.txt","w",encoding="utf-8").write("\n".join(fb))

sb = ["# Storyboard Ramayana Part 3", "", "| Scene | Bagian | Durasi klip | Narasi (VO) | Gambar (ringkas) | Kamera | Teks layar | Suara latar |", "|---|---|---|---|---|---|---|---|"]
pv = ["# Prompt video Ramayana Part 3 (Nexabot: Start Frame to Video, Landscape 16:9, 1080p, tanpa suara)", "",
      "Durasi " + ("DIUKUR dari VO asli." if dur else "PERKIRAAN dari jumlah kata; diganti setelah VO diukur."), "",
      "| Scene | Slider durasi | VO (dtk) |", "|---|---|---|"]
body = []; tot_k = 0; tot_v = 0
for x in S:
    i = x[0]; d, v, ukur = klip(x); tot_k += d; tot_v += v
    sb.append(f"| {i} | {x[1]} | {d} dtk | {x[6]} | {x[7]} | {x[8]} | {x[4]} | {x[10]} |")
    pv.append(f"| {i} | {d} dtk | {v:.2f} |")
    a,b = round(d/3), round(2*d/3)
    body += [f"## {i} · {x[4]} · {d} detik", "", f"VO: {x[6]}", "", "```",
      f"{i} — Animate the provided start frame as a cinematic realistic 3D film shot, landscape 16:9, {d} seconds, one continuous shot, no cuts. "
      f"Keep every character, face, costume, prop, colour and background exactly as in the start frame. "
      f"Camera: {x[8]}, very smooth with soft ease-in and ease-out, small movement only. "
      f"Action: 0-{a}s {x[9][0]}; {a}-{b}s {x[9][1]}; {b}-{d}s {x[9][2]}. "
      f"Movements are slow, natural and physically believable, with gentle secondary motion in hair, fabric, leaves and light; the last second is calm and stable. "
      f"Characters do not speak. Silent video, no voice, no music. {NEG}", "```", ""]
pv += ["", f"Total klip {tot_k} dtk; total VO {tot_v:.1f} dtk ({tot_v/60:.1f} menit).", ""] + body
open("storyboard.md","w",encoding="utf-8").write("\n".join(sb)+"\n")
open("prompt_video.md","w",encoding="utf-8").write("\n".join(pv))
w = [KATA(x[6]) for x in S]
print(len(S), "scene,", sum(w), "kata, kata/scene", min(w), max(w), "| est VO", round(tot_v/60,2), "menit | flow_blast", len(open("flow_blast.txt").read()), "karakter")
