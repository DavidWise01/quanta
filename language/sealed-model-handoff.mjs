// QG-059 — preserve old model and trial a provisional replacement.
// Local value-based records; no cryptographic sealing or independent witnesses.
import {demo as demoShift,verify as verifyChange} from './change-versus-noise.mjs';
export const VERSION='QG-059';
const clone=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const binary=x=>x===0||x===1;
function avg(v){return v.reduce((a,b)=>a+b,0)/v.length}
export function seed(alertLedger){
 const verified=verifyChange(alertLedger);
 if(verified.status!=='review'||!verified.checkpoints.at(-1)?.alert)throw Error('Shift alert required');
 const cfg=alertLedger.config;
 const raw=alertLedger.events.map(e=>e.outcome);
 const old=raw.slice(0,cfg.baselineSize);
 // QG-058 stops at the first alert; its last completed batch is candidate seed.
 const candidate=raw.slice(-cfg.batchSize);
 if(old.length!==cfg.baselineSize||candidate.length!==cfg.batchSize)throw Error('Incomplete evidence');
 const initial={version:VERSION,sealedOld:clone(alertLedger),oldModel:{
  count:old.length,rate:avg(old),status:'sealed_by_value'
 },candidate:{seedCount:candidate.length,seedRate:avg(candidate),status:'provisional'},
 confirmation:[],events:[],decision:'pending'};
 return initial;
}
export function assessment(record){
 if(!record||record.version!==VERSION)throw Error('Invalid replacement record');
 const original=verifyChange(record.sealedOld);
 if(original.status!=='review'||!original.checkpoints.at(-1)?.alert)throw Error('Missing valid shift alert');
 const cfg=record.sealedOld.config,raw=record.sealedOld.events.map(e=>e.outcome);
 const base=raw.slice(0,cfg.baselineSize),seedBatch=raw.slice(-cfg.batchSize);
 if(!equal(record.oldModel,{count:base.length,rate:avg(base),status:'sealed_by_value'})||
 !equal(record.candidate,{seedCount:seedBatch.length,seedRate:avg(seedBatch),status:'provisional'}))
 throw Error('Sealed source mismatch');
 if(!Array.isArray(record.confirmation)||record.confirmation.length>cfg.batchSize||!record.confirmation.every(binary))throw Error('Invalid confirmation');
 if(record.confirmation.length<cfg.batchSize)return {ready:false,decision:'pending',collected:record.confirmation.length,required:cfg.batchSize};
 const alpha=cfg.alpha;
 // One fixed confirmatory comparison, not an indefinite repeated test.
 const threshold=Math.sqrt(Math.log(4/alpha)/(2*seedBatch.length))
  +Math.sqrt(Math.log(4/alpha)/(2*record.confirmation.length));
 const gap=Math.abs(avg(record.confirmation)-avg(seedBatch));
 // Consistency check with provisional seed is not proof of a physical regime shift.
 return {ready:true,decision:gap>threshold?'reject':'promote',collected:record.confirmation.length,
  required:cfg.batchSize,gap,threshold,confirmedRate:avg(record.confirmation)};
}
export function verify(record){
 const state=assessment(record);
 if(!Array.isArray(record.events)||record.events.length!==record.confirmation.length)throw Error('Evidence length mismatch');
 for(let i=0;i<record.events.length;i++){
  const e=record.events[i];
  if(!e||e.index!==i||e.outcome!==record.confirmation[i])throw Error('Confirmation provenance mismatch');
 }
 if(record.decision!==state.decision)throw Error('Decision replay mismatch');
 return {valid:true,...state,oldRate:record.oldModel.rate,candidateRate:record.candidate.seedRate,
  events:record.events.length};
}
export function append(record,outcome){
 verify(record);
 if(record.decision!=='pending')throw Error('Candidate already decided');
 if(!binary(outcome))throw Error('Binary observation required');
 const index=record.confirmation.length;
 const next={...clone(record),confirmation:[...record.confirmation,outcome],
  events:[...clone(record.events),{index,outcome}]};
 next.decision=assessment(next).decision;
 verify(next);
 return next;
}
export function run(outcomes,alert=demoShift('shift')){
 if(!Array.isArray(outcomes))throw Error('Need confirmation outcomes');
 let state=seed(alert);
 for(const outcome of outcomes)state=append(state,outcome);
 return state;
}
export function demo(kind='promote'){
 if(kind==='promote')return run(Array(20).fill(1));
 if(kind==='reject')return run(Array(20).fill(0));
 throw Error('Unsupported demonstration');
}
