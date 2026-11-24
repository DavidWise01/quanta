// ADA-236N .dlw — independently bounded metabolic rates.
import {canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {deriveReplenishment,verifyReplenishment} from "./ada-235n-homeostatic-replenishment.mjs";
export function attenuateStep(g,l,p){
 const inputOpening=p?.inputClosing??0,activeOpening=p?.activeClosing??0,opening=inputOpening+activeOpening;
 const deficit=Math.max(0,l.target-opening);
 const gainR=l.enabled?bound(deficit/Math.max(1,l.target),0,1):0;
 const gainG=l.enabled?bound(g.stability/100,0,1):0;
 const accepted=Math.floor(Math.min(l.offered,deficit,l.capacity-opening)*gainR);
 const available=inputOpening+accepted;
 const transferred=Math.floor(Math.min(Math.floor(available/4),l.activeLimit-activeOpening)*gainG);
 const ready=activeOpening+transferred;
 const gainB=l.enabled?bound(ready/Math.max(1,Math.floor(l.activeLimit/4)),0,1):0;
 const spent=Math.floor(Math.min(ready,l.requested)*gainB);
 const inputClosing=available-transferred,activeClosing=ready-spent;
 return Object.freeze({depth:l.depth,capacity:l.capacity,activeLimit:l.activeLimit,target:l.target,deficit,inputOpening,activeOpening,offered:l.offered,accepted,rejected:l.offered-accepted,transferred,requested:l.requested,spent,inputClosing,activeClosing,totalClosing:inputClosing+activeClosing,cumulativeAccepted:(p?.cumulativeAccepted??0)+accepted,cumulativeSpent:(p?.cumulativeSpent??0)+spent,enabled:l.enabled,gains:Object.freeze([gainR,gainG,gainB])});
}
export function deriveAttenuation(chain){
 const source=deriveReplenishment(chain);if(!verifyReplenishment(chain,source).pass)throw Error("Replenishment replay failed");
 let prior=null;
 return Object.freeze(source.map((s,i)=>{
 const levels=Object.freeze(s.levels.map(l=>attenuateStep(chain[i],l,prior?.levels[l.depth])));
 const body={schema:"ADA-236N.attenuation.v1",generation:s.generation,sourceHash:s.sourceHash,replenishmentHash:s.hash,parent:prior?.hash??null,levels,growthFactor:1.025,unit:"nano-resource"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});return prior;
 }));
}
export function verifyAttenuation(chain,ledger){
 try{const a=deriveAttenuation(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((s,i)=>s.growthFactor===1.025&&s.levels.every(l=>Object.entries(l).filter(([k])=>k!=="enabled"&&k!=="gains").every(([,v])=>Number.isSafeInteger(v)&&v>=0)&&l.gains.every(x=>x>=0&&x<=1)&&l.inputOpening===(a[i-1]?.levels[l.depth].inputClosing??0)&&l.activeOpening===(a[i-1]?.levels[l.depth].activeClosing??0)&&l.offered===l.accepted+l.rejected&&l.accepted<=l.deficit&&l.inputClosing===l.inputOpening+l.accepted-l.transferred&&l.activeClosing===l.activeOpening+l.transferred-l.spent&&l.totalClosing===l.inputClosing+l.activeClosing&&l.totalClosing<=l.target&&l.activeClosing<=l.activeLimit&&l.spent<=l.requested&&l.cumulativeAccepted===l.totalClosing+l.cumulativeSpent&&(l.enabled||l.accepted+l.transferred+l.spent===0))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
