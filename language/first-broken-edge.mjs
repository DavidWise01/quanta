import {initialWheel,inspectWheel} from './center-pinch.mjs';
export const WALK=[1,1,2,3,5,8,13];
export const COUNTS=[3,4,5,8,13];
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function boundary(n,lobes=2) {
 if(!Number.isSafeInteger(n)||n<3||n>64||!Number.isSafeInteger(lobes)||lobes<1||lobes>8)throw Error('Invalid count or lobes');
 return {n,lobes,firstContact:1,outerIndex:0};
}
export function sample(n,lobes,s) {
 boundary(n,lobes);
 if(!Number.isFinite(s)||s<0||s>1.2)throw Error('Invalid strength');
 const w=initialWheel(n);
 const radial=w.ring.map((_,i)=>1-s*(.55+.45*Math.cos(lobes*2*Math.PI*i/n)));
 w.ring=w.ring.map((p,i)=>({x:p.x*radial[i],y:p.y*radial[i]}));
 let check=null,valid=true;
 try{check=inspectWheel(w)}catch{valid=false}
 if(radial.some(r=>r<=0))valid=false;
 return {n,lobes,s,valid,minRadius:Math.min(...radial),collided:radial.flatMap((r,i)=>r<=0?[i]:[]),euler:check?.euler??null,wheel:w};
}
export function start(n=8,lobes=2){return {version:'QG-046',spec:boundary(n,lobes),observations:[]}}
export function verify(log){
 if(!log||log.version!=='QG-046'||!Array.isArray(log.observations)||!same(log.spec,boundary(log.spec?.n,log.spec?.lobes)))throw Error('Invalid ledger');
 for(let i=0;i<log.observations.length;i++){const e=log.observations[i];if(e.index!==i||!same(e.result,sample(log.spec.n,log.spec.lobes,e.strength)))throw Error('Replay mismatch at '+i)}
 return {passed:true,count:log.observations.length};
}
export function append(log,strength){verify(log);return {version:'QG-046',spec:{...log.spec},observations:[...log.observations,{index:log.observations.length,strength,result:sample(log.spec.n,log.spec.lobes,strength)}]}}
export function demo(n=8,lobes=2){let l=start(n,lobes);for(const k of WALK)l=append(l,k/13);return l}
