/**
 * QG-037.1 — independent closure witness.
 * This verifier intentionally imports NO QG-036 unpack/recover/verify functions.
 * An independently supplied, trusted manifest is required; caller-controlled
 * manifest and packet together offer no tamper-proof authenticity.
 */
import {verify84211Strict,ACTORS,FACES} from "./byzantine-84211.mjs";
export const VERSION="QG-037.1",CARRIER="||||";
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const clone=x=>JSON.parse(JSON.stringify(x));
function independentlyUnfold(node){
 const leaves=[],visiting=new Set();
 function walk(n,depth){
  if(!n||typeof n!=="object"||Array.isArray(n)||depth>8||visiting.has(n))throw Error("Malformed or cyclic fold node");
  visiting.add(n);
  const keys=Object.keys(n).sort();
  if(n.kind==="pair"){
   if(!equal(keys,["children","kind"])||!Array.isArray(n.children)||n.children.length!==2)throw Error("Invalid pair node");
   walk(n.children[0],depth+1);walk(n.children[1],depth+1);
  }else if(n.kind==="identity"||n.kind==="chamber"){
   if(!equal(keys,["actor","kind","value"]))throw Error("Invalid fold leaf");
   leaves.push(clone(n));
  }else throw Error("Unknown fold kind");
  visiting.delete(n);
 }
 walk(node,0);return leaves;
}
function stagesFromFinal(root){
 const stages=[[root]],nodeLevels=[];
 for(let level=0;level<3;level++){
  const next=[];
  for(const node of stages.at(-1)){
   if(node.kind!=="pair"||!Array.isArray(node.children)||node.children.length!==2)throw Error("Invalid stage nesting");
   next.push(...node.children);
  }
  stages.push(next);
 }
 stages.reverse(); // expected widths 8,4,2,1
 return stages;
}
function manifestFromSource(source){
 verify84211Strict(source);
 if(!source.actors.every(a=>a.closed)||!source.ruling)throw Error("Manifest requires fully closed and judged state");
 return {schema:"QG-037-manifest.1",carrier:CARRIER,actors:clone(source.actors),ruling:clone(source.ruling),events:clone(source.events)};
}
export function buildClosureManifest(source){return manifestFromSource(source)}
export function verifyIndependentClosure(packet,manifest){
 try{
  if(!packet||packet.version!=="QG-036.1"||packet.shape!=="[84211]"||packet.carrier!==CARRIER||!equal(packet.widths,[8,4,2,1,1])||packet.interpretationProven!==false)throw Error("Invalid outer carrier");
  if(!manifest||manifest.schema!=="QG-037-manifest.1"||manifest.carrier!==CARRIER)throw Error("Invalid independent manifest");
  const original=clone({version:"QG-035.1",carrier:CARRIER,outer:[8,4,2,1,1],inner:[1,3,1,1],
   actors:manifest.actors,ruling:manifest.ruling,events:manifest.events});
  verify84211Strict(original);
  if(!original.actors.every(a=>a.closed)||!original.ruling)throw Error("Manifest is not fully sealed");
  if(!Array.isArray(packet.stages)||packet.stages.length!==5||!equal(packet.stages.map(s=>s.length),[8,4,2,1,1]))throw Error("Incorrect fold widths");
  if(!equal(packet.stages[3],packet.stages[4]))throw Error("Last 1 to 1 must be identical");
  const independent=stagesFromFinal(packet.stages[4][0]);
  if(!equal(packet.stages.slice(0,4),independent))throw Error("Intermediate tree differs from final independent unfolding");
  const leaves=independentlyUnfold(packet.stages[4][0]);
  if(leaves.length!==8)throw Error("Exactly eight leaves required");
  for(let i=0;i<4;i++){
   const id=ACTORS[i],ident=leaves[i*2],chamber=leaves[i*2+1];
   if(ident.kind!=="identity"||ident.actor!==id||ident.value!==id)throw Error("Actor identity differs");
   if(chamber.kind!=="chamber"||chamber.actor!==id||!equal(chamber.value,manifest.actors[i]))throw Error("Chamber does not match independently supplied manifest");
   if(chamber.value.faces.length!==6||new Set(chamber.value.faces).size!==6||chamber.value.faces.some(f=>!FACES.includes(f)))throw Error("Chamber has missing face");
  }
  if(!equal(packet.stages[0],leaves))throw Error("Stage zero differs from final folded leaves");
  // The verdict and event history are NOT stored inside the 8 witness leaves:
  // compare them against their external manifest and the QG-036 wrapper.
  if(!equal(packet.source,original)||!equal(packet.ledgerEvents,manifest.events))throw Error("Verdict, source or event history differs from independent manifest");
  return {pass:true,actors:4,faces:24,leaves:8,fold:[8,4,2,1,1],verdict:original.ruling.outcome,
   independentlyRecovered:true,manifestRequired:true,interpretationProven:false};
 }catch(e){return {pass:false,error:e.message}}
}
