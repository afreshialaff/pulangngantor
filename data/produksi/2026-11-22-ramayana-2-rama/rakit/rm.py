import numpy as np,cv2
alpha=np.load('alpha.npy');mask=np.load('mask.npy')
am=alpha.mean(2)
# sabuk tepi: tempat alpha berubah tajam
g=cv2.morphologyEx((am>0.03).astype(np.uint8),cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8))
band=cv2.dilate(g,np.ones((3,3),np.uint8))
def clean(f):
    o=f.astype(np.float32)
    r=np.clip((o-alpha*255)/(1-alpha),0,255).astype(np.uint8)
    r=cv2.inpaint(r,band*255,3,cv2.INPAINT_TELEA)
    # haluskan sedikit dalam area bintang agar tekstur menyatu
    b=cv2.GaussianBlur(r,(3,3),0);w=(np.clip(am*2.5,0,1))[...,None]*0.5
    return (r*(1-w)+b*w).astype(np.uint8)
