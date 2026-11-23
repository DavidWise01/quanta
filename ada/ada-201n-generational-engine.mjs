// ADA-201N · Generational +n deterministic append-only kernel.
// Phase II source freeze is a parent anchor, never mutated.
// No randomness, wall-clock input, consensus or mutable ancestors.
export const PHASE_II_FREEZE="e5ee94c473438ff6dc95ebdbacccf37e29fa09c1";
export const GENESIS_SEED=201;
export const SCHEMA="ADA-201N.generation.v1";
export const bound=(v,lo,hi)=>Math.max(lo,Math.min(hi,v));
export const canonical=value=>JSON.stringify(value);
export function fnv64(text){
 let h=0xcbf29ce484222325n;
 for(const byte of new TextEncoder().encode(text)){h^=BigInt(byte);h=BigInt.asUintN(64,h*0x100000001b3n)}
 return h.toString(16).padStart(16,"0");
}
export function lcg(seed){return (Math.imul(seed,1664525)+1013904223)>>>0}
export function genesis(){
 const frame={schema:SCHEMA,n:0,parent:null,parentRoot:PHASE_II_FREEZE,seed:GENESIS_SEED,signal:50,stability:100,energy:100,contacts:[50,50,50],decision:"ROOT",event:"phase-II-root-boundary"};
 return Object.freeze({...frame,contacts:Object.freeze([...frame.contacts]),hash:fnv64(canonical(frame))});
}
export function next(parent){
 if(!parent||parent.schema!==SCHEMA||!Number.isSafeInteger(parent.n)||parent.n<0||parent.n>=10000)throw Error("Invalid generation parent or generation limit");
 if(!verifyNode(parent))throw Error("Parent lineage tamper detected");
 const n=parent.n+1,seed=lcg(parent.seed),noise=((seed>>>12)%2001-1000)/1000;
 const delta=bound(0.12*Math.sin(n*0.43)+noise*0.18,-0.24,0.24);
 const signal=Number(bound(parent.signal+delta*10,0,100).toFixed(5));
 const contacts=[signal,Number(bound(parent.contacts[1]+(signal-parent.contacts[1])*0.2,0,100).toFixed(5)),Number(bound(parent.contacts[2]+(parent.contacts[1]-parent.contacts[2])*0.15,0,100).toFixed(5))];
 const stability=Number(bound(100-Math.abs(contacts[0]-contacts[1])*2.8,0,100).toFixed(5));
 const energy=Number(bound(parent.energy-0.25+0.5*(stability>=95?1:0),0,100).toFixed(5));
 const decision=stability>=90&&energy>=5?"APPEND":"HOLD";
 const frame={schema:SCHEMA,n,parent:parent.hash,parentRoot:parent.parentRoot,seed,signal,stability,energy,contacts,decision,event:decision==="APPEND"?"inherited-observation":"safety-gate-hold"};
 return Object.freeze({...frame,contacts:Object.freeze([...frame.contacts]),hash:fnv64(canonical(frame))});
}
export function verifyNode(item){
 if(!item||item.schema!==SCHEMA||!Number.isInteger(item.n)||item.n<0)return false;
 const {hash,...fields}=item;
 return typeof hash==="string"&&hash===fnv64(canonical(fields));
}
export function verifyChain(chain){
 if(!Array.isArray(chain)||chain.length<1||chain.length>10001)return {pass:false,reason:"Invalid chain length"};
 const first=genesis();
 if(canonical(chain[0])!==canonical(first))return {pass:false,reason:"Genesis mismatch"};
 for(let i=0;i<chain.length;i++){
  if(!verifyNode(chain[i]))return {pass:false,reason:"Hash mismatch at generation "+i};
  if(i>0&&canonical(chain[i])!==canonical(next(chain[i-1])))return {pass:false,reason:"Parent or deterministic transition mismatch at generation "+i};
 }
 return {pass:true,count:chain.length,last:chain.at(-1).hash};
}
export function advance(chain,steps=1){
 if(!Number.isSafeInteger(steps)||steps<1||steps>1000)throw Error("Steps must be 1..1000");
 const checked=verifyChain(chain);if(!checked.pass)throw Error(checked.reason);
 if(chain.length+steps>10001)throw Error("Generation cap exceeded");
 const out=chain.slice();for(let i=0;i<steps;i++)out.push(next(out.at(-1)));
 return out;
}
