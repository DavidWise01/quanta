// ADA-159N .dlw — Eye of the Observer, parametric 3D toroidal tornado
export const CANONICAL=String.raw`{outerbound,brace\tornado[innerbound(chaos/tornado)]}`;
export const EYE=Object.freeze([0,0,0]);
export const BANDS=Object.freeze([{name:"Vogel",space:"state space",coords:"vwxyz",code:"r8!",color:"#ff4565",tube:.89,hand:1},{name:"Voxel",space:"operant space",coords:"wxyz",code:"b8!",color:"#399dff",tube:.65,hand:-1},{name:"Vector",space:"operants",coords:"xy:`z`",code:"g8!",color:"#35ffa3",tube:.40,hand:1}].map(Object.freeze));
export const TAU=2*Math.PI;
export function point(u,v,k,t=0,chaos=.5){const b=BANDS[k],a=b.tube*(1+.08*chaos*Math.sin(3*u+2*v+t)),r=1.65+a*Math.cos(v),theta=u+b.hand*.42*Math.sin(v)+.11*chaos*Math.sin(3*v+2*u+t),y=2.1*a*Math.sin(v);return [r*Math.cos(theta),y,r*Math.sin(theta)];}
export function streamline(q,arm,k,t=0,chaos=.5){const b=BANDS[k];return point(b.hand*3*q+arm*TAU/4+t*b.hand,2*q+arm*TAU/4+t*.36,k,t,chaos);}
export function verify(){let samples=0,min=Infinity,closure=0;for(const t of [0,1,5,13])for(const a of [0,.5,1])for(let k=0;k<3;k++)for(let j=0;j<128;j++){const q=j*TAU/128,p=streamline(q,j%4,k,t,a),p2=streamline(q+TAU,j%4,k,t,a),r=Math.hypot(p[0],p[2]);min=Math.min(min,r);closure=Math.max(closure,Math.hypot(...p.map((v,i)=>v-p2[i])));if(!p.every(Number.isFinite)||r<.68||r>2.62||Math.abs(p[1])>2.03)throw Error("bound");samples++;}if(closure>1e-10||EYE.some(Boolean))throw Error("eye/closure");return {samples,minEyeClearance:min,maxClosureError:closure,eye:EYE,streams:12,width:42};}

 // ADA-159O .dlw — nonorientable return ribbon, fixed observer.
export const HALF_WIDTH=.24, RETURN_RADIUS=1.65;
export function ribbon(u,s,t=0,chaos=.5){const theta=u+t*.32,tw=u/2,mid=RETURN_RADIUS+.07*chaos*Math.sin(3*u+t),r=mid+s*Math.cos(tw);return [r*Math.cos(theta),.32*Math.sin(2*u+t)*chaos+s*Math.sin(tw),r*Math.sin(theta)];}
export function returnPath(q,t=0,chaos=.5){return ribbon(q,HALF_WIDTH*.86,t,chaos);}
const distance=(a,b)=>Math.hypot(...a.map((v,k)=>v-b[k]));
export function verifyReturn(){const original=verify();let samples=0,swapError=0,doubleError=0,minClearance=Infinity,minOneLap=Infinity,maxCenterError=0;for(const t of [0,1,5,13])for(const a of [0,.5,1])for(let j=0;j<128;j++){const u=j*TAU/128;for(const s of [-HALF_WIDTH,-.12,0,.12,HALF_WIDTH]){const p=ribbon(u,s,t,a);swapError=Math.max(swapError,distance(ribbon(u+TAU,s,t,a),ribbon(u,-s,t,a)));doubleError=Math.max(doubleError,distance(ribbon(u+2*TAU,s,t,a),p));minClearance=Math.min(minClearance,Math.hypot(p[0],p[2]));if(!p.every(Number.isFinite))throw Error("nonfinite");samples++;}minOneLap=Math.min(minOneLap,distance(returnPath(u+TAU,t,a),returnPath(u,t,a)));maxCenterError=Math.max(maxCenterError,distance(ribbon(u+TAU,0,t,a),ribbon(u,0,t,a)));}if(swapError>1e-10||doubleError>1e-10||minClearance<1.33||minOneLap<.4||EYE.some(Boolean))throw Error("return invariant");return {original,samples,swapError,doubleError,minClearance,minOneLap,maxCenterError,eye:EYE,halfTwists:1,edgeLaps:2};}

 // ADA-159P .dlw — dot-first frozen grammar; mirrored channels.
export const DOT_GRAMMAR=String.raw`\r8!\b8!\g8! | . | /g8!/b8!/r8!`;
export const DOT_RADIUS=.14;
export const CHANNELS=Object.freeze([0,1,2].map(k=>Object.freeze({band:k,ingress:true})).concat([2,1,0].map(k=>Object.freeze({band:k,ingress:false}))));
export function channel(q,k,side,t=0){const p=streamline(q,0,k,t,.5);return side===1?p:p.map(v=>-v);}
export function verifyDot(){const inherited=verifyReturn();let samples=0,maxMirror=0,min=Infinity;for(const t of [0,1,5,13])for(let k=0;k<3;k++)for(let j=0;j<256;j++){const p=channel(j*TAU/256,k,1,t),m=channel(j*TAU/256,k,-1,t);maxMirror=Math.max(maxMirror,Math.hypot(...p.map((v,i)=>v+m[i])));min=Math.min(min,Math.hypot(...p)-DOT_RADIUS);samples++;}if(maxMirror!==0||min<=0||EYE.some(Boolean)||CHANNELS.map(c=>c.band).join()!=="0,1,2,2,1,0")throw Error("dot");return {inherited,samples,maxMirror,minSurfaceClearance:min,eye:EYE,width:42,channelOrder:CHANNELS.map(c=>BANDS[c.band].code)};}
