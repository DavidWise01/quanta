// QG-074: independent declassification of a DISTINCT release artifact.
// Never changes QG-073 original labels. Synthetic review attestations do not
// prove that the proposed public bytes contain no restricted information.
import {verify as verifyGraph,inspect} from './provenance-transformation.mjs';
import {start as scopeStart,grant as scopeGrant,authorizeAction} from './hive-scoped-authority.mjs';
import {fixture as leaseFixture} from './hive-authority-lease.mjs';
import {generateFixtureSigner} from './signed-trust-anchor.mjs';
import {canonical} from './trust-anchor-rotation.mjs';
import {sha256} from './pinned-source-admission.mjs';
export const VERSION='QG-074', SCHEMA='QUANTA-QG-074-RELEASE';
const cp=x=>JSON.parse(JSON.stringify(x));
const equal=(a,b)=>canonical(a)===canonical(b);
const bytes=x=>new TextEncoder().encode(canonical(x));
function enc(x){return btoa(Array.from(new Uint8Array(x),v=>String.fromCharCode(v)).join('')).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'')}
function dec(s){if(typeof s!=='string'||!/^[a-zA-Z0-9_-]+$/.test(s))throw Error('Bad signature encoding');return Uint8Array.from(atob(s.replaceAll('-','+').replaceAll('_','/')+'='.repeat((4-s.length%4)%4)),x=>x.charCodeAt(0))}
async function key(jwk){if(jwk?.kty!=='OKP'||jwk?.crv!=='Ed25519')throw Error('Pinned Ed25519 key required');try{return await crypto.subtle.importKey('jwk',jwk,{name:'Ed25519'},false,['verify'])}catch{throw Error('Invalid pinned public key')}}
async function sign(priv,payload){if(priv?.algorithm?.name!=='Ed25519'||!priv.usages.includes('sign'))throw Error('Reviewer signing key required');return enc(await crypto.subtle.sign('Ed25519',priv,bytes(payload)))}
async function verifySig(pub,payload,sig){let ok=false;try{ok=await crypto.subtle.verify('Ed25519',await key(pub),dec(sig),bytes(payload))}catch{throw Error('Malformed reviewer signature')}if(!ok)throw Error('Reviewer signature invalid')}
function validatePolicy(policy){
 if(!policy||!Array.isArray(policy.reviewers)||policy.reviewers.length<3||
 typeof policy.registryDigest!=='string'||!/^[a-f0-9]{64}$/.test(policy.registryDigest)||
 !Number.isSafeInteger(policy.minReleaseSequence)||policy.minReleaseSequence<0)
 throw Error('Independently pinned reviewer policy required');
 const ids=new Set(),roots=new Set();
 for(const r of policy.reviewers){
  if(!r||typeof r.id!=='string'||!r.id||ids.has(r.id)||
  typeof r.ancestryRoot!=='string'||!r.ancestryRoot||!r.publicJwk)
   throw Error('Invalid reviewer policy');
  ids.add(r.id);roots.add(r.ancestryRoot);
 }
 if(roots.size<3)throw Error('Reviewer policy lacks three independent roots');
}
async function checkPolicy(policy){validatePolicy(policy);await Promise.all(policy.reviewers.map(r=>key(r.publicJwk)))}
export async function start(graph,policy){
 await checkPolicy(policy);await verifyGraph(graph,policy.registryDigest);
 return {version:VERSION,graph:cp(graph),policy:cp(policy),releases:[]};
}
export async function propose(record,{id,nodeId,publicText,destination='0root.ai'},policy){
 await audit(record,policy);
 if(!/^[a-z0-9._-]{1,80}$/i.test(id)||typeof publicText!=='string'||!publicText.length||
 publicText.length>2000||destination!=='0root.ai')throw Error('Invalid public release proposal');
 if(record.releases.some(r=>r.payload.id===id))throw Error('Duplicate release identifier');
 const node=await inspect(record.graph,nodeId,policy.registryDigest);
 if(node.classification!=='gated')throw Error('Release review requires a gated ancestor');
 return {schema:SCHEMA,id,sequence:record.releases.length+1,nodeId,
  nodeDigest:node.digest,graphDigest:await sha256(canonical(record.graph)),
  originalClassification:node.classification,ancestry:cp(node.ancestors),
  origins:cp(node.origins),releaseDigest:await sha256(publicText),destination,
  previousHash:record.releases.length?await sha256(canonical(record.releases.at(-1))):'GENESIS'};
}
export async function review(payload,reviewerId,privateKey){
 if(payload?.schema!==SCHEMA||typeof reviewerId!=='string'||!reviewerId)
 throw Error('Invalid release review request');
 return {reviewerId,signature:await sign(privateKey,payload)};
}
async function validateRelease(entry,graph,policy,prior){
 const p=entry?.payload;
 if(!p||p.schema!==SCHEMA||p.sequence!==prior.sequence+1||p.previousHash!==prior.hash||
 p.destination!=='0root.ai'||p.originalClassification!=='gated'||
 typeof entry.publicText!=='string'||!entry.publicText.length||
 entry.publicText.length>2000||p.releaseDigest!==await sha256(entry.publicText)||
 p.graphDigest!==await sha256(canonical(graph))||
 !/^[a-z0-9._-]{1,80}$/i.test(p.id))throw Error('Release content or sequence mismatch');
 const node=await inspect(graph,p.nodeId,policy.registryDigest);
 if(node.classification!=='gated'||p.nodeDigest!==node.digest||
 !equal(p.ancestry,node.ancestors)||!equal(p.origins,node.origins))
 throw Error('Original gated ancestry mismatch');
 if(!Array.isArray(entry.votes)||entry.votes.length<3||entry.votes.length>policy.reviewers.length)
 throw Error('Three reviewer approvals required');
 const ids=new Set(),roots=new Set();
 for(const v of entry.votes){
  const reviewer=policy.reviewers.find(r=>r.id===v?.reviewerId);
  if(!reviewer||ids.has(v.reviewerId))throw Error('Unknown or duplicate reviewer');
  ids.add(v.reviewerId);roots.add(reviewer.ancestryRoot);
  await verifySig(reviewer.publicJwk,p,v.signature);
 }
 if(roots.size<3)throw Error('Three independent reviewer roots required');
 return {sequence:p.sequence,hash:await sha256(canonical(entry))};
}
export async function audit(record,independentPolicy){
 await checkPolicy(independentPolicy);
 if(!record||record.version!==VERSION||!equal(record.policy,independentPolicy)||
 !Array.isArray(record.releases))throw Error('Independent reviewer policy mismatch');
 await verifyGraph(record.graph,independentPolicy.registryDigest);
 let prior={sequence:0,hash:'GENESIS'};
 const ids=new Set();
 for(const entry of record.releases){
  if(ids.has(entry?.payload?.id))throw Error('Duplicate release identifier');
  prior=await validateRelease(entry,record.graph,independentPolicy,prior);
  ids.add(entry.payload.id);
 }
 if(record.releases.length<independentPolicy.minReleaseSequence)
 throw Error('Release history rolled back below independent floor');
 return {valid:true,releases:record.releases.length,retainedGatedNodes:record.graph.nodes.filter(n=>n.classification==='gated').length};
}
export async function approve(record,payload,publicText,votes,policy){
 await audit(record,policy);
 // Independently reproduce the exact petition, not a caller-supplied alternative ancestry.
 const expected=await propose(record,{id:payload?.id,nodeId:payload?.nodeId,publicText,destination:payload?.destination},policy);
 if(!equal(payload,expected))throw Error('Release petition does not match pinned ancestry');
 const next={...cp(record),releases:[...cp(record.releases),{payload:cp(payload),publicText,votes:cp(votes)}]};
 await audit(next,policy);return next;
}
export async function authorizePublication(record,id,scope,trust,clock,policy){
 await audit(record,policy);
 const release=record.releases.find(x=>x.payload.id===id);
 if(!release)throw Error('Release not independently approved');
 // QG-072 receives *the distinct approved public artifact*, never a relabeled gated node.
 const capability=await authorizeAction(scope,{action:'publish',surface:'0root.ai',
  originSurface:'0root.ai',classification:'public'},trust,clock);
 return {allowed:true,artifactId:id,releaseDigest:release.payload.releaseDigest,
  gatedSourcePreserved:true,reviewerRoots:3,capability};
}
export async function fixture(mode='valid'){
 const {fixture:sourceFixture}=await import('./provenance-transformation.mjs');
 const sources=await sourceFixture('gated');
 const reviewers=await Promise.all(Array.from({length:4},()=>generateFixtureSigner()));
 const policy={registryDigest:sources.digest,minReleaseSequence:0,
  reviewers:reviewers.map((k,i)=>({id:'reviewer-'+i,ancestryRoot:mode==='shared-root'&&i===3?'root-1':'root-'+i,publicJwk:k.publicJwk}))};
 let record=await start(sources.record,policy);
 const publicText='Approved synthetic public announcement. No private notebook text.';
 const payload=await propose(record,{id:'release-1',nodeId:'out',publicText},policy);
 const selections=mode==='shared-root'?[0,1,3]:[0,1,2];
 const votes=await Promise.all(selections.map(i=>review(payload,'reviewer-'+i,
  mode==='forged-vote'&&i===2?reviewers[3].privateKey:reviewers[i].privateKey)));
 if(mode==='duplicate')votes[2]=cp(votes[1]);
 if(mode==='pending')return {record,policy,payload,publicText,votes,reviewers};
 if(mode==='tampered')return {record,policy,payload,publicText:publicText+' altered',votes,reviewers};
 record=await approve(record,payload,publicText,votes,policy);
 return {record,policy,payload,publicText,votes,reviewers};
}
export async function scopeFixture(){
 const f=await leaseFixture('active');
 let scope=await scopeStart(f.record,f.trust,f.clock);
 scope=await scopeGrant(scope,f.issuer.privateKey,[{action:'publish',surface:'0root.ai'}],f.trust,f.clock);
 return {scope,trust:f.trust,clock:f.clock};
}
