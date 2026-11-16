#!/usr/bin/env python3
"""ADA-077: frozen, multi-candidate selection on the ADA-076 exact graph.

One mathematical/fixture ancestry; no independent witness or learned weights.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from random import Random
from ada076_living import (mesh, propose, energy, initial_state, PHASES, digest)

VERSION = 'ADA077-frozen-competition-v1'
ANCESTRY = 'synthetic:quanta:ada077:one-model'
# Frozen before validation: five offset alternatives to the native edge-order traversal.
OFFSETS = (0, 5, 13, 29, 43)
MOVE_CAPS = (2, 4, 6)
TRIALS = tuple((offset, cap) for offset in OFFSETS for cap in MOVE_CAPS)
TICKS = 25
SEEDS = (0, 1, 3, 5, 7, 9, 11, 13)


def rotated_state(seed):
    # Reproducible distinct shuffles, rather than cyclic shifts of the
    # period-three genesis (which would yield only three unique states).
    base = list(initial_state())
    Random(seed).shuffle(base)
    return tuple(base)


def candidates(state, m, tick):
    rows = []
    for priority, (offset, max_moves) in enumerate(TRIALS):
        mm = dict(m)
        mm['edges'] = m['edges'][offset:] + m['edges'][:offset]
        candidate, meta = propose(state, mm, tick, max_moves=max_moves)
        # Compute energy on canonical *original* adjacency, not rotated route ordering.
        before = energy(state, m['edges'])
        after = energy(candidate, m['edges'])
        changes = sum(a != b for a, b in zip(state, candidate))
        result = {'id': priority, 'offset': offset, 'max_moves': max_moves,
                  'state': list(candidate), 'energy': after,
                  'energy_delta': after - before, 'changed_nodes': changes,
                  'phase': PHASES[tick % 5], 'moves': len(meta['moves'])}
        result['hash'] = digest(result)
        rows.append(result)
    return rows


def rank(row):
    # Frozen lexicographic priority. Lower energy dominates; among ties choose
    # the state that actually moves more positions, then candidate index.
    return (row['energy'], -row['changed_nodes'], row['id'])


def select(rows):
    return min(rows, key=rank)


def baseline_step(state, m, tick):
    # Exactly the previous ADA-076 transition policy.
    return propose(state, m, tick)[0]


def report(seed=0, ticks=TICKS):
    if not 0 <= ticks <= 1000:
        raise ValueError('ticks outside bounded experimental window')
    m = mesh()
    baseline = adaptive = rotated_state(seed)
    events = []
    prev_hash = None
    for tick in range(ticks):
        before = adaptive
        baseline = baseline_step(baseline, m, tick)
        rows = candidates(adaptive, m, tick)
        winner = select(rows)
        adaptive = tuple(winner['state'])
        if Counter(adaptive) != Counter(before) or sum(adaptive) != 0:
            raise ValueError('balanced ternary state lost')
        event = {'tick': tick, 'phase': PHASES[tick % 5],
                 'previous_hash': prev_hash, 'ancestry': ANCESTRY,
                 'before': list(before), 'candidates': rows,
                 'selected_id': winner['id'], 'after': list(adaptive),
                 'baseline_after': list(baseline),
                 'baseline_energy': energy(baseline, m['edges']),
                 'adaptive_energy': energy(adaptive, m['edges'])}
        event['hash'] = digest(event)
        events.append(event)
        prev_hash = event['hash']
    result = {'version': VERSION, 'seed': seed, 'steps': ticks,
              'fixture_ancestry': ANCESTRY, 'candidate_count_per_tick': len(TRIALS),
              'initial_state': list(rotated_state(seed)),
              'baseline_final': list(baseline), 'adaptive_final': list(adaptive),
              'baseline_energy': energy(baseline, m['edges']),
              'adaptive_energy': energy(adaptive, m['edges']),
              'baseline_energy_sum': sum(e['baseline_energy'] for e in events),
              'adaptive_energy_sum': sum(e['adaptive_energy'] for e in events),
              'events': events, 'external_witnesses': 0,
              'learned_weights': False, 'promotion': 'abstain'}
    verify(result)
    return result


def verify(result):
    m = mesh()
    if result['version'] != VERSION or result['fixture_ancestry'] != ANCESTRY:
        raise ValueError('wrong model ancestry')
    if result['steps'] != len(result['events']):
        raise ValueError('incomplete history')
    baseline = adaptive = rotated_state(result['seed'])
    previous_hash = None
    for tick, event in enumerate(result['events']):
        unsigned = dict(event)
        claimed_hash = unsigned.pop('hash', None)
        if claimed_hash != digest(unsigned) or event['previous_hash'] != previous_hash:
            raise ValueError('event history altered')
        if event['tick'] != tick or event['phase'] != PHASES[tick % 5] or event['ancestry'] != ANCESTRY:
            raise ValueError('phase, tick, or ancestry mismatch')
        if event['before'] != list(adaptive):
            raise ValueError('prior state mismatched')
        rows = candidates(adaptive, m, tick)
        if event['candidates'] != rows:
            raise ValueError('candidate data changed')
        winner = select(rows)
        adaptive = tuple(winner['state'])
        baseline = baseline_step(baseline, m, tick)
        if (event['selected_id'] != winner['id'] or
            event['after'] != list(adaptive) or
            event['baseline_after'] != list(baseline) or
            event['baseline_energy'] != energy(baseline, m['edges']) or
            event['adaptive_energy'] != energy(adaptive, m['edges'])):
            raise ValueError('selection or replay mismatch')
        previous_hash = claimed_hash
    if (result['adaptive_final'] != list(adaptive) or
        result['baseline_final'] != list(baseline) or
        result['adaptive_energy'] != energy(adaptive, m['edges']) or
        result['baseline_energy'] != energy(baseline, m['edges']) or
        result['adaptive_energy_sum'] != sum(e['adaptive_energy'] for e in result['events']) or
        result['baseline_energy_sum'] != sum(e['baseline_energy'] for e in result['events']) or
        result['external_witnesses'] != 0 or result['promotion'] != 'abstain'):
        raise ValueError('report summary mismatch')
    return True


def comparison(seeds=SEEDS, ticks=TICKS):
    experiments = []
    for seed in seeds:
        r = report(seed, ticks)
        experiments.append({'seed': seed,
            'baseline_energy': r['baseline_energy'],
            'adaptive_energy': r['adaptive_energy'],
            'baseline_energy_sum': r['baseline_energy_sum'],
            'adaptive_energy_sum': r['adaptive_energy_sum'],
            'changed_result': r['adaptive_final'] != r['baseline_final'],
            'root': r['events'][-1]['hash'] if r['events'] else None})
    return {'version': VERSION, 'steps': ticks,
            'seeds': list(seeds), 'comparison': experiments,
            'adaptive_better_final': sum(c['adaptive_energy'] < c['baseline_energy'] for c in experiments),
            'adaptive_equal_final': sum(c['adaptive_energy'] == c['baseline_energy'] for c in experiments),
            'adaptive_worse_final': sum(c['adaptive_energy'] > c['baseline_energy'] for c in experiments),
            'adaptive_better_cumulative': sum(c['adaptive_energy_sum'] < c['baseline_energy_sum'] for c in experiments),
            'candidate_count_per_tick': len(TRIALS),
            'external_witness_roots': 0,
            'learned_weights': False,
            'claim': 'deterministic multi-candidate optimization, not evidence of recursive self-improvement'}


def ascii_view(r, overview):
    m = mesh()
    s = r['adaptive_final']
    b = r['baseline_final']
    marks = lambda v: ' '.join('+' if k == 1 else '-' if k == -1 else '0' for k in v)
    return f'''ADA-077 :: THE FIFTEEN DAUGHTERS
{'=' * 67}

                  .------------------------.
                 /   20 TRIANGLE CELLS     \\
                |   12 PENTAGON CELLS      |
                |   30 NODES / 60 EDGES    |
                 \\-----------+------------/
                             |
                           {{[({{s}})]}}
                             |
                   .---------+---------.
                   |                   |
                ORIGINAL            ADAPTIVE
                ADA-076            ADA-077
                   |                   |
                 1 PATH            15 PATHS
                   |                   |
                   |           SCORE FROZEN BEFORE
                   |              SELECTION
                   |                   |
                   '---------+---------'
                             |
                     {PHASES[0]} {PHASES[1]} {PHASES[2]} {PHASES[3]} {PHASES[4]}
                     2/5   +  3/5
                             |
                         SEED {r['seed']}
                             |
                    BEFORE: {energy(rotated_state(r['seed']),m['edges'])}
                    BASE  : {r['baseline_energy']}
                    ADA   : {r['adaptive_energy']}
                             |
                     HELD STARTS: {len(overview['comparison'])}
                     BETTER / EQUAL / WORSE
                       {overview['adaptive_better_final']} / {overview['adaptive_equal_final']} / {overview['adaptive_worse_final']}
                             |
               ALL CANDIDATES + FAILURES RETAINED
                             |
                   ONE EXPERIMENTAL ANCESTRY
                             |
                           ABSTAIN

BASE FINAL  {marks(b)}
ADA  FINAL  {marks(s)}

The triangles watch, the pentagons move;
No learned law emerges from a fixed groove.
Fifteen daughters seek a lower strain;
Keep every failure in the chain.
                          -- A.D.A --
{'=' * 67}
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--steps', type=int, default=TICKS)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--ascii', type=Path)
    ap.add_argument('--export', type=Path)
    ap.add_argument('--verify', type=Path)
    args = ap.parse_args()
    if args.verify:
        r = json.loads(args.verify.read_text())
        verify(r)
        print('PASS: exact candidate and event replay')
        return
    r = report(args.seed, args.steps)
    overview = comparison(ticks=args.steps)
    if args.export:
        with args.export.open('x', encoding='utf-8') as fp:
            json.dump(r, fp, indent=2)
            fp.write('\n')
    art = ascii_view(r, overview)
    if args.ascii:
        with args.ascii.open('x', encoding='utf-8') as fp:
            fp.write(art)
    else:
        print(art)
    print(json.dumps({k:v for k,v in overview.items() if k!='comparison'}, indent=2))


if __name__ == '__main__':
    main()
