/**
 * QUANTA QG-014 — recoverable width fold.
 * A 128-bit source is represented by one terminal parity bit PLUS 127 witness bits.
 *
 * At each fold, (left,right) -> (left XOR right, witness=right).
 * Reverse: left=parent XOR witness, right=witness.
 *
 * This is a reversible change of representation, not compression, encryption
 * or a cryptographically authenticated commitment. The witness is required.
 */
export const RECOVERABLE_FOLD_VERSION = "QG-014.1";
export const FOLD_WIDTHS = Object.freeze([128,64,32,16,8,4,2,1,1]);
export const FOLD_CHUNKS = Object.freeze([
  Object.freeze([128,64,32,16]),
  Object.freeze([8,4,2,1]),
  Object.freeze([1])
]);

function requireBits(bits, size) {
  if (typeof bits !== "string" || bits.length !== size || /[^01]/.test(bits)) {
    throw new TypeError("Expected exactly " + size + " bits, each 0 or 1.");
  }
}
function freezeStage(stage, inputWidth, output, witness, operation) {
  return Object.freeze({
    stage,
    inputWidth,
    outputWidth: output.length,
    output,
    witness,
    operation,
    chunk: stage <= 3 ? "A" : stage <= 7 ? "B" : "terminal"
  });
}
/**
 * Run deterministic fold. 7 pair-folds + one identity fold.
 * All witness data is retained, in a read-only, serializable record.
 */
export function fold128(source) {
  requireBits(source,128);
  let current=source;
  const stages=[freezeStage(0,128,source,"","source")];
  for(let stage=1;stage<=7;stage++){
    let out="",witness="";
    for(let i=0;i<current.length;i+=2){
      const left=Number(current[i]),right=Number(current[i+1]);
      out+=String(left^right);
      witness+=String(right);
    }
    stages.push(freezeStage(stage,current.length,out,witness,"xor-right"));
    current=out;
  }
  stages.push(freezeStage(8,1,current,"","fixed-point"));
  return Object.freeze({
    version: RECOVERABLE_FOLD_VERSION,
    display: current, // one visible quantum chrome dot state
    sourceWidth: 128,
    witnessBits: 127,
    stages: Object.freeze(stages),
    chunkA: FOLD_CHUNKS[0],
    chunkB: FOLD_CHUNKS[1],
    terminal: FOLD_CHUNKS[2]
  });
}
/** Recover all 128 original bits from just the terminal dot and its 127-bit witness. */
export function unfold128(record) {
  if (!record || record.version !== RECOVERABLE_FOLD_VERSION ||
      !Array.isArray(record.stages) || record.stages.length!==9) {
    throw new TypeError("Invalid QG-014 fold record.");
  }
  requireBits(record.display,1);
  const stages=record.stages;
  if (stages[8].operation!=="fixed-point" || stages[8].output!==record.display ||
      stages[7].output!==record.display || stages[8].witness!=="") {
    throw new Error("Terminal fixed point was altered.");
  }
  let current=record.display;
  for(let i=7;i>=1;i--){
    const stage=stages[i],prior=stages[i-1],width=FOLD_WIDTHS[i];
    if(stage.operation!=="xor-right" || stage.inputWidth!==width*2 ||
       stage.outputWidth!==width || stage.output!==current ||
       typeof stage.witness!=="string")throw new Error("Broken fold lineage at stage "+i);
    requireBits(stage.witness,width);
    let restored="";
    for(let j=0;j<width;j++){
      const right=Number(stage.witness[j]),parent=Number(current[j]);
      restored+=String(parent^right)+String(right);
    }
    if(prior.output!==restored || prior.outputWidth!==restored.length) {
      throw new Error("Source replay mismatch at stage "+i);
    }
    current=restored;
  }
  requireBits(current,128);
  if(stages[0].operation!=="source" || stages[0].output!==current) {
    throw new Error("Initial source mismatch.");
  }
  return current;
}
export function validateFold128(record) {
  const errors=[];
  try{
    const recovered=unfold128(record);
    const widths=record.stages.map(x=>x.outputWidth);
    if(JSON.stringify(widths)!==JSON.stringify(FOLD_WIDTHS))throw new Error("Width schedule mismatch");
    if(record.witnessBits!==127 ||
       record.stages.slice(1,8).reduce((n,s)=>n+s.witness.length,0)!==127){
      throw new Error("Witness cardinality mismatch");
    }
    if(record.display!==String([...recovered].reduce((acc,x)=>acc^Number(x),0))){
      throw new Error("Terminal parity mismatch");
    }
  }catch(e){errors.push(e.message)}
  return Object.freeze({pass:errors.length===0,errors:Object.freeze(errors),widths:FOLD_WIDTHS});
}
/**
 * Portable transport frame contains terminal bit plus only the seven residual sets.
 * The source/stage outputs are reconstructed on import.
 * This frame is NOT authenticated. Seal it using QG-013 to protect integrity.
 */
export function exportFold128(record){
  const verdict=validateFold128(record);
  if(!verdict.pass)throw new Error(verdict.errors.join("; "));
  return Object.freeze({
    version:RECOVERABLE_FOLD_VERSION,
    terminal:record.display,
    witness:Object.freeze(record.stages.slice(1,8).map(x=>x.witness))
  });
}
export function importFold128(frame){
  if (!frame || frame.version!==RECOVERABLE_FOLD_VERSION ||
      !Array.isArray(frame.witness)||frame.witness.length!==7) {
    throw new TypeError("Invalid QG-014 witness frame.");
  }
  requireBits(frame.terminal,1);
  let current=frame.terminal;
  const outputs=Array(8),witness=frame.witness;
  outputs[7]=current;
  for(let i=7;i>=1;i--){
    requireBits(witness[i-1],FOLD_WIDTHS[i]);
    let restored="";
    for(let j=0;j<current.length;j++){
      const right=Number(witness[i-1][j]),parent=Number(current[j]);
      restored+=String(parent^right)+String(right);
    }
    current=restored;
    outputs[i-1]=current;
  }
  const stages=[freezeStage(0,128,outputs[0],"","source")];
  for(let i=1;i<=7;i++)stages.push(freezeStage(i,FOLD_WIDTHS[i-1],outputs[i],witness[i-1],"xor-right"));
  stages.push(freezeStage(8,1,frame.terminal,"","fixed-point"));
  const record=Object.freeze({
    version:RECOVERABLE_FOLD_VERSION,display:frame.terminal,sourceWidth:128,witnessBits:127,
    stages:Object.freeze(stages),chunkA:FOLD_CHUNKS[0],chunkB:FOLD_CHUNKS[1],terminal:FOLD_CHUNKS[2]
  });
  if(!validateFold128(record).pass)throw new Error("Fold frame did not reconstruct");
  return record;
}
