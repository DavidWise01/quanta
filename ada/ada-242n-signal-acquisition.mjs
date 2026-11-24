// ADA-242N .dlw — immutable synthetic raw acquisition, no interpretation.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveSensory,verifySensory} from "./ada-241n-directional-sensory.mjs";
export function syntheticSample(sourceHash,depth,face){
 const h=BigInt("0x"+fnv64(canonical([sourceHash,depth,face])).replace(/^0x/,""));
 return h%17n===0n?null:Number(h%1001n);
}
export function deriveAcquisition(chain){
 const source=deriveSensory(chain);if(!verifySensory(chain,source).pass)throw Error("Sensory replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const levels=Object.freeze(r.levels.map(l=>Object.freeze({depth:l.depth,axes:Object.freeze(l.axes.map(a=>Object.freeze({axis:a.axis,state:null,faces:Object.freeze(a.faces.map(f=>{const raw=syntheticSample(r.sourceHash,l.depth,f.face);return Object.freeze({...f,raw,observed:raw!==null});}))})))})));
 const body={schema:"ADA-242N.acquisition.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,sensoryHash:r.hash,parent,levels,growthFactor:1.025,authority:"OBSERVE_ONLY",origin:"DETERMINISTIC_SYNTHETIC",unit:"normalized-milli-signal"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyAcquisition(chain,ledger){
 try{const a=deriveAcquisition(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.levels.length===3&&r.levels.every(l=>l.axes.length===3&&l.axes.every(x=>x.state===null&&x.faces.length===2&&x.faces.every(f=>f.observed===(f.raw!==null)&&(f.raw===null||Number.isInteger(f.raw)&&f.raw>=0&&f.raw<=1000))))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
