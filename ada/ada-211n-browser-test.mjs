// ADA-211N · browser-level test of epoch buttons, ring canvas and immutable lineage.
import assert from "node:assert/strict";
import {chromium} from "playwright";
const base=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--enable-webgl","--enable-unsafe-swiftshader"]});
const page=await browser.newPage({viewport:{width:1280,height:860},acceptDownloads:true});
const errors=[];page.on("pageerror",e=>errors.push(e.message));
try{
 const r=await page.goto(base+"/ada/ada-211n-epoch-lab.html",{waitUntil:"networkidle",timeout:30000});
 assert.equal(r.status(),200);
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("GENESIS VERIFIED"));
 assert.equal((await page.locator("#count").innerText()).trim(),"1");
 await page.locator("#one").click();assert.equal((await page.locator("#count").innerText()).trim(),"2");
 await page.locator("#day").click();assert.equal((await page.locator("#count").innerText()).trim(),"26");
 assert.equal((await page.locator("#epochCount").innerText()).trim(),"2");
 assert.equal((await page.locator("#sealed").innerText()).trim(),"1");
 await page.locator("#batch").click();assert.equal((await page.locator("#count").innerText()).trim(),"266");
 assert.equal((await page.locator("#epochCount").innerText()).trim(),"12");
 assert.equal((await page.locator("#sealed").innerText()).trim(),"11");
 await page.locator("#audit").click();assert.match(await page.locator("#status").innerText(),/AUDIT PASS/);
 await page.locator("#rootAudit").click();assert.match(await page.locator("#status").innerText(),/ROOT PASS/);
 const canvas=await page.locator("#viz").evaluate(el=>({width:el.width,height:el.height}));
 assert(canvas.width>200&&canvas.height>200,"Real rendered canvas dimensions");
 const downloadPromise=page.waitForEvent("download");await page.locator("#export").click();const dl=await downloadPromise;
 assert.match(dl.suggestedFilename(),/ada-211n-epoch-11\.json/);
 assert.match(await page.locator("#status").innerText(),/EPOCH PROOF EXPORTED/);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({schema:"ADA-211N.browser.v1",pass:true,generations:266,epochs:12,sealed:11,canvas,errors},null,2));
}finally{await page.close();await browser.close()}
