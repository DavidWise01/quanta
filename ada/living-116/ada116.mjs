// ADA-116 .dlw — Hegemon source inf-+inf; visible shadow (inf) - + [inf]
// One simulated communication round = one angular arcsecond of model phase.
// No physical equivalence between angle and Planck time is asserted.
// ADA-115 .dlw — Hegemon visible source: (inf) - + [inf]
// Reliable barrier manifest assumed; unreliable observation links.
export function run(initial=[9,3,0,6,2,1,8,4,3],seed=115,mode="fault",cut=Infinity,restore=null){
 const q=initial.slice(),n=9,adj=Array.from({length:n},()=>[]);
 for(let i=0;i<n;i++)for(const j of [3*Math.floor(i/3)+(i%3+1)%3,3*((Math.floor(i/3)+1)%3)+i%3]){adj[i].push(j);adj[j].push(i);}
 const total=q.reduce((a,b)=>a+b,0),energy=()=>q.reduce((a,b)=>a+(9*b-total)**2,0);
 const views=q.map((v,i)=>new Map([[i,{id:i,version:0,value:v}]])),versions=Array(n).fill(0);
 let messages=0,lost=0,delayed=0,duplicates=0,stale=0,retries=0,epochs=0,moves=0,round=0,queue=[],blocked=false;
 const history=[q.slice()],events=[];
 if(restore){q.splice(0,n,...restore.q);seed=restore.seed;mode=restore.mode;versions.splice(0,n,...restore.versions);restore.views.forEach((v,i)=>{views[i]=new Map(v)});({messages,lost,delayed,duplicates,stale,retries,epochs,moves,round,queue,blocked}=restore);history.splice(0,history.length,...restore.history);events.splice(0,events.length,...restore.events);}
 function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;}
 function send(i,j,v){messages++;let p=rng();if(mode==="partition"||mode==="fault"&&p<.25){lost++;return;}
 let delay=mode==="fault"&&p<.50?3:1;if(delay>1)delayed++;
 queue.push({j,v,due:round+delay});if(mode==="fault"&&rng()<.2){duplicates++;queue.push({j,v,due:round+delay+1});}}
 function receive(j,v){const prev=views[j].get(v.id);if(prev&&prev.version>=v.version){stale++;return;}views[j].set(v.id,v);}
 function reconcile(ids){
 for(let attempt=0;attempt<=40;attempt++){
  if(views.every(w=>ids.every(i=>w.get(i)?.version===versions[i])))return true;
  if(attempt===40)return false;
  if(attempt>0)retries++;
  for(let i=0;i<n;i++)for(const j of adj[i])for(const k of ids){const v=views[i].get(k);if(v?.version===versions[k])send(i,j,v);}
  round++;
  const ready=queue.filter(p=>p.due<=round);queue=queue.filter(p=>p.due>round);
  for(const p of ready)receive(p.j,p.v);
 }return false;
 }
 if(!restore&&!reconcile([...q.keys()]))blocked=true;
 while(!blocked&&epochs<cut){
  const decisions=views.map(w=>{const a=[...w.values()].sort((a,b)=>b.value-a.value||a.id-b.id),b=[...w.values()].sort((a,b)=>a.value-b.value||a.id-b.id);return [a[0].id,b[0].id,a[0].value-b[0].value];});
  const [s,d,g]=decisions[0];if(decisions.some(v=>v.join()!=decisions[0].join()))throw Error("disagreement");
  if(g<2)break;
  const parent=Array(n).fill(-1),bfs=[s];parent[s]=s;
  for(let k=0;k<bfs.length;k++)for(const v of [...adj[bfs[k]].sort((a,b)=>a-b)])if(parent[v]<0){parent[v]=bfs[k];bfs.push(v);}
  const path=[d];while(path[0]!==s)path.unshift(parent[path[0]]);
  const before=energy(),start=messages;
  for(let k=0;k<path.length-1;k++){if(q[path[k]]<=0)throw Error("negative");q[path[k]]--;q[path[k+1]]++;moves++;}
  if(q.reduce((a,b)=>a+b,0)!==total||energy()>=before)throw Error("invariant");
  for(const i of [s,d])views[i].set(i,{id:i,version:++versions[i],value:q[i]});
  epochs++;history.push(q.slice());
  blocked=!reconcile([s,d]);events.push({epoch:epochs,path,before,after:energy(),attempted:messages-start,confirmed:!blocked});
 }
 const clock={turn:Math.floor(round/1296000),arcsecond:round%1296000};
 const checkpoint={q,seed,mode,versions,views:views.map(v=>[...v]),messages,lost,delayed,duplicates,stale,retries,epochs,moves,round,queue,blocked,history,events};
 return {initial,final:q,total,energy:energy(),epochs,moves,messages,lost,delayed,duplicates,stale,retries,round,blocked,history,events,clock,checkpoint};
}

export function test(){
 let seed=113;const inputs=[[9,3,0,6,2,1,8,4,3],...Array.from({length:9},(_,i)=>Array.from({length:9},(_,j)=>i===j?36:0))];
 for(let k=0;k<64;k++){const q=Array(9).fill(0);for(let j=0;j<36;j++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;q[seed%9]++;}inputs.push(q);}
 let cuts=0,pending=0;const cases=[];
 for(let i=0;i<inputs.length;i++){const q=inputs[i],s=115+i,full=run(q,s);if(full.blocked||full.energy!==0)throw Error("fixture");for(let cut=0;cut<=full.epochs;cut++){const pre=run(q,s,"fault",cut),cp=JSON.parse(JSON.stringify(pre.checkpoint));if(cp.queue.length)pending++;const resumed=run(q,s,"fault",Infinity,cp);if(JSON.stringify(full)!==JSON.stringify(resumed))throw Error("continuity "+i+" "+cut);cuts++;}cases.push({initial:q,seed:s,epochs:full.epochs,arcseconds:full.round,cuts:full.epochs+1});}
 const fixture=run(),partition=run(undefined,115,"partition"),restored=run(undefined,115,"partition",Infinity,JSON.parse(JSON.stringify(partition.checkpoint)));if(JSON.stringify(partition)!==JSON.stringify(restored))throw Error("blocked restore");
 const negative=run(undefined,115,"fault",5),damaged=JSON.parse(JSON.stringify(negative.checkpoint));damaged.queue=[];const divergent=run(undefined,115,"fault",Infinity,damaged);return {cases,cuts,pending,fixture,partitionPreserved:true,omittedQueueDetected:JSON.stringify(divergent)!==JSON.stringify(fixture)};
}

console.log(JSON.stringify(test(),null,2));
