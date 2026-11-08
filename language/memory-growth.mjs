/**
 * QUANTA QG-024.1 — Convergent Memory Growth (append-only ancestry DAG).
 * Each node stores an exact QG-020 canonical source snapshot and 0/1/2 parents.
 * A two-parent convergence uses the QG-023 explicit three-way paragraph merge.
 *
 * Node IDs are local sequence addresses, NOT globally unique hashes.
 * This is geometry/source provenance, not cryptography or autonomous memory.
 */
import {composeCorpusBox,recoverCorpusBox} from "./corpus-box.mjs";
import {instantiateCorpusMemory,appendCorpusRevision} from "./corpus-memory.mjs";
import {convergeCorpusMemory} from "./memory-convergence.mjs";

export const GROWTH_VERSION="QG-024.1";
export const GROWTH_CARRIER="||||";
export const GROWTH_LIMIT=32;
const freeze=Object.freeze;
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const copy=x=>JSON.parse(JSON.stringify(x));
const nodeId=i=>"n"+String(i).padStart(4,"0");
function canonical(source){const p=composeCorpusBox(source);recoverCorpusBox(p);return p;}
function ensureGraph(graph){
 if(!graph||graph.version!==GROWTH_VERSION||graph.carrier!==GROWTH_CARRIER||
    !Array.isArray(graph.nodes)||graph.nodes.length<1||graph.nodes.length>GROWTH_LIMIT)
  throw new TypeError("Invalid QG-024 ancestry graph");
}
function ancestors(nodes,id){
 const map=new Map(nodes.map(n=>[n.id,n]));if(!map.has(id))throw new RangeError("Unknown graph node "+id);
 const seen=new Set(),todo=[id];
 while(todo.length){
  const next=todo.pop();
  if(seen.has(next))continue;
  const n=map.get(next);
  if(!n)throw new Error("Dangling graph parent "+next);
  seen.add(next);todo.push(...n.parents);
 }
 return seen;
}
function commonAncestor(nodes,left,right){
 const ls=ancestors(nodes,left),rs=ancestors(nodes,right);
 // In an append-only topological graph the highest common creation index
 // is a deterministic common ancestor, not necessarily a unique graph-theoretic LCA.
 for(let i=nodes.length-1;i>=0;i--)if(ls.has(nodes[i].id)&&rs.has(nodes[i].id))return nodes[i].id;
 throw new Error("No common ancestor");
}
function synthMerge(sourceBase,sourceLeft,sourceRight,resolutions){
 const root=instantiateCorpusMemory(sourceBase,"QG-024 common ancestor");
 const left=appendCorpusRevision(root,sourceLeft,{comment:"QG-024 left head"});
 const right=appendCorpusRevision(root,sourceRight,{comment:"QG-024 right head"});
 return convergeCorpusMemory(left,right,resolutions);
}
function makeNode(index,kind,parents,source,comment,base=null,resolutions={}){
 if(typeof comment!=="string"||comment.length>256)throw new TypeError("Note must be <=256 characters");
 return freeze({id:nodeId(index),index,kind,parents:freeze([...parents]),
   base,comment,resolutions:freeze(copy(resolutions)),snapshot:canonical(source)});
}
export function instantiateGrowth(source,comment="Root"){
 const root=makeNode(0,"root",[],source,comment);
 return freeze({version:GROWTH_VERSION,carrier:GROWTH_CARRIER,nodes:freeze([root])});
}
function replay(graph){
 ensureGraph(graph);
 const preceding=[];
 for(let i=0;i<graph.nodes.length;i++){
  const n=graph.nodes[i];
  if(!n||n.index!==i||n.id!==nodeId(i)||!Array.isArray(n.parents)||
     typeof n.comment!=="string"||n.comment.length>256)
   throw new Error("Broken ancestry node address");
  const expected=canonical(recoverCorpusBox(n.snapshot));
  if(!eq(expected,n.snapshot))throw new Error("Noncanonical ancestry snapshot "+n.id);
  if(i===0){
   if(n.kind!=="root"||n.parents.length!==0||n.base!==null||
      !eq(n.resolutions,{}))throw new Error("Invalid origin node");
  }else if(n.kind==="branch"){
   if(n.parents.length!==1||!preceding.some(p=>p.id===n.parents[0])||
      n.base!==null||!eq(n.resolutions,{}))throw new Error("Invalid branch parent");
  }else if(n.kind==="convergence"){
   if(n.parents.length!==2||n.parents[0]===n.parents[1]||
     !n.parents.every(id=>preceding.some(p=>p.id===id)))
    throw new Error("Invalid convergence parents");
   const base=commonAncestor(preceding,n.parents[0],n.parents[1]);
   if(n.base!==base)throw new Error("Common ancestor witness mismatch");
   const get=id=>recoverCorpusBox(preceding.find(p=>p.id===id).snapshot);
   const merged=synthMerge(get(base),get(n.parents[0]),get(n.parents[1]),n.resolutions);
   if(!eq(merged.merged,n.snapshot))throw new Error("Convergence result differs from two parents");
  }else throw new Error("Unknown graph node kind");
  preceding.push(n);
 }
 return true;
}
function append(graph,node){
 if(graph.nodes.length>=GROWTH_LIMIT)throw new RangeError("Graph node limit reached");
 return freeze({version:GROWTH_VERSION,carrier:GROWTH_CARRIER,
  nodes:freeze([...graph.nodes,node])});
}
export function growCorpusBranch(graph,parentId,source,comment="Branch growth"){
 replay(graph);
 if(!graph.nodes.some(n=>n.id===parentId))throw new RangeError("Unknown parent node");
 return append(graph,makeNode(graph.nodes.length,"branch",[parentId],source,comment));
}
export function convergeGrowthBranches(graph,leftId,rightId,resolutions={},comment="Converged growth"){
 replay(graph);
 if(leftId===rightId)throw new Error("Two distinct parents required");
 const get=id=>{const n=graph.nodes.find(x=>x.id===id);if(!n)throw new RangeError("Unknown convergence parent "+id);return recoverCorpusBox(n.snapshot)};
 const baseId=commonAncestor(graph.nodes,leftId,rightId);
 const result=synthMerge(get(baseId),get(leftId),get(rightId),resolutions);
 return append(graph,makeNode(graph.nodes.length,"convergence",[leftId,rightId],
   recoverCorpusBox(result.merged),comment,baseId,resolutions));
}
export function recoverGrowthNode(graph,id){
 replay(graph);
 const node=graph.nodes.find(n=>n.id===id);
 if(!node)throw new RangeError("Unknown node");
 return recoverCorpusBox(node.snapshot);
}
export function traceGrowthAncestors(graph,id){
 replay(graph);
 const ids=ancestors(graph.nodes,id);
 return freeze(graph.nodes.filter(n=>ids.has(n.id)).reverse().map(n=>freeze({
   id:n.id,kind:n.kind,parents:n.parents,base:n.base,comment:n.comment
 })));
}
export function inspectGrowthGraph(graph){
 replay(graph);
 return freeze({nodes:graph.nodes.length,
  branches:graph.nodes.filter(n=>n.kind==="branch").length,
  convergences:graph.nodes.filter(n=>n.kind==="convergence").length,
  edges:graph.nodes.reduce((n,x)=>n+x.parents.length,0),
  heads:freeze(graph.nodes.filter(n=>!graph.nodes.some(x=>x.parents.includes(n.id))).map(n=>n.id))});
}
export function verifyGrowthGraph(graph){
 try{return freeze({pass:true,...inspectGrowthGraph(graph)})}
 catch(e){return freeze({pass:false,error:e.message})}
}
