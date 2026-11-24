// ADA-219N .dlw — long-horizon audit; no source mutation.
import {genesis,advance,canonical} from "./ada-201n-generational-engine.mjs";
import {derivePropagation,verifyPropagation} from "./ada-218n-epoch-propagation.mjs";
export function auditHorizon(chain){
 const a=derivePropagation(chain),sealed=a.filter(e=>e.state==="SEALED");
 const checks={replay:verifyPropagation(chain,a).pass,carryBound:a.every(e=>Math.abs(e.incoming)<=.125&&(e.outgoing===null||Math.abs(e.outgoing)<=.125)),offsetBound:a.every(e=>Math.abs(e.offset)<=.25),perceptionBound:a.every(e=>e.rows.every(r=>r.perception>=0&&r.perception<=100)),holdBypass:a.every(e=>e.rows.every(r=>r.permit||r.raw===r.perception)),growth:a.every(e=>e.growthFactor===1.025),tail:a.every(e=>e.state==="SEALED"||e.outgoing===null),lineage:a.every((e,i)=>e.parent===(a[i-1]?.hash??null)&&e.incoming===(a[i-1]?.outgoing??0))};
 const maxCarry=Math.max(0,...sealed.map(e=>Math.abs(e.outgoing)));
 const maxOffset=Math.max(0,...a.map(e=>Math.abs(e.offset)));
 const reversals=sealed.slice(1).filter((e,i)=>e.outgoing*sealed[i].outgoing<0).length;
 return {pass:Object.values(checks).every(Boolean),checks,epochs:a.length,sealed:sealed.length,maxCarry,maxOffset,reversals};
}
export function stressHorizon(steps=9600){
 if(!Number.isSafeInteger(steps)||steps<1||steps>10000)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 const before=canonical(chain),result=auditHorizon(chain);
 const short=chain.slice(0,Math.min(chain.length,240));
 const prefix=derivePropagation(short).filter(e=>e.state==="SEALED");
 const full=derivePropagation(chain);
 result.checks.prefix=prefix.every((e,i)=>canonical(e)===canonical(full[i]));
 result.checks.immutable=before===canonical(chain);
 result.pass=Object.values(result.checks).every(Boolean);return result;
}
