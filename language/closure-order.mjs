// QG-044: preserve interval pairing and closure order while folding.
// The notation is a symbolic relationship grammar, not a claim of physical topology.
const OPENS = Object.freeze({'[':']','(':')'});
const CLOSES = Object.freeze({']':'[',')':'('});
export const CANONICAL = '.[(.])';

export function analyzeClosure(source) {
  if (typeof source !== 'string') throw new TypeError('Expected a string');
  const stacks = {'[':[], '(':[]};
  const vertices = [], intervals = [], tokens = [];
  let event = 0;
  for (let i=0; i<source.length; i++) {
    const glyph=source[i];
    if (/\s/.test(glyph)) continue;
    if (glyph !== '.' && !(glyph in OPENS) && !(glyph in CLOSES))
      throw new Error('Unknown symbol at index '+i);
    tokens.push({glyph,index:i});
    if (glyph === '.') { vertices.push(i); continue; }
    if (glyph in OPENS) { stacks[glyph].push({open:i,openEvent:event++}); continue; }
    const openGlyph=CLOSES[glyph];
    if (!stacks[openGlyph].length) throw new Error('Unmatched closing '+glyph+' at '+i);
    const opener=stacks[openGlyph].pop();
    intervals.push({kind:openGlyph === '[' ? 'box':'fold',open:opener.open,close:i,openEvent:opener.openEvent,closeEvent:event++});
  }
  if (stacks['['].length || stacks['('].length) throw new Error('Unclosed boundary');
  intervals.sort((a,b)=>a.open-b.open);
  const crossings=[];
  for(let i=0;i<intervals.length;i++) for(let j=i+1;j<intervals.length;j++) {
    const a=intervals[i],b=intervals[j];
    if(a.open < b.open && b.open < a.close && a.close < b.close)
      crossings.push({first:i,second:j});
  }
  const closeOrder=[...intervals].sort((a,b)=>a.close-b.close).map(x=>x.kind);
  return {source,tokens,vertices,intervals,crossings,closeOrder,signature:intervals.map(x=>x.kind+':'+x.open+'-'+x.close).join('|')};
}
export function foldClosure(source) {
  const analyzed=analyzeClosure(source);
  return {
    version:'QG-044',
    tokens:analyzed.tokens.map(x=>({...x})),
    vertices:[...analyzed.vertices],
    intervals:analyzed.intervals.map(x=>({...x})),
    crossings:analyzed.crossings.map(x=>({...x})),
    closeOrder:[...analyzed.closeOrder],
    signature:analyzed.signature,
    original:source
  };
}
const same=(a,b)=>JSON.stringify(a) === JSON.stringify(b);
export function unfoldClosure(packet) {
  if (!packet || packet.version!=='QG-044' || !Array.isArray(packet.tokens))
    throw new Error('Invalid fold packet');
  let end=0;
  for(let i=0;i<packet.tokens.length;i++){
    const t=packet.tokens[i];
    if(!t || !Number.isSafeInteger(t.index) || t.index<end || typeof t.glyph!=='string' || t.glyph.length!==1)
      throw new Error('Invalid or out-of-order token position');
    end=t.index+1;
  }
  if (typeof packet.original!=='string') throw new Error('Missing original byte sequence');
  const source=packet.original;
  const actual=foldClosure(source);
  for(const key of ['tokens','vertices','intervals','crossings','closeOrder','signature'])
    if(!same(packet[key],actual[key])) throw new Error('Fold packet mismatch: '+key);
  return source;
}
export function compareClosures(first,second) {
  const a=analyzeClosure(first),b=analyzeClosure(second);
  return {
    sameMarks:[...first].sort().join('')===[...second].sort().join(''),
    sameSignature:a.signature===b.signature,
    firstCrossings:a.crossings.length,
    secondCrossings:b.crossings.length,
    firstCloseOrder:a.closeOrder,
    secondCloseOrder:b.closeOrder
  };
}
