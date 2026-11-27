// ADA-328N .dlw — cross-language vector reproduction.
import {readFileSync} from "node:fs";
import {createHash} from "node:crypto";
import assert from "node:assert/strict";
const cases=JSON.parse(readFileSync(new URL("./ada-328n-vectors.json",import.meta.url)));
for(const c of cases){
 const h=Buffer.alloc(4);h.writeUInt32BE(c.history.length);
 const b=Buffer.concat([Buffer.from("ADA-327N:sealed-history:v1\0"),h,...c.history.map((s,i)=>{const a=Buffer.alloc(4);a.writeUInt32BE(i+1);return Buffer.concat([a,Buffer.from(s)])})]);
 assert.equal(b.toString("hex"),c.preimage);
 assert.equal(createHash("sha256").update(b).digest("hex"),c.sha256);
 console.log(c.name,"PASS");
}
console.log("8/8 checks",process.version);
