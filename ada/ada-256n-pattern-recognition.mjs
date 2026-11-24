// ADA-256N .dlw — bounded temporal recognition of directly supported groups.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveAssociations,verifyAssociations} from "./ada-255n-contextual-association.mjs";
export const PATTERN_WINDOW=8;
export function recognize(history){
 const latest=history.at(-1);if(!latest)return Object.freeze([]);
 const masks=[...new Set(history.flatMap(r=>r.groups.map(g=>g.mask)))].sort((a,b)=>a-b);
 return Object.freeze(masks.map(mask=>{
 const presence=Object.freeze(history.map(r=>Object.freeze({generation:r.generation,present:r.groups.some(g=>g.mask===mask)})));
 const present=presence.at(-1).present,previous=presence.at(-2)?.present??false;
 const priorCount=presence.slice(0,-1).filter(p=>p.present).length;
 let status=present?(previous?"PERSISTING":priorCount?"RECURRING":"FORMING"):"HISTORICAL";
 const subsets=latest.groups.filter(g=>g.mask!==mask&&(g.mask&mask)===g.mask);
 const union=subsets.reduce((s,g)=>s|g.mask,0);
 if(!present&&previous)status=subsets.length>=2&&union===mask?"FRAGMENTING":"NO_LONGER_MAXIMAL";
 const members=Array.from({length:9},(_,i)=>i).filter(i=>mask&(1<<i));
 const supported=members.every((a,i)=>members.slice(i+1).every(b=>latest.edges.some(e=>e.from===a&&e.to===b&&e.semantic==="STABLE_AGREEMENT")));
 const incomplete=members.some((a,i)=>members.slice(i+1).some(b=>latest.edges.some(e=>e.from===a&&e.to===b&&e.semantic==="INSUFFICIENT")));
 if(!present&&previous&&!supported&&status!=="FRAGMENTING")status=incomplete?"UNRESOLVED":"DISSOLVING";
 return Object.freeze({mask,members:Object.freeze(members),presence,present,status,supported,incomplete,occurrences:presence.filter(p=>p.present).length});
 }));
}
export function derivePatterns(chain){
 const source=deriveAssociations(chain);if(!verifyAssociations(chain,source).pass)throw Error("Association replay failed");
 let parent=null;
 return Object.freeze(source.map((r,i)=>{
 const history=Object.freeze(source.slice(Math.max(0,i-PATTERN_WINDOW+1),i+1).map(s=>Object.freeze({generation:s.generation,associationHash:s.hash,groups:s.associations.groups,edges:s.associations.edges})));
 const patterns=recognize(history);
 const body={schema:"ADA-256N.patterns.v1",generation:r.generation,epoch:r.epoch,sourceHash:r.sourceHash,associationHash:r.hash,parent,history,patterns,window:PATTERN_WINDOW,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 parent=fnv64(canonical(body));return Object.freeze({...body,hash:parent});
 }));
}
export function verifyPatterns(chain,ledger){
 try{const a=derivePatterns(chain),s=deriveAssociations(chain);return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>r.parent===(a[i-1]?.hash??null)&&r.associationHash===s[i].hash&&r.growthFactor===1.025&&r.authority==="OBSERVE_ONLY"&&r.history.length===Math.min(i+1,PATTERN_WINDOW)&&r.history.every((h,j)=>{const q=s[i-r.history.length+1+j];return h.generation===q.generation&&h.associationHash===q.hash&&canonical(h.groups)===canonical(q.associations.groups)&&canonical(h.edges)===canonical(q.associations.edges)})&&r.patterns.every(p=>p.presence.length===r.history.length&&p.presence.every((x,j)=>x.present===r.history[j].groups.some(g=>g.mask===p.mask))&&(!p.present||p.supported))),count:a.length};}catch(e){return {pass:false,reason:e.message}}
}
export function patternFixtures(){
 const frame=(generation,masks,unknown=false)=>({generation,groups:masks.map(mask=>({mask})),edges:Array.from({length:9},(_,a)=>Array.from({length:9},(_,b)=>a<b?{from:a,to:b,semantic:masks.some(m=>(m&(1<<a))&&(m&(1<<b)))?"STABLE_AGREEMENT":unknown?"INSUFFICIENT":"STABLE_OPPOSITION"}:null)).flat().filter(Boolean)});
 const f=(frames,mask)=>recognize(frames).find(p=>p.mask===mask)?.status;
 const checks={formation:f([frame(0,[7])],7)==="FORMING",persistence:f([frame(0,[7]),frame(1,[7])],7)==="PERSISTING",fragmentation:f([frame(0,[7]),frame(1,[3,6])],7)==="FRAGMENTING",dissolution:f([frame(0,[7]),frame(1,[])],7)==="DISSOLVING",unknown:f([frame(0,[7]),frame(1,[],true)],7)==="UNRESOLVED",recurrence:f([frame(0,[7]),frame(1,[]),frame(2,[7])],7)==="RECURRING",expansion:f([frame(0,[3]),frame(1,[7])],3)==="NO_LONGER_MAXIMAL"};
 return {pass:Object.values(checks).every(Boolean),checks};
}
