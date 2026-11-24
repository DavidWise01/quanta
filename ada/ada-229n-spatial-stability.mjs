// ADA-229N .dlw — deterministic spatial stability audit.
import {genesis,advance,canonical} from "./ada-201n-generational-engine.mjs";
import {deriveMorphogenesis,verifyMorphogenesis} from "./ada-228n-morphogenesis.mjs";
export function auditSpatial(chain){
 const before=canonical(chain),a=deriveMorphogenesis(chain);
 const checks={replay:verifyMorphogenesis(chain,a).pass,sourceUnchanged:before===canonical(chain),growth:a.every(s=>s.growthFactor===1.025),lineage:a.every((s,i)=>s.parent===(a[i-1]?.hash??null)&&s.sourceHash===chain[i].hash),causality:a.every((s,i)=>i===0?s.previousSurfaceHash===null:typeof s.previousSurfaceHash==="string"),containment:a.every(s=>s.levels.every(l=>Math.max(...l.center.map(Math.abs))+l.R+l.r<=l.half+1e-8)),nestedBoxes:a.every(s=>s.levels.every((l,i)=>!i||l.center.every((x,j)=>Math.abs(x-s.levels[i-1].center[j])+l.half<=s.levels[i-1].half+1e-8))),volume:a.every(s=>s.levels.every(l=>{const v=2*Math.PI**2*l.R*l.r**2/(2*l.half)**3;return v>0&&v<1})),radius:a.every(s=>s.levels.every(l=>l.R>l.r&&l.r>0)),hold:a.every(s=>s.permit||s.levels.every(l=>l.mean===0&&l.drive.every(d=>d===0))),drive:a.every(s=>s.levels.every(l=>l.drive.every(d=>Math.abs(d)<=1)))};
 return {pass:Object.values(checks).every(Boolean),checks,generations:a.length,frames:a.length*3,minimumNormalizedClearance:Math.min(...a.flatMap(s=>s.levels.map(l=>l.clearance/l.half))),maximumOccupancy:Math.max(...a.flatMap(s=>s.levels.map(l=>2*Math.PI**2*l.R*l.r**2/(2*l.half)**3)))};
}
export function stressSpatial(steps=2400){
 if(!Number.isSafeInteger(steps)||steps<1||steps>9600)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 const result=auditSpatial(chain),prefix=deriveMorphogenesis(chain.slice(0,Math.min(240,chain.length))),full=deriveMorphogenesis(chain);
 result.checks.prefix=prefix.every((s,i)=>canonical(s)===canonical(full[i]));result.pass=Object.values(result.checks).every(Boolean);return result;
}
