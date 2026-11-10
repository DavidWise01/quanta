// QG-055: bounded deterministic value of waiting at one Fibonacci vertex.
// A known schedule is a modeling assumption, not a promise about future markets.
import {ROOTS} from './ambiguous-roots.mjs';
import {measure,compatible} from './observation-sufficiency.mjs';
import {priorPartition} from './independent-information.mjs';
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const copy=x=>JSON.parse(JSON.stringify(x));
export const DEFAULT=Object.freeze({costs:[1.2,.7,.3],waitFee:.05,discount:1,valuePerBit:1,budget:2});
function valid(cfg){
 if(!cfg||!Array.isArray(cfg.costs)||cfg.costs.length<1||cfg.costs.length>13||cfg.costs.some(c=>!Number.isFinite(c)||c<0)||
 !Number.isFinite(cfg.waitFee)||cfg.waitFee<0||!Number.isFinite(cfg.discount)||cfg.discount<=0||cfg.discount>1||
 !Number.isFinite(cfg.valuePerBit)||cfg.valuePerBit<0||!Number.isFinite(cfg.budget)||cfg.budget<0)
 throw Error('Invalid finite waiting profile');
 return cfg;
}
export function selectWaitingAction(first,profile=DEFAULT,now=0){
 valid(profile);
 if(!Number.isInteger(now)||now<0||now>=profile.costs.length)throw Error('Invalid time index');
 if(!first||first.step!==1||first.channel!=='amplitude'||!Number.isFinite(first.value))throw Error('Invalid first observation');
 const roots=compatible([first]);
 if(!roots.length)throw Error('Contradictory first sample');
 const bits=priorPartition(roots,1,'phase').expectedGain;
 const alternatives=[];
 for(let at=now;at<profile.costs.length;at++){
  const delay=at-now,waiting=profile.waitFee*delay,sensor=profile.costs[at],
  affordable=waiting+sensor<=profile.budget;
  const benefit=bits*profile.valuePerBit*Math.pow(profile.discount,delay);
  const net=benefit-waiting-sensor;
  alternatives.push({at,delay,waiting,sensor,benefit,net,affordable});
 }
 // Strictly positive utility; tie breaks toward earlier observation.
 const feasible=alternatives.filter(a=>a.affordable&&a.net>1e-10);
 feasible.sort((a,b)=>b.net-a.net||a.delay-b.delay);
 const best=feasible[0];
 return {now,roots,bits,alternatives,decision:best?
 {kind:best.at===now?'observe':'wait',at:best.at,net:best.net,delay:best.delay}:
 {kind:'stop',reason:bits===0?'already_identified':'no_positive_affordable_future'}};
}
export function startWaiting(root,overrides={}){
 if(!ROOTS.includes(root))throw Error('Unknown test root');
 const profile={...copy(DEFAULT),...copy(overrides)};
 valid(profile);
 const first={step:1,channel:'amplitude',value:measure(root,1,'amplitude')};
 return {version:'QG-055',profile,first,events:[],remaining:compatible([first]),status:'open',time:0,spent:0};
}
export function verifyWaiting(record){
 if(!record||record.version!=='QG-055'||!Array.isArray(record.events)||!['open','stopped','identified'].includes(record.status))
 throw Error('Invalid waiting record');
 valid(record.profile);
 let now=0,spent=0,status='open',remaining=compatible([record.first]);
 if(!remaining.length)throw Error('Contradictory first sample');
 for(let i=0;i<record.events.length;i++){
  if(status!=='open')throw Error('Events after closure');
  const e=record.events[i],plan=selectWaitingAction(record.first,{...record.profile,budget:record.profile.budget-spent},now).decision;
  if(!e||e.index!==i||e.kind!==plan.kind||e.at!==plan.at&&e.kind!=='stop')throw Error('Decision replay mismatch');
  if(plan.kind==='stop'){
   if(e.reason!==plan.reason)throw Error('Stop reason mismatch');
   status='stopped';
  }else if(plan.kind==='wait'){
   if(e.time!==now+1||e.fee!==record.profile.waitFee)throw Error('Wait event mismatch');
   spent+=e.fee;now++;
  }else{
   if(e.time!==now||e.cost!==record.profile.costs[now]||!Number.isFinite(e.value))throw Error('Observation event mismatch');
   spent+=e.cost;
   remaining=compatible([record.first,{step:1,channel:'phase',value:e.value}]);
   if(!remaining.length||!same(remaining,e.remaining))throw Error('Evidence mismatch');
   status=remaining.length===1?'identified':'stopped';
  }
 }
 if(record.time!==now||record.spent!==spent||record.status!==status||!same(record.remaining,remaining))
 throw Error('Final replay mismatch');
 return {valid:true,time:now,spent,status,remaining};
}
export function appendWaiting(record,observedValue=null){
 verifyWaiting(record);
 if(record.status!=='open')throw Error('Closed waiting record');
 const now=record.time,plan=selectWaitingAction(record.first,{...record.profile,budget:record.profile.budget-record.spent},now).decision;
 const event={index:record.events.length,kind:plan.kind};
 let time=now,spent=record.spent,status='open',remaining=[...record.remaining];
 if(plan.kind==='stop'){event.reason=plan.reason;status='stopped'}
 else if(plan.kind==='wait'){time++;event.at=plan.at;event.time=time;event.fee=record.profile.waitFee;spent+=event.fee}
 else {
  if(!Number.isFinite(observedValue))throw Error('Measured phase sample required');
  event.at=plan.at;event.time=now;event.cost=record.profile.costs[now];event.value=observedValue;
  remaining=compatible([record.first,{step:1,channel:'phase',value:observedValue}]);
  if(!remaining.length)throw Error('Contradictory phase measurement');
  event.remaining=[...remaining];spent+=event.cost;status=remaining.length===1?'identified':'stopped';
 }
 return {...copy(record),events:[...copy(record.events),event],time,spent,status,remaining};
}
export function simulateWaiting(root=5,overrides={}){
 let record=startWaiting(root,overrides);
 for(let i=0;i<record.profile.costs.length+1&&record.status==='open';i++){
  const plan=selectWaitingAction(record.first,{...record.profile,budget:record.profile.budget-record.spent},record.time).decision;
  record=appendWaiting(record,plan.kind==='observe'?measure(root,1,'phase'):null);
 }
 verifyWaiting(record);
 return record;
}
