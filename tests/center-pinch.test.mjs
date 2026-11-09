import test from 'node:test';
import assert from 'node:assert/strict';
import {FIBONACCI_WALK,SHAPES,initialWheel,inspectWheel,pinchWheel,startPinchLedger,appendPinch,verifyPinchLedger,demoPinch} from '../language/center-pinch.mjs';

test('all five permitted shape sizes begin as planar wheel graphs',()=>{
 for(const n of SHAPES){const x=inspectWheel(initialWheel(n));assert.deepEqual([x.vertices,x.edges,x.faces,x.euler],[n+1,2*n,n+1,2]);}
});
test('Fibonacci observations remain exactly 1 1 2 3 5 8 13',()=>{
 assert.deepEqual(FIBONACCI_WALK,[1,1,2,3,5,8,13]);
});
test('center and ring move under a nonzero pinch',()=>{
 const start=initialWheel(8),end=pinchWheel(start,{dx:0.02,dy:-0.01,strength:0.3,lobes:2});
 assert.notDeepEqual(start.center,end.center);assert.notDeepEqual(start.ring,end.ring);
 assert.equal(inspectWheel(end).euler,2);
});
test('zero action retains geometry exactly',()=>{
 const start=initialWheel(5),end=pinchWheel(start,{dx:0,dy:0,strength:0,lobes:1});
 assert.deepEqual(end,start);
});
test('full prescribed seven-step walk replays across five shapes',()=>{
 for(const n of SHAPES){const l=demoPinch(n);assert.equal(l.events.length,7);const result=verifyPinchLedger(l);assert.equal(result.summary.euler,2);assert.equal(result.summary.crossingFree,true);}
});
test('append creates a new ledger without mutating its parent',()=>{
 const x=startPinchLedger(4),serialized=JSON.stringify(x);
 const y=appendPinch(x,{dx:0.01,dy:0,strength:0.1,lobes:2});
 assert.equal(JSON.stringify(x),serialized);assert.equal(y.events.length,1);
});
test('reject nonexistent polygons and invalid numeric inputs',()=>{
 for(const n of [0,1,2,2.5,65,NaN])assert.throws(()=>initialWheel(n));
});
test('reject over-bounded pinch strength and excessive center offset',()=>{
 const w=initialWheel(8);
 assert.throws(()=>pinchWheel(w,{dx:0,dy:0,strength:0.9,lobes:2}));
 assert.throws(()=>pinchWheel(w,{dx:0.4,dy:0,strength:0.3,lobes:2}));
});
test('reject collapsed face when center lies on outer boundary',()=>{
 const w=initialWheel(4);w.center={...w.ring[0]};
 assert.throws(()=>inspectWheel(w),/Collapsed/);
});
test('reject crossing outer ring geometry',()=>{
 const w=initialWheel(4);[w.ring[1],w.ring[2]]=[w.ring[2],w.ring[1]];
 assert.throws(()=>inspectWheel(w),/Collapsed|cross/);
});
test('reject tampered prior snapshot before append',()=>{
 const l=demoPinch(5);l.events[0].snapshot.ring[0].x+=0.1;
 assert.throws(()=>verifyPinchLedger(l),/mismatch/);
});
test('reject altered action and current state',()=>{
 const l=demoPinch(8);l.events[3].action.strength=0.4;
 assert.throws(()=>verifyPinchLedger(l),/mismatch/);
 const b=demoPinch(8);b.current.center.x+=0.001;
 assert.throws(()=>verifyPinchLedger(b),/mismatch/);
});
test('reject deleted historical event',()=>{
 const l=demoPinch(13);l.events.splice(2,1);
 assert.throws(()=>verifyPinchLedger(l),/Event index/);
});
