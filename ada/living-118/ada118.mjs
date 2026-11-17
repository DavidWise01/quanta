// ADA-118 .dlw — finite symbolic PB substrate, not a nuclear model.
export const N=26, MODES=8;
// Eight reversible directions on Z26; opposite modes paired.
export const shifts=[1,-1,3,-3,5,-5,7,-7];
export function encode(m,p){if(!Number.isInteger(m)||m<0||m>=8||!Number.isInteger(p)||p<0||p>=26)throw Error("range");return 26*m+p;}
export function decode(a){if(!Number.isInteger(a)||a<0||a>=208)throw Error("range");return [Math.floor(a/26),a%26];}
export function step(a){const [m,p]=decode(a);return encode(m,(p+shifts[m]+26)%26);}
export function opposite(a){const [m,p]=decode(a);return encode(m^1,p);}
export function switchMode(a,m){return encode(m,decode(a)[1]);}
export function phase(t){t=BigInt(t);if(t<0n)throw Error("negative");return ["abc","bca","cab"][Number(t%1296000n/432000n)];}
export function test(){let addresses=0,inverse=0,cycles=0;const periods=[];for(let a=0;a<208;a++){if(encode(...decode(a))!==a)throw Error("address");addresses++;if(opposite(step(opposite(step(a))))!==a)throw Error("inverse");inverse++;}for(let m=0;m<8;m++){let a=encode(m,0),b=step(a),k=1;while(b!==a&&k<=26){b=step(b);k++;}if(k!==26)throw Error("cycle");periods.push(k);cycles++;}const seen=new Set([0]),q=[0];for(let i=0;i<q.length;i++){let a=q[i];for(const b of [step(a),...Array.from({length:8},(_,m)=>switchMode(a,m))])if(!seen.has(b)){seen.add(b);q.push(b);}}if(seen.size!==208)throw Error("reachability");const clockTests=[0n,431999n,432000n,863999n,864000n,1295999n,1296000n].map(t=>({tick:String(t),phase:phase(t)}));return {addresses,inverse,cycles,periods,reachable:seen.size,clockTests};}

console.log(JSON.stringify(test(),null,2));
