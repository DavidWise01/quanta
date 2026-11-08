/**
 * QUANTA QG-020 — Corpus Box, deterministic structured document transport.
 *
 * carrier ||||; corpus > documents > chapters > sections > paragraphs
 * Each paragraph is an exact QG-019 packet. Stable scoped IDs address source.
 * References are explicit, validated graph edges between existing addresses.
 * Canonical reconstruction checks all nested source and relational metadata.
 *
 * No compression, cryptography, automatic semantic inference or 11D physics.
 */
import {composeParagraphBox,recoverParagraphBox,expandParagraphBox} from "./paragraph-box.mjs";
export const CORPUS_VERSION="QG-020.1";
export const CORPUS_CARRIER="||||";
export const CORPUS_MAX_DOCUMENTS=8;
export const CORPUS_MAX_CHAPTERS=16;
export const CORPUS_MAX_SECTIONS=16;
export const CORPUS_MAX_PARAGRAPHS=32;
export const CORPUS_MAX_REFERENCES=256;
const SLUG=/^[a-z][a-z0-9-]{0,47}$/;
const freeze=Object.freeze;
function label(v,where,max=120){
 if(typeof v!=="string"||v.length>max||/[^\x20-\x7e]/.test(v))throw new TypeError(where+" must be printable ASCII up to "+max+" characters.");
 return v;
}
function slug(v,where){if(typeof v!=="string"||!SLUG.test(v))throw new TypeError(where+" needs a simple lowercase slug.");return v}
function arr(a,where,max){if(!Array.isArray(a)||a.length>max)throw new TypeError(where+" must be an array of <= "+max);return a;}
function explicitKeys(value,keys,where){
 if(!value||typeof value!=="object"||Array.isArray(value)||Object.keys(value).some(k=>!keys.includes(k)))
  throw new TypeError(where+" has invalid keys");
}
function distinct(items,where){
 const seen=new Set();for(const item of items){if(seen.has(item.id))throw new Error("Duplicate "+where+" ID "+item.id);seen.add(item.id)}
}
function sourceInput(source){
 explicitKeys(source,["title","documents","references"],"corpus");
 label(source.title,"Corpus title");
 const docs=arr(source.documents,"documents",CORPUS_MAX_DOCUMENTS);
 const references=arr(source.references??[],"references",CORPUS_MAX_REFERENCES);
 const documentOut=[];
 for(const doc of docs){
  explicitKeys(doc,["id","title","chapters"],"document");
  slug(doc.id,"Document ID");label(doc.title,"Document title");
  const chapters=arr(doc.chapters,"chapters",CORPUS_MAX_CHAPTERS);const chapterOut=[];
  for(const chapter of chapters){
   explicitKeys(chapter,["id","title","sections"],"chapter");
   slug(chapter.id,"Chapter ID");label(chapter.title,"Chapter title");
   const sections=arr(chapter.sections,"sections",CORPUS_MAX_SECTIONS);const sectionOut=[];
   for(const sec of sections){
    explicitKeys(sec,["id","title","paragraphs"],"section");
    slug(sec.id,"Section ID");label(sec.title,"Section title");
    const paragraphs=arr(sec.paragraphs,"paragraphs",CORPUS_MAX_PARAGRAPHS);
    if(!paragraphs.every(p=>typeof p==="string"))throw new TypeError("Every paragraph must be text.");
    sectionOut.push(freeze({id:sec.id,title:sec.title,paragraphs:freeze([...paragraphs])}));
   }
   distinct(sectionOut,"section");
   chapterOut.push(freeze({id:chapter.id,title:chapter.title,sections:freeze(sectionOut)}));
  }
  distinct(chapterOut,"chapter");
  documentOut.push(freeze({id:doc.id,title:doc.title,chapters:freeze(chapterOut)}));
 }
 distinct(documentOut,"document");
 const refs=references.map(ref=>{
  explicitKeys(ref,["from","to","relation"],"reference");
  if(typeof ref.from!=="string"||typeof ref.to!=="string"||typeof ref.relation!=="string"||
    !/^[a-z][a-z0-9-]{0,31}$/.test(ref.relation))throw new TypeError("Invalid reference");
  return freeze({from:ref.from,to:ref.to,relation:ref.relation});
 });
 return freeze({title:source.title,documents:freeze(documentOut),references:freeze(refs)});
}
function assemble(source){
 const canonical=sourceInput(source),items=[],index={};let order=0,previous=null;
 const add=(address,type,text,metadata,box=null)=>{
  if(Object.hasOwn(index,address))throw new Error("Duplicate corpus address "+address);
  const item=freeze({address,order:order++,type,text,metadata:freeze(metadata),
   previous,paragraph:box});
  items.push(item);index[address]=items.length-1;previous=address;
 };
 for(const doc of canonical.documents){
  const da="doc/"+doc.id;
  add(da,"document",doc.title,{documentId:doc.id});
  for(const chapter of doc.chapters){
   const ca=da+"/ch/"+chapter.id;
   add(ca,"chapter",chapter.title,{documentId:doc.id,chapterId:chapter.id});
   for(const sec of chapter.sections){
    const sa=ca+"/sec/"+sec.id;
    add(sa,"section",sec.title,{documentId:doc.id,chapterId:chapter.id,sectionId:sec.id});
    for(let p=0;p<sec.paragraphs.length;p++){
     const address=sa+"/p/"+p,text=sec.paragraphs[p];
     add(address,"paragraph",text,{documentId:doc.id,chapterId:chapter.id,sectionId:sec.id,paragraphIndex:p},
       composeParagraphBox(text));
    }
   }
  }
 }
 const links=canonical.references.map((ref,referenceIndex)=>{
  if(!Object.hasOwn(index,ref.from)||!Object.hasOwn(index,ref.to))
   throw new Error("Reference endpoint does not exist");
  return freeze({...ref,referenceIndex});
 });
 return {canonical,items:freeze(items),links:freeze(links),index:freeze(index)};
}
export function composeCorpusBox(source){
 const {canonical,items,links,index}=assemble(source);
 return freeze({version:CORPUS_VERSION,carrier:CORPUS_CARRIER,
  source:canonical,items,links,index,
  totalParagraphs:items.filter(i=>i.type==="paragraph").length});
}
export function recoverCorpusBox(packet){
 if(!packet||packet.version!==CORPUS_VERSION||packet.carrier!==CORPUS_CARRIER)throw new TypeError("Unknown corpus packet");
 const expected=composeCorpusBox(packet.source);
 if(packet.totalParagraphs!==expected.totalParagraphs||
    JSON.stringify(packet.items)!==JSON.stringify(expected.items)||
    JSON.stringify(packet.links)!==JSON.stringify(expected.links)||
    JSON.stringify(packet.index)!==JSON.stringify(expected.index))
   throw new Error("Corpus ordering, source, references or index altered");
 for(const item of packet.items)if(item.type==="paragraph" &&
     recoverParagraphBox(item.paragraph)!==item.text)throw new Error("Paragraph transport failed");
 return expected.source;
}
export function lookupCorpus(packet,address){
 recoverCorpusBox(packet);
 if(typeof address!=="string"||!Object.hasOwn(packet.index,address))throw new RangeError("Unknown corpus address");
 return packet.items[packet.index[address]];
}
export function expandCorpusBox(packet,level=4){
 recoverCorpusBox(packet);
 if(![1,2,3,4].includes(level))throw new RangeError("Level must be 1–4");
 const items=packet.items.map(item=>{
  if(item.type!=="paragraph")return freeze({address:item.address,type:item.type,label:item.text});
  const view=expandParagraphBox(item.paragraph,level);
  return freeze({address:item.address,type:"paragraph",text:item.text,level,
    lineCount:view.lines,segmentCount:view.segments,
    glyphCount:view.items.reduce((n,x)=>n+x.glyphCount,0),
    dotCount:view.items.reduce((n,x)=>n+x.dotCount,0),
    actions:view.somatic.length});
 });
 return freeze({level,carrier:CORPUS_CARRIER,items:freeze(items),links:packet.links,
  paragraphs:packet.totalParagraphs});
}
export function verifyCorpusBox(packet){
 try{
  const recovered=recoverCorpusBox(packet);
  const full=expandCorpusBox(packet,4),dots=expandCorpusBox(packet,1);
  const count=full.items.reduce((n,x)=>n+(x.glyphCount||0),0);
  const folded=dots.items.reduce((n,x)=>n+(x.dotCount||0),0);
  if(count!==folded)throw new Error("Dot count and glyph count differ");
  return freeze({pass:true,documents:recovered.documents.length,paragraphs:packet.totalParagraphs,
    references:packet.links.length,addresses:packet.items.length,glyphs:count});
 }catch(e){return freeze({pass:false,error:e.message});}
}
