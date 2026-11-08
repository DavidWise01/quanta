/**
 * QUANTA QG-029.1 — Temporal Societal Somatic Semantics
 *
 * One subject: IS (contextual identity), WAS (prior role/event), WHICH MEANS
 * (explicit interpretation) with exact place, year, group, IANA timezone,
 * cited evidence, and human-assigned ordinal social weight.
 *
 * Three roles bind to separate 60-ring phases via QG-028.
 * Temporal and social significance are NOT determined by an IANA offset,
 * a gender, a title, a glyph, or an inherent "importance" scale.
 */
import {bindSemanticLetter,recoverSemanticLetter} from "./semantic-ring.mjs";
export const VERSION="QG-029.1",CARRIER="||||";
export const ROLES=Object.freeze(["is","was","whichMeans"]);
export const DIMENSIONS=Object.freeze(["authority","reach","legacy"]);
const freeze=Object.freeze;
const own=Object.hasOwn;
function obj(x,name){if(!x||typeof x!=="object"||Array.isArray(x))throw new TypeError(name+" must be an object");return x;}
function keys(o,allowed,name){obj(o,name);if(Object.keys(o).some(k=>!allowed.includes(k)))throw new TypeError(name+" has unknown keys");}
function str(s,name,max=300){if(typeof s!=="string"||!s.trim()||s.length>max||/[\u0000-\u001f]/.test(s))throw new TypeError(name+" needs nonempty text up to "+max);return s;}
function yr(n,name){if(!Number.isInteger(n)||n<1||n>9999)throw new TypeError(name+" must be year 1..9999 CE");return n;}
function zoned(name){
 str(name,"IANA timezone",100);
 try{new Intl.DateTimeFormat("en-US",{timeZone:name}).format(new Date("2020-01-01T00:00:00Z"))}
 catch{throw new TypeError("Unrecognized IANA timezone")}
 return name;
}
function weight(w){
 keys(w,["authority","reach","legacy","confidence","basis"],"weight");
 const result={};
 for(const key of DIMENSIONS){
  if(!Number.isInteger(w[key])||w[key]<0||w[key]>5)throw new TypeError(key+" must be caller-assigned ordinal 0..5");
  result[key]=w[key];
 }
 if(typeof w.confidence!=="number"||!Number.isFinite(w.confidence)||w.confidence<0||w.confidence>1)
  throw new TypeError("Confidence must be 0..1");
 result.confidence=w.confidence;result.basis=str(w.basis,"weight basis",400);
 return freeze(result);
}
function evidenceList(list){
 if(!Array.isArray(list)||list.length>12)throw new TypeError("At most 12 evidence entries");
 return freeze(list.map(item=>{
  keys(item,["label","url"],"evidence");
  const label=str(item.label,"Evidence label",180);
  const url=str(item.url,"Evidence URL",1000);
  if(!/^https:\/\/[^\s]+$/i.test(url))throw new TypeError("Evidence must use an HTTPS URL");
  return freeze({label,url});
 }));
}
function context(c){
 keys(c,["year","timezone","place","group"],"context");
 return freeze({year:yr(c.year,"year"),timezone:zoned(c.timezone),
  place:str(c.place,"place",160),group:str(c.group,"group",160)});
}
function claim(input){
 keys(input,["id","letter","subject","is","was","whichMeans","context","wasYear","weight","evidence","status"],"claim");
 const id=str(input.id,"id",80);
 if(!/^[a-z][a-z0-9-]*$/.test(id))throw new TypeError("ID must be lowercase slug");
 const letter=str(input.letter,"letter",1);
 if(!/^[A-Z]$/.test(letter))throw new TypeError("letter must be uppercase A–Z");
 const ctx=context(input.context),wasYear=yr(input.wasYear,"wasYear");
 if(wasYear>ctx.year)throw new RangeError("WAS year cannot occur after contextual IS year");
 const status=input.status??"annotated";
 if(!["sourced","annotated","hypothesis","fictional"].includes(status))throw new TypeError("Unknown epistemic status");
 const evidence=evidenceList(input.evidence??[]);
 if(status==="sourced"&&!evidence.length)throw new TypeError("Sourced claims require evidence");
 return freeze({id,letter,subject:str(input.subject,"subject",180),
  is:str(input.is,"is",600),was:str(input.was,"was",600),
  whichMeans:str(input.whichMeans,"whichMeans",1000),
  context:ctx,wasYear,weight:weight(input.weight),evidence,status});
}
function record(input){
 const c=claim(input),bound=bindSemanticLetter(c.letter,0);
 const anchors=freeze(castRoles(c,bound));
 return freeze({version:VERSION,carrier:CARRIER,claim:c,anchors,
   witness:freeze({contextKey:[c.context.year,c.context.timezone,c.context.place,c.context.group].join("|"),
    metric:"human-assigned contextual ordinal; not inherent societal worth"})});
}
function castRoles(c,bound){
 return ROLES.map((role,i)=>freeze({
  role,text:c[role],station:bound.roles[i].station,phase:bound.roles[i].phase,
  phaseName:bound.roles[i].glyph.phase.quad,
  glyph:bound.roles[i].glyph,
  somatic:i===1?bound.roles[i].verbs:freeze([])
 }));
}
export function bindSocialContext(input){return record(input);}
export function recoverSocialContext(packet){
 if(!packet||packet.version!==VERSION||packet.carrier!==CARRIER)throw new TypeError("Unknown social context packet");
 const expected=record(packet.claim);
 if(JSON.stringify(expected)!==JSON.stringify(packet))throw new Error("Social context, chronology, station or role witness mismatch");
 for(const a of packet.anchors)recoverSemanticLetter({
  version:"QG-028.1",carrier:CARRIER,letter:packet.claim.letter,token:"||"+packet.claim.letter+"||",
  entryPhase:0,roles:packet.anchors.map((role,i)=>({
   role:["see","do","learn"][i],term:bindSemanticLetter(packet.claim.letter,0).roles[i].term,
   offset:i,phase:role.phase,degrees:role.phase*90,station:role.station,
   anchorHome:role.glyph.geometry[0].vertices[0].home,
   location:role.glyph.geometry[0].vertices[0].location,
   glyph:role.glyph,verbs:role.somatic
  })),exitPhase:3
 });
 return packet.claim;
}
export function compareSocialContext(a,b){
 const ca=recoverSocialContext(a),cb=recoverSocialContext(b);
 if(ca.subject!==cb.subject)throw new Error("Contexts must describe the same subject");
 const deltas=freeze(Object.fromEntries(DIMENSIONS.map(k=>[k,cb.weight[k]-ca.weight[k]])));
 const matched=ca.context.group===cb.context.group&&ca.context.place===cb.context.place;
 return freeze({subject:ca.subject,from:ca.context,to:cb.context,contextComparable:matched,
  delta:matched?deltas:null,
  note:matched?"Human-provided ordinal difference in matching group and place":"Different group/place: no numerical comparison inferred",
  isFrom:ca.is,isTo:cb.is,meansFrom:ca.whichMeans,meansTo:cb.whichMeans});
}
export function verifySocialContext(packet){
 try{const c=recoverSocialContext(packet);return freeze({pass:true,subject:c.subject,
  phaseStations:packet.anchors.map(x=>x.station),year:c.context.year,
  status:c.status,evidence:c.evidence.length});}
 catch(e){return freeze({pass:false,error:e.message});}
}
