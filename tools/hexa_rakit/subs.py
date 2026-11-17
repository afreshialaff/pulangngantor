import json,re
TL=json.load(open('timeline.json'))
U={'nol':0,'satu':1,'dua':2,'tiga':3,'empat':4,'lima':5,'enam':6,'tujuh':7,'delapan':8,'sembilan':9,'sepuluh':10,'sebelas':11,'seratus':100,'seribu':1000}
def parse(tokens):
    # returns value of a spelled-number token list
    total=0;cur=0;i=0
    while i<len(tokens):
        w=tokens[i]
        if w in ('belas',): cur=(cur%10)+10+ (cur-cur%10); 
        elif w=='puluh': cur=cur*10
        elif w=='ratus': cur=cur*100
        elif w=='ribu': total+= (cur or 1)*1000; cur=0
        elif w=='seratus': cur+=100
        elif w=='seribu': total+=1000
        elif w=='sepuluh': cur+=10
        elif w=='sebelas': cur+=11
        else:
            n=U[w]
            if cur%10==0 and cur>=10 and n<10: cur+=n
            else: cur=cur+n
        i+=1
    return total+cur
NW=set(U)|{'belas','puluh','ratus','ribu'}
def num_tokens_value(toks):
    # handle 'X belas' properly: digit then belas
    vals=[];res=0;cur=0
    out=0;seg=0
    i=0
    while i<len(toks):
        w=toks[i]
        if w in U and w not in('seratus','seribu','sepuluh','sebelas'):
            n=U[w]
            if i+1<len(toks) and toks[i+1]=='belas': seg+=10+n; i+=2; continue
            if i+1<len(toks) and toks[i+1]=='puluh': seg+=n*10; i+=2; continue
            if i+1<len(toks) and toks[i+1]=='ratus': seg+=n*100; i+=2; continue
            if i+1<len(toks) and toks[i+1]=='ribu': out+=(seg+n)*1000; seg=0; i+=2; continue
            seg+=n; i+=1; continue
        if w=='seratus': seg+=100
        elif w=='seribu': out+=1000
        elif w=='sepuluh': seg+=10
        elif w=='sebelas': seg+=11
        elif w=='ribu': out+=seg*1000; seg=0
        elif w=='puluh': seg*=10
        elif w=='ratus': seg*=100
        i+=1
    return out+seg
SKIP_ALONE={'satu','dua','tiga','empat','lima','enam'}  # small counts stay words unless part of bigger number
def digits(text):
    text=text.replace('abad kelima belas','abad ke-15').replace('abad ketiga belas','abad ke-13').replace('abad kedua puluh','abad ke-20')
    words=text.split(' ')
    out=[];i=0
    while i<len(words):
        m=re.match(r'^([A-Za-z]+)(.*)$',words[i]); 
        if m and m.group(1).lower() in NW:
            j=i;toks=[];tail=''
            while j<len(words):
                mm=re.match(r'^([A-Za-z]+)(.*)$',words[j])
                if not mm or mm.group(1).lower() not in NW: break
                toks.append(mm.group(1).lower()); tail=mm.group(2); j+=1
                if tail: break
            v=num_tokens_value(toks)
            prev=out[-1].lower() if out else ''
            if len(toks)==1 and toks[0] in ('satu','dua','tiga','empat','lima','enam','tujuh','delapan','sembilan') and prev not in('tahun','ms'):
                out.append(words[i]); i+=1; continue
            s=str(v)
            if v>=1000 and not (1000<=v<=2099 and prev in ('tahun','dan')): s=f'{v:,}'.replace(',','.')
            out.append(s+tail); i=j; continue
        out.append(words[i]); i+=1
    return ' '.join(out).replace('Rudolf II','Rudolf\u00a0II')
def syl(s): return max(1,len(re.findall(r'[aiueoéáčý]+',s.lower())))
def bal2(t,maxc=42):
    if len(t)<=maxc: return t
    w=t.split(' ');best=None
    for k in range(1,len(w)):
        a=' '.join(w[:k]);b=' '.join(w[k:])
        sc=abs(len(a)-len(b))+(0 if a.endswith(',') else 6)
        if len(a)<=maxc and len(b)<=maxc and (best is None or sc<best[0]): best=(sc,a+'\\N'+b)
    if best: return best[1]
    best=min(((max(len(' '.join(w[:k])),len(' '.join(w[k:]))),k) for k in range(1,len(w))))
    k=best[1]; return ' '.join(w[:k])+'\\N'+' '.join(w[k:])
def chunks(sent,maxc=42):
    if len(sent)<=2*maxc-6: return [bal2(sent)]
    w=sent.split(' ');n=len(sent);parts=-(-n//(2*maxc-8))
    target=n/parts;res=[];cur=[]
    best=None
    # choose split points minimizing deviation, preferring commas/colons
    import itertools
    pos=[];L=0
    for i,x in enumerate(w): L+=len(x)+1; pos.append(L)
    def score(cuts):
        segs=[];p=0
        for c in list(cuts)+[len(w)]: segs.append(' '.join(w[p:c])); p=c
        if any(len(x)>2*maxc-4 for x in segs): return None
        pen=sum(abs(len(x)-target) for x in segs)+sum(0 if x.endswith((',',':',';')) else 12 for x in segs[:-1])
        return pen,segs
    for cuts in itertools.combinations(range(1,len(w)),parts-1):
        r=score(cuts)
        if r and (best is None or r[0]<best[0]): best=r
    return [bal2(x) for x in best[1]]
cues=[]
for s in TL['scenes']:
    off=s['vo_at']-s['vo_start']
    for x in s['sents']:
        t=digits(x['text'])
        cs=chunks(t)
        a=x['start']+off;b=x['end']+off
        w=[syl(c) for c in cs];tot=sum(w);acc=a
        for c,wi in zip(cs,w):
            d=(b-a)*wi/tot
            cues.append([round(acc,3),round(acc+d,3),c,s['id']]); acc+=d
# extend each cue slightly to bridge tiny gaps (<0.6s) for readability
for i in range(len(cues)-1):
    g=cues[i+1][0]-cues[i][1]
    if 0<g<0.6: cues[i][1]=round(cues[i+1][0]-0.02,3)
    else: cues[i][1]=round(min(cues[i][1]+0.25,cues[i+1][0]-0.02),3)
json.dump(cues,open('cues.json','w'),ensure_ascii=False,indent=0)
for c in cues: print(c[3],c[0],c[1],c[2].replace('\\N',' / '))
