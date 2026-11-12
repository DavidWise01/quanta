// QG-063 — Prove the Source, Not Just the Claim.
// A trusted *locally pinned* registry is the admission authority, NOT a proof of
// website identity or source independence in the real world.
// Browser and Node 22 use WebCrypto SHA-256.
import {start as startAncestry,run as runAncestry,verify as verifyAncestry} from './three-surface-ancestry.mjs';
export const VERSION='QG-063';
const clone=x=>JSON.parse(JSON.stringify(x));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const name=x=>typeof x==='string'&&x.length>0&&x.length<=160;
const binary=x=>x===0||x===1;
const surfaces=['github','0root.ai','public-internet'];
export async function sha256(body){
 if(typeof body!=='string')throw Error('Text body required');
 const bytes=new TextEncoder().encode(body);
 const hashed=await crypto.subtle.digest('SHA-256',bytes);
 return Array.from(new Uint8Array(hashed),x=>x.toString(16).padStart(2,'0')).join('');
}
function manifestValid(m){
 return m&&name(m.source)&&surfaces.includes(m.surface)&&
 Array.isArray(m.ancestors)&&m.ancestors.length>0&&m.ancestors.every(name)&&
 typeof m.digest==='string'&&/^[0-9a-f]{64}$/.test(m.digest)&&
 (m.surface!=='public-internet'||m.policy&&
 ['allow','disallow','unknown'].includes(m.policy.robots)&&
 ['listed','unlisted','unknown'].includes(m.policy.llms));
}
function registryValid(registry){
 if(!Array.isArray(registry)||registry.length>32||registry.some(m=>!manifestValid(m)))throw Error('Invalid pinned registry');
 const keys=registry.map(m=>m.surface+'|'+m.source);
 if(new Set(keys).size!==keys.length)throw Error('Duplicate pinned source');
}
function packetValid(p){
 if(!p||!name(p.id)||!name(p.source)||!surfaces.includes(p.surface)||
 !binary(p.outcome)||typeof p.body!=='string'||p.epoch!=='post-withdrawal')
 throw Error('Invalid submitted packet');
}
async function audit(submitted,registry){
 registryValid(registry);
 const receipts=[],allowed=[],ids=new Set();
 for(let i=0;i<submitted.length;i++){
  const p=submitted[i];packetValid(p);
  if(ids.has(p.id))throw Error('Duplicate packet identifier');
  ids.add(p.id);
  const pin=registry.find(m=>m.source===p.source&&m.surface===p.surface);
  let status='quarantined_unknown_source',digest=null;
  if(pin){
   digest=await sha256(p.body);
   if(digest!==pin.digest)status='quarantined_digest_mismatch';
   else if(pin.surface==='public-internet'&&pin.policy.robots!=='allow')
    status=pin.policy.robots==='disallow'?'blocked_robots':'quarantined_policy_unknown';
   else status='accepted_pinned_content';
  }
  const receipt={index:i,id:p.id,source:p.source,surface:p.surface,status,digest,
    manifestDigest:pin?.digest??null};
  receipts.push(receipt);
  if(status==='accepted_pinned_content'){
   allowed.push({id:p.id,source:p.source,surface:p.surface,ancestors:clone(pin.ancestors),
    outcome:p.outcome,epoch:p.epoch,...(p.surface==='public-internet'?{policy:clone(pin.policy)}:{})});
  }
 }
 const ancestry=allowed.length?runAncestry(allowed):startAncestry();
 verifyAncestry(ancestry);
 return {receipts,ancestry,accepted:allowed.length,
  quarantined:receipts.filter(r=>r.status!=='accepted_pinned_content').length,
  decision:ancestry.decision};
}
export async function start(registry=[]){
 registryValid(registry);
 const state=await audit([],registry);
 return {version:VERSION,registry:clone(registry),submitted:[],...state};
}
export async function verify(record){
 if(!record||record.version!==VERSION||!Array.isArray(record.submitted))throw Error('Malformed source admission ledger');
 const expected=await audit(record.submitted,record.registry);
 for(const k of ['receipts','ancestry','accepted','quarantined','decision'])
  if(!same(expected[k],record[k]))throw Error('Admission replay mismatch: '+k);
 return {valid:true,...expected};
}
export async function append(record,packet){
 await verify(record);
 if(record.decision!=='collect')throw Error('Ancestry decision closed');
 packetValid(packet);
 const submitted=[...clone(record.submitted),clone(packet)];
 const derived=await audit(submitted,record.registry);
 const next={version:VERSION,registry:clone(record.registry),submitted,...derived};
 await verify(next);return next;
}
export async function authorize(record){
 await verify(record);
 if(record.ancestry.decision!=='eligible_for_explicit_authorization')throw Error('Independence and provenance gate unmet');
 const updated=clone(record);
 updated.ancestry=runAncestry(record.ancestry.packets);
 // The source verification gate intentionally NEVER grants authority;
 // QG-062 authorizes via separate explicit action.
 return {eligible:true,authority:'withdrawn',decision:updated.decision,
  nextAction:'explicit QG-062 authorize required'};
}
export async function fixture(kind='valid'){
 const manifests=[
  {surface:'github',source:'DavidWise01',body:'owned Git record',ancestors:['owned-publication']},
  {surface:'0root.ai',source:'0root.ai',body:'owned web mirror',ancestors:['owned-publication']},
  {surface:'public-internet',source:'site-a',body:'independent report A',ancestors:['origin-A'],policy:{robots:'allow',llms:'listed'}},
  {surface:'public-internet',source:'site-b',body:'independent report B',ancestors:[kind==='syndicated'?'origin-A':'origin-B'],policy:{robots:'allow',llms:'unlisted'}}
 ];
 const registry=await Promise.all(manifests.map(async({body,...m})=>({...m,digest:await sha256(body)})));
 let ledger=await start(registry);
 const packets=manifests.map((m,i)=>({id:'P'+i,source:m.source,surface:m.surface,body:m.body,outcome:0,epoch:'post-withdrawal'}));
 if(kind==='tampered')packets[2].body='modified report A';
 if(kind==='untrusted')packets[2].source='unknown-site';
 for(const p of packets)ledger=await append(ledger,p);
 return ledger;
}
