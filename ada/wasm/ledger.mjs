// ADA-286N .dlw — local append-only observation ledger.
const ZERO="0".repeat(64);
const hash=async value=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(JSON.stringify(value)))),b=>b.toString(16).padStart(2,"0")).join("");
const request=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)});
const done=t=>new Promise((ok,no)=>{t.oncomplete=ok;t.onabort=t.onerror=()=>no(t.error||Error("transaction aborted"))});
export async function openLedger(kernel){
 const db=await request(Object.assign(indexedDB.open("ada-286n-"+kernel.sha256,1),{onupgradeneeded:e=>e.target.result.createObjectStore("frames",{keyPath:"generation"})}));
 const read=async()=>request(db.transaction("frames").objectStore("frames").getAll());
 async function verify(){
  const records=await read();let previous=ZERO;
  for(let i=0;i<records.length;i++){
   const {digest,...body}=records[i];
   if(body.generation!==i||body.previous!==previous||body.source!==kernel.source||body.binary!==kernel.sha256||await hash(body)!==digest)throw Error("Ledger chain rejected");
   previous=digest;
  }
  return records;
 }
 async function append(frame){
  const records=await verify(),last=records.at(-1);
  if(frame.generation!==records.length)throw Error("Nonsequential observation");
  const body={generation:frame.generation,clock:frame.clock,pumps:frame.pumps,source:kernel.source,binary:kernel.sha256,previous:last?.digest??ZERO};
  const digest=await hash(body);
  const t=db.transaction("frames","readwrite"),completion=done(t);
  t.objectStore("frames").add({...body,digest});
  await completion;
  return digest;
 }
 return Object.freeze({verify,append,close:()=>db.close()});
}
