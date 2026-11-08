/** QUANTA QG-027 — 26 glyphs × three assigned semantic roles: SEE / DO / LEARN.
 * These are a deliberately authored lexicon, not naturally inferred meanings.
 * X uses hyphenated X-prefixed technical/constructed labels.
 */
export const SEMANTIC_TRIAD_VERSION="QG-027.1";
export const SEMANTIC_TRIAD_CARRIER="||||";
export const TRIAD_ROLES=Object.freeze(["see","do","learn"]);
const TERMS=Object.freeze([["Alarm","Action","Achieve"],["Beacon","Build","Become"],["Clue","Choose","Comprehend"],["Detail","Decide","Discover"],["Evidence","Experiment","Evolve"],["Feature","Follow","Find"],["Glimpse","Gather","Grow"],["Hint","Handle","Hone"],["Image","Interact","Integrate"],["Junction","Join","Judge"],["Key","Keep","Know"],["Light","Lift","Learn"],["Mark","Move","Master"],["Notice","Navigate","Name"],["Observe","Operate","Optimize"],["Pattern","Practice","Prove"],["Question","Query","Qualify"],["Ripple","Respond","Remember"],["Signal","Shape","Synthesize"],["Trace","Test","Transform"],["Unknown","Uncover","Understand"],["Vision","Verify","Validate"],["Warning","Work","Wisdom"],["X-ray","X-ray-test","X-reference"],["Yield","Yoke","Yearn"],["Zigzag","Zoom","Zero-in"]]);
export const SEMANTIC_ALPHABET=Object.freeze(Array.from({length:26},(_,i)=>{
 const letter=String.fromCharCode(65+i),[see,act,learn]=TERMS[i];
 return Object.freeze({letter,token:"||"+letter+"||",
  roles:Object.freeze({see,do:act,learn}),
  terms:Object.freeze([see,act,learn])});
}));
export function semanticTriad(letter){
 if(typeof letter!=="string"||!/^[A-Z]$/.test(letter))
  throw new TypeError("Expected one uppercase letter A–Z");
 return SEMANTIC_ALPHABET[letter.charCodeAt(0)-65];
}
export function semanticRole(letter,role){
 if(!TRIAD_ROLES.includes(role))throw new TypeError("Role must be see, do or learn");
 return semanticTriad(letter).roles[role];
}
export function semanticTriadText(text){
 if(typeof text!=="string"||text.length>128||!/^[A-Z ]*$/.test(text))
  throw new TypeError("Expected 0–128 uppercase A–Z letters and spaces");
 return Object.freeze({version:SEMANTIC_TRIAD_VERSION,carrier:SEMANTIC_TRIAD_CARRIER,
  source:text,items:Object.freeze([...text].map(ch=>ch===" "?null:semanticTriad(ch)))});
}
export function recoverSemanticTriadText(frame){
 if(!frame||frame.version!==SEMANTIC_TRIAD_VERSION||frame.carrier!==SEMANTIC_TRIAD_CARRIER)
  throw new TypeError("Unknown semantic triad frame");
 const expected=semanticTriadText(frame.source);
 if(JSON.stringify(frame)!==JSON.stringify(expected))throw new Error("Triad/letter sequence witness mismatch");
 return frame.source;
}
