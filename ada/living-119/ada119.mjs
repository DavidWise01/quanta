// ADA-119 .dlw — candidate 40-bit encoding of one symbolic quantum dot.
// RBG order retained. Eight bits per color, five for 26 symbols, eleven reserved.
export function pack(r,b,g,s,reserved=0){for(const [v,max] of [[r,255],[b,255],[g,255],[s,25],[reserved,2047]])if(!Number.isInteger(v)||v<0||v>max)throw Error("range");return (BigInt(r)<<32n)|(BigInt(b)<<24n)|(BigInt(g)<<16n)|(BigInt(s)<<11n)|BigInt(reserved);}
export function unpack(x){x=BigInt(x);if(x<0n||x>=1n<<40n)throw Error("width");const s=Number(x>>11n&31n);if(s>25)throw Error("reserved symbol");return [Number(x>>32n&255n),Number(x>>24n&255n),Number(x>>16n&255n),s,Number(x&2047n)];}
export function label(s){const a=String.fromCharCode(65+s),b=a.toLowerCase();return a+b+b+a;}
export function test(){let checks=0;for(let s=0;s<26;s++)for(let m=0;m<8;m++)for(const v of [0,255]){const a=[1<<m,v,255-v,s,2047],x=pack(...a);if(unpack(x).join()!=a.join())throw Error("roundtrip");checks++;}return {checks,labels:Array.from({length:26},(_,s)=>label(s)),maxWord:pack(255,255,255,25,2047).toString(16),width:40};}

console.log(JSON.stringify(test(),null,2));