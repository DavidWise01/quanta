// ADA-253N .dlw — causal rolling history of contemporaneous spatial relationships.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveSpatialRelationships,verifySpatialRelationships} from "./ada-252n-spatial-relationships.mjs";
export const RELATION_WINDOW=8;
export function temporalRelation(history){
 const observed=history.filter(h=>h.relation!==null);
 const sum=observed.reduce((s,h)=>s+h.relation,0);
 const trend=observed.length?Math.sign(sum):null;
 const agreement=observed.filter(h=>h.relation===1).length;
 const opposition=observed.filter(h=>h.relation===-1).length;
 const neutral=observed.filter(h=>h.relation===0).length;
 const coverage=history.length?observed.length/history.length:0;
 const current=history.at(-1)?.relation??null;
 return Object.freeze({current,trend,agreement,opposition,neutral,coverage,persistent:current!==null&&current!==0&&current===trend&&observed.length>=3&&coverage>=.75&&Math.max(agreement,opposition)>=Math.ceil(observed.length*.75)});
}
export function deriveTemporalRelationships(chain){
 const source=deriveSpatialRelationships(chain);if(!verifySpatialRelationships(chain,source).pass)throw Error("Spatial replay failed");
 let parent=null;
 return Object.freeze(source.map((r,i)=>{
 const slice=source.slice(Math.max(0,i-RELATION_WINDOW+1),i+1);
 const relationships=Object.freeze(r.relationships.map((row,j)=>Object.freeze(row.map((e,k)=>{
 const history=Object.freeze(slice.map(s=>Object.freeze({generation:s.generation,relation:s.relationships[j][k].relation})));
 return Object.freeze({...e,history,...temporalRelation(history)});
 }))));
 const body={schema:"ADA-253N.temporal-relationships.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,spatialHash:r.hash,parent,nodes:r.nodes,relationships,window:RELATION_WINDOW,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyTemporalRelationships(chain,ledger){
 try{const a=deriveTemporalRelationships(chain),s=deriveSpatialRelationships(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.spatialHash===s[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.relationships.length===9&&r.relationships.every((row,j)=>row.length===9&&row.every((e,k)=>e.history.length===Math.min(i+1,RELATION_WINDOW)&&e.history.every((h,t)=>{const p=s[i-e.history.length+1+t];return h.generation===p.generation&&h.relation===p.relationships[j][k].relation})&&e.current===s[i].relationships[j][k].relation&&(e.current!==null||!e.persistent)&&e.agreement+e.opposition+e.neutral===e.history.filter(h=>h.relation!==null).length))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function temporalFixtures(){
 const f=v=>temporalRelation(v.map((relation,generation)=>({relation,generation})));
 const checks={stable:f([1,1,1,1,1,1,1,1]).persistent,opposition:f([-1,-1,-1,-1]).persistent,impulse:!f([0,0,0,1]).persistent,missing:!f([1,1,1,null]).persistent,reversal:!f([1,1,1,1,1,1,1,-1]).persistent,neutral:f([0,0,0]).trend===0,unknown:f([null,null]).trend===null};
 return {pass:Object.values(checks).every(Boolean),checks};
}
