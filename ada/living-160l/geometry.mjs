// ADA-160F 4D anchored amplitude .dlw
export const TAU=2*Math.PI,CONTACTS=24,GATES=8,CHANNELS=Object.freeze([2,4,3,3,1,1]),GRAMMAR="{24/[2]/[4]/(3)/(3)/(1)/(1)";
export function clamp(x){if(!Number.isFinite(x))throw Error("finite");return Math.max(0,Math.min(1,x));}
export function route(n){if(!Number.isSafeInteger(n)||n<0||n>=24)throw Error("contact");return CHANNELS.map((size,i)=>({group:i,mod:size,channel:n%size}));}
export function wave4(k,theta,phase=0,amp=.18,pressure=0,anchored=true){if(!Number.isInteger(k)||k<0||k>=8||![theta,phase,amp].every(Number.isFinite)||amp<0||amp>.5)throw Error("input");const scale=1-clamp(pressure),r=(1.05+k*.27)*scale,envelope=anchored?Math.sin(12*theta)**2:1,a=amp*scale*envelope,radial=anchored?Math.sin(phase):Math.sin(24*theta+phase);return [(r+a*radial)*Math.cos(theta),a*Math.sin(phase),(r+a*radial)*Math.sin(theta),a*Math.cos(phase)];}
export function contact4(k,j,phase=0,amp=.18,p=0){if(!Number.isInteger(j)||j<0||j>24)throw Error("index");return wave4(k,j*TAU/24,phase,amp,p,true);}
export function rotate4(q,a,b){if(!Array.isArray(q)||q.length!==4||![...q,a,b].every(Number.isFinite))throw Error("4d");const v=q.slice(),c=Math.cos(a),s=Math.sin(a),d=Math.cos(b),t=Math.sin(b);v[0]=c*q[0]-s*q[3];v[3]=s*q[0]+c*q[3];v[1]=d*q[1]-t*q[2];v[2]=t*q[1]+d*q[2];return v;}
export function projection(q,a=0,b=0){const v=rotate4(q,a,b),f=4/(4+Math.max(-2.5,Math.min(2.5,v[3])));return [v[0]*f,v[1]*f,v[2]*f];}
export function verify4D(){let tests=0,contacts=0,neighborLinks=0,collapses=0,maxAnchorError=0,maxNormError=0,maxSeamError=0;const samples=[];for(const p of [0,.125,.5,.875,1])for(const phase of [0,.4,1.1,2.4]){let maxDisp=0;for(let k=0;k<8;k++){const R=(1-p)*(1.05+k*.27);for(let j=0;j<=24;j++){const theta=j*TAU/24,q=contact4(k,j,phase,.2,p),base=[R*Math.cos(theta),0,R*Math.sin(theta),0],err=Math.hypot(...q.map((x,i)=>x-base[i]));if(err>1e-11)throw Error("anchor");maxAnchorError=Math.max(err,maxAnchorError);contacts++;tests++;if(j<24){const q2=contact4(k,j+1,phase,.2,p),other=wave4(k,(j+1)*TAU/24,phase,.2,p,true);if(Math.hypot(...q2.map((x,i)=>x-other[i]))>1e-11)throw Error("neighbor");neighborLinks++;tests++;}}const a=wave4(k,0,phase,.2,p,true),b=wave4(k,TAU,phase,.2,p,true),seam=Math.hypot(...a.map((x,i)=>x-b[i]));if(seam>1e-11)throw Error("seam");maxSeamError=Math.max(maxSeamError,seam);tests++;for(let j=0;j<24;j++){const mid=wave4(k,(j+.5)*TAU/24,phase,.2,p,true),q=rotate4(mid,.37,.83),err=Math.abs(Math.hypot(...mid)-Math.hypot(...q));if(err>1e-11)throw Error("rotation");maxNormError=Math.max(err,maxNormError);maxDisp=Math.max(maxDisp,Math.abs(mid[1]),Math.abs(mid[3]));tests++;}if(p===1)for(const t of [.03,.2,1.4,3.7,TAU]){if(Math.hypot(...wave4(k,t,phase,.2,p,true))!==0)throw Error("closure");collapses++;tests++;}}samples.push({p,phase,maxTransverseAmplitude:maxDisp});}if(CHANNELS.length!==6||CHANNELS.reduce((s,x)=>s+x,0)!==14)throw Error("grammar");for(let j=0;j<24;j++){if(route(j).some((q,i)=>q.channel!==j%CHANNELS[i]))throw Error("route");tests+=6;}return {tests,contacts,neighborLinks,collapses,projectionNormError:maxNormError,anchorError:maxAnchorError,seamError:maxSeamError,orbitContacts:24,gateContacts:192,channelGrammar:GRAMMAR,channelSizes:CHANNELS,channelSum:14,notFactorization:true,samples};}

