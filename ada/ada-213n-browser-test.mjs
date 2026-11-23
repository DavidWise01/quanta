// ADA-213N · Chromium epoch ancestry and persisted receipt trace acceptance.
import assert from "node:assert/strict";
import {chromium} from "playwright";
const base=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--enable-webgl","--enable-unsafe-swiftshader"]});
const page=await browser.newPage({viewport:{width:1280,height:860},acceptDownloads:true});
const errors=[];page.on("pageerror",e=>errors.push(e.message));
try{
 const r=await page.goto(base+"/ada/ada-213n-epoch-lab.html",{waitUntil:"networkidle",timeout:30000});
 assert.equal(r.status(),200);
 await page.waitForFunction(()=>/GENESIS PERSISTED|RESTORE PASS/.test(document.querySelector("#status")?.textContent||""));
 await page.locator("#batch").click();
 assert.equal((await page.locator("#count").innerText()).trim(),"241");
 await page.locator("#epochInput").fill("9");
 await page.locator("#trace").click();
 assert.match(await page.locator("#traceState").innerText(),/EPOCH TRACE PASS.*epoch 9.*SEALED.*24 source generations.*1 source root.*SEALED RECEIPT/);
 assert.equal(await page.locator("#traceRows tr").count(),10);
 await page.locator("#epochInput").fill("10");
 await page.locator("#trace").click();
 assert.match(await page.locator("#traceState").innerText(),/EPOCH TRACE PASS.*epoch 10.*OPEN_TAIL.*1 source generations.*PROVISIONAL TAIL/);
 assert.equal(await page.locator("#traceRows tr").count(),11);
 assert.equal(await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00010")),null);
 const downloadPromise=page.waitForEvent("download");await page.locator("#proofExport").click();const file=await downloadPromise;
 assert.match(file.suggestedFilename(),/ada-213n-provenance-epoch-10\.json/);
 assert.match(await page.locator("#traceState").innerText(),/PROVENANCE EXPORTED/);
 await page.reload({waitUntil:"networkidle",timeout:30000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("RESTORE PASS"));
 assert.equal((await page.locator("#count").innerText()).trim(),"241");
 await page.locator("#epochInput").fill("9");await page.locator("#trace").click();
 assert.match(await page.locator("#traceState").innerText(),/EPOCH TRACE PASS/);
 await page.evaluate(()=>{const key="ADA-212N.epoch.sealed.00009";const r=JSON.parse(localStorage.getItem(key));r.holds+=1;localStorage.setItem(key,JSON.stringify(r))});
 await page.reload({waitUntil:"networkidle",timeout:30000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("ARCHIVE LOCKED"));
 await page.locator("#epochInput").fill("0");await page.locator("#trace").click();
 assert.match(await page.locator("#traceState").innerText(),/TRACE REJECTED/);
 await page.locator("#one").click();assert.match(await page.locator("#status").innerText(),/REJECTED/);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({schema:"ADA-213N.browser.v1",pass:true,sourceGenerations:241,sealedTraced:9,provisionalTail:10,reload:true,tamperLock:true,errors},null,2));
}finally{await page.close();await browser.close()}
