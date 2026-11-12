// QG-062 — Three surfaces, ancestry-connected evidence roots.
// This models declared source permissions and lineage; no network fetching or policy verification.
import {start as startRelearning,verify as verifyRelearning} from './relearning-without-amnesia.mjs';
export const VERSION='QG-062';
export const SURFACES=Object.freeze(['github','0root.ai','public-internet']);
const copy=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const named=x=>typeof x==='string'&&x.length>0&&x.length<=160;
const binary=x=>x===0||x===1;
function validate(packet){
 if(!packet||!named(packet.id)||!SURFACES.includes(packet.surface)||!named(packet.source)||
 !Array.isArray(packet.ancestors)||!packet.ancestors.length||packet.ancestors.length>32||
 packet.ancestors.some(x=>!named(x))||!binary(packet.outcome)||packet.epoch!=='post-withdrawal')
 throw Error('Invalid source packet');
 if(packet.surface==='public-internet'){
  if(!packet.policy||!['allow','disallow','unknown'].includes(packet.policy.robots)||
   !['listed','unlisted','unknown'].includes(packet.policy.llms))
   throw Error('Internet packet needs declared robots and llms policy');
 } else if(packet.policy!==undefined)throw Error('Owned corpus policy must be modeled separately');
}
function enriched(packet){
 const p=copy(packet);
 // Two owned surfaces are forced to share the same canonical ancestry, regardless of labels.
 const lineage=[...new Set([...p.ancestors, 'source:'+p.surface+':'+p.source,
  ...(p.surface==='github'||p.surface==='0root.ai'?['owned-corpus']:[])])];
 return {...p,canonicalLineage:lineage};
}
function classify(packet){
 if(packet.surface!=='public-internet')return 'owned-allowed-internal';
 if(packet.policy.robots==='disallow')return 'blocked-robots';
 if(packet.policy.robots==='unknown')return 'quarantined-policy-unknown';
 return packet.policy.llms==='listed'?'allowed-llms-discoverable':'allowed-robots-llms-not-authorization';
}
function linked(a,b){return a.some(x=>b.includes(x))}
function reconstruct(packets,candidate){
 const ids=new Set(),entries=[];
 for(const raw of packets){
  validate(raw);
  if(ids.has(raw.id))throw Error('Duplicate packet identifier');
  ids.add(raw.id);
  const p=enriched(raw);
  entries.push({packet:p,policyStatus:classify(p)});
 }
 const valid=entries.filter(e=>e.policyStatus.startsWith('allowed')||e.policyStatus==='owned-allowed-internal');
 // Connected components, including transitive links. This avoids double counting syndication.
 const parent=valid.map((_,i)=>i);
 const root=i=>{while(parent[i]!==i)i=parent[i];return i};
 for(let i=0;i<valid.length;i++)for(let j=0;j<i;j++){
  if(linked(valid[i].packet.canonicalLineage,valid[j].packet.canonicalLineage)){
   const ri=root(i),rj=root(j);if(ri!==rj)parent[ri]=rj;
  }
 }
 const groups=[];
 const where=new Map();
 for(let i=0;i<valid.length;i++){
  const key=root(i);
  if(!where.has(key)){where.set(key,groups.length);groups.push({members:[],lineage:[],outcomes:[]})}
  const g=groups[where.get(key)],p=valid[i].packet;
  g.members.push(p.id);
  g.outcomes.push(p.outcome);
  g.lineage=[...new Set([...g.lineage,...p.canonicalLineage])];
 }
 const components=groups.map((g,i)=>({
  index:i,members:g.members,lineage:g.lineage,
  outcome:g.outcomes.every(x=>x===g.outcomes[0])?g.outcomes[0]:null,
  conflict:g.outcomes.some(x=>x!==g.outcomes[0])
 }));
 const eligible=components.length>=3&&components.every(g=>!g.conflict&&g.outcome===candidate);
 const disagreement=components.some(g=>!g.conflict&&g.outcome!==candidate);
 const conflict=components.some(g=>g.conflict);
 const decision=conflict?'review_shared_ancestry':disagreement?'review_disagreement':
  eligible?'eligible_for_explicit_authorization':'collect';
 const events=entries.map((e,i)=>({
  index:i,id:e.packet.id,surface:e.packet.surface,source:e.packet.source,
  policyStatus:e.policyStatus,
  counted:valid.some(v=>v.packet.id===e.packet.id)
 }));
 return {events,components,count:components.length,blocked:events.filter(e=>!e.counted).length,
  decision};
}
export function start(){
 const inherited=startRelearning();
 verifyRelearning(inherited);
 return {version:VERSION,inherited,packets:[],events:[],components:[],
  decision:'collect',authority:'withdrawn',count:0,blocked:0};
}
export function verify(record){
 if(!record||record.version!==VERSION||!Array.isArray(record.packets)||
 !Array.isArray(record.events)||!Array.isArray(record.components))throw Error('Malformed QG-062 record');
 verifyRelearning(record.inherited);
 if(record.inherited.authority!=='withdrawn'||record.inherited.packets.length!==0)throw Error('Unexpected inherited state');
 const state=reconstruct(record.packets,record.inherited.candidate.hypothesis);
 if(!same(record.events,state.events)||!same(record.components,state.components)||
  record.decision!==state.decision||record.count!==state.count||record.blocked!==state.blocked)
  throw Error('Ancestry replay mismatch');
 if(!['withdrawn','provisional'].includes(record.authority)||record.authority==='provisional'&&state.decision!=='eligible_for_explicit_authorization')
  throw Error('Invalid authority');
 return {valid:true,...state,authority:record.authority,candidate:record.inherited.candidate.hypothesis,
  surfaces:[...SURFACES]};
}
export function append(record,packet){
 verify(record);
 if(record.authority!=='withdrawn'||record.decision!=='collect')throw Error('Collection closed');
 validate(packet);
 const next={...copy(record),packets:[...copy(record.packets),copy(packet)]};
 const state=reconstruct(next.packets,next.inherited.candidate.hypothesis);
 Object.assign(next,{events:state.events,components:state.components,count:state.count,
  blocked:state.blocked,decision:state.decision});
 verify(next);return next;
}
export function authorize(record){
 const v=verify(record);
 if(record.authority!=='withdrawn')throw Error('Already authorized');
 if(v.decision!=='eligible_for_explicit_authorization')throw Error('Independent ancestry threshold unmet');
 const next={...copy(record),authority:'provisional'};
 verify(next);return next;
}
export function run(packets){
 if(!Array.isArray(packets))throw Error('Packet array required');
 let state=start();for(const packet of packets)state=append(state,packet);return state;
}
export function fixture(kind='independent'){
 const owned=[
 {id:'g',surface:'github',source:'DavidWise01',ancestors:['repository-archive'],outcome:0,epoch:'post-withdrawal'},
 {id:'w',surface:'0root.ai',source:'0root.ai',ancestors:['website-mirror'],outcome:0,epoch:'post-withdrawal'}
 ];
 const ext=(id,site,ancestors,outcome=0,robots='allow',llms='listed')=>({
  id,surface:'public-internet',source:site,ancestors,outcome,epoch:'post-withdrawal',
  policy:{robots,llms}
 });
 if(kind==='independent')return run([...owned,ext('a','site-a',['upstream-a']),ext('b','site-b',['upstream-b'])]);
 if(kind==='syndicated')return run([...owned,ext('a','site-a',['wire-origin']),ext('b','site-b',['wire-origin'])]);
 if(kind==='transitive')return run([...owned,ext('a','site-a',['origin-a','bridge-ab']),ext('b','site-b',['bridge-ab','bridge-bc']),ext('c','site-c',['bridge-bc'])]);
 if(kind==='blocked')return run([...owned,ext('a','site-a',['origin-a'],0,'disallow'),ext('b','site-b',['origin-b'],0,'unknown')]);
 if(kind==='conflict')return run([...owned,ext('a','site-a',['wire-origin'],0),ext('b','site-b',['wire-origin'],1)]);
 throw Error('Unknown fixture');
}
