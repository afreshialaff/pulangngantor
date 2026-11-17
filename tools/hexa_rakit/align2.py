import re,json
T=open('/home/claude/pulangngantor/data/produksi/2026-11-17/vo_satu_kali.txt').read().strip().split('\n\n')
A=json.load(open('align.json'));P=A['pauses'];s0=A['s0'];endsp=A['end']
def syl(s): return len(re.findall(r'[aiueoéáčý]+',s.lower()))
S=[];para=[]
for i,p in enumerate(T):
    for x in re.split(r'(?<=[.!?])\s+',p.strip()):
        S.append(x);para.append(i)
Y=[syl(x) for x in S];N=len(S);n=len(P)
rate=(endsp-s0-sum(min(b-a,1) for a,b in P)*0.0)/sum(Y)
# fit rate excluding pauses roughly: total pause time
ptot=sum(b-a for a,b in P); rate=(endsp-s0-ptot)/sum(Y)
INF=1e18
def cost(a,b,i,inner):
    e=Y[i]*rate+inner; d=(b-a)-e; return d*d/max(e,1)
# prefix pause durations for inner pauses
def inner(q,j): return sum(P[k][1]-P[k][0] for k in range(q+1,j))
pre=[0]
for a,b in P: pre.append(pre[-1]+b-a)
def inn(q,j): return pre[j]-pre[q+1] if j>q+1 else 0
K=N-1
dp=[[INF]*n for _ in range(K)];bk=[[-1]*n for _ in range(K)]
for j in range(n): dp[0][j]=cost(s0,P[j][0],0,inn(-1,j))-3*(P[j][1]-P[j][0])
for k in range(1,K):
    for j in range(k,n):
        g=3*(P[j][1]-P[j][0])
        for q in range(max(0,j-12),j):
            if dp[k-1][q]>=INF: continue
            v=dp[k-1][q]+cost(P[q][1],P[j][0],k,inn(q,j))-g
            if v<dp[k][j]: dp[k][j]=v;bk[k][j]=q
best=min(range(n),key=lambda j:dp[K-1][j]+cost(P[j][1],endsp,K,inn(j,n)))
ch=[best]
for k in range(K-1,0,-1): ch.append(bk[k][ch[-1]])
ch=ch[::-1]
st=[s0]+[P[j][1] for j in ch]; en=[P[j][0] for j in ch]+[endsp]
out=[]
for i in range(N):
    out.append(dict(i=i,para=para[i],start=round(st[i],3),end=round(en[i],3),text=S[i],exp=round(Y[i]*rate,2)))
json.dump(out,open('sent.json','w'),ensure_ascii=False,indent=0)
bad=[o for o in out if abs((o['end']-o['start'])-o['exp'])>1.8]
for o in out: print(o['para']+1,o['start'],o['end'],round(o['end']-o['start'],2),o['exp'],o['text'][:50])
print('rate',rate,'N',N,'flag',len(bad))
