// QG-073: provenance survives transformations.
// Root classifications originate in a separately pinned source registry.
// A derived node's ancestry and confidentiality are computed, never accepted
// from its proposed output text. This is a synthetic information-flow model.
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
import {authorizeAction as checkScope} from './hive-scoped-authority.mjs';
export const VERSION='QG-073';
export const OPERATIONS=Object.freeze(['summarize','translate','combine','extract']);
const SURFACES=['github','0root.ai','public-internet'];
const cp=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>canonical(a)===canonical(b);
const goodId=x=>typeof x==='string'&&/^[a-zA-Z0-9._-]{1,80}$/.test(x);
function validateRegistry(reg){
 if(!Array.isArray(reg)||reg.length<1||reg.length>32)throw Error('Pinned source registry required');
 const seen=new Set();
 for(const x of reg){
  if(!x||!goodId(x.id)||seen.has(x.id)||!SURFACES.includes(x.surface)||
    !['public','gated'].includes(x.classification)||
    x.classification==='gated'&&x.surface!=='github'||
    !Array.isArray(x.ancestors)||!x.ancestors.length||
    x.ancestors.some(a=>!goodId(a))||typeof x.digest!=='string'||!/^[a-f0-9]{64}$/.test(x.digest))
   throw Error('Invalid or duplicated pinned source');
  seen.add(x.id);
 }
}
function inherited(parents){
 const roots=[...new Set(parents.flatMap(p=>p.ancestors))].sort();
 const origins=[...new Set(parents.flatMap(p=>p.origins))].sort();
 const classification=parents.some(p=>p.classification==='gated')?'gated':'public';
 return {classification,ancestors:roots,origins};
}
async function replay(events,registry){
 const nodes=new Map(),audit=[];
 for(let i=0;i<events.length;i++){
  const e=events[i];
  if(!e||!goodId(e.id)||nodes.has(e.id)||typeof e.text!=='string'||e.text.length>2000)
   throw Error('Invalid or duplicate evidence node');
  let node;
  if(e.kind==='source'){
   const pin=registry.find(x=>x.id===e.id);
   if(!pin||await sha256(e.text)!==pin.digest)throw Error('Unpinned or tampered source');
   if(e.parents!==undefined||e.operation!==undefined)throw Error('Source cannot claim derivation');
   node={id:e.id,kind:'source',digest:pin.digest,
    classification:pin.classification,ancestors:[...new Set(pin.ancestors)].sort(),origins:[pin.surface],
    parents:[],operation:null};
  }else if(e.kind==='derived'){
   if(!OPERATIONS.includes(e.operation)||!Array.isArray(e.parents)||
    !e.parents.length||e.parents.length>16||new Set(e.parents).size!==e.parents.length)
    throw Error('Invalid transformation parents');
   const parentNodes=e.parents.map(p=>nodes.get(p));
   if(parentNodes.some(p=>!p))throw Error('Unknown, forward or missing parent');
   const labels=inherited(parentNodes);
   node={id:e.id,kind:'derived',digest:await sha256(e.text),
    ...labels,parents:cp(e.parents),operation:e.operation};
  }else throw Error('Unrecognized evidence kind');
  nodes.set(e.id,node);audit.push(node);
 }
 return audit;
}
export async function start(registry,pinnedRegistryDigest){
 validateRegistry(registry);
 const digest=await sha256(canonical(registry));
 if(digest!==pinnedRegistryDigest)throw Error('Independent registry digest mismatch');
 return {version:VERSION,registry:cp(registry),registryDigest:digest,events:[],nodes:[]};
}
export async function verify(record,independentDigest){
 if(!record||record.version!==VERSION||!Array.isArray(record.events)||
 !Array.isArray(record.nodes))throw Error('Invalid provenance ledger');
 validateRegistry(record.registry);
 if(record.registryDigest!==independentDigest||
 await sha256(canonical(record.registry))!==independentDigest)
 throw Error('Independent source registry mismatch');
 const nodes=await replay(record.events,record.registry);
 if(!eq(nodes,record.nodes))throw Error('Derived provenance replay mismatch');
 return {valid:true,nodes:cp(nodes),count:nodes.length,gated:nodes.filter(n=>n.classification==='gated').length};
}
export async function appendSource(record,id,text,independentDigest){
 await verify(record,independentDigest);
 const event={kind:'source',id,text};
 const next={...cp(record),events:[...cp(record.events),event]};
 next.nodes=await replay(next.events,next.registry);
 await verify(next,independentDigest);return next;
}
export async function derive(record,{id,operation,parents,text},independentDigest){
 await verify(record,independentDigest);
 const event={kind:'derived',id,operation,parents:cp(parents),text};
 const next={...cp(record),events:[...cp(record.events),event]};
 next.nodes=await replay(next.events,next.registry);
 await verify(next,independentDigest);return next;
}
export async function inspect(record,id,digest){
 await verify(record,digest);
 const node=record.nodes.find(n=>n.id===id);
 if(!node)throw Error('Evidence node missing');
 return cp(node);
}
export async function authorizeTransfer(record,id,scopeRecord,trust,clock,destination,action,digest){
 const node=await inspect(record,id,digest);
 if(!SURFACES.includes(destination))throw Error('Unknown destination');
 if(node.classification==='gated'&&destination!=='github')
 throw Error('Derived gated provenance cannot cross public boundary');
 // QG-072 must never trust a caller-supplied data label.
 const request={action,surface:destination,
   originSurface:node.classification==='gated'?'github':node.origins[0],
   classification:node.classification};
 const receipt=await checkScope(scopeRecord,request,trust,clock);
 return {allowed:true,nodeId:id,ancestors:cp(node.ancestors),origins:cp(node.origins),
  classification:node.classification,receipt};
}
export async function fixture(kind='mixed'){
 const refs=[
  {id:'g',surface:'github',classification:'gated',ancestors:['owned-corpus'],text:'private notebook'},
  {id:'w',surface:'0root.ai',classification:'public',ancestors:['owned-corpus'],text:'public article'},
  {id:'e',surface:'public-internet',classification:'public',ancestors:['external-origin'],text:'third-party report'}
 ];
 const registry=await Promise.all(refs.map(async({text,...r})=>({...r,digest:await sha256(text)})));
 const digest=await sha256(canonical(registry));
 let record=await start(registry,digest);
 for(const r of refs)record=await appendSource(record,r.id,r.text,digest);
 if(kind==='sources')return {record,registry,digest};
 const parents=kind==='public'?['w','e']:kind==='gated'?['g']:['g','w','e'];
 record=await derive(record,{id:'out',operation:kind==='gated'?'translate':kind==='public'?'summarize':'combine',
 parents,text:'newly phrased synthetic output'},digest);
 return {record,registry,digest};
}
