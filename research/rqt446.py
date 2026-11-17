import math,json,sys
from pathlib import Path
import rqt445 as old

def compressed(E,L,f):
 if E<0:return set()
 m=abs(f); j=math.isqrt(E//(m*m))
 return {s for r in {L%m,(-L)%m} for t in [j*m+r] if t*t==E for s in {t,-t} if (s-L)%m==0}

def controls():
 n=0
 for f in range(1,41):
  for L in range(f):
   for E in range(401):
    t=math.isqrt(E); expected={s for s in {t,-t} if s*s==E and (s-L)%f==0}
    assert compressed(E,L,f)==expected;n+=1
 return n

if __name__=='__main__':
 src=Path(old.__file__).read_text(); start=src.index('def run(path):'); end=src.index("if __name__",start)
 code=src[start:end].replace('range(737,769)','range(769,801)').replace('y=[737,768]','y=[769,800]').replace('RQT=445','RQT=446')
 code=code.replace("cnt['coupled']+=1;t=math.isqrt(E)","cnt['coupled']+=1; ss_set=compressed(E,L,f); qbits.append((E.bit_length(),(E//(f*f)).bit_length())); t=math.isqrt(E)")
 code=code.replace('signs=signmask(t,L,abs(f))','signs=signmask(t,L,abs(f)); assert ss_set=={sign*t for sign in signs}')
 code=code.replace('if t*t!=E:continue','if t*t!=E:\n     assert not ss_set;continue')
 code=code.replace('hits=[]','hits=[];qbits=[]').replace("root19='OPEN',prefix18", "compression_bits={'max_E':max(a for a,b in qbits),'max_quotient':max(b for a,b in qbits)},root19='OPEN',prefix18")
 env=dict(vars(old));env.update(compressed=compressed,controls=controls);exec(code,env);out=env['run'](sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print(out)
