"""Hapus bintang: balikkan alpha blending putih, lalu haluskan sisa tepi tipis."""
import cv2, numpy as np

X0, Y0, S = 840, 1680, 120
_a = np.load(__file__.rsplit('/', 1)[0] + '/alpha.npy' if '/' in __file__ else 'alpha.npy')
_a3 = _a[..., None]
_b = (_a > 0.06).astype(np.uint8)
_k = lambda n: np.ones((n, n), np.uint8)
_ring = cv2.dilate(_b, _k(3)) - cv2.erode(_b, _k(3))
_wide = cv2.dilate((_a > 0.05).astype(np.uint8), _k(5)) - cv2.erode((_a > 0.05).astype(np.uint8), _k(5))


def clean(frame):
    roi = frame[Y0:Y0 + S, X0:X0 + S].astype(np.float32)
    rec = np.clip((roi - _a3 * 255) / (1 - _a3), 0, 255).astype(np.uint8)
    # tepi lebar kecuali pada garis gambar yang gelap, agar garis tidak putus
    g = cv2.cvtColor(rec, cv2.COLOR_BGR2GRAY)
    dark = (g < np.median(g) * 0.45).astype(np.uint8)
    keep = cv2.erode(cv2.dilate(dark, _k(3)), _k(3))
    mask = _ring | (_wide & (1 - keep))
    inp = cv2.inpaint(rec, mask, 3, cv2.INPAINT_TELEA)
    frame[Y0:Y0 + S, X0:X0 + S] = inp
    return frame
