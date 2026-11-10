// QG-047: explicit combinatorial vertex contraction at first contact.
// Retains complete source graph, provenance of every merged/dropped edge, and
// independently reconstructable successor. Graph topology, not physical phase.
import {sample} from './first-broken-edge.mjs';
import {inspectWheel} from './center-pinch.mjs';
const copy=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export const SHAPES=[3,4,5,8,13];
const pair=(a,b)=>[a,b].sort().join(':');
export function sourceGraph(n,lobes=1){
 const at=sample(n,lobes,1);
 const hits=at.collided;
 if(hits.length!==1 || hits[0]!==0)throw Error('Multiple simultaneous contacts: single-edge surgery prohibited');
 const vertices=[{id:'C',position:{...at.wheel.center}},...at.wheel.ring.map((p,i)=>({id:'R'+i,position:{...p}}))];
 const edges=[];
 for(let i=0;i<n;i++)edges.push({id:'rim:'+i,a:'R'+i,b:'R'+((i+1)%n)});
 for(let i=0;i<n;i++)edges.push({id:'spoke:'+i,a:'C',b:'R'+i});
 return {n,lobes,vertices,edges,contact:['C','R0'],strength:1};
}
export function contractFirstContact(n,lobes=1) {
 const original=sourceGraph(n,lobes);
 const survivor='C+R0',mapping=Object.fromEntries(original.vertices.map(v=>[v.id,v.id==='C'||v.id==='R0'?survivor:v.id]));
 const vertices=[{id:survivor,position:{x:0,y:0}},...original.vertices.filter(v=>v.id!=='C'&&v.id!=='R0').map(copy)];
 const keys=new Map(),edges=[],lineage=[];
 for(const e of original.edges){
   const a=mapping[e.a],b=mapping[e.b];
   if(a===b){lineage.push({source:e.id,destination:null,reason:'self-loop removed'});continue}
   const key=pair(a,b);
   if(keys.has(key)){lineage.push({source:e.id,destination:keys.get(key),reason:'parallel edge deduplicated'});continue}
   const dest='E'+edges.length;
   keys.set(key,dest);edges.push({id:dest,a,b});
   lineage.push({source:e.id,destination:dest,reason:'edge retained'});
 }
 const V=vertices.length,E=edges.length;
 // Use E-V+2 only after validating the graph is connected.
 const adj=Object.fromEntries(vertices.map(v=>[v.id,[]]));
 for(const e of edges){adj[e.a].push(e.b);adj[e.b].push(e.a)}
 const seen=new Set([vertices[0].id]),stack=[vertices[0].id];
 while(stack.length){for(const v of adj[stack.pop()])if(!seen.has(v)){seen.add(v);stack.push(v)}}
 if(seen.size!==V)throw Error('Successor graph disconnected');
 if(V!==n || E!==2*n-3)throw Error('Unexpected contraction edge count');
 const faces=E-V+2;
 // The remaining n-1 outer vertices and central survivor create a fan
 // of n-2 positive-area bounded triangles (for this radial geometry).
 const pos=Object.fromEntries(vertices.map(v=>[v.id,v.position]));
 const areas=[];
 for(let i=1;i<n-1;i++){
   const a=pos['R'+i],b=pos['R'+(i+1)];
   const area=(a.x*b.y-a.y*b.x)/2;
   if(!(area>1e-12))throw Error('Invalid successor face '+i);
   areas.push(area);
 }
 if(faces!==n-1||areas.length!==n-2)throw Error('Euler/face mismatch');
 return {version:'QG-047',original,successor:{vertices,edges,verticesCount:V,edgesCount:E,facesCount:faces,boundedFaces:areas.length,euler:V-E+faces,areas},vertexMap:mapping,edgeLineage:lineage,operation:{type:'contract',contact:['C','R0'],survivor}};
}
export function verifyContraction(packet) {
 if(!packet||packet.version!=='QG-047')throw Error('Invalid certificate');
 const n=packet.original?.n,lobes=packet.original?.lobes;
 const expected=contractFirstContact(n,lobes);
 if(!eq(packet,expected))throw Error('Contraction evidence mismatch');
 return {valid:true,originalV:packet.original.vertices.length,originalE:packet.original.edges.length,
   newV:packet.successor.verticesCount,newE:packet.successor.edgesCount,
   newF:packet.successor.facesCount,euler:packet.successor.euler};
}
export function startSurgeryLedger(n=8,lobes=1){
 return {version:'QG-047-ledger',n,lobes,events:[]};
}
export function appendSurgery(ledger) {
 verifySurgeryLedger(ledger);
 const certificate=contractFirstContact(ledger.n,ledger.lobes);
 return {version:'QG-047-ledger',n:ledger.n,lobes:ledger.lobes,
   events:[...copy(ledger.events),{index:ledger.events.length,certificate}]};
}
export function verifySurgeryLedger(ledger) {
 if(!ledger||ledger.version!=='QG-047-ledger'||!Array.isArray(ledger.events))throw Error('Invalid ledger');
 contractFirstContact(ledger.n,ledger.lobes);
 for(let i=0;i<ledger.events.length;i++){
   const e=ledger.events[i];
   if(!e||e.index!==i)throw Error('Broken event ordering');
   verifyContraction(e.certificate);
 }
 return {valid:true,events:ledger.events.length};
}
