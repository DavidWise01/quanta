import test from "node:test";
import assert from "node:assert/strict";
import {BASE,PER_QUAD,DIVISORS,stationRing,phaseStation,locateStation,toSexagesimal,fromSexagesimal,
 displaySexagesimal,parseSexagesimal,makeTransport,recoverTransport,verifyTransport} from "../language/sexagesimal-ring.mjs";

test("60 stations are exactly partitioned into four quads of 15",()=>{
 const ring=stationRing();
 assert.equal(ring.length,60);assert.equal(new Set(ring.map(p=>p.station)).size,60);
 for(let q=0;q<4;q++)assert.equal(ring.filter(p=>p.quad==="abcd"[q]).length,15);
 assert.deepEqual(ring.map(x=>x.angle).filter((_,i)=>i%15===0),[0,90,180,270]);
 assert.equal(BASE,60);assert.equal(PER_QUAD,15);
});
test("every phase quarter-turn returns after four rotations",()=>{
 for(let n=0;n<60;n++){
  const orbit=[n,phaseStation(n,1),phaseStation(n,2),phaseStation(n,3)];
  assert.equal(new Set(orbit).size,4);
  assert.equal(phaseStation(n,4),n);
  assert.equal(phaseStation(phaseStation(n,1),-1),n);
  assert.equal(locateStation(n).local,n%15);
 }
});
test("the divisors of 60 are exact and include 1 through 5",()=>{
 assert.deepEqual(DIVISORS,[1,2,3,4,5,6,10,12,15,20,30,60]);
 assert.ok([1,2,3,4,5].every(d=>60%d===0));
 assert.equal(DIVISORS.length,12);
});
test("sexagesimal boundary values and canonical placeholder positions",()=>{
 const cases=[["0",[0]],["1",[1]],["59",[59]],["60",[1,0]],["61",[1,1]],["3599",[59,59]],["3600",[1,0,0]],["3835",[1,3,55]],["216000",[1,0,0,0]]];
 for(const [value,digits] of cases){
  assert.deepEqual(toSexagesimal(value),digits);
  assert.equal(fromSexagesimal(digits).toString(),value);
  assert.equal(recoverTransport(makeTransport(value)).toString(),value);
 }
 assert.equal(displaySexagesimal([1,3,55]),"01:03:55");
 assert.deepEqual(parseSexagesimal("01:03:55"),[1,3,55]);
});
test("BigInt conversion is exact beyond JavaScript safe-number limit",()=>{
 const value=(60n**35n+59n*60n**2n+1n).toString();
 const digits=toSexagesimal(value);
 assert.equal(digits.length,36);
 assert.equal(fromSexagesimal(digits).toString(),value);
 const packet=makeTransport(value);
 assert.equal(verifyTransport(packet).pass,true);
 assert.equal(recoverTransport(JSON.parse(JSON.stringify(packet))).toString(),value);
});
test("tamper detection for phase, numeric source, station and carrier",()=>{
 const p=makeTransport("3835");
 const corrupt={...p,positions:[{...p.positions[0],phases:[...p.positions[0].phases].reverse()},...p.positions.slice(1)]};
 assert.equal(verifyTransport(corrupt).pass,false);
 assert.equal(verifyTransport({...p,decimal:"3836"}).pass,false);
 assert.equal(verifyTransport({...p,carrier:"||"}).pass,false);
 assert.equal(verifyTransport({...p,digits:[1,3,54]}).pass,false);
});
test("input bounds reject malformed sexagesimal values",()=>{
 for(const s of ["-1","1.5","4e3","abc",""]){assert.throws(()=>toSexagesimal(s),TypeError);}
 for(const s of ["60","01:60","-1","01::02","1:","00:01"]){assert.throws(()=>parseSexagesimal(s));}
 assert.throws(()=>fromSexagesimal([1,60]),TypeError);
 assert.throws(()=>fromSexagesimal([0,1]),TypeError);
 assert.throws(()=>phaseStation(60),RangeError);
});
