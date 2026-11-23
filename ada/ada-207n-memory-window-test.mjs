import assert from "node:assert/strict";
import {PHASE_II_FREEZE,genesis,advance,verifyChain} from "./ada-201n-generational-engine.mjs";
import {deriveMemory,verifyMemory,memoryProof,DEFAULT_CAPACITY} from "./ada-207n-memory-window.mjs";
const chain=advance([genesis()],120),ancestorBytes=JSON.stringify(chain),memory=deriveMemory(chain);
assert.equal(DEFAULT_CAPACITY,24);assert.equal(memory.capacity,24);assert.equal(memory.window.length,24);
assert.equal(memory.archivedCount,97);assert.equal(memory.window[0].n,97);assert.equal(memory.window.at(-1).n,120);
assert.equal(memory.firstActiveParent,chain[96].hash);assert.equal(memory.sourceTip,chain[120].hash);
assert.equal(memory.root,PHASE_II_FREEZE);assert(verifyMemory(chain,memory).pass);
assert.deepEqual(deriveMemory(chain),memory,"Deterministic working memory replay");
assert.equal(JSON.stringify(chain),ancestorBytes,"Compaction must never mutate archive");
assert(Object.isFrozen(memory)&&Object.isFrozen(memory.window)&&memory.window.every(Object.isFrozen));
for(const capacity of [1,8,24,64,256]){
 const frame=deriveMemory(chain,capacity);
 assert.equal(frame.window.length,Math.min(capacity,chain.length));
 assert.equal(frame.archivedCount,chain.length-frame.window.length);
 assert(verifyMemory(chain,frame).pass);
}
assert.equal(deriveMemory([genesis()]).archivedCount,0);
assert.throws(()=>deriveMemory(chain,0),/Capacity/);assert.throws(()=>deriveMemory(chain,257),/Capacity/);
const changed=structuredClone(memory);changed.window[0].signal+=1;
assert.equal(verifyMemory(chain,changed).pass,false,"Altered memory must be rejected");
const proof=memoryProof(chain,24);assert.equal(proof.root,PHASE_II_FREEZE);
assert.equal(proof.firstActiveParent,chain[96].hash);
const broken=structuredClone(chain);broken[13].energy=0;
assert.throws(()=>deriveMemory(broken),/Invalid inherited chain/);
assert(verifyChain(chain).pass);
console.log(JSON.stringify({schema:"ADA-207N.test.v1",pass:true,generations:chain.length,active:memory.window.length,archived:memory.archivedCount,checks:["24-slot working view","97 archived generations retained","immutable parent pointer","deterministic replay","capacity bounds","no source mutation","tamper rejection","source-root identity","memory proof"]},null,2));
