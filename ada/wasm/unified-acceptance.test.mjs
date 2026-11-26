// ADA-319N .dlw — acceptance of actual unified laboratory against staged release.
import {chromium} from "playwright";
import assert from "node:assert/strict";
import fs from "node:fs";
const m=JSON.parse(fs.readFileSync("package/manifest.json","utf8"));
const browser=await chromium.launch({headless:true});
const base=process.env.ADA_TEST_BASE||"http://127.0.0.1:8765";
const url=base+"/ada/ada-318n-unified-dimensions.html";
const checks=[];
async function load(p){await p.goto(url);await p.locator("#commit").fill(m.source_commit);await p.locator("#load").click();}
async function ready(p){await p.waitForFunction(()=>document.querySelector("#status").textContent.startsWith("READY"));}
async function report(p){return JSON.parse((await p.locator("#report").textContent()).split(/\n(?:Ledger digest|Recovered records|Full audit):/)[0]);}
try{
 const c=await browser.newContext(),p=await c.newPage();
 await load(p);await ready(p);
 let r=await report(p);assert.equal(r.generation,0);assert.equal(r.sha256,m.sha256);assert.equal(r.vertices,16);assert.equal(r.edges,32);assert.equal(r.pumps.length,3);assert.ok(Math.abs(r.normalizedIntensity-1)<1e-12);checks.push("native unified geometry");
 for(let g=1;g<=24;g++){await p.locator('[data-step="1"]').click();await p.waitForFunction(n=>{const t=document.querySelector("#report").textContent;return t.includes("Ledger digest:")&&JSON.parse(t.split("\nLedger digest:")[0]).generation===n},g);}
 r=await report(p);assert.equal(r.epoch,1);assert.match(await p.locator("#temporal").textContent(),/Generation 24 · completed epochs 1 · slot 0\/23/);const ancestry=JSON.parse(await p.locator("#ancestry").textContent());assert.deepEqual(ancestry.opening.map(x=>x.generation),[16,17,18,19,20,21,22,23]);checks.push("committed epoch and inherited context");
 await load(p);await ready(p);assert.equal((await report(p)).generation,24);assert.deepEqual(JSON.parse(await p.locator("#ancestry").textContent()),ancestry);
 await p.locator("#audit").click();await p.waitForFunction(()=>document.querySelector("#report").textContent.includes("Full audit: 25 records verified"));checks.push("reload and full audit");await c.close();
 for(const fault of ["missing","binding","binary"]){
  const c=await browser.newContext(),p=await c.newPage();
  if(fault==="missing")await p.route("**/ledger-abort.json",r=>r.fulfill({status:404,body:"missing"}));
  if(fault==="binding")await p.route("**/ledger-contention.json",async r=>{const res=await r.fetch(),j=await res.json();j.binding.source="0".repeat(40);await r.fulfill({response:res,json:j});});
  if(fault==="binary")await p.route("**/ada_browser.wasm",async r=>{const res=await r.fetch(),b=await res.body();b[b.length-1]^=1;await r.fulfill({response:res,body:b});});
  await load(p);await p.waitForFunction(()=>document.querySelector("#status").textContent.startsWith("HOLD")&&!document.querySelector("#load").disabled);
  assert.equal(await p.locator('[data-step="1"]').isDisabled(),true);assert.equal(await p.locator("#temporal").textContent(),"HOLD");checks.push(fault+" rejected");await c.close();
 }
 console.log(JSON.stringify({status:"PASS",source:m.source_commit,sha256:m.sha256,checks}));
}finally{await browser.close();}
