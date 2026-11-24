// ADA-257N .dlw — contextual inheritance across sealed epochs.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {epochHierarchy} from "./ada-211n-epoch-engine.mjs";
import {derivePatterns,verifyPatterns,PATTERN_WINDOW} from "./ada-256n-pattern-recognition.mjs";
export function deriveContextualInheritance(chain){
 const source=derivePatterns(chain);if(!verifyPatterns(chain,source).pass)throw Error("Pattern replay failed");
 let prior=null;
 return Object.freeze(epochHierarchy(chain).map(e=>{
 const first=source[e.sourceStart],last=source[e.sourceEnd];
 if(prior&&prior.state!=="SEALED")throw Error("Unsealed predecessor");
 const opening=prior?.closing??Object.freeze([]);
 const closing=last.history;
 const body={schema:"ADA-257N.contextual-inheritance.v1",epoch:e.epoch,state:e.state,epochHash:e.hash,parent:prior?.hash??null,firstPatternHash:first.hash,lastPatternHash:last.hash,opening,closing,closingPatterns:last.patterns,transfer:e.state==="SEALED"?"ELIGIBLE":"PROVISIONAL",window:PATTERN_WINDOW,growthFactor:1.025,authority:"OBSERVE_ONLY"};
 prior=Object.freeze({...body,hash:fnv64(canonical(body))});return prior;
 }));
}
export function verifyContextualInheritance(chain,ledger){
 try{const a=deriveContextualInheritance(chain),s=derivePatterns(chain),epochs=epochHierarchy(chain);
 return {pass:canonical(a)===canonical(ledger)&&a.every((r,i)=>{
 const e=epochs[i],first=s[e.sourceStart],last=s[e.sourceEnd];
 return r.parent===(a[i-1]?.hash??null)&&(!i||a[i-1].state==="SEALED")&&r.epochHash===e.hash&&r.firstPatternHash===first.hash&&r.lastPatternHash===last.hash&&canonical(r.opening)===canonical(a[i-1]?.closing??[])&&canonical(r.closing)===canonical(last.history)&&canonical([...r.opening,first.history.at(-1)].slice(-PATTERN_WINDOW))===canonical(first.history)&&r.closing.length<=PATTERN_WINDOW&&new Set(r.closing.map(h=>h.generation)).size===r.closing.length&&r.authority==="OBSERVE_ONLY"&&r.growthFactor===1.025;
 }),epochs:a.length,sealed:a.filter(r=>r.state==="SEALED").length};}catch(e){return {pass:false,reason:e.message}}
}
