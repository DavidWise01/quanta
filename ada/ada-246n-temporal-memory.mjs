// ADA-246N .dlw — bounded temporal memory over all nine comparators.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveAttention,verifyAttention} from "./ada-245n-selective-attention.mjs";
export const MEMORY_WINDOW=8;
export function memoryStep(candidate,previous,generation){
 const history=Object.freeze([...(previous?.history??[]),Object.freeze({generation,delta:candidate.delta,selected:candidate.selected})].slice(-MEMORY_WINDOW));
 const observed=history.filter(x=>x.delta!==null),mean=observed.length?Math.trunc(observed.reduce((n,x)=>n+x.delta,0)/observed.length):null;
 const trend=mean===null?null:mean>25?1:mean< -25?-1:0;
 const coverage=observed.length/history.length;
 return Object.freeze({address:candidate.address,axis:candidate.axis,depth:candidate.depth,current:candidate.delta,history,mean,trend,coverage,focusCount:history.filter(x=>x.selected).length,status:candidate.delta===null?"CURRENT_MISSING":observed.length<3?"WARMUP":"OBSERVED",persistent:candidate.delta!==null&&observed.length>=3&&coverage>=.75&&trend!==0&&trend!==null&&observed.filter(x=>Math.sign(x.delta)===trend&&Math.abs(x.delta)>25).length>=Math.ceil(observed.length*.75)});
}
export function deriveMemory(chain){
 const source=deriveAttention(chain);if(!verifyAttention(chain,source).pass)throw Error("Attention replay failed");
 let prior=null;
 return Object.freeze(source.map(r=>{
 const memory=Object.freeze(r.attention.map(c=>memoryStep(c,prior?.memory[c.address],r.generation)));
 const body={schema:"ADA-246N.memory.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,attentionHash:r.hash,parent:prior?.hash??null,levels:r.levels,attention:r.attention,memory,window:MEMORY_WINDOW,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});return prior;
 }));
}
export function verifyMemory(chain,ledger){
 try{const a=deriveMemory(chain),s=deriveAttention(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.attentionHash===s[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.memory.length===9&&canonical(r.levels)===canonical(s[i].levels)&&r.memory.every((m,j)=>m.current===s[i].attention[j].delta&&m.history.length===Math.min(i+1,MEMORY_WINDOW)&&m.history.every((h,k)=>{const p=s[i-m.history.length+1+k];return h.generation===p.generation&&h.delta===p.attention[j].delta&&h.selected===p.attention[j].selected})&&(m.current!==null||!m.persistent)&&m.coverage>=0&&m.coverage<=1)),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
