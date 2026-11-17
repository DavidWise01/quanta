// ADA-113 .dlw — neighbor-only flooding, deterministic distributed routing.
export function run(initial=[9,3,0,6,2,1,8,4,3]){
 const q=initial.slice(), n=9, adj=Array.from({length:n},()=>[]);
 for(let i=0;i<n;i++){for(const j of [3*Math.floor(i/3)+(i%3+1)%3,3*((Math.floor(i/3)+1)%3)+i%3]){adj[i].push(j);adj[j].push(i);}}
 const total=q.reduce((a,b)=>a+b,0), energy=()=>q.reduce((a,b)=>a+(9*b-total)**2,0);
 let messages=0,moves=0,epochs=0;const history=[q.slice()],events=[];
 while(true){
  // Each node starts with its own observation. Two synchronous neighbor rounds
  // suffice on this graph; no dedicated central observer.
  let views=q.map((v,i)=>new Map([[i,v]]));
  for(let r=0;r<2;r++){const next=views.map(v=>new Map(v));for(let i=0;i<n;i++)for(const j of adj[i]){messages++;for(const [k,v] of views[j])next[i].set(k,v);}views=next;}
  if(views.some(v=>v.size!==n))throw Error("incomplete view");
  const decisions=views.map(v=>{const a=[...v].sort((a,b)=>b[1]-a[1]||a[0]-b[0]),b=[...v].sort((a,b)=>a[1]-b[1]||a[0]-b[0]);return [a[0][0],b[0][0],a[0][1]-b[0][1]];});
  const [s,d,g]=decisions[0];if(decisions.some(v=>v.join()!=decisions[0].join()))throw Error("agreement");
  if(g<2)break;
  const parent=Array(n).fill(-1),queue=[s];parent[s]=s;
  for(let k=0;k<queue.length;k++)for(const v of [...adj[queue[k]]].sort((a,b)=>a-b))if(parent[v]<0){parent[v]=queue[k];queue.push(v);}
  const path=[d];while(path[0]!==s)path.unshift(parent[path[0]]);
  const before=energy();
  for(let k=0;k<path.length-1;k++){if(q[path[k]]<=0)throw Error("negative");q[path[k]]--;q[path[k+1]]++;moves++;}
  if(q.reduce((a,b)=>a+b,0)!==total||energy()>=before)throw Error("invariant");
  epochs++;events.push({epoch:epochs,path,before,after:energy()});history.push(q.slice());
 }
 return {initial,final:q,total,energy:energy(),epochs,moves,messages,history,events};
}
export function test(){const fixture=run(),corners=Array.from({length:9},(_,i)=>run(Array.from({length:9},(_,j)=>i===j?36:0)));let seed=113;const random=[];for(let k=0;k<64;k++){const q=Array(9).fill(0);for(let j=0;j<36;j++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;q[seed%9]++;}random.push(run(q));}if([fixture,...corners,...random].some(r=>r.energy!==0))throw Error("balance");return {fixture,corners,random};}

console.log(JSON.stringify(test(),null,2));
