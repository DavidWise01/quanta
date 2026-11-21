// ADA-160D .dlw — pressure acts on a shared-vertex triangular lattice.
// .*.  ->  >.*.<  ->  o
export const CELL_COUNT=13, GATES=8;
export function clampPressure(p){if(!Number.isFinite(p))throw Error("pressure");return Math.max(0,Math.min(1,p));}
export function phaseCell(k,j,p=0){if(!Number.isInteger(k)||k<0||k>=GATES||!Number.isInteger(j)||j<0||j>=CELL_COUNT)throw Error("cell");const P=clampPressure(p),R=1.05+k*.27,q=j*2*Math.PI/CELL_COUNT,qn=(j+1)*2*Math.PI/CELL_COUNT,m=(q+qn)/2,s=1-P;
const A=[R*s*Math.cos(q),R*s*Math.sin(q)],B=[R*s*Math.cos(qn),R*s*Math.sin(qn)],V=[(R-.25)*s*Math.cos(m),(R-.25)*s*Math.sin(m)];
return {A,V,B,center:[0,0],pressure:P,closed:P===1,state:P===1?"o":P===0?".*.":">.*.<"};}
export function signedArea({A,V,B}){return ((V[0]-A[0])*(B[1]-A[1])-(V[1]-A[1])*(B[0]-A[0]))/2;}
export function verifyPressure(){const tolerance=1e-10,results=[];let checks=0,shared=0,collapsed=0;
for(const p of [0,.125,.25,.5,.75,.875,1]){
 let min=Infinity,max=0;
 for(let k=0;k<GATES;k++)for(let j=0;j<CELL_COUNT;j++){
  const c=phaseCell(k,j,p),next=phaseCell(k,(j+1)%CELL_COUNT,p),un=phaseCell(k,j,0);
  const dist=(u,v)=>Math.hypot(u[0]-v[0],u[1]-v[1]);
  if(dist(c.B,next.A)>tolerance)throw Error("unshared boundary "+k+"/"+j);
  if(Math.abs(Math.abs(signedArea(c))-Math.abs(signedArea(un))*(1-p)**2)>tolerance)throw Error("area scaling");
  if(p===1&&(![c.A,c.V,c.B].every(v=>dist(v,[0,0])<tolerance)||c.state!=="o"))throw Error("closure");
  if(p<1&&c.closed)throw Error("premature closure");
  if(p===1)collapsed++;
  min=Math.min(min,Math.abs(signedArea(c)));max=Math.max(max,Math.abs(signedArea(c)));
  checks+=4;shared++;
 }
 results.push({pressure:p,areaFraction:(1-p)**2,minArea:min,maxArea:max,state:phaseCell(0,0,p).state});
}
for(let k=0;k<GATES;k++)for(let j=0;j<CELL_COUNT;j++){const before=phaseCell(k,j,0),after=phaseCell(k,j,1),again=phaseCell(k,j,0);if(after.state!=="o"||before.A[0]!==again.A[0]||before.V[1]!==again.V[1])throw Error("reversible parameters");checks++;}
return {cells:GATES*CELL_COUNT,sharedEdgesVerified:shared,checks,collapsed,results,reversibleByPressureControl:true,interpretation:"symbolic pressure contraction: not a physical equation of state"};}
