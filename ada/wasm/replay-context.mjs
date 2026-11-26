// ADA-299N .dlw — replay recorded ancestry using native addresses.
export function replayContext(kernel, context, epoch){
 const e=kernel.exports, size=e.ada_epoch_size()>>>0, count=e.ada_memory_window()>>>0;
 if(!Number.isSafeInteger(epoch)||epoch<0||epoch>Math.floor(4294967294/size))throw Error("Invalid epoch");
 if(size!==24||count!==8)throw Error("Inheritance invariants rejected");
 const start=epoch*size;
 if(start>=context.length)throw Error("Epoch not observed");
 if(epoch===0)return Object.freeze({epoch,ancestor:null,opening:[],sealed:context.length>=size});
 if(!Array.isArray(context.opening)||context.opening.length!==count)throw Error('Incomplete opening context');
 const opening=[];
 for(let i=0;i<count;i++){
  const address=e.ada_inherited_generation(epoch,i)>>>0;
  const expected=start-count+i;
  const r=context.opening[i];
  if(address!==expected||!r||r.generation!==address||r.source!==kernel.source||r.binary!==kernel.sha256||!/^[a-f0-9]{64}$/.test(r.digest))throw Error("Inherited address or ancestry rejected");
  const clock=Array.from({length:6},(_,f)=>e.ada_clock_field(address,f)>>>0);
  const pumps=Array.from({length:3},(_,p)=>Array.from({length:5},(_,f)=>e.ada_pump_field(address,p,f)));
  if(pumps.flat().some(x=>!Number.isFinite(x))||JSON.stringify(clock)!==JSON.stringify(r.clock)||JSON.stringify(pumps)!==JSON.stringify(r.pumps))throw Error("Inherited native observation mismatch");
  opening.push({generation:address,digest:r.digest,pumps:r.pumps});
 }
 return Object.freeze({epoch,ancestor:epoch-1,opening,sealed:context.length>=start+size});
}
