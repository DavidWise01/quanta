// ADA-292N .dlw — strict parity reference validation, before native comparison.
export function parseReference(line){
 const fields=line.split("\t");
 if(fields.length!==4)throw Error("Malformed reference row");
 const [name,raw,expected,kind]=fields;
 if(!/^ada_[a-z_]+$/.test(name)||!["u","i","f"].includes(kind))throw Error("Invalid reference schema");
 const parts=raw.split(",");
 if(parts.some(x=>! /^-?(0|[1-9][0-9]*)$/.test(x)||!Number.isSafeInteger(Number(x))||Number(x)<-2147483648||Number(x)>4294967295))throw Error("Invalid argument");
 if(kind==="f"&&expected==="NaN")return {name,args:parts.map(Number),want:NaN,kind};
 if(!/^-?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$/.test(expected))throw Error("Invalid reference number");
 const want=Number(expected);
 if(!Number.isFinite(want)||kind==="u"&&(!Number.isInteger(want)||want<0||want>4294967295)||kind==="i"&&(!Number.isInteger(want)||want< -2147483648||want>2147483647))throw Error("Reference number out of range");
 return {name,args:parts.map(Number),want,kind};
}
