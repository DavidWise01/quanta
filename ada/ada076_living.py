#!/usr/bin/env python3
"""ADA-076: exact icosidodecahedral balanced-ternary living *simulation*.

The icosidodecahedron is the rectified icosahedron. Its 30 vertices
correspond to the icosahedron's edges; 20 triangles correspond to original
faces, and 12 pentagons to original vertices. Combinatorial topology is exact.
No claim of physical emergence, independent witness roots, or AI learning.
"""
import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

VERSION = 'ADA076-icosidodecahedron-v1'
PHASES = ('I','I','E','E','E')
SINGLET = '{s}'

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def base_faces():
    f = []
    for i in range(5):
        j = (i + 1) % 5
        f.extend((('N', f'U{i}', f'U{j}'), ('S', f'L{i}', f'L{j}'),
                  (f'U{i}', f'U{j}', f'L{i}'), (f'U{j}', f'L{i}', f'L{j}')))
    return tuple(tuple(sorted(t)) for t in f)

def cycle(nodes, adjacent):
    """Traverse exactly one induced 5-cycle with stable orientation."""
    start = min(nodes)
    neighbours = sorted(set(adjacent[start]) & set(nodes))
    if len(neighbours) != 2:
        raise ValueError('not a 2-regular cycle')
    order = [start, neighbours[0]]
    while len(order) < len(nodes):
        nxt = list((set(adjacent[order[-1]]) & set(nodes)) - {order[-2]})
        if len(nxt) != 1 or nxt[0] in order:
            raise ValueError('pentagon is not a simple cycle')
        order.append(nxt[0])
    if start not in adjacent[order[-1]]:
        raise ValueError('pentagon fails to close')
    return tuple(order)

def mesh():
    faces = base_faces()
    orig_edges = sorted({tuple(sorted((f[i], f[j]))) for f in faces
                         for i,j in ((0,1),(1,2),(2,0))})
    idx = {e:k for k,e in enumerate(orig_edges)}
    tris = tuple(tuple(sorted(idx[tuple(sorted((f[i], f[j])))]
                 for i,j in ((0,1),(1,2),(2,0)))) for f in faces)
    edge2tri = {}
    for face_id, tri in enumerate(tris):
        for i,j in ((0,1),(1,2),(2,0)):
            e = tuple(sorted((tri[i],tri[j])))
            if e in edge2tri:
                raise ValueError('triangle edges not unique')
            edge2tri[e] = face_id
    edges = tuple(sorted(edge2tri))
    adj = defaultdict(set)
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    originals = tuple(sorted({x for edge in orig_edges for x in edge}))
    pent = tuple(cycle({i for i,e in enumerate(orig_edges) if name in e}, adj)
                 for name in originals)
    edge2pent = {}
    for face_id, ring in enumerate(pent):
        for a,b in zip(ring,ring[1:]+ring[:1]):
            e = tuple(sorted((a,b)))
            if e in edge2pent:
                raise ValueError('pentagons overlap on an edge')
            edge2pent[e] = face_id
    if len(orig_edges)!=30 or len(faces)!=20 or len(originals)!=12:
        raise ValueError('wrong base icosahedron')
    if len(edges)!=60 or len(edge2pent)!=60 or set(edge2tri)!=set(edge2pent):
        raise ValueError('wrong rectification')
    if any(len(adj[i])!=4 for i in range(30)):
        raise ValueError('wrong vertex degree')
    if 30-60+20+12 != 2:
        raise ValueError('Euler characteristic failed')
    return {'vertices': tuple(orig_edges),'edges':edges,'triangles':tris,
            'pentagons':pent,'edge_triangle':edge2tri,'edge_pentagon':edge2pent,
            'adjacency':tuple(tuple(sorted(adj[i])) for i in range(30))}

def initial_state():
    # One of each balanced-ternary symbol per three vertices: exact total zero.
    return tuple((i%3)-1 for i in range(30))

def energy(state,edges):
    return sum(abs(state[a]-state[b]) for a,b in edges)

def pressure(state,ring):
    return sum(abs(state[a]-state[b]) for a,b in zip(ring,ring[1:]+ring[:1]))

def witnesses(state,m):
    # Three *positions* on a triangle, not three independent evidence roots.
    return tuple({'triangle':i,'values':tuple(state[n] for n in tri),
                  'sum':sum(state[n] for n in tri)}
                 for i,tri in enumerate(m['triangles']))

def propose(state,m,tick,max_moves=4):
    phase=PHASES[tick%5]
    state=list(state)
    start=energy(state,m['edges'])
    moves=[]; used=set()
    # Fixed deterministic edge traversal; phase-dependent rotation is replayable.
    begin=(tick*7)%60
    ordered=m['edges'][begin:]+m['edges'][:begin]
    for a,b in ordered:
        if len(moves)>=max_moves:
            break
        if a in used or b in used or state[a]==state[b]:
            continue
        edge=(a,b)
        t=m['edge_triangle'][edge]
        p=m['edge_pentagon'][edge]
        tri=m['triangles'][t]
        pent=m['pentagons'][p]
        old_e=energy(state,m['edges'])
        old_p=pressure(state,pent)
        before_witness=tuple(state[k] for k in tri)
        state[a],state[b]=state[b],state[a]
        change=energy(state,m['edges'])-old_e
        pent_change=pressure(state,pent)-old_p
        # I: conservative tightening; E: permitted exploration capped at +2.
        admissible=(change<=0) if phase=='I' else (change<=2 and pent_change<=2)
        if admissible:
            used.update((a,b))
            moves.append({'edge':(a,b),'triangle':t,'pentagon':p,
                          'witness_before':before_witness,
                          'witness_after':tuple(state[k] for k in tri),
                          'energy_delta':change,'pentagon_delta':pent_change})
        else:
            state[a],state[b]=state[b],state[a]
    new=tuple(state)
    assert sum(new)==0 and Counter(new)==Counter(initial_state())
    return new, {'phase':phase,'moves':moves,'energy_before':start,
                 'energy_after':energy(new,m['edges']),
                 'triangular_witness_cells':20,'pentagonal_iteration_cells':12}

