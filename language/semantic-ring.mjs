/**
 * QUANTA QG-028.1 — Bind semantic SEE/DO/LEARN roles to the 60-station ring.
 *
 * For letter L with entry phase q, role r = 0/1/2:
 *   phase(L,r) = (q+r) mod 4
 *   station(L,r) = (home(anchor(L)) + 15*phase(L,r)) mod 60.
 *
 * Anchor is first point of the first canonical glyph stroke.
 * DO carries the same QG-026 ordered somatic pen verbs; SEE and LEARN
 * retain full geometry and canonical context as observations.
 * This encodes prescribed roles, not learned behavior or implicit meaning.
 */
import {semanticTriad,SEMANTIC_ALPHABET} from "./semantic-triad.mjs";
import {transportAlphabetRing,recoverAlphabetRing} from "./alphabet-ring.mjs";
import {locateStation,phaseStation} from "./sexagesimal-ring.mjs";

export const VERSION="QG-028.1";
export const CARRIER="||||";
export const ROLES=Object.freeze(["see","do","learn"]);
const freeze=Object.freeze;
function validateLetter(letter){
 if(typeof letter!=="string"||!/^[A-Z]$/.test(letter))throw new TypeError("Letter must be A–Z");
}
function validatePhase(q){
 if(!Number.isInteger(q)||q<0||q>3)throw new RangeError("Entry phase must be 0..3");
}
export function bindSemanticLetter(letter,entryPhase=0){
 validateLetter(letter);validatePhase(entryPhase);
 const triad=semanticTriad(letter);
 const roles=freeze(ROLES.map((role,offset)=>{
  const quad=(entryPhase+offset)%4;
  const glyph=transportAlphabetRing(letter,quad);
  const anchor=glyph.geometry[0]?.vertices[0];
  if(!anchor)throw new Error("Canonical glyph has no anchor vertex");
  return freeze({
   role,term:triad.roles[role],offset,phase:quad,
   degrees:quad*90,station:anchor.station,
   anchorHome:anchor.home,location:locateStation(anchor.station),
   glyph,verbs:role==="do"?glyph.somatic:freeze([])
  });
 }));
 return freeze({version:VERSION,carrier:CARRIER,letter,token:triad.token,
  entryPhase,roles,
  exitPhase:(entryPhase+3)%4});
}
export function recoverSemanticLetter(packet){
 if(!packet||packet.version!==VERSION||packet.carrier!==CARRIER||
  typeof packet.letter!=="string"||!Number.isInteger(packet.entryPhase))
  throw new TypeError("Unknown semantic ring binding");
 const expected=bindSemanticLetter(packet.letter,packet.entryPhase);
 if(JSON.stringify(packet)!==JSON.stringify(expected))throw new Error("Semantic/ring binding witness mismatch");
 for(const r of packet.roles)recoverAlphabetRing(r.glyph);
 return packet.letter;
}
export function bindSemanticText(text){
 if(typeof text!=="string"||text.length>128||!/^[A-Z ]*$/.test(text))
  throw new TypeError("Expected 0–128 uppercase letters and spaces");
 let phase=0;
 const items=freeze([...text].map((ch,index)=>{
  if(ch===" "){phase=0;return freeze({kind:"space",index,char:" ",resetTo:0})}
  const binding=bindSemanticLetter(ch,phase);
  phase=(phase+1)%4;
  return freeze({kind:"letter",index,char:ch,binding});
 }));
 return freeze({version:VERSION,carrier:CARRIER,source:text,items,terminalPhase:phase});
}
export function recoverSemanticText(packet){
 if(!packet||packet.version!==VERSION||packet.carrier!==CARRIER||
   typeof packet.source!=="string")throw new TypeError("Unknown semantic text packet");
 const expected=bindSemanticText(packet.source);
 if(JSON.stringify(packet)!==JSON.stringify(expected))throw new Error("Semantic text sequence or role witness mismatch");
 return packet.source;
}
export function verifySemanticBinding(packet){
 try{
  const text=recoverSemanticText(packet);
  const glyphs=packet.items.filter(x=>x.kind==="letter");
  for(const g of glyphs)recoverSemanticLetter(g.binding);
  return freeze({pass:true,source:text,letters:glyphs.length,
    roles:glyphs.length*3,completeAlphabet:SEMANTIC_ALPHABET.length,
    stations:60,doVerbs:glyphs.reduce((n,g)=>n+g.binding.roles[1].verbs.length,0)});
 }catch(error){return freeze({pass:false,error:error.message});}
}
