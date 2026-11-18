// ADA-124 .dlw — nine predictive manifestations, one AION nexus.
export const rates=[.02,.08,.14,.20,.28,.36,.45,.60,.80];
export function forecast(q,d,p){const a=Array(26).fill(0);for(const [o,w] of [[2*d,(1-p)**2],[-2*d,p*(1-p)],[0,p]])a[(q+o+26)%26]+=w;return a;}
export function run(seed,scenario="shift"){let x=seed>>>0,q=0,d=1,w=rates.map((_,i)=>i===1?.84:.02),loss=0,reactivations=0;const ledger=[],scores=[],memsistor=[],presist=[];let status=w.map(v=>v>=.15?"active":v<.03?"retired":"reserve");for(let t=0;t<208;t++){let flip=0;if(t){x=(Math.imul(x,1664525)+1013904223)>>>0;const p=scenario==="novel"? (t<70?.14:t<140?.60:.28):scenario==="shift"&&t>=104||scenario==="recover"&&t>=69&&t<139?.45:.08;flip=Number(x/4294967296<p);if(flip)d=-d;q=(q+d+26)%26;const u=w.map((v,i)=>(.985*v+.015/9)*(flip?rates[i]:1-rates[i]));const z=u.reduce((a,b)=>a+b,0);w=u.map(v=>v/z);}
const next=w.map(v=>v>=.15?"active":v<.03?"retired":"reserve");reactivations+=next.filter((v,i)=>v==="active"&&status[i]==="retired").length;status=next;
const prediction=Array(26).fill(0);for(let m=0;m<9;m++){const a=forecast(q,d,rates[m]);for(let j=0;j<26;j++)prediction[j]+=w[m]*a[j];}
if(t>=2){const f=ledger[t-2],err=f.prediction.reduce((a,v,i)=>a+(v-Number(i===q))**2,0);loss+=err;scores.push({issued:f.issued,target:t,actual:q,loss:err});}
const rec=Object.freeze({issued:t,target:t+2,q,weights:Object.freeze(w.slice()),status:Object.freeze(status.slice()),prediction:Object.freeze(prediction)});ledger.push(rec);presist.push({t,q,weights:w.slice()});if(presist.length>3)presist.shift();memsistor.push({t,flip,weights:w.slice(),status:status.slice()});}
return {seed,scenario,count:scores.length,loss,reactivations,ledger,scores,presist,memsistor};}
