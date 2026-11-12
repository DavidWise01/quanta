#!/usr/bin/env python3
"""RQT-319: finite-prefix fair scheduling on the recursively nested 3x3x3 tensor.

Each finite tensor address receives all 26 noncentral directions at a finite
stage. Preferences may reorder directions *inside* a stage only.
"""
import argparse
import hashlib
import itertools
import json

CENTER = (0, 0, 0)
DIRECTIONS = tuple((x, y, z) for z in (-1, 0, 1)
                   for y in (-1, 0, 1) for x in (-1, 0, 1))
MOVES = tuple(v for v in DIRECTIONS if v != CENTER)
assert len(DIRECTIONS) == 27 and len(MOVES) == 26

def shell(move):
    return sum(v * v for v in move)

def stage(generation, prefer=(3, 2, 1)):
    """Exhaust a finite generation, with configurable shell preferences."""
    assert generation >= 0
    shell_order = {s: i for i, s in enumerate(prefer)}
    moves = sorted(MOVES, key=lambda m: (shell_order[shell(m)], m))
    for path in itertools.product(range(27), repeat=generation):
        for movement in moves:
            yield {'generation': generation, 'path': path,
                   'movement': movement, 'shell': shell(movement)}

def verify(max_generation=2):
    total = 0
    by_stage = []
    hasher = hashlib.sha256()
    witness = {'vector': [1, 0, 0, 1], 'kind': 'bridge-only',
               'status': 'frozen-root-not-certified'}
    frozen_witness = json.dumps(witness, sort_keys=True)
    for g in range(max_generation + 1):
        seen = set()
        completed = 0
        for task in stage(g):
            key = (task['path'], task['movement'])
            assert key not in seen
            seen.add(key)
            completed += 1
            hasher.update(json.dumps(task, sort_keys=True).encode() + b'\n')
            assert json.dumps(witness, sort_keys=True) == frozen_witness
        expected = 26 * 27 ** g
        assert completed == expected
        by_stage.append({'generation': g, 'tensor_cells': 27 ** g,
                         'scheduled_moves': expected, 'completed_moves': completed})
        total += completed
    return {'status': 'finite-prefix-verified',
            'max_generation': max_generation, 'total_tasks': total,
            'stages': by_stage,
            'ordered_task_stream_sha256': hasher.hexdigest(),
            'proof': 'Every finite depth g has 26*27^g tasks and is fully serviced before depth g+1.',
            'caveat': 'No claim of infinite physical execution or a frozen eighteenth-root witness.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generations', type=int, default=2)
    args = parser.parse_args()
    assert 0 <= args.generations <= 3, 'Use <=3 generations for bounded replay.'
    print(json.dumps(verify(args.generations), indent=2))
