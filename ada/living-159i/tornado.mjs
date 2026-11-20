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

// ADA-159G .dlw — finite, lossless symbolic reserve with bounded discharge.
export const STORAGE=24600, RELEASE=3075;
export function reserveInitial(){return {...homeInitial(),bank:0,charged:0,drawn:0,spill:0};}
export function reserveStep(s,x,dist=[0,0,0],cap=CAP,limit=STORAGE,release=RELEASE){
 if([cap,limit,release].some(v=>!Number.isSafeInteger(v)||v<0||v>TURN)||s.bank>limit||s.bank<0||dist.length!==3||dist.some(d=>!Number.isSafeInteger(d)||Math.abs(d)>TURN))throw Error("input");
 const base=step(s,x),a=allocate(s.errors,cap),commands=[...a.commands],demand=norm(s.errors),current=norm(commands);
 let draw=Math.min(s.bank,release,demand-current),left=draw;
 const order=[0,1,2].sort((i,j)=>(Math.abs(s.errors[j])-Math.abs(commands[j]))-(Math.abs(s.errors[i])-Math.abs(commands[i]))||i-j);
 for(const i of order){const n=Math.min(left,Math.abs(s.errors[i])-Math.abs(commands[i]));commands[i]-=Math.sign(s.errors[i])*n;left-=n;}
 const unused=3*cap-current,charge=Math.min(unused,limit-s.bank+draw),spill=unused-charge,bank=s.bank-draw+charge;
 const layers=base.layers.map((l,i)=>{const d=i<3?dist[i]:commands[i-3];return {...l,nominal:l.delta,delta:l.delta+d,angle:wrap(l.angle+d),net:l.net+d,travel:l.travel-Math.abs(l.delta)+Math.abs(l.delta+d),adjustment:d};});
 return {...base,layers,errors:layers.slice(0,3).map((l,i)=>l.net+layers[i+3].net),commands,dist:[...dist],bank,charge,draw,overflow:spill,charged:s.charged+charge,drawn:s.drawn+draw,spill:s.spill+spill,correction:s.correction+norm(commands),disturbance:s.disturbance+norm(dist)};
}

// ADA-159H .dlw — causal two-transition forecast, frozen before actual input.
export function forecast(history){const z=[0,0,0],a=history.at(-2)??history.at(-1)??z,b=history.at(-1)??z;return [[...a],[...b]];}
export function plan(s,x,history){const predicted=forecast(history),maximum=Math.min(s.bank,RELEASE,Math.max(0,norm(s.errors)-3*CAP));
 const candidates=[...new Set([maximum,Math.floor(maximum/2),0])];let chosen=null;
 for(const release of candidates){const a=reserveStep(s,x,predicted[0],CAP,STORAGE,release),b=reserveStep(a,x,predicted[1]);const score=4*(norm(a.errors)+norm(b.errors))+(STORAGE-b.bank);
 if(!chosen||score<chosen.score)chosen={release,score,predicted,expected:[norm(a.errors),norm(b.errors)],bank:b.bank};}
 return Object.freeze({...chosen,predicted:Object.freeze(chosen.predicted.map(Object.freeze)),expected:Object.freeze(chosen.expected)});
}

// ADA-159I .dlw — causal rolling confidence on active forecasts.
export const WINDOW=8;
export function gate(scores){if(scores.length<4)return 0;const hits=scores.reduce((s,v)=>s+v,0);return hits*4>=scores.length*3?1:hits*2<=scores.length?-1:0;}
export function verify(){let ticks=0,pairs=0,accounts=0,bitChecks=0,states=[0,0,0],authorized=0,withheld=0;const scenarios=[];
 function run(name,inputs){let a=reserveInitial(),b=reserveInitial(),c=reserveInitial(),history=[],scores=[],trace=[],sumA=0,sumB=0,sumC=0,counts=[0,0,0],active=0;
 for(const d of inputs){const g=gate(scores),p=plan(a,1000,history),u=plan(b,1000,history),release=g===1?p.release:RELEASE;
 const q=reserveStep(a,1000,d,CAP,STORAGE,release);b=reserveStep(b,1000,d,CAP,STORAGE,u.release);c=reserveStep(c,1000,d);
 states[g+1]++;counts[g+1]++;if(g===1)authorized++;if(g===1&&p.release<Math.min(a.bank,RELEASE,Math.max(0,norm(a.errors)-3*CAP)))withheld++;
 if(q.bank!==a.bank+q.charge-q.draw||q.bank<0||q.bank>STORAGE||norm(q.commands)+q.charge+q.overflow!==3*CAP+q.draw||q.draw>release)throw Error("ledger");accounts++;
 for(let i=0;i<3;i++){if(q.errors[i]!==a.errors[i]+d[i]+q.commands[i]||Math.abs(q.commands[i])>Math.abs(a.errors[i])||wrap(q.layers[i].angle+q.layers[i+3].angle)!==wrap(q.errors[i]))throw Error("pair");pairs++;}
 // Ignore jointly quiet observations: silence must not grant active predictive authority.
 const pred=p.predicted[0];if(norm(pred)||norm(d)){scores.push(Number(pred.every((v,i)=>v===d[i])));if(scores.length>WINDOW)scores.shift();active++;}
 a=q;history.push([...d]);if(history.length>2)history.shift();const ea=norm(a.errors),eb=norm(b.errors),ec=norm(c.errors);sumA+=ea;sumB+=eb;sumC+=ec;ticks++;trace.push({tick:a.tick,gate:g,actual:d,predicted:pred,confidence:scores.length?scores.reduce((s,v)=>s+v,0)/scores.length:null,gated:ea,anticipatory:eb,greedy:ec,bank:a.bank});}
 return {name,sumA,sumB,sumC,counts,active,bankA:a.bank,bankB:b.bank,bankC:c.bank,trace};}
 const quiet=Array.from({length:8},()=>[0,0,0]);let seed=159;
 const patterns=[["constant",i=>[6150,0,0]],["alternating",i=>[i%2?-6150:6150,0,0]],["two-on-two-off",i=>[i%4<2?6150:0,0,0]],["step-reversal",i=>[i<16?6150:-6150,0,0]],["three-pair reversal",i=>[i%2?-4100:4100,i%2?2050:-2050,1025]],["unpredictable",i=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return [seed%18451-9225,0,0];}]];
 for(const [name,fn] of patterns)scenarios.push(run(name,[...quiet,...Array.from({length:64},(_,i)=>fn(i)),...quiet]));
 const randomCases=[];for(let j=0;j<64;j++){const inputs=[...quiet,...Array.from({length:64},()=>Array.from({length:3},()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%8193-4096;})),...quiet];const {trace,...r}=run("random-"+j,inputs);randomCases.push(r);}
 for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");bitChecks++;}
 return {ticks,pairs,accounts,bitChecks,states,authorized,withheld,scenarios,randomCases};}
