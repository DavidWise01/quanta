// ADA-199N · Strict verification of the exact files served by public GitHub Pages.
// Run: node ada/ada-199n-pages-integrity.mjs
// Requires Node 22+; no external packages.
import fs from "node:fs";
import crypto from "node:crypto";

const base=(process.env.ADA_PUBLIC_BASE||"https://davidwise01.github.io/quanta").replace(/\\/$/,"");
const output=process.env.ADA_REPORT_DIR||"ada/verification-results/pages-integrity";
fs.mkdirSync(output,{recursive:true});
const expected=JSON.parse(fs.readFileSync(new URL("./ada-199n-source-integrity.json",import.meta.url),"utf8"));
const result={schema:"ADA-199N.pages-integrity.v1",base,checkedAt:new Date().toISOString(),manifestMatches:false,passed:0,failed:0,results:[]};
const gitBlobHash=bytes=>crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+" ","utf8")).update(Buffer.from([0])).update(bytes).digest("hex");
async function fetchBytes(url){
 const response=await fetch(url,{redirect:"follow",signal:AbortSignal.timeout(20000),headers:{"User-Agent":"ADA-199N-Verification/1.0","Cache-Control":"no-cache"}});
 if(!response.ok)throw Error("HTTP "+response.status+" "+url);
 return Buffer.from(await response.arrayBuffer());
}
try{
 const manifestUrl=base+"/ada/ada-199n-source-integrity.json";
 const remoteBytes=await fetchBytes(manifestUrl);
 const localBytes=fs.readFileSync(new URL("./ada-199n-source-integrity.json",import.meta.url));
 result.manifestMatches=Buffer.compare(remoteBytes,localBytes)===0;
 if(!result.manifestMatches)throw Error("Public manifest differs from repository checkout");
 const files=Object.entries(expected.files);
 if(files.length!==8)throw Error("Expected eight pinned lab files; found "+files.length);
 for(const [path,expectedHash] of files){
  const entry={path,expected:expectedHash,actual:null,pass:false};
  try{
   const bytes=await fetchBytes(base+"/"+path);
   entry.actual=gitBlobHash(bytes);
   entry.bytes=bytes.length;
   entry.pass=entry.actual===expectedHash;
   if(!entry.pass)entry.error="Published HTML does not match pinned Git blob SHA";
  }catch(e){entry.error=String(e.message)}
  result.results.push(entry);
  result[entry.pass?"passed":"failed"]++;
  console.log((entry.pass?"PASS ":"FAIL ")+path+(entry.error?": "+entry.error:""));
 }
}catch(e){result.error=String(e.message);result.failed++}
finally{
 result.success=result.manifestMatches&&result.passed===8&&result.failed===0;
 fs.writeFileSync(output+"/report.json",JSON.stringify(result,null,2)+"\\n");
 console.log(JSON.stringify(result,null,2));
 if(!result.success)process.exitCode=1;
}
