/**
 * QUANTA QG-013.1 — deterministic reversible transport + standard authenticated envelope.
 * Chrome folding is a lineage visualization, not encryption.
 * Works in modern browsers and Node 22+; cryptographic keys never enter the GitHub repo.
 */
import { runChromeDot, validateChromeDot } from "./chrome-dot.mjs";

export const SPIRAL_SIGNATURE = "12|8/64/3|2/16/8|/4/2/1/1";
export const SPIRAL_VERSION = "QG-013.1";
export const ROUTE_ID = "gray8-outer-spiral-v1";
export const KDF_ITERATIONS = 250000;

function assertDimension(d) {
  if (!Number.isInteger(d) || d < 3 || d > 11) throw new RangeError("Dimension must be integer 3..11.");
}
export function gray(i) { return i ^ (i >>> 1); }
export function ungray(v) {
  let n = v;
  for (let shift = 1; shift < 32; shift *= 2) n ^= n >>> shift;
  return n >>> 0;
}

/** Clockwise outer-to-inner spiral, starting at top left and moving right. */
export function spiralCells(width, height) {
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1) {
    throw new RangeError("Grid dimensions must be positive integers.");
  }
  const cells = [];
  let left = 0, right = width - 1, top = 0, bottom = height - 1;
  while (left <= right && top <= bottom) {
    for (let x = left; x <= right; x++) cells.push([x, top]);
    top++;
    for (let y = top; y <= bottom; y++) cells.push([right, y]);
    right--;
    if (top <= bottom) { for (let x = right; x >= left; x--) cells.push([x, bottom]); bottom--; }
    if (left <= right) { for (let y = bottom; y >= top; y--) cells.push([left, y]); left++; }
  }
  return cells;
}

export function instantiateSpiral(dimension = 11) {
  assertDimension(dimension);
  const width = 2 ** Math.ceil((dimension - 3) / 2);
  const height = 2 ** Math.floor((dimension - 3) / 2);
  const cells = spiralCells(width, height);
  const routes = [];
  const representatives = [];
  const addressToPosition = Array(2 ** dimension).fill(-1);
  const globules = [];
  for (let seq = 0; seq < cells.length; seq++) {
    const [x, y] = cells[seq];
    const globuleIndex = y * width + x;
    const addresses = Array.from({ length: 8 }, (_, j) => gray(8 * globuleIndex + j));
    const chrome = runChromeDot(addresses.map(a => a.toString(2).padStart(dimension, "0")));
    if (!validateChromeDot(chrome).pass) throw new Error("Chrome lineage failed validation.");
    const lastId = chrome.terminalId;
    globules.push(Object.freeze({
      traversal: seq, index: globuleIndex, x, y,
      addresses: Object.freeze(addresses),
      terminalId: lastId,
      lineage: chrome.nodes[0].leaves
    }));
    representatives.push(lastId);
    for (const address of addresses) {
      if (addressToPosition[address] !== -1) throw new Error("Duplicate vertex address.");
      addressToPosition[address] = routes.length;
      routes.push(address);
    }
  }
  if (routes.length !== 2 ** dimension || addressToPosition.includes(-1)) {
    throw new Error("Spiral must cover all hypercube vertex addresses.");
  }
  return Object.freeze({
    version: SPIRAL_VERSION, signature: SPIRAL_SIGNATURE, dimensions: dimension,
    width, height,
    globules: Object.freeze(globules),
    route: Object.freeze(routes),
    inverse: Object.freeze(addressToPosition),
    representatives: Object.freeze(representatives)
  });
}

export function encodeVertexOrder(values, spiral) {
  if (!Array.isArray(values) || values.length !== spiral.route.length) throw new RangeError("One value per vertex required.");
  return spiral.route.map(id => values[id]);
}

export function decodeVertexOrder(transported, spiral) {
  if (!Array.isArray(transported) || transported.length !== spiral.route.length) throw new RangeError("Invalid transported value count.");
  const restored = Array(transported.length);
  for (let i = 0; i < transported.length; i++) restored[spiral.route[i]] = transported[i];
  return restored;
}

function url64(bytes) {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}
function fromUrl64(value) {
  if (typeof value !== "string" || !/^[A-Za-z0-9_-]+$/.test(value)) throw new TypeError("Invalid base64url field.");
  const s = value.replace(/-/g, "+").replace(/_/g, "/");
  const bytes = atob(s.padEnd(Math.ceil(s.length / 4) * 4, "="));
  return Uint8Array.from(bytes, c => c.charCodeAt(0));
}
function cryptoProvider() {
  if (!globalThis.crypto?.subtle || !globalThis.crypto?.getRandomValues) throw new Error("Web Crypto requires a secure origin and modern browser/Node.");
  return globalThis.crypto;
}
function text(s) { return new TextEncoder().encode(s); }
function headerFor(dimension) {
  return {
    dimensions: dimension, signature: SPIRAL_SIGNATURE, algorithm: "AES-256-GCM",
    kdf: "PBKDF2-HMAC-SHA-256", iterations: KDF_ITERATIONS, route: ROUTE_ID
  };
}
async function keyFromPassword(password, salt, iterations) {
  const crypto = cryptoProvider();
  const material = await crypto.subtle.importKey("raw", text(password), "PBKDF2", false, ["deriveKey"]);
  return crypto.subtle.deriveKey(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations },
    material, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]
  );
}

/** Encrypt UTF-8. Random salt & nonce are newly generated for each envelope. */
export async function sealTransport(message, password, dimension = 11) {
  assertDimension(dimension);
  if (typeof message !== "string") throw new TypeError("Payload must be UTF-8 text.");
  if (typeof password !== "string" || password.length < 12) throw new TypeError("Use a passphrase of at least 12 characters.");
  const crypto = cryptoProvider(), header = headerFor(dimension);
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const nonce = crypto.getRandomValues(new Uint8Array(12));
  const key = await keyFromPassword(password, salt, KDF_ITERATIONS);
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv: nonce, additionalData: text(JSON.stringify(header)), tagLength: 128 },
    key, text(message)
  );
  return {
    version: SPIRAL_VERSION, header,
    salt: url64(salt), nonce: url64(nonce),
    ciphertext: url64(new Uint8Array(ciphertext))
  };
}

export async function openTransport(envelope, password) {
  if (!envelope || envelope.version !== SPIRAL_VERSION) throw new TypeError("Unknown envelope version.");
  if (typeof password !== "string") throw new TypeError("Password required.");
  const header = envelope.header;
  if (!header || !Number.isInteger(header.dimensions) || header.dimensions < 3 || header.dimensions > 11 ||
      JSON.stringify(header) !== JSON.stringify(headerFor(header.dimensions))) {
    throw new TypeError("Unsupported or modified authenticated header.");
  }
  const salt = fromUrl64(envelope.salt), nonce = fromUrl64(envelope.nonce);
  if (salt.length !== 16 || nonce.length !== 12) throw new TypeError("Invalid nonce or salt length.");
  const key = await keyFromPassword(password, salt, KDF_ITERATIONS);
  const clear = await cryptoProvider().subtle.decrypt(
    { name: "AES-GCM", iv: nonce, additionalData: text(JSON.stringify(header)), tagLength: 128 },
    key, fromUrl64(envelope.ciphertext)
  );
  return new TextDecoder("utf-8", { fatal: true }).decode(clear);
}