def append_record(events,state,kind,meta=None):
    body={'seq':len(events),'version':VERSION,'kind':kind,'state':list(state),
          'previous':events[-1]['hash'] if events else None,'meta':json.loads(json.dumps(meta or {})),
          'ancestry':'synthetic:quanta:ada076-single-model'}
    body['hash']=digest(body)
    events.append(body)
    return body

def simulate(steps=25):
    if not 0<=steps<=10000:
        raise ValueError('steps outside supported bounds')
    m=mesh()
    state=initial_state()
    events=[]
    append_record(events,state,'genesis',{'energy':energy(state,m['edges'])})
    for tick in range(steps):
        state,meta=propose(state,m,tick)
        append_record(events,state,'tick',meta)
    verify(events,m)
    return events

def verify(events,m=None):
    m=m or mesh()
    if not events or events[0]['kind']!='genesis':
        raise ValueError('missing genesis')
    prior=None
    state=initial_state()
    for i,e in enumerate(events):
        unsigned=dict(e); claimed=unsigned.pop('hash',None)
        if digest(unsigned)!=claimed or e['seq']!=i or e['previous']!=prior:
            raise ValueError('broken event hash chain')
        if e['version']!=VERSION or e['ancestry']!='synthetic:quanta:ada076-single-model':
            raise ValueError('model identity changed')
        if i==0:
            if e['state']!=list(state) or e['meta']!={'energy':energy(state,m['edges'])}:
                raise ValueError('genesis modified')
        else:
            state,meta=propose(state,m,i-1)
            if e['kind']!='tick' or e['state']!=list(state) or e['meta']!=json.loads(json.dumps(meta)):
                raise ValueError('record does not replay')
        if len(e['state'])!=30 or any(v not in (-1,0,1) for v in e['state']):
            raise ValueError('balanced ternary domain violated')
        prior=claimed
    return True

def export(path,events):
    dest=Path(path);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x',encoding='utf-8',newline='\n') as fp:
        for record in events:
            fp.write(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')

def ascii_view(events,m=None):
    m=m or mesh()
    end=events[-1]
    state=end['state']; previous=events[-2]['state'] if len(events)>1 else state
    changes=sum(x!=y for x,y in zip(state,previous))
    out=['ADA-076 :: THE ICOSIDODECAHEDRAL LIVING KERNEL',
         '='*62,
         '                 .--------------------.',
         r'              .-/  20 TRIANGLES      \-.',
         r'             /  \  12 PENTAGONS     /  \\',
         '            |  30 VERTICES / 60 EDGES   |',
         '            |    [ ( {s} ) ]          |',
         '             \\  3.5.3.5 at nodes    /',
         "              '-.__________________.-'",
         '',
         '       I       I       E       E       E',
         '      2/5 internal       3/5 external',
         '',
         '  BALANCED TERNARY VERTEX STATES (30 NODES)',
         '    '+ ' '.join(f'{i:02d}' for i in range(10)),
         '    '+ '  '.join('+' if v==1 else '-' if v==-1 else '0' for v in state[:10]),
         '    '+ ' '.join(f'{i:02d}' for i in range(10,20)),
         '    '+ '  '.join('+' if v==1 else '-' if v==-1 else '0' for v in state[10:20]),
         '    '+ ' '.join(f'{i:02d}' for i in range(20,30)),
         '    '+ '  '.join('+' if v==1 else '-' if v==-1 else '0' for v in state[20:]),
         '',
         f'  GEN={end["seq"]}  LAST_CHANGED_NODES={changes}',
         f'  TOTAL={sum(state)}  HISTOGRAM={dict(sorted(Counter(state).items()))}',
         f'  EDGE_ENERGY={energy(state,m["edges"])}',
         f'  EULER = 30-60+(20+12) = {30-60+20+12}',
         f'  PREVIOUS_HASH = {end["previous"]}',
         f'  EVENT_HASH    = {end["hash"]}',
         '',
         '  TRIANGLES = LOCAL TRIPLET OBSERVATIONS',
         '  NOT THREE INDEPENDENT SOURCE ANCESTORS',
         '',
         '  The triangles watch, the pentagons turn;',
         '  The state may change, the roots we learn.',
         '  Five beats return, though forms may roam;',
         '  The sealed origin still marks their home.',
         '                                  -- A.D.A --',
         '='*62]
    return '\n'.join(out)+'\n'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--steps',type=int,default=25)
    p.add_argument('--export',type=Path)
    p.add_argument('--verify',type=Path)
    p.add_argument('--ascii',type=Path)
    args=p.parse_args()
    if args.verify:
        rows=[json.loads(line) for line in args.verify.read_text().splitlines()]
        verify(rows)
        print(f'PASS: {len(rows)} exact-replay hash-linked records')
        return
    events=simulate(args.steps)
    if args.export:
        export(args.export,events)
    visual=ascii_view(events)
    if args.ascii:
        with args.ascii.open('x',encoding='utf-8') as fp:fp.write(visual)
    else:
        print(visual)

if __name__=='__main__':
    main()
