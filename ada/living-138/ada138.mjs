// ADA-138 .dlw — exact evidence identity and conflict quarantine.
// Event identity includes model lineage, scenario, seed, and ordered observation interval.
export class Memsistor{
 constructor(){this.events=new Map();this.attempts=0;this.duplicates=0;this.conflicts=0;}
 ingest(e){this.attempts++;const id=JSON.stringify([e.root,e.scenario,e.seed,e.start,e.end]);const p=this.events.get(id);
 if(!p){this.events.set(id,{payloads:new Set([e.bits]),routes:new Set([e.route])});return;}
 p.routes.add(e.route);if(p.payloads.has(e.bits)){this.duplicates++;return;}p.payloads.add(e.bits);this.conflicts++;}
 snapshot(){const keys=new Map();let valid=0,quarantined=0;for(const [id,p] of this.events){if(p.payloads.size!==1){quarantined++;continue;}valid++;const bits=[...p.payloads][0];keys.set(bits,(keys.get(bits)||0)+1);}return {valid,quarantined,keys:[...keys].sort((a,b)=>a[0].localeCompare(b[0])),attempts:this.attempts,duplicates:this.duplicates,conflicts:this.conflicts,roots:new Set([...this.events.keys()].map(k=>JSON.parse(k)[0])).size};}
}
// ADA-135 .dlw — antistrophic paired counterfactual evaluation.
// Parent engines namespaced; same observed seeded world, no future labels used for routing.
const Uminus=(()=>{// ADA-131 .dlw — generational protection with expiring leases.
const rates=[.02,.08,.14,.20,.28,.36,.45,.60,.80];
function forecast(q,d,p){const a=Array(26).fill(0);for(const [o,w] of [[2*d,(1-p)**2],[-2*d,p*(1-p)],[0,p]])a[(q+o+26)%26]+=w;return a;}
// Unnormalized Bayesian update is linear. Cache powers of the zero-observation
// matrix; its normalization can be postponed until the end of a run.
function buildCache(gate=5,capacity=8,policy="permanent",lease=64){return {gate,capacity,policy,lease,seen:new Uint32Array(4096),total:new Uint32Array(4096),last:new Uint32Array(4096),clock:0,blocks:new Map(),hits:0,misses:0,evictions:0,buildTerms:0,bypasses:0,archived:new Set(),resurrections:0,events:[]};}
function getBlock(key,c){
 const id=parseInt(key,2);c.clock++;c.total[id]++;c.last[id]=c.clock;if(c.total[id]===8||c.total[id]===13)c.events.push({clock:c.clock,key,event:c.total[id]===8?"thrive":"promote"});if(c.blocks.has(key)){c.hits++;return c.blocks.get(key);}
 c.misses++;
 if(++c.seen[id]<c.gate){c.bypasses++;return null;}
 c.seen[id]=0;
 let M=rates.map((_,i)=>rates.map((_,j)=>Number(i===j)));
 // Exploit diagonal plus rank-one structure: 2 products per matrix entry plus 1 likelihood product.
 for(const b of key){const sums=M[0].map((_,j)=>M.reduce((s,row)=>s+row[j],0));M=M.map((row,i)=>row.map((v,j)=>(.985*v+.015/9*sums[j])*(b==="1"?rates[i]:1-rates[i])));c.buildTerms+=243;}
 if(c.blocks.size===c.capacity){let victim=c.blocks.keys().next().value;if(c.policy!=="fifo"){const rank=id=>c.policy==="lfu"?0:c.policy==="permanent"?(c.total[id]>=13?2:c.total[id]>=8?1:0):c.clock-c.last[id]>c.lease?0:c.total[id]>=13?2:c.total[id]>=8?1:0;for(const k of c.blocks.keys()){const a=parseInt(k,2),b=parseInt(victim,2),ra=rank(a),rb=rank(b);if(ra<rb||ra===rb&&(c.policy==="lease"?c.last[a]<c.last[b]:c.total[a]<c.total[b]||c.total[a]===c.total[b]&&c.last[a]<c.last[b]))victim=k;}}c.blocks.delete(victim);c.evictions++;c.archived.add(victim);c.events.push({clock:c.clock,key:victim,event:"archive"});}
 if(c.archived.has(key)){c.resurrections++;c.events.push({clock:c.clock,key,event:"reconstruct"});}else c.events.push({clock:c.clock,key,event:"compile"});
 c.blocks.set(key,M);return M;
}
function run(seed,scenario="shift",cache=buildCache()){
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
;return {run,buildCache};})();
const Uplus=(()=>{// ADA-133 .dlw — probation, economic admission and protected descendant lease.
const rates=[.02,.08,.14,.20,.28,.36,.45,.60,.80];
function forecast(q,d,p){const a=Array(26).fill(0);for(const [o,w] of [[2*d,(1-p)**2],[-2*d,p*(1-p)],[0,p]])a[(q+o+26)%26]+=w;return a;}
// Unnormalized Bayesian update is linear. Cache powers of the zero-observation
// matrix; its normalization can be postponed until the end of a run.
function buildCache(gate=5,capacity=8,policy="permanent",lease=64,composeGate=34,leaseChild=64){return {leaseChild,nursery:new Map(),childLast:new Map(),graduates:0,integrityChecks:0,gate,capacity,policy,lease,composeGate,pairs:new Map(),composed:new Map(),pairHits:0,pairBuilds:0,pairEligible:0,pairEvictions:0,seen:new Uint32Array(4096),total:new Uint32Array(4096),last:new Uint32Array(4096),clock:0,blocks:new Map(),hits:0,misses:0,evictions:0,buildTerms:0,bypasses:0,archived:new Set(),resurrections:0,events:[]};}
function getBlock(key,c){
 const id=parseInt(key,2);c.clock++;c.total[id]++;c.last[id]=c.clock;if(c.total[id]===8||c.total[id]===13)c.events.push({clock:c.clock,key,event:c.total[id]===8?"thrive":"promote"});if(c.blocks.has(key)){c.hits++;return c.blocks.get(key);}
 c.misses++;
 if(++c.seen[id]<c.gate){c.bypasses++;return null;}
 c.seen[id]=0;
 let M=rates.map((_,i)=>rates.map((_,j)=>Number(i===j)));
 // Exploit diagonal plus rank-one structure: 2 products per matrix entry plus 1 likelihood product.
 for(const b of key){const sums=M[0].map((_,j)=>M.reduce((s,row)=>s+row[j],0));M=M.map((row,i)=>row.map((v,j)=>(.985*v+.015/9*sums[j])*(b==="1"?rates[i]:1-rates[i])));c.buildTerms+=243;}
 if(c.blocks.size+c.composed.size===c.capacity&&c.composed.size){const child=[...c.composed.keys()].find(k=>c.clock-c.childLast.get(k)>c.leaseChild);if(child){c.composed.delete(child);c.pairEvictions++;}else{let victim=[...c.blocks.keys()].sort((x,y)=>c.total[parseInt(x,2)]-c.total[parseInt(y,2)]||c.last[parseInt(x,2)]-c.last[parseInt(y,2)])[0];c.blocks.delete(victim);c.archived.add(victim);c.evictions++;}}
 if(c.blocks.size===c.capacity){let victim=c.blocks.keys().next().value;if(c.policy!=="fifo"){const rank=id=>c.policy==="lfu"?0:c.policy==="permanent"?(c.total[id]>=13?2:c.total[id]>=8?1:0):c.clock-c.last[id]>c.lease?0:c.total[id]>=13?2:c.total[id]>=8?1:0;for(const k of c.blocks.keys()){const a=parseInt(k,2),b=parseInt(victim,2),ra=rank(a),rb=rank(b);if(ra<rb||ra===rb&&(c.policy==="lease"?c.last[a]<c.last[b]:c.total[a]<c.total[b]||c.total[a]===c.total[b]&&c.last[a]<c.last[b]))victim=k;}}c.blocks.delete(victim);c.evictions++;c.archived.add(victim);c.events.push({clock:c.clock,key:victim,event:"archive"});}
 if(c.archived.has(key)){c.resurrections++;c.events.push({clock:c.clock,key,event:"reconstruct"});}else c.events.push({clock:c.clock,key,event:"compile"});
 c.blocks.set(key,M);return M;
}
function run(seed,scenario="shift",cache=buildCache()){
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
 if(t-cursor>=24){
 const key=flips.slice(cursor+1,cursor+25).join(""),a=key.slice(0,12),b=key.slice(12);
 cPair: {
 const c=cache;c.pairEligible++;
 let M=c.composed.get(key);
 if(M){c.pairHits++;c.childLast.set(key,c.clock);}
 else{
 const n=c.nursery.get(key)||{count:0,eligible:0,seeds:new Set(),first:c.clock};
 n.count++;n.seeds.add(seed);if(c.blocks.has(a)&&c.blocks.has(b))n.eligible++;c.nursery.set(key,n);
 // Witness roles: ordered parents, recurrence across distinct runs, expected economics.
 // 729 construction terms / 81 saved terms = nine uses to break even.
 if(n.count<c.composeGate||n.seeds.size<3||n.eligible<10||!c.blocks.has(a)||!c.blocks.has(b))break cPair;
 // At most one child slot; don't displace a recently used child.
 if(c.composed.size&&[...c.composed.keys()].some(k=>c.clock-c.childLast.get(k)<=c.leaseChild))break cPair;
 const A=c.blocks.get(a),B=c.blocks.get(b);
 M=B.map(row=>A[0].map((_,j)=>row.reduce((s,v,k)=>s+v*A[k][j],0)));c.buildTerms+=729;c.pairBuilds++;if(M.some(row=>row.some(v=>!Number.isFinite(v)||v<0)))throw Error('integrity');c.integrityChecks++;
 if(c.blocks.size+c.composed.size>=c.capacity){if(c.composed.size){c.composed.delete(c.composed.keys().next().value);c.pairEvictions++;}else{let victim=[...c.blocks.keys()].sort((x,y)=>c.total[parseInt(x,2)]-c.total[parseInt(y,2)]||c.last[parseInt(x,2)]-c.last[parseInt(y,2)])[0];c.blocks.delete(victim);c.archived.add(victim);c.evictions++;}}
 c.composed.set(key,M);c.childLast.set(key,c.clock);c.graduates++;c.events.push({clock:c.clock,key,event:'graduate',parents:[a,b],count:n.count,eligible:n.eligible,seeds:n.seeds.size});n.count=0;n.eligible=0;n.seeds.clear();
 }
 bank=M.map(row=>row.reduce((s,v,i)=>s+v*bank[i],0));const z=bank.reduce((a,b)=>a+b,0);bank=bank.map(v=>v/z);matrixMultiplies++;rawTokens+=24;encodedTokens++;cursor+=24;updates+=216;continue;
 }
 }
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
;return {run,buildCache};})();



export function experiment(start=28000,n=64,order=["stable","shift","recover","novel"]){
 const A=Uminus.buildCache(),B=Uplus.buildCache(),m=new Memsistor(),seen=new Set(),history=[],records=[],imported=new Map();let primary=0,extra=0,delta=0,probes=0,last=-Infinity,lastCost=0,uniqueImports=0;
 // Shadow records its own candidate encounters using the same source event identity.
 for(const scenario of order)for(let i=0;i<n;i++){
 const seed=start+i,ba=A.buildTerms,x=Uminus.run(seed,scenario,A),minus=3*x.scalarUpdates+81*x.matrixMultiplies+A.buildTerms-ba;primary+=minus;
 const raw=x.memory.map(v=>v.flip);let cursor=0;const batch=[];
 for(const f of x.ledger){if(!f.active)continue;while(cursor<f.cursor){if(f.cursor-cursor>=24){const e=Object.freeze({root:"ADA-synthetic-v1",scenario,seed,start:cursor+1,end:cursor+24,bits:raw.slice(cursor+1,cursor+25).join(""),route:"primary"});batch.push(e);records.push(e);m.ingest(e);}cursor+=f.cursor-cursor>=12?12:1;}}
 const k=history.length,admit=(k-last>=4||lastCost>0&&Math.abs(minus-lastCost)/lastCost>.25)&&extra+68000<=.15*primary;let plus=null;
 if(admit){
 // Import only completed earlier runs, never the current trial into its own nursery.
 // Shadow-local recurrence for the current trial is allowed; prior counts are refreshed from exact IDs.
 for(const e of records){if(e.scenario===scenario&&e.seed===seed)continue;const id=JSON.stringify([e.root,e.scenario,e.seed,e.start,e.end]);if(seen.has(id))continue;seen.add(id);let r=imported.get(e.bits);if(!r){r={count:0,seeds:new Set()};imported.set(e.bits,r);}r.count++;r.seeds.add(e.seed);uniqueImports++;}
 for(const [key,v] of imported){let r=B.nursery.get(key);if(!r){r={count:0,eligible:0,seeds:new Set(),first:B.clock};B.nursery.set(key,r);}r.count=v.count;r.seeds=new Set(v.seeds);}
 const bb=B.buildTerms,y=Uplus.run(seed,scenario,B);plus=3*y.scalarUpdates+81*y.matrixMultiplies+B.buildTerms-bb;extra+=plus;probes++;last=k;
 if(plus>68000||x.updates!==y.updates||x.forecasts!==y.forecasts)throw Error("invariant");
 for(let t=0;t<208;t++){if(raw[t]!==y.memory[t].flip)throw Error("ancestry");for(let j=0;j<26;j++)delta=Math.max(delta,Math.abs(x.ledger[t].prediction[j]-y.ledger[t].prediction[j]));}
 }
 history.push({seed,scenario,minus,plus});lastCost=minus;
 }
 const clean=m.snapshot(),repeated=new Memsistor(),reverse=new Memsistor(),conflict=new Memsistor();
 for(const e of records)for(const route of ["W1","W2","W3"])repeated.ingest({...e,route});
 for(const e of [...records].reverse())for(const route of ["W3","W1","W2"])reverse.ingest({...e,route});
 for(const e of records)conflict.ingest(e);
 const bad={...records[0],bits:(records[0].bits[0]==="0"?"1":"0")+records[0].bits.slice(1),route:"W3"};conflict.ingest(bad);conflict.ingest(bad);
 const same=(a,b)=>JSON.stringify(a.keys)===JSON.stringify(b.keys)&&a.valid===b.valid;
 if(!same(clean,repeated.snapshot())||!same(clean,reverse.snapshot())||conflict.snapshot().quarantined!==1||delta>1e-12||extra>.15*primary)throw Error("verification");
 return {primary,extra,probes,delta,graduates:B.graduates,descendantHits:B.pairHits,uniqueImports,clean,repeated:repeated.snapshot(),reverse:reverse.snapshot(),conflict:conflict.snapshot(),records,history};
}
