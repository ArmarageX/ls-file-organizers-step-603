import json, re, requests
from pathlib import Path
from bs4 import BeautifulSoup
BASE='https://ls-file-organizers-step-603.onrender.com'
TARGET='https://lestallion.com/blogs/product-reviews/best-vertical-desktop-file-organizers-with-step-design'
PREV='https://ls-rotating-organizers-602.surge.sh/index.html'
PAGES=['index.html','fit-sizing-clearance.html','workflow-layout-handoff.html','specs-compatibility.html','maintenance-durability-care.html','checklist-red-flags.html','scenario-small-office.html','about.html','contact.html','privacy.html']
SUP=PAGES[1:7]; TRUST=PAGES[7:]
def text(soup):
    soup=BeautifulSoup(str(soup),'html.parser')
    for t in soup(['script','style','nav','header','footer','aside']): t.decompose()
    return soup.get_text(' ')
def wc(txt): return len(re.findall(r"\b[\w'-]+\b", txt))
def sim(a,b,n):
    def toks(x): return re.findall(r'[a-z]{3,}',x.lower())
    A=toks(a);B=toks(b);sa=set(tuple(A[i:i+n]) for i in range(max(0,len(A)-n+1)));sb=set(tuple(B[i:i+n]) for i in range(max(0,len(B)-n+1)))
    return len(sa&sb)/max(1,min(len(sa),len(sb)))
qa={'pages':{},'support_similarity':{},'trust_similarity':{},'assets':{}}
texts={}
for f in PAGES:
    url=BASE+'/'+f
    r=requests.get(url,timeout=30)
    soup=BeautifulSoup(r.text,'html.parser')
    links=[a.get('href','') for a in soup.find_all('a')]
    imgs=[img.get('src') for img in soup.find_all('img')]
    txt=text(soup); texts[f]=txt
    qa['pages'][f]={'status':r.status_code,'words':wc(txt),'target_links':links.count(TARGET),'prev_links':links.count(PREV),'schema':bool(soup.find('script',type='application/ld+json')),'images':len(imgs),'footer_trust':all(x in links for x in ['about.html','contact.html','privacy.html']),'brand_home':bool(soup.select_one('a.brand[href="index.html"]'))}
    for src in imgs:
        au=BASE+'/'+src if not src.startswith('http') else src
        if au not in qa['assets']:
            ar=requests.get(au,timeout=30)
            qa['assets'][au]={'status':ar.status_code,'content_type':ar.headers.get('content-type'),'bytes':len(ar.content)}
for i,a in enumerate(SUP):
    for b in SUP[i+1:]: qa['support_similarity'][a+'|'+b]=round(sim(texts[a],texts[b],8),3)
for i,a in enumerate(TRUST):
    for b in TRUST[i+1:]: qa['trust_similarity'][a+'|'+b]=round(sim(texts[a],texts[b],6),3)
Path('live_qa.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa,indent=2))
