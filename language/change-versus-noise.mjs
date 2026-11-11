// QG-058 — fixed-window change screening with familywise alpha spending.
// Alerts are evidence of incompatibility with a stationary independent Bernoulli
// model, NOT proof of a physical regime change. Observations precede conclusions.
export const VERSION='QG-058';
export const DEFAULT=Object.freeze({baselineSize:20,batchSize:20,alpha:.05});
const copy=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const binary=x=>x===0||x===1;
function config(options){
 const c={...DEFAULT,...options};
 if(!Number.isSafeInteger(c.baselineSize)||c.baselineSize<10||c.baselineSize>1000||
 !Number.isSafeInteger(c.batchSize)||c.batchSize<10||c.batchSize>1000||
 !Number.isFinite(c.alpha)||c.alpha<=0||c.alpha>=1)throw Error('Invalid change-screening configuration');
 return c;
}
export function checkpoint(baseline,monitor,alpha,batchIndex){
 if(!Array.isArray(baseline)||!Array.isArray(monitor)||!baseline.length||!monitor.length||
  !baseline.every(binary)||!monitor.every(binary)||!Number.isSafeInteger(batchIndex)||batchIndex<1||
  !Number.isFinite(alpha)||alpha<=0||alpha>=1)throw Error('Invalid checkpoint evidence');
 // Sum_{k=1}^infinity alpha/(k(k+1)) = alpha, preserving a
 // familywise false-alert bound by a union bound across fixed checkpoints.
 const allocatedAlpha=alpha/(batchIndex*(batchIndex+1));
 const baselineRate=baseline.reduce((a,b)=>a+b,0)/baseline.length;
 const monitorRate=monitor.reduce((a,b)=>a+b,0)/monitor.length;
 const threshold=Math.sqrt(Math.log(4/allocatedAlpha)/(2*baseline.length))
  +Math.sqrt(Math.log(4/allocatedAlpha)/(2*monitor.length));
 const delta=monitorRate-baselineRate;
 return {batchIndex,allocatedAlpha,baselineRate,monitorRate,delta,
  threshold,alert:Math.abs(delta)>threshold,
  interpretation:Math.abs(delta)>threshold?'investigate_shift':'no_detected_shift'};
}
export function start(options={}){
 return {version:VERSION,config:config(options),events:[],status:'baseline',
  baselineCount:0,monitorCount:0,checkpoints:[]};
}
function calculate(events,c){
 const base=[],checkpoints=[],monitor=[];
 let status='baseline';
 for(const e of events){
  if(!binary(e.outcome))throw Error('Nonbinary event');
  if(base.length<c.baselineSize){
   base.push(e.outcome);
   status=base.length===c.baselineSize?'monitoring':'baseline';
  }else{
   if(status==='review')throw Error('Events after review alert');
   monitor.push(e.outcome);status='monitoring';
   if(monitor.length===c.batchSize){
    const result=checkpoint(base,monitor,c.alpha,checkpoints.length+1);
    checkpoints.push(result);
    status=result.alert?'review':'monitoring';
    monitor.length=0;
   }
  }
 }
 return {status,baselineCount:base.length,monitorCount:monitor.length,checkpoints};
}
export function verify(record){
 if(!record||record.version!==VERSION||!Array.isArray(record.events)||!Array.isArray(record.checkpoints))
 throw Error('Malformed change ledger');
 const c=config(record.config);
 const history=[];
 for(let i=0;i<record.events.length;i++){
  const e=record.events[i];
  if(!e||e.index!==i||!binary(e.outcome))throw Error('Invalid event index or outcome');
  history.push({index:i,outcome:e.outcome});
  const current=calculate(history,c);
  if(!eq(e.snapshot,current))throw Error('Event snapshot mismatch at '+i);
 }
 const expected=calculate(history,c);
 if(record.status!==expected.status||record.baselineCount!==expected.baselineCount||
 record.monitorCount!==expected.monitorCount||!eq(record.checkpoints,expected.checkpoints))
 throw Error('Final checkpoint replay mismatch');
 return {valid:true,...expected,events:record.events.length};
}
export function append(record,outcome){
 verify(record);
 if(!binary(outcome))throw Error('Outcome must be 0 or 1');
 if(record.status==='review')throw Error('Review alert is a stopping boundary');
 const index=record.events.length;
 const inputs=record.events.map(e=>({index:e.index,outcome:e.outcome}));
 inputs.push({index,outcome});
 const state=calculate(inputs,config(record.config));
 return {...copy(record),events:[...copy(record.events),{index,outcome,snapshot:copy(state)}],
  status:state.status,baselineCount:state.baselineCount,monitorCount:state.monitorCount,
  checkpoints:copy(state.checkpoints)};
}
export function run(outcomes,options={}){
 if(!Array.isArray(outcomes))throw Error('Outcome sequence must be an array');
 let ledger=start(options);
 for(const outcome of outcomes)ledger=append(ledger,outcome);
 return ledger;
}
export function demo(kind='shift'){
 const baseline=[...Array(20).fill(0)];
 const future=kind==='shift'?Array(20).fill(1):
  kind==='stable'?Array(20).fill(0):null;
 if(!future)throw Error('Unknown demo fixture');
 return run([...baseline,...future]);
}
