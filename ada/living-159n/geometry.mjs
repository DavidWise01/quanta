// ADA-159N .dlw — Eye of the Observer, parametric 3D toroidal tornado
export const CANONICAL=String.raw`{outerbound,brace\tornado[innerbound(chaos/tornado)]}`;
export const EYE=Object.freeze([0,0,0]);
export const BANDS=Object.freeze([{name:"Vogel",space:"state space",coords:"vwxyz",code:"r8!",color:"#ff4565",tube:.89,hand:1},{name:"Voxel",space:"operant space",coords:"wxyz",code:"b8!",color:"#399dff",tube:.65,hand:-1},{name:"Vector",space:"operants",coords:"xy:`z`",code:"g8!",color:"#35ffa3",tube:.40,hand:1}].map(Object.freeze));
export const TAU=2*Math.PI;
export function point(u,v,k,t=0,chaos=.5){const b=BANDS[k],a=b.tube*(1+.08*chaos*Math.sin(3*u+2*v+t)),r=1.65+a*Math.cos(v),theta=u+b.hand*.42*Math.sin(v)+.11*chaos*Math.sin(3*v+2*u+t),y=2.1*a*Math.sin(v);return [r*Math.cos(theta),y,r*Math.sin(theta)];}
export function streamline(q,arm,k,t=0,chaos=.5){const b=BANDS[k];return point(b.hand*3*q+arm*TAU/4+t*b.hand,2*q+arm*TAU/4+t*.36,k,t,chaos);}
export function verify(){let samples=0,min=Infinity,closure=0;for(const t of [0,1,5,13])for(const a of [0,.5,1])for(let k=0;k<3;k++)for(let j=0;j<128;j++){const q=j*TAU/128,p=streamline(q,j%4,k,t,a),p2=streamline(q+TAU,j%4,k,t,a),r=Math.hypot(p[0],p[2]);min=Math.min(min,r);closure=Math.max(closure,Math.hypot(...p.map((v,i)=>v-p2[i])));if(!p.every(Number.isFinite)||r<.68||r>2.62||Math.abs(p[1])>2.03)throw Error("bound");samples++;}if(closure>1e-10||EYE.some(Boolean))throw Error("eye/closure");return {samples,minEyeClearance:min,maxClosureError:closure,eye:EYE,streams:12,width:42};}
