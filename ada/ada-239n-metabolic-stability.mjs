// ADA-239N .dlw — integrated replay and independent synthetic disturbance fixtures.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {deriveEquilibrium,verifyEquilibrium,equilibriumStep} from "./ada-238n-adaptive-equilibrium.mjs";
export function auditMetabolism(chain){
 const before=canonical(chain),a=deriveEquilibrium(chain),prefix=deriveEquilibrium(chain.slice(0,Math.min(240,chain.length)));
 const checks={replay:verifyEquilibrium(chain,a).pass,sourceUnchanged:before===canonical(chain),prefix:prefix.every((r,i)=>canonical(r)===canonical(a[i])),lineage:a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.sourceHash===chain[i].hash),policyCausality:a.every((r,i)=>r.policyParent===(r.epoch===0?null:a[r.epoch*24-1].hash)),policyWithinEpoch:a.every((r,i)=>!i||r.epoch!==a[i-1].epoch||r.levels.every((l,d)=>canonical(l.policy)===canonical(a[i-1].levels[d].policy))),growth:a.every(r=>r.growthFactor===1.025)};
 return {pass:Object.values(checks).every(Boolean),checks,generations:a.length,frames:a.length*3,tip:a.at(-1)?.hash};
}
export function disturbanceSuite(){
 const policy=Object.freeze({target:75,circulation:100,expenditure:100});
 const stages=[["supply",120,100,10,true],["starvation",120,0,10,true],["hold",24,100,10,false],["recovery",120,100,10,true],["saturation",120,1000,0,true]];
 let p=null;const results=[];
 for(const [name,count,offered,requested,enabled] of stages){
 const opening=p?.totalClosing??0;let accepted=0,spent=0,valid=true;
 for(let i=0;i<count;i++){
 const r=equilibriumStep({stability:100},{depth:0,capacity:1000,activeLimit:500,offered,requested,enabled},p,policy);
 accepted+=r.accepted;spent+=r.spent;
 valid=valid&&r.totalClosing>=0&&r.totalClosing<=1000&&r.activeClosing<=500&&r.cumulativeAccepted===r.cumulativeSpent+r.totalClosing&&(enabled||r.accepted+r.transferred+r.spent===0);
 p=r;
 }
 results.push({name,count,opening,accepted,spent,closing:p.totalClosing,pass:valid&&opening+accepted-spent===p.totalClosing&&(name!=="starvation"||accepted===0)&&(name!=="hold"||opening===p.totalClosing)&&(name!=="recovery"||p.totalClosing>opening)&&(name!=="saturation"||p.totalClosing<=750)});
 }
 return {pass:results.every(r=>r.pass),results};
}
export function stressMetabolism(steps=2400){
 if(!Number.isSafeInteger(steps)||steps<1||steps>9600)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 const audit=auditMetabolism(chain),disturbances=disturbanceSuite();return {pass:audit.pass&&disturbances.pass,audit,disturbances};
}
