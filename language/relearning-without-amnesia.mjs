// QG-061 — Relearning Without Amnesia.
// Root-ancestry witness accounting; no trusted verification of claimed roots.
import {demo as withdrawalDemo,verify as verifyWithdrawal} from './right-to-be-wrong.mjs';
export const VERSION='QG-061';
export const REQUIRED_ROOTS=3;
const copy=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const binary=x=>x===0||x===1;
const nonblank=x=>typeof x==='string'&&x.length>0&&x.length<=120;
function candidateFrom(history){
 const v=verifyWithdrawal(history);
 if(v.authority!=='withdrawn'||v.status!=='withdraw')throw Error('Verified withdrawal required');
 // This proposal is derived from the NEW post-promotion validation batch.
 // It may coincide with an older model; such coincidence is not restoration.
 const values=history.validation;
 const rate=values.reduce((a,b)=>a+b,0)/values.length;
 return {hypothesis:rate>=.5?1:0,source:'withdrawal-validation',rate,status:'candidate'};
}
function validatePacket(packet){
 if(!packet||!nonblank(packet.id)||!nonblank(packet.surface)||!nonblank(packet.ancestryRoot)||
 !binary(packet.outcome)||packet.epoch!=='post-withdrawal')
 throw Error('Invalid or non-fresh witness packet');
}
function snapshot(packets,candidate){
 const seen=new Map(),ids=new Set(),events=[];
 for(const p of packets){
  validatePacket(p);
  if(ids.has(p.id))throw Error('Duplicate packet identifier');
  ids.add(p.id);
  const prior=seen.get(p.ancestryRoot);
  let classification;
  if(!prior){classification='independent_claim'}
  else classification=prior.outcome===p.outcome?'mirrored_or_repeated':'ancestry_conflict';
  // Map first entry must retain both measured outcome and evidence id.
  if(!prior)seen.set(p.ancestryRoot,{outcome:p.outcome,id:p.id});
  events.push({index:events.length,id:p.id,surface:p.surface,ancestryRoot:p.ancestryRoot,
   outcome:p.outcome,classification});
 }
 const roots=[...seen.entries()].map(([ancestryRoot,first])=>({ancestryRoot,outcome:first.outcome,firstId:first.id}));
 const conflict=events.some(e=>e.classification==='ancestry_conflict');
 const supporting=roots.filter(e=>e.outcome===candidate.hypothesis).length;
 const decision=conflict?'review_lineage':roots.length<REQUIRED_ROOTS?'collect':
 supporting===roots.length?'eligible_for_provisional_authority':'review_disagreement';
 return {events,roots,count:roots.length,supporting,conflict,decision};
}
export function start(history=withdrawalDemo('withdraw')){
 const candidate=candidateFrom(history);
 return {version:VERSION,withdrawal:copy(history),candidate,packets:[],witnesses:[],
  events:[],decision:'collect',authority:'withdrawn',supporting:0};
}
export function verify(record){
 if(!record||record.version!==VERSION||!Array.isArray(record.packets)||
 !Array.isArray(record.events)||!Array.isArray(record.witnesses))throw Error('Malformed relearning ledger');
 const candidate=candidateFrom(record.withdrawal);
 if(!equal(record.candidate,candidate))throw Error('Candidate derivation mismatch');
 const state=snapshot(record.packets,candidate);
 const validAuthority=(record.authority==='withdrawn'||record.authority==='provisional');
 if(!validAuthority||record.authority==='provisional'&&state.decision!=='eligible_for_provisional_authority')
 throw Error('Unauthorized restoration of model authority');
 if(!equal(record.events,state.events)||!equal(record.witnesses,state.roots)||
 record.decision!==state.decision||record.supporting!==state.supporting)
 throw Error('Witness lineage replay mismatch');
 return {valid:true,...state,authority:record.authority,candidate:copy(candidate),
  historicalAuthority:record.withdrawal.authority};
}
export function appendPacket(record,packet){
 verify(record);
 if(record.authority!=='withdrawn'||record.decision!=='collect')throw Error('Candidate collection closed');
 validatePacket(packet);
 const next={...copy(record),packets:[...copy(record.packets),copy(packet)]};
 const s=snapshot(next.packets,next.candidate);
 next.events=s.events;next.witnesses=s.roots;next.supporting=s.supporting;next.decision=s.decision;
 verify(next);return next;
}
export function authorize(record){
 const s=verify(record);
 if(record.authority!=='withdrawn')throw Error('Candidate already authorized');
 if(s.decision!=='eligible_for_provisional_authority')throw Error('Independent matching evidence requirement unmet');
 const next={...copy(record),authority:'provisional'};
 verify(next);return next;
}
export function run(packets,history=withdrawalDemo('withdraw')){
 if(!Array.isArray(packets))throw Error('Witness packets required');
 let state=start(history);
 for(const p of packets)state=appendPacket(state,p);
 return state;
}
export function demo(kind='eligible'){
 const root=start().candidate.hypothesis;
 const packets=[
 {id:'owned-git',surface:'gated-GitHub',ancestryRoot:'owned-corpus',outcome:root,epoch:'post-withdrawal'},
 {id:'owned-public',surface:'public-0root.ai',ancestryRoot:'owned-corpus',outcome:root,epoch:'post-withdrawal'},
 {id:'external-A',surface:'external-public-A',ancestryRoot:'external-A',outcome:root,epoch:'post-withdrawal'},
 {id:'external-B',surface:'external-public-B',ancestryRoot:'external-B',outcome:kind==='disagree'?1-root:root,epoch:'post-withdrawal'}];
 if(kind==='eligible')return run(packets);
 if(kind==='disagree')return run(packets);
 if(kind==='conflict')return run(packets.slice(0,2).map((p,i)=>i===1?{...p,outcome:1-root}:p));
 throw Error('Unknown demo');
}
