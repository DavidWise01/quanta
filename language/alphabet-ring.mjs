/**
 * QUANTA QG-026.1 — Alphabet / 60-Ring Phase-Semantic-Somatic Transport
 *
 * QG-016 5×5 glyph vertices are mapped injectively to 25 home stations:
 * home = 2 * (5*y + x), so home is one of 0,2,...,48.
 * In quadrant q (a/b/c/d), active station = (home + 15*q) mod 60.
 *
 * Each somatic verb gets ring addresses for its source/destination/turn.
 * Explicit canonical letter and source paths remain in the packet witness.
 * The ring view is a transport phase, not a rigid spatial rotation of a glyph.
 *
 * This is a QUANTA design, not Babylonian/Vedic writing or a physics claim.
 */
import {alphabet, pathsFor, transportLetter, tokenFor} from "./alphabet-box.mjs";
import {BASE, PER_QUAD, QUAD_NAMES, phaseStation, locateStation} from "./sexagesimal-ring.mjs";

export const ALPHABET_RING_VERSION="QG-026.1";
export const ALPHABET_RING_CARRIER="||||";
export const ALPHABET_RING_MAX_TEXT=128;
export const ALPHABET_RING_PHASES=Object.freeze([0,90,180,270]);
const freeze=Object.freeze;
const has=Object.hasOwn;
function letterOf(v){
 if(typeof v!=="string"||v.length!==1||!alphabet().includes(v))
  throw new TypeError("Expected one uppercase A-Z glyph.");
 return v;
}
function phaseOf(q){
 if(!Number.isInteger(q)||q<0||q>3)throw new RangeError("Quad index must be 0..3.");
 return q;
}
function meaningOf(v){
 if(v!==null&&(typeof v!=="string"||v.length>256))
  throw new TypeError("Optional meaning must be null or a string <=256 characters.");
 return v;
}
export function homeStation(point){
 if(!point||!Number.isInteger(point.x)||!Number.isInteger(point.y)||
  point.x<0||point.x>4||point.y<0||point.y>4)
  throw new TypeError("Expected a vertex on the 5x5 canonical glyph grid.");
 return 2*(5*point.y+point.x);
}
export function sourceFromHome(station){
 if(!Number.isInteger(station)||station<0||station>48||station%2!==0)
  throw new RangeError("Home station must be one of the 25 even stations from 0 to 48.");
 const index=station/2;return freeze({x:index%5,y:Math.floor(index/5)});
}
export function ringAddress(point,quad=0){
 const q=phaseOf(quad);
 const home=homeStation(point),station=phaseStation(home,q);
 return freeze({source:freeze({x:point.x,y:point.y}),home,station,
  quad:QUAD_NAMES[q],quarterTurns:q,degrees:q*90,
  location:locateStation(station)});
}
function ringVerb(verb,quad){
 const v={verb:verb.verb,stroke:verb.stroke};
 if(verb.from)v.from=ringAddress(verb.from,quad);
 if(verb.to)v.to=ringAddress(verb.to,quad);
 if(verb.at)v.at=ringAddress(verb.at,quad);
 if(verb.verb==="DRAW"){v.dx=verb.dx;v.dy=verb.dy;}
 if(verb.verb==="TURN")v.orientation=verb.orientation;
 return freeze(v);
}
export function transportAlphabetRing(letter,quad=0,options={}){
 const ch=letterOf(letter),q=phaseOf(quad),meaning=meaningOf(options.meaning??null);
 const source=pathsFor(ch),base=transportLetter(ch);
 const strokes=freeze(source.map((path,i)=>freeze({
  stroke:i,
  vertices:freeze(path.map(p=>ringAddress(p,q)))
 })));
 const somatic=freeze(base.quads[0].somatic.map(v=>ringVerb(v,q)));
 return freeze({
  version:ALPHABET_RING_VERSION,carrier:ALPHABET_RING_CARRIER,
  token:tokenFor(ch),semantic:freeze({letter:ch,meaning}),
  phase:freeze({quad:QUAD_NAMES[q],index:q,degrees:q*90,stationShift:q*PER_QUAD}),
  geometry:strokes,somatic
 });
}
export function recoverAlphabetRing(packet){
 if(!packet||packet.version!==ALPHABET_RING_VERSION||
  packet.carrier!==ALPHABET_RING_CARRIER||
  typeof packet.token!=="string"||!/^\|\|[A-Z]\|\|$/.test(packet.token)||
  !packet.semantic||!packet.phase)
  throw new TypeError("Invalid alphabet ring packet.");
 const ch=letterOf(packet.token[2]);
 const expected=transportAlphabetRing(ch,packet.phase.index,{meaning:packet.semantic.meaning});
 if(JSON.stringify(expected)!==JSON.stringify(packet))
  throw new Error("Phase, letter source, stroke or somatic witness mismatch.");
 return freeze({letter:ch,meaning:packet.semantic.meaning,source:pathsFor(ch)});
}
function checkText(input){
 if(typeof input!=="string"||input.length>ALPHABET_RING_MAX_TEXT||!/^[A-Z ]*$/.test(input))
  throw new TypeError("Transport supports 0..128 uppercase A-Z letters and spaces.");
}
export function transportAlphabetRingText(input,options={}){
 checkText(input);
 const meaning=meaningOf(options.meaning??null);
 let phase=0;const items=[];
 for(let i=0;i<input.length;i++){
  const ch=input[i];
  if(ch===" "){
   items.push(freeze({type:"space",index:i,char:" ",resetTo:0}));
   phase=0;
  }else{
   items.push(freeze({type:"glyph",index:i,char:ch,
    packet:transportAlphabetRing(ch,phase,{meaning})}));
   phase=(phase+1)%4;
  }
 }
 return freeze({version:ALPHABET_RING_VERSION,carrier:ALPHABET_RING_CARRIER,
  source:input,meaning,items:freeze(items),terminalPhase:phase});
}
export function recoverAlphabetRingText(stream){
 if(!stream||stream.version!==ALPHABET_RING_VERSION||
  stream.carrier!==ALPHABET_RING_CARRIER||typeof stream.source!=="string"||
  !Array.isArray(stream.items))
  throw new TypeError("Invalid alphabet ring stream.");
 checkText(stream.source);
 const expected=transportAlphabetRingText(stream.source,{meaning:stream.meaning});
 if(JSON.stringify(expected)!==JSON.stringify(stream))
  throw new Error("Alphabet ring text phase, spacing, or vertex witness mismatch.");
 return stream.source;
}
export function verifyAlphabetRing(stream){
 try{
  const source=recoverAlphabetRingText(stream);
  const glyphs=stream.items.filter(x=>x.type==="glyph");
  for(const item of glyphs)recoverAlphabetRing(item.packet);
  return freeze({pass:true,source,characters:source.length,glyphs:glyphs.length,
   spaces:source.length-glyphs.length,stations:BASE,quads:4,
   verbs:glyphs.reduce((n,item)=>n+item.packet.somatic.length,0)});
 }catch(error){return freeze({pass:false,error:error.message});}
}
