import test from "node:test";
import assert from "node:assert/strict";
import {
  sendChromeDot, receiveChromeDot, composeChromeFrame, recoverChromeFrame
} from "../language/authenticated-chrome.mjs";
import {sealTransport,openTransport,KDF_ITERATIONS} from "../language/downward-spiral.mjs";
const word="01010110".repeat(16);
const password="example-only-password-for-audit";
test("AUD-01 baseline: valid authenticated transport roundtrip", async()=>{
  const env=await sendChromeDot(word,password,11,"sender-claimed");
  const out=await receiveChromeDot(env,password);
  assert.equal(out.sourceBits,word);
  assert.equal(out.verified,true);
});
test("AUD-02 REPLAY PRESENT: identical ciphertext accepted twice",async()=>{
  const env=await sendChromeDot(word,password,11);
  const one=await receiveChromeDot(env,password);
  const two=await receiveChromeDot(env,password);
  assert.deepEqual(one,two);
});
test("AUD-03 no sender identity proof: same shared passphrase can assert any sourceTag",async()=>{
  const env=await sendChromeDot(word,password,11,"claimed-external-person");
  const out=await receiveChromeDot(env,password);
  assert.equal(out.sourceTag,"claimed-external-person");
  assert.equal(out.verified,true); // authenticated by password, not human identity
});
test("AUD-04 no external source commitment: same terminal+altered witness yields valid different source",()=>{
  const frame=composeChromeFrame(word);
  const altered={
    ...frame,
    fold:{...frame.fold, witness:[
      (frame.fold.witness[0][0]==="0"?"1":"0")+frame.fold.witness[0].slice(1),
      ...frame.fold.witness.slice(1)
    ]}
  };
  const out=recoverChromeFrame(altered);
  assert.notEqual(out.sourceBits,word);
  assert.equal(out.verified,true); // structural validation, not external integrity
});
test("AUD-05 metadata and ciphertext tampering blocked by GCM",async()=>{
  const env=await sendChromeDot(word,password,11);
  for(const x of [
    {...env, header:{...env.header,route:"attacker-route"}},
    {...env, header:{...env.header,iterations:1}},
    {...env, ciphertext:"ABCD"}
  ]) await assert.rejects(receiveChromeDot(x,password));
});
test("AUD-06 12-character weak passphrase accepted: length is not entropy",async()=>{
  const weak="aaaaaaaaaaaa";
  const env=await sealTransport("known plaintext",weak,11);
  assert.equal(await openTransport(env,weak),"known plaintext");
  assert.equal(KDF_ITERATIONS,250000);
});
test("AUD-07 length bucket visible: ciphertext size differs with padded block count",async()=>{
  const small=await sealTransport("a",password,3);
  const big=await sealTransport("a".repeat(64),password,3);
  assert.notEqual(small.ciphertext.length,big.ciphertext.length);
});
test("AUD-08 altered outer chromeProtocol is rejected by parser, but not authenticated as AAD",async()=>{
  const env=await sendChromeDot(word,password,3);
  await assert.rejects(receiveChromeDot({...env,chromeProtocol:"QG-015.2"},password));
});
