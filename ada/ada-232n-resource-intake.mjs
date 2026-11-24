// ADA-232N .dlw — integer resource accounting; synthetic external supply.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {derivePumps,verifyPumps} from "./ada-231n-three-pumps.mjs";
export function deriveIntake(chain){
 const source=derivePumps(chain);if(!verifyPumps(chain,source).pass)throw Error("Pump replay failed");
 let parent=null,previous=null;
 return Object.freeze(source.map((s,i)=>{
 const levels=Object.freeze(s.levels.map(l=>{
 const capacity=Math.floor(l.pumps[0].capacity*1e9);
 const opening=previous?.levels[l.depth].closing??0;
 const offered=Math.floor(capacity*chain[i].signal/1000);
 const accepted=l.pumps[0].enabled?Math.min(offered,capacity-opening):0;
 return Object.freeze({depth:l.depth,capacity,opening,offered,accepted,rejected:offered-accepted,closing:opening+accepted,enabled:l.pumps[0].enabled});
 }));
 const body={schema:"ADA-232N.intake.v1",generation:s.generation,sourceHash:s.sourceHash,pumpHash:s.hash,parent,levels,growthFactor:1.025,supply:"SYNTHETIC_SIGNAL",unit:"nano-resource"};
 parent=fnv64(canonical(body));previous=Object.freeze({...body,hash:parent});return previous;
 }));
}
export function verifyIntake(chain,ledger){
 try{const expected=deriveIntake(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every((s,i)=>s.growthFactor===1.025&&s.levels.every(l=>[l.capacity,l.opening,l.offered,l.accepted,l.rejected,l.closing].every(x=>Number.isSafeInteger(x)&&x>=0)&&l.opening===(expected[i-1]?.levels[l.depth].closing??0)&&l.closing===l.opening+l.accepted&&l.offered===l.accepted+l.rejected&&l.closing<=l.capacity&&(l.enabled||l.accepted===0))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
