import {createHash} from 'node:crypto';
import {performance} from 'node:perf_hooks';
const hash=x=>createHash('sha256').update(JSON.stringify(x)).digest('hex');
const zero='0'.repeat(64), source='a'.repeat(40),binary='b'.repeat(64);
function frame(g,previous){return {generation:g,clock:[g,Math.floor(g/24),g%24,g%8,g%360,Math.floor(g%360/120)],pumps:Array.from({length:3},(_,i)=>[(g+i*120)%360,1/3,0,0,0]),source,binary,previous};}
function audit(rows){let prev=zero;for(const [i,r] of rows.entries()){const {digest,...body}=r;if(body.generation!==i||body.previous!==prev||hash(body)!==digest)throw Error('chain');prev=digest;}return prev;}
const results=[];for(const n of [24,240,2400,24000]){const rows=[];for(let g=0;g<n;g++){const body=frame(g,rows.at(-1)?.digest??zero);rows.push({...body,digest:hash(body)});}const full=[],inc=[];for(let i=0;i<7;i++){let t=performance.now();const head=audit(rows);const a=hash(frame(n,head));full.push(performance.now()-t);t=performance.now();const b=hash(frame(n,rows.at(-1).digest));inc.push(performance.now()-t);if(a!==b)throw Error('parity');}const med=x=>x.sort((a,b)=>a-b)[3];results.push({n,full_ms:med(full),incremental_ms:med(inc),digest_match: true});}console.log(JSON.stringify({node:process.version,scope:'in-memory synthetic SHA-256 chain; not IndexedDB or Rust',repetitions:7,results},null,2));
