#!/usr/bin/env python3
"""ADA-063 external-definition replay: exact quadratic-map orbit checks.

The recurrence is externally documented, but input fixtures and expected
outputs are authored within Quanta. No external witness is authenticated.
"""
from fractions import Fraction as F
import json
from ada055_candidates import hash_payload, MANIFOLD, SINGLET

SOURCE = {
    "source_url": "https://mathworld.wolfram.com/MandelbrotSet.html",
    "source_title": "Mandelbrot Set (Wolfram MathWorld)",
    "source_role": "published mathematical definition",
    "definition": "z_(n+1)=z_n^2+c, z_0=0",
}
# These exact finite-orbit examples are Quanta-authored test fixtures,
# not data extracted from or certified by the external page.
FIXTURES = (
    ("zero", (0,0), ((0,0),(0,0),(0,0),(0,0))),
    ("one", (1,0), ((0,0),(1,0),(2,0),(5,0))),
    ("minus_one", (-1,0), ((0,0),(-1,0),(0,0),(-1,0))),
    ("imaginary_i", (0,1), ((0,0),(0,1),(-1,1),(0,-1))),
    ("minus_two", (-2,0), ((0,0),(-2,0),(2,0),(2,0))),
)
EXPERIMENT="ADA063-exact-orbit-v1"
SOURCE_ANCESTRY="quanta-owned:fixture-authored"


def evolve(parameter, count=4):
    cr,ci = (F(v) for v in parameter)
    zr=zi=F(0)
    trace=[(zr,zi)]
    for _ in range(count-1):
        zr, zi = zr*zr-zi*zi+cr, 2*zr*zi+ci
        trace.append((zr,zi))
    return tuple(trace)


def evaluate():
    results=[]
    for name,c,expected in FIXTURES:
        actual=evolve(c,len(expected))
        passed=actual==tuple(tuple(map(F,p)) for p in expected)
        body={
            "name":name, "parameter":[str(x) for x in c],
            "expected":[list(map(str,p)) for p in expected],
            "actual":[list(map(str,p)) for p in actual],
            "pass":passed, "source_ancestry":SOURCE_ANCESTRY,
        }
        body["digest"]=hash_payload(body)
        results.append(body)
    return {
        "experiment":EXPERIMENT,
        "external_definition":SOURCE,
        "external_definition_authored_by_quanta":False,
        "fixtures_authored_by_quanta":True,
        "source_independent_of_quanta_for_definition":True,
        "independent_empirical_witnesses":0,
        "manifold":MANIFOLD,
        "singlet":SINGLET,
        "results":results,
        "exact_orbit_passes":sum(r["pass"] for r in results),
        "total":len(results),
        "promotion":"abstain",
        "warning":"Finite exact-orbit agreement does not prove infinite-orbit boundedness, external independent witnessing or physical coupling."
    }


if __name__=="__main__":
    print(json.dumps(evaluate(),indent=2))
