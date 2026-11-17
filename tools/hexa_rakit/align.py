import re,json
T=open('/home/claude/pulangngantor/data/produksi/2026-11-17/vo_satu_kali.txt').read().strip().split('\n\n')
P=[tuple(map(float,l.split())) for l in open('sil.txt')]
# speech start/end
s0=P[0][1] if P[0][0]<0.1 else 0.0
P=[p for p in P if p[0]>0.1]
end=399.8
if P[-1][1]>=end-0.05: endsp=P[-1][0]; P=P[:-1]
else: endsp=end
L=[len(p) for p in T]; tot=sum(L); rate=(endsp-s0)/tot
n=len(P);K=len(T)-1
INF=1e18
import functools
# dp[k][j]: best cost with k-th boundary at pause j
mid=[(a+b)/2 for a,b in P]
def cost(a,b,i):  # paragraph i from time a to b
    e=L[i]*rate; return ((b-a)-e)**2/e
dp=[[INF]*n for _ in range(K)];bk=[[-1]*n for _ in range(K)]
for j in range(n):
    dp[0][j]=cost(s0,P[j][0],0)-8*(P[j][1]-P[j][0])
for k in range(1,K):
    for j in range(n):
        g=8*(P[j][1]-P[j][0])
        for q in range(j):
            v=dp[k-1][q]+cost(P[q][1],P[j][0],k)-g
            if v<dp[k][j]: dp[k][j]=v;bk[k][j]=q
best=min(range(n),key=lambda j:dp[K-1][j]+cost(P[j][1],endsp,K))
ch=[best]
for k in range(K-1,0,-1): ch.append(bk[k][ch[-1]])
ch=ch[::-1]
segs=[];a=s0
for i,j in enumerate(ch):
    segs.append((a,P[j][0],P[j][1]-P[j][0])); a=P[j][1]
segs.append((a,endsp,0))
for i,(a,b,g) in enumerate(segs):
    print(f"S{i+1:02d} {a:7.2f}-{b:7.2f} dur {b-a:5.2f} exp {L[i]*rate:5.2f} gap {g:.2f}")
json.dump({'segs':segs,'pauses':P,'s0':s0,'end':endsp},open('align.json','w'))
print('long pauses sorted',sorted([round(b-a,2) for a,b in P])[-30:])
