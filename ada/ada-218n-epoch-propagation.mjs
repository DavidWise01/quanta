// ADA-218N .dlw — bounded, forward-only adaptive feedback.
import {verifyChain,canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveEpochMutation} from "./ada-216n-epoch-mutation.mjs";
export function derivePropagation(chain){
 const audit=verifyChain(chain);if(!audit.pass)throw Error(audit.reason);
 const mutations=new Map(deriveEpochMutation(chain).map(m=>[m.effectiveEpoch,m]));
 const out=[];let carry=0,parent=null;
 const round=x=>Number(x.toFixed(6));
 for(const e of epochHierarchy(chain)){
  const m=mutations.get(e.epoch),incoming=carry;
  const offset=round(bound((m?.offset??0)+incoming,-0.25,0.25));
  const rows=chain.slice(e.sourceStart,e.sourceEnd+1).map(g=>{
   const permit=g.decision==="APPEND"&&g.stability>=90&&g.energy>=5&&m?.decision!=="HOLD";
   return Object.freeze({generation:g.n,sourceHash:g.hash,raw:g.signal,perception:round(permit?bound(g.signal*(1+offset),0,100):g.signal),permit});
  });
  const eligible=e.state==="SEALED"&&rows.every(r=>r.permit||r.generation===0)&&rows.some(r=>r.permit);
  const residual=round(rows.reduce((s,r)=>s+(r.perception-r.raw)/100,0)/rows.length);
  const outgoing=e.state==="SEALED"?(eligible?round(bound(0.5*incoming+0.25*residual,-0.125,0.125)):0):null;
  const body={schema:"ADA-218N.propagation.v1",epoch:e.epoch,state:e.state,epochHash:e.hash,mutationHash:m?.hash??null,parent,incoming,offset,residual,outgoing,growthFactor:1.025,rows:Object.freeze(rows)};
  parent=fnv64(canonical(body));out.push(Object.freeze({...body,hash:parent}));
  if(outgoing!==null)carry=outgoing;
 }
 return Object.freeze(out);
}
export function verifyPropagation(chain,ledger){
 try{return {pass:canonical(derivePropagation(chain))===canonical(ledger)}}catch(e){return {pass:false,reason:e.message}}
}
