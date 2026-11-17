// ADA-112 .dlw. Run with node ada112.mjs
export function run(mode="routed", initial=[9,3,0,6,2,1,8,4,3],steps=100){
 let q=initial.slice(), history=[q.slice()],moves=0;
 const edges=[],adj=Array.from({length:9},()=>[]);
 for(let f=0;f<3;f++)for(let k=0;k<3;k++){
  edges.push([3*k+f,3*((k+(f===1?2:1))%3)+f],[3*k+f,3*k+(f+1)%3]);
 }
 for(const [i,j] of edges){adj[i].push(j);adj[j].push(i);}
 const total=q.reduce((a,b)=>a+b,0);
 const energy=()=>q.reduce((a,b)=>a+(9*b-total)**2,0);
 function move(i,j){if(q[i]>0){q[i]--;q[j]++;moves++;}}
 for(let t=0;t<steps;t++){
  if(mode==="routed"){
   const i=q.indexOf(Math.max(...q)),j=q.indexOf(Math.min(...q));
   if(q[i]-q[j]>=2){
    const parent=Array(9).fill(-1),queue=[i];parent[i]=i;
    for(let k=0;k<queue.length;k++)for(const v of adj[queue[k]])if(parent[v]<0){parent[v]=queue[k];queue.push(v);}
    const path=[j];while(path[0]!==i)path.unshift(parent[path[0]]);
    for(let k=0;k<path.length-1;k++)move(path[k],path[k+1]);
   }
  }else for(const [i,j] of edges){
   if(mode==="fixed")move(i,j);
   else if(q[i]-q[j]>=2)move(i,j);else if(q[j]-q[i]>=2)move(j,i);
  }
  if(q.some(x=>x<0)||q.reduce((a,b)=>a+b,0)!==total)throw Error("conservation");
  history.push(q.slice());
 }
 return {initial,final:q,total,moves,energy:energy(),history};
}
export function test(){
 const modes=["fixed","local","routed"],results=Object.fromEntries(modes.map(m=>[m,run(m)]));
 const corners=Array.from({length:9},(_,i)=>{const q=Array(9).fill(0);q[i]=36;return Object.fromEntries(modes.map(m=>[m,run(m,q).energy]));});
 if(results.routed.energy!==0||corners.some(c=>c.routed!==0))throw Error("routed");
 return {results,corners};
}

console.log(JSON.stringify(test(),null,2));
