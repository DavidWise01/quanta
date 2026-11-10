import test from 'node:test';import assert from 'node:assert/strict';
import {measure} from '../language/observation-sufficiency.mjs';
import {chooseObservation,startBound,appendBound,verifyBound,runBound} from '../language/no-wasted-movement.mjs';
test('ambiguous 5/8 pair chooses phase at same position',()=>{
 const l=startBound(5),choice=chooseObservation(l.observations,l.index,{movementCost:.25});
 assert.equal(choice.kind,'stay');assert.equal(choice.step,1);assert.equal(choice.channel,'phase');assert.equal(choice.gain,1);
});
test('second observation stays at position 1',()=>{
 const l=appendBound(startBound(5),5);assert.equal(l.observations[1].step,1);assert.deepEqual(l.remaining,[5]);assert.equal(l.index,1);
});
test('repeated amplitude is never chosen over informative phase',()=>{
 const l=startBound(8);const c=chooseObservation(l.observations,0,{movementCost:0});assert.equal(c.channel,'phase');
});
test('identify all eight roots without unnecessary movement',()=>{
 for(let r=1;r<=8;r++){const l=runBound(r);assert.deepEqual(l.remaining,[r]);assert.ok(l.decisions.length<=1)}
});
test('no further measurement after identification',()=>{
 const l=appendBound(startBound(5),5);assert.equal(chooseObservation(l.observations,l.index).kind,'stop');
});
test('already known singleton stops at once',()=>assert.equal(chooseObservation(startBound(1).observations,0).kind,'stop'));
test('without phase sensor, preserve ambiguity at the first vertex',()=>{
 const l=startBound(5,{allowPhase:false,movementCost:10});
 assert.equal(chooseObservation(l.observations,0,{allowPhase:false,movementCost:10}).kind,'stop');
});
test('moving to second identical 1 gives no new amplitude information',()=>{
 const l=startBound(5,{allowPhase:false,movementCost:0});
 assert.equal(chooseObservation(l.observations,0,{allowPhase:false,movementCost:0}).kind,'stop');
});
test('expected gain forecast is not falsely recorded as observed gain',()=>{
 const l=appendBound(startBound(5),5);assert.equal(l.decisions[0].expectedGain,1);assert.equal(l.remaining.length,1);
});
test('ledger replay succeeds',()=>{for(let r=1;r<=8;r++)assert.equal(verifyBound(runBound(r)).valid,true)});
test('historical event is append-by-value',()=>{const old=startBound(5),snap=JSON.stringify(old);appendBound(old,5);assert.equal(JSON.stringify(old),snap)});
test('reject altered candidate list',()=>{const l=appendBound(startBound(5),5);l.remaining=[5,8];assert.throws(()=>verifyBound(l),/mismatch/)});
test('reject fabricated decision',()=>{const l=appendBound(startBound(5),5);l.decisions[0].kind='move';assert.throws(()=>verifyBound(l),/mismatch/)});
test('reject fabricated measurement',()=>{const l=appendBound(startBound(5),5);l.decisions[0].observation.value=0;assert.throws(()=>verifyBound(l))});
test('reject unsupported index',()=>assert.throws(()=>chooseObservation([],8)));
test('reject negative movement cost',()=>assert.throws(()=>chooseObservation([],0,{movementCost:-1})));
test('reject contradictory prior',()=>assert.throws(()=>chooseObservation([{step:1,channel:'amplitude',value:-1}],0)));
