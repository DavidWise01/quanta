// ADA-223N .dlw — local morphology, derived from directional attenuation.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveDirectional,verifyDirectional} from "./ada-222n-directional-attenuation.mjs";
const round=x=>Number(x.toFixed(6));
export function deriveMorphology(chain){
 const source=deriveDirectional(chain);if(!verifyDirectional(chain,source).pass)throw Error("Directional replay failed");
 let parent=null;
 return Object.freeze(source.map(s=>{
  const R=s.permit?round(.4+.1*s.gains[0]):.45;
  const r=s.permit?round(.1+.1*s.gains[1]):.15;
  const tilt=s.permit?round((1-s.gains[2])*Math.PI/4*s.direction[2]):0;
  const clearance=round(1-Math.max(...s.center.map(Math.abs))-R-r);
  const body={schema:"ADA-223N.morphology.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,directionalHash:s.hash,parent,center:s.center,R,r,tilt,clearance,permit:s.permit,growthFactor:1.025};
  parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyMorphology(chain,ledger){
 try{const expected=deriveMorphology(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.R>s.r&&s.r>=.1&&s.R<=.5&&s.r<=.2&&s.clearance>=.05&&Math.abs(s.tilt)<=Math.PI/4+1e-6&&s.growthFactor===1.025),count:expected.length}}catch(e){return {pass:false,reason:e.message}}
}
