/**
 * QG-041.1 — Experienced observer: a utility preference learned from samples,
 * not a predetermined play-count switch, a subjective-consciousness claim,
 * or an enumerated 24! search.
 */
export const VERSION="QG-041.1";
export const SPACE_24_FACTORIAL="620448401733239439360000";
const copy=v=>JSON.parse(JSON.stringify(v));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const validId=s=>typeof s==="string"&&/^[a-z][a-z0-9-]{0,31}$/.test(s);
const oneOf=(v,a)=>a.includes(v);
const finite=n=>typeof n==="number"&&Number.isFinite(n)&&n>=0&&n<=10;
const allowed=["index","parent","mode","game","games","patterns","payoff","cost"];
const average=a=>a.reduce((x,y)=>x+y,0)/a.length;
export function instantiateObserver({declaredPriorGames="0"}={}){
 if(typeof declaredPriorGames!=="string"||!/^(0|[1-9][0-9]*)$/.test(declaredPriorGames)||BigInt(declaredPriorGames)>BigInt(SPACE_24_FACTORIAL))throw Error("Invalid declared prior experience");
 return {version:VERSION,space:SPACE_24_FACTORIAL,declaredPriorGames,provenPriorGames:false,
    events:[],choice:"undetermined",scores:{play:null,observe:null},sampled:{play:0,observe:0},history:[]};
}
function score(event,seen){
 const games=event.mode==="play"?[event.game]:event.games;
 const newPatterns=event.patterns.filter(x=>!seen.has(x)).length;
 const variety=new Set(games).size;
 // Explicit utility proxy: information novelty + breadth + payoff - attention cost.
 // These are modelling assumptions, not measured subjective fun.
 return {utility:2*newPatterns+0.75*variety+event.payoff-event.cost,
   novelPatterns:newPatterns,distinctGames:variety};
}
function replay(declaredPriorGames,events){
 const s=instantiateObserver({declaredPriorGames}),seen=new Set(),samples={play:[],observe:[]};
 for(let i=0;i<events.length;i++){
  const e=events[i];
  if(!e||Object.keys(e).some(k=>!allowed.includes(k))||e.index!==i||e.parent!==(i?"e"+String(i-1).padStart(4,"0"):null)||
   !oneOf(e.mode,["play","observe"])||!Array.isArray(e.patterns)||e.patterns.length<1||e.patterns.length>12||
   new Set(e.patterns).size!==e.patterns.length||e.patterns.some(x=>!validId(x))||!finite(e.payoff)||!finite(e.cost))throw Error("Invalid observation event");
  if(e.mode==="play"){
   if(!validId(e.game)||e.games!==undefined)throw Error("Invalid game play");
  }else{
   if(e.game!==undefined||!Array.isArray(e.games)||e.games.length<2||e.games.length>6||
    e.games.some(x=>!validId(x))||new Set(e.games).size!==e.games.length)throw Error("Observer must compare distinct games");
  }
  const evaluation=score(e,seen);
  e.patterns.forEach(x=>seen.add(x));
  samples[e.mode].push(evaluation.utility);
  const recentPlay=samples.play.slice(-6),recentObserve=samples.observe.slice(-3);
  const playScore=recentPlay.length?average(recentPlay):null;
  const observeScore=recentObserve.length?average(recentObserve):null;
  // No automatic transition for age/count: require exposure to both strategies.
  const ready=samples.play.length>=6&&samples.observe.length>=3;
  let choice="undetermined";
  if(ready)choice=observeScore>playScore+0.25?"observe":playScore>observeScore+0.25?"play":"indifferent";
  s.history.push({event:i,mode:e.mode,utility:evaluation.utility,
    novelPatterns:evaluation.novelPatterns,distinctGames:evaluation.distinctGames,
    choice,playScore,observeScore});
  s.events.push(copy(e));s.choice=choice;s.scores={play:playScore,observe:observeScore};
  s.sampled={play:samples.play.length,observe:samples.observe.length};
 }
 return s;
}
export function verifyObserverStrict(state){
 if(!state||state.version!==VERSION||state.space!==SPACE_24_FACTORIAL||
 !Array.isArray(state.events)||state.events.length>128)throw Error("Invalid observer header");
 const rebuilt=replay(state.declaredPriorGames,state.events);
 if(!eq(rebuilt,state))throw Error("Observer state differs from append-only replay");
 return {pass:true,choice:state.choice,events:state.events.length,sampled:state.sampled};
}
export function verifyObserver(state){try{return verifyObserverStrict(state)}catch(e){return {pass:false,error:e.message}}}
export function appendExperience(state,input){
 verifyObserverStrict(state);
 if(state.events.length>=128)throw Error("Bounded observer history");
 const i=state.events.length;
 return replay(state.declaredPriorGames,[...state.events,{...copy(input),index:i,parent:i?"e"+String(i-1).padStart(4,"0"):null}]);
}
export function simulatedVeteran({declaredPriorGames=SPACE_24_FACTORIAL,watchRich=true}={}){
 let s=instantiateObserver({declaredPriorGames});
 // Six actual simulated plays in a single repeated game; new patterns taper.
 for(let i=0;i<9;i++)s=appendExperience(s,{mode:"play",game:"arena",patterns:[i<2?"same":i<5?"known":"routine"],payoff:1,cost:0.8});
 for(let i=0;i<4;i++)s=appendExperience(s,{
   mode:"observe",games:["arena","chess","go","cards"],
   patterns:watchRich?["cross"+i,"strategy"+i]:["routine"],
   payoff:0.1,cost:watchRich?0.6:4});
 return s;
}
