// QG-056: uncertain future cost, finite one-tick decision.
// Forecast probabilities are assumptions. Realized outcomes are supplied separately.
import {ROOTS} from './ambiguous-roots.mjs';
import {measure,compatible} from './observation-sufficiency.mjs';
import {priorPartition} from './independent-information.mjs';
const cp=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const TOL=1e-10;
export const DEFAULT=Object.freeze({
 currentCost:.8, waitFee:.05, valuePerBit:1, budget:2,
 future:[{price:.2,probability:.6},{price:1.4,probability:.4}]
});
function config(o){
 const x={...DEFAULT,...cp(o),future:cp(o?.future??DEFAULT.future)};
 if(!Number.isFinite(x.currentCost)||x.currentCost<0||!Number.isFinite(x.waitFee)||x.waitFee<0||
 !Number.isFinite(x.valuePerBit)||x.valuePerBit<0||!Number.isFinite(x.budget)||x.budget<0||
 !Array.isArray(x.future)||!x.future.length||x.future.length>16||
 x.future.some(v=>!v||!Number.isFinite(v.price)||v.price<0||!Number.isFinite(v.probability)||v.probability<0))
 throw Error('Invalid forecast');
 if(Math.abs(x.future.reduce((a,b)=>a+b.probability,0)-1)>1e-9)throw Error('Probabilities must sum to 1');
 return x;
}
export function evaluate(first,options={}){
 const x=config(options),roots=compatible([first]);
 if(!first||first.step!==1||first.channel!=='amplitude'||!roots.length)throw Error('Invalid first observation');
 const bits=priorPartition(roots,1,'phase').expectedGain,benefit=bits*x.valuePerBit;
 const buyNow= x.currentCost<=x.budget? benefit-x.currentCost : -Infinity;
 const outcomes=x.future.map((v,i)=>{
  const affordable=x.waitFee+v.price<=x.budget+TOL;
  const net=benefit-v.price;
  return {index:i,price:v.price,probability:v.probability,affordable,
   conditionalAction:affordable&&net>TOL?'buy':'stop',conditionalSurplus:affordable?Math.max(0,net):0};
 });
 const expectedFuture=outcomes.reduce((v,o)=>v+o.probability*o.conditionalSurplus,0);
 const wait= x.waitFee<=x.budget ? expectedFuture-x.waitFee : -Infinity;
 let decision={kind:'stop',reason:bits===0?'already_identified':'no_positive_expected_value',expectedNet:0};
 // Earlier action wins ties; no optionality is silently assigned to 'buy now'.
 if(buyNow>TOL)decision={kind:'buy_now',expectedNet:buyNow};
 if(wait>Math.max(0,buyNow)+TOL)decision={kind:'wait',expectedNet:wait};
 return {config:x,roots,bits,benefit,buyNow,wait,expectedFuture,outcomes,decision};
}
export function start(root=5,options={}){
 if(!ROOTS.includes(root))throw Error('Unsupported fixture root');
 const first={step:1,channel:'amplitude',value:measure(root,1,'amplitude')};
 return {version:'QG-056',first,forecast:config(options),events:[],
 phase:'initial',remaining:compatible([first]),spent:0};
}
export function verify(record){
 if(!record||record.version!=='QG-056'||!Array.isArray(record.events)||record.events.length>2)throw Error('Invalid ledger');
 const f=evaluate(record.first,record.forecast);
 let phase='initial',spent=0,remaining=f.roots;
 for(let i=0;i<record.events.length;i++){
  const e=record.events[i];
  if(!e||e.index!==i)throw Error('Event index mismatch');
  if(phase==='initial'){
   if(e.action!==f.decision.kind||!eq(e.priorForecast,f))throw Error('Policy or forecast replay mismatch');
   if(e.action==='stop'){phase='stopped';}
   else if(e.action==='wait'){phase='waiting';spent+=f.config.waitFee;}
   else if(e.action==='buy_now'){
    if(!Number.isFinite(e.value))throw Error('Missing measurement');
    remaining=compatible([record.first,{step:1,channel:'phase',value:e.value}]);
    if(!remaining.length||!eq(remaining,e.remaining))throw Error('Measurement replay mismatch');
    spent+=f.config.currentCost;phase='observed';
   }else throw Error('Unknown action');
  }else if(phase==='waiting'){
   if(e.action!=='reveal'||!Number.isSafeInteger(e.outcomeIndex)||e.outcomeIndex<0||e.outcomeIndex>=f.outcomes.length)
    throw Error('Invalid realized outcome');
   const outcome=f.outcomes[e.outcomeIndex];
   if(e.observedPrice!==outcome.price||e.conditionalAction!==outcome.conditionalAction)throw Error('Outcome mismatch');
   if(outcome.conditionalAction==='buy'){
    if(!Number.isFinite(e.value))throw Error('Missing future measurement');
    remaining=compatible([record.first,{step:1,channel:'phase',value:e.value}]);
    if(!remaining.length||!eq(remaining,e.remaining))throw Error('Future observation mismatch');
    spent+=outcome.price;phase='observed';
   }else if(e.value!==null||!eq(e.remaining,remaining))throw Error('Unobserved outcome fabricated evidence');
   else phase='stopped';
  }else throw Error('Events after terminal decision');
 }
 if(phase!==record.phase||spent!==record.spent||!eq(remaining,record.remaining))throw Error('Ledger total mismatch');
 return {valid:true,phase,spent,remaining:[...remaining],decision:f.decision};
}
export function decide(record,observedValue=null){
 verify(record);
 if(record.phase!=='initial')throw Error('Decision already made');
 const f=evaluate(record.first,record.forecast),d=f.decision;
 const e={index:0,action:d.kind,priorForecast:cp(f)};
 let remaining=[...record.remaining],phase='stopped',spent=0;
 if(d.kind==='wait'){phase='waiting';spent=f.config.waitFee}
 if(d.kind==='buy_now'){
  if(!Number.isFinite(observedValue))throw Error('Now measurement required');
  remaining=compatible([record.first,{step:1,channel:'phase',value:observedValue}]);
  if(!remaining.length)throw Error('Contradictory observation');
  e.value=observedValue;e.remaining=[...remaining];spent=f.config.currentCost;phase='observed';
 }
 return {...cp(record),events:[e],phase,spent,remaining};
}
export function reveal(record,outcomeIndex,observedValue=null){
 verify(record);
 if(record.phase!=='waiting')throw Error('No pending waiting opportunity');
 const f=evaluate(record.first,record.forecast),o=f.outcomes[outcomeIndex];
 if(!o)throw Error('Outcome not in forecast support');
 const e={index:1,action:'reveal',outcomeIndex,observedPrice:o.price,conditionalAction:o.conditionalAction,value:null,remaining:[...record.remaining]};
 let phase='stopped',spent=record.spent,remaining=[...record.remaining];
 if(o.conditionalAction==='buy'){
  if(!Number.isFinite(observedValue))throw Error('Future measurement required');
  remaining=compatible([record.first,{step:1,channel:'phase',value:observedValue}]);
  if(!remaining.length)throw Error('Contradictory future observation');
  e.value=observedValue;e.remaining=[...remaining];spent+=o.price;phase='observed';
 }
 return {...cp(record),events:[...cp(record.events),e],phase,spent,remaining};
}
export function demonstrate(root=5,index=0,options={}){
 let l=start(root,options),d=evaluate(l.first,l.forecast).decision;
 l=decide(l,d.kind==='buy_now'?measure(root,1,'phase'):null);
 if(l.phase==='waiting'){
  const x=evaluate(l.first,l.forecast).outcomes[index];
  l=reveal(l,index,x?.conditionalAction==='buy'?measure(root,1,'phase'):null);
 }
 return l;
}
