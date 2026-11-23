import assert from "node:assert/strict";
import {PHASE_II_FREEZE,genesis,advance,verifyChain} from "./ada-201n-generational-engine.mjs";
import {geometryStress,verifyGeometryStress,project3D} from "./ada-208n-geometry-stress.mjs";
const chain=advance([genesis()],240),original=JSON.stringify(chain);
const config={capacity:24,width:960,height:540,az:.4,el:.37,zoom:6};
const snapshot=geometryStress(chain,config);
assert.equal(snapshot.generations,241);
assert.equal(snapshot.sourceRoot,PHASE_II_FREEZE);
assert.equal(snapshot.active,24);assert.equal(snapshot.archived,217);
assert.equal(snapshot.samples.length,24);assert.equal(snapshot.samples[0].n,217);assert.equal(snapshot.samples.at(-1).n,240);
assert.equal(snapshot.growthSteps+snapshot.holds,240);
assert(snapshot.maxStep<=.0250001);assert(snapshot.maxPolicy<=.2500001);
assert(snapshot.samples.every(p=>[p.x,p.y,p.depth].every(Number.isFinite)));
assert.equal(verifyGeometryStress(chain,snapshot,config).pass,true);
assert.deepEqual(geometryStress(chain,config),snapshot,"Bit-identical projection replay");
assert.equal(JSON.stringify(chain),original,"No mutation of frozen ancestry");
const altered=structuredClone(snapshot);altered.samples[0].x+=1;
assert.equal(verifyGeometryStress(chain,altered,config).pass,false);
for(const capacity of [1,8,24,64,256]){
 const cfg={...config,capacity},view=geometryStress(chain,cfg);
 assert.equal(view.active,Math.min(capacity,chain.length));
 assert.equal(view.archived,chain.length-view.active);
 assert(verifyGeometryStress(chain,view,cfg).pass);
}
for(const az of [-3.14,-1,0,1,3.14])for(const el of [-1.2,0,1.2]){
 const p=project3D({x:1.5,y:.25,z:-.5},az,el,10,960,540);
 assert([p.x,p.y,p.depth].every(Number.isFinite));
}
assert.throws(()=>project3D({x:1,y:0,z:0},0,0,0,960,540),/Invalid projection/);
assert.throws(()=>geometryStress(chain,{...config,capacity:257}),/Invalid active capacity/);
const corrupted=structuredClone(chain);corrupted[23].energy=0;
assert.throws(()=>geometryStress(corrupted,config),/Ancestry invalid/);
assert(verifyChain(chain).pass);
console.log(JSON.stringify({schema:"ADA-208N.test.v1",pass:true,generations:snapshot.generations,active:snapshot.active,archived:snapshot.archived,
 holds:snapshot.holds,growthSteps:snapshot.growthSteps,growthSize:snapshot.growthSize,policy:snapshot.mutationPolicy,
 geometryHash:snapshot.hash,checks:["240 transitions","24 active/217 archived","multiple 3D rotations","capacity 1..256","growth HOLD accounting","mutation limits","deterministic geometry replay","altered geometry rejection","immutable ancestry"]},null,2));
