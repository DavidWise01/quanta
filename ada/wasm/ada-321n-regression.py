# ADA-321N .dlw — isolated synthetic fixture regression, no publication.
import copy,hashlib,json,pathlib,subprocess,sys,tempfile
validator=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).with_name('verify-publication-v5.py')
source='a'*40; binary=b'\x00asm\x01\x00\x00\x00'; digest=hashlib.sha256(binary).hexdigest()
parity=dict(status='PASS',checks=57933,tolerance=1e-12,maxError=0.0,host='Node WebAssembly')
binding={k:ch*64 for k,ch in zip(('ledger','contention','abort'),'bcd')}
def bind(k):return dict(source=source,binary=digest,ledger=binding['ledger'],harness=binding[k])
u=dict(status='PASS',source=source,sha256=digest,checks=['native unified geometry','committed epoch and inherited context','reload and full audit','missing rejected','binding rejected','binary rejected'])
files={'manifest.json':dict(schema='ADA-281N.package.v1',authority='OBSERVE_ONLY',source_commit=source,double_build_equal=True,sha256=digest,bytes=len(binary),parity=parity,transaction_sources=binding),'parity.json':parity,'reference-schema.json':dict(status='PASS',checks=20,valid=6,rejected=14),'chromium.json':dict(status='PASS',source=source,sha256=digest,checks=['compiled initialization and geometry','24 sequential appends and inheritance','persistent reload and identical ancestry','missing asset rejected','corrupt asset rejected']),'ledger-contention.json':dict(status='PASS',scope='synthetic kernel; real IndexedDB; two connections',binding=bind('contention'),result=dict(commits=1,rejections=1,staleRejected=True,recovered=1,generations=[0,1],linked=True)),'ledger-abort.json':dict(status='PASS',scope='synthetic kernel; real IndexedDB; explicit transaction abort',binding=bind('abort'),result=dict(inserted=True,aborted=True,rejected=True,invalidated=True,before=[0],genesisPreserved=True,after=[0,1],linked=True,retryPreserved=True)),'unified-acceptance.json':u,'ada_browser.wasm':binary}
key='unified-acceptance.json'
def field(k,v):return lambda f:f[key].__setitem__(k,v)
cases=[('valid',lambda f:None,True),('missing',lambda f:f.pop(key),False),('invalid JSON',lambda f:f.__setitem__(key,b'{'),False),('null',lambda f:f.__setitem__(key,None),False),('array',lambda f:f.__setitem__(key,[]),False),('failed status',field('status','FAIL'),False),('wrong source',field('source','e'*40),False),('wrong binary',field('sha256','e'*64),False),('missing group',field('checks',u['checks'][:-1]),False),('reordered groups',field('checks',u['checks'][::-1]),False),('extra group',field('checks',u['checks']+['extra']),False),('duplicate group',field('checks',u['checks'][:-1]+[u['checks'][0]]),False),('wrong type',field('checks',True),False),('extra field',field('extra',True),False),('missing field',lambda f:f[key].pop('source'),False),('duplicate JSON key',lambda f:f.__setitem__(key,('{"status":"FAIL",'+json.dumps(u)[1:]).encode()),False),('boolean parity error',lambda f:f['parity.json'].__setitem__('maxError',False),False)]
results=[]
for name,mutate,expected in cases:
 f=copy.deepcopy(files);mutate(f)
 with tempfile.TemporaryDirectory() as d:
  for k,v in f.items(): (pathlib.Path(d)/k).write_bytes(v if isinstance(v,bytes) else json.dumps(v).encode())
  r=subprocess.run([sys.executable,str(validator),d,source],capture_output=True,text=True)
  actual=r.returncode==0;results.append(dict(case=name,expected=expected,accepted=actual,match=actual==expected,returncode=r.returncode))
print(json.dumps(dict(scope='synthetic fixtures; no native or browser execution',validator_blob=hashlib.sha1(b'blob '+str(validator.stat().st_size).encode()+b'\0'+validator.read_bytes()).hexdigest(),cases=results,matched=sum(x['match'] for x in results)),indent=2))
