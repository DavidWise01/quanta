// ADA-224N .dlw — nested spatial frames, immutable derived history.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveMorphology,verifyMorphology} from "./ada-223n-local-morphology.mjs";
const round=x=>Number(x.toFixed(9));
export function deriveNested(chain){
 const source=deriveMorphology(chain);if(!verifyMorphology(chain,source).pass)throw Error("Morphology replay failed");
 let parent=null,anchor=null;
 return Object.freeze(source.map(s=>{
  if(!anchor||anchor.epoch!==s.epoch)anchor={epoch:s.epoch,sourceHash:s.hash,center:s.center};
  const levels=Object.freeze([0,1,2].map(depth=>{
   const half=1/4**depth;
   return Object.freeze({depth,half,center:Object.freeze(s.center.map(x=>round(x*half))),R:round(s.R*half),r:round(s.r*half),tilt:s.tilt});
  }));
  const body={schema:"ADA-224N.nested.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,morphologyHash:s.hash,epochAnchor:anchor.sourceHash,parent,levels,growthFactor:1.025};
  parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyNested(chain,ledger){
 try{const expected=deriveNested(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.levels.every((l,i)=>Math.max(...l.center.map(Math.abs))+l.R+l.r<=l.half+1e-9&&(!i||Math.max(...l.center.map(Math.abs))+l.half<=s.levels[i-1].half))&&s.growthFactor===1.025),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
