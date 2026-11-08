/**
 * QUANTA QG-016.1 — Alphabet Box / Phase–Semantic–Somatic Transport.
 *
 * Carrier: |||| ; tokens: ||A|| .. ||Z||
 * Quad phase: a=0°, b=90°, c=180°, d=270°.
 * Four presentation levels per quad: 4,3,2,1.
 *
 * Geometric strokes are polygonal vector paths in a 5×5 lattice.
 * Semantic channel is stable glyph identity plus optional application-assigned meaning.
 * Somatic channel is an ordered series of pen verbs with coordinates.
 * Presentation folding never deletes original graph/strokes in the packet.
 *
 * Not encryption, font rendering, a language understanding claim or physics.
 */
export const ALPHABET_BOX_VERSION="QG-016.1";
export const BOX_CARRIER="||||";
export const QUADS=Object.freeze([
  Object.freeze({name:"a",degrees:0}),
  Object.freeze({name:"b",degrees:90}),
  Object.freeze({name:"c",degrees:180}),
  Object.freeze({name:"d",degrees:270})
]);
export const LEVELS=Object.freeze([4,3,2,1]);

// Each semicolon separates pen strokes. Paths use five-grid points.
const PATTERNS=Object.freeze({
 A:"0,4 2,0 4,4;1,3 3,3",
 B:"0,0 0,4;0,0 3,0 4,1 3,2 0,2;0,2 3,2 4,3 3,4 0,4",
 C:"4,0 1,0 0,1 0,3 1,4 4,4",
 D:"0,0 0,4 2,4 4,3 4,1 2,0 0,0",
 E:"4,0 0,0 0,4 4,4;0,2 3,2",
 F:"0,4 0,0 4,0;0,2 3,2",
 G:"4,0 1,0 0,1 0,3 1,4 4,4 4,2 2,2",
 H:"0,0 0,4;4,0 4,4;0,2 4,2",
 I:"0,0 4,0;2,0 2,4;0,4 4,4",
 J:"0,0 4,0;3,0 3,3 2,4 1,4 0,3",
 K:"0,0 0,4;4,0 0,2 4,4",
 L:"0,0 0,4 4,4",
 M:"0,4 0,0 2,2 4,0 4,4",
 N:"0,4 0,0 4,4 4,0",
 O:"1,0 3,0 4,1 4,3 3,4 1,4 0,3 0,1 1,0",
 P:"0,4 0,0 3,0 4,1 3,2 0,2",
 Q:"1,0 3,0 4,1 4,3 3,4 1,4 0,3 0,1 1,0;2,2 4,4",
 R:"0,4 0,0 3,0 4,1 3,2 0,2;2,2 4,4",
 S:"4,0 1,0 0,1 1,2 3,2 4,3 3,4 0,4",
 T:"0,0 4,0;2,0 2,4",
 U:"0,0 0,3 1,4 3,4 4,3 4,0",
 V:"0,0 2,4 4,0",
 W:"0,0 1,4 2,2 3,4 4,0",
 X:"0,0 4,4;4,0 0,4",
 Y:"0,0 2,2 4,0;2,2 2,4",
 Z:"0,0 4,0 0,4 4,4"
});
const LETTERS=Object.freeze(Object.keys(PATTERNS));
function requireLetter(ch){
 if(typeof ch!=="string"||!Object.hasOwn(PATTERNS,ch))throw new TypeError("Use one uppercase ASCII letter A–Z.");
}
function pointPair(s){
 const p=s.split(",").map(Number);
 if(p.length!==2||p.some(x=>!Number.isInteger(x)||x<0||x>4))throw new Error("Invalid canonical stroke grid");
 return Object.freeze({x:p[0],y:p[1]});
}
function compilePaths(pattern){
 return Object.freeze(pattern.split(";").map(stroke=>Object.freeze(stroke.split(" ").map(pointPair))));
}
const GLYPHS=Object.freeze(Object.fromEntries(LETTERS.map(ch=>[ch,compilePaths(PATTERNS[ch])])));
export function alphabet(){return LETTERS;}
export function pathsFor(letter){requireLetter(letter);return GLYPHS[letter];}
export function tokenFor(letter){requireLetter(letter);return "||"+letter+"||";}
export function parseToken(token){
 if(typeof token!=="string"||!(/^\|\|[A-Z]\|\|$/).test(token))throw new TypeError("Expected token ||A|| through ||Z||.");
 return token[2];
}
export function rotatePoint(point,degrees){
 const {x,y}=point;
 if(degrees===0)return Object.freeze({x,y});
 if(degrees===90)return Object.freeze({x:4-y,y:x});
 if(degrees===180)return Object.freeze({x:4-x,y:4-y});
 if(degrees===270)return Object.freeze({x:y,y:4-x});
 throw new RangeError("Phase must be 0/90/180/270 degrees");
}
export function rotatePaths(paths,degrees){
 return Object.freeze(paths.map(stroke=>Object.freeze(stroke.map(pt=>rotatePoint(pt,degrees)))));
}
function strokeVerbs(paths){
 const verbs=[];
 for(let s=0;s<paths.length;s++){
   const path=paths[s];
   if(!path.length)continue;
   verbs.push(Object.freeze({verb:"PEN_UP",stroke:s}));
   verbs.push(Object.freeze({verb:"MOVE",to:path[0],stroke:s}));
   for(let i=1;i<path.length;i++){
     const from=path[i-1],to=path[i];
     const dx=to.x-from.x,dy=to.y-from.y;
     verbs.push(Object.freeze({verb:"DRAW",from,to,dx,dy,stroke:s}));
     if(i>=2){
       const earlier=path[i-2],ax=from.x-earlier.x,ay=from.y-earlier.y;
       const cross=ax*dy-ay*dx;
       if(cross!==0)verbs.push(Object.freeze({verb:"TURN",orientation:cross>0?"clockwise":"counterclockwise",stroke:s,at:from}));
     }
   }
   verbs.push(Object.freeze({verb:"PEN_UP",stroke:s}));
 }
 return Object.freeze(verbs);
}
function presentation(paths,level){
 // 4 = full line geometry; 3 = vertices, 2 = midpoints per stroke,
 // 1 = one point. All are projections; immutable full source stays in packet.
 const points=paths.flat();
 if(level===4)return Object.freeze({kind:"geometry",paths});
 if(level===3)return Object.freeze({kind:"vertices",points:Object.freeze(points)});
 const total=points.length;
 if(!total)throw new Error("Missing source geometry");
 if(level===2){
  const a=points[0],b=points[total-1];
  return Object.freeze({kind:"endpoints",points:Object.freeze([a,b])});
 }
 const sum=points.reduce((o,p)=>({x:o.x+p.x,y:o.y+p.y}),{x:0,y:0});
 return Object.freeze({kind:"chrome-dot",point:Object.freeze({x:sum.x/total,y:sum.y/total})});
}
export function transportLetter(letter,options={}){
 requireLetter(letter);
 const meaning=options.meaning??null;
 if(meaning!==null&&(typeof meaning!=="string"||meaning.length>256))throw new TypeError("Meaning must be a string <=256 chars or null.");
 const source=GLYPHS[letter];
 const quads=Object.freeze(QUADS.map(q=>{
  const paths=rotatePaths(source,q.degrees);
  return Object.freeze({
   name:q.name,degrees:q.degrees,
   geometry:paths,
   somatic:strokeVerbs(paths),
   levels:Object.freeze(LEVELS.map(level=>Object.freeze({level,view:presentation(paths,level)})))
  });
 }));
 return Object.freeze({
  version:ALPHABET_BOX_VERSION,
  carrier:BOX_CARRIER,
  token:tokenFor(letter),
  semantic:Object.freeze({letter,name:"LATIN CAPITAL LETTER "+letter,meaning}),
  source,
  quads
 });
}
export function recoverLetter(packet){
 if(!packet||packet.version!==ALPHABET_BOX_VERSION||packet.carrier!==BOX_CARRIER)throw new TypeError("Unknown box packet");
 const letter=parseToken(packet.token);
 if(packet.semantic?.letter!==letter)throw new Error("Semantic identity mismatch");
 const expected=JSON.stringify(GLYPHS[letter]);
 if(JSON.stringify(packet.source)!==expected)throw new Error("Source geometry mismatch");
 if(!Array.isArray(packet.quads)||packet.quads.length!==4)throw new Error("All four quads are required");
 for(let i=0;i<4;i++){
  const q=packet.quads[i],canonical=QUADS[i];
  if(q.name!==canonical.name||q.degrees!==canonical.degrees ||
     JSON.stringify(q.geometry)!==JSON.stringify(rotatePaths(GLYPHS[letter],canonical.degrees)) ||
     JSON.stringify(q.somatic)!==JSON.stringify(strokeVerbs(rotatePaths(GLYPHS[letter],canonical.degrees))) ||
     JSON.stringify(q.levels)!==JSON.stringify(LEVELS.map(level=>({level,view:presentation(rotatePaths(GLYPHS[letter],canonical.degrees),level)}))))
     throw new Error("Quad phase / geometry / somatic / level mismatch at "+canonical.name);
 }
 return Object.freeze({letter,token:packet.token,meaning:packet.semantic.meaning,source:GLYPHS[letter]});
}
export function transportText(text,options={}){
 if(typeof text!=="string"||!(/^[A-Z]*$/).test(text)||text.length>1024)throw new TypeError("Use 0–1024 uppercase A–Z letters.");
 return Object.freeze({version:ALPHABET_BOX_VERSION,carrier:BOX_CARRIER,packets:Object.freeze([...text].map(ch=>transportLetter(ch,options)))});
}
export function recoverText(stream){
 if(!stream||stream.version!==ALPHABET_BOX_VERSION||stream.carrier!==BOX_CARRIER||!Array.isArray(stream.packets)||stream.packets.length>1024)throw new TypeError("Invalid box stream");
 return stream.packets.map(p=>recoverLetter(p).letter).join("");
}
