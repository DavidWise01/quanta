/**
 * QG-034 · Canonical executable instantiation.
 * The fixture is SYNTHETIC and is not a claim about historical source independence.
 * Deterministic, observation-only, append-only, no external fetch or automatic edits.
 */
import {instantiateThreeWitness,observeThreeWitnesses,verifyThreeWitnesses} from "./three-witness-roots.mjs";
import {instantiateWitnessLineage,traceWitnessLineage,verifyWitnessLineage} from "./witness-lineage.mjs";
const urls=["https://a.example/one","https://b.example/two","https://c.example/three"];
const fixture={
 society:{id:"ada-1843",letter:"A",subject:"Ada Lovelace",is:"Mathematical writer",was:"Mathematics student",whichMeans:"Illustrative Engine commentary",wasYear:1833,
 context:{year:1843,timezone:"Europe/London",place:"London",group:"Computing scholarship"},
 weight:{authority:2,reach:2,legacy:4,confidence:.7,basis:"Illustrative metadata only"},
 evidence:[{label:"Synthetic source",url:urls[0]}],status:"sourced"},
 target:"meaning",nodes:[
 {id:"meaning",statement:"Illustrative Engine commentary",role:"conclusion",year:1843,status:"annotated",requires:["study"],evidence:[]},
 {id:"study",statement:"Studied mathematics",role:"prerequisite",year:1833,status:"unknown",requires:[],evidence:[]}
 ]};
const node=(id,kind,parents,url="https://archive.example/"+id)=>({id,kind,parents,label:id,url});
export function instantiateCanonicalKernel(){
 const upstream=observeThreeWitnesses(instantiateThreeWitness(fixture),"study",["a","b","c"].map((id,i)=>({
  id,root:"study",position:"supports",statement:"Synthetic declaration only",year:1843,
  source:{label:"Synthetic source "+id,url:urls[i]},independence:"Three distinct example domains; original ancestry not authenticated"
 })));
 const ancestry=[
  node("a","witness",["copy-a"],urls[0]),
  node("b","witness",["copy-b"],urls[1]),
  node("c","witness",["copy-c"],urls[2]),
  node("copy-a","record",["original"]),
  node("copy-b","record",["original"]),
  node("copy-c","record",["original"]),
  node("original","origin",[])
 ];
 const ledger=traceWitnessLineage(instantiateWitnessLineage(upstream),ancestry);
 const q33=verifyThreeWitnesses(upstream),q34=verifyWitnessLineage(ledger);
 if(!q33.pass||!q34.pass)throw new Error("Boot verification rejected");
 if(ledger.report.independentLineages!==1||ledger.report.threeIndependent)throw new Error("Shared-root guard failed");
 return {mode:"observation-only",persisted:false,fixture:true,sourceCommit:"1e3f749",q33,q34,ledger};
}
export function canonicalStatus(){
 const kernel=instantiateCanonicalKernel();
 return {kernel:"QG-034.1",carrier:"||||",status:"INSTANTIATED",q33Verified:kernel.q33.pass,
 q34Verified:kernel.q34.pass,witnesses:3,independentLineages:kernel.ledger.report.independentLineages,
 evidenceRoots:kernel.ledger.report.uniqueOrigins.length,interpretationProven:false,
 storage:"Explicit export / version control required",fixture:true};
}
if(typeof process!=="undefined"&&process.argv?.[1]&&import.meta.url===new URL("file://"+process.argv[1]).href){
 console.log(JSON.stringify(canonicalStatus(),null,2));
}
