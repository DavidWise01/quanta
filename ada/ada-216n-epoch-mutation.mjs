// ADA-216N .dlw — prospective epoch adaptation, separate from immutable source.
import {verifyChain,canonical,fnv64,bound} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy,EPOCH_SIZE} from "./ada-211n-epoch-engine.mjs";
import {deriveEpochContacts} from "./ada-214n-epoch-contacts.mjs";
export function deriveEpochMutation(chain){
 const check=verifyChain(chain);if(!check.pass)throw Error(check.reason);
 const epochs=epochHierarchy(chain),contacts=deriveEpochContacts(chain),out=[];
 let units=0;
 for(const e of epochs){
  if(e.state!=="SEALED")continue;
  const c=contacts[e.epoch],t=c.state.toph;
  const allowed=t.eligibleToSeal&&t.heldDecisions===0&&t.minimumStability>=90&&t.minimumEnergy>=5;
  const proposed=allowed?Math.sign(c.state.jane.deltaFromParent):0;
  const next=bound(units+proposed,-10,10);
  const body={schema:"ADA-216N.epoch-mutation.v1",epoch:e.epoch,epochHash:e.hash,contactHash:c.hash,parent:out.at(-1)?.hash??null,effectiveEpoch:e.epoch+1,decision:!allowed?"HOLD":next===units?"UNCHANGED":"ADAPT",step:(next-units)/40,offset:next/40,growthFactor:1.025};
  units=next;out.push(Object.freeze({...body,hash:fnv64(canonical(body))}));
 }
 return Object.freeze(out);
}
export function verifyEpochMutation(chain,ledger){
 try{return {pass:canonical(deriveEpochMutation(chain))===canonical(ledger)}}catch(e){return {pass:false,reason:e.message}}
}
