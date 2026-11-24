// ADA-225N .dlw — volume accounting, not additive physical occupancy.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveNested,verifyNested} from "./ada-224n-nested-spatial.mjs";
const round=x=>Number(x.toPrecision(12));
export function deriveVolume(chain){
 const nested=deriveNested(chain);if(!verifyNested(chain,nested).pass)throw Error("Nested replay failed");
 let parent=null,prior=null;
 return Object.freeze(nested.map(s=>{
  const levels=Object.freeze(s.levels.map(l=>{
   const volume=round(2*Math.PI**2*l.R*l.r**2),boxVolume=round((2*l.half)**3);
   const fraction=round(volume/boxVolume),previous=prior?.levels[l.depth]?.fraction??fraction;
   return Object.freeze({depth:l.depth,volume,boxVolume,fraction,delta:round(fraction-previous),operant:Math.abs(fraction-previous)<1e-10?0:Math.sign(fraction-previous)});
  }));
  const body={schema:"ADA-225N.volume.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,nestedHash:s.hash,parent,levels,growthFactor:1.025,accounting:"LOCAL_NON_ADDITIVE"};
  parent=fnv64(canonical(body));prior=Object.freeze({...body,hash:parent});return prior;
 }));
}
export function verifyVolume(chain,ledger){
 try{const expected=deriveVolume(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.growthFactor===1.025&&s.levels.every((l,i)=>l.fraction>0&&l.fraction<1&&(!i||Math.abs(l.volume/s.levels[i-1].volume-1/64)<1e-6)&&Math.abs(l.fraction-s.levels[0].fraction)<1e-6)),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
