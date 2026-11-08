import test from "node:test";
import assert from "node:assert/strict";
import {
  composeChromeFrame, recoverChromeFrame, sendChromeDot, receiveChromeDot
} from "../language/authenticated-chrome.mjs";

const PASSWORD="local-test-only-long-password-2026";
const SOURCE="01011010".repeat(16);
test("QG-015 folds 128 bits into one terminal bit with 127 witness bits",()=>{
  const frame=composeChromeFrame(SOURCE,"witness-A");
  assert.equal(frame.fold.terminal.length,1);
  assert.equal(frame.fold.witness.join("").length,127);
  const recovered=recoverChromeFrame(frame);
  assert.equal(recovered.sourceBits,SOURCE);
  assert.equal(recovered.verified,true);
  assert.deepEqual(recovered.widths,[128,64,32,16,8,4,2,1,1]);
});
test("the complete authenticated transport round-trips across 3D..11D",async()=>{
  for(let d=3;d<=11;d++){
    const envelope=await sendChromeDot(SOURCE,PASSWORD,d,"origin-"+d);
    const decoded=await receiveChromeDot(envelope,PASSWORD);
    assert.equal(decoded.sourceBits,SOURCE);
    assert.equal(decoded.sourceTag,"origin-"+d);
    assert.equal(envelope.header.dimensions,d);
  }
});
test("wrong password and tampered encrypted data are rejected",async()=>{
  const env=await sendChromeDot(SOURCE,PASSWORD,11);
  await assert.rejects(receiveChromeDot(env,"wrong-but-long-password"));
  await assert.rejects(receiveChromeDot({...env,header:{...env.header,dimensions:10}},PASSWORD));
  const i=8,old=env.ciphertext[i];
  await assert.rejects(receiveChromeDot({...env,ciphertext:env.ciphertext.slice(0,i)+(old==="A"?"B":"A")+env.ciphertext.slice(i+1)},PASSWORD));
  await assert.rejects(receiveChromeDot({...env,chromeProtocol:"QG-999"},PASSWORD));
});
test("two sends of the same source create different authenticated envelopes",async()=>{
  const a=await sendChromeDot(SOURCE,PASSWORD,11);
  const b=await sendChromeDot(SOURCE,PASSWORD,11);
  assert.notEqual(a.salt,b.salt);
  assert.notEqual(a.nonce,b.nonce);
  assert.notEqual(a.ciphertext,b.ciphertext);
});
test("frame modification without authentication is not protection",()=>{
  const frame=composeChromeFrame(SOURCE);
  const altered={...frame,fold:{...frame.fold,terminal:frame.fold.terminal==="0"?"1":"0"}};
  assert.notEqual(recoverChromeFrame(altered).sourceBits,SOURCE);
});
test("invalid or malformed sources fail closed",async()=>{
  assert.throws(()=>composeChromeFrame("1010"),TypeError);
  assert.throws(()=>composeChromeFrame(SOURCE,""),TypeError);
  assert.throws(()=>recoverChromeFrame({}),TypeError);
  await assert.rejects(receiveChromeDot({chromeProtocol:"QG-015.1"},PASSWORD));
});
