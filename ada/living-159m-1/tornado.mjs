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

// ADA-159J .dlw — matched-state counterfactual action scores, two-tick delayed settlement.
export const UTILITY_WINDOW=8;
export function authority(scores){if(scores.length<4)return 0;const v=scores.reduce((a,b)=>a+b,0);return v>0?1:v<0?-1:0;}
export function shadowIssue(s,history,scores){const p=plan(s,1000,history),max=Math.min(s.bank,RELEASE,Math.max(0,norm(s.errors)-3*CAP));return Object.freeze({tick:s.tick,reactive:max,anticipatory:p.release,gate:authority(scores),state:s,informative:p.release!==max});}
export function settle(ticket,d1,d2){const a=reserveStep(ticket.state,1000,d1,CAP,STORAGE,ticket.reactive),b=reserveStep(ticket.state,1000,d1,CAP,STORAGE,ticket.anticipatory),a2=reserveStep(a,1000,d2),b2=reserveStep(b,1000,d2);const cost=(q,r)=>4*(norm(q.errors)+norm(r.errors))+STORAGE-r.bank;return cost(a,a2)-cost(b,b2);}

// ADA-159K .dlw — three matched-state horizons, settlement after actual observations.
export const SCALES=Object.freeze([5,8,13]);
export function scaleGate(scores){const v=scores.map(authority);return v.every(x=>x===1)?1:v.some(x=>x===-1)?-1:0;}
export function advanceShadow(p,d){const a=reserveStep(p.a,1000,d,CAP,STORAGE,p.age===0?p.reactive:RELEASE),b=reserveStep(p.b,1000,d,CAP,STORAGE,p.age===0?p.anticipatory:RELEASE);return {...p,a,b,age:p.age+1,area:p.area+norm(a.errors)-norm(b.errors)};}
export function session(){return {live:reserveInitial(),greedy:reserveInitial(),anti:reserveInitial(),two:reserveInitial(),hist:[],scores:[[],[],[]],short:[],pending:[],p2:null,sums:[0,0,0,0]};}
export function evolve(s,d){const g=scaleGate(s.scores),t=shadowIssue(s.live,s.hist,[]),tt=shadowIssue(s.two,s.hist,s.short),release=g===1?t.anticipatory:t.reactive,live=reserveStep(s.live,1000,d,CAP,STORAGE,release),greedy=reserveStep(s.greedy,1000,d),anti=reserveStep(s.anti,1000,d,CAP,STORAGE,plan(s.anti,1000,s.hist).release),two=reserveStep(s.two,1000,d,CAP,STORAGE,tt.gate===1?tt.anticipatory:tt.reactive);
 const scores=s.scores.map(v=>[...v]),short=[...s.short],done=[],pending=[...s.pending];let rollouts=0;if(t.informative)pending.push({a:s.live,b:s.live,reactive:t.reactive,anticipatory:t.anticipatory,age:0,area:0,tick:s.live.tick,signs:[]});
 const next=pending.map(p=>{const v=advanceShadow(p,d);rollouts+=2;if(v.age!==live.tick-v.tick)throw Error("causality");const k=SCALES.indexOf(v.age);if(k>=0){const gain=4*v.area+v.b.bank-v.a.bank;scores[k].push(gain);if(scores[k].length>8)scores[k].shift();v.signs=[...p.signs,Math.sign(gain)];done.push({k,gain,signs:v.signs,tick:v.tick});}return v;}).filter(v=>v.age<13);
 if(s.p2&&s.p2.ticket.informative){short.push(settle(s.p2.ticket,s.p2.actual,d));if(short.length>8)short.shift();}
 if(live.bank!==s.live.bank+live.charge-live.draw||norm(live.commands)+live.charge+live.overflow!==3*CAP+live.draw||live.draw>release||live.bank<0||live.bank>STORAGE)throw Error("ledger");
 for(let i=0;i<3;i++)if(live.errors[i]!==s.live.errors[i]+d[i]+live.commands[i]||wrap(live.layers[i].angle+live.layers[i+3].angle)!==wrap(live.errors[i]))throw Error("pair");
 return {live,greedy,anti,two,hist:[...s.hist,[...d]].slice(-2),scores,short,pending:next,p2:{ticket:tt,actual:[...d]},sums:[live,greedy,anti,two].map((v,i)=>s.sums[i]+norm(v.errors)),g,release,issued:t.informative,withheld:release<t.reactive,done,rollouts};}

