// ADA-227N .dlw — causal specialization of fixed response surfaces.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveBoundary,verifyBoundary} from "./ada-226n-boundary-differentiation.mjs";
const round=x=>Number(x.toFixed(9));
export function deriveSpecialization(chain){
 const source=deriveBoundary(chain);if(!verifyBoundary(chain,source).pass)throw Error("Boundary replay failed");
 let parent=null,prior=null;
 return Object.freeze(source.map((s,i)=>{
  const g=chain[i],permit=g.decision==="APPEND"&&g.stability>=90&&g.energy>=5;
  const levels=Object.freeze(s.levels.map(l=>Object.freeze({depth:l.depth,faces:Object.freeze(l.faces.map((f,j)=>{
   const previous=prior?.levels[l.depth].faces[j];
   const memory=round(.75*(previous?.memory??f.attenuation)+.25*f.attenuation);
   const axis=f.face[1],role={X:"STABILITY",Y:"ENERGY",Z:"CONTACT"}[axis];
   const input={X:g.stability/100,Y:g.energy/100,Z:1-Math.abs(g.contacts[0]-g.contacts[2])/100}[axis];
   const response=permit?round(Math.min(f.attenuation,memory)*input):0;
   return Object.freeze({face:f.face,role,clearance:f.clearance,attenuation:f.attenuation,memory,response,permit});
  }))})));
  const body={schema:"ADA-227N.specialization.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,boundaryHash:s.hash,parent,levels,growthFactor:1.025};
  parent=fnv64(canonical(body));prior=Object.freeze({...body,hash:parent});return prior;
 }));
}
export function verifySpecialization(chain,ledger){
 try{const expected=deriveSpecialization(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.growthFactor===1.025&&s.levels.every(l=>l.faces.length===6&&l.faces.every(f=>f.memory>=0&&f.memory<=1&&f.response>=0&&f.response<=f.attenuation&&(!f.permit?f.response===0:true)))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
