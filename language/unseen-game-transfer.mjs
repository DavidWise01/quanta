/**
 * QG-043.1 — Unseen-game transfer.
 * Training and transfer sets have DISJOINT game identities.
 * Candidate selection uses training labels only; held-out game identities
 * are never used to rank candidates. Deterministic synthetic evaluation.
 */
import {verifyObserverStrict,instantiateObserver,appendExperience} from "./emergent-observer.mjs";
import {BASELINE,CANDIDATES} from "./observer-discovery.mjs";
export const VERSION="QG-043.1";
const clone=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const fail=m=>{throw Error(m)};
const id=s=>typeof s==="string"&&/^[a-z][a-z0-9-]{0,31}$/.test(s);
const round=x=>Math.round(x*1e9)/1e9;
const predict=(w,f)=>round(w.reduce((s,x,i)=>s+x*f[i],0));
const mse=(w,rows)=>round(rows.reduce((s,r)=>s+(predict(w,r.features)-r.target)**2,0)/rows.length);
function evaluate(source,labels,trainingGames,transferGames,margin){
 verifyObserverStrict(source);
 if(!Array.isArray(trainingGames)||!Array.isArray(transferGames)||trainingGames.length<2||transferGames.length<2||
 trainingGames.length>16||transferGames.length>16||
 [...trainingGames,...transferGames].some(g=>!id(g))||
 new Set(trainingGames).size!==trainingGames.length||new Set(transferGames).size!==transferGames.length||
 trainingGames.some(g=>transferGames.includes(g)))fail("Training and unseen game IDs must be disjoint");
 if(!Array.isArray(labels)||labels.length!==source.events.length||source.events.length<20||
 !Number.isFinite(margin)||margin<0||margin>2)fail("Invalid evaluation configuration");
 const rows={train:[],transfer:[]};
 for(let i=0;i<source.events.length;i++){
  const e=source.events[i],l=labels[i],games=e.mode==="play"?[e.game]:e.games;
  if(!l||Object.keys(l).sort().join(",")!=="event,target"||l.event!==i||
 typeof l.target!=="number"||!Number.isFinite(l.target)||l.target<0||l.target>30)fail("Invalid outcome label");
  const isTrain=games.every(g=>trainingGames.includes(g));
  const isTransfer=games.every(g=>transferGames.includes(g));
  if(isTrain===isTransfer)fail("Mixed or unassigned game identity: information leakage");
  rows[isTrain?"train":"transfer"].push({event:i,mode:e.mode,
   features:[source.history[i].novelPatterns,source.history[i].distinctGames,e.payoff,e.cost],target:l.target});
 }
 for(const part of [rows.train,rows.transfer]){
  if(part.length<8||!["play","observe"].every(mode=>part.some(r=>r.mode===mode)))fail("Both partitions require 8 events and both modes");
 }
 const rank=CANDIDATES.map((w,index)=>({index,error:mse(w,rows.train)})).sort((a,b)=>a.error-b.error||a.index-b.index);
 const winner=rank[0],w=[...CANDIDATES[winner.index]],baselineTrain=mse(BASELINE,rows.train),
  baselineTransfer=mse(BASELINE,rows.transfer),candidateTransfer=mse(w,rows.transfer);
 const accepted=winner.error+margin<baselineTrain&&candidateTransfer+margin<baselineTransfer;
 return {trainingGames:[...trainingGames],transferGames:[...transferGames],
  trainingSamples:rows.train.length,transferSamples:rows.transfer.length,
  originalModel:[...BASELINE],candidateModel:w,candidateIndex:winner.index,
  baselineTrain,candidateTrain:winner.error,baselineTransfer,candidateTransfer,
  margin,accepted,decision:accepted?"transfer-supported":"transfer-not-supported",
  leakageDetected:false,truthProven:false};
}
function replay(source,labels,trainingGames,transferGames,margin,events){
 const s={version:VERSION,source:clone(source),labels:clone(labels),trainingGames:[...trainingGames],
 transferGames:[...transferGames],margin,events:[],result:null};
 evaluate(s.source,s.labels,s.trainingGames,s.transferGames,s.margin);
 for(let i=0;i<events.length;i++){
  const e=events[i];
  if(i!==0||!e||Object.keys(e).sort().join(",")!=="index,kind,parent"||
 e.kind!=="evaluate-transfer"||e.index!==0||e.parent!==null)fail("Invalid transfer ledger");
  s.result=evaluate(s.source,s.labels,s.trainingGames,s.transferGames,s.margin);
  s.events.push(clone(e));
 }
 return s;
}
export function instantiateTransfer(source,labels,{trainingGames,transferGames,margin=0.1}){
 return replay(source,labels,trainingGames,transferGames,margin,[]);
}
export function appendTransferEvaluation(state){
 verifyTransferStrict(state);
 if(state.events.length)fail("Already evaluated");
 return replay(state.source,state.labels,state.trainingGames,state.transferGames,state.margin,
  [{kind:"evaluate-transfer",index:0,parent:null}]);
}
export function verifyTransferStrict(state){
 if(!state||state.version!==VERSION||!Array.isArray(state.events)||state.events.length>1)fail("Invalid transfer state");
 const expected=replay(state.source,state.labels,state.trainingGames,state.transferGames,state.margin,state.events);
 if(!eq(expected,state))fail("Transfer replay differs");
 return {pass:true,decision:state.result?.decision??"undetermined",evaluated:state.result!==null};
}
export function verifyTransfer(state){try{return verifyTransferStrict(state)}catch(e){return {pass:false,error:e.message}}}
export function simulatedTransfer({scenario="generalizes"}={}){
 if(!["generalizes","fails-transfer","baseline-best"].includes(scenario))fail("Unknown demo scenario");
 const trainingGames=["arena","chess","go"],transferGames=["solstice","shogi","hex"];
 let source=instantiateObserver();
 for(let i=0;i<24;i++){
  const train=i<12,observe=i%3!==0;
  const games=train?trainingGames:transferGames;
  source=appendExperience(source,observe?
   {mode:"observe",games:[games[1],games[2]],patterns:["pattern"+i],payoff:0.4,cost:1}:
   {mode:"play",game:games[0],patterns:["pattern"+i],payoff:2,cost:0.4});
 }
 const labels=source.events.map((e,i)=>{
  const f=[source.history[i].novelPatterns,source.history[i].distinctGames,e.payoff,e.cost];
  const w=scenario==="baseline-best"||scenario==="fails-transfer"&&i>=12?BASELINE:CANDIDATES[0];
  return {event:i,target:predict(w,f)};
 });
 return instantiateTransfer(source,labels,{trainingGames,transferGames});
}
