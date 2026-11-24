// ADA-251N .dlw — contextual topology without inferred relationships.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveAdaptivePerception,verifyAdaptivePerception} from "./ada-248n-adaptive-perception.mjs";
export const PHASE_VII_PARENT="37ba1fc4b51247d4ed8289894a9021c037b3f591";
export function relationshipTopology(){
 return Object.freeze(Array.from({length:9},(_,a)=>Object.freeze(Array.from({length:9},(_,b)=>Object.freeze({from:a,to:b,kind:a===b?"SELF":Math.floor(a/3)===Math.floor(b/3)?"SAME_FRAME":a%3===b%3?"SAME_AXIS":"CROSS_FRAME_AXIS",relation:null,observed:false})))));
}
export function deriveContext(chain){
 const source=deriveAdaptivePerception(chain);if(!verifyAdaptivePerception(chain,source).pass)throw Error("Perception replay failed");
 const topology=relationshipTopology();let parent=null;
 return Object.freeze(source.map(r=>{
 const nodes=Object.freeze(r.channels.map(c=>Object.freeze({address:c.address,depth:Math.floor(c.address/3),axis:["X","Y","Z"][c.address%3],current:c.current,effective:c.effective,state:c.state,focused:r.focus.includes(c.address)})));
 const body={schema:"ADA-251N.context.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,perceptionHash:r.hash,phaseVIIParent:PHASE_VII_PARENT,parent,nodes,topology,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyContext(chain,ledger){
 try{const a=deriveContext(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.nodes.length===9&&r.nodes.every((n,j)=>n.address===j&&(n.current!==null||n.effective===null&&n.state===null))&&r.topology.length===9&&r.topology.every((row,j)=>row.length===9&&row.every((e,k)=>e.from===j&&e.to===k&&e.kind===r.topology[k][j].kind&&e.relation===null&&!e.observed))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
