// ADA-293N .dlw — native/WASM comparison, Node host.
import fs from "node:fs";
import {parseReference} from "./reference-schema.mjs";
const [binary,reference]=process.argv.slice(2);
const {instance:{exports:e}}=await WebAssembly.instantiate(fs.readFileSync(binary));
const lines=fs.readFileSync(reference,"utf8").replace(/\r?\n$/, "").split(/\r?\n/);
let checks=0,maxError=0;
for(const line of lines){
 const {name,args,want,kind}=parseReference(line);
 if(typeof e[name]!=="function")throw Error("missing export "+name);
 const actual=e[name](...args);
 const got=kind==="u"?actual>>>0:actual;
 const error=Math.abs(got-want);
 const pass=kind==="f"?(Number.isNaN(want)?Number.isNaN(got):Number.isFinite(got)&&error<=1e-12):got===want;
 if(!pass)throw Error(JSON.stringify({name,args,want,got}));
 if(kind==="f"&&Number.isFinite(error))maxError=Math.max(maxError,error);
 checks++;
}
if(checks!==57933)throw Error("unexpected reference count "+checks);
console.log(JSON.stringify({checks,maxError,tolerance:1e-12,status:"PASS",host:"Node WebAssembly"},null,2));
