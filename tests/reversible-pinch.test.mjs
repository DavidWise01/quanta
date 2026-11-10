import test from 'node:test';
import assert from 'node:assert/strict';
import {COUNTS,freezePinch,unfoldPinch,examineLoss,verifyFrozen,stripPreimage,startLedger,verifyLedger,appendFold} from '../language/reversible-pinch.mjs';
import {sourceGraph} from '../language/post-contact-reconstruction.mjs';
test('roundtrip restores full source for five rings',()=>{
 for(const n of COUNTS){const p=freezePinch(n);assert.deepEqual(unfoldPinch(p),sourceGraph(n));assert.equal(verifyFrozen(p).roundTrip,true)}
});
test('source and successor cardinality differences tracked',()=>{
 for(const n of COUNTS){const a=examineLoss(freezePinch(n));assert.deepEqual([a.originalVertices,a.successorVertices,a.originalEdges,a.successorEdges],[n+1,n,2*n,2*n-3])}
});
test('every removed/deduplicated edge has retained evidence',()=>{
 const x=examineLoss(freezePinch(8));assert.equal(x.edgeEvents.length,3);
 assert.deepEqual(x.edgeEvents.map(e=>e.reason).sort(),['parallel edge deduplicated','parallel edge deduplicated','self-loop removed']);
});
test('stripped successor has insufficient preimage',()=>{
 const p=freezePinch(8),s=stripPreimage(p);
 assert.equal(s.successor.verticesCount,8);assert.throws(()=>unfoldPinch(s),/Missing reversible/);
});
test('reject lost original vertices',()=>{
 const p=freezePinch(5);delete p.preimage.original;assert.throws(()=>unfoldPinch(p),/Preimage/);
});
test('reject modified original vertex identity',()=>{
 const p=freezePinch(8);p.preimage.original.vertices[0].id='FORGED';assert.throws(()=>unfoldPinch(p),/Preimage/);
});
test('reject modified original edge identity',()=>{
 const p=freezePinch(8);p.contracted.original.edges[0].id='FORGED';assert.throws(()=>unfoldPinch(p));
});
test('reject altered mapping',()=>{
 const p=freezePinch(8);p.preimage.vertexMap.R1='C+R0';assert.throws(()=>unfoldPinch(p),/Preimage/);
});
test('reject altered edge lineage',()=>{
 const p=freezePinch(13);p.contracted.edgeLineage[0].destination='FAKE';assert.throws(()=>unfoldPinch(p));
});
test('reject altered successor',()=>{
 const p=freezePinch(4);p.contracted.successor.verticesCount=100;assert.throws(()=>verifyFrozen(p));
});
test('independent packets do not share mutable evidence',()=>{
 const a=freezePinch(8),b=freezePinch(8);a.preimage.original.vertices[0].id='X';
 assert.equal(verifyFrozen(b).valid,true);
});
test('ledger append does not mutate previous',()=>{
 const a=startLedger(8),before=JSON.stringify(a),b=appendFold(a);
 assert.equal(JSON.stringify(a),before);assert.equal(verifyLedger(b).count,1);
});
test('ledger rejects erased historical event',()=>{
 const a=appendFold(appendFold(startLedger(8)));a.events.shift();assert.throws(()=>verifyLedger(a),/mismatch/);
});
test('ledger rejects modified historical evidence',()=>{
 const a=appendFold(startLedger(8));a.events[0].frozen.preimage.edgeLineage.pop();assert.throws(()=>verifyLedger(a),/mismatch/);
});
test('unsupported multi-contact contraction rejected',()=>assert.throws(()=>freezePinch(8,2),/Multiple simultaneous/));
