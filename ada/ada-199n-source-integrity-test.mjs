// ADA-199N · Deterministic source-integrity gate.
// Run: node ada/ada-199n-source-integrity-test.mjs
import fs from "node:fs";
import crypto from "node:crypto";
import assert from "node:assert/strict";
const manifest=JSON.parse(fs.readFileSync(new URL("./ada-199n-source-integrity.json",import.meta.url),"utf8"));
assert.equal(manifest.schema,"ADA-199N.source-integrity.v1");
assert.equal(manifest.algorithm,"git-blob-sha1");
// Git's canonical blob hash of "hello\\n" (verified against git hash-object).
const vector=Buffer.from("hello\n");
const vectorHeader=Buffer.concat([Buffer.from("blob "+vector.length),Buffer.from([0])]);
assert.equal(crypto.createHash("sha1").update(vectorHeader).update(vector).digest("hex"),"ce013625030ba8dba906f756967f9e9ca394464a","Git blob header calibration");
const entries=Object.entries(manifest.files);
assert.equal(entries.length,8,"Eight pinned labs required");
const results=[];
for(const [name,expected] of entries){
 assert.ok(/^ada\/ada-19[1-8]n-[a-z0-9-]+\.html$/.test(name),"Unexpected path "+name);
 assert.match(expected,/^[0-9a-f]{40}$/);
 const bytes=fs.readFileSync(new URL("../"+name,import.meta.url));
 const prefix=Buffer.concat([Buffer.from("blob "+bytes.length,"utf8"),Buffer.from([0])]);
 const actual=crypto.createHash("sha1").update(prefix).update(bytes).digest("hex");
 const pass=actual===expected;
 results.push({name,expected,actual,pass});
 console.log((pass?"PASS":"FAIL")+" "+name+" "+actual);
}
const passed=results.filter(r=>r.pass).length;
const result={schema:"ADA-199N.source-integrity.result.v1",passed,total:entries.length,results};
console.log(JSON.stringify(result,null,2));
if(passed!==entries.length)process.exitCode=1;
