// QG-051 — repeat a position, change the observation channel.
// Synthetic finite candidate family; no physical identification implied.
import {ROOTS,response} from './ambiguous-roots.mjs';
export const WALK=Object.freeze([1,1,2,3,5,8,13]);
export const RING_SIZE=13;
export const EPS=1e-9;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const clone=x=>JSON.parse(JSON.stringify(x));
export const thetaAt=step=>{if(!WALK.includes(step))throw Error('Step outside Fibonacci walk');return 2*Math.PI*(step%RING_SIZE)/RING_SIZE};
export const measure=(root,step,channel)=>{
 if(!ROOTS.includes(root))throw Error('Unknown root');
 const t=thetaAt(step);
 if(channel==='amplitude')return response(root,t);
 if(channel==='phase')return Math.sin(root*t);
 throw Error('Unknown channel');
};
export function compatible(observations,eps=EPS){
 if(!Array.isArray(observations)||!Number.isFinite(eps)||eps<=0||eps>1e-5)throw Error('Invalid observations');
 for(const o of observations)if(!o||!WALK.includes(o.step)||!['amplitude','phase'].includes(o.channel)||!Number.isFinite(o.value)||Math.abs(o.value)>1+eps)throw Error('Invalid observation');
 return ROOTS.filter(root=>observations.every(o=>Math.abs(measure(root,o.step,o.channel)-o.value)<=eps));
}
export function allowedSchedule(){
 return WALK.map((step,i)=>({step,channel:i===1?'phase':'amplitude'}));
}
export function runBlind(hiddenRoot,schedule=allowedSchedule()){
 if(!ROOTS.includes(hiddenRoot)||!Array.isArray(schedule))throw Error('Invalid experiment');
 const observations=[],snapshots=[];
 for(let i=0;i<schedule.length;i++){
  const {step,channel}=schedule[i];
  const value=measure(hiddenRoot,step,channel);
  observations.push({step,channel,value});
  const remaining=compatible(observations);
  snapshots.push({index:i,step,channel,remaining:[...remaining],identified:remaining.length===1});
 }
 return {version:'QG-051',schedule:clone(schedule),observations,snapshots,conclusion:snapshots.length?snapshots.at(-1).remaining:ROOTS};
}
export function verifyBlind(record){
 if(!record||record.version!=='QG-051'||!Array.isArray(record.schedule)||!Array.isArray(record.observations)||!Array.isArray(record.snapshots)||record.schedule.length!==record.observations.length||record.schedule.length!==record.snapshots.length)throw Error('Invalid record');
 const obs=[];
 for(let i=0;i<record.schedule.length;i++){
  const s=record.schedule[i],o=record.observations[i],v=record.snapshots[i];
  if(!s||s.step!==WALK[i]||s.channel!==(i===1?'phase':'amplitude')||!o||o.step!==s.step||o.channel!==s.channel)throw Error('Noncanonical schedule');
  // Check data against all candidates, not a declared hidden root.
  if(!Number.isFinite(o.value))throw Error('Bad measurement');
  obs.push(o);
  const remaining=compatible(obs);
  if(!v||v.index!==i||v.step!==s.step||v.channel!==s.channel||!same(v.remaining,remaining)||v.identified!==(remaining.length===1))throw Error('Observation replay mismatch');
 }
 const expected=obs.length?compatible(obs):ROOTS;
 if(!same(record.conclusion,expected))throw Error('Final conclusion mismatch');
 return {valid:true,firstUnique:record.snapshots.findIndex(s=>s.identified)+1||null,remaining:[...expected]};
}
export function minimalWithinAllowed(root){
 if(!ROOTS.includes(root))throw Error('Unknown root');
 const amplitudeAtOne=compatible([{step:1,channel:'amplitude',value:measure(root,1,'amplitude')}]);
 const withPhase=compatible([{step:1,channel:'amplitude',value:measure(root,1,'amplitude')},{step:1,channel:'phase',value:measure(root,1,'phase')}]);
 const allAmplitude=compatible([...new Set(WALK)].map(step=>({step,channel:'amplitude',value:measure(root,step,'amplitude')})));
 return {root,firstAmplitude:amplitudeAtOne,withPhase,allAmplitude,
   earliestUnderSchedule:amplitudeAtOne.length===1?1:withPhase.length===1?2:null};
}
export function completeAudit(){
 const audits=ROOTS.map(minimalWithinAllowed);
 if(audits.some(a=>a.withPhase.length!==1||a.withPhase[0]!==a.root))throw Error('Insufficient joint observations');
 return {version:'QG-051-audit',ring:RING_SIZE,walk:[...WALK],audits};
}
