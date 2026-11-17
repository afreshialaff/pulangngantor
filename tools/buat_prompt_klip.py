#!/usr/bin/env python3
"""Menulis prompt_video.md: tiap scene = satu blok siap-salin (aturan umum + negative ada di tiap blok)."""
import json, sys
folder = sys.argv[1]
d = json.load(open(f"{folder}/storyboard.json"))
scenes = {s["id"]: s for s in d["scenes"]}

RULES = ("GENERAL RULES: 15-second clip, 16:9, 24fps. Use the attached image as the exact first frame and keep its composition, "
 "framing, colors and lighting for the whole clip. Cinematic noir mood, 35mm film grain, deep midnight navy and black shadows, "
 "single warm amber light source, archival texture. Slow, smooth, deliberate motion only; the camera moves in one direction at a "
 "steady speed with no sudden changes. Show no readable text, letters, numbers, captions, logos or watermarks; any script or "
 "writing stays abstract and unreadable. No real or recognizable faces; people appear only as hands or silhouettes. "
 "Do not add new objects that are not in the first frame unless described. Keep the last 1 second calm and stable so it can be trimmed or cross-faded.")
NEG = ("NEGATIVE PROMPT: fast cuts, jump cut, shaky camera, handheld shake, whip pan, zoom burst, morphing, warping text, melting objects, "
 "extra fingers, deformed hands, face distortion, glitch, flicker, strobe, lens flare overload, subtitles, captions, watermark, logo, "
 "cartoon, anime, 3D render look, bright saturated colors, overexposed, daylight, blur smear, low resolution")

# (kamera, gerak detail 0-5 / 5-10 / 10-15, suasana audio ref)
EN = {
"S01": ("Slow steady dolly-in, eye level, starting wide on the desk and ending close on the open pages.",
 "Camera glides forward toward the old open codex. Dust motes drift through the amber lamp beam. The lamp flickers very softly once.",
 "Dust keeps drifting; the lamp glow steadies. The dark window reflection of the office slowly shifts a few centimeters.",
 "Camera settles on the open pages and stops completely; only dust moves."),
"S02": ("Locked-off close-up, then a gentle slide to the left at the end.",
 "Close-up of the worn vellum cover beside the ruler; nothing moves except a faint breathing of the amber rim light.",
 "A gloved hand (no face, hand only) slowly lifts the cover and opens it a few centimeters.",
 "Camera slides slowly left along the thick page edges, shallow depth of field, then holds."),
"S03": ("Slow horizontal pan from left to right at table level.",
 "Pan drifts across the invented plant illustration card; amber light warms the parchment.",
 "Pan continues past the star diagram and the bathing pools card with pipes.",
 "Pan stops on the jar card and recipe-lines card; the amber light grows slightly stronger, then holds."),
"S04": ("Extreme macro, shallow focus, locked camera then a very slow pull-back.",
 "Macro of lines of invented, unreadable script in dark ink on vellum; grain and fibers visible, raking amber light.",
 "Focus slowly racks from word to word, left to right, along one line of script.",
 "Camera pulls back very slowly revealing the whole paragraph; hold still at the end."),
"S05": ("Slow tilt-up from desk level to the sample.",
 "Camera tilts up from the dark lab bench to a small vellum sample under the amber lamp.",
 "In the blurred background, tiny amber indicator lights on the instruments pulse softly and slowly; nothing readable on screens.",
 "Camera drifts closer to the sample's texture and holds."),
"S06": ("Locked camera with a single slow rack focus.",
 "Focus racks from the stack of old books in the foreground to the open page.",
 "A thin ultraviolet-blue line of light sweeps once, slowly, across the page from left to right.",
 "The blue light fades out completely; only the amber lamp remains. Camera still."),
"S07": ("Slow lateral dolly to the right at shelf level.",
 "Dolly moves past shelves of old jars and books in a 17th-century alchemist's study, candlelight flickering gently.",
 "Candle flames sway slightly; shadows move slowly on the wall.",
 "Camera stops on the old page where a faint, erased signature glows very softly; hold."),
"S08": ("Slow push-in, low angle on the table.",
 "Close-up of the small pile of gold ducats catching the amber candlelight.",
 "Camera drifts to the wax-sealed letter beside the coins.",
 "Candlelight dims partially, the coins keep a soft glint; camera stops."),
"S09": ("Slow side-tracking shot following the hand.",
 "A hand only (no face) writes on a letter with a quill, ink dripping very slightly.",
 "The hand folds the letter and presses a wax seal; amber candle glow on the wax.",
 "Camera follows the sealed letter as it is placed on a small stack; hold on the stack."),
"S10": ("Slow pan to the right following the street.",
 "A wrapped package is slid into the courier's saddlebag next to the sealed letter; moonlight on stone.",
 "Camera pans along the wet cobblestone street toward the distant Rome rooftops.",
 "The amber lantern light shrinks into the distance as the camera settles; hold."),
"S11": ("Slow forward dolly down the corridor, centered.",
 "Dolly moves along a vast dim library corridor between towering bookshelves, dust floating in the lantern light.",
 "Camera discovers the rare-book dealer's trunk in the corner of the frame.",
 "The trunk lid opens a little and soft amber light spills out; camera stops."),
"S12": ("Locked-off shot, then a slow tilt-up.",
 "A sealed archival box on a reading-room table, perfectly still, long shadows.",
 "Camera tilts up slowly toward the large glass windows of the reading room.",
 "Amber desk lamps in the room switch on one by one, softly; hold on the final frame."),
"S13": ("Slow push-in, slightly high angle over the desk.",
 "Stacks of papers with invented, unreadable cipher tables on the desk under an amber lamp.",
 "The rotors of the vintage cipher machine turn slowly, one click at a time.",
 "Camera moves closer to a sheet covered in red pencil marks, then freezes."),
"S14": ("Locked-off macro, top-down, perfectly stable.",
 "A hand-drawn bar chart of descending bars on aged paper, lit from the side by amber light.",
 "A red pencil draws a circle around the first and second bars, slowly (pencil may be seen, no hand face).",
 "A third red circle is drawn; the pencil rests on the paper. Camera does not move."),
"S15": ("Slow pan to the left across the board.",
 "The investigation board with red strings between index cards and invented plant sketches, amber lamp glow at the left.",
 "Camera follows one red string from card to card, strings sway very slightly.",
 "Camera stops on one blank index card in the middle; hold."),
"S16": ("Locked camera with a slow rack focus.",
 "Two aged paper strips side by side, one chaotic pattern, one overly regular, under amber light.",
 "Focus racks slowly from the chaotic strip to the regular strip.",
 "The amber lamp dims slightly; the regular strip stays in focus; hold."),
"S17": ("Slow push-in on the table.",
 "A table of invented syllables written on parchment, amber lamp light, dark workshop.",
 "A perforated card is lowered slowly onto the table, covering most of the syllables.",
 "Fragments of words show through the holes of the card; camera stops completely."),
"S18": ("Slow lateral dolly through a dark room.",
 "Faint invented scripts appear softly on the dark walls, abstract and unreadable.",
 "Camera dollies past the empty desk and amber lamp.",
 "One script glyph on the wall glows amber then fades slowly; hold in the dark."),
"S19": ("Locked-off shot, then a slow zoom-out.",
 "A newspaper page (no readable headlines) pinned on a corkboard under an amber desk lamp.",
 "A hand (no face) pulls the page off the board; the torn edge stays on the pin.",
 "Only an empty pin remains on the corkboard; camera zooms out slowly and holds."),
"S20": ("Slow push-in at desk level.",
 "Ten index cards with invented plant labels lie on the desk beside a magnifying glass.",
 "The magnifying glass slides slowly over a card, amber light refracting through it.",
 "The empty chair behind the desk fills the frame; the lamp dims slowly; hold."),
"S21": ("Slow tilt from the floor up to the desks.",
 "A row of empty scriptorium writing desks in the dark.",
 "Shadows of hands moving as if writing appear softly on the wall behind the desks.",
 "Small amber lamps on the desks light up one by one; hold on the last frame."),
"S22": ("Slow pan to the right across the board.",
 "An office investigation board divided into three zones, amber lamp light.",
 "Red strings on the left zone pull taut and straight (solid evidence).",
 "Loose index cards on the right zone sway gently (conjecture); camera holds."),
"S23": ("Slow dolly forward down the archive aisle, centered.",
 "Rows of filing cabinets labelled with invented symbols line a night office archive room.",
 "Camera passes one folder sticking out of a drawer.",
 "Camera stops facing the single amber lamp at the far end of the aisle; hold."),
"S24": ("Locked-off macro, then a slow pull-back.",
 "Macro of a plant drawing with small invented, unreadable labels, amber raking light, parchment grain.",
 "Focus moves gently from label to label.",
 "Camera pulls back slowly to reveal many labels around the drawing; hold."),
"S25": ("Slow, gentle push-in toward the desk.",
 "The open codex on the lone desk in a dark office, the night city faintly visible through the window.",
 "Camera drifts closer; the lamp glow breathes very subtly.",
 "Amber light settles on one page, the rest falls into shadow; hold."),
"S26": ("Slow pull-back from the desk to a wide shot.",
 "The amber desk lamp slowly dims; the codex is a faint silhouette.",
 "Camera pulls back, revealing the empty dark office and city lights through the window.",
 "The scene fades toward navy darkness, only distant city lights remain; hold."),
}

