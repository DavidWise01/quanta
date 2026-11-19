// ADA-159B .dlw — 42-bit Stargate, three-layer tornado.
export const GATE="00 11 [ 24 /|\\ 42 ] 11 00";
export const WIDTH=42, TURN=1296000000, OFFSET=1025;
export const LAYERS=Object.freeze(["|V| vector","[] voxel","{[()]} vogel"]);
export function pack(s,c,i,w){const a=[s,c,i,w],n=[24,9,1,8];if(a.some((v,j)=>typeof v!=="bigint"||v<0n||v>=1n<<BigInt(n[j])))throw Error("width");return s|(c<<24n)|(i<<33n)|(w<<34n);}
export function unpack(v){if(typeof v!=="bigint"||v<0n||v>=1n<<42n)throw Error("width");return [v&0xffffffn,(v>>24n)&511n,(v>>33n)&1n,(v>>34n)&255n];}

 // ADA-159C .dlw — antistrophic circulation, local phase offsets.
export const FRAME=Object.freeze([{name:"|V| vector",hand:1,phase:0},{name:"[] voxel",hand:-1,phase:2},{name:"{[()]} vogel",hand:1,phase:4}].map(Object.freeze));
const wrap=a=>((a%TURN)+TURN)%TURN;
export function initial(){return {tick:0,x:null,layers:FRAME.map((f,i)=>({...f,angle:i*TURN/3,net:0,push:0,pull:0}))};}
export function step(s,x){if(!Number.isSafeInteger(x)||x<0||x>TURN)throw Error("x in milliarcseconds");const latched=s.tick%8===0?x:s.x;
 return {tick:s.tick+1,x:latched,layers:s.layers.map(l=>{const p=(s.tick+l.phase)%8,pull=p>=4,local=pull?-(latched+OFFSET):latched,delta=l.hand*local;
 return {...l,p,delta,angle:wrap(l.angle+delta),net:l.net+delta,push:l.push+Number(!pull),pull:l.pull+Number(pull)};})};}
export function verify(){let cases=0;for(const x of [0,1,1000,1025,123456,TURN-1,TURN]){let s=initial();for(let n=0;n<80;n++){s=step(s,n%8===0?x:0);if(s.layers.some(l=>l.angle<0||l.angle>=TURN))throw Error("wrap");if((n+1)%8===0){const cycles=(n+1)/8;for(const l of s.layers)if(l.net!==-4100*l.hand*cycles||l.push!==4*cycles||l.pull!==4*cycles)throw Error("balance");cases++;}}}
 for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("payload");cases++;}
 let s=initial();const ledger=[];for(let i=0;i<8;i++){s=step(s,1000);ledger.push(s);}return {cases,cycleNet:s.layers.map(l=>l.net),events:24,ledger};}
