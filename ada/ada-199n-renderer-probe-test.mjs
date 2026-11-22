// ADA-199N · Regression test against the exact browser smoke-test context probe.
import fs from "node:fs";
import assert from "node:assert/strict";
const src=fs.readFileSync(new URL("./ada-199n-browser-smoke.mjs",import.meta.url),"utf8");
const start=src.indexOf('const renderState=await stage.locator("canvas").first().evaluate((el,mode)=>');
const end=src.indexOf("},mode);",start);
assert.ok(start>=0&&end>start,"Renderer probe found in smoke test");
const arrow=src.slice(src.indexOf("evaluate(",start)+9,end+1);
const probe=Function("return ("+arrow+")")();
const gl={isContextLost(){return false}};
const record=(mode,getContext)=>{const called=[];const value=probe({width:1024,height:768,getContext(type){called.push(type);return getContext(type)}},mode);return {value,called}};
const v1=record("WEBGL · LIVE",t=>{if(t==="webgl2")throw Error("WebGL2 unsupported");return t==="webgl"?gl:null});
const v2=record("WEBGL · LIVE",t=>t==="webgl2"?gl:null);
const fallback=record("CANVAS2D · PROJECTED",t=>{if(t!=="2d")throw Error("InvalidStateError");return {fillRect(){}}});
assert.equal(v1.value.hasLiveGL,true,"WebGL1 recognized even when WebGL2 rejects");
assert.equal(v2.value.hasLiveGL,true,"WebGL2 recognized");
assert.equal(fallback.value.contextName,"2d","Canvas2D identified without WebGL probes");
assert.deepEqual(fallback.called,["2d"],"Do not query WebGL on 2D-owned canvas");
console.log(JSON.stringify({schema:"ADA-199N.render-probe.v1",passed:3,total:3,results:{webgl1:v1.value,webgl2:v2.value,canvas2d:fallback.value}},null,2));
