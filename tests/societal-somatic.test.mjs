import test from "node:test";
import assert from "node:assert/strict";
import {bindSocialContext,recoverSocialContext,compareSocialContext,verifySocialContext}
 from "../language/societal-somatic.mjs";
const ada=()=>({
 id:"ada-1843",letter:"A",subject:"Ada Lovelace",
 is:"British mathematical writer publishing notes on the Analytical Engine",
 was:"A student of mathematics and collaborator with Charles Babbage",
 whichMeans:"Her 1843 notes discussed the planned machine as a general-purpose symbolic processor",
 wasYear:1833,context:{year:1843,timezone:"Europe/London",place:"London",group:"Early computing scholarship"},
 weight:{authority:2,reach:2,legacy:4,confidence:.7,
  basis:"Illustrative human annotation about scholarly reach; not an objective rating of a person"},
 evidence:[{label:"Science Museum Group Ada Lovelace",url:"https://collection.sciencemuseumgroup.org.uk/people/cp38764/ada-lovelace"}],
 status:"sourced"
});
test("IS WAS WHICH MEANS anchors use 3 different 60-ring stations",()=>{
 const p=bindSocialContext(ada());
 assert.deepEqual(p.anchors.map(x=>x.role),["is","was","whichMeans"]);
 assert.equal(new Set(p.anchors.map(x=>x.station)).size,3);
 assert.deepEqual(p.anchors.map(x=>x.phase),[0,1,2]);
 assert.equal(p.anchors[1].somatic.some(v=>v.verb==="DRAW"),true);
 assert.deepEqual(recoverSocialContext(p),ada());
});
test("sourced example has year, IANA timezone, location and citation witness",()=>{
 const p=bindSocialContext(ada());
 assert.equal(p.claim.context.timezone,"Europe/London");
 assert.equal(p.claim.context.year,1843);
 assert.equal(p.claim.evidence.length,1);
 assert.equal(verifySocialContext(p).pass,true);
});
test("fictional king privileges remain explicitly annotated, not universal facts",()=>{
 const c=ada();
 c.id="fictional-king";c.letter="K";c.subject="Fictional king";
 c.is="Ruler of an imaginary kingdom";c.was="Heir to an invented throne";
 c.whichMeans="A fictional court may grant privileges; laws depend on the fictional polity";
 c.context={year:1500,timezone:"Europe/London",place:"Imaginary court",group:"Imaginary nobility"};
 c.wasYear=1490;c.status="fictional";c.evidence=[];
 assert.equal(verifySocialContext(bindSocialContext(c)).pass,true);
});
test("same-subject weight deltas only when same place and group",()=>{
 const first=bindSocialContext(ada()),secondData=ada();
 secondData.id="ada-1844";secondData.context={...secondData.context,year:1844};
 secondData.weight={...secondData.weight,legacy:5};
 const d=compareSocialContext(first,bindSocialContext(secondData));
 assert.equal(d.contextComparable,true);
 assert.equal(d.delta.legacy,1);
 const moved=ada();moved.id="ada-elsewhere";moved.context={...moved.context,place:"Other location"};
 const difference=compareSocialContext(first,bindSocialContext(moved));
 assert.equal(difference.contextComparable,false);
 assert.equal(difference.delta,null);
});
test("change in chronology, time zone or citation invalidates the canonical packet",()=>{
 const p=bindSocialContext(ada());
 const bad=JSON.parse(JSON.stringify(p));bad.claim.wasYear=1844;
 assert.equal(verifySocialContext(bad).pass,false);
 const zone=JSON.parse(JSON.stringify(p));zone.claim.context.timezone="America/Chicago";
 assert.equal(verifySocialContext(zone).pass,false);
 const station=JSON.parse(JSON.stringify(p));station.anchors[1].station=59;
 assert.equal(verifySocialContext(station).pass,false);
});
test("invalid dates, time zones, status and unsupported source metadata rejected",()=>{
 for(const mutate of [
  c=>{c.wasYear=1845},c=>{c.context.timezone="Not/AZone"},
  c=>{c.weight.authority=6},c=>{c.status="sourced";c.evidence=[]},
  c=>{c.evidence[0].url="http://example.org"},
  c=>{c.letter="a"}
 ]){
  const c=ada();mutate(c);assert.throws(()=>bindSocialContext(c));
 }
});
test("JSON serialization and recovery preserve exactly every recorded field",()=>{
 const p=bindSocialContext(ada());
 assert.deepEqual(recoverSocialContext(JSON.parse(JSON.stringify(p))),ada());
 assert.ok(Object.isFrozen(p.claim));
 assert.ok(Object.isFrozen(p.anchors));
});
