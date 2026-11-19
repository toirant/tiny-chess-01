import os,json,urllib.request as r
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0}
T={'P':"KKKKUUUUMMOQLLMPKKKOLJIKLMMGKKKK",'N':"ACEECGKKEKMNELNOEKNOELMNCGKLACEE",'B':"GIIIIKKKIKLMILLMIKMMIMMMILKKGIII",'R':"KKKKLMMMJKKKJKKKJKKKJKKKJKKKKKKL",'Q':"GIIJIKKKIKLLJKLLKKLLILLLIKLKGIIJ",'K':"K"*32}
P={k:[(ord(s[(i//10-2)*4+min(i%10-1,8-i%10)])-75)*5 if 2<=i//10<=9 and 1<=i%10<=8 else 0 for i in range(120)]for k,s in T.items()}
KN=(-21,-19,-12,-8,8,12,19,21)
KI=(-11,-10,-9,-1,1,9,10,11)
DB={'B':(-11,-9,9,11),'R':(-10,-1,1,10)}
LIM=10**5;INF=10**9;MATE=900000;N=[0];BM=[None]
class X(Exception):pass
def A(b,s):
 if b[s+9]=='P'or b[s+11]=='P':return 1
 for d in KN:
  if b[s+d]=='N':return 1
 for d in KI:
  if b[s+d]=='K':return 1
 for p,ds in DB.items():
  for d in ds:
   t=s+d
   while b[t]=='.':t+=d
   if b[t]in p+'Q':return 1
 return 0
def Y(i,j):
 if i<40:
  for q in'QRBN':yield(i,j,q)
 else:yield(i,j,'')
def G(b,c,e):
 for i,p in enumerate(b):
  if p=='P':
   j=i-10
   if b[j]=='.':
    yield from Y(i,j)
    if 80<i<89 and b[i-20]=='.':yield(i,i-20,'')
   for d in(-9,-11):
    j=i+d
    if b[j].islower()or j==e:yield from Y(i,j)
  elif p in'NK':
   for d in(KN if p=='N'else KI):
    t=b[i+d]
    if t=='.'or t.islower():yield(i,i+d,'')
   if p=='K'and 93<i<96:
    fb=b[::-1].swapcase();s=1 if i==95 else-1
    if c&1 and b[i+s]=='.'and b[i+2*s]=='.'and b[i+3*s]=='R'and not A(fb,119-i)and not A(fb,119-i-s):yield(i,i+2*s,'')
    if c&2 and b[i-s]=='.'and b[i-2*s]=='.'and b[i-3*s]=='.'and b[i-4*s]=='R'and not A(fb,119-i)and not A(fb,119-i+s):yield(i,i-2*s,'')
  elif p in'BRQ':
   for d in DB[p]if p!='Q'else DB['B']+DB['R']:
    j=i+d
    while b[j]=='.':yield(i,j,'');j+=d
    if b[j].islower():yield(i,j,'')
def D(b,c,e,m):
 i,j,q=m;p=b[i];s=list(b);s[i]='.'
 if p=='P'and j==e:s[j+10]='.'
 if p=='K'and abs(j-i)==2:
  s[98 if j>i else 91]='.';s[(i+j)//2]='R'
 s[j]=q or p;nb=''.join(s)
 if p=='K':c&=12
 elif p=='R':c&=~{98:1,91:2}.get(i,0)
 c&=~{28:4,21:8}.get(j,0)
 ne=i-10 if p=='P'and i-j==20 else -1
 return nb[::-1].swapcase(),((c&3)<<2)|((c&12)>>2),119-ne if ne>=0 else -1
def L(b,c,e):
 o=[]
 for m in G(b,c,e):
  nb,nc,ne=D(b,c,e,m)
  if not A(nb,nb.find('k')):o.append((m,nb,nc,ne))
 return o
def E(b):
 s=10
 for i,p in enumerate(b):
  if p.isalpha():
   q=p.upper();s+=V[q]+P[q][i] if p.isupper()else -V[q]-P[q][119-i]
 return s
def Q(b,c,e,a,be):
 N[0]+=1
 if N[0]>LIM:raise X
 st=E(b)
 if st>=be:return be
 if st>a:a=st
 for m in G(b,c,e):
  i,j,q=m;t=b[j]
  if t=='.'and j!=e and not q:continue
  nb,nc,ne=D(b,c,e,m)
  if A(nb,nb.find('k')):continue
  s=-Q(nb,nc,ne,-be,-a)
  if s>=be:return be
  if s>a:a=s
 return a
def S(b,c,e,d,a,be,pl):
 N[0]+=1
 if N[0]>LIM:raise X
 if d<=0:return Q(b,c,e,a,be)
 ms=L(b,c,e)
 if not ms:return -MATE+pl if A(b[::-1].swapcase(),119-b.find('K'))else 0
 ms.sort(key=lambda t:V.get(b[t[0][1]],0),reverse=True)
 best=-INF
 for m,nb,nc,ne in ms:
  s=-S(nb,nc,ne,d-1,-be,-a,pl+1)
  if s>best:
   best=s
   if pl==0:BM[0]=m
  if s>a:a=s
  if a>=be:break
 return best
def TH(b,c,e):
 N[0]=0;BM[0]=None
 ms=L(b,c,e)
 if not ms:return None
 b0=ms[0][0]
 for d in range(1,40):
  try:S(b,c,e,d,-INF,INF,0)
  except X:break
  if BM[0]:b0=BM[0]
 return b0
def SN(i):return chr(96+i%10)+str(10-i//10)
def FEN(f):
 p,s,ca,ep=f.split()[:4]
 b=list(' '*20+' ........ '*8+' '*20)
 i=21
 for ch in p:
  if ch=='/':i+=2
  elif ch.isdigit():i+=int(ch)
  else:b[i]=ch;i+=1
 b=''.join(b)
 cc=sum(1<<i for i,x in enumerate('KQkq')if x in ca)
 ee=-1
 if ep!='-':ee=4+ord(ep[0])-10*int(ep[1])
 if s=='b':
  b=b[::-1].swapcase();cc=((cc&3)<<2)|((cc&12)>>2);ee=119-ee if ee>=0 else -1
 return b,cc,ee,s=='b'
def UC(m,fl):
 i,j,q=m
 if fl:i,j=119-i,119-j
 return SN(i)+SN(j)+q.lower()
def PO(u,rt,o):
 return json.load(r.urlopen(u+rt,json.dumps(o).encode()))
def main():
 u=os.getenv('MAKEFUN_ENV_URL')
 while 1:
  g=PO(u,'/game',{})
  s=g.get('status')
  if s=='done':break
  if s=='your_move':
   b,c,e,fl=FEN(g['fen'])
   m=TH(b,c,e)
   PO(u,'/move',{'game':g['game'],'move':UC(m,fl)if m else g['legal_moves'][0]})
if __name__=='__main__':main()
