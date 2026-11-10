// QG-050 — ambiguous roots. Distinguish observational equivalence from identity.
// Synthetic radial generator only. The unknown generator is never given to inference.
export const ROOTS=Object.freeze([1,2,3,4,5,6,7,8]);
export const RING_SIZES=Object.freeze([3,4,5,8,13]);
export const OFFGRID=Object.freeze([Math.PI/17,Math.PI/13,Math.PI/11,Math.PI/7]);
const EPS=1e-9;
const clone=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function finite(v){return typeof v==='number'&&Number.isFinite(v)}
export function response(root,theta){
 if(!ROOTS.includes(root)||!finite(theta))throw Error('Invalid root or angle');
 return .55+.45*Math.cos(root*theta);
}
export function ringObservations(n,root){
 if(!RING_SIZES.includes(n))throw Error('Unsupported ring');
 return Array.from({length:n},(_,i)=>({theta:2*Math.PI*i/n,value:response(root,2*Math.PI*i/n),index:i}));
}
export function matchingRoots(observations,eps=EPS){
 if(!Array.isArray(observations)||observations.length===0||!finite(eps)||eps<=0||eps>1e-5)throw Error('Invalid observations or tolerance');
 for(const o of observations)if(!o||!finite(o.theta)||!finite(o.value)||o.value<0||o.value>1||o.index!==undefined&&(!Number.isSafeInteger(o.index)||o.index<0))throw Error('Invalid observed sample');
 return ROOTS.filter(r=>observations.every(o=>Math.abs(response(r,o.theta)-o.value)<=eps));
}
export function equivalenceClasses(n,roots=ROOTS){
 if(!RING_SIZES.includes(n)||!Array.isArray(roots)||roots.length===0||new Set(roots).size!==roots.length||roots.some(x=>!ROOTS.includes(x)))throw Error('Invalid roots or ring');
 const remaining=new Set(roots),classes=[];
 while(remaining.size){
  const first=remaining.values().next().value;remaining.delete(first);
  const cl=[first];
  for(const r of [...remaining]){
   let sameRing=true;
   for(let j=0;j<n;j++)if(Math.abs(response(first,2*Math.PI*j/n)-response(r,2*Math.PI*j/n))>EPS){sameRing=false;break}
   if(sameRing){remaining.delete(r);cl.push(r)}
  }
  classes.push(cl);
 }
 return classes;
}
export function nextProbe(roots,angles=OFFGRID){
 if(!Array.isArray(roots)||roots.length<2||new Set(roots).size!==roots.length||roots.some(x=>!ROOTS.includes(x))||!Array.isArray(angles)||!angles.length||angles.some(x=>!finite(x)))throw Error('Invalid candidates or probes');
 const scored=angles.map(theta=>{
  const vals=roots.map(r=>response(r,theta));
  return {theta,spread:Math.max(...vals)-Math.min(...vals),predictions:roots.map((root,i)=>({root,value:vals[i]}))};
 }).sort((a,b)=>b.spread-a.spread);
 return scored[0].spread>EPS?scored[0]:null;
}
export function startDiscovery(n,observations){
 if(!RING_SIZES.includes(n)||!Array.isArray(observations)||!observations.length)throw Error('Missing observations');
 // Require initial observations to be exactly the complete ring, in indexed order.
 if(observations.length!==n)throw Error('Incomplete ring');
 for(let i=0;i<n;i++)if(observations[i].index!==i||Math.abs(observations[i].theta-2*Math.PI*i/n)>EPS)throw Error('Invalid ring index');
 const roots=matchingRoots(observations);
 if(!roots.length)throw Error('No explaining root');
 return {version:'QG-050',ringSize:n,ring:clone(observations),additional:[],remaining:roots};
}
export function verifyDiscovery(ledger){
 if(!ledger||ledger.version!=='QG-050'||!RING_SIZES.includes(ledger.ringSize)||!Array.isArray(ledger.additional)||!Array.isArray(ledger.remaining))throw Error('Invalid discovery ledger');
 const initial=startDiscovery(ledger.ringSize,ledger.ring);
 let remaining=initial.remaining;
 for(let i=0;i<ledger.additional.length;i++){
  const x=ledger.additional[i];
  if(!x||x.index!==i||!OFFGRID.some(t=>Math.abs(t-x.theta)<=EPS)||!finite(x.value))throw Error('Bad probe event');
  const expected=nextProbe(remaining);
  if(!expected||Math.abs(expected.theta-x.theta)>EPS)throw Error('Unjustified probe selection');
  const next=matchingRoots([...ledger.ring,...ledger.additional.slice(0,i+1)]);
  if(!same(x.remaining,next))throw Error('Probe replay mismatch');
  remaining=next;
 }
 if(!same(remaining,ledger.remaining))throw Error('Final candidate mismatch');
 return {valid:true,candidates:[...remaining],unique:remaining.length===1,probes:ledger.additional.length};
}
export function appendProbe(ledger,observedValue){
 verifyDiscovery(ledger);
 const probe=nextProbe(ledger.remaining);
 if(!probe)throw Error('No distinguishing probe exists');
 if(!finite(observedValue)||observedValue<0||observedValue>1)throw Error('Invalid probe value');
 const idx=ledger.additional.length;
 const event={index:idx,theta:probe.theta,value:observedValue};
 const remaining=matchingRoots([...ledger.ring,...ledger.additional,event]);
 if(!remaining.length)throw Error('Observation contradicts every candidate');
 event.remaining=[...remaining];
 return {...clone(ledger),additional:[...clone(ledger.additional),event],remaining};
}
export function demo(n=8,hiddenRoot=1){
 let ledger=startDiscovery(n,ringObservations(n,hiddenRoot));
 while(ledger.remaining.length>1&&ledger.additional.length<OFFGRID.length){
  const p=nextProbe(ledger.remaining);if(!p)break;
  ledger=appendProbe(ledger,response(hiddenRoot,p.theta));
 }
 return ledger;
}
