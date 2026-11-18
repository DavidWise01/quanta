// ADA-130 .dlw — bounded operational forgetting; immutable observation ancestry.
export const rates=[.02,.08,.14,.20,.28,.36,.45,.60,.80];
export function forecast(q,d,p){const a=Array(26).fill(0);for(const [o,w] of [[2*d,(1-p)**2],[-2*d,p*(1-p)],[0,p]])a[(q+o+26)%26]+=w;return a;}
// Unnormalized Bayesian update is linear. Cache powers of the zero-observation
// matrix; its normalization can be postponed until the end of a run.
export function buildCache(gate=5,capacity=8,policy="lfu"){return {gate,capacity,policy,seen:new Uint32Array(4096),total:new Uint32Array(4096),last:new Uint32Array(4096),clock:0,blocks:new Map(),hits:0,misses:0,evictions:0,buildTerms:0,bypasses:0,archived:new Set(),resurrections:0,events:[]};}
function getBlock(key,c){
 const id=parseInt(key,2);c.clock++;c.total[id]++;c.last[id]=c.clock;if(c.blocks.has(key)){c.hits++;return c.blocks.get(key);}
 c.misses++;
 if(++c.seen[id]<c.gate){c.bypasses++;return null;}
 c.seen[id]=0;
 let M=rates.map((_,i)=>rates.map((_,j)=>Number(i===j)));
 // Exploit diagonal plus rank-one structure: 2 products per matrix entry plus 1 likelihood product.
 for(const b of key){const sums=M[0].map((_,j)=>M.reduce((s,row)=>s+row[j],0));M=M.map((row,i)=>row.map((v,j)=>(.985*v+.015/9*sums[j])*(b==="1"?rates[i]:1-rates[i])));c.buildTerms+=243;}
 if(c.blocks.size===c.capacity){let victim=c.blocks.keys().next().value;if(c.policy!=="fifo"){for(const k of c.blocks.keys()){const a=parseInt(k,2),b=parseInt(victim,2);if(c.policy==="lru"?c.last[a]<c.last[b]:c.total[a]<c.total[b]||c.total[a]===c.total[b]&&c.last[a]<c.last[b])victim=k;}}c.blocks.delete(victim);c.evictions++;c.archived.add(victim);c.events.push({clock:c.clock,key:victim,event:"archive"});}
 if(c.archived.has(key)){c.resurrections++;c.events.push({clock:c.clock,key,event:"reconstruct"});}else c.events.push({clock:c.clock,key,event:"compile"});
 c.blocks.set(key,M);return M;
}
export function run(seed,scenario="shift",cache=buildCache()){
 let x=seed>>>0,q=0,d=1,w=.02,bank=rates.map((_,i)=>i===1?.84:.02),cursor=0,fast=.08,awake=0,loss=0,forecasts=0,updates=0,wakes=0,was=false;
 let scalarUpdates=0,matrixMultiplies=0,rawTokens=0,encodedTokens=0;const flips=[0],ledger=[],scores=[],presist=[],memory=[];
 for(let t=0;t<208;t++){
 if(t){x=(Math.imul(x,1664525)+1013904223)>>>0;const p=scenario==="novel"?(t<70?.14:t<140?.60:.28):scenario==="shift"&&t>=104||scenario==="recover"&&t>=69&&t<139?.45:.08;const flip=Number(x/4294967296<p);flips.push(flip);if(flip)d=-d;q=(q+d+26)%26;fast=.12*flip+.88*fast;const prior=w*.985+(1-w)*.015,a=prior*(flip?.45:.55),b=(1-prior)*(flip?.08:.92);w=a/(a+b);updates+=2;}
 // Wake on ambiguous regime, mismatch, or periodic probe; stay awake for 8 ticks.
 const trigger=t%32===0||Math.abs(fast-((1-w)*.08+w*.45))>.12||(w>=.25&&w<=.75);
 if(trigger)awake=8;else awake=Math.max(0,awake-1);
 const active=awake>0;if(active&&!was)wakes++;was=active;
 const lo=forecast(q,d,.08),hi=forecast(q,d,.45);forecasts+=2;
 let prediction=lo.map((v,i)=>(1-w)*v+w*hi[i]);
 if(active){
 // Replay missed observations only on wake; no nine-model updates or forecasts during sleep.
 while(cursor<t){
 const length=t-cursor>=12?12:1;rawTokens+=length;encodedTokens++;
 if(length===12){
 const key=flips.slice(cursor+1,cursor+13).join("");
 const M=getBlock(key,cache);
 if(M){bank=M.map(row=>row.reduce((s,v,i)=>s+v*bank[i],0));matrixMultiplies++;const z=bank.reduce((a,b)=>a+b,0);bank=bank.map(v=>v/z);}else for(const bit of key){const u=bank.map((v,i)=>(.985*v+.015/9)*(bit==="1"?rates[i]:1-rates[i])),z=u.reduce((a,b)=>a+b,0);bank=u.map(v=>v/z);scalarUpdates+=9;}
 }else{
 const flip=flips[cursor+1],u=bank.map((v,i)=>(.985*v+.015/9)*(flip?rates[i]:1-rates[i])),z=u.reduce((a,b)=>a+b,0);bank=u.map(v=>v/z);scalarUpdates+=9;
 }
 cursor+=length;updates+=9*length;
 }
 const p9=Array(26).fill(0);for(let m=0;m<9;m++){const a=forecast(q,d,rates[m]);forecasts++;for(let j=0;j<26;j++)p9[j]+=bank[m]*a[j];}prediction=prediction.map((v,i)=>(v+p9[i])/2);
 }
 if(t>=2){const f=ledger[t-2],e=f.prediction.reduce((a,v,i)=>a+(v-Number(i===q))**2,0);loss+=e;scores.push({issued:t-2,target:t,actual:q,loss:e});}
 ledger.push(Object.freeze({issued:t,target:t+2,q,active,cursor,forecasts,updates,prediction:Object.freeze(prediction)}));memory.push({t,flip:flips[t],active,cursor});presist.push({t,q,w,active});if(presist.length>3)presist.shift();
 }
 return {seed,scenario,count:scores.length,loss,forecasts,updates,wakes,scalarUpdates,matrixMultiplies,rawTokens,encodedTokens,sleepTicks:ledger.filter(f=>!f.active).length,ledger,scores,presist,memory};
}
