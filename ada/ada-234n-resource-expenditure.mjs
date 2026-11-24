// ADA-234N .dlw — integrated R/G/B accounting, separate prospective replay.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveCirculation,verifyCirculation} from "./ada-233n-internal-circulation.mjs";
import {deriveIntake} from "./ada-232n-resource-intake.mjs";
export function deriveExpenditure(chain){
 const source=deriveCirculation(chain),intake=deriveIntake(chain);
 if(!verifyCirculation(chain,source).pass)throw Error("Circulation replay failed");
 let parent=null,prior=null;
 return Object.freeze(source.map((s,i)=>{
 const levels=Object.freeze(s.levels.map(l=>{
 const g=chain[i],p=prior?.levels[l.depth],inputOpening=p?.inputClosing??0,activeOpening=p?.activeClosing??0;
 const offered=intake[i].levels[l.depth].offered;
 const accepted=l.enabled?Math.min(offered,l.capacity-inputOpening-activeOpening):0;
 const available=inputOpening+accepted;
 const transferred=l.enabled?Math.min(Math.floor(available*g.stability/400),l.activeLimit-activeOpening):0;
 const ready=activeOpening+transferred;
 const requested=Math.floor(l.capacity*(100-g.energy)/2000)+Math.floor(l.capacity/100);
 const spent=l.enabled?Math.min(ready,requested):0;
 const inputClosing=available-transferred,activeClosing=ready-spent,totalClosing=inputClosing+activeClosing;
 return Object.freeze({depth:l.depth,capacity:l.capacity,activeLimit:l.activeLimit,inputOpening,activeOpening,offered,accepted,rejected:offered-accepted,transferred,requested,spent,inputClosing,activeClosing,totalClosing,cumulativeSpent:(p?.cumulativeSpent??0)+spent,cumulativeAccepted:(p?.cumulativeAccepted??0)+accepted,enabled:l.enabled});
 }));
 const body={schema:"ADA-234N.expenditure.v1",generation:s.generation,sourceHash:s.sourceHash,circulationHash:s.hash,parent,levels,growthFactor:1.025,unit:"nano-resource",model:"INTEGRATED_REPLAY_SYNTHETIC"};
 parent=fnv64(canonical(body));prior=Object.freeze({...body,hash:parent});return prior;
 }));
}
export function verifyExpenditure(chain,ledger){
 try{const expected=deriveExpenditure(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every((s,i)=>s.growthFactor===1.025&&s.levels.every(l=>Object.entries(l).filter(([k])=>!["enabled"].includes(k)).every(([,v])=>Number.isSafeInteger(v)&&v>=0)&&l.inputOpening===(expected[i-1]?.levels[l.depth].inputClosing??0)&&l.activeOpening===(expected[i-1]?.levels[l.depth].activeClosing??0)&&l.offered===l.accepted+l.rejected&&l.inputClosing===l.inputOpening+l.accepted-l.transferred&&l.activeClosing===l.activeOpening+l.transferred-l.spent&&l.totalClosing===l.inputClosing+l.activeClosing&&l.totalClosing<=l.capacity&&l.activeClosing<=l.activeLimit&&l.spent<=l.requested&&l.cumulativeAccepted===l.totalClosing+l.cumulativeSpent&&(l.enabled||l.accepted+l.transferred+l.spent===0))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
