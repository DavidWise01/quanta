// ADA-159A .dlw — proposed lossless structural packing; not a physical quantum model.
export function pack(spectrum,chrome,singlet,coordinates){
 const fields=[spectrum,chrome,singlet,coordinates], widths=[24,9,1,8];
 if(fields.some((v,i)=>typeof v!=="bigint"||v<0n||v>=(1n<<BigInt(widths[i]))))throw Error("field width");
 return spectrum|(chrome<<24n)|(singlet<<33n)|(coordinates<<34n);
}
export function unpack(v){if(typeof v!=="bigint"||v<0n||v>=1n<<42n)throw Error("width");return [v&0xffffffn,(v>>24n)&511n,(v>>33n)&1n,(v>>34n)&255n];}
export function verify(){let n=0;for(let i=0;i<42;i++){const v=1n<<BigInt(i);if(pack(...unpack(v))!==v)throw Error("basis");n++;}for(const v of [0n,(1n<<42n)-1n]){if(pack(...unpack(v))!==v)throw Error("edge");n++;}let x=1n;for(let i=0;i<4096;i++){x=(x*25214903917n+11n)&((1n<<42n)-1n);if(pack(...unpack(x))!==x)throw Error("roundtrip");n++;}return n;}