// ADA-160G .dlw — reversible local phase exchange
export const CONTACT_GROUPS=Object.freeze([2,4,3,3,1,1]);
export function phaseSeed(k=0){if(!Number.isInteger(k)||k<0||k>=8)throw Error("gate");const re=Array(24).fill(0),im=Array(24).fill(0);re[(3*k)%24]=1;im[(3*k+1)%24]=.5;return {re,im};}
export function phaseEnergy(v){if(v.re.length!==24||v.im.length!==24)throw Error("shape");return v.re.reduce((a,x,i)=>a+x*x+v.im[i]*v.im[i],0);}
export function phaseTransfer(v,a,parity=0){if(!Number.isFinite(a)||![0,1].includes(parity))throw Error("parameter");const re=v.re.slice(),im=v.im.slice(),c=Math.cos(a),s=Math.sin(a);for(let j=parity;j<24+parity;j+=2){const i=j%24,k=(j+1)%24;for(const x of [re,im]){const A=x[i],B=x[k];x[i]=c*A-s*B;x[k]=s*A+c*B;}}return {re,im};}
export function phaseStep(v,a){return phaseTransfer(phaseTransfer(v,a,0),a,1);}
export function phaseWave4(k,theta,v,pressure=0,amplitude=.2){if(!Number.isFinite(theta)||!Number.isFinite(amplitude)||amplitude<0||amplitude>.5)throw Error("wave");const j=Math.floor(((theta%TAU+TAU)%TAU)*24/TAU)%24,env=Math.sin(12*theta)**2,s=1-clamp(pressure),R=(1.05+k*.27)*s,ar=v.re[j]*env*amplitude*s,ai=v.im[j]*env*amplitude*s;return [(R+ar)*Math.cos(theta),ai,(R+ar)*Math.sin(theta),ar];}
export function verifyTransfer(){let checks=0,steps=0,anchorChecks=0,closureChecks=0,maxEnergyError=0,maxRestoreError=0,localityChecks=0;
for(let k=0;k<8;k++){let v=phaseSeed(k),e=phaseEnergy(v);for(let t=0;t<40;t++){const before=v,after=phaseStep(v,.13),err=Math.abs(phaseEnergy(after)-e);maxEnergyError=Math.max(maxEnergyError,err);if(err>2e-12)throw Error("energy");checks++;steps++;const back=phaseTransfer(phaseTransfer(after,-.13,1),-.13,0),restore=Math.max(...before.re.map((x,i)=>Math.abs(x-back.re[i])),...before.im.map((x,i)=>Math.abs(x-back.im[i])));maxRestoreError=Math.max(maxRestoreError,restore);if(restore>2e-12)throw Error("inverse");checks++;v=after;for(let j=0;j<=24;j++){const th=j*TAU/24,p=phaseWave4(k,th,v,.4),R=.6*(1.05+k*.27),base=[R*Math.cos(th),0,R*Math.sin(th),0];if(Math.hypot(...p.map((x,i)=>x-base[i]))>1e-11)throw Error("contact");anchorChecks++;checks++;}const p=phaseWave4(k,0,v,.4),q=phaseWave4(k,TAU,v,.4);if(Math.hypot(...p.map((x,i)=>x-q[i]))>1e-11)throw Error("seam");closureChecks++;checks++;if(Math.hypot(...phaseWave4(k,.137,v,1))!==0)throw Error("closure");checks++;}}
const probe=phaseSeed(0),m=phaseTransfer(probe,.2,0);for(let i=0;i<24;i++){if(i!==0&&i!==1&&m.re[i]!==probe.re[i])throw Error("nonlocal");localityChecks++;checks++;}
for(const i of [0,1,2,3,7,13,23]){if(route(i).some((c,j)=>c.mod!==CONTACT_GROUPS[j]))throw Error("route");checks++;}
return {checks,steps,anchorChecks,closureChecks,localityChecks,maxEnergyError,maxRestoreError,perGateSignalEnergy:1.25,gates:8,contactsPerGate:24,groups:CONTACT_GROUPS,model:"norm-preserving reversible nearest-neighbor signal mixing, not physical energy conservation"};}

