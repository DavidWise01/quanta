/**
 * QG-035.1: one symbolic [84211] enclosure, four inner 1311 chambers.
 * Computational model only: no physical quantum behavior claimed.
 * The judge can append a ruling but cannot rewrite sealed witness statements.
 */
export const VERSION="QG-035.1",CARRIER="||||",OUTER=Object.freeze([8,4,2,1,1]),INNER=Object.freeze([1,3,1,1]);
export const ACTORS=Object.freeze(["AaaA","BbbB","CccC","DddD"]);
export const FACES=Object.freeze(["+x","-x","+y","-y","+z","-z"]);
const deep=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function text(x){if(typeof x!=="string"||!x.trim()||x.length>900||/[\u0000-\u001f]/.test(x))throw Error("Invalid text");return x}
function initial(){return {version:VERSION,carrier:CARRIER,outer:[...OUTER],inner:[...INNER],actors:ACTORS.map(id=>({id,faces:[],closed:false,statement:null,source:null})),ruling:null,events:[]}}
function replay(events){
 if(!Array.isArray(events)||events.length>64)throw Error("Bounded event ledger required");
 const state=initial();
 for(let i=0;i<events.length;i++){
  const e=events[i];
  if(!e||e.index!==i||e.parent!==(i?"e"+String(i-1).padStart(4,"0"):null))throw Error("Broken append-only chain");
  if(e.kind==="face"){
   const a=state.actors.find(x=>x.id===e.actor);
   if(!a||a.closed||!FACES.includes(e.face)||a.faces.includes(e.face)||Object.keys(e).some(k=>!["index","parent","kind","actor","face"].includes(k)))throw Error("Invalid face");
   a.faces.push(e.face);
  }else if(e.kind==="seal"){
   const a=state.actors.find(x=>x.id===e.actor);
   if(!a||a.closed||a.faces.length!==6||a.faces.some(f=>!FACES.includes(f)))throw Error("All six faces must close");
   if(e.actor==="DddD"&&!state.actors.slice(0,3).every(x=>x.closed))throw Error("Judge requires three sealed players");
   if(Object.keys(e).some(k=>!["index","parent","kind","actor","statement","source"].includes(k)))throw Error("Unknown seal fields");
   if(e.actor!=="DddD"&&e.statement===undefined)throw Error("Missing witness statement");
   a.statement=text(e.statement);
   a.source=text(e.source);
   a.closed=true;
  }else if(e.kind==="ruling"){
   if(state.ruling||!state.actors.every(x=>x.closed))throw Error("Four closed chambers required");
   if(!["support","challenge","insufficient"].includes(e.outcome)||Object.keys(e).some(k=>!["index","parent","kind","outcome","rationale"].includes(k)))throw Error("Invalid ruling");
   state.ruling={outcome:e.outcome,rationale:text(e.rationale),interpretationProven:false};
  }else throw Error("Unknown event");
  state.events.push(deep(e));
 }
 return state;
}
export function instantiate84211(){return initial()}
export function append84211(state,event){
 verify84211Strict(state);
 if(state.events.length>=64)throw Error("Event bound");
 const i=state.events.length,next={...deep(event),index:i,parent:i?"e"+String(i-1).padStart(4,"0"):null};
 const s=replay([...state.events,next]);return s;
}
export function verify84211Strict(state){
 if(!state||state.version!==VERSION||state.carrier!==CARRIER||!eq(state.outer,OUTER)||!eq(state.inner,INNER))throw Error("Invalid quantum box header");
 const rebuilt=replay(state.events);if(!eq(rebuilt,state))throw Error("State disagrees with replay");
 return {pass:true,closed:state.actors.filter(x=>x.closed).length,judgeRuling:state.ruling!==null};
}
export function verify84211(state){try{return verify84211Strict(state)}catch(e){return {pass:false,error:e.message}}}
export function inspect84211(state){
 verify84211Strict(state);
 return {shape:"[84211]",fold:[...OUTER],chamber:"1311",chamberCount:4,faceCount:24,
 closed:state.actors.filter(a=>a.closed).map(a=>a.id),ruling:state.ruling,interpretationProven:false};
}
