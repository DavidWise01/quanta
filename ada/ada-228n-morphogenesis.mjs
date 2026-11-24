// ADA-228N .dlw — causal descendant morphology from six local surfaces.
import {canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {deriveSpecialization,verifySpecialization} from "./ada-227n-geometric-specialization.mjs";
import {deriveNested} from "./ada-224n-nested-spatial.mjs";
const round=x=>Number(x.toFixed(9));
export function deriveMorphogenesis(chain){
 const source=deriveSpecialization(chain),nested=deriveNested(chain);
 if(!verifySpecialization(chain,source).pass)throw Error("Specialization replay failed");
 let parent=null;
 return Object.freeze(source.map((s,i)=>{
  const previous=source[i-1],g=chain[i],permit=g.decision==="APPEND"&&g.stability>=90&&g.energy>=5;
  const levels=Object.freeze(nested[i].levels.map(l=>{
   const faces=previous?.levels[l.depth].faces;
   const diff=[0,1,2].map(j=>permit&&faces?faces[2*j+1].response-faces[2*j].response:0);
   const mean=permit&&faces?faces.reduce((a,f)=>a+f.response,0)/6:0;
   const center=Object.freeze(l.center.map((x,j)=>round(bound(x+.05*l.half*diff[j],-.25*l.half,.25*l.half))));
   const R=round(bound(l.R+.025*l.half*mean,.4*l.half,.5*l.half));
   const r=round(bound(l.r+.0125*l.half*mean,.1*l.half,.2*l.half));
   return Object.freeze({depth:l.depth,half:l.half,center,R,r,tilt:l.tilt,clearance:round(l.half-Math.max(...center.map(Math.abs))-R-r),drive:Object.freeze(diff),mean:round(mean)});
  }));
  const body={schema:"ADA-228N.morphogenesis.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,previousSurfaceHash:previous?.hash??null,nestedHash:nested[i].hash,parent,permit,levels,growthFactor:1.025};
  parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyMorphogenesis(chain,ledger){
 try{const expected=deriveMorphogenesis(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.growthFactor===1.025&&s.levels.every(l=>l.clearance>=.05*l.half-1e-8&&l.R>l.r&&l.drive.every(d=>Math.abs(d)<=1)&&(!s.permit?l.mean===0&&l.drive.every(d=>d===0):true))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
