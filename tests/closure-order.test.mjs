import test from 'node:test';
import assert from 'node:assert/strict';
import {CANONICAL,analyzeClosure,foldClosure,unfoldClosure,compareClosures} from '../language/closure-order.mjs';
test('canonical interleaved enclosure crosses once',()=>{
 const a=analyzeClosure(CANONICAL); assert.equal(a.crossings.length,1);
 assert.deepEqual(a.closeOrder,['box','fold']); assert.equal(a.vertices.length,2);
});
test('nested syntax has no crossing and opposite closure order',()=>{
 const a=analyzeClosure('.[(.)]'); assert.equal(a.crossings.length,0);
 assert.deepEqual(a.closeOrder,['fold','box']);
});
test('same characters do not imply same structure',()=>{
 const x=compareClosures('.[(.])','.[(.)]');
 assert.equal(x.sameMarks,true);assert.equal(x.sameSignature,false);
 assert.equal(x.firstCrossings,1);assert.equal(x.secondCrossings,0);
});
test('exact byte round-trip including spaces',()=>{
 for(const s of [CANONICAL,'.[(.)]','[ ( . ] )','.(.)','.[.]','', '   '])
   assert.equal(unfoldClosure(foldClosure(s)),s);
});
test('sequential boundaries have no crossing',()=>{
 const a=analyzeClosure('[.](.)');assert.equal(a.crossings.length,0);
});
test('multiple crossings counted deterministically',()=>{
 const a=analyzeClosure('[(][)]');assert.equal(a.crossings.length,2);
});
test('unmatched closer rejected',()=>assert.throws(()=>analyzeClosure('].'),/Unmatched/));
test('unclosed opener rejected',()=>assert.throws(()=>analyzeClosure('[(.'),/Unclosed/));
test('unknown token rejected',()=>assert.throws(()=>analyzeClosure('[*.]'),/Unknown/));
test('tampered closure order rejected',()=>{
 const p=foldClosure(CANONICAL);p.closeOrder.reverse();
 assert.throws(()=>unfoldClosure(p),/mismatch/);
});
test('tampered pairing rejected',()=>{
 const p=foldClosure(CANONICAL);p.intervals[0].close++;
 assert.throws(()=>unfoldClosure(p),/mismatch/);
});
test('tampered original rejected',()=>{
 const p=foldClosure(CANONICAL);p.original='.[(.)]';
 assert.throws(()=>unfoldClosure(p),/mismatch/);
});
test('original preserved as immutable value, not external object reference',()=>{
 const p=foldClosure(CANONICAL); const next={...p,tokens:p.tokens.map(t=>({...t}))};
 next.tokens[0].glyph='[';assert.equal(unfoldClosure(p),CANONICAL);
 assert.throws(()=>unfoldClosure(next),/mismatch/);
});
