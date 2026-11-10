// QG-054 — Cost of Knowing: finite-model, one-step net-value bound.
// Units are invented utility credits, not joules or physical capacitance.
import {ROOTS} from './ambiguous-roots.mjs';
import {measure,compatible} from './observation-sufficiency.mjs';
import {priorPartition} from './independent-information.mjs';
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const copy=x=>JSON.parse(JSON.stringify(x));
export const SETTINGS=Object.freeze({valuePerBit:1,phaseCost:0.35,amplitudeCost:0.1,movementCost:0.25,budget:1});
function validateSettings(s){
 if(!s||Object.keys(SETTINGS).some(k=>!Number.isFinite(s[k])||s[k]<0))throw Error('Invalid cost parameters');
 if(s.valuePerBit===0)return s;
 return s;
}
export function optionsAtOne(observations,settings=SETTINGS){
 validateSettings(settings);
 if(!Array.isArray(observations)||observations.length!==1||
   observations[0].step!==1||observations[0].channel!=='amplitude')throw Error('First observation required at vertex 1');
 const roots=compatible(observations);
 if(!roots.length)throw Error('Inconsistent evidence');
 // Only the repeated second 1 is available; no unauthorized additional coordinate.
 const choices=['amplitude','phase'].map(channel=>{
  const estimate=priorPartition(roots,1,channel).expectedGain;
  const cost=channel==='phase'?settings.phaseCost:settings.amplitudeCost;
  return {step:1,channel,expectedBits:estimate,benefit:estimate*settings.valuePerBit,
   cost,net:estimate*settings.valuePerBit-cost,affordable:cost<=settings.budget};
 });
 const feasible=choices.filter(c=>c.affordable&&c.net>1e-10);
 feasible.sort((a,b)=>b.net-a.net||a.cost-b.cost||a.channel.localeCompare(b.channel));
 const best=feasible[0]??null;
 return {roots,choices,decision:best?{kind:'observe',...best}:{kind:'stop',reason:choices.some(c=>c.expectedBits>0)?'not_worth_cost_or_unaffordable':'no_new_information'},settings:{...settings}};
}
export function startCost(root=5,overrides={}){
 if(!ROOTS.includes(root))throw Error('Unknown fixture root');
 const settings={...SETTINGS,...overrides};
 validateSettings(settings);
 const first={step:1,channel:'amplitude',value:measure(root,1,'amplitude')};
 return {version:'QG-054',settings,first,events:[],remaining:compatible([first]),spent:0};
}
export function verifyCost(log){
 if(!log||log.version!=='QG-054'||!Array.isArray(log.events)||log.events.length>1)throw Error('Invalid cost ledger');
 const initial=optionsAtOne([log.first],log.settings);
 let roots=initial.roots,spent=0;
 for(let i=0;i<log.events.length;i++){
  const event=log.events[i],choice=initial.decision;
  if(!choice||choice.kind!=='observe'||!event||event.index!==0||event.step!==1||event.channel!==choice.channel||
     event.estimate!==choice.expectedBits||event.cost!==choice.cost||!Number.isFinite(event.value))
    throw Error('Decision replay mismatch');
  roots=compatible([log.first,{step:1,channel:choice.channel,value:event.value}]);
  if(!roots.length||!equal(event.remaining,roots))throw Error('Observation replay mismatch');
  spent+=choice.cost;
 }
 if(!equal(roots,log.remaining)||spent!==log.spent)throw Error('Cost ledger mismatch');
 return {valid:true,remaining:[...roots],spent,observations:log.events.length+1,
   prospective:initial.decision};
}
export function appendCost(log,observedValue){
 verifyCost(log);
 if(log.events.length)throw Error('Second Fibonacci position already observed');
 const plan=optionsAtOne([log.first],log.settings).decision;
 if(!plan)throw Error('No worthwhile affordable measurement');
 if(!Number.isFinite(observedValue))throw Error('Bad observed value');
 const roots=compatible([log.first,{step:1,channel:plan.channel,value:observedValue}]);
 if(!roots.length)throw Error('Observation contradicts every root');
 return {...copy(log),events:[{index:0,step:1,channel:plan.channel,value:observedValue,
   estimate:plan.expectedBits,cost:plan.cost,remaining:roots}],remaining:roots,spent:plan.cost};
}
export function demoCost(root=5,overrides={}){
 const log=startCost(root,overrides),plan=optionsAtOne([log.first],log.settings).decision;
 return plan?appendCost(log,measure(root,1,plan.channel)):log;
}
export function threshold(root=5,settings=SETTINGS){
 const ledger=startCost(root,settings);
 const p=priorPartition(ledger.remaining,1,'phase');
 return {candidateCount:ledger.remaining.length,phaseExpectedBits:p.expectedGain,
 breakEvenPhaseCost:p.expectedGain*ledger.settings.valuePerBit,
 rule:'strictly positive net value required'};
}
