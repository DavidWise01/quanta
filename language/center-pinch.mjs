// QG-045: verified planar radial center-pinch of a wheel graph.
// The declared wheel's graph topology and planar triangle fan survive each accepted event.
// This is Euclidean geometry; it does not create or prove a torus.
export const FIBONACCI_WALK = Object.freeze([1,1,2,3,5,8,13]);
export const SHAPES = Object.freeze([3,4,5,8,13]);
const EPS=1e-9;
const clone=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const cross=(a,b,c)=>(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);
const finite=p=>p && Number.isFinite(p.x) && Number.isFinite(p.y);
const edge=(a,b,c,d)=>cross(a,b,c)*cross(a,b,d)<-EPS && cross(c,d,a)*cross(c,d,b)<-EPS;
export function initialWheel(n) {
 if(!Number.isSafeInteger(n)||n<3||n>64) throw new RangeError('outer count must be 3..64');
 return {n,center:{x:0,y:0},ring:Array.from({length:n},(_,i)=>({x:Math.cos(i*2*Math.PI/n),y:Math.sin(i*2*Math.PI/n)}))};
}
export function inspectWheel(w) {
 if(!w || !Number.isSafeInteger(w.n) || w.n<3||w.n>64 || !finite(w.center) ||
    !Array.isArray(w.ring)||w.ring.length!==w.n||!w.ring.every(finite))
    throw new Error('Malformed wheel');
 const n=w.n,center=w.center, ring=w.ring,faces=[];
 for(let i=0;i<n;i++) {
   const a=ring[i],b=ring[(i+1)%n];
   const area2=cross(center,a,b);
   if(area2<=EPS) throw new Error('Collapsed or reversed triangular face '+i);
   faces.push(area2/2);
 }
 for(let i=0;i<n;i++) for(let j=i+1;j<n;j++) {
   // Test non-adjacent outer ring edges for crossing.
   if(j===i+1 || (i===0 && j===n-1)) continue;
   if(edge(ring[i],ring[(i+1)%n],ring[j],ring[(j+1)%n]))
     throw new Error('Outer edges cross');
 }
 // Each spoke may only meet its own incident edges.
 for(let i=0;i<n;i++) for(let j=0;j<n;j++) {
   if(j===i || (j+1)%n===i) continue;
   if(edge(center,ring[i],ring[j],ring[(j+1)%n]))
     throw new Error('Spoke crosses outer edge');
 }
 const V=n+1,E=2*n,F=n+1;
 return {vertices:V,edges:E,faces:F,boundedFaces:n,euler:V-E+F,
   minimumFaceArea:Math.min(...faces),totalBoundedArea:faces.reduce((a,b)=>a+b,0),
   crossingFree:true,center:{...center}};
}
function inputAction(action) {
 if(!action || !Number.isFinite(action.dx) || !Number.isFinite(action.dy) ||
    !Number.isFinite(action.strength) || !Number.isSafeInteger(action.lobes) ||
    action.lobes<1 || action.lobes>8 || action.strength<0 || action.strength>0.72 ||
    Math.abs(action.dx)>0.12 || Math.abs(action.dy)>0.12)
   throw new Error('Invalid bounded pinch action');
 return {dx:action.dx,dy:action.dy,strength:action.strength,lobes:action.lobes};
}
export function pinchWheel(w,action) {
 inspectWheel(w);
 const a=inputAction(action), center={x:w.center.x+a.dx,y:w.center.y+a.dy};
 const ring=w.ring.map((v,i)=>{
   const theta=2*Math.PI*i/w.n;
   const radial=1-a.strength*(0.55+0.45*Math.cos(a.lobes*theta));
   return {x:center.x+(v.x-w.center.x)*radial,y:center.y+(v.y-w.center.y)*radial};
 });
 const next={n:w.n,center,ring};
 inspectWheel(next); // No inference of continuity from endpoint alone: see certificate below.
 // Continuous interpolation w(t) of the center and radial factors; validate
 // a bounded sequence of samples, only a computational check, not proof for all t.
 for(let t=1;t<20;t++) {
   const k=t/20,c={x:w.center.x+a.dx*k,y:w.center.y+a.dy*k};
   const partial={n:w.n,center:c,ring:w.ring.map((v,i)=>{
     const th=2*Math.PI*i/w.n;
     const s=1-k*a.strength*(0.55+0.45*Math.cos(a.lobes*th));
     return {x:c.x+(v.x-w.center.x)*s,y:c.y+(v.y-w.center.y)*s};
   })};
   inspectWheel(partial);
 }
 return next;
}
export function startPinchLedger(n) {
 const initial=initialWheel(n);
 return {version:'QG-045',initial,events:[],current:clone(initial)};
}
export function appendPinch(ledger,action) {
 verifyPinchLedger(ledger);
 const normalized=inputAction(action),next=pinchWheel(ledger.current,normalized);
 const record={index:ledger.events.length,action:normalized,
   before:inspectWheel(ledger.current),after:inspectWheel(next),snapshot:clone(next)};
 return {version:'QG-045',initial:clone(ledger.initial),
   events:[...clone(ledger.events),record],current:clone(next)};
}
export function verifyPinchLedger(ledger) {
 if(!ledger || ledger.version!=='QG-045'||!Array.isArray(ledger.events))
   throw new Error('Invalid ledger');
 if(!eq(ledger.initial,initialWheel(ledger.initial?.n))) throw new Error('Modified initial geometry');
 let state=clone(ledger.initial);
 inspectWheel(state);
 for(let i=0;i<ledger.events.length;i++) {
   const record=ledger.events[i];
   if(!record || record.index!==i) throw new Error('Event index discontinuity');
   const before=inspectWheel(state);
   const next=pinchWheel(state,record.action);
   const after=inspectWheel(next);
   if(!eq(before,record.before) || !eq(after,record.after) || !eq(next,record.snapshot))
     throw new Error('Pinch replay mismatch at event '+i);
   if(after.vertices!==before.vertices || after.edges!==before.edges ||
      after.faces!==before.faces || after.euler!==2)
     throw new Error('Topology conservation failed');
   state=next;
 }
 if(!eq(state,ledger.current)) throw new Error('Current geometry mismatch');
 return {valid:true,events:ledger.events.length,summary:inspectWheel(state)};
}
export function demoPinch(n=8) {
 let ledger=startPinchLedger(n);
 for(const k of FIBONACCI_WALK) {
   ledger=appendPinch(ledger,{dx:0.005,dy:-0.003,strength:k/100,lobes:2});
 }
 return ledger;
}
