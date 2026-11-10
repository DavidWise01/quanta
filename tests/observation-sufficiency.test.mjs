import test from 'node:test';
import assert from 'node:assert/strict';
import {ROOTS} from '../language/ambiguous-roots.mjs';
import {WALK,RING_SIZE,measure,compatible,allowedSchedule,runBlind,verifyBlind,minimalWithinAllowed,completeAudit} from '../language/observation-sufficiency.mjs';
test('walk is exactly seven Fibonacci checkpoints',()=>assert.deepEqual(WALK,[1,1,2,3,5,8,13]));
test('repeat step one uses phase without moving',()=>assert.deepEqual(allowedSchedule().slice(0,2),[{step:1,channel:'amplitude'},{step:1,channel:'phase'}]));
test('zero observations cannot identify one of eight roots',()=>assert.equal(compatible([]).length,8));
test('at vertex one, roots 5 and 8 alias in amplitude',()=>assert.deepEqual(minimalWithinAllowed(5).firstAmplitude,[5,8]));
test('at vertex one, roots 6 and 7 alias in amplitude',()=>assert.deepEqual(minimalWithinAllowed(6).firstAmplitude,[6,7]));
test('all amplitude-only samples on thirteen vertices retain both aliases',()=>{
 for(const [a,b] of [[5,8],[6,7]]){const x=minimalWithinAllowed(a);assert.deepEqual(x.allAmplitude,[a,b])}
});
test('phase at same vertex resolves root 5 versus 8',()=>assert.deepEqual(minimalWithinAllowed(5).withPhase,[5]));
test('phase at same vertex resolves root 6 versus 7',()=>assert.deepEqual(minimalWithinAllowed(7).withPhase,[7]));
test('all eight candidate roots uniquely identifiable by two-channel observations',()=>{
 const audit=completeAudit();assert.equal(audit.audits.length,8);
 for(const a of audit.audits)assert.deepEqual(a.withPhase,[a.root]);
});
test('some roots are unique after only one amplitude measurement',()=>assert.equal(minimalWithinAllowed(1).earliestUnderSchedule,1));
test('ambiguous roots require the repeated-position phase measurement',()=>assert.equal(minimalWithinAllowed(8).earliestUnderSchedule,2));
test('blind replay preserves all candidates until evidence separates them',()=>{
 const r=runBlind(5);assert.deepEqual(r.snapshots[0].remaining,[5,8]);assert.deepEqual(r.snapshots[1].remaining,[5]);
 assert.equal(verifyBlind(r).firstUnique,2);
});
test('all eight blind experiments replay exactly',()=>{for(const root of ROOTS){const r=runBlind(root);assert.deepEqual(verifyBlind(r).remaining,[root])}});
test('detect measurement tampering',()=>{const r=runBlind(5);r.observations[1].value=.25;assert.throws(()=>verifyBlind(r))});
test('detect hidden extra movement',()=>{const r=runBlind(5);r.schedule[1].step=2;assert.throws(()=>verifyBlind(r),/Noncanonical/)});
test('detect candidate rewriting',()=>{const r=runBlind(5);r.snapshots[0].remaining=[5];assert.throws(()=>verifyBlind(r),/replay/)});
test('reject unsupported channel',()=>assert.throws(()=>measure(1,1,'hardware')));
test('reject unsupported step',()=>assert.throws(()=>measure(1,4,'amplitude')));
