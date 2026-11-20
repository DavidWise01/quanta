// ADA-159B .dlw — 42-bit Stargate, three-layer tornado.
export const GATE="00 11 [ 24 /|\\ 42 ] 11 00";
export const WIDTH=42, TURN=1296000000, OFFSET=1025;
export const LAYERS=Object.freeze(["|V| vector","[] voxel","{[()]} vogel"]);
export function pack(s,c,i,w){const a=[s,c,i,w],n=[24,9,1,8];if(a.some((v,j)=>typeof v!=="bigint"||v<0n||v>=1n<<BigInt(n[j])))throw Error("width");return s|(c<<24n)|(i<<33n)|(w<<34n);}
export function unpack(v){if(typeof v!=="bigint"||v<0n||v>=1n<<42n)throw Error("width");return [v&0xffffffn,(v>>24n)&511n,(v>>33n)&1n,(v>>34n)&255n];}


 // ADA-159D .dlw — mirrored, equal-time antistrophic pairs.
export const FRAME=Object.freeze([{name:"vector",hand:1,phase:0},{name:"voxel",hand:-1,phase:2},{name:"vogel",hand:1,phase:4}].map(Object.freeze));
const wrap=a=>((a%TURN)+TURN)%TURN;
export function initial(){return {tick:0,x:null,layers:[1,-1].flatMap(side=>FRAME.map((f,i)=>({...f,side,hand:f.hand*side,angle:wrap(side*i*TURN/3),net:0,push:0,pull:0,travel:0})))};}
export function step(s,x){if(!Number.isSafeInteger(x)||x<0||x>TURN)throw Error("x in milliarcseconds");const latched=s.tick%8===0?x:s.x;
 return {tick:s.tick+1,x:latched,layers:s.layers.map(l=>{const p=(s.tick+l.phase)%8,pull=p>=4,local=pull?-(latched+OFFSET):latched,delta=l.hand*local;
 return {...l,p,delta,angle:wrap(l.angle+delta),net:l.net+delta,push:l.push+Number(!pull),pull:l.pull+Number(pull),travel:l.travel+Math.abs(delta)};})};}
export function check(s){for(let i=0;i<3;i++){const a=s.layers[i],b=s.layers[i+3];if(a.net+b.net!==0||a.delta+b.delta!==0||wrap(a.angle+b.angle)!==0||a.push!==b.push||a.pull!==b.pull||a.travel!==b.travel)throw Error("mirror");}if(s.layers.reduce((v,l)=>v+l.net,0)!==0)throw Error("net");}

// ADA-159E .dlw — bounded pairwise homeostasis, one-tick observation delay.
export const CAP=1025;
export function homeInitial(){return {...initial(),correction:0,disturbance:0,errors:[0,0,0]};}
export function homeStep(s,x,dist=[0,0,0],cap=CAP){
 if(!Number.isSafeInteger(cap)||cap<0||cap>TURN||dist.length!==3||dist.some(d=>!Number.isSafeInteger(d)||Math.abs(d)>TURN))throw Error("input");
 const base=step(s,x),commands=s.errors.map(e=>-Math.sign(e)*Math.min(Math.abs(e),cap));
 const layers=base.layers.map((l,i)=>{const d=i<3?dist[i]:commands[i-3];return {...l,nominal:l.delta,delta:l.delta+d,angle:wrap(l.angle+d),net:l.net+d,travel:l.travel-Math.abs(l.delta)+Math.abs(l.delta+d),adjustment:d};});
 const errors=layers.slice(0,3).map((l,i)=>l.net+layers[i+3].net);
 return {...base,layers,errors,commands,dist:[...dist],correction:s.correction+commands.reduce((a,b)=>a+Math.abs(b),0),disturbance:s.disturbance+dist.reduce((a,b)=>a+Math.abs(b),0)};
}

