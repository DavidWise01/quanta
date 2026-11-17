// ADA-120 .dlw — causal 2-second AION prediction, deterministic synthetic fixture.
// One simulated second = one tick = one angular arcsecond, by convention only.
export function run(seed=120){
 let x=seed>>>0, q=0,velocity=1,previous=null,ledger=[],scores=[],pending=new Map(),stats={aion:0,hold:0,total:0},observed=[];
 function rng(){x=(Math.imul(x,1664525)+1013904223)>>>0;return x/4294967296;}
 for(let t=0;t<208;t++){
  if(t>0){if(rng()<.08)velocity=-velocity;q=(q+velocity+26)%26;}
  observed.push(q);
  const matured=pending.get(t);
  if(matured){const hit=matured.aion===q,hold=matured.hold===q;stats.aion+=Number(hit);stats.hold+=Number(hold);stats.total++;scores.push({issued:matured.issued,target:t,actual:q,hit,hold});pending.delete(t);}
  const d=previous===null?0:((q-previous+26)%26===1?1:-1);
  const record=Object.freeze({issued:t,target:t+2,source:q,velocity:d,aion:(q+2*d+26)%26,hold:q});
  ledger.push(record);pending.set(t+2,record);previous=q;
 }
 return {seed,stats,observed,ledger,scores,pending:[...pending.values()]};
}
export function test(){const fixture=run(),cases=Array.from({length:64},(_,i)=>run(120+i));const totals=cases.reduce((a,r)=>({aion:a.aion+r.stats.aion,hold:a.hold+r.stats.hold,total:a.total+r.stats.total}),{aion:0,hold:0,total:0});for(const r of cases){if(r.stats.total!==206||r.pending.length!==2)throw Error("horizon");for(const s of r.scores){if(s.target-s.issued!==2||s.actual!==r.observed[s.target]||r.ledger[s.issued].source!==r.observed[s.issued])throw Error("causality");}if(JSON.stringify(r)!==JSON.stringify(run(r.seed)))throw Error("replay");}return {fixture,totals,cases:cases.map(r=>({seed:r.seed,...r.stats})),seedCount:64};}

console.log(JSON.stringify(test(),null,2));