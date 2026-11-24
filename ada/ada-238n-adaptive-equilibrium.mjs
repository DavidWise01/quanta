// ADA-238N .dlw — adaptive target and rates from preceding sealed epoch.
import {canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveAttenuation,verifyAttenuation} from "./ada-236n-metabolic-attenuation.mjs";
export function equilibriumStep(g,l,p,policy){
 const inputOpening=p?.inputClosing??0,activeOpening=p?.activeClosing??0,opening=inputOpening+activeOpening;
 const target=Math.floor(l.capacity*policy.target/100),deficit=Math.max(0,target-opening);
 const gainR=l.enabled?bound(deficit/Math.max(1,target),0,1):0;
 const gainG=l.enabled?bound(g.stability/100,0,1)*policy.circulation/100:0;
 const accepted=Math.floor(Math.min(l.offered,deficit,l.capacity-opening)*gainR);
 const available=inputOpening+accepted;
 const transferred=Math.floor(Math.min(Math.floor(available/4),l.activeLimit-activeOpening)*gainG);
 const ready=activeOpening+transferred;
 const gainB=l.enabled?bound(ready/Math.max(1,Math.floor(l.activeLimit/4)),0,1)*policy.expenditure/100:0;
 const spent=Math.floor(Math.min(ready,l.requested)*gainB);
 const inputClosing=available-transferred,activeClosing=ready-spent;
 return Object.freeze({depth:l.depth,capacity:l.capacity,target,inputOpening,activeOpening,offered:l.offered,accepted,rejected:l.offered-accepted,transferred,requested:l.requested,spent,inputClosing,activeClosing,totalClosing:inputClosing+activeClosing,cumulativeAccepted:(p?.cumulativeAccepted??0)+accepted,cumulativeSpent:(p?.cumulativeSpent??0)+spent,enabled:l.enabled,gains:Object.freeze([gainR,gainG,gainB]),policy});
}
export function deriveEquilibrium(chain){
 const source=deriveAttenuation(chain);if(!verifyAttenuation(chain,source).pass)throw Error("Attenuation replay failed");
 let prior=null,priorEpoch=null;const out=[];
 for(const e of epochHierarchy(chain)){
 const policies=Object.freeze([0,1,2].map(d=>{
 const p=priorEpoch?.levels[d],old=priorEpoch?.policies[d]??{target:75,circulation:100,expenditure:100};
 const scarce=p&&p.totalClosing<p.target*.8, surplus=p&&p.totalClosing>p.target*.95;
 const step=priorEpoch?.state==="SEALED"&&priorEpoch.holds===0?(scarce?1:surplus?-1:0):0;
 return Object.freeze({target:bound(old.target+step*5,50,85),circulation:bound(old.circulation+step*5,50,100),expenditure:bound(old.expenditure-step*5,50,100)});
 }));
 for(let i=e.sourceStart;i<=e.sourceEnd;i++){
 const s=source[i],levels=Object.freeze(s.levels.map(l=>equilibriumStep(chain[i],l,prior?.levels[l.depth],policies[l.depth])));
 const body={schema:"ADA-238N.equilibrium.v1",generation:s.generation,epoch:e.epoch,sourceHash:s.sourceHash,attenuationHash:s.hash,policyParent:priorEpoch?.hash??null,parent:prior?.hash??null,levels,growthFactor:1.025};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});out.push(prior);
 }
 priorEpoch={state:e.state,holds:e.holds,hash:prior.hash,levels:prior.levels,policies};
 }
 return Object.freeze(out);
}
export function verifyEquilibrium(chain,ledger){
 try{const a=deriveEquilibrium(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((s,i)=>s.growthFactor===1.025&&s.levels.every(l=>l.policy.target>=50&&l.policy.target<=85&&l.policy.circulation>=50&&l.policy.circulation<=100&&l.policy.expenditure>=50&&l.policy.expenditure<=100&&l.gains.every(g=>g>=0&&g<=1)&&[l.accepted,l.transferred,l.spent,l.inputClosing,l.activeClosing,l.cumulativeAccepted,l.cumulativeSpent].every(v=>Number.isSafeInteger(v)&&v>=0)&&l.inputOpening===(a[i-1]?.levels[l.depth].inputClosing??0)&&l.activeOpening===(a[i-1]?.levels[l.depth].activeClosing??0)&&l.offered===l.accepted+l.rejected&&l.inputClosing===l.inputOpening+l.accepted-l.transferred&&l.activeClosing===l.activeOpening+l.transferred-l.spent&&l.totalClosing===l.inputClosing+l.activeClosing&&l.totalClosing<=l.capacity&&l.cumulativeAccepted===l.totalClosing+l.cumulativeSpent&&(l.enabled||l.accepted+l.transferred+l.spent===0))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
