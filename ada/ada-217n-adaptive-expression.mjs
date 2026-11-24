// ADA-217N .dlw — prospective expression, never a source transition.
import {verifyChain,canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveEpochMutation} from "./ada-216n-epoch-mutation.mjs";
export function deriveAdaptiveExpression(chain){
 const audit=verifyChain(chain);if(!audit.pass)throw Error(audit.reason);
 const epochs=epochHierarchy(chain),mutations=deriveEpochMutation(chain);
 const byEpoch=new Map(mutations.map(m=>[m.effectiveEpoch,m]));
 let parent=null;
 return Object.freeze(epochs.flatMap(e=>{
  const m=byEpoch.get(e.epoch),offset=m?.offset??0;
  return chain.slice(e.sourceStart,e.sourceEnd+1).map(g=>{
   const permitted=g.decision==="APPEND"&&g.stability>=90&&g.energy>=5&&m?.decision!=="HOLD";
   const expressed=permitted?offset:0;
   const body={schema:"ADA-217N.expression.v1",generation:g.n,epoch:e.epoch,sourceHash:g.hash,mutationHash:m?.hash??null,parent,raw:g.signal,offset:expressed,perception:Number(bound(g.signal*(1+expressed),0,100).toFixed(5)),decision:g.decision,expression:permitted?"PERMIT":"BYPASS",growthFactor:1.025};
   parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
  });
 }));
}
export function verifyAdaptiveExpression(chain,ledger){
 try{return {pass:canonical(deriveAdaptiveExpression(chain))===canonical(ledger)}}catch(e){return {pass:false,reason:e.message}}
}
