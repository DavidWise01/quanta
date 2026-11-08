import test from "node:test";
import assert from "node:assert/strict";
import {alphabet,pathsFor} from "../language/alphabet-box.mjs";
import {phaseStation} from "../language/sexagesimal-ring.mjs";
import {homeStation,sourceFromHome,ringAddress,transportAlphabetRing,
 recoverAlphabetRing,transportAlphabetRingText,recoverAlphabetRingText,
 verifyAlphabetRing,ALPHABET_RING_PHASES} from "../language/alphabet-ring.mjs";

test("all 25 canonical grid vertices have distinct reversible home addresses",()=>{
 const stations=new Set();
 for(let y=0;y<5;y++)for(let x=0;x<5;x++){
  const home=homeStation({x,y});stations.add(home);
  assert.deepEqual(sourceFromHome(home),{x,y});
  assert.equal(home,(5*y+x)*2);
 }
 assert.equal(stations.size,25);
 assert.equal(Math.min(...stations),0);
 assert.equal(Math.max(...stations),48);
});
test("four quarter turns are exact +15 mod 60, restoring every home station",()=>{
 assert.deepEqual(ALPHABET_RING_PHASES,[0,90,180,270]);
 for(let y=0;y<5;y++)for(let x=0;x<5;x++){
  const p={x,y},home=homeStation(p);
  const stations=[0,1,2,3].map(q=>ringAddress(p,q).station);
  assert.deepEqual(stations,[0,1,2,3].map(q=>phaseStation(home,q)));
  assert.equal(new Set(stations).size,4);
  assert.equal(phaseStation(stations[3],1),home);
 }
});
test("A–Z strokes and semantic source roundtrip at all four phases",()=>{
 assert.equal(alphabet().length,26);
 for(const ch of alphabet())for(let q=0;q<4;q++){
  const p=transportAlphabetRing(ch,q,{meaning:"context only"});
  assert.equal(p.token,"||"+ch+"||");
  assert.equal(p.geometry.length,pathsFor(ch).length);
  assert.equal(p.phase.stationShift,q*15);
  assert.deepEqual(recoverAlphabetRing(p).source,pathsFor(ch));
  assert.equal(recoverAlphabetRing(JSON.parse(JSON.stringify(p))).letter,ch);
  for(const stroke of p.geometry)for(const v of stroke.vertices){
   assert.deepEqual(v.source,sourceFromHome(v.home));
   assert.equal(v.station,(v.home+q*15)%60);
  }
 }
});
test("Q tail remains a distinct stroke with located MOVE, DRAW, TURN verbs",()=>{
 for(let q=0;q<4;q++){
  const p=transportAlphabetRing("Q",q);
  assert.equal(p.geometry.length,2);
  assert.equal(p.somatic.filter(v=>v.verb==="MOVE").length,2);
  assert.ok(p.somatic.some(v=>v.verb==="TURN"));
  assert.ok(p.somatic.some(v=>v.verb==="DRAW"&&v.from&&v.to));
  const last=p.geometry[1].vertices.at(-1);
  assert.deepEqual(last.source,{x:4,y:4});
  assert.equal(last.station,phaseStation(48,q));
  for(const v of p.somatic){
   for(const end of [v.from,v.to,v.at])if(end){
    assert.equal(end.station,phaseStation(homeStation(end.source),q));
   }
  }
 }
});
test("word transport preserves exact letter order, spaces, and per-letter 90-degree phases",()=>{
 for(const input of ["","Q","Q T Z","QUANTA","ABCDEFGHIJKLMNOPQRSTUVWXYZ",
   "Q  Q"," QUANTA ","Q T Z  QUANTA"]){
  const p=transportAlphabetRingText(input);
  assert.equal(recoverAlphabetRingText(p),input);
  assert.equal(verifyAlphabetRing(p).pass,true);
 }
 const stream=transportAlphabetRingText("QUANTA BOX");
 assert.deepEqual(stream.items.filter(x=>x.type==="glyph").map(x=>x.packet.phase.quad),
  ["a","b","c","d","a","b","a","b","c"]);
});
test("tampering with source vertices, phase, semantic identity, or somatic verbs fails",()=>{
 const q=transportAlphabetRing("Q",2);
 const altered=JSON.parse(JSON.stringify(q));
 altered.geometry[1].vertices[1].station=42;
 assert.throws(()=>recoverAlphabetRing(altered),/mismatch/);
 const badPhase={...q,phase:{...q.phase,degrees:90}};
 assert.throws(()=>recoverAlphabetRing(badPhase),/mismatch/);
 const badVerb={...q,somatic:[]};
 assert.throws(()=>recoverAlphabetRing(badVerb),/mismatch/);
 const text=transportAlphabetRingText("Q T");
 assert.equal(verifyAlphabetRing({...text,items:[...text.items].reverse()}).pass,false);
});
test("invalid nonalphabet text, vertex coordinates and illegal phase rejected",()=>{
 for(const s of ["hello","A!","A\nB","A".repeat(129),"123"]){
  assert.throws(()=>transportAlphabetRingText(s),TypeError);
 }
 for(const p of [{x:5,y:0},{x:0,y:-1},{x:0.5,y:1}]){
  assert.throws(()=>homeStation(p),TypeError);
 }
 for(const n of [-1,1,49,60])assert.throws(()=>sourceFromHome(n),RangeError);
 assert.throws(()=>transportAlphabetRing("a",0),TypeError);
 assert.throws(()=>transportAlphabetRing("A",4),RangeError);
});
