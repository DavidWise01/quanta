/**
 * QG-036.1 — Lossless [84211] closure.
 * Eight leaf records represent (actor identifier, complete sealed actor) x4.
 * Every 2:1 fold retains BOTH child nodes, not a lossy summary.
 * The final 1->1 is an identical value-preserving closure.
 * Replay equivalence is structural, NOT cryptographic authentication.
 */
import {ACTORS,OUTER,verify84211Strict,instantiate84211,append84211,FACES} from "./byzantine-84211.mjs";
export const VERSION="QG-036.1",CARRIER="||||";
const clone=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function pack(source){
 const leaves=ACTORS.flatMap((id,i)=>[
  {kind:"identity",actor:id,value:id},
  {kind:"chamber",actor:id,value:clone(source.actors[i])}
 ]);
 const stages=[leaves];let nodes=leaves;
 for(const width of [4,2,1]){
  const parents=[];
  for(let i=0;i<nodes.length;i+=2)parents.push({kind:"pair",children:[clone(nodes[i]),clone(nodes[i+1])]});
  stages.push(parents);nodes=parents;
 }
 // The fifth station does not discard or rewrite the fourth.
 stages.push(clone(stages[3]));
 return stages;
}
function leafRecovery(node){
 if(node.kind==="pair"){
  if(!Array.isArray(node.children)||node.children.length!==2)throw Error("Corrupt pair");
  return [...leafRecovery(node.children[0]),...leafRecovery(node.children[1])];
 }
 return [node];
}
function validSource(source){
 verify84211Strict(source);
 if(!source.actors.every(a=>a.closed))throw Error("All four chambers must be closed");
 if(!source.ruling)throw Error("A completed judge ruling is required");
 for(const a of source.actors)if(a.faces.length!==6||new Set(a.faces).size!==6)throw Error("Six-face closure required");
 return source;
}
export function close84211(source){
 validSource(source);
 const canonical=clone(source),stages=pack(canonical);
 const packet={version:VERSION,carrier:CARRIER,shape:"[84211]",widths:[...OUTER],source:canonical,stages,
  ledgerEvents:clone(canonical.events),interpretationProven:false};
 verifyLossless84211Strict(packet);
 return packet;
}
export function recover84211(packet){
 verifyLossless84211Strict(packet);
 return clone(packet.source);
}
export function verifyLossless84211Strict(packet){
 if(!packet||packet.version!==VERSION||packet.carrier!==CARRIER||packet.shape!=="[84211]"||
  !equal(packet.widths,OUTER)||packet.interpretationProven!==false)throw Error("Invalid closure header");
 const source=validSource(packet.source),expected=pack(source);
 if(!equal(packet.stages,expected))throw Error("Fold differs from canonical preserved ancestry");
 if(!equal(packet.ledgerEvents,source.events))throw Error("Original event ledger not preserved");
 const recovered=leafRecovery(packet.stages[4][0]);
 if(!equal(recovered,expected[0]))throw Error("Final chamber leaves are not exactly recoverable");
 if(!equal(packet.stages[3],packet.stages[4]))throw Error("Final 1 to 1 must be unchanged");
 return {pass:true,widths:[8,4,2,1,1],actors:4,faces:24,leaves:8,
  events:source.events.length,allSealed:true,hasRuling:true,exactRecovery:true,interpretationProven:false};
}
export function verifyLossless84211(packet){
 try{return verifyLossless84211Strict(packet)}catch(e){return {pass:false,error:e.message}}
}
export function demo84211(){
 let s=instantiate84211();
 for(const id of ACTORS){
  for(const face of FACES)s=append84211(s,{kind:"face",actor:id,face});
  s=append84211(s,{kind:"seal",actor:id,statement:"Synthetic sealed report "+id,source:"Synthetic lineage "+id});
 }
 return append84211(s,{kind:"ruling",outcome:"insufficient",rationale:"No independent source authentication in demonstration"});
}
