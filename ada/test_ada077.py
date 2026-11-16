#!/usr/bin/env python3
"""ADA-077 regression checks for topology, candidate selection and history."""
import copy
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from ada076_living import initial_state, mesh, energy, PHASES
from ada077_selection import (TRIALS, SEEDS, rotated_state, candidates, select, rank,
                              report, verify, comparison, ascii_view, baseline_step)


class LivingCompetitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = mesh()
        cls.first = report(0,25)
        cls.multi = comparison()

    def test_icosidodecahedron_counts(self):
        self.assertEqual((len(self.m['vertices']),len(self.m['edges']),
                          len(self.m['triangles']),len(self.m['pentagons'])),
                         (30,60,20,12))
        self.assertEqual(30-60+20+12,2)

    def test_distinct_starting_states(self):
        states = [rotated_state(i) for i in SEEDS]
        self.assertEqual(len(set(states)),len(SEEDS))
        self.assertTrue(all(Counter(x)==Counter(initial_state()) for x in states))

    def test_frozen_fifteen_candidates(self):
        self.assertEqual(len(TRIALS),15)
        self.assertEqual(TRIALS[0],(0,2))
        self.assertEqual(TRIALS[-1],(43,6))

    def test_phase_schedule(self):
        self.assertEqual(PHASES,('I','I','E','E','E'))
        self.assertEqual([x['phase'] for x in self.first['events'][:5]],list(PHASES))

    def test_all_candidate_states_preserve_inventory(self):
        for e in self.first['events']:
            before=Counter(e['before'])
            for row in e['candidates']:
                self.assertEqual(Counter(row['state']),before)
                self.assertEqual(sum(row['state']),0)

    def test_candidates_have_hash_and_failures(self):
        for e in self.first['events']:
            self.assertEqual(len(e['candidates']),15)
            self.assertEqual(len({x['id'] for x in e['candidates']}),15)
            self.assertIn(e['selected_id'],range(15))

    def test_frozen_rank(self):
        for e in self.first['events']:
            chosen=next(x for x in e['candidates'] if x['id']==e['selected_id'])
            self.assertEqual(rank(chosen),min(map(rank,e['candidates'])))

    def test_energy_matches_canonical_mesh(self):
        for e in self.first['events']:
            self.assertEqual(e['adaptive_energy'],energy(e['after'],self.m['edges']))
            self.assertEqual(e['baseline_energy'],energy(e['baseline_after'],self.m['edges']))

    def test_state_history_replays(self):
        self.assertTrue(verify(self.first))
        self.assertEqual(self.first['steps'],25)

    def test_tampered_candidate_rejected(self):
        falsified=copy.deepcopy(self.first)
        falsified['events'][2]['candidates'][0]['energy']+=1
        with self.assertRaises(ValueError):verify(falsified)

    def test_tampered_selection_rejected(self):
        falsified=copy.deepcopy(self.first)
        falsified['events'][4]['selected_id']=99
        with self.assertRaises(ValueError):verify(falsified)

    def test_missing_event_rejected(self):
        falsified=copy.deepcopy(self.first)
        del falsified['events'][3]
        with self.assertRaises(ValueError):verify(falsified)

    def test_baseline_original_policy_unchanged(self):
        state=rotated_state(0)
        for tick in range(25):
            state=baseline_step(state,self.m,tick)
        self.assertEqual(list(state),self.first['baseline_final'])

    def test_score_has_counterexample(self):
        self.assertEqual(self.multi['adaptive_better_final'],7)
        self.assertEqual(self.multi['adaptive_worse_final'],1)
        self.assertEqual(self.multi['adaptive_equal_final'],0)
        self.assertGreater(self.multi['comparison'][0]['adaptive_energy'],
                           self.multi['comparison'][0]['baseline_energy'])

    def test_cumulative_better_in_this_fixture(self):
        self.assertEqual(self.multi['adaptive_better_cumulative'],8)

    def test_no_claim_of_learning(self):
        self.assertFalse(self.multi['learned_weights'])
        self.assertEqual(self.multi['external_witness_roots'],0)
        self.assertEqual(self.first['promotion'],'abstain')

    def test_ascii_contains_counterexample(self):
        visual=ascii_view(self.first,self.multi)
        self.assertIn('7 / 0 / 1',visual)
        self.assertIn('15 PATHS',visual)
        self.assertIn('ABSTAIN',visual)

    def test_deterministic(self):
        self.assertEqual(report(0,3),report(0,3))
        self.assertEqual(comparison(ticks=2),comparison(ticks=2))


if __name__=='__main__':
    unittest.main()
