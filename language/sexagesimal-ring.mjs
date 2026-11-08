/**
 * QUANTA QG-025 — SEXAGESIMAL 60 RING
 * Historical inspiration: Babylonian radix-60 positional notation.
 * The four-quad 15-station phase ring is a QUANTA design, not a historical claim.
 * Carrier |||| ; 60 stations, 0..59; 4x15; 90°=+15 modulo 60.
 * Integer radix conversion uses BigInt. Glyph source witnesses remain explicit.
 */
export const VERSION="QG-025.1", CARRIER="||||", BASE=60, QUADS=4, PER_QUAD=15;
export const DIVISORS=Object.freeze([1,2,3,4,5,6,10,12,15,20,30,60]);
export const QUAD_NAMES=Object.freeze(["a","b","c","d"]);
const freeze=Object.freeze;
function station(n){if(!Number.isInteger(n)||n<0||n>=BASE)throw new RangeError("Station must be 0..59");return n}
function bigint(v){if(typeof v==="bigint"&&v>=0n)return v;if(typeof v==="string"&&/^(0|[1-9][0-9]*)$/.test(v))return BigInt(v);throw new TypeError("Nonnegative integer string or bigint required");}
export function phaseStation(n,turns=1){
 station(n);if(!Number.isInteger(turns))throw new TypeError("Integer quarter turns required");
 return ((n+PER_QUAD*(turns%4))%BASE+BASE)%BASE;
}
export function locateStation(n){
 station(n);return freeze({station:n,quad:QUAD_NAMES[Math.floor(n/PER_QUAD)],local:n%PER_QUAD,angle:n*6});
}
export function stationRing(){
 return freeze(Array.from({length:BASE},(_,n)=>locateStation(n)));
}
export function toSexagesimal(number){
 let x=bigint(number);
 if(x===0n)return freeze([0]);
 const digits=[];
 while(x>0n){digits.unshift(Number(x%60n));x/=60n;}
 return freeze(digits);
}
export function fromSexagesimal(digits){
 if(!Array.isArray(digits)||digits.length<1||digits.length>256||!digits.every(d=>Number.isInteger(d)&&d>=0&&d<BASE))
  throw new TypeError("Expected 1..256 sexagesimal digits 0..59");
 if(digits.length>1&&digits[0]===0)throw new TypeError("Leading zero not canonical");
 return digits.reduce((acc,d)=>acc*60n+BigInt(d),0n);
}
export function displaySexagesimal(digits){
 fromSexagesimal(digits);
 return digits.map(d=>String(d).padStart(2,"0")).join(":");
}
export function parseSexagesimal(s){
 if(typeof s!=="string"||!/^(?:[0-5]?\d)(?::(?:[0-5]?\d))*$/.test(s))throw new TypeError("Use colon-separated digits 0..59");
 const digits=s.split(":").map(Number);
 fromSexagesimal(digits);return freeze(digits);
}
export function makeTransport(number){
 const digits=toSexagesimal(number);
 const positions=freeze(digits.map((digit,index)=>freeze({
  index,digit,
  location:locateStation(digit),
  phases:freeze(Array.from({length:4},(_,q)=>freeze({
    quad:QUAD_NAMES[q],degrees:90*q,station:phaseStation(digit,q)
  })))
 })));
 return freeze({version:VERSION,carrier:CARRIER,radix:BASE,
   decimal:bigint(number).toString(),digits,positions});
}
export function recoverTransport(packet){
 if(!packet||packet.version!==VERSION||packet.carrier!==CARRIER||packet.radix!==BASE)
  throw new TypeError("Unknown sexagesimal transport frame");
 const expected=makeTransport(packet.decimal);
 if(JSON.stringify(packet)!==JSON.stringify(expected))throw new Error("Transport witness or phase mismatch");
 return fromSexagesimal(packet.digits);
}
export function verifyTransport(packet){
 try{const value=recoverTransport(packet);return freeze({pass:true,decimal:value.toString(),digits:packet.digits.length,stations:BASE,quads:QUADS});}
 catch(error){return freeze({pass:false,error:error.message});}
}
