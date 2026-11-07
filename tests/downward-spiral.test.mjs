import test from "node:test";
import assert from "node:assert/strict";
import {
  SPIRAL_SIGNATURE, spiralCells, gray, ungray, instantiateSpiral,
  encodeVertexOrder, decodeVertexOrder, sealTransport, openTransport
} from "../language/downward-spiral.mjs";

test("literal author's spiral signature stays unchanged", () => {
  assert.equal(SPIRAL_SIGNATURE, "12|8/64/3|2/16/8|/4/2/1/1");
});

test("outer-inward spiral covers rectangular cells once", () => {
  for (const [w,h] of [[1,1],[1,2],[2,1],[2,2],[4,2],[16,16]]) {
    const cells = spiralCells(w,h);
    assert.equal(cells.length,w*h);
    assert.equal(new Set(cells.map(([x,y]) => x+":"+y)).size,w*h);
    assert.deepEqual(cells[0],[0,0]);
  }
  assert.deepEqual(spiralCells(3,3),[[0,0],[1,0],[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[1,1]]);
});

test("Gray encoding is invertible within all supported dimensions", () => {
  for (let d=3;d<=11;d++) for (let i=0;i<2**d;i++) assert.equal(ungray(gray(i)),i);
});

test("all dimensions 3..11 preserve each unique vertex and eight-source globules", () => {
  for (let d=3;d<=11;d++) {
    const s=instantiateSpiral(d),count=2**d;
    assert.equal(s.route.length,count);
    assert.equal(s.globules.length,count/8);
    assert.equal(new Set(s.route).size,count);
    assert.equal(s.width*s.height,count/8);
    assert.equal(new Set(s.globules.map(g=>g.x+":"+g.y)).size,count/8);
    for(let i=0;i<count;i++)assert.equal(s.route[s.inverse[i]],i);
    for(const g of s.globules) {
      assert.equal(g.addresses.length,8);
      assert.equal(g.lineage.length,8);
      assert.deepEqual(g.lineage,g.addresses.map(x=>x.toString(2).padStart(d,"0")));
      for(let j=1;j<8;j++) {
        const delta=g.addresses[j]^g.addresses[j-1];
        assert.equal((delta&(delta-1)),0);
        assert.notEqual(delta,0);
      }
    }
  }
});

test("11D: 2048 vertices / 256 globules / 16×16 grid", () => {
  const s=instantiateSpiral(11);
  assert.equal(s.route.length,2048);
  assert.equal(s.globules.length,256);
  assert.deepEqual([s.width,s.height],[16,16]);
  assert.equal(11*2**10,11264);
});

test("reversible transport round-trips arbitrary ordered records without loss", () => {
  const spiral=instantiateSpiral(11);
  const source=Array.from({length:2048},(_,i)=>({id:i,payload:"source-"+i}));
  const transmitted=encodeVertexOrder(source,spiral);
  assert.deepEqual(decodeVertexOrder(transmitted,spiral),source);
  assert.notDeepEqual(transmitted,source);
});

test("AES-GCM round-trip, independent nonces and Unicode", async () => {
  const password="testing-only-strong-passphrase-🌈";
  const message="QUANTA → 11D ✦ globule 👁 8→4→2→1→1";
  const a=await sealTransport(message,password,11);
  const b=await sealTransport(message,password,11);
  assert.equal(await openTransport(a,password),message);
  assert.equal(await openTransport(b,password),message);
  assert.notEqual(a.nonce,b.nonce);
  assert.notEqual(a.salt,b.salt);
  assert.notEqual(a.ciphertext,b.ciphertext);
});

test("AES-GCM rejects wrong password, changed header and tampered ciphertext", async () => {
  const password="testing-only-strong-passphrase";
  const x=await sealTransport("classified test payload",password,11);
  await assert.rejects(openTransport(x,"incorrect password"));
  await assert.rejects(openTransport({...x,header:{...x.header,dimensions:10}},password));
  await assert.rejects(openTransport({...x,header:{...x.header,signature:"modified"}},password));
  const last=x.ciphertext.at(-1);
  const swapped=last==="A"?"B":"A";
  // Change a middle base64url char to ensure a changed cipher byte.
  const idx=12;
  const changed=x.ciphertext.slice(0,idx)+(x.ciphertext[idx]==="A"?"B":"A")+x.ciphertext.slice(idx+1);
  await assert.rejects(openTransport({...x,ciphertext:changed},password));
});

test("unsupported dimensions are refused", () => {
  for(const bad of [0,2,12,11.5,"11",null]) assert.throws(()=>instantiateSpiral(bad),RangeError);
});

test("AES-GCM actually transports byte blocks through the spiral with reversible padding", async () => {
  const password="another-test-only-long-passphrase";
  for(const [d,message] of [[3,""],[3,"Hello 🌐! repeated enough to span more than eight bytes"],[11,"short"],[11,"x".repeat(2071)]]) {
    const env=await sealTransport(message,password,d);
    const utf8length=new TextEncoder().encode(message).length;
    const n=2**d, blocks=Math.ceil(utf8length/n);
    const raw=Uint8Array.from(atob(env.ciphertext.replace(/-/g,"+").replace(/_/g,"/")),c=>c.charCodeAt(0));
    assert.equal(raw.length,4+blocks*n+16,"expected authenticated padded frame length");
    assert.equal(await openTransport(env,password),message);
  }
});
