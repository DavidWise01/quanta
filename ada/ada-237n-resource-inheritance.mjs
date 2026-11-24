// ADA-237N .dlw — epoch resource receipts; no duplication or new supply.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveAttenuation,verifyAttenuation} from "./ada-236n-metabolic-attenuation.mjs";
export function deriveResourceInheritance(chain){
 const a=deriveAttenuation(chain);if(!verifyAttenuation(chain,a).pass)throw Error("Attenuation replay failed");
 let prior=null;
 return Object.freeze(epochHierarchy(chain).map(e=>{
 const first=a[e.sourceStart],last=a[e.sourceEnd],rows=a.slice(e.sourceStart,e.sourceEnd+1);
 const levels=Object.freeze(first.levels.map((l,d)=>{
 const z=last.levels[d],opening=l.inputOpening+l.activeOpening;
 const accepted=rows.reduce((n,r)=>n+r.levels[d].accepted,0),spent=rows.reduce((n,r)=>n+r.levels[d].spent,0);
 return Object.freeze({depth:d,capacity:l.capacity,opening,inputOpening:l.inputOpening,activeOpening:l.activeOpening,accepted,spent,closing:z.totalClosing,inputClosing:z.inputClosing,activeClosing:z.activeClosing,cumulativeAccepted:z.cumulativeAccepted,cumulativeSpent:z.cumulativeSpent});
 }));
 const body={schema:"ADA-237N.resource-inheritance.v1",epoch:e.epoch,state:e.state,epochHash:e.hash,parent:prior?.hash??null,firstMetabolicHash:first.hash,lastMetabolicHash:last.hash,levels,growthFactor:1.025,transfer:e.state==="SEALED"?"ELIGIBLE":"PROVISIONAL"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});return prior;
 }));
}
export function verifyResourceInheritance(chain,ledger){
 try{const a=deriveResourceInheritance(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((e,i)=>e.growthFactor===1.025&&e.parent===(a[i-1]?.hash??null)&&(!i||a[i-1].state==="SEALED")&&e.levels.every((l,d)=>Object.values(l).every(x=>Number.isSafeInteger(x)&&x>=0)&&l.opening===l.inputOpening+l.activeOpening&&l.inputOpening===(a[i-1]?.levels[d].inputClosing??0)&&l.activeOpening===(a[i-1]?.levels[d].activeClosing??0)&&l.closing===l.inputClosing+l.activeClosing&&l.opening+l.accepted-l.spent===l.closing&&l.closing<=l.capacity&&l.cumulativeAccepted===l.cumulativeSpent+l.closing)),epochs:a.length,sealed:a.filter(e=>e.state==="SEALED").length};}catch(e){return {pass:false,reason:e.message}}
}
