// ADA-245N .dlw — bounded observation-only attention, preserving every comparator.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveDifferentiation,verifyDifferentiation} from "./ada-244n-signal-differentiation.mjs";
export const ATTENTION_LIMIT=3;
export function selectAttention(levels){
 const candidates=levels.flatMap(l=>l.axes.map((a,j)=>({depth:l.depth,axis:a.axis,address:l.depth*3+j,state:a.state,delta:a.delta,score:a.delta===null?null:Math.abs(a.delta)})));
 const eligible=candidates.filter(c=>c.state===-1||c.state===1).sort((a,b)=>b.score-a.score||a.address-b.address);
 const selected=new Set(eligible.slice(0,ATTENTION_LIMIT).map(c=>c.address));
 return Object.freeze(candidates.map(c=>Object.freeze({...c,selected:selected.has(c.address),rank:eligible.findIndex(x=>x.address===c.address)+1||null})));
}
export function deriveAttention(chain){
 const source=deriveDifferentiation(chain);if(!verifyDifferentiation(chain,source).pass)throw Error("Differentiation replay failed");
 let parent=null;
 return Object.freeze(source.map(r=>{
 const attention=selectAttention(r.levels);
 const body={schema:"ADA-245N.attention.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,differentiationHash:r.hash,parent,levels:r.levels,attention,limit:ATTENTION_LIMIT,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyAttention(chain,ledger){
 try{const a=deriveAttention(chain),s=deriveDifferentiation(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>{
 const ranked=r.attention.filter(x=>x.rank!==null).sort((a,b)=>a.rank-b.rank);
 return r.parent===(a[i-1]?.hash??null)&&r.differentiationHash===s[i].hash&&canonical(r.levels)===canonical(s[i].levels)&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.attention.length===9&&r.attention.filter(x=>x.selected).length===Math.min(ATTENTION_LIMIT,ranked.length)&&r.attention.every(x=>x.selected===(x.rank!==null&&x.rank<=ATTENTION_LIMIT)&&((x.state===null||x.state===0)?x.rank===null:true))&&ranked.every((x,j)=>x.rank===j+1&&(!j||ranked[j-1].score>x.score||ranked[j-1].score===x.score&&ranked[j-1].address<x.address));
 }),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
