/**
 * QUANTA QG-030.1 — Chasing Roots.
 * An auditable backwards dependency walk for QG-029 contextual claims:
 * WHICH MEANS -> REQUIRES -> ... -> leaf roots / missing evidence.
 * Exact nested social witness is retained. No inference of historical truth.
 */
import {bindSocialContext,recoverSocialContext} from "./societal-somatic.mjs";
import {bindSemanticLetter} from "./semantic-ring.mjs";
export const ROOT_VERSION="QG-030.1",ROOT_CARRIER="||||";
export const MAX_NODES=60,MAX_EDGES=180;
const freeze=Object.freeze;
const ID=/^[a-z][a-z0-9-]{0,63}$/;
const STATUSES=freeze(["sourced","annotated","hypothesis","unknown","disputed"]);
const own=Object.hasOwn;
const exact=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function fingerprint(value){
 // FNV-1a over JSON UTF-16 code units: deterministic error-detection only.
 let h=14695981039346656037n;
 for(const ch of JSON.stringify(value)){
  h^=BigInt(ch.charCodeAt(0));
  h=(h*1099511628211n)&((1n<<64n)-1n);
 }
 return h.toString(16).padStart(16,"0");
}
function plain(v,fields,label){
 if(!v||typeof v!=="object"||Array.isArray(v)||Object.keys(v).some(k=>!fields.includes(k)))throw new TypeError("Invalid "+label+" fields");
}
function nonempty(s,label,max=600){
 if(typeof s!=="string"||!s.trim()||s.length>max||/[\u0000-\u001f]/.test(s))throw new TypeError("Invalid "+label);
 return s;
}
function ident(v,label){if(typeof v!=="string"||!ID.test(v))throw new TypeError("Invalid "+label+" ID");return v}
function evidence(list){
 if(!Array.isArray(list)||list.length>12)throw new TypeError("Evidence must be an array of at most 12 URLs");
 return freeze(list.map(x=>{
  plain(x,["label","url"],"evidence");
  const label=nonempty(x.label,"evidence label",160),url=nonempty(x.url,"evidence URL",1000);
  if(!/^https:\/\/[^\s]+$/i.test(url))throw new TypeError("Evidence requires HTTPS");
  return freeze({label,url});
 }));
}
function normalize(input){
 plain(input,["society","target","nodes"],"root graph");
 const society=input.society?.version==="QG-029.1"?input.society:bindSocialContext(input.society);
 const claim=recoverSocialContext(society);
 const target=ident(input.target,"target");
 if(!Array.isArray(input.nodes)||input.nodes.length<1||input.nodes.length>MAX_NODES)throw new TypeError("Expected 1–60 root nodes");
 const ids=new Set(),nodes=input.nodes.map((n,i)=>{
  plain(n,["id","statement","role","status","year","requires","evidence"],"node");
  const id=ident(n.id,"node");if(ids.has(id))throw new Error("Duplicate node ID "+id);ids.add(id);
  const role=n.role??"prerequisite";if(!["conclusion","prerequisite"].includes(role))throw new TypeError("Invalid node role");
  if(typeof n.year!=="number"||!Number.isInteger(n.year)||n.year<1||n.year>claim.context.year)throw new TypeError("Node year must be 1..contextual year");
  if(!STATUSES.includes(n.status))throw new TypeError("Invalid knowledge status");
  if(!Array.isArray(n.requires)||n.requires.length>MAX_NODES)throw new TypeError("Invalid prerequisites");
  const req=n.requires.map(v=>ident(v,"required node"));
  if(new Set(req).size!==req.length)throw new Error("Duplicate prerequisite");
  const ev=evidence(n.evidence??[]);
  if(n.status==="sourced"&&!ev.length)throw new Error("Sourced node requires explicit evidence");
  return freeze({id,statement:nonempty(n.statement,"statement",1000),role,status:n.status,year:n.year,
    requires:freeze(req),evidence:ev});
 });
 if(!ids.has(target))throw new Error("Missing target node");
 const index=new Map(nodes.map(n=>[n.id,n]));
 if(index.get(target).role!=="conclusion"||index.get(target).statement!==claim.whichMeans)
  throw new Error("Target must be a conclusion matching WHICH MEANS exactly");
 let edgeCount=0;
 for(const n of nodes)for(const id of n.requires){
  edgeCount++;if(edgeCount>MAX_EDGES)throw new RangeError("Too many edges");
  const child=index.get(id);
  if(!child)throw new Error("Unresolved prerequisite reference "+id);
  if(child.year>n.year)throw new Error("Dependency cannot postdate its parent claim");
 }
 const visit=new Set(),done=new Set();
 function dfs(id){
  if(visit.has(id))throw new Error("Dependency cycle at "+id);
  if(done.has(id))return;
  visit.add(id);
  for(const next of index.get(id).requires)dfs(next);
  visit.delete(id);done.add(id);
 }
 for(const n of nodes)dfs(n.id);
 return {society,claim,target,nodes:freeze(nodes),index,edgeCount};
}
function chase(normal){
 const {target,index}=normal,seen=new Set(),order=[],gaps=[],roots=[];
 function walk(id,depth){
  if(seen.has(id))return;seen.add(id);
  const node=index.get(id);
  order.push(freeze({id,depth,role:node.role,status:node.status,year:node.year,statement:node.statement}));
  if(node.requires.length===0){
   roots.push(id);
   if(node.status!=="sourced")gaps.push(freeze({id,reason:"Leaf lacks supplied cited source",status:node.status}));
  }else{
   if(node.status==="disputed"||node.status==="unknown")
    gaps.push(freeze({id,reason:"Dependent statement is disputed/unknown",status:node.status}));
   for(const child of node.requires)walk(child,depth+1);
  }
 }
 walk(target,0);
 return freeze({order:freeze(order),roots:freeze(roots),gaps:freeze(gaps),
  reachable:seen.size,unlinked:freeze(normal.nodes.filter(n=>!seen.has(n.id)).map(n=>n.id))});
}
export function composeRootChase(input){
 const n=normalize(input),trace=chase(n);
 const ring=bindSemanticLetter(n.claim.letter,0);
 const phases=freeze(["is","was","whichMeans"].map((role,i)=>freeze({
   role,station:ring.roles[i].station,quad:ring.roles[i].glyph.phase.quad
 })));
 const core={version:ROOT_VERSION,carrier:ROOT_CARRIER,
  society:n.society,target:n.target,nodes:n.nodes,phases,trace};
 return freeze({...core,fingerprint:fingerprint(core)});
}
export function recoverRootChase(packet){
 if(!packet||packet.version!==ROOT_VERSION||packet.carrier!==ROOT_CARRIER)throw new TypeError("Unknown root packet");
 const expected=composeRootChase({society:packet.society,target:packet.target,nodes:packet.nodes});
 if(!exact(packet,expected))throw new Error("Root dependency, phase or evidence witness mismatch");
 return freeze({claim:recoverSocialContext(packet.society),trace:packet.trace,nodes:packet.nodes});
}
export function verifyRootChase(packet){
 try{
  const r=recoverRootChase(packet);
  return freeze({pass:true,subject:r.claim.subject,roots:r.trace.roots.length,
   gaps:r.trace.gaps.length,reached:r.trace.reachable,unlinked:r.trace.unlinked.length,
   interpretationProven:false});
 }catch(e){return freeze({pass:false,error:e.message})}
}
