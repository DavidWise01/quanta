#!/usr/bin/env python3
"""ADA-065: frozen orbit engine versus published external numeric references.

The reference values below are transcribed, source-attributed data, not
internally generated expected orbits. Finite tests are not physical witnesses.
"""
from datetime import datetime
from fractions import Fraction as F
import json
from ada063_external_replay import evolve
from ada055_candidates import hash_payload, MANIFOLD, SINGLET

CAPTURE_DATE="2026-11-15"  # source consultation date, not an archived web response
SOURCE_ROOTS={
  "OEIS_A003095":"https://oeis.org/A003095",
  "PLUS_MATHS":"https://plus.maths.org/comment/8560",
}
# Expected terms manually transcribed from cited published pages.
# Do not derive these by calling evolve().
PUBLISHED_CASES=(
  ("oeis_plus_one","OEIS_A003095", (1,0),
   (0,1,2,5,26,677,458330,210066388901)),
  ("plus_zero","PLUS_MATHS", (0,0), (0,0,0,0)),
  ("plus_minus_one","PLUS_MATHS",(-1,0),(0,-1,0,-1,0)),
  ("plus_plus_one","PLUS_MATHS",(1,0),(0,1,2,5,26)),
)
VERSION="ADA065-external-references-v1"


def verify():
    rows=[]
    for case,source,parameter,expected in PUBLISHED_CASES:
        actual=evolve(parameter,len(expected))
        expected_pairs=tuple((F(x),F(0)) for x in expected)
        matched=actual==expected_pairs
        row={
          "case":case, "source_key":source,"source_url":SOURCE_ROOTS[source],
          "parameter":[str(x) for x in parameter],
          "reference_values":[str(x) for x in expected],
          "computed_values":[str(x[0]) if x[1]==0 else str(x) for x in actual],
          "matched":matched,
          "source_capture_date":CAPTURE_DATE,
          "source_role":"published reference values",
          "reference_transcription":"manual",
          "code_ancestry":"quanta-owned",
        }
        row["digest"]=hash_payload(row)
        rows.append(row)
    summary={
      "version":VERSION,"manifold":MANIFOLD,"singlet":SINGLET,
      "sources":SOURCE_ROOTS,"cases":rows,
      "passing":sum(r["matched"] for r in rows),"total":len(rows),
      "distinct_external_publication_roots":len(SOURCE_ROOTS),
      "independent_empirical_witness_roots":0,
      "reference_capture_bytes_archived":False,
      "promotion":"abstain",
      "limitation":"Finite published sequences validate numeric implementation on examples, not physical coupling or independent empirical confirmation.",
    }
    summary["digest"]=hash_payload(summary)
    return summary


if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