// ADA-160H .dlw — regulated resonance, selective transfer, local veto.

export function contactInequality(v){return v.re.reduce((s,x,i)=>{const e=x*x+v.im[i]*v.im[i];return s+e*e;},0);}
export function selectivePass(v,angle,parity=0,threshold=1e-7){if(!Number.isFinite(angle)||angle<0||angle>Math.PI/2||![0,1].includes(parity)||!Number.isFinite(threshold)||threshold<0)throw Error("parameter");
const re=v.re.slice(),im=v.im.slice(),decisions=[],co=Math.cos(angle),si=Math.sin(angle);
for(let j=parity;j<24+parity;j+=2){const a=j%24,b=(j+1)%24,ar=re[a],ai=im[a],br=re[b],bi=im[b],initial=(ar*ar+ai*ai-br*br-bi*bi)**2;let best={score:initial,angle:0,reduction:0};
for(const sign of [-1,1]){const sn=si*sign,ra=co*ar-sn*br,ia=co*ai-sn*bi,rb=sn*ar+co*br,ib=sn*ai+co*bi,score=(ra*ra+ia*ia-rb*rb-ib*ib)**2;if(score<best.score-threshold)best={score,angle:sign*angle,reduction:initial-score};}
if(best.angle){const c=Math.cos(best.angle),sn=Math.sin(best.angle);re[a]=c*ar-sn*br;im[a]=c*ai-sn*bi;re[b]=sn*ar+c*br;im[b]=sn*ai+c*bi;}
decisions.push({a,b,angle:best.angle,accepted:!!best.angle,reduction:best.reduction});}
return {state:{re,im},decisions};}
export function selectiveStep(v,angle,threshold=1e-7){const a=selectivePass(v,angle,0,threshold),b=selectivePass(a.state,angle,1,threshold);return {state:b.state,decisions:[...a.decisions,...b.decisions],accepted:a.decisions.filter(x=>x.accepted).length+b.decisions.filter(x=>x.accepted).length};}
export function selectiveUndo(v,decisions){const s={re:v.re.slice(),im:v.im.slice()};for(let j=decisions.length-1;j>=0;j--){const d=decisions[j];if(!d.accepted)continue;const c=Math.cos(d.angle),sn=Math.sin(d.angle);for(const arr of [s.re,s.im]){const a=arr[d.a],b=arr[d.b];arr[d.a]=c*a+sn*b;arr[d.b]=-sn*a+c*b;}}return s;}
export function verifySelective(){let checks=0,accepted=0,skipped=0,maxEnergyError=0,maxUndoError=0,maxInequalityIncrease=0,contactChecks=0,pressureChecks=0;const rows=[];
for(const angle of [.05,.13,.3,.6])for(let k=0;k<8;k++){let selective=phaseSeed(k),continuous=phaseSeed(k),energy=phaseEnergy(selective),initialScore=contactInequality(selective),recordAccepted=0;
for(let t=0;t<100;t++){const before=selective,beforeScore=contactInequality(before),step=selectiveStep(before,angle);selective=step.state;continuous=phaseStep(continuous,angle);
const err=Math.abs(phaseEnergy(selective)-energy),rise=contactInequality(selective)-beforeScore;if(err>1e-11||rise>1e-10)throw Error("invariant");checks+=2;maxEnergyError=Math.max(maxEnergyError,err);maxInequalityIncrease=Math.max(maxInequalityIncrease,rise);
const restored=selectiveUndo(selective,step.decisions),undoError=Math.max(...restored.re.map((x,i)=>Math.abs(x-before.re[i])),...restored.im.map((x,i)=>Math.abs(x-before.im[i])));if(undoError>1e-11)throw Error("undo");maxUndoError=Math.max(maxUndoError,undoError);checks++;
accepted+=step.accepted;recordAccepted+=step.accepted;skipped+=24-step.accepted;
if(t%10===0){for(let j=0;j<24;j++){const th=j*TAU/24,v=phaseWave4(k,th,selective,.5),r=.5*(1.05+k*.27);if(Math.hypot(v[0]-r*Math.cos(th),v[1],v[2]-r*Math.sin(th),v[3])>1e-10)throw Error("anchor");checks++;contactChecks++;}if(Math.hypot(...phaseWave4(k,.123,selective,1))!==0)throw Error("closure");pressureChecks++;checks++;}}
rows.push({angle,gate:k,accepted:recordAccepted,initialInequality:initialScore,selectiveInequality:contactInequality(selective),continuousInequality:contactInequality(continuous)});}
if(!accepted||!skipped)throw Error("no regulation");return {checks,accepted,skipped,contactChecks,pressureChecks,maxEnergyError,maxUndoError,maxInequalityIncrease,rows,criterion:"Local neighboring SO(2) rotations accepted only when squared node-energy imbalance decreases, preserving global L2 norm."};}

 // ADA-160I .dlw — append-only local phase memory; evidence can bias direction only if candidate is currently useful.
