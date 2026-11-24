// ADA-248N .dlw — prospective per-channel perceptual adaptation.
import {canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {deriveMemory,verifyMemory} from "./ada-246n-temporal-memory.mjs";
export function adaptPolicy(previous,history){
 const observed=history.filter(h=>h.delta!==null);
 if(history.length<8||observed.length<6)return Object.freeze({...previous});
 const changes=observed.slice(1).filter((h,i)=>Math.abs(h.delta-observed[i].delta)>100).length;
 const step=changes>=Math.ceil((observed.length-1)*.5)?-1:changes===0?1:0;
 return Object.freeze({window:bound(previous.window+step,3,8),threshold:bound(previous.threshold-step*5,25,100),sensitivity:bound(previous.sensitivity+step*5,50,100)});
}
export function deriveAdaptivePerception(chain){
 const source=deriveMemory(chain);if(!verifyMemory(chain,source).pass)throw Error("Memory replay failed");
 let prior=null,previousEpoch=null;const out=[];
 for(const e of epochHierarchy(chain)){
 const policies=Object.freeze(Array.from({length:9},(_,j)=>{
 const old=previousEpoch?.policies[j]??{window:8,threshold:25,sensitivity:100};
 return previousEpoch?.state==="SEALED"&&previousEpoch.holds===0?adaptPolicy(old,previousEpoch.memory[j].history):Object.freeze({...old});
 }));
 for(let i=e.sourceStart;i<=e.sourceEnd;i++){
 const s=source[i];
 const channels=Object.freeze(s.memory.map((m,j)=>{
 const policy=policies[j],history=Object.freeze(m.history.slice(-policy.window)),observed=history.filter(h=>h.delta!==null);
 const effective=m.current===null?null:Math.trunc(m.current*policy.sensitivity/100);
 const state=effective===null?null:effective>policy.threshold?1:effective< -policy.threshold?-1:0;
 return Object.freeze({address:m.address,policy,history,current:m.current,effective,state,coverage:observed.length/history.length});
 }));
 const ranked=channels.filter(c=>c.state===1||c.state===-1).sort((a,b)=>Math.abs(b.effective)-Math.abs(a.effective)||a.address-b.address);
 const focus=Object.freeze(ranked.slice(0,3).map(c=>c.address));
 const body={schema:"ADA-248N.adaptive-perception.v1",generation:s.generation,epoch:e.epoch,sourceHash:s.sourceHash,memoryHash:s.hash,parent:prior?.hash??null,policyParent:previousEpoch?.hash??null,channels,focus,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});out.push(prior);
 }
 previousEpoch={state:e.state,holds:e.holds,hash:prior.hash,policies,memory:source[e.sourceEnd].memory};
 }
 return Object.freeze(out);
}
export function verifyAdaptivePerception(chain,ledger){
 try{const a=deriveAdaptivePerception(chain),s=deriveMemory(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.memoryHash===s[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.focus.length<=3&&new Set(r.focus).size===r.focus.length&&r.channels.every((c,j)=>c.policy.window>=3&&c.policy.window<=8&&c.policy.threshold>=25&&c.policy.threshold<=100&&c.policy.sensitivity>=50&&c.policy.sensitivity<=100&&c.current===s[i].memory[j].current&&canonical(c.history)===canonical(s[i].memory[j].history.slice(-c.policy.window))&&(c.current===null?c.effective===null&&c.state===null:Math.abs(c.effective)<=Math.abs(c.current))&&(!i||r.epoch!==a[i-1].epoch||canonical(c.policy)===canonical(a[i-1].channels[j].policy)))&&r.focus.every(j=>r.channels[j].state===1||r.channels[j].state===-1)),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
