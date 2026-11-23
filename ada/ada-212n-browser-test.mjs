// ADA-212N · Chromium verification of write-once sealed epoch receipts across reloads.
import assert from "node:assert/strict";
import {chromium} from "playwright";
const base=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--enable-webgl","--enable-unsafe-swiftshader"]});
const page=await browser.newPage({viewport:{width:1280,height:860},acceptDownloads:true});
const errors=[];page.on("pageerror",e=>errors.push(e.message));
try{
 const r=await page.goto(base+"/ada/ada-212n-epoch-lab.html",{waitUntil:"networkidle",timeout:30000});
 assert.equal(r.status(),200);
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("GENESIS PERSISTED"));
 assert.equal((await page.locator("#count").innerText()).trim(),"1");
 await page.locator("#day").click();assert.equal((await page.locator("#count").innerText()).trim(),"25");
 assert.equal((await page.locator("#sealed").innerText()).trim(),"1");
 const before=await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00000"));
 assert.equal(JSON.parse(before).state,"SEALED");
 assert.equal(await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00001")),null,"OPEN_TAIL is not persisted");
 await page.reload({waitUntil:"networkidle",timeout:30000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("RESTORE PASS"));
 assert.equal((await page.locator("#count").innerText()).trim(),"25");
 await page.locator("#batch").click();assert.equal((await page.locator("#count").innerText()).trim(),"265");
 assert.equal((await page.locator("#sealed").innerText()).trim(),"11");
 assert.equal(await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00000")),before,"SEALED receipt was overwritten");
 await page.locator("#audit").click();assert.match(await page.locator("#status").innerText(),/AUDIT PASS/);
 const canvas=await page.locator("#viz").evaluate(e=>({w:e.width,h:e.height}));
 assert(canvas.w>200&&canvas.h>200);
 await page.evaluate(()=>{const key="ADA-212N.epoch.sealed.00003",v=JSON.parse(localStorage.getItem(key));v.holds+=1;localStorage.setItem(key,JSON.stringify(v))});
 await page.reload({waitUntil:"networkidle",timeout:30000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("ARCHIVE LOCKED"));
 await page.locator("#one").click();assert.match(await page.locator("#status").innerText(),/REJECTED/);
 assert.equal((await page.locator("#count").innerText()).trim(),"1","Corrupted history is not loaded");
 assert.deepEqual(errors,[],"No uncaught browser errors");
 console.log(JSON.stringify({schema:"ADA-212N.browser.v1",pass:true,sealedBefore:1,sealedAfter:11,generations:265,canvas,checks:["reload recovery","sealed permanence","OPEN_TAIL provisional","tamper lock","3D canvas"],errors},null,2));
}finally{await page.close();await browser.close()}