// ADA-159L .dlw — adaptive SeeSaw; each horizon votes on the same completed ticket.
export function balance(scores,weights){if(scores.some(v=>v.length<4))return 0;const u=scores.map(v=>{const m=v.reduce((a,b)=>a+b,0),n=v.reduce((a,b)=>a+Math.abs(b),0);return n?m/n:0;});const value=u.reduce((a,b,k)=>a+b*weights[k],0);return Math.sign(value);}
export function learnWeights(weights,signs){const target=signs[2];return weights.map((w,k)=>Math.max(1,Math.min(16,w+(signs[k]===target?1:-1))));}
export function seesawSession(){return {...session(),weights:[4,4,4]};}
export function seesawStep(s,d){const g=balance(s.scores,s.weights),t=shadowIssue(s.live,s.hist,[]),release=g===1?t.anticipatory:t.reactive,live=reserveStep(s.live,1000,d,CAP,STORAGE,release);
 const scores=s.scores.map(v=>[...v]),done=[],pending=[...s.pending];let weights=[...s.weights],rollouts=0;if(t.informative)pending.push({a:s.live,b:s.live,reactive:t.reactive,anticipatory:t.anticipatory,age:0,area:0,tick:s.live.tick,signs:[]});
 const next=pending.map(p=>{const v=advanceShadow(p,d);rollouts+=2;if(v.age!==live.tick-v.tick)throw Error("causality");const k=SCALES.indexOf(v.age);if(k>=0){const gain=4*v.area+v.b.bank-v.a.bank;scores[k].push(gain);if(scores[k].length>8)scores[k].shift();v.signs=[...p.signs,Math.sign(gain)];done.push({k,gain,signs:v.signs,tick:v.tick});if(k===2)weights=learnWeights(weights,v.signs);}return v;}).filter(v=>v.age<13);
 if(live.bank!==s.live.bank+live.charge-live.draw||norm(live.commands)+live.charge+live.overflow!==3*CAP+live.draw||live.draw>release||live.bank<0||live.bank>STORAGE)throw Error("ledger");
 for(let i=0;i<3;i++)if(live.errors[i]!==s.live.errors[i]+d[i]+live.commands[i]||wrap(live.layers[i].angle+live.layers[i+3].angle)!==wrap(live.errors[i]))throw Error("pair");
 if(weights.some(w=>w<1||w>16))throw Error("weights");
 return {...s,live,hist:[...s.hist,[...d]].slice(-2),scores,weights,pending:next,g,release,issued:t.informative,withheld:release<t.reactive,done,rollouts};}
export function experiment(seed=159){let ticks=0,issued=0,rollouts=0,withheld=0,completed=0,states=[0,0,0],settled=[0,0,0],weightsSum=[0,0,0];
 function run(name,inputs,keep=false){let s=seesawSession(),k=session(),trace=[],sum=0;for(const d of inputs){s=seesawStep(s,d);k=evolve(k,d);sum+=norm(s.live.errors);ticks++;issued+=Number(s.issued);withheld+=Number(s.withheld);rollouts+=s.rollouts;states[s.g+1]++;for(const v of s.done){settled[v.k]++;if(v.k===2)completed++;}if(keep)trace.push({tick:s.live.tick,gate:s.g,weights:s.weights,bank:s.live.bank,error:norm(s.live.errors),settled:s.done});}s.weights.forEach((v,i)=>weightsSum[i]+=v);return {name,sums:[sum,...k.sums],weights:s.weights,pending:s.pending.length,trace};}
 const quiet=Array.from({length:8},()=>[0,0,0]);let x=seed>>>0;const rand=()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x;};
 const suite=[["constant",i=>[6150,0,0]],["alternating",i=>[i%2?-6150:6150,0,0]],["two-on-two-off",i=>[i%4<2?6150:0,0,0]],["step-reversal",i=>[i<16?6150:-6150,0,0]],["three-pair reversal",i=>[i%2?-4100:4100,i%2?2050:-2050,1025]],["unpredictable",i=>[rand()%18451-9225,0,0]],["pattern-to-noise",i=>[i<32?(i%2?-6150:6150):rand()%18451-9225,0,0]]];
 const scenarios=suite.map(([name,f])=>run(name,[...quiet,...Array.from({length:64},(_,i)=>f(i)),...quiet],true));const cases=[];for(let j=0;j<64;j++){const {trace,...v}=run("random-"+j,[...quiet,...Array.from({length:64},()=>Array.from({length:3},()=>rand()%8193-4096)),...quiet]);cases.push(v);}
 const sums=[0,0,0,0,0],comparisons=[1,2,3,4].map(()=>[0,0,0]);for(const v of cases){v.sums.forEach((n,i)=>sums[i]+=n);for(let i=1;i<5;i++)comparisons[i-1][v.sums[0]<v.sums[i]?0:v.sums[0]>v.sums[i]?1:2]++;}
 for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");}
 if(issued!==completed+[...scenarios,...cases].reduce((a,v)=>a+v.pending,0))throw Error("tickets");
 return {seed,ticks,pairs:3*ticks,issued,completed,rollouts,withheld,states,settled,weightsSum,bitChecks:42,sums,comparisons,scenarios,cases};}

