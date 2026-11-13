// QG-076 — Withdrawal Must Reach Every Agent.
// A trusted independent withdrawal checkpoint is required for all modeled publication.
// Full snapshot hash and min sequence are external inputs; never derived from agent memory.
// No actual network synchronization or live publishing is performed.
import {start as startWithdrawal,petition,review,withdraw,verify as verifyWithdrawal,authorizePublication as publicationGate} from './release-withdrawal.mjs';
import {fixture as releaseFixture,propose as proposeRelease,review as reviewRelease,approve as approveRelease,scopeFixture} from './independent-declassification.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-076',REQUIRED_WITHDRAWAL_SEQUENCE=1;
const copy=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>canonical(a)===canonical(b);
const validId=x=>typeof x==='string'&&/^[a-zA-Z0-9._-]{1,80}$/.test(x);
function validatePin(pin){
 if(!pin||!pin.withdrawalPin||!pin.withdrawalPin.releasePolicy||
 !Number.isSafeInteger(pin.withdrawalPin.minWithdrawalSequence)||
 pin.withdrawalPin.minWithdrawalSequence<REQUIRED_WITHDRAWAL_SEQUENCE||
 typeof pin.headDigest!=='string'||!/^[0-9a-f]{64}$/.test(pin.headDigest))
 throw Error('Independently pinned withdrawal floor and head digest required');
}
export async function inspectAgent(report,pin){
 validatePin(pin);
 if(!report||!validId(report.agentId)||!['online','offline'].includes(report.connection)||
 !report.snapshot)throw Error('Malformed hive withdrawal report');
 const digest=await sha256(canonical(report.snapshot));
 if(report.connection==='offline')return {agentId:report.agentId,state:'offline',mayPublish:false,
  digest,reason:'offline cannot establish current withdrawal state'};
 let proof;
 try{proof=await verifyWithdrawal(report.snapshot,pin.withdrawalPin)}
 catch(e){
  try{
   await verifyWithdrawal(report.snapshot,{...pin.withdrawalPin,minWithdrawalSequence:0});
   return {agentId:report.agentId,state:'stale',mayPublish:false,
    digest,reason:'withdrawal floor not met'};
  }catch{}
  return {agentId:report.agentId,state:'invalid',mayPublish:false,
   digest,reason:'signed release or withdrawal replay failed'};
 }
 if(digest!==pin.headDigest)return {agentId:report.agentId,state:'stale',mayPublish:false,
  digest,reason:'snapshot differs from independently pinned current head'};
 return {agentId:report.agentId,state:'current',mayPublish:true,
  digest,reason:'verified exact current withdrawal checkpoint',withdrawals:proof.withdrawals};
}
export async function start(independentPin){
 validatePin(independentPin);
 return {version:VERSION,pin:copy(independentPin),reports:[],receipts:[]};
}
export async function verify(ledger,independentPin){
 validatePin(independentPin);
 if(!ledger||ledger.version!==VERSION||!same(ledger.pin,independentPin)||
 !Array.isArray(ledger.reports)||!Array.isArray(ledger.receipts)||
 ledger.reports.length!==ledger.receipts.length)throw Error('Hive withdrawal ledger or independent pin mismatch');
 const ids=new Set(),actual=[];
 for(const report of ledger.reports){
  if(ids.has(report?.agentId))throw Error('Duplicate agent identity');
  ids.add(report.agentId);
  actual.push(await inspectAgent(report,independentPin));
 }
 if(!same(actual,ledger.receipts))throw Error('Hive withdrawal receipts tampered');
 return {valid:true,total:actual.length,current:actual.filter(x=>x.state==='current').length,
  stale:actual.filter(x=>x.state==='stale').length,
  offline:actual.filter(x=>x.state==='offline').length,
  invalid:actual.filter(x=>x.state==='invalid').length,receipts:actual};
}
export async function append(ledger,report,independentPin){
 await verify(ledger,independentPin);
 if(ledger.reports.some(x=>x.agentId===report?.agentId))throw Error('Duplicate agent identity');
 const next={...copy(ledger),reports:[...copy(ledger.reports),copy(report)]};
 next.receipts=await Promise.all(next.reports.map(x=>inspectAgent(x,independentPin)));
 await verify(next,independentPin);return next;
}
export async function authorizePublication(ledger,agentId,releaseId,scope,trust,clock,independentPin){
 await verify(ledger,independentPin);
 const index=ledger.reports.findIndex(r=>r.agentId===agentId);
 if(index<0||!ledger.receipts[index].mayPublish)throw Error('Agent publication denied: stale, offline or invalid');
 const record=ledger.reports[index].snapshot;
 const authorization=await publicationGate(record,releaseId,scope,trust,clock,independentPin.withdrawalPin);
 return {agentId,releaseId,allowed:true,verifiedHeadDigest:independentPin.headDigest,
  withdrawalSequence:record.events.length,authorization};
}
export async function fixture(mode='mixed'){
 const source=await releaseFixture('valid');
 let releases=source.record;
 const text='A second independently approved synthetic public artifact.';
 const p=await proposeRelease(releases,{id:'release-2',nodeId:'out',publicText:text},source.policy);
 const v=await Promise.all([0,1,2].map(i=>reviewRelease(p,'reviewer-'+i,source.reviewers[i].privateKey)));
 releases=await approveRelease(releases,p,text,v,source.policy);
 const withdrawalPin={releasePolicy:copy(source.policy),minWithdrawalSequence:0};
 const stale=await startWithdrawal(releases,withdrawalPin);
 const wp=await petition(stale,'release-1',withdrawalPin);
 const votes=await Promise.all([0,1,2].map(i=>review(wp,'reviewer-'+i,source.reviewers[i].privateKey)));
 const current=await withdraw(stale,wp,votes,withdrawalPin);
 const pin={withdrawalPin:{...copy(withdrawalPin),minWithdrawalSequence:1},
  headDigest:await sha256(canonical(current))};
 const invalid=copy(current);invalid.events[0].votes[0].signature='AAAA';
 const divergent=copy(current);divergent.events[0].votes.reverse(); // valid same floor, different head
 const packets={
  current:{agentId:'agent-a',connection:'online',snapshot:copy(current)},
  stale:{agentId:'agent-b',connection:'online',snapshot:copy(stale)},
  offline:{agentId:'agent-c',connection:'offline',snapshot:copy(current)},
  invalid:{agentId:'agent-d',connection:'online',snapshot:invalid},
  divergent:{agentId:'agent-e',connection:'online',snapshot:divergent}
 };
 const selection=mode==='mixed'?['current','stale','offline','invalid','divergent']:
  mode==='current'?[mode]:mode==='stale'?[mode]:mode==='offline'?[mode]:
  mode==='invalid'?[mode]:mode==='divergent'?[mode]:null;
 if(!selection)throw Error('Unknown fixture mode');
 let ledger=await start(pin);
 for(const id of selection)ledger=await append(ledger,packets[id],pin);
 return {ledger,pin,packets,source,scope:await scopeFixture()};
}
