// ADA-233N .dlw — conservative internal circulation, derived from immutable intake.
import {canonical,fnv64} from "./ada-201n-generational-engine.mjs";
import {deriveIntake,verifyIntake} from "./ada-232n-resource-intake.mjs";
export function deriveCirculation(chain){
 const source=deriveIntake(chain);if(!verifyIntake(chain,source).pass)throw Error("Intake replay failed");
 let parent=null,prior=null;
 return Object.freeze(source.map((s,i)=>{
 const levels=Object.freeze(s.levels.map(l=>{
 const activeOpening=prior?.levels[l.depth].activeClosing??0;
 const inputOpening=prior?.levels[l.depth].inputClosing??0;
 const available=inputOpening+l.accepted;
 const activeLimit=Math.floor(l.capacity/2);
 const requested=Math.floor(available*chain[i].stability/400);
 const transferred=l.enabled?Math.min(requested,activeLimit-activeOpening):0;
 return Object.freeze({depth:l.depth,capacity:l.capacity,activeLimit,inputOpening,activeOpening,accepted:l.accepted,requested,transferred,inputClosing:available-transferred,activeClosing:activeOpening+transferred,totalClosing:l.closing,enabled:l.enabled,expenditure:0});
 }));
 const body={schema:"ADA-233N.circulation.v1",generation:s.generation,sourceHash:s.sourceHash,intakeHash:s.hash,parent,levels,growthFactor:1.025,unit:"nano-resource"};
 parent=fnv64(canonical(body));prior=Object.freeze({...body,hash:parent});return prior;
 }));
}
export function verifyCirculation(chain,ledger){
 try{const expected=deriveCirculation(chain);return {pass:canonical(expected)===canonical(ledger)&&expected.every((s,i)=>s.growthFactor===1.025&&s.levels.every(l=>[l.inputOpening,l.activeOpening,l.accepted,l.requested,l.transferred,l.inputClosing,l.activeClosing,l.totalClosing].every(x=>Number.isSafeInteger(x)&&x>=0)&&l.inputOpening===(expected[i-1]?.levels[l.depth].inputClosing??0)&&l.activeOpening===(expected[i-1]?.levels[l.depth].activeClosing??0)&&l.inputClosing===l.inputOpening+l.accepted-l.transferred&&l.activeClosing===l.activeOpening+l.transferred&&l.inputClosing+l.activeClosing===l.totalClosing&&l.totalClosing<=l.capacity&&l.activeClosing<=l.activeLimit&&l.transferred<=l.requested&&l.expenditure===0&&(l.enabled||l.transferred===0))),count:expected.length};}catch(e){return {pass:false,reason:e.message}}
}
