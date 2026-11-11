// QG-057 — Forecast Reliability. All predictions issued before outcomes.
// Finite Bernoulli calibration with an explicit Beta(3,2) illustrative prior.
// Value-based replay is not an authenticated external event record.
export const VERSION='QG-057';
export const PRIOR=Object.freeze({low:3,high:2});
export const DEFAULT_BINS=Object.freeze([0,.2,.4,.6,.8,1]);
const copy=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const validProbability=p=>typeof p==='number'&&Number.isFinite(p)&&p>=0&&p<=1;
function checkPrior(prior){
 if(!prior||!Number.isSafeInteger(prior.low)||!Number.isSafeInteger(prior.high)||prior.low<=0||prior.high<=0)throw Error('Invalid prior');
}
export function startCalibration(prior=PRIOR){
 checkPrior(prior);
 return {version:VERSION,prior:copy(prior),events:[],pending:null,samples:0,low:0};
}
export function nextForecast(ledger){
 verifyCalibration(ledger);
 if(ledger.pending!==null)throw Error('Unresolved forecast');
 return (ledger.prior.low+ledger.low)/(ledger.prior.low+ledger.prior.high+ledger.samples);
}
export function issueForecast(ledger){
 verifyCalibration(ledger);
 if(ledger.pending!==null)throw Error('Resolve previous forecast first');
 const probability=(ledger.prior.low+ledger.low)/(ledger.prior.low+ledger.prior.high+ledger.samples);
 const pending={id:ledger.events.length+1,probability,issuedAfter:ledger.events.length};
 return {...copy(ledger),pending};
}
export function resolveForecast(ledger,outcome){
 verifyCalibration(ledger);
 if(!ledger.pending)throw Error('A prediction must precede an outcome');
 if(outcome!==0&&outcome!==1)throw Error('Outcome must be 0 or 1');
 const p=ledger.pending.probability,entry={...copy(ledger.pending),outcome,brier:(p-outcome)**2};
 return {...copy(ledger),events:[...copy(ledger.events),entry],pending:null,
  samples:ledger.samples+1,low:ledger.low+outcome};
}
export function verifyCalibration(ledger){
 if(!ledger||ledger.version!==VERSION||!Array.isArray(ledger.events)||!Number.isSafeInteger(ledger.samples)||
  !Number.isSafeInteger(ledger.low)||ledger.pending!==null&&typeof ledger.pending!=='object')throw Error('Malformed forecast ledger');
 checkPrior(ledger.prior);
 let low=0;
 for(let i=0;i<ledger.events.length;i++){
  const event=ledger.events[i],probability=(ledger.prior.low+low)/(ledger.prior.low+ledger.prior.high+i);
  if(!event||event.id!==i+1||event.issuedAfter!==i||!validProbability(event.probability)||
   Math.abs(event.probability-probability)>1e-12||(event.outcome!==0&&event.outcome!==1)||
   Math.abs(event.brier-(event.probability-event.outcome)**2)>1e-12)
   throw Error('Forecast/outcome lineage mismatch at '+i);
  low+=event.outcome;
 }
 if(ledger.samples!==ledger.events.length||ledger.low!==low)throw Error('Forecast totals mismatch');
 if(ledger.pending){
  const p=(ledger.prior.low+low)/(ledger.prior.low+ledger.prior.high+ledger.events.length);
  if(ledger.pending.id!==ledger.events.length+1||ledger.pending.issuedAfter!==ledger.events.length||
   !validProbability(ledger.pending.probability)||Math.abs(ledger.pending.probability-p)>1e-12)
   throw Error('Pending forecast cannot be backdated or edited');
 }
 return {valid:true,count:ledger.samples,low:ledger.low,pending:ledger.pending!==null};
}
export function reportCalibration(ledger,bins=DEFAULT_BINS){
 verifyCalibration(ledger);
 if(!Array.isArray(bins)||bins.length<2||bins[0]!==0||bins.at(-1)!==1||
  bins.some((x,i)=>!validProbability(x)||(i>0&&x<=bins[i-1])))throw Error('Invalid bins');
 const count=ledger.samples,meanBrier=count?ledger.events.reduce((s,e)=>s+e.brier,0)/count:null;
 const calibration=bins.slice(0,-1).map((start,i)=>{
  const end=bins[i+1],group=ledger.events.filter(e=>e.probability>=start&&(i===bins.length-2?e.probability<=end:e.probability<end));
  return {start,end,count:group.length,meanForecast:group.length?group.reduce((s,e)=>s+e.probability,0)/group.length:null,
   observedRate:group.length?group.reduce((s,e)=>s+e.outcome,0)/group.length:null};
 });
 return {samples:count,successes:ledger.low,empiricalRate:count?ledger.low/count:null,
  nextPredictedLow:(ledger.prior.low+ledger.low)/(ledger.prior.low+ledger.prior.high+count),
  meanBrier,calibration,warning:count<20?'Small-sample calibration is uncertain':'Sample size alone does not prove calibration',
  provenance:'one synthetic outcome stream; no independent witnesses'};
}
export function runSequence(outcomes,prior=PRIOR){
 if(!Array.isArray(outcomes))throw Error('Outcomes must be an array');
 let ledger=startCalibration(prior);
 for(const result of outcomes)ledger=resolveForecast(issueForecast(ledger),result);
 verifyCalibration(ledger);return ledger;
}
