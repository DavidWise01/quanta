// ADA-306N .dlw — explicit abort after insertion, then recovery; synthetic kernel.
import {chromium} from "playwright";
import assert from "node:assert/strict";
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage();
 await page.goto(process.env.ADA_TEST_BASE||"http://127.0.0.1:8765/ada/ada-299n-operational-lab.html");
 const result=await page.evaluate(async()=>{
  const {openLedger}=await import("/ada/wasm/ledger-incremental.mjs");
  const kernel={source:"c".repeat(40),sha256:"d".repeat(64),exports:{ada_clock_field:(g,i)=>[g,Math.floor(g/24),g%24,g%8,g%360,Math.floor(g%360/120)][i],ada_pump_field:(g,i,j)=>j===0?(g+i*120)%360:j===1?1/3:0}};
  const frame=g=>({generation:g,clock:Array.from({length:6},(_,i)=>kernel.exports.ada_clock_field(g,i)),pumps:Array.from({length:3},(_,i)=>Array.from({length:5},(_,j)=>kernel.exports.ada_pump_field(g,i,j)))});
  let ledger=await openLedger(kernel);
  try{
   await ledger.verify();const genesis=await ledger.append(frame(0));
   const original=IDBObjectStore.prototype.add;
   let inserted=false,aborted=false,rejected=false;
   IDBObjectStore.prototype.add=function(...args){
    const req=original.apply(this,args);
    if(this.name==="frames"&&args[0]?.generation===1){const tx=this.transaction;req.addEventListener("success",()=>{inserted=true;tx.abort();aborted=true},{once:true});}
    return req;
   };
   try{await ledger.append(frame(1));}catch{rejected=true;}finally{IDBObjectStore.prototype.add=original;}
   let invalidated=false;try{await ledger.append(frame(1));}catch{invalidated=true;}
   ledger.close();ledger=await openLedger(kernel);
   const before=await ledger.verify();
   const retry=await ledger.append(frame(1));const after=await ledger.verify();
   return {inserted,aborted,rejected,invalidated,before:before.map(x=>x.generation),genesisPreserved:before[0]?.digest===genesis,after:after.map(x=>x.generation),linked:after[1]?.previous===genesis,retryPreserved:after[1]?.digest===retry};
  }finally{ledger.close();}
 });
 assert.deepEqual(result,{inserted:true,aborted:true,rejected:true,invalidated:true,before:[0],genesisPreserved:true,after:[0,1],linked:true,retryPreserved:true});
 console.log(JSON.stringify({status:"PASS",scope:"synthetic kernel; real IndexedDB; explicit transaction abort",result}));
}finally{await browser.close();}
