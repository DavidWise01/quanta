import assert from "node:assert/strict";
import {parseReference} from "./reference-schema.mjs";
const valid=[["ada_clock_field\t0,0\t0\tu",0],["ada_clock_field\t4294967295,0\t4294967295\tu",4294967295],["ada_consequence\t-1,0\t-2\ti",-2],["ada_pump_field\t0,3,0\tNaN\tf",NaN],["ada_pump_field\t0,0,1\t1.25e-3\tf",0.00125],["ada_pump_field\t0,0,1\t-0\tf",-0]];
const invalid=["ada_clock_field\t0,0\t\tu","ada_pump_field\t0,3,0\tinvalid\tf","ada_pump_field\t0,3,0\tInfinity\tf","ada_pump_field\t0,3,0\t NaN\tf","ada_clock_field\t0,0\t-1\tu","ada_clock_field\t0,0\t4294967296\tu","ada_clock_field\t0,0\t1.5\tu","ada_consequence\t-1,0\t2147483648\ti","ada_clock_field\t,0\t0\tu","ada_clock_field\t4294967296,0\t0\tu","ada_clock_field\t0,0\t0\tx","ada_clock_field\t0,0\t0\tu\textra","ada_clock_field\t0,0\t0x0\tu","ada_clock_field\t0,0\tNaN\tu"];
for(const [line,want] of valid)assert.ok(Object.is(parseReference(line).want,want));
for(const line of invalid)assert.throws(()=>parseReference(line));
console.log(JSON.stringify({status:"PASS",valid:valid.length,rejected:invalid.length,checks:valid.length+invalid.length}));
