import {strictJSON,requireUnified} from './strict-release-json.mjs';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const bytes=readFileSync(new URL('./strict-release-json.mjs',import.meta.url));
const blob=createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
assert.equal(blob,'8fdf831f32a554268c57c36f1260eae63245a91f');
const cases=[];
function test(name,fn,expected){let actual=true;try{fn()}catch{actual=false}cases.push({name,expected,actual,match:actual===expected})}
for(const [name,raw,expected] of [['nested','{"a":[1,true,null,{"x":"a"}]}',true],['escaped string','{"a":"\\\""}',true],['same key different objects','[{"a":1},{"a":2}]',true],['duplicate','{"a":1,"a":2}',false],['escaped duplicate','{"a":1,"\\u0061":2}',false],['nested duplicate','{"x":{"a":1,"a":2}}',false],['NaN','NaN',false],['overflow','1e999',false],['trailing','{}{}',false],['leading zero','01',false],['trailing comma','[1,]',false],['depth','['.repeat(130)+'0'+']'.repeat(130),false],['missing colon','{"a" 1}',false],['negative exponent','-1e-3',true]])test(name,()=>strictJSON(raw),expected);
const source='a'.repeat(40),digest='b'.repeat(64),u={status:'PASS',source,sha256:digest,checks:['native unified geometry','committed epoch and inherited context','reload and full audit','missing rejected','binding rejected','binary rejected']};
for(const [name,r,expected] of [['valid receipt',u,true],['wrong source',{...u,source:'c'.repeat(40)},false],['wrong digest',{...u,sha256:'c'.repeat(64)},false],['failed status',{...u,status:'FAIL'},false],['missing group',{...u,checks:u.checks.slice(1)},false],['reordered',{...u,checks:[...u.checks].reverse()},false],['extra field',{...u,extra:1},false],['null',null,false],['array',[],false],['boolean checks',{...u,checks:true},false]])test(name,()=>requireUnified(r,source,digest),expected);
console.log(JSON.stringify({node:process.version,blob,scope:'Node parser and receipt unit tests; not browser or WASM execution',cases,matched:cases.filter(x=>x.match).length},null,2));
if(cases.some(x=>!x.match))process.exitCode=1;
