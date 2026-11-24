// ADA-235N .dlw — reserve-targeted replenishment, separate integrated replay.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveExpenditure,verifyExpenditure} from "./ada-234n-resource-expenditure.mjs";
export function replenishStep(g,l,p){
 const inputOpening=p?.inputClosing??0,activeOpening=p?.activeClosing??0;
 const opening=inputOpening+activeOpening,target=Math.floor(l.capacity*3/4);
 const deficit=Math.max(0,target-opening);
 const accepted=l.enabled?Math.min(l.offered,deficit,l.capacity-opening):0;
 const available=inputOpening+accepted;
 const transferred=l.enabled?Math.min(Math.floor(available*g.stability/400),l.activeLimit-activeOpening):0;
 const ready=activeOpening+transferred,spent=l.enabled?Math.min(ready,l.requested):0;
 const inputClosing=available-transferred,activeClosing=ready-spent;
 return Object.freeze({depth:l.depth,capacity:l.capacity,activeLimit:l.activeLimit,target,deficit,inputOpening,activeOpening,offered:l.offered,accepted,rejected:l.offered-accepted,transferred,requested:l.requested,spent,inputClosing,activeClosing,totalClosing:inputClosing+activeClosing,cumulativeAccepted:(p?.cumulativeAccepted??0)+accepted,cumulativeSpent:(p?.cumulativeSpent??0)+spent,enabled:l.enabled});
}
export function deriveReplenishment(chain){
 const source=deriveExpenditure(chain);if(!verifyExpenditure(chain,source).pass)throw Error("Expenditure replay failed");
 let prior=null;
 return Object.freeze(source.map((s,i)=>{
 const levels=Object.freeze(s.levels.map(l=>replenishStep(chain[i],l,prior?.levels[l.depth])));
 const body={schema:"ADA-235N.replenishment.v1",generation:s.generation,sourceHash:s.sourceHash,expenditureHash:s.hash,parent:prior?.hash??null,levels,growthFactor:1.025,unit:"nano-resource",policy:"TARGET_75_PERCENT"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});return prior;
 }));
}
export function verifyReplenishment(chain,ledger){
 try{const expected=deriveReplenishment(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every((s,i)=>s.growthFactor===1.025&&s.levels.every(l=>Object.entries(l).filter(([k])=>k!=="enabled").every(([,v])=>Number.isSafeInteger(v)&&v>=0)&&l.inputOpening===(expected[i-1]?.levels[l.depth].inputClosing??0)&&l.activeOpening===(expected[i-1]?.levels[l.depth].activeClosing??0)&&l.accepted<=l.deficit&&l.offered===l.accepted+l.rejected&&l.inputClosing===l.inputOpening+l.accepted-l.transferred&&l.activeClosing===l.activeOpening+l.transferred-l.spent&&l.totalClosing===l.inputClosing+l.activeClosing&&l.totalClosing<=l.target&&l.activeClosing<=l.activeLimit&&l.spent<=l.requested&&l.cumulativeAccepted===l.totalClosing+l.cumulativeSpent&&(l.enabled||l.accepted+l.transferred+l.spent===0))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
