// ADA-230N .dlw — acceptance gate, append-only strengthening of ADA-229N.
import {canonical,genesis,advance} from "./ada-201n-generational-engine.mjs";
import {auditSpatial} from "./ada-229n-spatial-stability.mjs";
import {deriveMorphogenesis} from "./ada-228n-morphogenesis.mjs";
import {deriveSpecialization} from "./ada-227n-geometric-specialization.mjs";
export function certifySpatial(chain){
 const result=auditSpatial(chain),m=deriveMorphogenesis(chain),s=deriveSpecialization(chain);
 result.checks.exactCausality=m.every((r,i)=>r.previousSurfaceHash===(s[i-1]?.hash??null)&&r.sourceHash===s[i].sourceHash);
 const prefix=deriveMorphogenesis(chain.slice(0,Math.min(240,chain.length)));
 result.checks.prefix=prefix.every((r,i)=>canonical(r)===canonical(m[i]));
 result.pass=Object.values(result.checks).every(Boolean);
 return result;
}
export function runFreeze(steps=2400){
 if(!Number.isSafeInteger(steps)||steps<1||steps>9600)throw Error("Invalid horizon");
 let chain=[genesis()];for(let i=0;i<steps;i+=1000)chain=advance(chain,Math.min(1000,steps-i));
 return certifySpatial(chain);
}
