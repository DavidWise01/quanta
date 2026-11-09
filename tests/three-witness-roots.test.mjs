import test from "node:test";
import assert from "node:assert/strict";
import {instantiateThreeWitness,observeThreeWitnesses,reviewThreeWitnesses,verifyThreeWitnesses,inspectThreeWitnesses} from "../language/three-witness-roots.mjs";
const urls=["https://collection.sciencemuseumgroup.org.uk/people/cp38764/ada-lovelace","https://www.hsm.ox.ac.uk/imagining-ai","https://www.britannica.com/biography/Ada-Lovelace"];
const rootContext=()=>({
 society:{id:"ada-1843",letter:"A",subject:"Ada Lovelace",is:"Mathematical writer",was:"Mathematics student",whichMeans:"Her notes discussed the Engine's possibilities",wasYear:1833,
 context:{year:1843,timezone:"Europe/London",place:"London",group:"Computing scholarship"},
 weight:{authority:2,reach:2,legacy:4,confidence:.7,basis:"Illustrative assigned annotation"},evidence:[{label:"Museum",url:urls[0]}],status:"sourced"},
 target:"meaning",nodes:[
 {id:"meaning",statement:"Her notes discussed the Engine's possibilities",role:"conclusion",year:1843,status:"annotated",requires:["study"],evidence:[]},
 {id:"study",statement:"Studied mathematics",role:"prerequisite",year:1833,status:"unknown",requires:[],evidence:[]}
 ]});
const witnesses=(statuses=["supports","supports","challenges"])=>statuses.map((position,i)=>({
 id:["museum","oxford","britannica"][i],root:"study",position,statement:"Independent declared perspective "+i,year:1843,
 source:{label:"Source "+i,url:urls[i]},independence:"Distinct publisher asserted; not independently authenticated"
}));
test("three witness assignments have distinct ring slots and keep their sources",()=>{
 const ledger=observeThreeWitnesses(instantiateThreeWitness(rootContext()),"study",witnesses());
 assert.equal(verifyThreeWitnesses(ledger).pass,true);
 assert.equal(ledger.trios[0].witnesses.length,3);
 assert.equal(new Set(ledger.trios[0].slots.map(s=>s.ringStation)).size,3);
 assert.deepEqual(ledger.trios[0].slots.map(s=>s.quad),["a","b","c"]);
 assert.deepEqual(ledger.trios[0].affected,["meaning","study"]);
});
test("classification distinguishes unanimity, split, and incomplete",()=>{
 for(const [vote,expected] of [
 [["supports","supports","supports"],"unanimous-support"],
 [["challenges","challenges","challenges"],"unanimous-challenge"],
 [["supports","supports","challenges"],"split"],
 [["supports","undetermined","challenges"],"incomplete"]
 ]){
  const l=observeThreeWitnesses(instantiateThreeWitness(rootContext()),"study",witnesses(vote));
  assert.equal(l.trios[0].assessment.classification,expected);
  assert.equal(l.trios[0].assessment.interpretationProven,false);
 }
});
test("review records assessment but retains all three originals and the root",()=>{
 let l=observeThreeWitnesses(instantiateThreeWitness(rootContext()),"study",witnesses());
 const before=l;
 l=reviewThreeWitnesses(l,"t0000","insufficient","The cited records require closer inspection",{label:"Reviewer note",url:urls[1]});
 assert.equal(verifyThreeWitnesses(l).pass,true);
 assert.equal(l.trios[0].state,"reviewed");
 assert.equal(l.trios[0].witnesses.length,3);
 assert.equal(l.rootPacket.nodes[1].status,"unknown");
 assert.equal(before.trios[0].state,"open");
 assert.equal(l.events.length,2);
 assert.equal(inspectThreeWitnesses(l).interpretationProven,false);
});
test("duplicate identities, duplicate source hosts, wrong roots and wrong group size rejected",()=>{
 const initial=instantiateThreeWitness(rootContext());
 const duplicateIds=witnesses();duplicateIds[1].id=duplicateIds[0].id;
 const duplicateHosts=witnesses();duplicateHosts[1].source.url="https://collection.sciencemuseumgroup.org.uk/other";
 const wrongRoot=witnesses();wrongRoot[1].root="meaning";
 for(const set of [duplicateIds,duplicateHosts,wrongRoot,witnesses().slice(0,2)])
  assert.throws(()=>observeThreeWitnesses(initial,"study",set));
});
test("invalid witness years, evidence URLs, and role statements rejected",()=>{
 const initial=instantiateThreeWitness(rootContext());
 const future=witnesses();future[0].year=1844;
 const wrongDate=witnesses();wrongDate[0].year=1832;
 const insecure=witnesses();insecure[0].source.url="http://example.org";
 const badPosition=witnesses();badPosition[0].position="king";
 for(const set of [future,wrongDate,insecure,badPosition])
  assert.throws(()=>observeThreeWitnesses(initial,"study",set));
});
test("event replay rejects edited witness, review, parent or counts",()=>{
 let l=observeThreeWitnesses(instantiateThreeWitness(rootContext()),"study",witnesses());
 l=reviewThreeWitnesses(l,"t0000","support","Reviewer annotation",{label:"Review",url:urls[0]});
 for(const change of [
  x=>{x.trios[0].witnesses[0].statement="Silently changed"},
  x=>{x.events[1].parent="e9999"},
  x=>{x.events[1].review.rationale="Changed after review"},
  x=>{x.trios[0].assessment.counts.supports=3}
 ]){
  const x=JSON.parse(JSON.stringify(l));change(x);
  assert.equal(verifyThreeWitnesses(x).pass,false);
 }
});
test("multiple independent trios serialize, and review only once",()=>{
 let l=instantiateThreeWitness(rootContext());
 l=observeThreeWitnesses(l,"study",witnesses());
 const next=witnesses(["challenges","supports","undetermined"]).map((w,i)=>({...w,id:w.id+"-b"}));
 l=observeThreeWitnesses(l,"study",next);
 l=reviewThreeWitnesses(l,"t0001","insufficient","More study needed",{label:"Review",url:urls[1]});
 assert.equal(verifyThreeWitnesses(JSON.parse(JSON.stringify(l))).pass,true);
 assert.equal(inspectThreeWitnesses(l).open,1);
 assert.throws(()=>reviewThreeWitnesses(l,"t0001","support","Again",{label:"Review",url:urls[0]}));
});
