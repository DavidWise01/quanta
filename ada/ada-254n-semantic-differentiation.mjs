// ADA-254N .dlw — bounded descriptive semantics, observation only.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveTemporalRelationships,verifyTemporalRelationships} from "./ada-253n-temporal-relationships.mjs";
export function classifyRelationship(e){
 if(e.current===null||e.history.filter(h=>h.relation!==null).length<3||e.coverage<.75)return "INSUFFICIENT";
 if(e.current===0)return "NEUTRAL";
 if(e.persistent)return e.current===1?"STABLE_AGREEMENT":"STABLE_OPPOSITION";
 const prior=e.history.slice(0,-1).filter(h=>h.relation!==null);
 if(prior.length>=3&&prior.filter(h=>h.relation===-e.current).length>=Math.ceil(prior.length*.75))return "REVERSAL";
 return "EMERGING_CHANGE";
}
export function deriveSemantics(chain){
 const source=deriveTemporalRelationships(chain);if(!verifyTemporalRelationships(chain,source).pass)throw Error("Temporal replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const relationships=Object.freeze(r.relationships.map(row=>Object.freeze(row.map(e=>Object.freeze({...e,semantic:classifyRelationship(e)})))));
 const body={schema:"ADA-254N.semantics.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,temporalHash:r.hash,parent,nodes:r.nodes,relationships,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifySemantics(chain,ledger){
 try{const a=deriveSemantics(chain),s=deriveTemporalRelationships(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.temporalHash===s[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&canonical(r.nodes)===canonical(s[i].nodes)&&r.relationships.length===9&&r.relationships.every((row,j)=>row.length===9&&row.every((e,k)=>{const {semantic,...base}=e;return canonical(base)===canonical(s[i].relationships[j][k])&&semantic===classifyRelationship(base)&&semantic===r.relationships[k][j].semantic}))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function semanticFixtures(){
 const f=(v,persistent=false)=>classifyRelationship({current:v.at(-1),history:v.map(relation=>({relation})),coverage:v.filter(x=>x!==null).length/v.length,persistent});
 const cases=[[f([1,1,1],true),"STABLE_AGREEMENT"],[f([-1,-1,-1],true),"STABLE_OPPOSITION"],[f([1,1,1,-1]),"REVERSAL"],[f([0,0,1]),"EMERGING_CHANGE"],[f([1,1,0]),"NEUTRAL"],[f([1,1,null]),"INSUFFICIENT"],[f([1]),"INSUFFICIENT"]];
 return {pass:cases.every(([a,b])=>a===b),cases};
}