// ADA-159F .dlw — local priority, transferable per-tick correction capacity.
export function allocate(errors,cap=CAP){const own=errors.map(e=>Math.min(Math.abs(e),cap)),extra=[0,0,0];let reserve=3*cap-own.reduce((a,b)=>a+b,0),initialReserve=reserve;
 const order=[0,1,2].sort((a,b)=>(Math.abs(errors[b])-own[b])-(Math.abs(errors[a])-own[a])||a-b);
 for(const i of order){extra[i]=Math.min(reserve,Math.abs(errors[i])-own[i]);reserve-=extra[i];}
 return {own,extra,initialReserve,reserve,commands:errors.map((e,i)=>-Math.sign(e)*(own[i]+extra[i]))};}
export function sharedStep(s,x,dist=[0,0,0],cap=CAP){
 if(!Number.isSafeInteger(cap)||cap<0||cap>TURN||dist.length!==3||dist.some(d=>!Number.isSafeInteger(d)||Math.abs(d)>TURN))throw Error("input");
 const base=step(s,x),allocation=allocate(s.errors,cap),commands=allocation.commands;
 const layers=base.layers.map((l,i)=>{const d=i<3?dist[i]:commands[i-3];return {...l,nominal:l.delta,delta:l.delta+d,angle:wrap(l.angle+d),net:l.net+d,travel:l.travel-Math.abs(l.delta)+Math.abs(l.delta+d),adjustment:d};});
 const errors=layers.slice(0,3).map((l,i)=>l.net+layers[i+3].net);
 return {...base,layers,errors,commands,allocation,dist:[...dist],correction:s.correction+commands.reduce((a,b)=>a+Math.abs(b),0),disturbance:s.disturbance+dist.reduce((a,b)=>a+Math.abs(b),0)};
}
const norm=a=>a.reduce((s,v)=>s+Math.abs(v),0);
export function verify(){let ticks=0,pairs=0,bitChecks=0,impulses=0,random=0;const cases=[];
 function advance(s,d,cap=CAP,x=1000){const q=sharedStep(s,x,d,cap),a=q.allocation;if(norm(q.commands)!==Math.min(norm(s.errors),3*cap)||a.reserve!==3*cap-norm(q.commands)||a.extra.reduce((a,b)=>a+b,0)>a.initialReserve)throw Error("capacity");
 for(let i=0;i<3;i++){if(q.errors[i]!==s.errors[i]+d[i]+q.commands[i]||Math.abs(q.commands[i])<Math.min(Math.abs(s.errors[i]),cap)||Math.abs(q.commands[i])>Math.abs(s.errors[i])||wrap(q.layers[i].angle+q.layers[i+3].angle)!==wrap(q.errors[i]))throw Error("pair");pairs++;}ticks++;return q;}
 for(const d of [[4100,0,0],[4100,-4100,4100],[0,-1026,0],[1,2,-3],[10000,0,-512]])for(const cap of [1,512,1025,2050]){if(cap===1&&norm(d)>100)continue;let a=advance(homeInitial(),d,cap),b=homeStep(homeInitial(),1000,d,cap);let n=0,m=0;while(norm(a.errors)){a=advance(a,[0,0,0],cap);n++;}while(norm(b.errors)){b=homeStep(b,1000,[0,0,0],cap);m++;}if(n!==Math.ceil(norm(d)/(3*cap))||n>m)throw Error("drain");impulses++;cases.push({dist:d,cap,shared:n,local:m});}
 const scenarios=[];for(const d of [[2050,0,0],[3075,0,0],[4100,0,0],[1025,-1025,1025],[2050,-2050,0],[512,-1025,1538]]){let a=homeInitial(),b=homeInitial();const trace=[];for(let j=0;j<32;j++){a=advance(a,d);b=homeStep(b,1000,d);trace.push({tick:j+1,shared:norm(a.errors),local:norm(b.errors)});}const expected=norm(d)+31*Math.max(0,norm(d)-3*CAP);if(norm(a.errors)!==expected)throw Error("persistent");scenarios.push({dist:d,shared:norm(a.errors),local:norm(b.errors),trace});}
 let s=homeInitial(),seed=159;for(let j=0;j<4096;j++){const d=Array.from({length:3},()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%8193-4096;});s=advance(s,d,seed%3076,seed%100000);random++;}
 for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");bitChecks++;}
 return {ticks,pairs,bitChecks,impulses,random,cases,scenarios};}
