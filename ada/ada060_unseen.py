#!/usr/bin/env python3
"""ADA-060: frozen selector challenged by separate synthetic oracle.

All candidate evaluations and failures are retained in the report.
Never appends to the scheduled operational evidence ledger.
"""
import json
from ada059_select import PARENTS, propose, choose, VERSION as SELECTOR_VERSION
from ada055_candidates import MANIFOLD, SINGLET, hash_payload
from ada060_oracle import challenge, RULE_VERSION, SOURCE_ROOT


def run():
    cases = []
    for index, parent in enumerate(PARENTS):
        root, candidates = propose(parent)
        selected = choose(candidates, True)  # untouched ADA-059 selector
        if selected is None:
            raise ValueError("frozen selector had no passing candidate")
        challenge_results = []
        for c in candidates:
            result = challenge(c["state"])  # intentionally NO history evidence
            challenge_results.append({
                "candidate_root": c["candidate_root"],
                "factor": c["factor"],
                "preselection_full_envelope": c["all_pass"],
                **result
            })
        result_by_root = {x["candidate_root"]: x for x in challenge_results}
        result = result_by_root[selected["candidate_root"]]
        cases.append({
            "case": index, "parent_root": root, "selected_root": selected["candidate_root"],
            "selected_factor": selected["factor"], "selected_state": selected["state"],
            "selected_result": result,
            "all_candidate_challenges": challenge_results,
            "decision": result["promotion"],
        })
    report = {
        "selector_version": SELECTOR_VERSION,
        "challenge_version": RULE_VERSION,
        "source_ancestry": SOURCE_ROOT,
        "manifold": MANIFOLD,
        "singlet": SINGLET,
        "cases": cases,
        "known_challenge_passes": sum(c["selected_result"]["known_pass"] for c in cases),
        "rejections": sum(c["decision"] == "reject" for c in cases),
        "abstentions": sum(c["decision"] == "abstain" for c in cases),
        "promotions": sum(c["decision"] == "eligible" for c in cases),
        "caveat": "No independent source witnesses or measured replay supplied",
    }
    report["root"] = hash_payload(report)
    return report


if __name__ == "__main__":
    result = run()
    print(json.dumps({
        "cases": len(result["cases"]), "known_passes":result["known_challenge_passes"],
        "rejections":result["rejections"],"abstentions":result["abstentions"],
        "promotions":result["promotions"],
        "selected": [{k:c[k] for k in ("case","selected_factor","selected_state","decision")}
                     for c in result["cases"]],"root":result["root"]
    }, indent=2))