out = []
out.append("# Prompt video siap-salin — Pulang ngantor: Naskah Voynich\n")
out.append("Cara pakai: untuk tiap scene, unggah gambar S## yang sudah di-upscale sebagai first frame, lalu salin SELURUH isi blok di bawah judul scene itu (aturan umum dan negative sudah ada di tiap blok). Durasi generate: 15 detik. Potong ekor klip ke 'Durasi pakai' setelah VO final diukur.\n")
out.append("| Scene | Generate | Durasi pakai (perkiraan) |\n|---|---|---|")
for sid, s in scenes.items():
    out.append(f"| {sid} | 15 dtk | {s['durasi_pakai']} dtk |")
out.append("")
for sid, s in scenes.items():
    cam, a, b, c = EN[sid]
    subject = s["flow_prompt"].split(". Style:")[0]
    out.append(f"## {sid} — {s['bagian']} (generate 15 dtk, pakai ~{s['durasi_pakai']} dtk)\n")
    out.append("```")
    out.append(f"FIRST FRAME: image {sid} (attached). Scene: {subject}.")
    out.append(f"DURATION: 15 seconds. ASPECT: 16:9.")
    out.append(f"CAMERA: {cam}")
    out.append(f"SECONDS 0-5: {a}")
    out.append(f"SECONDS 5-10: {b}")
    out.append(f"SECONDS 10-15: {c}")
    out.append(f"AMBIENT FEEL (for mood only, no sound needed): {s['sfx']}.")
    out.append(RULES)
    out.append(NEG)
    out.append("```\n")
open(f"{folder}/prompt_video.md", "w").write("\n".join(out))
print("ok", len(scenes))
