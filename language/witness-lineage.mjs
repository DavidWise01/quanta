/**
 * QG-034.1 Witness Lineage. Declared attribution graph, not authenticated provenance.
 * A derived report cannot promote QG-033 votes into independently supported facts.
 */
import {verifyThreeWitnesses} from "./three-witness-roots.mjs";
export const VERSION="QG-034.1",CARRIER="||||",MAX_NODES=96,MAX_EVENTS=64;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const validId=x=>typeof x==="string"&&/^[a-z][a-z0-9-]{0,63}$/.test(x);
function requireId(x){if(!validId(x))throw Error("Invalid ancestry ID");return x}
function str(x){if(typeof x!=="string"||!x.trim()||x.length>1000||/[\x00-\x1f]/.test(x))throw Error("Invalid provenance text");return x}
function url(x){str(x);let u;try{u=new URL(x)}catch{throw Error("Invalid HTTPS URL")};if(u.protocol!=="https:"||u.username||u.password)throw Error("Invalid HTTPS URL");return x}
function canonicalNodes(nodes,ids){
 if(!Array.isArray(nodes)||nodes.length<3||nodes.length>MAX_NODES)throw Error("Lineage node bound");
 const out=nodes.map(n=>{
  if(!n||Object.keys(n).some(k=>!["id","kind","parents","label","url"].includes(k)))throw Error("Unknown node fields");
  const id=requireId(n.id),kind=n.kind;
  if(!["witness","record","origin"].includes(kind))throw Error("Invalid node kind");
  if(!Array.isArray(n.parents)||n.parents.length>MAX_NODES||new Set(n.parents).size!==n.parents.length||n.parents.some(p=>!validId(p)))throw Error("Invalid parent edges");
  if(kind==="origin"&&n.parents.length)throw Error("Origin cannot have parents");
  if(kind!=="origin"&&!n.parents.length)throw Error("Non-origin must cite ancestry");
  return {id,kind,parents:[...n.parents].sort(),label:str(n.label),url:url(n.url)};
 });
 const map=new Map(out.map(n=>[n.id,n]));if(map.size!==out.length)throw Error("Duplicate ancestry node");
 for(const n of out)for(const p of n.parents)if(!map.has(p)||p===n.id)throw Error("Missing or self-referential ancestry");
 if(out.filter(n=>n.kind==="witness").length!==3)throw Error("Exactly three witness nodes required");
 for(const id of ids)if(map.get(id)?.kind!=="witness")throw Error("Witness ID must match QG-033");
 if(out.some(n=>n.kind==="witness"&&!ids.includes(n.id)))throw Error("Unexpected witness node");
 const state=new Map();
 function visit(id){if(state.get(id)===1)throw Error("Ancestry cycle");if(state.get(id)===2)return;state.set(id,1);for(const p of map.get(id).parents)visit(p);state.set(id,2)}
 for(const n of out)visit(n.id);
 return out.sort((a,b)=>a.id.localeCompare(b.id));
}
function analysis(nodes,ids){
 const map=new Map(nodes.map(n=>[n.id,n])),memo=new Map();
 function roots(id){if(memo.has(id))return memo.get(id);const n=map.get(id);const r=n.kind==="origin"?[id]:[...new Set(n.parents.flatMap(roots))].sort();memo.set(id,r);return r}
 const paths=ids.map(id=>({witness:id,origins:roots(id)}));
 const union=[...new Set(paths.flatMap(p=>p.origins))].sort();
 // An origin that supports multiple witness reports is one source, not multiple independent votes.
 const overlap=[];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const shared=paths[i].origins.filter(x=>paths[j].origins.includes(x));if(shared.length)overlap.push({pair:[ids[i],ids[j]],origins:shared})}
 // Connected components in the witness-origin bipartite graph: conservative independent lineages.
 const seen=new Set(),groups=[];
 for(let i=0;i<3;i++){if(seen.has(ids[i]))continue;const component=new Set([ids[i]]);let change=true;while(change){change=false;for(const p of paths){if(!component.has(p.witness)&&p.origins.some(r=>paths.some(q=>component.has(q.witness)&&q.origins.includes(r)))){component.add(p.witness);change=true}}}component.forEach(x=>seen.add(x));groups.push([...component].sort())}
 const insufficient=paths.some(p=>p.origins.length===0);
 return {paths,sharedOrigins:overlap,uniqueOrigins:union,independentLineages:groups.length,lineages:groups,threeIndependent:!insufficient&&groups.length===3,interpretationProven:false};
}
function rebuild(x){
 if(!x||x.version!==VERSION||x.carrier!==CARRIER||!Array.isArray(x.events)||x.events.length>MAX_EVENTS)throw Error("Invalid lineage ledger");
 if(!verifyThreeWitnesses(x.source).pass)throw Error("Source QG-033 ledger invalid");
 const trio=x.source.trios.find(t=>t.id===x.trioId);
 if(!trio)throw Error("QG-033 trio not found");
 const ids=trio.witnesses.map(w=>w.id);let nodes=null,report=null,parent=null;
 for(let i=0;i<x.events.length;i++){
  const e=x.events[i];if(e.index!==i||e.parent!==parent||!["trace","review"].includes(e.kind))throw Error("Broken event chain");
  if(e.kind==="trace"){if(nodes)throw Error("Trace cannot replace original");nodes=canonicalNodes(e.nodes,ids);
   for(const w of trio.witnesses){const n=nodes.find(n=>n.id===w.id);if(n.url!==w.source.url)throw Error("Witness source URL differs from QG-033")}
   report=analysis(nodes,ids);if(!same(report,e.report))throw Error("Altered ancestry result");
  }else{if(!nodes||e.verdict!=="review-required"||!e.rationale||typeof e.rationale!=="string"||!e.rationale.trim())throw Error("Invalid lineage review");str(e.rationale)}
  parent="e"+String(i).padStart(4,"0");
 }
 if(!same(nodes,x.nodes)||!same(report,x.report))throw Error("Snapshot differs from lineage replay");
 return {trio,nodes,report};
}
export function instantiateWitnessLineage(source,trioId="t0000"){
 if(!verifyThreeWitnesses(source).pass||!source.trios.some(t=>t.id===trioId))throw Error("Verified QG-033 trio required");
 return {version:VERSION,carrier:CARRIER,source:JSON.parse(JSON.stringify(source)),trioId,nodes:null,report:null,events:[]};
}
export function traceWitnessLineage(ledger,nodes){
 const old=rebuild(ledger);if(old.nodes)throw Error("Ancestry already traced; preserve original");
 const canonical=canonicalNodes(nodes,old.trio.witnesses.map(w=>w.id));
 for(const w of old.trio.witnesses)if(canonical.find(n=>n.id===w.id).url!==w.source.url)throw Error("Witness source mismatch");
 const report=analysis(canonical,old.trio.witnesses.map(w=>w.id)),i=ledger.events.length;
 return {...ledger,nodes:canonical,report,events:[...ledger.events,{kind:"trace",index:i,parent:i?"e"+String(i-1).padStart(4,"0"):null,nodes:canonical,report}]};
}
export function reviewWitnessLineage(ledger,rationale){
 const {nodes}=rebuild(ledger);if(!nodes)throw Error("Trace required");str(rationale);
 const i=ledger.events.length;if(i>=MAX_EVENTS)throw Error("Event bound");
 return {...ledger,events:[...ledger.events,{kind:"review",index:i,parent:i?"e"+String(i-1).padStart(4,"0"):null,verdict:"review-required",rationale}]};
}
export function inspectWitnessLineage(ledger){return rebuild(ledger).report}
export function verifyWitnessLineage(ledger){try{const r=rebuild(ledger);return {pass:true,report:r.report}}catch(e){return {pass:false,error:e.message}}}
