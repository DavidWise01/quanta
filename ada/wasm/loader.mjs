// ADA-282N .dlw — fail-closed browser loader; no JS computational fallback.
const required=["ada_abi_version","ada_growth_numerator","ada_growth_denominator","ada_prefer","ada_typed_version","ada_epoch_size","ada_memory_window","ada_prefer_typed","ada_consequence","ada_clock_field","ada_clock_advance","ada_memory_generation","ada_tesseract_coordinate","ada_tesseract_edge","ada_pump_field","ada_inherited_generation","ada_equilibrium_field"];
export async function loadKernel(base,expectedCommit){
 if(!/^[a-f0-9]{40}$/.test(expectedCommit))throw Error("Expected source commit required");
 const root=new URL(base,import.meta.url);
 async function get(name){const r=await fetch(new URL(name,root),{cache:"no-store",redirect:"error"});if(!r.ok)throw Error(name+": HTTP "+r.status);return r;}
 const manifest=await (await get("manifest.json")).json();
 if(manifest.schema!=="ADA-281N.package.v1"||manifest.source_commit!==expectedCommit||manifest.authority!=="OBSERVE_ONLY"||manifest.double_build_equal!==true||manifest.parity?.status!=="PASS"||manifest.parity?.checks!==57933||manifest.parity?.tolerance!==1e-12||!Number.isFinite(manifest.parity?.maxError)||manifest.parity.maxError<0||manifest.parity.maxError>1e-12||!/^[a-f0-9]{64}$/.test(manifest.sha256)||!Number.isSafeInteger(manifest.bytes)||manifest.bytes<=0||manifest.bytes>16*1024*1024)throw Error("Package manifest rejected");
 const bytes=await (await get("ada_browser.wasm")).arrayBuffer();
 if(bytes.byteLength!==manifest.bytes)throw Error("Binary length mismatch");
 const digest=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)),b=>b.toString(16).padStart(2,"0")).join("");
 if(digest!==manifest.sha256)throw Error("Binary digest mismatch");
 const module=await WebAssembly.compile(bytes);
 if(WebAssembly.Module.imports(module).length!==0)throw Error("Unexpected imports");
 const instance=await WebAssembly.instantiate(module,{});
 const e=instance.exports;
 for(const name of required)if(typeof e[name]!=="function")throw Error("Missing ABI export "+name);
 if(e.ada_abi_version()!==1||e.ada_typed_version()!==2||e.ada_growth_numerator()!==41||e.ada_growth_denominator()!==40||e.ada_epoch_size()!==24||e.ada_memory_window()!==8)throw Error("Invariant mismatch");
 if(e.ada_clock_field(360,4)!==0||e.ada_clock_field(24,1)!==1||e.ada_prefer(99,4,2,4,2)!==0||e.ada_consequence(0,2)!==5)throw Error("ABI smoke mismatch");
 return Object.freeze({exports:e,source:manifest.source_commit,sha256:digest,bytes:bytes.byteLength});
}
