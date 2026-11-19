// ADA-159B .dlw — 42-bit Stargate, three-layer tornado.
export const GATE="00 11 [ 24 /|\\ 42 ] 11 00";
export const WIDTH=42, TURN=1296000000, OFFSET=1025;
export const LAYERS=Object.freeze(["|V| vector","[] voxel","{[()]} vogel"]);
export function pack(s,c,i,w){const a=[s,c,i,w],n=[24,9,1,8];if(a.some((v,j)=>typeof v!=="bigint"||v<0n||v>=1n<<BigInt(n[j])))throw Error("width");return s|(c<<24n)|(i<<33n)|(w<<34n);}
export function unpack(v){if(typeof v!=="bigint"||v<0n||v>=1n<<42n)throw Error("width");return [v&0xffffffn,(v>>24n)&511n,(v>>33n)&1n,(v>>34n)&255n];}
export function step(s,x){if(!Number.isSafeInteger(x)||x<0||x>TURN)throw Error("x in milliarcseconds");const phase=s.tick%8,pull=phase>=4,delta=pull?-(x+OFFSET):x;return {tick:s.tick+1,angle:((s.angle+delta)%TURN+TURN)%TURN,net:s.net+delta,phase,pull,delta};}
export function cycle(x){let s={tick:0,angle:0,net:0};const ledger=[];for(let i=0;i<8;i++){s=step(s,x);ledger.push({...s});}return {state:s,ledger};}
export function verify(){let cases=0;for(const x of [0,1,1000,1025,123456,TURN-1,TURN]){const {state,ledger}=cycle(x);if(state.net!==-4100||ledger.filter(v=>v.pull).length!==4||ledger.some(v=>v.angle<0||v.angle>=TURN))throw Error("cycle");cases++;}let v=0n;for(let j=0;j<42;j++){v=1n<<BigInt(j);if(pack(...unpack(v))!==v)throw Error("packing");cases++;}return {cases,netMilliarcseconds:-4100,phases:8,layers:3,layerEvents:24};}
