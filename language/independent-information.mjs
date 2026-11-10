// QG-052: information gain is candidate elimination under a declared model.
// No independence of physical sensors is claimed.
import {ROOTS} from './ambiguous-roots.mjs';
import {WALK,measure,compatible} from './observation-sufficiency.mjs';
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b),copy=x=>JSON.parse(JSON.stringify(x));
const log2=x=>Math.log2(x);
export function priorPartition(remaining,step=1,channel='phase'){
 if(!Array.isArray(remaining)||remaining.length<1||new Set(remaining).size!==remaining.length||remaining.some(r=>!ROOTS.includes(r))||!WALK.includes(step)||!['phase','amplitude'].includes(channel))throw Error('Invalid candidate partition');
 const groups=[];
 for(const root of remaining){
  const value=measure(root,step,channel);
  const match=groups.find(g=>Math.abs(g.value-value)<=1e-9);
  if(match)match.roots.push(root);
  else groups.push({value,roots:[root]});
 }
 const N=remaining.length;
 const expectedPosterior=groups.reduce((v,g)=>v+g.roots.length/N*log2(g.roots.length),0);
 const expectedGain=log2(N)-expectedPosterior;
 return {step,channel,prior:[...remaining],groups,expectedGain,priorEntropy:log2(N),expectedPosterior};
}
export function gainForOutcome(observations,step,channel,value){
 if(!Array.isArray(observations)||!Number.isFinite(value))throw Error('Bad sample');
 const before=compatible(observations);
 if(!before.length)throw Error('Inconsistent prior observations');
 const after=compatible([...observations,{step,channel,value}]);
 if(!after.length)throw Error('Observation contradicts all candidate roots');
 const bits=log2(before.length)-log2(after.length);
 return {before,after,bits,newInformation:bits>1e-10,step,channel,value};
}
export function startLedger(root){
 if(!ROOTS.includes(root))throw Error('Unsupported synthetic root');
 const first={step:1,channel:'amplitude',value:measure(root,1,'amplitude')};
 return {version:'QG-052',first,events:[],remaining:compatible([first])};
}
export function appendSecond(ledger,channel,value){
 verifyLedger(ledger);
 if(ledger.events.length)throw Error('Fibonacci repeated position already consumed');
 if(!['amplitude','phase'].includes(channel))throw Error('Unknown channel');
 const outcome=gainForOutcome([ledger.first],1,channel,value);
 const event={index:0,step:1,channel,value,...outcome};
 return {version:ledger.version,first:copy(ledger.first),events:[event],remaining:[...outcome.after]};
}
export function verifyLedger(ledger){
 if(!ledger||ledger.version!=='QG-052'||!ledger.first||ledger.first.step!==1||ledger.first.channel!=='amplitude'||!Array.isArray(ledger.events)||ledger.events.length>1||!Array.isArray(ledger.remaining))throw Error('Malformed ledger');
 const prior=compatible([ledger.first]);
 if(!prior.length)throw Error('Initial measurement has no explaining root');
 let last=prior;
 for(let i=0;i<ledger.events.length;i++){
  const e=ledger.events[i];
  if(!e||e.index!==i||e.step!==1)throw Error('Wrong observation index or position');
  const expected=gainForOutcome([ledger.first],e.step,e.channel,e.value);
  const cmp={index:0,step:1,channel:e.channel,value:e.value,...expected};
  if(!same(e,cmp))throw Error('Evidence or information-gain mismatch');
  last=expected.after;
 }
 if(!same(last,ledger.remaining))throw Error('Candidate history mismatch');
 return {valid:true,observations:1+ledger.events.length,remaining:[...last]};
}
export function compareChannels(hiddenRoot=5){
 const first=startLedger(hiddenRoot);
 const sameValue=measure(hiddenRoot,1,'amplitude');
 const phaseValue=measure(hiddenRoot,1,'phase');
 const repeated=appendSecond(first,'amplitude',sameValue);
 const diversified=appendSecond(first,'phase',phaseValue);
 return {first,repeated,diversified,
  amplitudeForecast:priorPartition(first.remaining,1,'amplitude'),
  phaseForecast:priorPartition(first.remaining,1,'phase')};
}
export function auditAll(){
 return ROOTS.map(root=>{
  const {repeated,diversified,phaseForecast}=compareChannels(root);
  return {root,repeatedBits:repeated.events[0].bits,phaseBits:diversified.events[0].bits,
   phaseExpectedGain:phaseForecast.expectedGain,remaining:diversified.remaining};
 });
}
