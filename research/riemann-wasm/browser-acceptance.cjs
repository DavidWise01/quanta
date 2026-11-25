// RIEMANN-011: actual Chromium browser acceptance for the Rust/WASM viewer.
// Run with: node research/riemann-wasm/browser-acceptance.cjs http://127.0.0.1:8765/docs/riemann-rust/
// Requires playwright installed in the CI checkout.
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8765/docs/riemann-rust/';
const cases = [
  // [option, steps, expected mask, expected radius, theta, phi]
  [0, 3, [true,false,false,true,false], 1,3,0],
  [1, 1, [false,true,false,true,false], 3,0,0],
  [2, 3, [true,true,true,true,true], 1,0,0],
  [3, 1, [false,false,false,true,false], 3,17,23],
  [4, 3, [true,false,true,true,false], 1,0,3],
  [5, 3, [true,false,true,true,false], 1,1,0],
];
(async () => {
  const browser = await chromium.launch({headless:true});
  let page;
  try {
    page = await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
    const errors = [];
    page.on('pageerror', e=>errors.push(e.message));
    page.on('console', m=>{if(m.type()==='error') errors.push('console: '+m.text())});
    const response=await page.goto(url,{waitUntil:'networkidle',timeout:45000});
    assert.ok(response && response.ok(),'view page should load over HTTP');
    await page.waitForFunction(()=>document.querySelector('#wasmStatus')?.textContent?.includes('LOADED'),null,{timeout:25000});
    assert.equal(await page.locator('#wasmStatus').innerText(),'RUST/WASM LOADED · v10');
    assert.equal(await page.locator('#step').isEnabled(),true,'WASM controls enabled');
    assert.equal(await page.locator('#run').isEnabled(),true,'WASM play enabled');
    for(const [option,steps,bits,radius,theta,phi] of cases){
      await page.selectOption('#scenario',String(option));
      await page.locator('#steps').fill(String(steps));
      await page.locator('#steps').dispatchEvent('change');
      assert.equal(Number(await page.locator('#outRadius').innerText()),radius,'case '+option+' radius');
      assert.equal(Number(await page.locator('#outTheta').innerText()),theta,'case '+option+' theta');
      assert.equal(Number(await page.locator('#outPhi').innerText()),phi,'case '+option+' phi');
      for(let i=0;i<5;i++){
        const el=page.locator('#flag'+i);
        assert.equal(await el.evaluate(e=>e.classList.contains('yes')),bits[i],'case '+option+' flag '+i);
      }
      console.log('Chromium case C'+(option+1)+' PASS');
    }
    await page.locator('#reset').click();
    assert.equal(Number(await page.locator('#steps').inputValue()),0,'reset zeroes steps');
    await page.locator('#step').click();
    assert.equal(Number(await page.locator('#steps').inputValue()),1,'step advances by one');
    assert.deepEqual(errors,[], 'no JavaScript errors');
    const canvas=await page.locator('#arena').evaluate(e=>({width:e.width,height:e.height}));
    assert.ok(canvas.width>200&&canvas.height>200,'canvas layout');
    console.log('CHROMIUM ACCEPTANCE PASS: 6/6 cases, 30 flags, reset/step, canvas, zero errors');
  } finally { await browser.close(); }
})().catch(err=>{console.error('CHROMIUM ACCEPTANCE FAIL:',err.stack||err);process.exit(1)});
