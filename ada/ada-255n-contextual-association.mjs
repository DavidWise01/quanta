// ADA-255N .dlw — directly supported contextual associations.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveSemantics,verifySemantics} from "./ada-254n-semantic-differentiation.mjs";
export function associate(matrix){
 const n=9,groups=[],edges=[];
 if(matrix.length!==n||matrix.some(r=>r.length!==n))throw Error("Invalid topology");
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
 const e=matrix[i][j];if(e.semantic!==matrix[j][i].semantic)throw Error("Asymmetric semantics");
 edges.push(Object.freeze({from:i,to:j,semantic:e.semantic}));
 }
 // Enumerate maximal cliques, not connected components. No inferred edges.
 for(let mask=1;mask<(1<<n);mask++){
 const members=Array.from({length:n},(_,i)=>i).filter(i=>mask&(1<<i));
 if(members.length<2||!members.every((a,i)=>members.slice(i+1).every(b=>matrix[a][b].semantic==="STABLE_AGREEMENT")))continue;
 if(Array.from({length:n},(_,i)=>i).some(b=>!(mask&(1<<b))&&members.every(a=>matrix[a][b].semantic==="STABLE_AGREEMENT")))continue;
 const support=Object.freeze(edges.filter(e=>members.includes(e.from)&&members.includes(e.to)));
 groups.push(Object.freeze({mask,members:Object.freeze(members),support,kind:"DIRECT_AGREEMENT"}));
 }
 return Object.freeze({groups:Object.freeze(groups),edges:Object.freeze(edges),unassociated:Object.freeze(Array.from({length:n},(_,i)=>i).filter(i=>!groups.some(g=>g.members.includes(i))))});
}
export function deriveAssociations(chain){
 const source=deriveSemantics(chain);if(!verifySemantics(chain,source).pass)throw Error("Semantic replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const associations=associate(r.relationships);
 const body={schema:"ADA-255N.association.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,semanticHash:r.hash,parent,nodes:r.nodes,relationships:r.relationships,associations,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyAssociations(chain,ledger){
 try{const a=deriveAssociations(chain),s=deriveSemantics(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.semanticHash===s[i].hash&&canonical(r.relationships)===canonical(s[i].relationships)&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.associations.edges.length===36&&r.associations.groups.every(g=>g.support.length===g.members.length*(g.members.length-1)/2&&g.support.every(e=>e.semantic==="STABLE_AGREEMENT"&&r.relationships[e.from][e.to].semantic===e.semantic))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function associationFixtures(){
 const fixture=pairs=>Array.from({length:9},(_,i)=>Array.from({length:9},(_,j)=>({semantic:pairs.some(([a,b])=>a===i&&b===j||b===i&&a===j)?"STABLE_AGREEMENT":"INSUFFICIENT"})));
 const bridge=associate(fixture([[0,1],[1,2]])),triangle=associate(fixture([[0,1],[1,2],[0,2]])),empty=associate(fixture([]));
 const checks={noTransitiveInference:bridge.groups.length===2&&bridge.groups.every(g=>g.members.length===2),completeTriangle:triangle.groups.length===1&&triangle.groups[0].members.length===3,missingNotAgreement:empty.groups.length===0,allPairsRetained:bridge.edges.length===36,unassociated:empty.unassociated.length===9};
 return {pass:Object.values(checks).every(Boolean),checks};
}
