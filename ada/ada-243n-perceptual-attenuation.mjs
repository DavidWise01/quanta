// ADA-243N .dlw — preserve raw acquisition; derive bounded perceived intensity.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveAcquisition,verifyAcquisition} from "./ada-242n-signal-acquisition.mjs";
export function perceive(raw,gain){
 if(!Number.isFinite(gain)||gain<0||gain>1)throw Error("Invalid attenuation");
 if(raw===null)return null;
 if(!Number.isInteger(raw)||raw<0||raw>1000)throw Error("Invalid raw signal");
 return Math.floor(raw*gain);
}
export function derivePerception(chain){
 const source=deriveAcquisition(chain);if(!verifyAcquisition(chain,source).pass)throw Error("Acquisition replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const levels=Object.freeze(r.levels.map(l=>Object.freeze({depth:l.depth,axes:Object.freeze(l.axes.map(a=>Object.freeze({axis:a.axis,state:null,faces:Object.freeze(a.faces.map(f=>{const perceived=perceive(f.raw,f.attenuation);return Object.freeze({...f,perceived,loss:f.raw===null?null:f.raw-perceived});}))})))})));
 const body={schema:"ADA-243N.perception.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,acquisitionHash:r.hash,parent,levels,growthFactor:1.025,authority:"OBSERVE_ONLY",unit:"normalized-milli-signal"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyPerception(chain,ledger){
 try{const a=derivePerception(chain),source=deriveAcquisition(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.acquisitionHash===source[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.levels.every((l,d)=>l.axes.every((x,j)=>x.state===null&&x.faces.every((f,k)=>f.raw===source[i].levels[d].axes[j].faces[k].raw&&(f.raw===null?f.perceived===null&&f.loss===null: Number.isInteger(f.perceived)&&f.perceived>=0&&f.perceived<=f.raw&&f.raw===f.perceived+f.loss))))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