export function memorySeed(k=0){return {signal:phaseSeed(k),history:[],epoch:0,accepted:0,vetoed:0};}
export function memoryStep(s,angle=.13,threshold=1e-7,weight=.35,depth=8){
if(!Number.isFinite(angle)||angle<0||angle>Math.PI/2||!Number.isFinite(threshold)||threshold<0||!Number.isFinite(weight)||weight<0||weight>1||!Number.isInteger(depth)||depth<1||depth>100)throw Error("parameter");
const signal={re:s.signal.re.slice(),im:s.signal.im.slice()},history=s.history.slice(),ledger=[],decisions=[];let accepted=0;
for(const parity of [0,1])for(let j=parity;j<24+parity;j+=2){const a=j%24,b=(j+1)%24,ar=signal.re[a],ai=signal.im[a],br=signal.re[b],bi=signal.im[b],initial=(ar*ar+ai*ai-br*br-bi*bi)**2,key=a+"-"+b;
const candidates=[-1,1].map(dir=>{const t=dir*angle,c=Math.cos(t),si=Math.sin(t),ra=c*ar-si*br,ia=c*ai-si*bi,rb=si*ar+c*br,ib=si*ai+c*bi,gain=initial-(ra*ra+ia*ia-rb*rb-ib*ib)**2;
const recent=history.filter(h=>h.key===key&&h.dir===dir).slice(-depth),prior=recent.length?recent.reduce((x,h)=>x+h.gain,0)/recent.length:0;return {dir,gain,prior,score:gain+weight*prior};});
const eligible=candidates.filter(x=>x.gain>threshold);eligible.sort((x,y)=>y.score-x.score||y.gain-x.gain||x.dir-y.dir);
const winner=eligible[0]??null,dir=winner?.dir??0,theta=dir*angle;
if(winner){const c=Math.cos(theta),si=Math.sin(theta);signal.re[a]=c*ar-si*br;signal.im[a]=c*ai-si*bi;signal.re[b]=si*ar+c*br;signal.im[b]=si*ai+c*bi;accepted++;}
const event={tick:s.epoch+1,parity,key,a,b,dir,gain:winner?.gain??0,prior:winner?.prior??0,decision:dir?"accepted":"vetoed"};ledger.push(event);history.push(event);decisions.push({a,b,angle:theta,accepted:!!dir});}
return {signal,history,ledger,decisions,epoch:s.epoch+1,accepted:s.accepted+accepted,vetoed:s.vetoed+24-accepted};}
export function memoryUndo(signal,decisions){return selectiveUndo(signal,decisions);}
export function verifyMemory(){let checks=0,accepted=0,vetoed=0,maxNormError=0,maxUndoError=0,maxImbalanceRise=0,anchorChecks=0;const rows=[];
for(const angle of [.05,.13,.3,.6])for(let k=0;k<8;k++){let m=memorySeed(k),baseline=phaseSeed(k),original=phaseEnergy(m.signal);for(let t=0;t<100;t++){const before=m.signal,prevScore=contactInequality(before),step=memoryStep(m,angle,1e-7,.35,8),normError=Math.abs(phaseEnergy(step.signal)-original),imbalanceRise=contactInequality(step.signal)-prevScore;if(normError>1e-11||imbalanceRise>1e-10)throw Error("invariants");checks+=2;maxNormError=Math.max(maxNormError,normError);maxImbalanceRise=Math.max(maxImbalanceRise,imbalanceRise);
const old=memoryUndo(step.signal,step.decisions),err=Math.max(...old.re.map((x,i)=>Math.abs(x-before.re[i])),...old.im.map((x,i)=>Math.abs(x-before.im[i])));if(err>1e-11)throw Error("undo");maxUndoError=Math.max(maxUndoError,err);checks++;
if(step.ledger.length!==24||step.ledger.some(e=>e.decision==="accepted"&&e.gain<=1e-7)||step.history.length!==(t+1)*24||step.ledger.some(e=>e.tick!==t+1))throw Error("evidence");checks++;
accepted+=step.ledger.filter(e=>e.decision==="accepted").length;vetoed+=step.ledger.filter(e=>e.decision==="vetoed").length;
baseline=selectiveStep(baseline,angle).state;m=step;
if(t%20===0){for(let j=0;j<24;j++){const theta=j*TAU/24,v=phaseWave4(k,theta,m.signal,.3),r=.7*(1.05+k*.27);if(Math.hypot(v[0]-r*Math.cos(theta),v[1],v[2]-r*Math.sin(theta),v[3])>1e-10)throw Error("anchor");checks++;anchorChecks++;}}}
rows.push({angle,gate:k,accepted:m.accepted,vetoed:m.vetoed,finalInequality:contactInequality(m.signal),withoutMemory:contactInequality(baseline),observations:m.history.length});}
if(!accepted||!vetoed)throw Error("decision types");return {checks,accepted,vetoed,maxNormError,maxUndoError,maxImbalanceRise,anchorChecks,rows,historyPerRun:2400,rule:"Append-only observed local gains; recent 8 directed pair observations influence ranking but cannot override a presently harmful candidate."};}

 // ADA-160J .dlw — forecasts are written before candidate validation; no simulated advantage assumed.
