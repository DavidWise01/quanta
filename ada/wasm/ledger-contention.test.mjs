// ADA-305N .dlw — real IndexedDB contention test; synthetic kernel only.
import {chromium} from "playwright";
import assert from "node:assert/strict";
const browser=await chromium.launch({headless:true});
try {
 const context=await browser.newContext();
 const page=await context.newPage();
 await page.goto(process.env.ADA_TEST_BASE||"http://127.0.0.1:8765/ada/ada-299n-operational-lab.html");
 const result=await page.evaluate(async()=>{
  const {openLedger}=await import("/ada/wasm/ledger-incremental.mjs");
  const kernel={source:"a".repeat(40),sha256:"b".repeat(64),exports:{ada_clock_field:(g,i)=>[g,Math.floor(g/24),g%24,g%8,g%360,Math.floor(g%360/120)][i],ada_pump_field:(g,i,j)=>j===0?(g+i*120)%360:j===1?1/3:0}};
  const frame=g=>({generation:g,clock:Array.from({length:6},(_,i)=>kernel.exports.ada_clock_field(g,i)),pumps:Array.from({length:3},(_,i)=>Array.from({length:5},(_,j)=>kernel.exports.ada_pump_field(g,i,j)))});
  const a=await openLedger(kernel),b=await openLedger(kernel);
  try{
   await a.verify();await b.verify();
   const race=await Promise.allSettled([a.append(frame(0)),b.append(frame(0))]);
   const winner=race[0].status==="fulfilled"?a:b,loser=winner===a?b:a;
   const stale=await Promise.allSettled([loser.append(frame(1))]);
   const recovered=await loser.verify();
   await loser.append(frame(1));
   const final=await winner.verify();
   return {commits:race.filter(x=>x.status==="fulfilled").length,rejections:race.filter(x=>x.status==="rejected").length,staleRejected:stale[0].status==="rejected",recovered:recovered.length,generations:final.map(x=>x.generation),linked:final[1]?.previous===final[0]?.digest};
  }finally{a.close();b.close()}
 });
 assert.deepEqual(result,{commits:1,rejections:1,staleRejected:true,recovered:1,generations:[0,1],linked:true});
 console.log(JSON.stringify({status:"PASS",scope:"synthetic kernel; real IndexedDB; two connections",result}));
}finally{await browser.close()}
