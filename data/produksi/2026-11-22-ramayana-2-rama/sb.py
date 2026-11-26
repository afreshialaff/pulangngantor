from vo import VO; from img import S,CHAR,STYLE; from motion import M
sb=["# Storyboard Ramayana Part 2: Rama (awatara Wisnu sampai menjelang penobatan)","","Kelas: fakta = sejarah/naskah; kisah = isi kitab (catatan kepercayaan); versi = tradisi lain.",""]
pg=["# Prompt gambar Flow (Nano Banana, 16:9)","","## Gaya (ditambahkan di setiap scene)",STYLE,"","## Character lock"]+[f"- **{k}**: {v}" for k,v in CHAR.items()]+["","## Scene"]
for sid,bag,kls,vo in VO:
    ch,sc=S[sid]
    sb+= [f"## {sid} · {bag} ({kls})",f"- VO: {vo}",f"- Visual: {sc}",f"- Karakter: {', '.join(ch) or '-'}",f"- Kamera: {M[sid][0]}",""]
    pg+= [f"### {sid}",f"{sid}. "+(f"Use characters: {', '.join(ch)}. " if ch else "")+sc+". "+STYLE,""]
open("storyboard.md","w").write("\n".join(sb)); open("prompt_gambar.md","w").write("\n".join(pg))
