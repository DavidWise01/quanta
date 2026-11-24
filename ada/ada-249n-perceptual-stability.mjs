// ADA-249N .dlw — long-horizon perception audit and synthetic fixtures.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {deriveAdaptivePerception,verifyAdaptivePerception,adaptPolicy} from "./ada-248n-adaptive-perception.mjs";
import {deriveMemory,memoryStep} from "./ada-246n-temporal-memory.mjs";
import {differentiate} from "./ada-244n-signal-differentiation.mjs";
import {perceive} from "./ada-243n-perceptual-attenuation.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
export function auditPerception(chain){
 const before=canonical(chain),a=deriveAdaptivePerception(chain),m=deriveMemory(chain),epochs=epochHierarchy(chain);
 const prefix=deriveAdaptivePerception(chain.slice(0,Math.min(240,chain.length)));
 const checks={
 replay:verifyAdaptivePerception(chain,a).pass,
 sourceUnchanged:before===canonical(chain),
 prefix:prefix.every((r,i)=>canonical(r)===canonical(a[i])),
 lineage:a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.sourceHash===chain[i].hash&&r.memoryHash===m[i].hash),
 policyCausality:epochs.every(e=>a.slice(e.sourceStart,e.sourceEnd+1).every(r=>r.policyParent===(e.sourceStart?a[e.sourceStart-1].hash:null))),
 policyHold:epochs.every((e,i)=>!i||!epochs[i-1].holds||a[e.sourceStart].channels.every((c,j)=>canonical(c.policy)===canonical(a[e.sourceStart-1].channels[j].policy))),
 missing:a.every(r=>r.channels.every(c=>c.current!==null||c.effective===null&&c.state===null&&!r.focus.includes(c.address))),
 focus:a.every(r=>canonical(r.focus)===canonical(r.channels.filter(c=>c.state===1||c.state===-1).sort((x,y)=>Math.abs(y.effective)-Math.abs(x.effective)||x.address-y.address).slice(0,3).map(c=>c.address))),
 history:a.every(r=>r.channels.every(c=>c.history.length<=8&&new Set(c.history.map(h=>h.generation)).size===c.history.length)),
 authority:a.every(r=>r.authority==="OBSERVE_ONLY"),growth:a.every(r=>r.growthFactor===1.025)};
 return {pass:Object.values(checks).every(Boolean),checks,generations:a.length,channels:a.length*9,tip:a.at(-1)?.hash};
}
export function perceptualFixtures(){
 const policy={window:6,threshold:50,sensitivity:80};
 const rows=v=>v.map((delta,generation)=>({generation,delta,selected:false}));
 const memory=values=>values.reduce((p,delta,generation)=>memoryStep({address:0,axis:"X",depth:0,delta,selected:false},p,generation),null);
 const stable=adaptPolicy(policy,rows(Array(8).fill(300)));
 const volatile=adaptPolicy(policy,rows([300,-300,300,-300,300,-300,300,-300]));
 const missing=adaptPolicy(policy,rows([null,null,null,300,300,300,300,300]));
 let low=policy,high=policy;for(let i=0;i<100;i++){low=adaptPolicy(low,rows([300,-300,300,-300,300,-300,300,-300]));high=adaptPolicy(high,rows(Array(8).fill(300)))}
 const checks={missingRaw:perceive(null,0)===null,zeroRaw:perceive(0,1)===0,attenuatedZero:perceive(1000,0)===0,missingPair:differentiate(null,100).state===null,deadband:differentiate(0,25).state===0&&differentiate(0,26).state===1&&differentiate(26,0).state===-1,sustained:memory(Array(8).fill(300)).persistent,impulse:!memory([0,0,0,0,0,0,0,900]).persistent,reversal:memory([...Array(8).fill(300),...Array(8).fill(-300)]).trend===-1,missingCurrent:!memory([300,300,300,300,300,300,300,null]).persistent,stablePolicy:stable.window===7&&stable.sensitivity===85&&stable.threshold===45,volatilePolicy:volatile.window===5&&volatile.sensitivity===75&&volatile.threshold===55,missingPolicy:canonical(missing)===canonical(policy),lowerSaturation:low.window===3&&low.sensitivity===50&&low.threshold===100,upperSaturation:high.window===8&&high.sensitivity===100&&high.threshold===25};
 return {pass:Object.values(checks).every(Boolean),checks};
}
export function stressPerception(steps=2400){
 if(!Number.isSafeInteger(steps)||steps<1||steps>9600)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 const audit=auditPerception(chain),fixtures=perceptualFixtures();return {pass:audit.pass&&fixtures.pass,audit,fixtures};
}
