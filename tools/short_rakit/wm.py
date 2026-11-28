"""Bangun peta alpha bintang Gemini dari latar polos (S05, S11), lalu uji pembalikan alpha."""
import cv2, numpy as np, glob

X0, Y0, S = 840, 1680, 120  # kotak yang memuat bintang


def crop(f):
    return cv2.imread(f)[Y0:Y0 + S, X0:X0 + S].astype(np.float32)


def plane_bg(c, mask):
    yy, xx = np.mgrid[0:S, 0:S]
    A = np.stack([np.ones_like(xx), xx, yy, xx * xx, yy * yy, xx * yy], -1).astype(np.float64)
    bg = np.zeros_like(c)
    for k in range(3):
        coef = np.linalg.lstsq(A[~mask], c[..., k][~mask], rcond=None)[0]
        bg[..., k] = A @ coef
    return bg


# topeng kasar bintang dari S11 (latar gelap rata)
c = crop('wm/S11_4.png')
base = np.median(c.reshape(-1, 3), 0)
rough = (np.abs(c - base).max(-1) > 6).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(rough)
big = 1 + np.argmax(st[1:, 4])
rough = (lab == big).astype(np.uint8)
print('bintang bbox', st[big])
mask = cv2.dilate(rough, np.ones((9, 9), np.uint8)) > 0
alphas = []
for f in sorted(glob.glob('wm/S05_*.png') + glob.glob('wm/S11_*.png')):
    c = crop(f)
    bg = plane_bg(c, mask)
    a = ((c - bg) / np.maximum(255 - bg, 1)).mean(-1)
    alphas.append(a)
alpha = np.median(np.stack(alphas), 0)
alpha[~mask] = 0
alpha = np.clip(alpha, 0, 0.9)
np.save('alpha.npy', alpha.astype(np.float32))
print('alpha maks', alpha.max(), 'median inti', np.median(alpha[rough > 0]))
