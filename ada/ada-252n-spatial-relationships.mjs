// ADA-252N .dlw — simultaneous spatial relationships, observation only.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveContext,verifyContext} from "./ada-251n-contextual-architecture.mjs";
export function spatialRelation(a,b){
 if(a.state===null||b.state===null)return Object.freeze({relation:null,observed:false,difference:null,strength:null});
 if(![-1,0,1].includes(a.state)||![-1,0,1].includes(b.state)||!Number.isInteger(a.effective)||!Number.isInteger(b.effective))throw Error("Invalid contextual state");
 return Object.freeze({relation:a.state*b.state,observed:true,difference:b.effective-a.effective,strength:Math.min(Math.abs(a.effective),Math.abs(b.effective))});
}
export function deriveSpatialRelationships(chain){
 const source=deriveContext(chain);if(!verifyContext(chain,source).pass)throw Error("Context replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const relationships=Object.freeze(r.topology.map(row=>Object.freeze(row.map(e=>Object.freeze({...e,...spatialRelation(r.nodes[e.from],r.nodes[e.to])})))));
 const body={schema:"ADA-252N.spatial-relationships.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,contextHash:r.hash,parent,nodes:r.nodes,relationships,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifySpatialRelationships(chain,ledger){
 try{const a=deriveSpatialRelationships(chain),s=deriveContext(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.contextHash===s[i].hash&&canonical(r.nodes)===canonical(s[i].nodes)&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.relationships.length===9&&r.relationships.every((row,j)=>row.length===9&&row.every((e,k)=>e.from===j&&e.to===k&&e.relation===r.relationships[k][j].relation&&canonical(spatialRelation(r.nodes[j],r.nodes[k]))===canonical({relation:e.relation,observed:e.observed,difference:e.difference,strength:e.strength})&&(e.observed?e.difference===-r.relationships[k][j].difference:e.difference===null)))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
