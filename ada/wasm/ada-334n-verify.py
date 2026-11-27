import hashlib, re, sys, zipfile, json
SUITES='cycle_tests adaptive_period_tests recovery_tests differential_tests recovery_comparison_tests head_commitment_tests canonical_vector_tests host_sha256_tests'.split()
NAMES={'compiler.txt','source.txt','equilibrium-blob.txt'}|{s+'.log' for s in SUITES}
def verify(path,source,blob):
    if not all(re.fullmatch('[0-9a-f]{40}',x) for x in (source,blob)): raise ValueError('invalid expected identity')
    with zipfile.ZipFile(path) as z:
        entries=z.infolist(); names=[x.filename for x in entries]
        if len(names)!=len(set(names)) or set(names)!=NAMES|{'SHA256SUMS'}: raise ValueError('archive inventory')
        if any(x.file_size>2_000_000 or x.is_dir() or (x.external_attr>>16)&0o170000==0o120000 for x in entries): raise ValueError('entry bounds')
        data={n:z.read(n) for n in names}
    inventory={}
    for line in data['SHA256SUMS'].decode('ascii').splitlines():
        m=re.fullmatch(r'([0-9a-f]{64})  ([a-zA-Z0-9_.-]+)',line)
        if not m or m[2] in inventory: raise ValueError('checksum format')
        inventory[m[2]]=m[1]
    if set(inventory)!=NAMES or any(hashlib.sha256(data[n]).hexdigest()!=h for n,h in inventory.items()): raise ValueError('checksum mismatch')
    if data['source.txt'].decode().strip()!=source or data['equilibrium-blob.txt'].decode().strip()!=blob: raise ValueError('source mismatch')
    compiler=data['compiler.txt'].decode();
    if not re.search(r'^release: 1\.85\.1$',compiler,re.M) or not re.search(r'^host: \S+$',compiler,re.M): raise ValueError('compiler identity')
    for s in SUITES:
        log=data[s+'.log'].decode(); summaries=re.findall(r'^test result:.*$',log,re.M)
        if len(summaries)!=1 or not re.fullmatch(r'test result: ok\. 1 passed; 0 failed; 0 ignored; 0 measured; \d+ filtered out; finished in [0-9.]+s',summaries[0]): raise ValueError('suite summary: '+s)
        if not re.search(r'^test (?:\w+::)*'+s+r'::\w+ \.\.\. ok$',log,re.M): raise ValueError('suite identity: '+s)
    return {'status':'CONSISTENT','source':source,'equilibrium_blob':blob,'suites':len(SUITES),'scope':'archive consistency only; provenance not authenticated'}
if __name__=='__main__':
    try: print(json.dumps(verify(*sys.argv[1:])))
    except Exception as e: sys.exit(str(e))
