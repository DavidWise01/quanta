// ADA-247N .dlw — sealed epoch perceptual inheritance receipts.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveMemory,verifyMemory,MEMORY_WINDOW} from "./ada-246n-temporal-memory.mjs";
export function derivePerceptualInheritance(chain){
 const m=deriveMemory(chain);if(!verifyMemory(chain,m).pass)throw Error("Memory replay failed");
 let prior=null;
 return Object.freeze(epochHierarchy(chain).map(e=>{
 const first=m[e.sourceStart],last=m[e.sourceEnd];
 const channels=Object.freeze(last.memory.map((z,d)=>{
 const opening=prior?.channels[d].closing??Object.freeze([]);
 const closing=z.history;
 return Object.freeze({address:z.address,opening,closing,firstObservation:first.memory[d].current,lastObservation:z.current,coverage:z.coverage,trend:z.trend});
 }));
 const body={schema:"ADA-247N.perceptual-inheritance.v1",epoch:e.epoch,state:e.state,epochHash:e.hash,parent:prior?.hash??null,firstMemoryHash:first.hash,lastMemoryHash:last.hash,channels,window:MEMORY_WINDOW,growthFactor:1.025,authority:"OBSERVE_ONLY",transfer:e.state==="SEALED"?"ELIGIBLE":"PROVISIONAL"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});return prior;
 }));
}
export function verifyPerceptualInheritance(chain,ledger){
 try{const a=derivePerceptualInheritance(chain),m=deriveMemory(chain),epochs=epochHierarchy(chain);
 return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&(!i||a[i-1].state==="SEALED")&&r.epochHash===epochs[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.channels.length===9&&r.channels.every((c,d)=>canonical(c.opening)===canonical(a[i-1]?.channels[d].closing??[])&&canonical(c.closing)===canonical(m[epochs[i].sourceEnd].memory[d].history)&&c.opening.length<=MEMORY_WINDOW&&c.closing.length<=MEMORY_WINDOW&&new Set(c.closing.map(h=>h.generation)).size===c.closing.length&&canonical([...c.opening,Object.freeze({generation:m[epochs[i].sourceStart].generation,delta:m[epochs[i].sourceStart].attention[d].delta,selected:m[epochs[i].sourceStart].attention[d].selected})].slice(-MEMORY_WINDOW))===canonical(m[epochs[i].sourceStart].memory[d].history))),epochs:a.length,sealed:a.filter(r=>r.state==="SEALED").length};}catch(e){return {pass:false,reason:e.message}}
}
