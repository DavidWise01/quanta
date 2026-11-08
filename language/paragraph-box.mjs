/**
 * QUANTA QG-019 — Paragraph Box
 * A paragraph is an ordered sequence of QG-018 sentence fragments and explicit
 * line-break witnesses, with stable relational addresses and optional context.
 *
 * Geometry is a projection; exact original characters remain in the packet.
 * Not compression, encryption, or natural-language meaning inference.
 */
import {composeSentenceBox,recoverSentenceBox,expandSentenceBox} from "./sentence-box.mjs";
export const PARAGRAPH_VERSION="QG-019.1";
export const PARAGRAPH_CARRIER="||||";
export const PARAGRAPH_LIMIT=4096;
const valid=/^[A-Za-z .,!?;:'"()\-\n]*$/;
function immutable(o){return Object.freeze(o);}
function verifyText(input){
 if(typeof input!=="string"||input.length>PARAGRAPH_LIMIT||!valid.test(input))
  throw new TypeError("Paragraph allows up to 4096 ASCII letters, basic punctuation, spaces and LF line breaks.");
}
function segments(line){
 // Include sentence terminator clusters in the preceding segment; preserve every space.
 const matches=line.match(/[^.!?]*[.!?]+|[^.!?]+$/g)||[];
 const result=[];
 for(const part of matches){
  for(let at=0;at<part.length;at+=128)result.push(part.slice(at,at+128));
 }
 if(result.join("")!==line)throw new Error("Segmentation lost a source character.");
 return result;
}
function construct(input,context){
 let globalIndex=0,segmentIndex=0,sentenceIndex=0;
 const records=[],lines=input.split("\n");
 for(let lineIndex=0;lineIndex<lines.length;lineIndex++){
  const line=lines[lineIndex],chunks=segments(line);
  for(const raw of chunks){
   const box=composeSentenceBox(raw);
   const isEnd=/[.!?]$/.test(raw);
   records.push(immutable({
    type:"sentence",index:segmentIndex++,lineIndex,offset:globalIndex,
    raw,box,endsSentence:isEnd,
    sentenceIndex,contextRef:context===null?null:"paragraph-context"
   }));
   globalIndex+=raw.length;if(isEnd)sentenceIndex++;
  }
  if(lineIndex<lines.length-1){
   records.push(immutable({type:"linebreak",lineIndex,offset:globalIndex,raw:"\n"}));
   globalIndex++;
  }
 }
 if(globalIndex!==input.length)throw new Error("Paragraph offsets mismatched.");
 const withRelations=records.map((r,i)=>{
  if(r.type!=="sentence")return r;
  const prev=records.slice(0,i).reverse().find(x=>x.type==="sentence");
  const next=records.slice(i+1).find(x=>x.type==="sentence");
  return immutable({...r,relation:immutable({
   previous:prev?prev.index:null,next:next?next.index:null,
   previousLine:prev?prev.lineIndex:null,nextLine:next?next.lineIndex:null
  })});
 });
 return immutable(withRelations);
}
export function composeParagraphBox(text,options={}){
 verifyText(text);
 const context=options.context??null;
 if(context!==null&&(typeof context!=="string"||context.length>1024))
  throw new TypeError("Context must be a string of up to 1024 characters or null.");
 const records=construct(text,context);
 return immutable({
  version:PARAGRAPH_VERSION,carrier:PARAGRAPH_CARRIER,
  source:text,context,records,
  lineCount:text.split("\n").length,
  segmentCount:records.filter(r=>r.type==="sentence").length
 });
}
export function recoverParagraphBox(packet){
 if(!packet||packet.version!==PARAGRAPH_VERSION||packet.carrier!==PARAGRAPH_CARRIER||
    typeof packet.source!=="string"||!Array.isArray(packet.records))
   throw new TypeError("Invalid paragraph packet.");
 verifyText(packet.source);
 const expected=composeParagraphBox(packet.source,{context:packet.context});
 if(packet.lineCount!==expected.lineCount||packet.segmentCount!==expected.segmentCount||
    JSON.stringify(packet.records)!==JSON.stringify(expected.records))
   throw new Error("Paragraph ordering, line break, context or relation witness changed.");
 for(const record of packet.records){
  if(record.type==="sentence"&&recoverSentenceBox(record.box)!==record.raw)
   throw new Error("Embedded sentence failed reconstruction.");
 }
 return packet.source;
}
export function expandParagraphBox(packet,level=4){
 const source=recoverParagraphBox(packet);
 if(![1,2,3,4].includes(level))throw new RangeError("Presentation level must be 1–4.");
 const lineItems=[],links=[],actions=[];
 let currentLine=0;
 for(const record of packet.records){
  if(record.type==="linebreak"){currentLine++;continue;}
  const view=expandSentenceBox(record.box,level);
  lineItems.push(immutable({
   index:record.index,lineIndex:record.lineIndex,sentenceIndex:record.sentenceIndex,
   raw:record.raw,offset:record.offset,level,
   glyphCount:view.items.filter(x=>x.kind==="glyph").length,
   dotCount:level===1?view.items.filter(x=>x.kind==="glyph").length:0,
   items:view.items,relationships:view.relationships
  }));
  links.push(immutable({from:record.relation.previous,to:record.index,line:record.lineIndex}));
  actions.push(immutable({verb:"PARAGRAPH_SEGMENT",index:record.index,lineIndex:record.lineIndex}));
  actions.push(...view.somatic);
 }
 return immutable({
  source,context:packet.context,level,
  lines:packet.lineCount,segments:packet.segmentCount,
  items:immutable(lineItems),links:immutable(links),somatic:immutable(actions)
 });
}
export function verifyParagraphBox(packet){
 try{
  const text=recoverParagraphBox(packet),full=expandParagraphBox(packet,4),fold=expandParagraphBox(packet,1);
  const glyphs=full.items.reduce((n,x)=>n+x.glyphCount,0);
  if(fold.items.reduce((n,x)=>n+x.dotCount,0)!==glyphs)
   throw new Error("Folded visual glyph count changed.");
  return immutable({pass:true,lines:full.lines,segments:full.segments,
    glyphs,actions:full.somatic.length,characters:text.length});
 }catch(e){return immutable({pass:false,error:e.message});}
}
