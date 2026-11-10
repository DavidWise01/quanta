// QG-053 No-Wasted-Movement Bound.
// Finite model selection among legal channels and current/next Fibonacci positions.
import {ROOTS} from './ambiguous-roots.mjs';
import {WALK,measure,compatible} from './observation-sufficiency.mjs';
import {priorPartition} from './independent-information.mjs';
const copy=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export const CHANNELS=Object.freeze(['amplitude','phase']);
export function chooseObservation(observations,index,{allowPhase=true,movementCost=0}={}){
 if(!Array.isArray(observations)||!Number.isInteger(index)||index<0||index>=WALK.length||!Number.isFinite(movementCost)||movementCost<0)throw Error('Invalid decision state');
 const remaining=compatible(observations);
 if(!remaining.length)throw Error('Contradictory evidence');
 if(remaining.length===1)return {kind:'stop',reason:'identified',remaining};
 const current=WALK[index],next=index+1<WALK.length?WALK[index+1]:null;
 // Current means measuring a new channel at the same coordinate, not repeating identical evidence.
 const spent=new Set(observations.filter(o=>o.step===current).map(o=>o.channel));
 const choices=[];
 for(const channel of CHANNELS){
  if(channel==='phase'&&!allowPhase)continue;
  if(!spent.has(channel)){
   const p=priorPartition(remaining,current,channel);
   choices.push({kind:'stay',step:current,channel,gain:p.expectedGain,cost:0,net:p.expectedGain});
  }
  if(next!==null&&next!==current){
   const p=priorPartition(remaining,next,channel);
   choices.push({kind:'move',step:next,channel,gain:p.expectedGain,cost:movementCost,net:p.expectedGain-movementCost});
  }
 }
 choices.sort((a,b)=>b.net-a.net || b.gain-a.gain || (a.kind==='stay'?-1:1));
 const best=choices[0];
 if(!best||best.gain<=1e-10||best.net<=1e-10)return {kind:'stop',reason:'no_positive_information_gain',remaining,choices};
 return {...best,remaining,choices};
}
export function startBound(root=5,{allowPhase=true,movementCost=0.25}={}){
 if(!ROOTS.includes(root))throw Error('Unknown synthetic root');
 const first={step:1,channel:'amplitude',value:measure(root,1,'amplitude')};
 return {version:'QG-053',index:0,allowPhase,movementCost,observations:[first],decisions:[],remaining:compatible([first])};
}
export function verifyBound(record){
 if(!record||record.version!=='QG-053'||!Number.isInteger(record.index)||record.index<0||record.index>=WALK.length||!Array.isArray(record.observations)||!Array.isArray(record.decisions))throw Error('Invalid bound record');
 let obs=[record.observations[0]],index=0;
 if(!obs[0]||obs[0].step!==1||obs[0].channel!=='amplitude'||!Number.isFinite(obs[0].value)||compatible(obs).length===0)throw Error('Invalid first observation');
 for(let i=0;i<record.decisions.length;i++){
  const event=record.decisions[i],choice=chooseObservation(obs,index,{allowPhase:record.allowPhase,movementCost:record.movementCost});
  if(!event||event.index!==i||choice.kind==='stop')throw Error('Decision discontinuity');
  if(event.kind!==choice.kind||event.step!==choice.step||event.channel!==choice.channel||Math.abs(event.expectedGain-choice.gain)>1e-10)throw Error('Decision replay mismatch');
  const observed=event.observation;
  if(!observed||observed.step!==choice.step||observed.channel!==choice.channel||!Number.isFinite(observed.value))throw Error('Observation mismatch');
  obs.push(copy(observed));
  if(!compatible(obs).length)throw Error('Contradictory observation');
  if(!eq(event.remaining,compatible(obs)))throw Error('Candidate replay mismatch');
  if(choice.kind==='move')index++;
  else if(index+1<WALK.length&&WALK[index+1]===WALK[index])index++;
 }
 if(!eq(obs,record.observations)||index!==record.index||!eq(compatible(obs),record.remaining))throw Error('Ledger mismatch');
 return {valid:true,index,remaining:[...record.remaining],events:record.decisions.length};
}
export function appendBound(record,root){
 verifyBound(record);
 if(!ROOTS.includes(root))throw Error('Invalid test root');
 const choice=chooseObservation(record.observations,record.index,{allowPhase:record.allowPhase,movementCost:record.movementCost});
 if(choice.kind==='stop')return copy(record);
 const observed={step:choice.step,channel:choice.channel,value:measure(root,choice.step,choice.channel)};
 const next=[...record.observations,observed],remaining=compatible(next);
 if(!remaining.length)throw Error('Contradictory observation');
 const index=choice.kind==='move'?record.index+1:record.index+1<WALK.length&&WALK[record.index+1]===WALK[record.index]?record.index+1:record.index;
 return {...copy(record),index,observations:next,remaining,decisions:[...copy(record.decisions),{index:record.decisions.length,kind:choice.kind,step:choice.step,channel:choice.channel,expectedGain:choice.gain,observation:observed,remaining}]};
}
export function runBound(root=5,opts={}){
 let record=startBound(root,opts);
 for(let k=0;k<WALK.length*2;k++){
  const choice=chooseObservation(record.observations,record.index,{allowPhase:record.allowPhase,movementCost:record.movementCost});
  if(choice.kind==='stop')break;
  record=appendBound(record,root);
 }
 return record;
}
