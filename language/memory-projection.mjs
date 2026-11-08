/**
 * QUANTA QG-022.1 — Memory Projection.
 * One displayed Chrome Dot selects ONE immutable QG-021 corpus revision.
 * The retained ledger and reference are the witness; the dot is not a
 * compressed archive or source of cryptographic authenticity.
 */
import {
  verifyCorpusMemory,recoverCorpusRevision,traceCorpusLineage
} from "./corpus-memory.mjs";
import {expandCorpusBox} from "./corpus-box.mjs";

export const PROJECTION_VERSION="QG-022.1";
export const PROJECTION_CARRIER="||||";
export const PROJECTION_LEVELS=Object.freeze([4,3,2,1]);
const freeze=Object.freeze;
function check(memory) {
 const report=verifyCorpusMemory(memory);
 if(!report.pass)throw new Error("Invalid corpus memory: "+report.error);
 return report;
}
function findRevision(memory,id) {
 const revision=memory.revisions.find(r=>r.id===id);
 if(!revision)throw new RangeError("Unknown revision ID");
 return revision;
}
function sourceMetrics(revision) {
 const source=recoverCorpusRevision(
  {version:"QG-021.1",carrier:"||||",revisions:[{
   ...revision,id:"r0000",index:0,parent:null,lineage:[]
  }]}, "r0000");
 const paragraphs=revision.snapshot.items.filter(x=>x.type==="paragraph");
 const letters=paragraphs.reduce((sum,p)=>sum+([...p.text].filter(x=>/[A-Za-z]/.test(x)).length),0);
 return freeze({documents:source.documents.length,paragraphs:paragraphs.length,
   letters,addresses:revision.snapshot.items.length});
}
/** Build a complete projection record that holds only an address, not source copies. */
export function projectCorpusRevision(memory,id) {
 check(memory);
 const r=findRevision(memory,id),metrics=sourceMetrics(r);
 const phases=freeze(PROJECTION_LEVELS.map(level=>{
  const view=expandCorpusBox(r.snapshot,level);
  const dots=level===1 ? metrics.letters : 0;
  return freeze({level,glyphs:metrics.letters,dots,
   addresses:view.items.length,description:
    level===4?"source strokes":
    level===3?"vertices":
    level===2?"endpoints":"one visible revision Chrome Dot"});
 }));
 return freeze({
  version:PROJECTION_VERSION,carrier:PROJECTION_CARRIER,
  revision:id,ledgerVersion:memory.version,
  terminal:freeze({kind:"chrome-dot",glyph:"•",revision:id}),
  metrics,phases,
  witness:freeze({kind:"ledger-reference",revision:id,parent:r.parent})
 });
}
/** Recompute and compare a projection before showing source. */
export function unfoldCorpusProjection(memory,projection) {
 check(memory);
 if(!projection||projection.version!==PROJECTION_VERSION||
    projection.carrier!==PROJECTION_CARRIER||typeof projection.revision!=="string")
  throw new TypeError("Unknown memory projection");
 const expected=projectCorpusRevision(memory,projection.revision);
 if(JSON.stringify(expected)!==JSON.stringify(projection))
  throw new Error("Projection witness, phase or revision mismatch");
 const source=recoverCorpusRevision(memory,projection.revision);
 return freeze({revision:projection.revision,source,metrics:expected.metrics});
}
/** Walk backward from the selected revision, never overwriting source. */
export function walkRevisionHistory(memory,id) {
 check(memory);
 const r=findRevision(memory,id),stack=[];
 for(let i=r.index;i>=0;i--){
  const step=memory.revisions[i];
  stack.push(freeze({
   revision:step.id,parent:step.parent,comment:step.comment,
   addresses:step.snapshot.items.length,
   paragraphs:step.snapshot.totalParagraphs,
   changes:freeze(step.lineage.map(x=>freeze({
    from:x.from,to:x.to,change:x.change,basis:x.basis
   })))
  }));
 }
 return freeze(stack);
}
/** A paragraph's exact historical address can be walked through prior revisions. */
export function walkParagraphProjection(memory,id,address){
 check(memory);
 findRevision(memory,id);
 return traceCorpusLineage(memory,id,address);
}
export function verifyCorpusProjection(memory,projection){
 try{
  const output=unfoldCorpusProjection(memory,projection);
  const history=walkRevisionHistory(memory,output.revision);
  if(!history.length||history[0].revision!==projection.revision||
     history.at(-1).revision!=="r0000")throw new Error("History walk incomplete");
  if(!PROJECTION_LEVELS.every((x,i)=>projection.phases[i].level===x))
    throw new Error("Phase sequence mismatch");
  return freeze({pass:true,revision:output.revision,
   historicalVersions:history.length,
   paragraphs:output.metrics.paragraphs,glyphs:output.metrics.letters});
 }catch(e){return freeze({pass:false,error:e.message});}
}
