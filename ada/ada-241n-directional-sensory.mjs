// ADA-241N .dlw — directional sensory geometry, observation-only initialization.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveSpecialization,verifySpecialization} from "./ada-227n-geometric-specialization.mjs";
import {deriveEquilibrium,verifyEquilibrium} from "./ada-238n-adaptive-equilibrium.mjs";
export const PHASE_VI_PARENT="e815ef6243e1c2ffe8996f7d93c73badfb6d9a2c";
export function deriveSensory(chain){
 const s=deriveSpecialization(chain),m=deriveEquilibrium(chain);
 if(!verifySpecialization(chain,s).pass||!verifyEquilibrium(chain,m).pass)throw Error("Inherited replay failed");
 let parent=null;
 return Object.freeze(s.map((r,i)=>{
 const levels=Object.freeze(r.levels.map(l=>{
 const axes=Object.freeze(["X","Y","Z"].map((axis,j)=>{
 const faces=Object.freeze([-1,1].map(sign=>{
 const face=(sign<0?"-":"+")+axis,f=l.faces.find(v=>v.face===face);
 if(!f)throw Error("Missing inherited face "+face);
 return Object.freeze({face,sign,normal:Object.freeze([0,1,2].map(k=>k===j?sign:0)),attenuation:f.attenuation,raw:null,observed:false});
 }));
 return Object.freeze({axis,faces,state:null,domain:Object.freeze([-1,0,1])});
 }));
 return Object.freeze({depth:l.depth,axes,reserve:m[i].levels[l.depth].totalClosing,capacity:m[i].levels[l.depth].capacity});
 }));
 const body={schema:"ADA-241N.sensory.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,surfaceHash:r.hash,metabolismHash:m[i].hash,phaseVIParent:PHASE_VI_PARENT,parent,levels,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifySensory(chain,ledger){
 try{const a=deriveSensory(chain);return {pass:canonical(a)===canonical(ledger)&&a.every(r=>r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.levels.length===3&&r.levels.every(l=>l.axes.length===3&&new Set(l.axes.flatMap(x=>x.faces.map(f=>f.face))).size===6&&l.axes.every(x=>x.state===null&&x.faces.length===2&&x.faces.every(f=>f.raw===null&&!f.observed&&f.attenuation>=0&&f.attenuation<=1)&&x.faces[0].normal.every((v,j)=>v===-x.faces[1].normal[j])))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
