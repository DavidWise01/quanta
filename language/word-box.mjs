/**
 * QUANTA QG-017 · compositional box transport.
 * Canonical grammar: |||| ( ||A|| ... ||Z|| | SPACE )* ||||
 *
 * Unlike QG-016's 4 fully expanded rotations per glyph, this transport packet
 * carries minimal reversible references to the canonical glyph dictionary.
 * Geometry, somatic verbs and presentation states are reconstructed on receipt.
 *
 * Per-glyph phase follows a→b→c→d, advancing by 90° on each letter.
 * Spaces separate words and reset the phase. The separator and original order
 * remain stored explicitly. Semantic tokens are contextual annotations, not
 * independent natural-language understanding.
 */
import {transportLetter, recoverLetter, rotatePoint, pathsFor, tokenFor} from "./alphabet-box.mjs";

export const WORD_BOX_VERSION="QG-017.1";
export const WORD_CARRIER="||||";
export const WORD_PHASES=Object.freeze(["a","b","c","d"]);
export const WORD_ANGLES=Object.freeze([0,90,180,270]);
export const WORD_LEVELS=Object.freeze([4,3,2,1]);
export const WORD_MAX_LENGTH=128;
const GRAMMAR=/^[A-Z]*(?: [A-Z]+)*$/;
function checkInput(value){
 if(typeof value!=="string"||value.length>WORD_MAX_LENGTH||!GRAMMAR.test(value))
  throw new TypeError("Expected uppercase A–Z words, separated by one space, max 128 chars.");
}
function freezeRecord(item){return Object.freeze(item)}
function makeActions(letter,angle,offset,wordIndex,letterIndex){
 const p=transportLetter(letter).quads.find(q=>q.degrees===angle);
 return Object.freeze(p.somatic.map(event=>freezeRecord({
  ...event, letter, wordIndex, letterIndex,
  to:event.to?freezeRecord({x:event.to.x+offset,y:event.to.y}):undefined,
  from:event.from?freezeRecord({x:event.from.x+offset,y:event.from.y}):undefined,
  at:event.at?freezeRecord({x:event.at.x+offset,y:event.at.y}):undefined
 })));
}
function tokenAt(ch,index,wordIndex,inWordIndex,angle,offset){
 return freezeRecord({
  type:"glyph",index,wordIndex,inWordIndex,
  token:tokenFor(ch),phase:WORD_PHASES[angle/90],degrees:angle,
  offset,levelSchedule:WORD_LEVELS
 });
}
export function composeWordBox(input,options={}){
 checkInput(input);
 const context=options.context??null;
 if(context!==null&&(typeof context!=="string"||context.length>512))
   throw new TypeError("Context must be a string <=512 characters or null.");
 let wordIndex=0,inWordIndex=0,cursor=0,phase=0;
 const packets=[];
 for(let index=0;index<input.length;index++){
  const ch=input[index];
  if(ch===" "){
   packets.push(freezeRecord({type:"space",index,offset:cursor,width:2}));
   wordIndex++;inWordIndex=0;cursor+=2;phase=0;
  }else{
   packets.push(tokenAt(ch,index,wordIndex,inWordIndex,phase*90,cursor));
   inWordIndex++;cursor+=6;phase=(phase+1)%4;
  }
 }
 return freezeRecord({version:WORD_BOX_VERSION,carrier:WORD_CARRIER,source:input,context,
    tokens:Object.freeze(packets),width:cursor});
}
function canonicalEqual(a,b){return JSON.stringify(a)===JSON.stringify(b);}
export function recoverWordBox(packet){
 if(!packet||packet.version!==WORD_BOX_VERSION||packet.carrier!==WORD_CARRIER ||
  typeof packet.source!=="string"||!Array.isArray(packet.tokens))
   throw new TypeError("Invalid word transport packet.");
 checkInput(packet.source);
 // Derive all expected ordered indices, spaces, offsets and rotations afresh.
 const expected=composeWordBox(packet.source,{context:packet.context});
 if(packet.width!==expected.width||!canonicalEqual(packet.tokens,expected.tokens))
   throw new Error("Word order / spacing / phase / offset witness mismatch.");
 return packet.source;
}
export function expandWordBox(packet,level=4){
 const source=recoverWordBox(packet);
 if(!WORD_LEVELS.includes(level))throw new RangeError("Level must be 4, 3, 2, or 1.");
 const rendered=[];
 const actions=[];
 for(const t of packet.tokens){
  if(t.type==="space"){rendered.push(freezeRecord({...t,view:{kind:"space"}}));continue;}
  const glyph=transportLetter(t.token[2]).quads[t.degrees/90];
  const view=glyph.levels.find(s=>s.level===level).view;
  let world;
  if(view.kind==="geometry"){
   world=freezeRecord({kind:view.kind,paths:Object.freeze(view.paths.map(stroke=>Object.freeze(stroke.map(p=>freezeRecord({x:p.x+t.offset,y:p.y}))))});
  }else if(view.kind==="chrome-dot"){
   world=freezeRecord({kind:view.kind,point:freezeRecord({x:view.point.x+t.offset,y:view.point.y})});
  }else{
   world=freezeRecord({kind:view.kind,points:Object.freeze(view.points.map(p=>freezeRecord({x:p.x+t.offset,y:p.y})))});
  }
  rendered.push(freezeRecord({...t,view:world}));
  actions.push(...makeActions(t.token[2],t.degrees,t.offset,t.wordIndex,t.inWordIndex));
 }
 return freezeRecord({source,level,width:packet.width,items:Object.freeze(rendered),somatic:Object.freeze(actions),
   semantic:freezeRecord({text:source,context:packet.context,words:Object.freeze(source?source.split(" "):[])})});
}
export function verifyWordBox(packet){
 try{
  const recovered=recoverWordBox(packet),e4=expandWordBox(packet,4),e1=expandWordBox(packet,1);
  const letters=[...recovered].filter(ch=>ch!==" ").length;
  if(e4.items.length!==recovered.length||e1.items.length!==recovered.length)throw new Error("Lost character locations");
  if(e4.somatic.some(a=>a.letterIndex<0||a.wordIndex<0))throw new Error("Invalid somatic address");
  return freezeRecord({pass:true,letters,spaces:recovered.length-letters,
   verbs:e4.somatic.length,quads:4,levels:4,source:recovered});
 }catch(e){return freezeRecord({pass:false,error:e.message});}
}
