from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import numpy as np
f = Image.open('S01_2.png').convert('RGB').crop((0, 290, 1080, 1100)).resize((960, 720), Image.LANCZOS)
f = ImageEnhance.Contrast(ImageEnhance.Color(f).enhance(1.15)).enhance(1.12)
base = Image.new('RGB', (1280, 720), (11, 20, 36))
base.paste(f, (320, 0))
x = np.arange(1280, dtype=float)
a = np.clip((600 - x) / 270, 0, 1) ** 1.2
a = Image.fromarray((np.tile(a, (720, 1)) * 255).astype(np.uint8))
base = Image.composite(Image.new('RGB', base.size, (10, 12, 20)), base, a)
d = ImageDraw.Draw(base)
# lingkaran investigasi merah mengelilingi jemuran
S = 3
ov = Image.new('RGBA', (1280 * S, 720 * S))
o = ImageDraw.Draw(ov)
box = [v * S for v in (900, 40, 1215, 650)]
o.arc(box, -75, 268, fill=(214, 40, 40, 255), width=13 * S)
base.paste(ov.resize(base.size, Image.LANCZOS), (0, 0), ov.resize(base.size, Image.LANCZOS))
F = '/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
def text(xy, s, size, fill, stroke=9):
    font = ImageFont.truetype(F, size)
    d.text((xy[0] + 6, xy[1] + 8), s, font=font, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0))
    d.text(xy, s, font=font, fill=fill, stroke_width=stroke, stroke_fill=(10, 10, 10))
    return d.textbbox(xy, s, font=font, stroke_width=stroke)
text((48, 38), 'HANTU...', 168, (233, 217, 197))
d.rounded_rectangle([48, 296, 262, 396], 14, fill=(139, 30, 30))
d.text((155, 345), 'ATAU', font=ImageFont.truetype(F, 76), fill=(233, 217, 197), anchor='mm')
bb = text((48, 420), 'JEMURAN?', 128, (244, 162, 89))
print(bb)
base.save('thumbnail.jpg', quality=93)
