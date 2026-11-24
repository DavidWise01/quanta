// ADA-221N .dlw — normalized spatial expression; provisional Phase IV parent.
import {canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {derivePropagation} from "./ada-218n-epoch-propagation.mjs";
export const PARENT="52c3317bd9d1d478e71a925314ae88062777b960";
export const BOX_HALF=1, MAJOR_RADIUS=.45, MINOR_RADIUS=.15, MAX_SHIFT=.25;
const round=x=>Number(x.toFixed(6));
export function deriveSpatial(chain){
 const epochs=derivePropagation(chain),out=[];let parent=null;
 for(const e of epochs)for(const r of e.rows){
  const delta=r.permit?bound((r.perception-r.raw)/100,-MAX_SHIFT,MAX_SHIFT):0;
  const angle=(r.generation%24)*Math.PI/12;
  const center=Object.freeze([round(delta*Math.cos(angle)),round(delta*Math.sin(angle)),round(delta)]);
  const body={schema:"ADA-221N.spatial.v1",parentCommit:PARENT,epoch:e.epoch,generation:r.generation,sourceHash:r.sourceHash,propagationParent:e.parent,parent,center,boxHalf:BOX_HALF,majorRadius:MAJOR_RADIUS,minorRadius:MINOR_RADIUS,growthFactor:1.025,permit:r.permit};
  parent=fnv64(canonical(body));out.push(Object.freeze({...body,hash:parent}));
 }
 return Object.freeze(out);
}
export function verifySpatial(chain,ledger){
 try{const expected=deriveSpatial(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every(r=>r.center.every(x=>Math.abs(x)+MAJOR_RADIUS+MINOR_RADIUS<=BOX_HALF)&&(!r.permit?r.center.every(x=>x===0):true)),count:expected.length}}catch(e){return {pass:false,reason:e.message}}
}
