import importlib.util, pathlib, tempfile, zipfile, hashlib,json
p=pathlib.Path(__file__).with_name('ada-332n-verify.py'); spec=importlib.util.spec_from_file_location('v',p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
s='a'*40;b='b'*40
base={'source.txt':s.encode(),'equilibrium-blob.txt':b.encode(),'compiler.txt':b'release: 1.85.1\nhost: x86_64-unknown-linux-gnu\n'}
for suite in v.SUITES:base[suite+'.log']=f'test equilibrium::{suite}::example ... ok\ntest result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 9 filtered out; finished in 0.01s\n'.encode()
results=[]
for case in ['valid','missing','extra','wrong_source','wrong_blob','wrong_compiler','failed_suite','wrong_suite','checksum_tamper','duplicate_inventory','traversal','oversized','duplicate_entry','forged_consistent']:
 d=base.copy()
 if case=='missing':d.pop('compiler.txt')
 if case=='extra':d['extra.txt']=b'x'
 if case=='wrong_source':d['source.txt']=b'c'*40
 if case=='wrong_blob':d['equilibrium-blob.txt']=b'c'*40
 if case=='wrong_compiler':d['compiler.txt']=b'release: 1.0.0\nhost: x\n'
 if case=='failed_suite':d['cycle_tests.log']=d['cycle_tests.log'].replace(b'0 failed',b'1 failed')
 if case=='wrong_suite':d['cycle_tests.log']=d['adaptive_period_tests.log']
 if case=='traversal':d['../source.txt']=b'x'
 if case=='oversized':d['compiler.txt']=b'x'*2000001
 d['SHA256SUMS']=''.join(f'{hashlib.sha256(x).hexdigest()}  {n}\n' for n,x in sorted(d.items())).encode()
 if case=='checksum_tamper':d['source.txt']+=b'x'
 if case=='duplicate_inventory':d['SHA256SUMS']+=d['SHA256SUMS'].splitlines()[0]+b'\n'
 with tempfile.TemporaryDirectory() as tmp:
  zpath=pathlib.Path(tmp)/'fixture.zip'
  with zipfile.ZipFile(zpath,'w') as z:
   for n,x in d.items():z.writestr(n,x)
   if case=='duplicate_entry':z.writestr('source.txt',d['source.txt'])
  try:v.verify(zpath,s,b);actual=True
  except Exception:actual=False
 expected=case in ('valid','forged_consistent');results.append(dict(case=case,expected=expected,accepted=actual,match=actual==expected))
print(json.dumps({'scope':'synthetic archives only','cases':results,'matched':sum(x['match'] for x in results)},indent=2))
assert all(x['match'] for x in results)
