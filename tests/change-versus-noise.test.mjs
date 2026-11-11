import test from 'node:test';import assert from 'node:assert/strict';
import {DEFAULT,start,append,verify,run,demo,checkpoint} from '../language/change-versus-noise.mjs';
test('initial ledger starts without assumptions of observations',()=>{const x=start();assert.equal(x.events.length,0);assert.equal(x.status,'baseline')});
test('fixed 20 observations freeze baseline at monitor boundary',()=>{const x=run(Array(20).fill(0));assert.equal(x.status,'monitoring');assert.equal(x.baselineCount,20)});
test('incomplete monitor cannot trigger alert',()=>{const x=run(Array(39).fill(0));assert.equal(x.checkpoints.length,0);assert.equal(x.monitorCount,19)});
test('fixed extreme shift raises investigate alert',()=>{const x=demo('shift');assert.equal(x.status,'review');assert.equal(x.checkpoints[0].alert,true)});
test('stationary identical samples do not alert',()=>{const x=demo('stable');assert.equal(x.status,'monitoring');assert.equal(x.checkpoints[0].alert,false)});
test('positive and negative shift are screened symmetrically',()=>{
 const a=run([...Array(20).fill(1),...Array(20).fill(0)]);
 assert.equal(a.status,'review');assert.equal(a.checkpoints[0].delta,-1);
});
test('alpha spending first batch equals half total alpha',()=>{const c=demo('stable').checkpoints[0];assert.equal(c.allocatedAlpha,.025)});
test('second batch receives alpha/6',()=>{
 const x=run(Array(60).fill(0));assert.equal(x.checkpoints.length,2);
 assert.ok(Math.abs(x.checkpoints[1].allocatedAlpha-.05/6)<1e-14);
});
test('second repeated screen uses stricter threshold',()=>{
 const x=run(Array(60).fill(0));assert.ok(x.checkpoints[1].threshold>x.checkpoints[0].threshold);
});
test('threshold smaller than one for canonical fixed windows',()=>assert.ok(demo('stable').checkpoints[0].threshold<1));
test('no false claim that zero alerts means stationary process',()=>assert.equal(demo('stable').checkpoints[0].interpretation,'no_detected_shift'));
test('one alert stops further appending',()=>assert.throws(()=>append(demo('shift'),0),/stopping/));
test('stable stream can append subsequent monitoring batches',()=>assert.equal(run(Array(60).fill(0)).checkpoints.length,2));
test('replay succeeds for both fixtures',()=>{for(const x of [demo('stable'),demo('shift')])assert.equal(verify(x).valid,true)});
test('append retains original evidence immutable by value',()=>{const x=start(),s=JSON.stringify(x);append(x,0);assert.equal(JSON.stringify(x),s)});
test('reject altered historical observation',()=>{const x=demo('shift');x.events[0].outcome=1;assert.throws(()=>verify(x),/snapshot/)});
test('reject altered checkpoint threshold',()=>{const x=demo('shift');x.checkpoints[0].threshold=0;assert.throws(()=>verify(x),/replay/)});
test('reject altered event order',()=>{const x=demo('stable');x.events[0].index=5;assert.throws(()=>verify(x),/index/)});
test('reject altered snapshot',()=>{const x=demo('stable');x.events[0].snapshot.baselineCount=4;assert.throws(()=>verify(x),/snapshot/)});
test('reject tampered status',()=>{const x=demo('stable');x.status='review';assert.throws(()=>verify(x),/replay/)});
test('reject nonbinary observation',()=>assert.throws(()=>append(start(),.5),/0 or 1/));
test('reject invalid alpha',()=>assert.throws(()=>start({alpha:1})));
test('reject tiny windows below validity bound',()=>assert.throws(()=>start({baselineSize:3})));
test('checkpoint finite results and valid direction',()=>{
 const c=checkpoint(Array(20).fill(0),Array(20).fill(1),.05,1);
 assert.equal(c.delta,1);assert.equal(c.interpretation,'investigate_shift');
});
test('fixed non-extreme difference need not alert',()=>{
 const x=run([...Array(20).fill(0),...Array(12).fill(1),...Array(8).fill(0)]);
 assert.equal(x.checkpoints[0].alert,false);
});
test('baseline remains retained in event provenance',()=>{
 const x=demo('shift');assert.deepEqual(x.events.slice(0,20).map(e=>e.outcome),Array(20).fill(0));
});
