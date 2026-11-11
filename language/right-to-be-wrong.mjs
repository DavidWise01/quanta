// QG-060 — The right to be wrong: retract CURRENT authority, not historical evidence.
// One fixed, new validation window; no claim of general, universal drift detection.
import {demo as promotedFixture,verify as verifyHandoff} from './sealed-model-handoff.mjs';
export const VERSION='QG-060';
const copy=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const binary=x=>x===0||x===1;
const avg=v=>v.reduce((s,x)=>s+x,0)/v.length;
function fromPromotion(handoff){
 const source=verifyHandoff(handoff);
 if(source.decision!=='promote'||!source.ready)throw Error('A verified promoted handoff is required');
 const n=handoff.confirmation.length,alpha=handoff.sealedOld.config.alpha;
 const promotedRate=avg(handoff.confirmation);
 return {n,alpha,promotedRate,source};
}
function expected(ledger){
 if(!ledger||ledger.version!==VERSION||!Array.isArray(ledger.validation)||!Array.isArray(ledger.events))throw Error('Malformed withdrawal ledger');
 const {n,alpha,promotedRate}=fromPromotion(ledger.promotion);
 if(ledger.validation.length>n||!ledger.validation.every(binary))throw Error('Invalid fresh validation window');
 if(ledger.events.length!==ledger.validation.length)throw Error('Event count mismatch');
 for(let i=0;i<ledger.events.length;i++){
  const e=ledger.events[i];
  if(!e||e.index!==i||e.outcome!==ledger.validation[i]||e.source!=='fresh-QG-060-validation')throw Error('Event lineage mismatch');
 }
 if(ledger.validation.length<n)return {n,alpha,promotedRate,ready:false,authority:'provisional',status:'collect',count:ledger.validation.length,rate:null,delta:null,threshold:null};
 const rate=avg(ledger.validation);
 // Single two-sample comparison: Hoeffding + union bound under iid Bernoulli assumption.
 const threshold=Math.sqrt(Math.log(4/alpha)/(2*n))+Math.sqrt(Math.log(4/alpha)/(2*n));
 const delta=Math.abs(promotedRate-rate);
 return {n,alpha,promotedRate,ready:true,authority:delta>threshold?'withdrawn':'provisional',
  status:delta>threshold?'withdraw':'retain',count:n,rate,delta,threshold};
}
export function seed(promoted){
 fromPromotion(promoted);
 return {version:VERSION,promotion:copy(promoted),validation:[],events:[],decision:'collect',
   authority:'provisional',withdrawal:null};
}
export function verify(ledger){
 const s=expected(ledger);
 if(ledger.decision!==s.status||ledger.authority!==s.authority)throw Error('Authority replay mismatch');
 const expectedWithdrawal=s.status==='withdraw'?{
  trigger:'post-promotion-validation',oldAuthority:'provisional',newAuthority:'withdrawn',
  referenceRate:s.promotedRate,newRate:s.rate,delta:s.delta,threshold:s.threshold,
  preservedPromotion:true
 }:null;
 if(!eq(ledger.withdrawal,expectedWithdrawal))throw Error('Withdrawal certificate mismatch');
 return {valid:true,...s,preservedPromotion:true};
}
export function append(ledger,outcome){
 verify(ledger);
 if(ledger.decision!=='collect')throw Error('Validation window is closed');
 if(!binary(outcome))throw Error('Only binary fresh observations allowed');
 const i=ledger.validation.length,next={
  ...copy(ledger),
  validation:[...ledger.validation,outcome],
  events:[...copy(ledger.events),{index:i,outcome,source:'fresh-QG-060-validation'}]
 };
 const state=expected(next);
 next.decision=state.status;
 next.authority=state.authority;
 if(state.status==='withdraw')next.withdrawal={
  trigger:'post-promotion-validation',oldAuthority:'provisional',newAuthority:'withdrawn',
  referenceRate:state.promotedRate,newRate:state.rate,delta:state.delta,threshold:state.threshold,
  preservedPromotion:true
 };
 verify(next);
 return next;
}
export function run(outcomes,promotion=promotedFixture('promote')){
 if(!Array.isArray(outcomes))throw Error('Validation outcomes must be an array');
 let state=seed(promotion);
 for(const outcome of outcomes)state=append(state,outcome);
 return state;
}
export function demo(type='withdraw'){
 if(type==='withdraw')return run(Array(20).fill(0));
 if(type==='retain')return run(Array(20).fill(1));
 throw Error('Unsupported demonstration fixture');
}
