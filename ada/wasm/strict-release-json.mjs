// ADA-322N .dlw — strict JSON lexical scan, then native parse.
export function strictJSON(s){
 let i=0;
 const ws=()=>{while(i<s.length&&/[ \t\r\n]/.test(s[i]))i++};
 function str(){const start=i++;while(i<s.length){const c=s[i++];if(c==='"')return JSON.parse(s.slice(start,i));if(c==='\\')i++;}throw Error("Unterminated JSON string")}
 function value(depth=0){if(depth>128)throw Error("JSON depth");ws();const c=s[i];
 if(c==='{'){i++;ws();const keys=new Set();if(s[i]==='}'){i++;return}while(true){ws();if(s[i]!=='"')throw Error("Expected key");const k=str();if(keys.has(k))throw Error("Duplicate JSON key");keys.add(k);ws();if(s[i++]!==':')throw Error("Expected colon");value(depth+1);ws();const d=s[i++];if(d==='}')return;if(d!==',')throw Error("Expected comma")}}
 if(c==='['){i++;ws();if(s[i]===']'){i++;return}while(true){value(depth+1);ws();const d=s[i++];if(d===']')return;if(d!==',')throw Error("Expected comma")}}
 if(c==='"'){str();return}
 const m=/^(?:true|false|null|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)/.exec(s.slice(i));if(!m)throw Error("Invalid JSON value");if(!["true","false","null"].includes(m[0])&&!Number.isFinite(Number(m[0])))throw Error("Nonfinite JSON number");i+=m[0].length;
 }
 value();ws();if(i!==s.length)throw Error("Trailing JSON");return JSON.parse(s);
}
export function requireUnified(u,commit,digest){
 const expected={status:"PASS",source:commit,sha256:digest,checks:["native unified geometry","committed epoch and inherited context","reload and full audit","missing rejected","binding rejected","binary rejected"]};
 if(!u||Array.isArray(u)||typeof u!=="object"||Object.keys(u).length!==4||!Object.keys(expected).every(k=>Object.hasOwn(u,k)&&JSON.stringify(u[k])===JSON.stringify(expected[k])))throw Error("Unified acceptance rejected");
}
