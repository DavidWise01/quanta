// ADA-244N .dlw — ternary directional differentiation, observation only.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {derivePerception,verifyPerception} from "./ada-243n-perceptual-attenuation.mjs";
export const DEADBAND=25;
export function differentiate(negative,positive){
 for(const v of [negative,positive])if(v!==null&&(!Number.isInteger(v)||v<0||v>1000))throw Error("Invalid perceived intensity");
 if(negative===null||positive===null)return Object.freeze({delta:null,state:null,status:"INCOMPLETE"});
 const delta=positive-negative;
 return Object.freeze({delta,state:delta>DEADBAND?1:delta< -DEADBAND?-1:0,status:"OBSERVED"});
}
export function deriveDifferentiation(chain){
 const source=derivePerception(chain);if(!verifyPerception(chain,source).pass)throw Error("Perception replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const levels=Object.freeze(r.levels.map(l=>Object.freeze({depth:l.depth,axes:Object.freeze(l.axes.map(a=>{
 const negative=a.faces.find(f=>f.sign===-1),positive=a.faces.find(f=>f.sign===1);
 if(!negative||!positive)throw Error("Missing directional address");
 return Object.freeze({...a,...differentiate(negative.perceived,positive.perceived)});
 }))})));
 const body={schema:"ADA-244N.differentiation.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,perceptionHash:r.hash,parent,levels,deadband:DEADBAND,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyDifferentiation(chain,ledger){
 try{const a=deriveDifferentiation(chain),p=derivePerception(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.perceptionHash===p[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.levels.every((l,d)=>l.axes.every((x,j)=>canonical(x.faces)===canonical(p[i].levels[d].axes[j].faces)&& (x.faces.some(f=>f.perceived===null)?x.state===null&&x.delta===null:x.delta===x.faces.find(f=>f.sign===1).perceived-x.faces.find(f=>f.sign===-1).perceived&&x.state===(x.delta>DEADBAND?1:x.delta< -DEADBAND?-1:0))))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
