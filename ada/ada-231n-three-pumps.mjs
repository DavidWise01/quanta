// ADA-231N .dlw — three-pump geometry, no resource transfer yet.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveMorphogenesis,verifyMorphogenesis} from "./ada-228n-morphogenesis.mjs";
export const PHASE_V_PARENT="be5227d1578246587d7b6cffcb8af129459659d6";
const round=x=>Number(x.toFixed(9));
export function derivePumps(chain){
 const source=deriveMorphogenesis(chain);if(!verifyMorphogenesis(chain,source).pass)throw Error("Morphology replay failed");
 let parent=null;
 return Object.freeze(source.map(s=>{
 const levels=Object.freeze(s.levels.map(l=>{
 const pumps=Object.freeze(["R","G","B"].map((id,i)=>{
 const angle=i*2*Math.PI/3, radius=.5*l.half;
 const direction=Object.freeze([round(Math.cos(angle)),0,round(Math.sin(angle))]);
 const position=Object.freeze(l.center.map((x,j)=>round(x+radius*direction[j])));
 return Object.freeze({id,angleDegrees:i*120,direction,position,capacity:round(l.half**3),enabled:s.permit,flow:0});
 }));
 return Object.freeze({depth:l.depth,half:l.half,center:l.center,pumps});
 }));
 const body={schema:"ADA-231N.pumps.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,morphologyHash:s.hash,parent,phaseVParent:PHASE_V_PARENT,levels,growthFactor:1.025};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyPumps(chain,ledger){
 try{const expected=derivePumps(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.growthFactor===1.025&&s.levels.every(l=>l.pumps.length===3&&l.pumps.every((p,i)=>p.flow===0&&p.position.every(x=>Math.abs(x)<=l.half+1e-9)&&l.pumps.every((q,j)=>i===j||Math.abs(p.direction.reduce((a,x,k)=>a+x*q.direction[k],0)+.5)<1e-8)))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
