// ADA-289N .dlw — actual Chromium acceptance, not a simulated engine.
import {chromium} from "playwright";
import assert from "node:assert/strict";
import fs from "node:fs";
const base=process.env.ADA_TEST_BASE||"http://127.0.0.1:8765";
const manifest=JSON.parse(fs.readFileSync("package/manifest.json","utf8"));
const browser=await chromium.launch({headless:true});
const checks=[];
const url=base+"/ada/ada-288n-adaptive-equilibrium.html";
async function load(page){await page.goto(url);await page.locator("#commit").fill(manifest.source_commit);await page.locator("#load").click();}
async function ready(page){await page.waitForFunction(()=>document.querySelector("#status").textContent.startsWith("READY"),{},{timeout:20000});}
async function report(page){return JSON.parse((await page.locator("#report").textContent()).split(/\n(?:Ledger digest|Recovered records):/)[0]);}
try{
 const context=await browser.newContext();const page=await context.newPage();
 await load(page);await ready(page);
 let r=await report(page);assert.equal(r.generation,0);assert.equal(r.sha256,manifest.sha256);assert.equal(r.vertices,16);assert.equal(r.edges,32);assert.equal(r.pumps.length,3);assert.ok(Math.abs(r.normalizedIntensity-1)<1e-12);checks.push("compiled initialization and geometry");
 for(let g=1;g<=24;g++){await page.locator('[data-step="1"]').click();await page.waitForFunction(n=>{const t=document.querySelector("#report").textContent;return t.includes("Ledger digest:")&&JSON.parse(t.split("\nLedger digest:")[0]).generation===n},g);}
 r=await report(page);assert.equal(r.generation,24);assert.equal(r.epoch,1);assert.ok(r.equilibrium.window>=3&&r.equilibrium.window<=8);const receipt=JSON.parse(await page.locator("#ancestry").textContent());assert.deepEqual(receipt.opening.map(x=>x.generation),[16,17,18,19,20,21,22,23]);checks.push("24 sequential appends and inheritance");
 await load(page);await ready(page);assert.equal((await report(page)).generation,24);assert.deepEqual(JSON.parse(await page.locator("#ancestry").textContent()),receipt);checks.push("persistent reload and identical ancestry");
 await context.close();
 for(const fault of ["missing","corrupt"]){const c=await browser.newContext();const p=await c.newPage();await p.route("**/ada_browser.wasm",async route=>{if(fault==="missing")await route.fulfill({status:404,body:"missing"});else{const res=await route.fetch(),b=await res.body();b[b.length-1]^=1;await route.fulfill({response:res,body:b});}});await load(p);await p.waitForFunction(()=>document.querySelector("#status").textContent.startsWith("HOLD")&&!document.querySelector("#load").disabled);assert.equal(await p.locator('[data-step="1"]').isDisabled(),true);checks.push(fault+" asset rejected");await c.close();}
 console.log(JSON.stringify({status:"PASS",checks,source:manifest.source_commit,sha256:manifest.sha256},null,2));
}finally{await browser.close();}
