import test from "node:test";
import assert from "node:assert/strict";
import {composeRootChase} from "../language/chasing-roots.mjs";
import {
 instantiateRootPropagation,propagateRoots,recoverRootRevision,
 inspectRootImpact,verifyRootPropagation
} from "../language/root-propagation.mjs";
const url="https://collection.sciencemuseumgroup.org.uk/people/cp38764/ada-lovelace";
function fixture(){
 const society={id:"ada-1843",letter:"A",subject:"Ada Lovelace",
  is:"Mathematical writer",was:"Studied mathematics and collaborated with Babbage",
  whichMeans:"Her notes explored the Analytical Engine's wider possibilities",
  wasYear:1833,context:{year:1843,timezone:"Europe/London",place:"London",group:"Computing scholarship"},
  weight:{authority:2,reach:2,legacy:4,confidence:.7,basis:"Illustrative human annotation"},
  evidence:[{label:"Museum",url}],status:"sourced"};
 return {society,target:"meaning",nodes:[
  {id:"meaning",statement:society.whichMeans,role:"conclusion",year:1843,status:"annotated",requires:["notes","engine"],evidence:[]},
  {id:"notes",statement:"Notes were published in 1843",role:"prerequisite",year:1843,status:"sourced",requires:["study"],evidence:[{label:"Museum",url}]},
  {id:"engine",statement:"An Analytical Engine was proposed",role:"prerequisite",year:1837,status:"sourced",requires:[],evidence:[{label:"Museum",url}]},
  {id:"study",statement:"She studied mathematics",role:"prerequisite",year:1833,status:"unknown",requires:[],evidence:[]}
 ]};
}
function update(id="study"){
 return {id,status:"sourced",evidence:[{label:"Museum biography",url}]};
}
test("new cited root evidence propagates through all reverse dependents",()=>{
 const initial=instantiateRootPropagation(fixture());
 const ledger=propagateRoots(initial,[update()]);
 assert.equal(verifyRootPropagation(ledger).pass,true);
 assert.deepEqual(ledger.revisions[1].changedRoots,["study"]);
 assert.deepEqual(ledger.revisions[1].affected,["meaning","notes","study"]);
 assert.equal(inspectRootImpact(ledger,"p0001").interpretationNeedsReview,true);
 assert.equal(ledger.revisions[1].snapshot.trace.gaps.length,0);
 assert.equal(initial.revisions.length,1);
 assert.equal(recoverRootRevision(initial,"p0000").nodes.at(-1).status,"unknown");
 assert.equal(recoverRootRevision(ledger,"p0001").nodes.at(-1).status,"sourced");
});
test("two independent root updates share dependent nodes without duplicate propagation",()=>{
 const ledger=propagateRoots(instantiateRootPropagation(fixture()),[
  update("study"),
  {id:"engine",status:"unknown",evidence:[]}
 ]);
 assert.deepEqual(ledger.revisions[1].changedRoots,["study","engine"]);
 assert.deepEqual(ledger.revisions[1].affected,["meaning","notes","engine","study"]);
 assert.equal(new Set(ledger.revisions[1].affected).size,4);
});
test("an unchanged update is refused and ancestors remain unmodified",()=>{
 const initial=instantiateRootPropagation(fixture());
 assert.throws(()=>propagateRoots(initial,[{id:"study",status:"unknown",evidence:[]}]),/no change/);
 const revised=propagateRoots(initial,[update()]);
 assert.equal(recoverRootRevision(revised,"p0000").nodes.at(-1).status,"unknown");
 assert.ok(Object.isFrozen(revised.revisions));
});
test("internal nodes and invented root addresses cannot be changed through root-only interface",()=>{
 const initial=instantiateRootPropagation(fixture());
 assert.throws(()=>propagateRoots(initial,[update("notes")]),/leaf root/);
 assert.throws(()=>propagateRoots(initial,[update("missing")]),/leaf root/);
 assert.throws(()=>propagateRoots(initial,[update(),update()]),/Duplicate root update/);
});
test("source claim wording and interpretations never silently change on propagation",()=>{
 const initial=instantiateRootPropagation(fixture()),ledger=propagateRoots(initial,[update()]);
 const before=recoverRootRevision(ledger,"p0000"),after=recoverRootRevision(ledger,"p0001");
 assert.equal(before.claim.whichMeans,after.claim.whichMeans);
 assert.equal(before.nodes[0].statement,after.nodes[0].statement);
 assert.equal(after.nodes[0].status,"annotated");
 assert.equal(inspectRootImpact(ledger,"p0001").claimStatusUnchanged,true);
});
test("tampering with history, propagation impact, or evidence fails replay",()=>{
 const ledger=propagateRoots(instantiateRootPropagation(fixture()),[update()]);
 const variants=[
  {...ledger,revisions:[ledger.revisions[0],{...ledger.revisions[1],parent:"p9999"}]},
  {...ledger,revisions:[ledger.revisions[0],{...ledger.revisions[1],affected:[]}]},
  {...ledger,revisions:[ledger.revisions[0],{...ledger.revisions[1],changedRoots:["engine"]}]},
 ];
 for(const c of variants)assert.equal(verifyRootPropagation(c).pass,false);
 const clone=JSON.parse(JSON.stringify(ledger));
 clone.revisions[1].snapshot.nodes.at(-1).evidence[0].url="https://changed.example";
 assert.equal(verifyRootPropagation(clone).pass,false);
});
test("JSON roundtrip and multiple generations exactly reproduce history",()=>{
 let ledger=instantiateRootPropagation(composeRootChase(fixture()));
 ledger=propagateRoots(ledger,[update()],"Evidence arrived");
 ledger=propagateRoots(ledger,[{id:"engine",status:"disputed",evidence:[]}],"Reassess engine root");
 const restored=JSON.parse(JSON.stringify(ledger));
 assert.equal(verifyRootPropagation(restored).pass,true);
 assert.equal(restored.revisions.length,3);
 assert.equal(recoverRootRevision(restored,"p0000").trace.gaps.length,1);
 assert.equal(recoverRootRevision(restored,"p0001").trace.gaps.length,0);
 assert.equal(recoverRootRevision(restored,"p0002").trace.gaps.length,1);
});
