import test from "node:test";
import assert from "node:assert/strict";
import {instantiateReconciliation,encounterRootConflict,decideRootConflict,inspectRootReconciliation,verifyRootReconciliation} from "../language/root-reconciliation.mjs";
const url="https://collection.sciencemuseumgroup.org.uk/people/cp38764/ada-lovelace";
function source(){
 const society={id:"ada-1843",letter:"A",subject:"Ada Lovelace",is:"Mathematical writer",
  was:"Student of mathematics",whichMeans:"Her notes explored the Analytical Engine's possibilities",
  wasYear:1833,context:{year:1843,timezone:"Europe/London",place:"London",group:"Computing scholarship"},
  weight:{authority:2,reach:2,legacy:4,confidence:.7,basis:"Illustrative annotation"},
  evidence:[{label:"Biography",url}],status:"sourced"};
 return {society,target:"meaning",nodes:[
  {id:"meaning",statement:society.whichMeans,role:"conclusion",year:1843,status:"annotated",requires:["notes"],evidence:[]},
  {id:"notes",statement:"Notes appeared in 1843",role:"prerequisite",year:1843,status:"annotated",requires:["study"],evidence:[]},
  {id:"study",statement:"Studied mathematics",role:"prerequisite",year:1833,status:"unknown",requires:[],evidence:[]}
 ]};
}
function observation(id,position,root="study"){
 return {id,root,position,statement:position==="supports"?"The record supports this premise":"The record challenges this premise",
  year:1843,evidence:[{label:"Document "+id,url}],question:"Which source supports this statement?"};
}
function pair(){
 return [observation("witness-a","supports"),observation("witness-b","challenges")];
}
test("two opposite cited observations stay distinct and open",()=>{
 const base=instantiateReconciliation(source());
 const ledger=encounterRootConflict(base,...pair());
 assert.equal(verifyRootReconciliation(ledger).pass,true);
 assert.equal(base.conflicts.length,0);
 assert.equal(ledger.conflicts[0].state,"open");
 assert.equal(ledger.conflicts[0].observations.length,2);
 assert.deepEqual(ledger.conflicts[0].affected,["meaning","notes","study"]);
 assert.equal(inspectRootReconciliation(ledger).interpretationProven,false);
});
test("explicit sourced decision adds event without erasing competing evidence",()=>{
 let ledger=encounterRootConflict(instantiateReconciliation(source()),...pair());
 ledger=decideRootConflict(ledger,"c0000","insufficient","Available sources do not settle the question",[{label:"Review",url}]);
 assert.equal(verifyRootReconciliation(ledger).pass,true);
 assert.equal(ledger.conflicts[0].state,"reviewed");
 assert.equal(ledger.conflicts[0].decision.choice,"insufficient");
 assert.equal(ledger.conflicts[0].observations.length,2);
 assert.equal(ledger.events.length,2);
 assert.equal(ledger.rootPacket.nodes[2].status,"unknown");
});
test("review choices support/challenge/insufficient remain non-proofs",()=>{
 for(const choice of ["support","challenge","insufficient"]){
  let l=encounterRootConflict(instantiateReconciliation(source()),...pair());
  l=decideRootConflict(l,"c0000",choice,"Human assessment",[{label:"Review",url}]);
  assert.equal(verifyRootReconciliation(l).interpretationProven,false);
 }
});
test("agreeing assertions, different roots, duplicate identity rejected",()=>{
 const l=instantiateReconciliation(source());
 assert.throws(()=>encounterRootConflict(l,observation("a","supports"),observation("b","supports")) );
 assert.throws(()=>encounterRootConflict(l,observation("a","supports"),observation("a","challenges")) );
 assert.throws(()=>encounterRootConflict(l,observation("a","supports"),observation("b","challenges","notes")));
});
test("missing links, future observation, invented root and empty review evidence rejected",()=>{
 const l=instantiateReconciliation(source());
 const a=observation("a","supports"),b=observation("b","challenges");
 for(const changed of [{...a,evidence:[]},{...a,year:1844},{...a,root:"none"}]){
  assert.throws(()=>encounterRootConflict(l,changed,b));
 }
 const open=encounterRootConflict(l,a,b);
 assert.throws(()=>decideRootConflict(open,"c0000","support","Reason",[]));
 assert.throws(()=>decideRootConflict(open,"missing","support","Reason",[{label:"Review",url}]));
});
test("changed observations, event chain and decisions fail full replay",()=>{
 let l=encounterRootConflict(instantiateReconciliation(source()),...pair());
 l=decideRootConflict(l,"c0000","support","Reviewed sources",[{label:"Review",url}]);
 const c=JSON.parse(JSON.stringify(l));c.conflicts[0].observations[1].statement="Edited silently";
 assert.equal(verifyRootReconciliation(c).pass,false);
 const d=JSON.parse(JSON.stringify(l));d.events[1].previous="e9999";
 assert.equal(verifyRootReconciliation(d).pass,false);
 const e=JSON.parse(JSON.stringify(l));e.events[1].decision.rationale="Modified";
 assert.equal(verifyRootReconciliation(e).pass,false);
});
test("serialized multi-conflict history replays and retains original root source",()=>{
 let l=instantiateReconciliation(source());
 l=encounterRootConflict(l,...pair());
 l=encounterRootConflict(l,observation("c","challenges"),observation("d","supports"));
 const before=l;
 l=decideRootConflict(l,"c0001","challenge","Comparison",[{label:"Review",url}]);
 const copy=JSON.parse(JSON.stringify(l));
 assert.equal(verifyRootReconciliation(copy).pass,true);
 assert.equal(copy.conflicts.length,2);
 assert.equal(inspectRootReconciliation(copy).open,1);
 assert.equal(before.conflicts[1].state,"open");
});
