// ADA-209N · exact byte-integrity for local checkout and public GitHub Pages.
// Uses Git's documented blob SHA-1 framing: "blob <byte-length>\0" + bytes.
import fs from "node:fs/promises";
import crypto from "node:crypto";
import assert from "node:assert/strict";
const manifest=JSON.parse(await fs.readFile(new URL("./ada-209n-pinned-pages.json",import.meta.url),"utf8"));
assert.equal(manifest.schema,"ADA-209N.pinned-pages.v1");
assert.equal(manifest.algorithm,"git-blob-sha1");
assert.equal(manifest.repository,"DavidWise01/quanta");
assert.equal(manifest.branch,"main");
const files=Object.entries(manifest.files);
assert.equal(files.length,9);
const blobSha=bytes=>crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
const publicMode=process.argv.includes("--public");
const root=new URL("../",import.meta.url);
const results=[];
for(const [file,expected] of files){
 assert.match(file,/^ada\/ada-(?:20[1-8]n-.*\.(?:html|mjs))$/);
 assert.match(expected,/^[a-f0-9]{40}$/);
 const local=await fs.readFile(new URL(file,root));
 const localHash=blobSha(local);
 assert.equal(localHash,expected,"Pinned local source drift: "+file);
 let publicHash=null;
 if(publicMode){
  const url=new URL(file,manifest.base.replace(/\/$/,"")+"/");
  const response=await fetch(url,{headers:{"cache-control":"no-cache"}});
  assert.equal(response.status,200,"Public Pages response "+file+" / "+response.status);
  const publicBytes=Buffer.from(await response.arrayBuffer());
  publicHash=blobSha(publicBytes);
  assert.equal(publicHash,expected,"Published Pages bytes differ from pinned source: "+file);
 }
 results.push({file,localHash,publicHash});
}
console.log(JSON.stringify({schema:"ADA-209N.pages-integrity.v1",passed:true,mode:publicMode?"local-and-public":"local-only",count:results.length,results},null,2));
