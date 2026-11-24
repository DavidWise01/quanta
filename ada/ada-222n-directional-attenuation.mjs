// ADA-222N .dlw — independent directional attenuation, derived only.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveSpatial,verifySpatial} from "./ada-221n-spatial-expression.mjs";
const round=x=>Number(x.toFixed(6));
export function deriveDirectional(chain){
 const spatial=deriveSpatial(chain);if(!verifySpatial(chain,spatial).pass)throw Error("Spatial source invalid");
 let parent=null;
 return Object.freeze(spatial.map((s,i)=>{
  const g=chain[i];
  const gains=Object.freeze([g.stability/100,g.energy/100,1-Math.abs(g.contacts[0]-g.contacts[2])/100].map(round));
  const center=Object.freeze(s.center.map((x,j)=>s.permit?round(x*gains[j]):0));
  const direction=Object.freeze(center.map(x=>Math.sign(x)));
  const body={schema:"ADA-222N.directional.v1",generation:s.generation,epoch:s.epoch,sourceHash:s.sourceHash,spatialHash:s.hash,parent,gains,center,direction,permit:s.permit,growthFactor:1.025};
  parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyDirectional(chain,ledger){
 try{const expected=deriveDirectional(chain),source=deriveSpatial(chain);
 return {pass:canonical(expected)===canonical(ledger)&&expected.every((r,i)=>r.gains.every(g=>g>=0&&g<=1)&&r.center.every((x,j)=>Math.abs(x)<=Math.abs(source[i].center[j])&&Math.abs(x)+.6<=1&&(!x||Math.sign(x)===Math.sign(source[i].center[j])))&&r.growthFactor===1.025),count:expected.length};
 }catch(e){return {pass:false,reason:e.message}}
}
