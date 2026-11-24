// ADA-226N .dlw — six exact support-plane clearances per local frame.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveNested,verifyNested} from "./ada-224n-nested-spatial.mjs";
const round=x=>Number(x.toFixed(9));
export function deriveBoundary(chain){
 const nested=deriveNested(chain);if(!verifyNested(chain,nested).pass)throw Error("Nested replay failed");
 let parent=null;
 return Object.freeze(nested.map(s=>{
  const levels=Object.freeze(s.levels.map(l=>{
   // Torus axis is rotated from Y about Z by tilt; support = R*radial projection+r.
   const axis=[-Math.sin(l.tilt),Math.cos(l.tilt),0];
   const faces=Object.freeze(["X","Y","Z"].flatMap((name,i)=>[-1,1].map(sign=>{
    const extent=l.R*Math.sqrt(Math.max(0,1-axis[i]**2))+l.r;
    const clearance=round(l.half-sign*l.center[i]-extent);
    const ratio=round(clearance/l.half);
    return Object.freeze({face:(sign<0?"-":"+")+name,clearance,ratio,attenuation:round(Math.max(0,Math.min(1,ratio/.25))),state:ratio<0?"BREACH":ratio<.25?"NEAR":"CLEAR"});
   })));
   return Object.freeze({depth:l.depth,faces,minimum:Math.min(...faces.map(f=>f.clearance))});
  }));
  const body={schema:"ADA-226N.boundary.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,nestedHash:s.hash,parent,levels,growthFactor:1.025};
  parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyBoundary(chain,ledger){
 try{const expected=deriveBoundary(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(s=>s.growthFactor===1.025&&s.levels.every(l=>l.faces.length===6&&l.faces.every(f=>f.clearance>=0&&f.attenuation>=0&&f.attenuation<=1))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
