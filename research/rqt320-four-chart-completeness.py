#!/usr/bin/env python3
"""RQT-320: four tensor movement charts exhaust each permitted parity coset."""
from collections import deque
from itertools import product
import json

PARITIES = ((0,1,1,1), (1,0,0,1), (1,1,1,0))
CHARTS = tuple(tuple(i for i in range(4) if i != missing) for missing in range(4))
MOVES = tuple(sorted(set(tuple((2*s if i == axis else 0) for i in range(4))
                         for chart in CHARTS for axis in chart for s in (-1,1))))
assert len(MOVES) == 8

def check(radius=2):
    result=[]
    for parity in PARITIES:
        origin=parity
        expected={tuple(parity[i]+2*z[i] for i in range(4))
                  for z in product(range(-radius,radius+1),repeat=4)}
        seen={origin}
        queue=deque([origin])
        while queue:
            node=queue.popleft()
            for move in MOVES:
                dest=tuple(node[i]+move[i] for i in range(4))
                if dest in expected and dest not in seen:
                    seen.add(dest)
                    queue.append(dest)
        assert seen == expected
        result.append({'parity': ''.join(map(str,parity)), 'radius':radius,
                       'vectors':len(expected), 'reached':len(seen)})
    return {'status':'finite-box-complete','four_charts':CHARTS,
            'unique_elementary_moves':MOVES,'results':result,
            'total_verified':sum(a['reached'] for a in result),
            'proof':'Every r=p+2z is reachable using sum(abs(z_i)) +-2 elementary coordinate steps, each present in one of four 3-axis movement charts.',
            'limitation':'Coverage does not certify norm, divisibility, rank or binary order. Frozen root-18 matrices remain unavailable.'}

if __name__=='__main__':
    print(json.dumps(check(2),indent=2))
