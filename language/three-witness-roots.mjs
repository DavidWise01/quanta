/**
 * QUANTA QG-033.1 — Three-Witness Root Consensus.
 * One verified QG-030 / latest QG-031 leaf root, exactly 3 declared witnesses,
 * 3 distinct cited source hosts, and 3 QG-028 quarter-turn phase slots.
 *
 * Consensus here = observed alignment of statements, NOT historical truth.
 * Sources/independence are declared and structurally checked, not authenticated.
 * Append-only events preserve each witness and reviewer determination.
 */
import {composeRootChase,recoverRootChase} from "./chasing-roots.mjs";
import {verifyRootPropagation} from "./root-propagation.mjs";
import {bindSemanticLetter} from "./semantic-ring.mjs";

export const VERSION="QG-033.1",CARRIER="||||",LIMIT=32;
const freeze=Object.freeze;
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const ID=/^[a-z][a-z0-9-]{0,63}$/;
function field(s,name,max=900){if(typeof s!=="string"||!s.trim()||s.length>max||/[\u0000-\u001f]/.test(s))throw new TypeError("Invalid "+name);return s}
function id(s,name){if(typeof s!=="string"||!ID.test(s))throw new TypeError("Invalid "+name);return s}
function shape(o,keys,name){if(!o||typeof o!=="object"||Array.isArray(o)||Object.keys(o).some(k=>!keys.includes(k)))throw new TypeError("Invalid "+name)}
function evidence(e){
 shape(e,["label","url","host"],"source evidence");
 const label=field(e.label,"source label",200),url=field(e.url,"source HTTPS URL",1000);
 let host;try{const u=new URL(url);if(u.protocol!=="https:"||u.username||u.password)throw Error();host=u.hostname.toLowerCase()}catch{throw new TypeError("Evidence needs a valid HTTPS URL")}
 if(Object.hasOwn(e,"host")&&e.host!==host)throw new Error("Source host and HTTPS URL mismatch");
 return freeze({label,url,host});
}
function rooted(source){
 let root=source;
 if(root?.version==="QG-031.1"){
  const report=verifyRootPropagation(root);
  if(!report.pass)throw new Error("Invalid propagation history: "+report.error);
  root=root.revisions.at(-1).snapshot;
 }else if(root?.version!=="QG-030.1")root=composeRootChase(root);
 recoverRootChase(root);return root;
}
function witness(input,root){
 shape(input,["id","root","position","statement","year","source","independence"],"witness");
 const wid=id(input.id,"witness ID"),rootId=id(input.root,"root ID");
 if(rootId!==root.id)throw new Error("Witness points to another root");
 if(!["supports","challenges","undetermined"].includes(input.position))
  throw new TypeError("Invalid witness position");
 if(!Number.isInteger(input.year)||input.year<root.year||input.year>root.contextYear)
  throw new RangeError("Witness year outside root's contextual interval");
 const source=evidence(input.source);
 return freeze({id:wid,root:rootId,position:input.position,statement:field(input.statement,"statement"),
  year:input.year,source,independence:field(input.independence,"independence declaration",600)});
}
function affected(packet,rootId){
 const rev=new Map(packet.nodes.map(n=>[n.id,[]]));
 for(const n of packet.nodes)for(const child of n.requires)rev.get(child).push(n.id);
 const seen=new Set(),q=[rootId];for(let i=0;i<q.length;i++){
  const node=q[i];if(seen.has(node))continue;seen.add(node);
  for(const parent of rev.get(node))if(!seen.has(parent))q.push(parent);
 }
 return freeze(packet.nodes.filter(n=>seen.has(n.id)).map(n=>n.id));
}
function evaluate(witnesses){
 const votes={supports:0,challenges:0,undetermined:0};
 for(const w of witnesses)votes[w.position]++;
 const result=votes.undetermined?"incomplete":
   votes.supports===3?"unanimous-support":
   votes.challenges===3?"unanimous-challenge":"split";
 return freeze({classification:result,counts:freeze(votes),
   majority:votes.supports>votes.challenges?"supports":votes.challenges>votes.supports?"challenges":"none",
   interpretationProven:false});
}
function trio(packet,rootId,inputs,index){
 const rid=id(rootId,"root ID");
 const r=packet.nodes.find(n=>n.id===rid);
 if(!r||r.requires.length!==0)throw new Error("Witnesses must point at a leaf root");
 if(!Array.isArray(inputs)||inputs.length!==3)throw new TypeError("Exactly three witnesses required");
 const ws=inputs.map(x=>witness(x,{...r,contextYear:packet.society.claim.context.year}));
 if(new Set(ws.map(x=>x.id)).size!==3)throw new Error("Witness IDs must differ");
 if(new Set(ws.map(x=>x.source.host)).size!==3)
  throw new Error("Witnesses must cite three different declared source hosts");
 const phase=bindSemanticLetter(packet.society.claim.letter,0);
 const slots=freeze(ws.map((w,i)=>freeze({
  witness:w.id,ringStation:phase.roles[i].station,quad:phase.roles[i].glyph.phase.quad,
  phaseDegrees:phase.roles[i].degrees
 })));
 return freeze({id:"t"+String(index).padStart(4,"0"),root:rid,
  witnesses:freeze(ws),slots,assessment:evaluate(ws),affected:affected(packet,rid),
  review:null,state:"open"});
}
function decide(input,trio){
 shape(input,["id","outcome","rationale","source"],"review");
 if(input.id!==trio.id)throw new Error("Review must name exact trio");
 if(!["support","challenge","insufficient"].includes(input.outcome))throw new TypeError("Invalid outcome");
 return freeze({id:trio.id,outcome:input.outcome,rationale:field(input.rationale,"rationale"),
  source:evidence(input.source)});
}
export function instantiateThreeWitness(source){
 return freeze({version:VERSION,carrier:CARRIER,rootPacket:rooted(source),
  trios:freeze([]),events:freeze([])});
}
function rebuild(ledger){
 if(!ledger||ledger.version!==VERSION||ledger.carrier!==CARRIER||
  !Array.isArray(ledger.trios)||!Array.isArray(ledger.events)||
  ledger.trios.length>LIMIT||ledger.events.length>LIMIT*2)
  throw new TypeError("Invalid three-witness ledger");
 recoverRootChase(ledger.rootPacket);
 const canonical=[];let last=null;
 for(let i=0;i<ledger.events.length;i++){
  const e=ledger.events[i];
  if(!e||e.index!==i||e.parent!==last||!["trio","review"].includes(e.kind))
   throw new Error("Broken append-only event chain");
  if(e.kind==="trio"){
   if(canonical.length>=LIMIT)throw new RangeError("Trio limit");
   const expected=trio(ledger.rootPacket,e.root,e.witnesses,canonical.length);
   if(!eq(expected,e.record))throw new Error("Trio witness changed");
   canonical.push(expected);
  }else{
   const j=canonical.findIndex(t=>t.id===e.id);
   if(j<0||canonical[j].state!=="open")throw new Error("Invalid review target");
   const review=decide(e.review,canonical[j]);
   if(!eq(review,e.review))throw new Error("Review witness changed");
   canonical[j]=freeze({...canonical[j],state:"reviewed",review});
  }
  last="e"+String(i).padStart(4,"0");
 }
 if(!eq(canonical,ledger.trios))throw new Error("Trio state differs from event replay");
}
function append(ledger,event,trios){
 return freeze({version:VERSION,carrier:CARRIER,rootPacket:ledger.rootPacket,
  trios:freeze(trios),events:freeze([...ledger.events,freeze(event)])});
}
export function observeThreeWitnesses(ledger,rootId,witnesses){
 rebuild(ledger);
 if(ledger.trios.length>=LIMIT)throw new RangeError("Trio limit");
 const t=trio(ledger.rootPacket,rootId,witnesses,ledger.trios.length),i=ledger.events.length;
 return append(ledger,{kind:"trio",index:i,parent:i?"e"+String(i-1).padStart(4,"0"):null,
  root:rootId,witnesses:t.witnesses,record:t},[...ledger.trios,t]);
}
export function reviewThreeWitnesses(ledger,trioId,outcome,rationale,source){
 rebuild(ledger);
 const at=ledger.trios.findIndex(x=>x.id===trioId);
 if(at<0||ledger.trios[at].state!=="open")throw new Error("Review requires an open trio");
 const review=decide({id:trioId,outcome,rationale,source},ledger.trios[at]),i=ledger.events.length;
 const next=[...ledger.trios];next[at]=freeze({...next[at],state:"reviewed",review});
 return append(ledger,{kind:"review",index:i,parent:i?"e"+String(i-1).padStart(4,"0"):null,
  id:trioId,review},next);
}
export function inspectThreeWitnesses(ledger){
 rebuild(ledger);
 return freeze({trios:ledger.trios.length,
  open:ledger.trios.filter(t=>t.state==="open").length,
  reviewed:ledger.trios.filter(t=>t.state==="reviewed").length,
  classifications:freeze(ledger.trios.map(t=>freeze({id:t.id,class:t.assessment.classification,
    majority:t.assessment.majority,affected:t.affected}))),
  interpretationProven:false});
}
export function verifyThreeWitnesses(ledger){
 try{return freeze({pass:true,...inspectThreeWitnesses(ledger)})}
 catch(e){return freeze({pass:false,error:e.message})}
}
