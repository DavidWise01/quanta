// ADA-123 .dlw — evidence gated AION, synthetic task; 1 tick = 1 simulated second.
export function forecast(q,d,p){const a=Array(26).fill(0);for(const [o,w] of [[2*d,(1-p)**2],[-2*d,p*(1-p)],[0,p]])a[(q+o+26)%26]+=w;return a;}
export function run(seed,scenario="shift"){let x=seed>>>0,q=0,d=1,w=0.02,mode="JIT",switches=0;const ledger=[],scores=[],memsistor=[],presist=[];let loss=0,otf=0;for(let t=0;t<208;t++){let flip=0;if(t){x=(Math.imul(x,1664525)+1013904223)>>>0;const p=scenario==="shift"&&t>=104||scenario==="recover"&&t>=69&&t<139?.45:.08;flip=Number(x/4294967296<p);if(flip)d=-d;q=(q+d+26)%26;const prior=w*.985+(1-w)*.015;const a=prior*(flip?.45:.55),b=(1-prior)*(flip?.08:.92);w=a/(a+b);}
const before=mode;if(w>=.8)mode="OTF";else if(w<=.2)mode="JIT";if(before!==mode)switches++;otf+=Number(mode==="OTF");
const predicted=(1-w)*.08+w*.45; // mixture of rate regimes, forecast marginalizes over a fixed regime for two ticks
const low=forecast(q,d,.08),high=forecast(q,d,.45),prediction=Object.freeze(low.map((v,i)=>(1-w)*v+w*high[i]));
if(t>=2){const f=ledger[t-2],err=f.prediction.reduce((a,v,i)=>a+(v-Number(i===q))**2,0);loss+=err;scores.push({issued:f.issued,target:t,actual:q,loss:err});}
const rec=Object.freeze({issued:t,target:t+2,q,w,mode,predicted,prediction});ledger.push(rec);presist.push({t,q,w,mode});if(presist.length>3)presist.shift();memsistor.push({t,flip,mode,posterior:w});}
return {seed,scenario,count:scores.length,loss,switches,otf,ledger,scores,presist,memsistor};}
