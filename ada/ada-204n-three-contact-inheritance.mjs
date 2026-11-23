// ADA-204N · Three-contact generational inheritance, an additive derived ledger.
// NEVER mutates an ADA-201N node, the ADA-202N archive, or its Phase II source root.
import {PHASE_II_FREEZE,verifyChain,fnv64,canonical,bound} from "./ada-201n-generational-engine.mjs";
export const CONTACT_SCHEMA="ADA-204N.contacts.v1";
const r5=x=>Number(x.toFixed(5));
const freeze=x=>Object.freeze(x);
const identity=(n,role)=>"ADA204-"+role+"-G"+String(n).padStart(5,"0");
function record(parent,gen){
 const n=gen.n,previous=parent?.state||null;
 const jane=freeze({id:identity(n,"JANE"),inherited:previous?.jane.id||null,observation:gen.contacts[0],delta:r5(gen.contacts[0]-(previous?.jane.observation??gen.contacts[0]))});
 const toph=freeze({id:identity(n,"TOPH"),inherited:previous?.toph.id||null,stability:gen.stability,energy:gen.energy,eligible:n===0?true:gen.stability>=90&&gen.energy>=5,criterion:"stability >= 90 AND energy >= 5"});
 const ada=freeze({id:identity(n,"ADA"),inherited:previous?.ada.id||null,action:n===0?"ROOT":toph.eligible?"APPEND":"HOLD",authority:"ONE_DIODIC_GATE"});
 // A HOLD is a preserved generation event, not deletion of the child node.
 const state=freeze({jane,toph,ada});
 const body={schema:CONTACT_SCHEMA,n,generationHash:gen.hash,sourceRoot:PHASE_II_FREEZE,parent:parent?.hash||null,state,decision:ada.action};
 return freeze({...body,hash:fnv64(canonical(body))});
}
export function deriveContacts(chain){
 const audit=verifyChain(chain);if(!audit.pass)throw Error("Cannot inherit from invalid generation chain: "+audit.reason);
 const out=[];for(const gen of chain)out.push(record(out.at(-1),gen));
 return freeze(out);
}
export function verifyContacts(chain,ledger){
 try{
  if(!Array.isArray(ledger)||ledger.length!==chain.length)return {pass:false,reason:"Contact ledger length mismatch"};
  const expected=deriveContacts(chain);
  for(let i=0;i<expected.length;i++)if(canonical(ledger[i])!==canonical(expected[i]))return {pass:false,reason:"Contact derivation mismatch at n="+i};
  return {pass:true,generations:ledger.length,tip:ledger.at(-1).hash,holds:ledger.filter(x=>x.decision==="HOLD").length,append:ledger.filter(x=>x.decision==="APPEND").length,root:PHASE_II_FREEZE};
 }catch(error){return {pass:false,reason:error.message}}
}
export function contactProof(chain,n=chain.length-1){
 if(!Number.isSafeInteger(n)||n<0||n>=chain.length)throw Error("Invalid generation");
 const ledger=deriveContacts(chain),entry=ledger[n];
 return freeze({schema:"ADA-204N.contact-proof.v1",n,sourceRoot:PHASE_II_FREEZE,sourceGenerationHash:chain[n].hash,contactHash:entry.hash,previousContactHash:entry.parent,contacts:entry.state,decision:entry.decision,independentSourceRoots:1});
}