export function forecastSeed(k=0){return {signal:phaseSeed(k),history:[],tick:0,forecasted:0,error:0,accepted:0,vetoed:0};}
export function forecastStep(s,angle=.13,threshold=1e-7,historyWeight=.25){if(!Number.isFinite(angle)||angle<0||angle>Math.PI/2||!Number.isFinite(threshold)||threshold<0||!Number.isFinite(historyWeight)||historyWeight<0||historyWeight>1)throw Error("parameter");
const re=s.signal.re.slice(),im=s.signal.im.slice(),events=[],decisions=[];let forecasts=0,error=0,accepted=0,guided=0;
for(const parity of [0,1])for(let j=parity;j<24+parity;j+=2){const a=j%24,b=(j+1)%24,ar=re[a],ai=im[a],br=re[b],bi=im[b],key=a+"-"+b,initial=(ar*ar+ai*ai-br*br-bi*bi)**2;
const options=[-1,1].map(dir=>{const recent=s.history.filter(x=>x.key===key&&x.dir===dir&&x.angle===angle).slice(-8),forecast=recent.length?recent.reduce((sum,x)=>sum+x.actual,0)/recent.length:null;const c=Math.cos(angle),sn=Math.sin(dir*angle),ra=c*ar-sn*br,ia=c*ai-sn*bi,rb=sn*ar+c*br,ib=sn*ai+c*bi,actual=initial-(ra*ra+ia*ia-rb*rb-ib*ib)**2;return {dir,forecast,actual,samples:recent.length};});
const useful=options.filter(x=>x.actual>threshold),best=useful.slice().sort((x,y)=>y.actual-x.actual)[0],chosen=useful.slice().sort((x,y)=>y.actual+historyWeight*(y.forecast??0)-x.actual-historyWeight*(x.forecast??0))[0];
if(chosen){const c=Math.cos(angle),sn=Math.sin(chosen.dir*angle);re[a]=c*ar-sn*br;im[a]=c*ai-sn*bi;re[b]=sn*ar+c*br;im[b]=sn*ai+c*bi;accepted++;if(chosen.dir!==best.dir)guided++;}
for(const x of options){if(x.forecast!==null){forecasts++;error+=Math.abs(x.forecast-x.actual);}events.push({tick:s.tick+1,key,a,b,parity,dir:x.dir,angle,forecast:x.forecast,actual:x.actual,samples:x.samples,chosen:x.dir===chosen?.dir});}
decisions.push({a,b,angle:(chosen?.dir??0)*angle,accepted:!!chosen});
}
return {signal:{re,im},history:s.history.concat(events),events,decisions,tick:s.tick+1,forecasted:s.forecasted+forecasts,error:s.error+error,accepted:s.accepted+accepted,vetoed:s.vetoed+24-accepted,historyGuided:(s.historyGuided??0)+guided};
}
export function verifyForecast(){let checks=0,forecasts=0,accepted=0,vetoed=0,guided=0,anchorChecks=0,maxNormError=0,maxUndoError=0;const rows=[];
for(const angle of [.05,.13,.3,.6])for(let k=0;k<8;k++){let v=forecastSeed(k),baseline=phaseSeed(k),energy=phaseEnergy(v.signal);
for(let t=0;t<80;t++){const previous=v.signal,prior=contactInequality(previous),n=forecastStep(v,angle),norm=Math.abs(phaseEnergy(n.signal)-energy),rise=contactInequality(n.signal)-prior;if(norm>1e-11||rise>1e-10)throw Error("invariant");maxNormError=Math.max(maxNormError,norm);checks+=2;
const restored=selectiveUndo(n.signal,n.decisions),undo=Math.max(...restored.re.map((x,i)=>Math.abs(x-previous.re[i])),...restored.im.map((x,i)=>Math.abs(x-previous.im[i])));if(undo>1e-11)throw Error("undo");maxUndoError=Math.max(maxUndoError,undo);checks++;
if(n.events.length!==48||n.history.length!==(t+1)*48||n.events.some(x=>x.tick!==t+1||x.chosen&&x.actual<=1e-7||x.forecast!==null&&x.samples===0))throw Error("ledger");checks++;
forecasts+=n.forecasted-v.forecasted;accepted+=n.accepted-v.accepted;vetoed+=n.vetoed-v.vetoed;guided+=n.historyGuided-(v.historyGuided??0);baseline=selectiveStep(baseline,angle).state;v=n;
if(t%20===0)for(let j=0;j<24;j++){const theta=j*TAU/24,q=phaseWave4(k,theta,v.signal,.4),r=.6*(1.05+k*.27);if(Math.hypot(q[0]-r*Math.cos(theta),q[1],q[2]-r*Math.sin(theta),q[3])>1e-10)throw Error("anchor");anchorChecks++;checks++;}}
rows.push({angle,gate:k,forecasts:v.forecasted,mae:v.error/v.forecasted,forecastedImbalance:contactInequality(v.signal),baselineImbalance:contactInequality(baseline)});}
if(!forecasts||!accepted||!vetoed)throw Error("coverage");return {checks,forecasts,accepted,vetoed,guided,anchorChecks,maxNormError,maxUndoError,rows,interpretation:"Forecast learned from last 8 same-angle directed-pair counterfactual outcomes; current local effect verified before transfer. Benchmarked against 160H, no gain demonstrated."};}

 // ADA-160K .dlw — causal rolling calibration with immutable raw forecast observations.
