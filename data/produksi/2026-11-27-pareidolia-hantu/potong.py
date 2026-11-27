import re,json
exec(open('vo.py').read())
G=[[1.2,0.34],[3.68,0.46],[5.52,0.66],[7.22,0.44],[8.48,0.5],[11.36,0.34],[13.18,0.36],[15.1,0.52],[17.8,0.32],[18.94,0.88],[22.88,0.32],[24.94,0.4],[27.6,1.08],[31.18,0.42],[35.86,0.6],[38.02,0.38],[38.46,0.36],[39.62,0.44],[42.72,0.86],[47.3,0.5],[49.52,0.42],[51.06,0.5],[55.56,0.88],[58.82,0.4],[61.12,0.42],[64.26,0.88],[65.98,0.32],[69.08,0.5],[71.96,0.42],[72.9,0.28],[73.84,0.88],[75.96,0.44],[79.42,0.36],[81.82,0.78],[84.3,0.38],[87.82,0.56],[90.64,0.32],[92.42,0.82],[94.46,0.3],[98.04,0.56],[102.3,0.9],[105.8,0.42],[108.5,0.42],[110.8,0.96],[116.54,0.4],[119.4,0.42],[123.08,0.86],[125.94,0.28]]
D=127.11
paras=[v for *_,v in VO]
L=[len(re.sub(r'[^a-z]','',p.lower())) for p in paras]
sil=sum(g[1] for g in G); speak=D-sil; T=sum(L)
N=len(paras)
# speech time before a gap
cum=[];acc=0
for s,l in G: cum.append(s-acc); acc+=l
INF=1e18
dp={(0,-1):(0,None)}
best=[{-1:(0,None)}]
for k in range(1,N):
    cur={}
    for j,(s,l) in enumerate(G):
        for i,(c,_) in best[k-1].items():
            if i>=j: continue
            prev=cum[i] if i>=0 else 0
            exp=speak*L[k-1]/T
            cost=c+((cum[j]-prev-exp)/1.0)**2+ 12*max(0,.85-l)
            if j not in cur or cost<cur[j][0]: cur[j]=(cost,i)
    best.append(cur)
end=min(best[-1],key=lambda j:best[-1][j][0]+(speak-cum[j]-speak*L[-1]/T)**2)
idx=[end]
for k in range(N-1,1,-1): idx.append(best[k][idx[-1]][1])
idx=idx[::-1]
cuts=[0]+[round(G[j][0]+G[j][1]/2,2) for j in idx]+[D]
for n,(a,b) in enumerate(zip(cuts,cuts[1:])):
    j=idx[n] if n<len(idx) else None
    print(VO[n][0],a,b,round(b-a,2),G[j][1] if j is not None else '', round(L[n]/(b-a),1),paras[n][-30:])
json.dump(cuts,open('cuts.json','w'))
