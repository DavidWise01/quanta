#!/usr/bin/env python3
"""ADA-076 exact topology, five-beat dynamics, and immutable replay tests."""
from collections import Counter
import json
import tempfile
import unittest
from pathlib import Path
from ada076_living import (PHASES, mesh, energy, initial_state, witnesses,
    propose, simulate, verify, export, ascii_view, digest)

class LivingKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = mesh()
        cls.events = simulate(25)

    def test_exact_polyhedron_counts(self):
        self.assertEqual((len(self.m['vertices']), len(self.m['edges']),
                          len(self.m['triangles']),len(self.m['pentagons'])),
                         (30,60,20,12))
    def test_icosidodecahedron_euler(self):
        self.assertEqual(30-60+(20+12),2)
    def test_every_vertex_has_four_neighbors(self):
        self.assertTrue(all(len(x)==4 for x in self.m['adjacency']))
    def test_each_edge_triangle_and_pentagon(self):
        self.assertEqual(set(self.m['edges']),set(self.m['edge_triangle']))
        self.assertEqual(set(self.m['edges']),set(self.m['edge_pentagon']))
    def test_face_sizes_and_uniqueness(self):
        self.assertTrue(all(len(set(t))==3 for t in self.m['triangles']))
        self.assertTrue(all(len(set(p))==5 for p in self.m['pentagons']))
        self.assertEqual(len(set(map(frozenset,self.m['triangles']))),20)
        self.assertEqual(len(set(map(frozenset,self.m['pentagons']))),12)
    def test_balanced_ternary_genesis(self):
        self.assertEqual(Counter(initial_state()),Counter({-1:10,0:10,1:10}))
    def test_five_beat_schedule(self):
        self.assertEqual(PHASES,('I','I','E','E','E'))
        self.assertEqual([e['meta']['phase'] for e in self.events[1:11]],list(PHASES)*2)
    def test_state_domain_and_histograms(self):
        for e in self.events:
            self.assertEqual(Counter(e['state']),Counter(initial_state()))
            self.assertEqual(sum(e['state']),0)
    def test_moves_are_disjoint_and_limited(self):
        for e in self.events[1:]:
            moves=e['meta']['moves']
            self.assertLessEqual(len(moves),4)
            used=[v for m in moves for v in m['edge']]
            self.assertEqual(len(used),len(set(used)))
    def test_every_move_has_local_face_context(self):
        for e in self.events[1:]:
            for move in e['meta']['moves']:
                self.assertIn(tuple(move['edge']), self.m['edges'])
                self.assertEqual(len(move['witness_before']),3)
                self.assertEqual(len(move['witness_after']),3)
                self.assertGreaterEqual(move['pentagon'],0)
    def test_edges_actually_move(self):
        self.assertGreater(sum(len(e['meta']['moves']) for e in self.events[1:]),10)
        self.assertNotEqual(self.events[0]['state'],self.events[-1]['state'])
    def test_tamper_detected(self):
        cloned=json.loads(json.dumps(self.events))
        cloned[14]['state'][0] *= -1
        with self.assertRaises(ValueError): verify(cloned)
    def test_missing_generation_detected(self):
        with self.assertRaises(ValueError):verify(self.events[:4]+self.events[5:])
    def test_provenance_not_fake_independent_witnesses(self):
        self.assertEqual(len({e['ancestry'] for e in self.events}),1)
        self.assertEqual(len(witnesses(initial_state(),self.m)),20)
    def test_deterministic_replay(self):
        self.assertEqual(simulate(25),self.events)
        self.assertTrue(verify(self.events))
    def test_exclusive_archive(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'generations.jsonl'
            export(p,self.events)
            saved=p.read_bytes()
            with self.assertRaises(FileExistsError):export(p,self.events)
            self.assertEqual(saved,p.read_bytes())
            self.assertTrue(verify([json.loads(s) for s in p.read_text().splitlines()]))
    def test_ascii_has_math_and_final_hash(self):
        text=ascii_view(self.events)
        for k in ('30 VERTICES','60 EDGES','20 TRIANGLES','12 PENTAGONS',
                  'EULER = 30-60+(20+12) = 2',self.events[-1]['hash']):
            self.assertIn(k,text)
    def test_empty_and_large_steps_rejected(self):
        with self.assertRaises(ValueError):simulate(-1)
        with self.assertRaises(ValueError):simulate(10001)
        self.assertTrue(verify(simulate(0)))

if __name__=='__main__':
    unittest.main()
