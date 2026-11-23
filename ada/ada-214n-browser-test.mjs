// ADA-214N · Chromium verifies inherited epoch contacts, stored ancestry and safety gate.
import assert from "node:assert/strict";
import {chromium} from "playwright";
const base=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--enable-webgl","--enable-unsafe-swiftshader"]});
const page=await browser.newPage({viewport:{width:1280,height:860},acceptDownloads:true});
const errors=[];page.on("pageerror",e=>errors.push(e.message));
try{
 const response=await page.goto(base+"/ada/ada-214n-epoch-lab.html",{waitUntil:"networkidle",timeout:30000});
 assert.equal(response.status(),200);
 await page.waitForFunction(()=>/GENESIS PERSISTED|RESTORE PASS/.test(document.querySelector("#status")?.textContent||""));
 assert.match(await page.locator("#contactState").innerText(),/EPOCH CONTACT REPLAY PASS.*1 epochs/);
 await page.locator("#batch").click();
 assert.equal((await page.locator("#count").innerText()).trim(),"241");
 assert.match(await page.locator("#contactState").innerText(),/EPOCH CONTACT REPLAY PASS.*11 epochs.*10 sealed.*17 retained HOLD/);
 assert.equal(await page.locator("#contactRows tr").count(),11);
 const last=page.locator("#contactRows tr").first();
 assert.equal((await last.locator("td").nth(0).innerText()).trim(),"10");
 assert.equal((await last.locator("td").nth(2).innerText()).trim(),"1");
 assert.equal((await last.locator("td").nth(3).innerText()).trim(),"OPEN_TAIL");
 const saved=await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00009"));
 assert(saved);
 assert.equal(await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00010")),null);
 await page.reload({waitUntil:"networkidle",timeout:30000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("RESTORE PASS"));
 assert.match(await page.locator("#contactState").innerText(),/11 epochs.*10 sealed.*17 retained HOLD/);
 assert.equal(await page.evaluate(()=>localStorage.getItem("ADA-212N.epoch.sealed.00009")),saved);
 await page.locator("#epochInput").fill("9");await page.locator("#trace").click();
 assert.match(await page.locator("#traceState").innerText(),/EPOCH TRACE PASS.*SEALED RECEIPT/);
 const canvas=await page.locator("#viz").evaluate(e=>({w:e.width,h:e.height}));
 assert(canvas.w>200&&canvas.h>200);
 await page.evaluate(()=>{const key="ADA-212N.epoch.sealed.00009",e=JSON.parse(localStorage.getItem(key));e.holds+=1;localStorage.setItem(key,JSON.stringify(e))});
 await page.reload({waitUntil:"networkidle",timeout:30000});
 await page.waitForFunction(()=>document.querySelector("#status")?.textContent.includes("ARCHIVE LOCKED"));
 await page.locator("#one").click();assert.match(await page.locator("#status").innerText(),/REJECTED/);
 assert.equal((await page.locator("#count").innerText()).trim(),"1");
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({schema:"ADA-214N.browser.v1",pass:true,generations:241,epochContacts:11,sealed:10,holds:17,openTail:true,canvas,errors},null,2));
}finally{await page.close();await browser.close()}
