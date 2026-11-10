import test from 'node:test';
import assert from 'node:assert/strict';
import {SHAPES,sourceGraph,contractFirstContact,verifyContraction,startSurgeryLedger,appendSurgery,verifySurgeryLedger} from '../language/post-contact-reconstruction.mjs';
test('five permitted outer counts yield contracted planar graphs',()=>{
 for(const n of SHAPES){const x=contractFirstContact(n),v=verifyContraction(x);assert.deepEqual([v.originalV,v.originalE,v.newV,v.newE,v.newF,v.euler],[n+1,2*n,n,2*n-3,n-1,2])}
});
test('exactly one rim-center contact at s=1 for one lobe',()=>{
 for(const n of SHAPES)assert.deepEqual(sourceGraph(n).contact,['C','R0']);
});
test('merge preserves both identities in vertex mapping',()=>{
 const x=contractFirstContact(8);assert.equal(x.vertexMap.C,'C+R0');assert.equal(x.vertexMap.R0,'C+R0');
});
test('one contracted self-loop and two duplicate edges tracked',()=>{
 const x=contractFirstContact(8);
 assert.equal(x.edgeLineage.filter(e=>e.reason==='self-loop removed').length,1);
 assert.equal(x.edgeLineage.filter(e=>e.reason==='parallel edge deduplicated').length,2);
});
test('all source edges appear exactly once in lineage',()=>{
 const x=contractFirstContact(13);
 assert.deepEqual(x.edgeLineage.map(v=>v.source),x.original.edges.map(e=>e.id));
});
test('successor fan has n-2 positive areas',()=>{
 for(const n of SHAPES){const a=contractFirstContact(n).successor.areas;assert.equal(a.length,n-2);assert.ok(a.every(x=>x>0))}
});
test('reject simultaneous multiple contacts rather than silently merging',()=>{
 assert.throws(()=>contractFirstContact(8,2),/Multiple simultaneous/);
});
test('reject invalid n and lobes',()=>{
 assert.throws(()=>contractFirstContact(2));assert.throws(()=>contractFirstContact(5,0));
});
test('tampering with vertex mapping fails',()=>{
 const p=contractFirstContact(8);p.vertexMap.R1='C+R0';assert.throws(()=>verifyContraction(p),/mismatch/);
});
test('tampering with lineage fails',()=>{
 const p=contractFirstContact(8);p.edgeLineage[0].destination='forged';assert.throws(()=>verifyContraction(p),/mismatch/);
});
test('tampering with survivor graph fails',()=>{
 const p=contractFirstContact(5);p.successor.edges.pop();assert.throws(()=>verifyContraction(p),/mismatch/);
});
test('ledger append does not mutate original',()=>{
 const l=startSurgeryLedger(4),before=JSON.stringify(l);const next=appendSurgery(l);
 assert.equal(JSON.stringify(l),before);assert.equal(verifySurgeryLedger(next).events,1);
});
test('ledger rejects missing or tampered historical event',()=>{
 const l=appendSurgery(appendSurgery(startSurgeryLedger(8)));
 l.events.splice(0,1);assert.throws(()=>verifySurgeryLedger(l),/ordering/);
 const m=appendSurgery(startSurgeryLedger(8));m.events[0].certificate.original.edges[0].a='X';
 assert.throws(()=>verifySurgeryLedger(m),/mismatch/);
});
test('original wheel evidence is preserved in contraction certificate',()=>{
 const c=contractFirstContact(3);assert.equal(c.original.vertices.length,4);assert.equal(c.original.edges.length,6);assert.equal(c.successor.boundedFaces,1);
});
