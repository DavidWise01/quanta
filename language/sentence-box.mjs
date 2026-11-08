/**
 * QUANTA QG-018 — sentence transport.
 * A sentence is an ordered stream of word boxes, punctuation, case and spaces.
 * Word boxes use QG-017, while the sentence owns the inter-word phase register.
 * The phase is continuous across words and resets at '.', '?' or '!'.
 *
 * This is a geometric syntax language, not encryption or natural-language inference.
 */
import { composeWordBox, recoverWordBox, expandWordBox } from "./word-box.mjs";
import { transportLetter } from "./alphabet-box.mjs";

export const SENTENCE_BOX_VERSION="QG-018.1";
export const SENTENCE_CARRIER="||||";
export const SENTENCE_MAX=512;
export const SENTENCE_PHASES=Object.freeze(["a","b","c","d"]);
export const SENTENCE_ENDINGS=Object.freeze([".","?","!"]);
const VALID=/^[A-Za-z .,!?;:'"()-]*$/;
const SCAN=/[A-Za-z]+| +|[.,!?;:'"()-]/g;

function freeze(value){return Object.freeze(value);}
function assertSource(text){
 if(typeof text!=="string" || text.length>SENTENCE_MAX || !VALID.test(text)){
  throw new TypeError("Sentence must be <=512 characters using A-Z, a-z, spaces or permitted punctuation.");
 }
}
function tokenize(text){
 let offset=0, wordIndex=0, phase=0, sentenceIndex=0, previousWordIndex=null;
 const tokens=[];
 for(const match of text.matchAll(SCAN)){
  const raw=match[0],start=match.index;
  if(start!==offset)throw new Error("Unparsed sentence input");
  offset=start+raw.length;
  if(/^[A-Za-z]+$/.test(raw)){
   const upper=raw.toUpperCase();
   const wordBox=composeWordBox(upper);
   const caseMask=[...raw].map((ch)=>ch!==ch.toUpperCase()?1:0).join("");
   const entryPhase=phase;
   phase=(phase+raw.length)%4;
   tokens.push(freeze({
    kind:"word",start,end:offset,raw,upper,caseMask,wordIndex,sentenceIndex,
    entryPhase,exitPhase:phase,
    phase:SENTENCE_PHASES[entryPhase],
    relation:freeze({follows:previousWordIndex,precedes:null}),
    box:wordBox
   }));
   previousWordIndex=wordIndex;wordIndex++;
  }else if(/^ +$/.test(raw)){
   tokens.push(freeze({kind:"space",start,end:offset,raw,count:raw.length,sentenceIndex}));
  }else{
   const boundary=SENTENCE_ENDINGS.includes(raw);
   tokens.push(freeze({kind:"punctuation",start,end:offset,raw,
     action:boundary?"SENTENCE_END":"MARK",
     phaseBefore:phase,phaseAfter:boundary?0:phase,
     sentenceIndex
   }));
   if(boundary){phase=0;sentenceIndex++;previousWordIndex=null;}
  }
 }
 if(offset!==text.length)throw new Error("Tokenizer skipped content");
 // Link adjacent word tokens within each sentence, ignoring spaces and soft punctuation.
 const words=tokens.filter(t=>t.kind==="word");
 const nextWord=new Map();
 for(let i=0;i<words.length;i++){
  const w=words[i],next=words[i+1];
  nextWord.set(w.wordIndex,next&&next.sentenceIndex===w.sentenceIndex?next.wordIndex:null);
 }
 return freeze(tokens.map(t=>t.kind==="word"
  ? freeze({...t,relation:freeze({...t.relation,precedes:nextWord.get(t.wordIndex)})})
  :t));
}
export function composeSentenceBox(text,options={}){
 assertSource(text);
 const context=options.context??null;
 if(context!==null && (typeof context!=="string"||context.length>512))
  throw new TypeError("Context must be a string up to 512 characters or null.");
 const tokens=tokenize(text);
 return freeze({
  version:SENTENCE_BOX_VERSION,carrier:SENTENCE_CARRIER,source:text,context,
  tokens,sentenceCount:tokens.filter(t=>t.kind==="punctuation"&&t.action==="SENTENCE_END").length,
  wordCount:tokens.filter(t=>t.kind==="word").length
 });
}
export function recoverSentenceBox(packet){
 if(!packet||packet.version!==SENTENCE_BOX_VERSION||packet.carrier!==SENTENCE_CARRIER||
 typeof packet.source!=="string"||!Array.isArray(packet.tokens))throw new TypeError("Invalid sentence box.");
 assertSource(packet.source);
 const expected=composeSentenceBox(packet.source,{context:packet.context});
 if(JSON.stringify(packet.tokens)!==JSON.stringify(expected.tokens) ||
 packet.sentenceCount!==expected.sentenceCount ||
 packet.wordCount!==expected.wordCount){
  throw new Error("Sentence order, phase, punctuation or context witness mismatch");
 }
 for(const t of packet.tokens)if(t.kind==="word" && recoverWordBox(t.box)!==t.upper){
  throw new Error("Word box failed to recover");
 }
 return packet.source;
}
/** Expand every word using sentence-global phases, with explicit 'PEN_UP' gaps. */
export function expandSentenceBox(packet,level=4){
 const original=recoverSentenceBox(packet);
 if(![1,2,3,4].includes(level))throw new RangeError("Level must be 1..4.");
 let cursor=0;
 const items=[],somatic=[],relationships=[];
 for(const t of packet.tokens){
  if(t.kind!=="word"){
   items.push(freeze({...t,x:cursor}));
   cursor+=t.kind==="space"?t.count*3:3;
   continue;
  }
  const local=expandWordBox(t.box,level);
  const run=[];
  for(let i=0;i<t.upper.length;i++){
   const letter=t.upper[i],angle=((t.entryPhase+i)%4)*90;
   const quad=transportLetter(letter).quads[angle/90];
   const view=quad.levels.find(s=>s.level===level).view;
   const x=cursor+i*6;
   function translate(p){return freeze({x:p.x+x,y:p.y});}
   const world=view.kind==="geometry"
     ?freeze({kind:"geometry",paths:freeze(view.paths.map(stroke=>freeze(stroke.map(translate))))})
     :view.kind==="chrome-dot"
     ?freeze({kind:"chrome-dot",point:translate(view.point)})
     :freeze({kind:view.kind,points:freeze(view.points.map(translate))});
   const glyph=freeze({kind:"glyph",letter: t.raw[i],canonical:letter,
     wordIndex:t.wordIndex,sentenceIndex:t.sentenceIndex,phase:SENTENCE_PHASES[angle/90],
     degrees:angle,x,view:world});
   run.push(glyph);items.push(glyph);
   somatic.push(freeze({verb:"PEN_UP",x,wordIndex:t.wordIndex}));
   for(const v of quad.somatic){
    somatic.push(freeze({...v,wordIndex:t.wordIndex,sentenceIndex:t.sentenceIndex,
      letter,from:v.from?translate(v.from):undefined,to:v.to?translate(v.to):undefined,
      at:v.at?translate(v.at):undefined}));
   }
  }
  relationships.push(freeze({word:t.raw,index:t.wordIndex,sentenceIndex:t.sentenceIndex,
    follows:t.relation.follows,precedes:t.relation.precedes,
    entryPhase:t.phase,exitPhase:SENTENCE_PHASES[t.exitPhase]}));
  cursor+=t.upper.length*6;
 }
 return freeze({level,source:original,context:packet.context,width:cursor,
   items:freeze(items),somatic:freeze(somatic),relationships:freeze(relationships)});
}
export function verifySentenceBox(packet){
 try{
  const text=recoverSentenceBox(packet),deep=expandSentenceBox(packet,4);
  const shallow=expandSentenceBox(packet,1);
  if(deep.relationships.length!==packet.wordCount||
     shallow.items.filter(t=>t.kind==="glyph").length!==[...text].filter(c=>/[A-Za-z]/.test(c)).length)
      throw new Error("Geometry composition or word relationships lost");
  return freeze({pass:true,source:text,words:packet.wordCount,boundaries:packet.sentenceCount,
    glyphs:shallow.items.filter(t=>t.kind==="glyph").length,verbs:deep.somatic.length});
 }catch(e){return freeze({pass:false,error:e.message});}
}
