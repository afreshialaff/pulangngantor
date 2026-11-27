import numpy as np,subprocess,json,cv2
T=json.load(open('../asm/timeline.json'))
X0,Y0,S=1660,820,160
fr=[]
for s in T['scenes']:
    r=subprocess.run(['ffmpeg','-v','error','-i',s['clip'],'-vf',f'crop={S}:{S}:{X0}:{Y0},fps=1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    fr+=list(np.frombuffer(r,np.uint8).reshape(-1,S,S,3))
fr=np.array(fr);np.save('crops.npy',fr);print(fr.shape,flush=True)
mn=fr.min(0).astype(np.float32).mean(2)
mask=(mn>25).astype(np.uint8);mask=cv2.dilate(mask,np.ones((9,9),np.uint8))
print('mask px',mask.sum())
A=[]
for f in fr:
    bg=cv2.inpaint(np.ascontiguousarray(f),mask*255,6,cv2.INPAINT_TELEA).astype(np.float32)
    o=f.astype(np.float32);den=255-bg
    A.append(np.where(den>50,(o-bg)/np.maximum(den,1),np.nan))
alpha=np.nan_to_num(np.nanmedian(np.array(A),0));alpha=np.clip(alpha,0,0.95);alpha[mask==0]=0
print('alpha max',alpha.max(),'mean',alpha[mask>0].mean())
np.save('alpha.npy',alpha);np.save('mask.npy',mask)
cv2.imwrite('alpha.png',cv2.resize((alpha*255).astype(np.uint8)[:,:,::-1],(480,480),interpolation=cv2.INTER_NEAREST))
