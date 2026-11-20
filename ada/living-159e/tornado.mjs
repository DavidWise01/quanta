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
export function verify(){let ticks=0,pairs=0,impulses=0,overloads=0,bitChecks=0;let sample=[];
 function advance(s,x,d,c=CAP){const q=homeStep(s,x,d,c);for(let i=0;i<3;i++){const expected=s.errors[i]+d[i]-Math.sign(s.errors[i])*Math.min(Math.abs(s.errors[i]),c);if(q.errors[i]!==expected||Math.abs(q.commands[i])>c||wrap(q.layers[i].angle+q.layers[i+3].angle)!==wrap(expected))throw Error("recurrence");pairs++;}if(q.layers.some(l=>l.angle<0||l.angle>=TURN))throw Error("wrap");ticks++;return q;}
 for(const x of [0,1000,1025,10000,TURN-1])for(const magnitude of [1,1025,1026,4100,10000])for(const sign of [-1,1]){let s=homeInitial();const d=[sign*magnitude,-sign*magnitude,sign*magnitude];s=advance(s,x,d);if(s.errors.some((e,i)=>e!==d[i]))throw Error("delay");const n=Math.ceil(magnitude/CAP);for(let j=1;j<=n;j++){s=advance(s,x,[0,0,0]);if(j<n&&s.errors.every(e=>e===0))throw Error("early");}if(s.errors.some(Boolean))throw Error("recovery");impulses++;}
 for(const d of [512,1025,2050,4100]){let s=homeInitial();for(let j=0;j<32;j++)s=advance(s,1000,[d,-d,d]);const expected=d+31*Math.max(0,d-CAP);if(s.errors[0]!==expected)throw Error("persistent");if(d>CAP)overloads++;for(let j=0;j<Math.ceil(expected/CAP);j++)s=advance(s,1000,[0,0,0]);if(s.errors.some(Boolean))throw Error("drain");}
 let s=homeInitial();for(let j=0;j<16;j++){s=advance(s,1000,j===2?[4100,0,0]:[0,0,0]);sample.push({tick:s.tick,errors:s.errors,commands:s.commands,dist:s.dist,layers:s.layers});}
 for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");bitChecks++;}
 return {ticks,pairs,impulses,overloads,bitChecks,sample};}