// ADA-159M .dlw — alternating evaluator orientation, no self reward.
export function rotateWeights(weights,signs,turn){const dir=turn%2===0?1:2;return weights.map((w,k)=>Math.max(1,Math.min(16,w+(signs[k]===signs[(k+dir)%3]?1:-1))));}
export function mobiusStep(s,d){const g=balance(s.scores,s.weights),t=shadowIssue(s.live,s.hist,[]),release=g===1?t.anticipatory:t.reactive,live=reserveStep(s.live,1000,d,CAP,STORAGE,release);
 const scores=s.scores.map(v=>[...v]),done=[],pending=[...s.pending];let weights=[...s.weights],rollouts=0,turn=s.turn??0;if(t.informative)pending.push({a:s.live,b:s.live,reactive:t.reactive,anticipatory:t.anticipatory,age:0,area:0,tick:s.live.tick,signs:[]});
 const next=pending.map(p=>{const v=advanceShadow(p,d);rollouts+=2;if(v.age!==live.tick-v.tick)throw Error("causality");const k=SCALES.indexOf(v.age);if(k>=0){const gain=4*v.area+v.b.bank-v.a.bank;scores[k].push(gain);if(scores[k].length>8)scores[k].shift();v.signs=[...p.signs,Math.sign(gain)];done.push({k,gain,signs:v.signs,tick:v.tick});if(k===2){weights=rotateWeights(weights,v.signs,turn);turn++;}}return v;}).filter(v=>v.age<13);
 if(live.bank!==s.live.bank+live.charge-live.draw||norm(live.commands)+live.charge+live.overflow!==3*CAP+live.draw||live.draw>release||live.bank<0||live.bank>STORAGE)throw Error("ledger");
 for(let i=0;i<3;i++)if(live.errors[i]!==s.live.errors[i]+d[i]+live.commands[i]||wrap(live.layers[i].angle+live.layers[i+3].angle)!==wrap(live.errors[i]))throw Error("pair");
 if(weights.some(w=>w<1||w>16))throw Error("weights");
 return {...s,turn,live,hist:[...s.hist,[...d]].slice(-2),scores,weights,pending:next,g,release,issued:t.informative,withheld:release<t.reactive,done,rollouts};}
