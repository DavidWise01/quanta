// ADA-208N · Generational geometry and inherited-state stress.
// A deterministic projected 3D test surface; it does not assert a physical optical processor.
import {PHASE_II_FREEZE,canonical,fnv64,verifyChain} from "./ada-201n-generational-engine.mjs";
import {deriveContacts} from "./ada-204n-three-contact-inheritance.mjs";
import {deriveGrowth} from "./ada-205n-homeostatic-growth.mjs";
import {deriveMutations,STEP_LIMIT,TOTAL_LIMIT} from "./ada-206n-bounded-mutation.mjs";
import {deriveMemory,MAX_CAPACITY} from "./ada-207n-memory-window.mjs";
export const STRESS_SCHEMA="ADA-208N.geometry-stress.v1";
export const project3D=({x,y,z},az,el,zoom,width,height)=>{
 if(![x,y,z,az,el,zoom,width,height].every(Number.isFinite)||zoom<=0||width<=0||height<=0)throw Error("Invalid projection parameters");
 const rx=x*Math.cos(az)-z*Math.sin(az),rz=x*Math.sin(az)+z*Math.cos(az);
 const ry=y*Math.cos(el)-rz*Math.sin(el),depth=y*Math.sin(el)+rz*Math.cos(el);
 if(zoom+depth<=0.1)throw Error("Projection behind camera");
 const k=Math.min(width,height)*1.2/(zoom+depth);
 return Object.freeze({x:Number((width/2+rx*k).toFixed(5)),y:Number((height/2-ry*k).toFixed(5)),depth:Number(depth.toFixed(5))});
};
export function geometryStress(chain,{capacity=24,width=960,height=540,az=0.4,el=0.37,zoom=6}={}){
 const audit=verifyChain(chain);if(!audit.pass)throw Error("Ancestry invalid: "+audit.reason);
 if(!Number.isSafeInteger(capacity)||capacity<1||capacity>MAX_CAPACITY)throw Error("Invalid active capacity");
 const contacts=deriveContacts(chain),growth=deriveGrowth(chain),mutations=deriveMutations(chain),memory=deriveMemory(chain,capacity);
 const samples=memory.window.map((item,i)=>{
  const n=item.n,gen=chain[n],angle=n*.37,rad=1.5+(gen.signal-50)*.012;
  const p=project3D({x:rad*Math.cos(angle),y:(gen.stability-95)*.035,z:rad*Math.sin(angle)},az,el,zoom,width,height);
  return Object.freeze({n,x:p.x,y:p.y,depth:p.depth,hash:gen.hash,decision:gen.decision});
 });
 if(samples.some(p=>![p.x,p.y,p.depth].every(Number.isFinite)))throw Error("Nonfinite geometry");
 const holds=contacts.filter(x=>x.decision==="HOLD").length;
 const growthSteps=growth.at(-1).growthSteps;
 if(growthSteps+holds!==chain.length-1)throw Error("HOLD/APPEND accounting mismatch");
 const maxStep=Math.max(...mutations.map(x=>Math.abs(x.applied)));
 const maxPolicy=Math.max(...mutations.map(x=>Math.abs(x.policy)));
 if(maxStep>STEP_LIMIT+1e-7||maxPolicy>TOTAL_LIMIT+1e-7)throw Error("Mutation bound violation");
 if(memory.sourceTip!==chain.at(-1).hash)throw Error("Memory/source tip mismatch");
 const content={schema:STRESS_SCHEMA,sourceRoot:PHASE_II_FREEZE,generations:chain.length,capacity,archived:memory.archivedCount,active:memory.window.length,holds,growthSteps,
  growthSize:growth.at(-1).size,mutationPolicy:mutations.at(-1).policy,maxStep,maxPolicy,sourceTip:chain.at(-1).hash,
  contactTip:contacts.at(-1).hash,growthTip:growth.at(-1).hash,mutationTip:mutations.at(-1).hash,memoryHash:memory.hash,viewport:{width,height,az,el,zoom},
  samples:Object.freeze(samples)};
 return Object.freeze({...content,hash:fnv64(canonical(content))});
}
export function verifyGeometryStress(chain,snapshot,config={}){
 try{const actual=geometryStress(chain,config);return canonical(actual)===canonical(snapshot)?{pass:true,hash:actual.hash,generations:actual.generations,holds:actual.holds,active:actual.active}:{pass:false,reason:"Projected stress snapshot mismatch"}}
 catch(error){return {pass:false,reason:error.message}}
}
