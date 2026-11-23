// ADA-199N · Browser runtime smoke tests. Executes against local HTTP server, not file://.
// Invoke: ADA_BASE_URL=http://127.0.0.1:8765 node ada/ada-199n-browser-smoke.mjs
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
const root=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
const forceCanvas=process.env.ADA_FORCE_CANVAS==="1";
const requireWebGL=process.env.ADA_REQUIRE_WEBGL==="1";
if(forceCanvas&&requireWebGL)throw Error("Invalid test setup: cannot require both WebGL and forced Canvas2D");
const routes=[
["191N","ada-191n-integrated-living-lab.html","run","stats","replay","verification"],
["192N","ada-192n-unified-observation-3d.html","run","metrics","replay","renderMode"],
["193N","ada-193n-persistent-3d-memory.html","run","stats","replay","status"],
["194N","ada-194n-3d-adaptive-learning.html","run","stats","verify","integrity"],
["195N","ada-195n-3d-failure-repair.html","run","stats","verify","verification"],
["196N","ada-196n-unified-three-contact-3d.html","batch","stats","verify","status"],
["197N","ada-197n-best-policy-3d.html","run","stats","verify","status"],
["198N","ada-198n-3d-stress-recovery.html","run","stats","replay","status"]
];
const output=process.env.ADA_REPORT_DIR||"ada/verification-results";
fs.mkdirSync(output,{recursive:true});
let browser;
try{
 browser=await chromium.launch({headless:true,args:["--no-sandbox","--enable-webgl","--enable-unsafe-swiftshader","--use-gl=angle","--use-angle=swiftshader"]});
}catch(error){
 const report={schema:"ADA-199N.smoke.v3",base:root,forceCanvas,requireWebGL,passed:0,failed:routes.length,results:routes.map(([version])=>({version,status:"FAIL",reason:"Chromium launch failed: "+String(error.message||error)})),fatal:{stage:"chromium-launch",message:String(error.message||error)}};
 fs.writeFileSync(path.join(output,"report.json"),JSON.stringify(report,null,2)+"\n");
 console.error("Chromium launch failed:",error);
 process.exit(1);
}
let passed=0,failed=0;const results=[];
try{
for(const [version,file,stepId,statsId,verifyId,statusId] of routes){
let page=null;
const errors=[],failedRequests=[];
const url=root+"/ada/"+file;
const item={version,url,checks:[],errors,failedRequests};
const assert=(name,ok,detail="")=>{item.checks.push({name,pass:!!ok,detail});if(!ok)throw Error(name+(detail?" - "+detail:""))};
try{
page=await browser.newPage({viewport:{width:1280,height:880}});
if(forceCanvas)await page.route("**/three.min.js",route=>route.abort("blockedbyclient"));
page.on("pageerror",e=>errors.push(e.message));
page.on("requestfailed",request=>failedRequests.push({url:request.url(),reason:request.failure()?.errorText}));
const response=await page.goto(url,{waitUntil:"domcontentloaded",timeout:20000});
assert("route HTTP 200",response?.status()===200,String(response?.status()));
assert("document title",await page.title()!== "");
assert("action control",await page.locator("#"+stepId).count()===1);
assert("metric panel",await page.locator("#"+statsId).count()===1);
const beforeStats=(await page.locator("#"+statsId).innerText()).trim();
await page.locator("#"+stepId).click({timeout:12000});
try{
 await page.waitForFunction(({statsId,beforeStats})=>{
  const text=(document.getElementById(statsId)?.innerText||"").trim();
  return text.length>15&&text!==beforeStats
 },{statsId,beforeStats},{timeout:12000});
}catch(e){
 const last=(await page.locator("#"+statsId).innerText().catch(()=>"<unavailable>")).trim();
 throw Error("Metrics did not advance after #"+stepId+"; before="+JSON.stringify(beforeStats.slice(0,180))+"; last="+JSON.stringify(last.slice(0,180))+"; pageErrors="+JSON.stringify(errors.slice(-3))+"; cause="+e.message);
}
const stats=(await page.locator("#"+statsId).innerText()).trim();
assert("simulation produced metrics",stats.length>15,stats.slice(0,100));
assert("simulation changed displayed metrics",stats!==beforeStats,"Before: "+beforeStats.slice(0,80)+" After: "+stats.slice(0,80));
assert("no uncaught errors during run",errors.length===0,errors.join("; "));
await page.locator("#"+verifyId).click({timeout:12000});
try{
 await page.waitForFunction(statusId=>{
  const text=(document.getElementById(statusId)?.innerText||"").trim();
  return /REPLAY\s+(?:PASS|FAIL)/i.test(text)
 },statusId,{timeout:12000});
}catch(e){
 const last=(await page.locator("#"+statusId).innerText().catch(()=>"<unavailable>")).trim();
 throw Error("Replay verdict did not arrive after #"+verifyId+"; last="+JSON.stringify(last.slice(0,180))+"; pageErrors="+JSON.stringify(errors.slice(-3))+"; cause="+e.message);
}
const status=(await page.locator("#"+statusId).innerText()).trim();
assert("replay check passed",/PASS/i.test(status)&&!/FAIL/i.test(status),status);
assert("no uncaught errors during replay",errors.length===0,errors.join("; "));
if(version!=="191N"){
const stage=page.locator("#stage");
assert("visual stage exists",await stage.count()===1);
await page.waitForFunction(() => {const s=document.querySelector("#stage");const mode=document.querySelector("#renderMode,#engine,#render,#mode")?.textContent||"";return !!s?.querySelector("canvas")&&/WEBGL|CANVAS\s*2D|CANVAS2D|2D\s*PROJECTED/i.test(mode)},null,{timeout:16000});
assert("rendered canvas exists",await stage.locator("canvas").count()>0);
const size=await stage.locator("canvas").first().evaluate(el=>({width:el.width,height:el.height}));
assert("renderer has nonzero pixel dimensions",size.width>100&&size.height>100,JSON.stringify(size));
const mode=await page.evaluate(()=>document.querySelector("#renderMode,#engine,#render,#mode")?.textContent||"");
item.renderMode=mode;
// Query only the context type actually owned by the canvas. Asking for WebGL on a
// Canvas2D-owned canvas can throw InvalidStateError in real browsers.
const renderState=await stage.locator("canvas").first().evaluate((el,mode)=>{
 const webgl=/WEBGL/i.test(mode);
 let context=null,error=null,contextName=null;
 const candidates=webgl?["webgl2","webgl","experimental-webgl"]:["2d"];
 for(const name of candidates){
   try{const c=el.getContext(name);if(c){context=c;contextName=name;break}}
   catch(e){error=String(e)}
 }
 return {type:webgl?"webgl":"canvas2d",contextName,contextAvailable:!!context,hasLiveGL:webgl&&!!context&&!context.isContextLost?.(),pixelArea:el.width*el.height,error:context?null:error}
},mode);
item.renderState=renderState;
assert("canvas has usable drawing surface",renderState.pixelArea>10000,JSON.stringify(renderState));
assert("canvas owns an available drawing context",renderState.contextAvailable,JSON.stringify(renderState));
if(requireWebGL){
assert("real WebGL renderer activated",/WEBGL/i.test(mode),mode);
assert("live WebGL drawing context exists",renderState.hasLiveGL,JSON.stringify(renderState));
}
if(forceCanvas)assert("forced Canvas2D fallback activated",/CANVAS\s*2D|CANVAS2D|2D\s*PROJECTED|REPLAY PASS\s*·\s*2D/i.test(mode),mode);
assert("renderer mode declared",/WEBGL|CANVAS\s*2D|CANVAS2D|2D\s*PROJECTED|REPLAY PASS\s*·\s*2D/i.test(mode),mode);
}
await page.screenshot({path:path.join(output,version+"-screenshot.png"),fullPage:true});
item.status="PASS";passed++;
}catch(e){item.status="FAIL";item.reason=e.message;failed++;
try{if(page)await page.screenshot({path:path.join(output,version+"-failure.png"),fullPage:true})}catch{}}
results.push(item);if(page)try{await page.close()}catch(e){item.closeError=String(e.message||e)}
console.log(version+" "+item.status+(item.reason?": "+item.reason:""));
}
}finally{await browser.close()}
const report={schema:"ADA-199N.smoke.v3",base:root,forceCanvas,requireWebGL,passed,failed,results};
fs.writeFileSync(path.join(output,"report.json"),JSON.stringify(report,null,2)+"\n");
console.log(JSON.stringify(report,null,2));
if(failed)process.exitCode=1;