export function mobiusExperiment(seed=159){let ticks=0,issued=0,rollouts=0,withheld=0,completed=0,states=[0,0,0],settled=[0,0,0],weightsSum=[0,0,0];
 function run(name,inputs,keep=false){let s=seesawSession(),k=session(),prior=seesawSession(),trace=[],sum=0,priorSum=0;for(const d of inputs){s=mobiusStep(s,d);prior=seesawStep(prior,d);priorSum+=norm(prior.live.errors);k=evolve(k,d);sum+=norm(s.live.errors);ticks++;issued+=Number(s.issued);withheld+=Number(s.withheld);rollouts+=s.rollouts;states[s.g+1]++;for(const v of s.done){settled[v.k]++;if(v.k===2)completed++;}if(keep)trace.push({tick:s.live.tick,gate:s.g,weights:s.weights,bank:s.live.bank,error:norm(s.live.errors),settled:s.done});}s.weights.forEach((v,i)=>weightsSum[i]+=v);return {name,sums:[sum,...k.sums,priorSum],weights:s.weights,pending:s.pending.length,trace};}
 const quiet=Array.from({length:8},()=>[0,0,0]);let x=seed>>>0;const rand=()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x;};
 const suite=[["constant",i=>[6150,0,0]],["alternating",i=>[i%2?-6150:6150,0,0]],["two-on-two-off",i=>[i%4<2?6150:0,0,0]],["step-reversal",i=>[i<16?6150:-6150,0,0]],["three-pair reversal",i=>[i%2?-4100:4100,i%2?2050:-2050,1025]],["unpredictable",i=>[rand()%18451-9225,0,0]],["pattern-to-noise",i=>[i<32?(i%2?-6150:6150):rand()%18451-9225,0,0]]];
 const scenarios=suite.map(([name,f])=>run(name,[...quiet,...Array.from({length:64},(_,i)=>f(i)),...quiet],true));const cases=[];for(let j=0;j<64;j++){const {trace,...v}=run("random-"+j,[...quiet,...Array.from({length:64},()=>Array.from({length:3},()=>rand()%8193-4096)),...quiet]);cases.push(v);}
 const sums=[0,0,0,0,0,0],comparisons=[1,2,3,4,5].map(()=>[0,0,0]);for(const v of cases){v.sums.forEach((n,i)=>sums[i]+=n);for(let i=1;i<6;i++)comparisons[i-1][v.sums[0]<v.sums[i]?0:v.sums[0]>v.sums[i]?1:2]++;}
 for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");}
 if(issued!==completed+[...scenarios,...cases].reduce((a,v)=>a+v.pending,0))throw Error("tickets");
 return {seed,ticks,pairs:3*ticks,issued,completed,rollouts,withheld,states,settled,weightsSum,bitChecks:42,sums,comparisons,scenarios,cases};}

export function verifyRotation(){let n=0;for(let t=0;t<2;t++)for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)for(let c=-1;c<=1;c++){const signs=[a,b,c],w=rotateWeights([4,4,4],signs,t);for(let k=0;k<3;k++){if(w[k]!==4+(signs[k]===signs[(k+(t?2:1))%3]?1:-1))throw Error("rotation");n++;}}return n;}
 // ADA-159M.1 .dlw — canonical nested geometry; shared implicit point.
export const CANONICAL="{vogel ; state space ; {vwxyz}^{n} |r8!| [voxel ; operant space , {wxyz}^{n} |b8!| ( vector ; operants , {xy:`z`}^{n} |g8!| )]}";
export const POINT=Object.freeze({id:"implicit-point",kind:"shared-reference"});
export function geometry(n=1){if(!Number.isSafeInteger(n)||n<0)throw Error("n");return Object.freeze({kind:"vogel",space:"state space",coordinates:"vwxyz",spectrum:"r8!",n,point:POINT,child:Object.freeze({kind:"voxel",space:"operant space",coordinates:"wxyz",spectrum:"b8!",n,point:POINT,child:Object.freeze({kind:"vector",space:"operants",coordinates:"xy:`z`",spectrum:"g8!",n,point:POINT})})});}
export function nestedSession(n=1){return {...seesawSession(),geometry:geometry(n)};}
export function nestedStep(s,d){return {...mobiusStep(s,d),geometry:s.geometry};}
export function verifyGeometry(){let checks=0;for(const n of [0,1,2,5,8,13,21]){let s=nestedSession(n);const g=s.geometry;if(g.point!==g.child.point||g.point!==g.child.child.point||g.point!==POINT)throw Error("point identity");if([g,g.child,g.child.child].map(v=>v.spectrum).join(",")!=="r8!,b8!,g8!")throw Error("spectrum");for(let j=0;j<32;j++){s=nestedStep(s,[j%2?6150:-6150,0,0]);if(s.geometry!==g||s.geometry.point!==POINT)throw Error("geometry persistence");checks++;}}for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");checks++;}return {checks,geometryTicks:224,payloadChecks:42,sharedPoint:true};}