export function calibrationSeed(k=0){return {signal:phaseSeed(k),history:[],tick:0,rawAE:0,calAE:0,predictions:0,accepted:0,vetoed:0};}
export function calibratedStep(s,angle=.13,threshold=1e-7,alpha=.35,enabled=true){
if(!Number.isFinite(angle)||angle<0||angle>Math.PI/2||!Number.isFinite(threshold)||threshold<0||!Number.isFinite(alpha)||alpha<0||alpha>1)throw Error("parameter");
const re=s.signal.re.slice(),im=s.signal.im.slice(),events=[],decisions=[];let rawAE=0,calAE=0,predictions=0,accepted=0;
for(const parity of [0,1])for(let j=parity;j<24+parity;j+=2){const a=j%24,b=(j+1)%24,ar=re[a],ai=im[a],br=re[b],bi=im[b],initial=(ar*ar+ai*ai-br*br-bi*bi)**2,key=a+"-"+b;
const candidates=[-1,1].map(dir=>{const past=s.history.filter(h=>h.key===key&&h.dir===dir&&h.angle===angle).slice(-8),raw=past.length?past.reduce((sum,h)=>sum+h.observed,0)/past.length:null;
const residual=past.length?past.reduce((sum,h)=>sum+(h.observed-h.raw),0)/past.length:0,cal=raw===null?null:raw+(enabled?alpha*residual:0);
const c=Math.cos(angle),si=Math.sin(dir*angle),ra=c*ar-si*br,ia=c*ai-si*bi,rb=si*ar+c*br,ib=si*ai+c*bi,gain=initial-(ra*ra+ia*ia-rb*rb-ib*ib)**2;return {dir,raw,cal,gain,samples:past.length};});
for(const c of candidates)if(c.raw!==null){rawAE+=Math.abs(c.raw-c.gain);calAE+=Math.abs(c.cal-c.gain);predictions++;}
const eligible=candidates.filter(x=>x.gain>threshold).sort((x,y)=>y.gain-x.gain),selected=eligible[0]??null;
if(selected){const c=Math.cos(angle),si=Math.sin(selected.dir*angle);re[a]=c*ar-si*br;im[a]=c*ai-si*bi;re[b]=si*ar+c*br;im[b]=si*ai+c*bi;accepted++;}
for(const c of candidates)events.push({tick:s.tick+1,key,a,b,parity,angle,dir:c.dir,raw:c.raw,calibrated:c.cal,observed:c.gain,samples:c.samples,selected:selected?.dir===c.dir});
decisions.push({a,b,angle:(selected?.dir??0)*angle,accepted:!!selected});}
return {signal:{re,im},history:s.history.concat(events),events,decisions,tick:s.tick+1,rawAE:s.rawAE+rawAE,calAE:s.calAE+calAE,predictions:s.predictions+predictions,accepted:s.accepted+accepted,vetoed:s.vetoed+24-accepted};
}
export function verifyCalibration(){let checks=0,forecasts=0,maxNormError=0,maxUndoError=0,anchors=0,rows=[];for(const angle of [.05,.13,.3,.6])for(let k=0;k<8;k++){let s=calibrationSeed(k),energy=phaseEnergy(s.signal);
for(let t=0;t<80;t++){const before=s.signal,score=contactInequality(before),next=calibratedStep(s,angle,1e-7,.35,true),normError=Math.abs(phaseEnergy(next.signal)-energy),rise=contactInequality(next.signal)-score;if(normError>1e-11||rise>1e-10)throw Error("invariant");maxNormError=Math.max(normError,maxNormError);checks+=2;
const restored=selectiveUndo(next.signal,next.decisions),undo=Math.max(...restored.re.map((x,i)=>Math.abs(x-before.re[i])),...restored.im.map((x,i)=>Math.abs(x-before.im[i])));if(undo>1e-11)throw Error("inverse");maxUndoError=Math.max(undo,maxUndoError);checks++;
if(next.events.length!==48||next.history.length!==(t+1)*48||next.events.some(x=>x.tick!==t+1||x.raw===null&&x.calibrated!==null||x.selected&&x.observed<=1e-7))throw Error("event provenance");checks++;
if(t%20===0)for(let j=0;j<24;j++){const theta=j*TAU/24,q=phaseWave4(k,theta,next.signal,.4),r=.6*(1.05+k*.27);if(Math.hypot(q[0]-r*Math.cos(theta),q[1],q[2]-r*Math.sin(theta),q[3])>1e-10)throw Error("anchor");anchors++;checks++;}
s=next;}forecasts+=s.predictions;rows.push({angle,gate:k,forecasts:s.predictions,rawMAE:s.rawAE/s.predictions,calibratedMAE:s.calAE/s.predictions,improvement:(s.rawAE-s.calAE)/s.predictions,accepted:s.accepted});}
if(forecasts<1)throw Error("no forecasts");return {checks,forecasts,anchors,maxNormError,maxUndoError,rows,method:"Causal rolling-8 mean baseline with residual-bias shrinkage correction; each candidate forecast evaluated using only prior records. The transfer decision remains constrained by current local improvement. Calibration does not affect actions in this bound."};}

