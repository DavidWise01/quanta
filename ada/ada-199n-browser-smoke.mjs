// ADA-199N · Browser runtime smoke tests. Executes against local HTTP server, not file://.
// Invoke: ADA_BASE_URL=http://127.0.0.1:8765 node ada/ada-199n-browser-smoke.mjs
import { chromium } from "playwright";
const root=(process.env.ADA_BASE_URL||"http://127.0.0.1:8765").replace(/\/$/,"");
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
const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
let passed=0,failed=0;const results=[];
try{
for(const [version,file,stepId,statsId,verifyId,statusId] of routes){
const page=await browser.newPage({viewport:{width:1280,height:880}});
const errors=[];page.on("pageerror",e=>errors.push(e.message));
const url=root+"/ada/"+file;
const item={version,url,checks:[],errors};
const assert=(name,ok,detail="")=>{item.checks.push({name,pass:!!ok,detail});if(!ok)throw Error(name+(detail?" - "+detail:""))};
try{
const response=await page.goto(url,{waitUntil:"domcontentloaded",timeout:20000});
assert("route HTTP 200",response?.status()===200,String(response?.status()));
assert("document title",await page.title()!== "");
assert("action control",await page.locator("#"+stepId).count()===1);
assert("metric panel",await page.locator("#"+statsId).count()===1);
await page.locator("#"+stepId).click({timeout:12000});
await page.waitForTimeout(250);
const stats=(await page.locator("#"+statsId).innerText()).trim();
assert("simulation produced metrics",stats.length>15,stats.slice(0,100));
assert("no uncaught errors during run",errors.length===0,errors.join("; "));
await page.locator("#"+verifyId).click({timeout:12000});
await page.waitForTimeout(150);
const status=(await page.locator("#"+statusId).innerText()).trim();
assert("replay check passed",/PASS/i.test(status)&&!/FAIL/i.test(status),status);
assert("no uncaught errors during replay",errors.length===0,errors.join("; "));
if(version!=="191N"){
const stage=page.locator("#stage");
assert("visual stage exists",await stage.count()===1);
await page.waitForTimeout(1100);
assert("rendered canvas exists",await stage.locator("canvas").count()>0);
}
item.status="PASS";passed++;
}catch(e){item.status="FAIL";item.reason=e.message;failed++}
results.push(item);await page.close();
console.log(version+" "+item.status+(item.reason?": "+item.reason:""));
}
}finally{await browser.close()}
const report={schema:"ADA-199N.smoke.v1",base:root,passed,failed,results};
console.log(JSON.stringify(report,null,2));
if(failed)process.exitCode=1;
