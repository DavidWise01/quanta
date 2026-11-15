#!/usr/bin/env python3
"""ADA-064: read-only exact finite-orbit observer."""
import json
from ada055_candidates import hash_payload
from ada063_external_replay import evaluate, evolve

REFERENCE="https://mathworld.wolfram.com/MandelbrotSet.html"

def observe():
    upstream=evaluate()
    if upstream["external_definition"]["source_url"]!=REFERENCE:
        raise ValueError("source mismatch")
    records=[]
    for item in upstream["results"]:
        actual=[list(map(str,p)) for p in evolve(item["parameter"],len(item["expected"]))]
        row={"name":item["name"],"parameter":item["parameter"],
             "upstream_digest":item["digest"],"actual":actual,
             "finite_replay_pass":actual==item["expected"]==item["actual"],
             "source_root":"quanta-owned:derived-observer"}
        row["digest"]=hash_payload(row)
        records.append(row)
    report={"version":"ADA064-v1","external_definition":REFERENCE,
            "fixture_ancestry":"quanta-owned:authored-fixtures",
            "observer_ancestry":"quanta-owned:derived-observer",
            "observations":records,
            "passes":sum(r["finite_replay_pass"] for r in records),
            "total":len(records),"independent_empirical_witnesses":0,
            "physical_coupling_tested":False,"promotion":"abstain"}
    report["digest"]=hash_payload(report)
    return report

if __name__=="__main__":
    print(json.dumps(observe(),indent=2))
