// ADA-297N .dlw — atomic append, complete native replay, source-isolated recovery.
const ZERO="0".repeat(64);
const hash=async body=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(JSON.stringify(body)))),b=>b.toString(16).padStart(2,"0")).join("");
const request=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)});
const done=t=>new Promise((ok,no)=>{t.oncomplete=ok;t.onabort=t.onerror=()=>no(t.error||Error("transaction aborted"))});
export async function openLedger(kernel){
 if(!/^[a-f0-9]{40}$/.test(kernel.source)||!/^[a-f0-9]{64}$/.test(kernel.sha256))throw Error("Invalid ledger ancestry");
 const e=kernel.exports;
 function validate(frame,g){
  if(g>24000||frame.generation!==g)throw Error("Invalid generation");
  const clock=Array.from({length:6},(_,i)=>e.ada_clock_field(g,i)>>>0);
  const pumps=Array.from({length:3},(_,i)=>Array.from({length:5},(_,j)=>e.ada_pump_field(g,i,j)));
  if(clock.includes(4294967295)||pumps.flat().some(x=>!Number.isFinite(x))||JSON.stringify(clock)!==JSON.stringify(frame.clock)||JSON.stringify(pumps)!==JSON.stringify(frame.pumps))throw Error("Native observation mismatch");
 }
 const name="ada-297n-"+kernel.source+"-"+kernel.sha256;
 const opening=indexedDB.open(name,1);
 const db=await new Promise((ok,no)=>{opening.onupgradeneeded=()=>opening.result.createObjectStore("frames",{keyPath:"generation"});opening.onblocked=()=>no(Error("Ledger open blocked"));opening.onerror=()=>no(opening.error);opening.onsuccess=()=>ok(opening.result);});
 db.onversionchange=()=>db.close();
 const read=()=>request(db.transaction("frames").objectStore("frames").getAll());
 async function verify(){
  const rows=await read();let previous=ZERO;
  for(let i=0;i<rows.length;i++){
   const {digest,...body}=rows[i];validate(body,i);
   if(body.previous!==previous||body.source!==kernel.source||body.binary!==kernel.sha256||await hash(body)!==digest)throw Error("Ledger chain rejected");
   previous=digest;
  }
  return rows;
 }
 async function append(frame){
  const rows=await verify(),last=rows.at(-1);validate(frame,rows.length);
  const body={generation:frame.generation,clock:frame.clock,pumps:frame.pumps,source:kernel.source,binary:kernel.sha256,previous:last?.digest??ZERO};
  const digest=await hash(body);
  const t=db.transaction("frames","readwrite"),completion=done(t),store=t.objectStore("frames");
  // Both reads and add execute within the same serialized transaction.
  const cursor=store.openCursor(null,"prev");
  cursor.onsuccess=()=>{const current=cursor.result?.value;if((current?.generation??-1)!==rows.length-1||(current?.digest??ZERO)!==body.previous){t.abort();return;}store.add({...body,digest});};
  await completion;
  return digest;
 }
 return Object.freeze({verify,append,close:()=>db.close(),name});
}
