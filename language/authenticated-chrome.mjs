/**
 * QG-015.1 · Authenticated Chrome Dot Transport.
 *
 * One visible parity bit + 127 witness bits are serialized into the QG-013
 * authenticated spiral transport, then reconstructed and checked on receipt.
 *
 * This is a demonstration protocol, not an independently audited encryption
 * system. Authentication relies on AES-GCM and the password-derived key.
 */
import {
  fold128, unfold128, exportFold128, importFold128, validateFold128
} from "./recoverable-fold.mjs";
import {
  sealTransport, openTransport, SPIRAL_SIGNATURE
} from "./downward-spiral.mjs";

export const AUTHENTICATED_CHROME_VERSION = "QG-015.1";
const WITNESS_LENGTHS = Object.freeze([64, 32, 16, 8, 4, 2, 1]);

function require128(bits) {
  if (typeof bits !== "string" || !/^[01]{128}$/.test(bits)) {
    throw new TypeError("QG-015 requires exactly 128 binary source bits.");
  }
}
function parseFrame(json) {
  let frame;
  try { frame = JSON.parse(json); }
  catch { throw new TypeError("Authenticated payload is not a valid fold frame."); }
  if (!frame || frame.protocol !== AUTHENTICATED_CHROME_VERSION ||
      frame.signature !== SPIRAL_SIGNATURE ||
      typeof frame.sourceTag !== "string" ||
      frame.sourceTag.length === 0 ||
      frame.sourceTag.length > 96 ||
      !frame.fold || frame.fold.version !== "QG-014.1" ||
      !Array.isArray(frame.fold.witness) ||
      frame.fold.witness.length !== 7 ||
      !frame.fold.witness.every((w, i) => typeof w === "string" &&
        /^[01]+$/.test(w) && w.length === WITNESS_LENGTHS[i]) ||
      !/^[01]$/.test(frame.fold.terminal)) {
    throw new TypeError("Malformed authenticated Chrome Dot frame.");
  }
  return frame;
}
export function composeChromeFrame(sourceBits, sourceTag = "quanta-source") {
  require128(sourceBits);
  if (typeof sourceTag !== "string" || sourceTag.length === 0 ||
      sourceTag.length > 96) throw new TypeError("Source tag must have 1–96 characters.");
  const record = fold128(sourceBits);
  const verdict = validateFold128(record);
  if (!verdict.pass) throw new Error("QG-014 lineage failed: " + verdict.errors.join("; "));
  return Object.freeze({
    protocol: AUTHENTICATED_CHROME_VERSION,
    signature: SPIRAL_SIGNATURE,
    sourceTag,
    fold: exportFold128(record)
  });
}
export function recoverChromeFrame(frame) {
  const validated = parseFrame(JSON.stringify(frame));
  const record = importFold128(validated.fold);
  const originalBits = unfold128(record);
  if (originalBits.length !== 128 || !validateFold128(record).pass) {
    throw new Error("Recovered source failed the fold invariant.");
  }
  return Object.freeze({
    sourceBits: originalBits,
    sourceTag: validated.sourceTag,
    terminal: record.display,
    witnessBits: 127,
    widths: Object.freeze(record.stages.map(s => s.outputWidth)),
    verified: true
  });
}
/** Seal the full terminal + lineage frame with QG-013 AES-GCM. */
export async function sendChromeDot(sourceBits, password, dimension = 11, sourceTag = "quanta-source") {
  const frame = composeChromeFrame(sourceBits, sourceTag);
  const envelope = await sealTransport(JSON.stringify(frame), password, dimension);
  return Object.freeze({
    ...envelope,
    chromeProtocol: AUTHENTICATED_CHROME_VERSION
  });
}
/** Fail closed on wrong passwords, altered frames, routes, dimensions or ciphertext. */
export async function receiveChromeDot(envelope, password) {
  if (!envelope || envelope.chromeProtocol !== AUTHENTICATED_CHROME_VERSION) {
    throw new TypeError("Unrecognized authenticated Chrome Dot envelope.");
  }
  const authenticatedPayload = await openTransport(envelope, password);
  return recoverChromeFrame(parseFrame(authenticatedPayload));
}
