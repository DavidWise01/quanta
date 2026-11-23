// ADA-201N · real Chromium control and rendering smoke test.
import {chromium} from "playwright";
import assert from "node:assert/strict";
const base=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--enable-webgl","--enable-unsafe-swiftshader"]});
const page=await browser.newPage({viewport:{width:1280,height:850},acceptDownloads:true});
const errors=[];page.on("pageerror",e=>errors.push(e.message));
try{
 const response=await page.goto(base+"/ada/ada-201n-generational-lab.html",{waitUntil:"networkidle",timeout:25000});
 assert.equal(response.status(),200);
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("GENESIS VERIFIED"));
 assert.equal((await page.locator("#gen").innerText()).trim(),"0");
 await page.locator("#plusOne").click();assert.equal((await page.locator("#gen").innerText()).trim(),"1");
 await page.locator("#plusFive").click();assert.equal((await page.locator("#gen").innerText()).trim(),"6");
 await page.locator("#nInput").fill("13");await page.locator("#plusN").click();assert.equal((await page.locator("#gen").innerText()).trim(),"19");
 await page.locator("#verify").click();assert.match(await page.locator("#status").innerText(),/REPLAY PASS/);
 await page.reload({waitUntil:"networkidle",timeout:25000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("RESTORE PASS"));
 assert.equal((await page.locator("#gen").innerText()).trim(),"19","Generations must survive browser reload");
 assert.match(await page.locator("#storageState").innerText(),/19?\d? write-once records|20 write-once records/);
 const parent=await page.locator("#rootHash").innerText();assert.match(parent,/^[0-9a-f]+…$/);
 const size=await page.locator("#scene").evaluate(e=>({w:e.width,h:e.height}));assert(size.w>300&&size.h>250);
 await page.locator("#reset").click();assert.match(await page.locator("#status").innerText(),/GENESIS PASS/);
 assert.equal((await page.locator("#gen").innerText()).trim(),"19","Genesis audit must never delete history");
 await page.locator("#nInput").fill("0");await page.locator("#plusN").click();assert.match(await page.locator("#status").innerText(),/REJECTED/);
 assert.equal((await page.locator("#gen").innerText()).trim(),"19");
 const downloadPromise=page.waitForEvent("download");await page.locator("#export").click();const download=await downloadPromise;assert.match(download.suggestedFilename(),/ada-201n-generations-19\.json/);
 await page.evaluate(()=>{const key="ADA-202N.journal.entry.00003";const node=JSON.parse(localStorage.getItem(key));node.signal+=1;localStorage.setItem(key,JSON.stringify(node))});
 await page.reload({waitUntil:"networkidle",timeout:25000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("ARCHIVE LOCKED"));
 await page.locator("#plusOne").click();
 assert.match(await page.locator("#status").innerText(),/REJECTED/,"Tampered ancestry blocks appends");
 assert.equal((await page.locator("#gen").innerText()).trim(),"0","No tampered generation is loaded");
 assert.deepEqual(errors,[],"No uncaught browser errors");
 console.log(JSON.stringify({schema:"ADA-201N.browser.v1",pass:true,n:19,render:size,controls:["genesis","+1","+5","+n","replay","reload restore","audit","reject-invalid","export","tamper lock"],errors},null,2));
}catch(e){console.error("ADA-201N browser verification failed",e.message,"errors",errors);throw e}finally{await page.close();await browser.close()}
