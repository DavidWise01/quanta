/**
 * QG-042.1 — Observer's Discovery.
 * Deterministic candidate selection uses training labels only.
 * An untouched holdout checks whether a proposed replacement predicts a
 * separately supplied proxy better than the QG-041 utility weights.
 * Discovery is a model comparison, not subjective experience or self-awareness.
 */
import {verifyObserverStrict} from "./emergent-observer.mjs";
export const VERSION="QG-042.1";
export const BASELINE=Object.freeze([2,0.75,1,-1]);
export const CANDIDATES=Object.freeze([
 Object.freeze([0.5,2,0.2,-0.3]),
 Object.freeze([1,1.5,0.5,-0.5]),
 Object.freeze([2,0.75,1,-1]),
 Object.freeze([0.1,2.5,0.1,-0.2])
]);
const clone=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const fail=msg=>{throw Error(msg)};
const rounded=v=>Math.round(v*1e9)/1e9;
const compute=(weights,features)=>rounded(weights.reduce((sum,w,i)=>sum+w*features[i],0));
const mse=(weights,rows)=>rounded(rows.reduce((sum,r)=>sum+(compute(weights,r.features)-r.target)**2,0)/rows.length);
function features(state,i){
 const e=state.events[i],h=state.history[i];
 return [h.novelPatterns,h.distinctGames,e.payoff,e.cost];
}
function checkLabels(labels,size){
 if(!Array.isArray(labels)||labels.length!==size||labels.some((v,i)=>!v||Object.keys(v).sort().join(",")!=="event,target"||v.event!==i||typeof v.target!=="number"||!Number.isFinite(v.target)||v.target<0||v.target>20))fail("Every event needs one bounded independently supplied outcome label");
}
function records(state,labels){
 verifyObserverStrict(state);
 checkLabels(labels,state.events.length);
 if(state.events.length<12||state.events.length>128)fail("At least 12 original experiences required");
 const rows=labels.map((label,i)=>({event:i,mode:state.events[i].mode,features:features(state,i),target:label.target}));
 const cut=Math.floor(rows.length*2/3);
 if(cut<8||rows.length-cut<4)fail("Insufficient split");
 for(const portion of [rows.slice(0,cut),rows.slice(cut)])
  if(!["play","observe"].every(mode=>portion.some(r=>r.mode===mode)))fail("Both modes required in training and holdout");
 return {train:rows.slice(0,cut),holdout:rows.slice(cut),cut};
}
function calculate(state,labels,margin){
 if(!(typeof margin==="number"&&Number.isFinite(margin)&&margin>=0&&margin<=2))fail("Invalid improvement threshold");
 const {train,holdout,cut}=records(state,labels);
 const baselineTrain=mse(BASELINE,train),baselineHoldout=mse(BASELINE,holdout);
 // The candidate is chosen on training outcomes only, not the holdout.
 const ranked=CANDIDATES.map((w,index)=>({index,trainingMse:mse(w,train)}))
   .sort((a,b)=>a.trainingMse-b.trainingMse||a.index-b.index);
 const best=ranked[0],candidate=[...CANDIDATES[best.index]];
 const candidateHoldout=mse(candidate,holdout);
 const accepted=best.trainingMse+margin<baselineTrain&&candidateHoldout+margin<baselineHoldout;
 return {cut,trainingCount:train.length,holdoutCount:holdout.length,baseline:[...BASELINE],candidate,
  baselineTrain,baselineHoldout,candidateTrain:best.trainingMse,candidateHoldout,
  accepted,decision:accepted?"adopt-proposal":"retain-baseline",independentTruthProven:false};
}
function replay(state,labels,margin,events){
 const s={version:VERSION,source:clone(state),labels:clone(labels),margin,events:[],result:null};
 // Replay result is derived from frozen inputs; only one evaluation is permitted.
 for(let i=0;i<events.length;i++){
  const e=events[i];
  if(!e||e.index!==i||e.parent!==(i?"e"+String(i-1).padStart(4,"0"):null)||
   e.kind!=="evaluate"||i!==0||Object.keys(e).sort().join(",")!=="index,kind,parent")fail("Invalid discovery ledger");
  s.result=calculate(s.source,s.labels,s.margin);
  s.events.push(clone(e));
 }
 return s;
}
export function instantiateDiscovery(state,labels,{margin=0.1}={}){
 // Require valid inputs even before first evaluation.
 calculate(state,labels,margin);
 return replay(state,labels,margin,[]);
}
export function appendDiscoveryEvaluation(s){
 verifyDiscoveryStrict(s);
 if(s.events.length)fail("One precommitted holdout evaluation per discovery");
 return replay(s.source,s.labels,s.margin,[{kind:"evaluate",index:0,parent:null}]);
}
export function verifyDiscoveryStrict(s){
 if(!s||s.version!==VERSION||!Array.isArray(s.events)||s.events.length>1)fail("Invalid discovery state");
 calculate(s.source,s.labels,s.margin);
 const expected=replay(s.source,s.labels,s.margin,s.events);
 if(!equal(expected,s))fail("Discovery replay mismatch");
 return {pass:true,evaluated:!!s.result,decision:s.result?.decision||"undetermined"};
}
export function verifyDiscovery(s){try{return verifyDiscoveryStrict(s)}catch(e){return {pass:false,error:e.message}}}
export function simulatedDiscovery({scenario="positive"}={}){
 if(!["positive","negative","mixed"].includes(scenario))fail("Unknown fixture");
 // Samples include both modes in training AND holdout, rather than using
 // QG-041's original all-play-then-all-observe demo chronology.
 const {instantiateObserver,appendExperience}=simulationImports();
 let state=instantiateObserver();
 for(let i=0;i<18;i++){
  const observe=i%3!==0;
  state=appendExperience(state,observe?
   {mode:"observe",games:["arena","chess","go"],patterns:["watch"+i],payoff:0.3,cost:1}:
   {mode:"play",game:"arena",patterns:["play"+i],payoff:2,cost:0.4});
 }
 const labels=state.events.map((e,i)=>{
  const f=features(state,i);
  const truth=scenario==="positive"?CANDIDATES[0]:scenario==="negative"?BASELINE:
    (i<12?CANDIDATES[0]:BASELINE);
  return {event:i,target:compute(truth,f)};
 });
 return instantiateDiscovery(state,labels);
}
// Reuse a static import, never dynamic loading or background processes.
import {instantiateObserver,appendExperience} from "./emergent-observer.mjs";
function simulationImports(){return {instantiateObserver,appendExperience}}