export const ARMS=[0,.35,1];
export function adaptiveSeed(k=0){return {signal:phaseSeed(k),history:[],tick:0,losses:[0,0,0],choices:[0,0,0],n:0};}
export function adaptiveStep(s,angle=.13){
const re=s.signal.re.slice(),im=s.signal.im.slice(),events=[],decisions=[],losses=s.losses.slice(),choices=s.choices.slice();let n=s.n;
for(const parity of [0,1])for(let j=parity;j<24+parity;j+=2){
const a=j%24,b=(j+1)%24,key=a+"-"+b,ar=re[a],ai=im[a],br=re[b],bi=im[b],start=(ar*ar+ai*ai-br*br-bi*bi)**2;
const candidates=[-1,1].map(dir=>{
const hist=s.history.filter(h=>h.key===key&&h.dir===dir&&h.angle===angle).slice(-8),raw=hist.length?hist.reduce((v,h)=>v+h.actual,0)/hist.length:null;
const bias=hist.length?hist.reduce((v,h)=>v+h.actual-(h.raw??h.actual),0)/hist.length:0;
const scores=ARMS.map(alpha=>hist.length>=3?hist.filter(h=>h.raw!==null).reduce((v,h)=>v+Math.abs(h.raw+alpha*h.bias-h.actual),0)/Math.max(1,hist.filter(h=>h.raw!==null).length):Infinity);
let arm=0;for(let i=1;i<3;i++)if(scores[i]<scores[arm]-1e-12)arm=i;
const c=Math.cos(angle),t=Math.sin(angle*dir),ra=c*ar-t*br,ia=c*ai-t*bi,rb=t*ar+c*br,ib=t*ai+c*bi,actual=start-(ra*ra+ia*ia-rb*rb-ib*ib)**2;
if(raw!==null){n++;choices[arm]++;for(let i=0;i<3;i++)losses[i]+=Math.abs(raw+ARMS[i]*bias-actual);}
return {dir,raw,bias,arm,actual};
});
const chosen=candidates.filter(x=>x.actual>1e-7).sort((x,y)=>y.actual-x.actual)[0];
if(chosen){const c=Math.cos(angle),t=Math.sin(angle*chosen.dir);re[a]=c*ar-t*br;im[a]=c*ai-t*bi;re[b]=t*ar+c*br;im[b]=t*ai+c*bi;}
for(const x of candidates)events.push({tick:s.tick+1,key,a,b,angle,dir:x.dir,raw:x.raw,bias:x.bias,alpha:ARMS[x.arm],adapted:x.raw===null?null:x.raw+ARMS[x.arm]*x.bias,actual:x.actual,selected:x.dir===chosen?.dir});
decisions.push({a,b,angle:(chosen?.dir??0)*angle,accepted:!!chosen});
}
return {signal:{re,im},history:s.history.concat(events),events,decisions,tick:s.tick+1,losses,choices,n};
}
export function verifyAdaptive(){let checks=0,forecasts=0,anchors=0,maxNormError=0,maxUndoError=0,rows=[];
for(const angle of [.05,.13,.3,.6])for(let k=0;k<8;k++){let v=adaptiveSeed(k),energy=phaseEnergy(v.signal);
for(let t=0;t<80;t++){const before=v.signal,previous=contactInequality(before),s=adaptiveStep(v,angle),e=Math.abs(phaseEnergy(s.signal)-energy);if(e>1e-11||contactInequality(s.signal)>previous+1e-10)throw Error("signal norm or inequality");maxNormError=Math.max(maxNormError,e);checks+=2;
const restored=selectiveUndo(s.signal,s.decisions),err=Math.max(...restored.re.map((x,i)=>Math.abs(x-before.re[i])),...restored.im.map((x,i)=>Math.abs(x-before.im[i])));if(err>1e-11)throw Error("reverse");maxUndoError=Math.max(maxUndoError,err);checks++;
if(s.events.length!==48||s.history.length!==48*(t+1)||s.choices.reduce((a,b)=>a+b,0)!==s.n||s.events.some(x=>x.selected&&x.actual<=1e-7))throw Error("ledger");checks++;v=s;
if(t%20===0)for(let j=0;j<24;j++){const th=j*TAU/24,q=phaseWave4(k,th,v.signal,.4),r=.6*(1.05+k*.27);if(Math.hypot(q[0]-r*Math.cos(th),q[1],q[2]-r*Math.sin(th),q[3])>1e-10)throw Error("anchor");checks++;anchors++;}}
forecasts+=v.n;rows.push({angle,gate:k,forecasts:v.n,rawMAE:v.losses[0]/v.n,fixedMAE:v.losses[1]/v.n,fullMAE:v.losses[2]/v.n,choices:v.choices,finalInequality:contactInequality(v.signal)});}
return {checks,forecasts,anchors,maxNormError,maxUndoError,rows,rule:"Causal contact-specific selection of calibration alpha 0, .35 or 1 by prior rolling loss; current outcome is never used to select its own alpha; original evidence remains append-only."};}
