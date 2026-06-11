#!/usr/bin/env python3
"""Run the evm-gasfit pipeline, excluding some clients from the worst case.

Thin wrapper around what ``evm-gasfit run`` does (see ``evm_gasfit.cli._run``),
with one deviation: every configured client — ethrex included — is *fitted* and
appears on the runtime/glue pages, but the across-client worst-case proposal
(``new_gas.csv``, ``new_gas_proposal.md``, ``new_gas_all_params.csv``, and any
derived params) is built from a results frame with ``WORST_CASE_EXCLUDE`` clients
dropped. So ethrex's (slower) numbers are still visible but never set a proposed
gas cost. This mirrors the bottleneck side, which excludes the same clients from
its worst-case throughput (scripts/build_bottlenecks.py — keep the sets in sync).

This is why ``make gasfit`` calls this script instead of the ``evm-gasfit`` CLI.
The exclusion uses evm-gasfit's public ``build_proposal``; if a version bump
changes that signature, this wrapper (not the CLI) is what to re-check.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from evm_gasfit.api import GasFit
from evm_gasfit.proposal.build import build_proposal

# Clients fitted and shown on the site, but excluded from worst-case selection.
# Mirrors build_bottlenecks.py's WORST_CASE_EXCLUDE — keep the two in sync.
WORST_CASE_EXCLUDE = {"ethrex"}


def main() -> int:
    p = argparse.ArgumentParser(prog="run_gasfit")
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--runtimes", required=True, type=Path)
    p.add_argument("--opcounts", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()

    fit = GasFit.from_config(args.config)
    fit.load_runtimes(args.runtimes)
    fit.load_opcounts(args.opcounts)

    # Fit every configured client (ethrex included) so they all show up on the
    # runtime/glue pages and in results.csv...
    fit.estimate_models()
    if fit.config.glue_adjustment.enabled:
        fit.estimate_glue()

    # ...then build the proposal from the worst-case-eligible clients only, so an
    # excluded client never becomes the slowest (binding) client for a param.
    assert fit.estimate_output is not None  # populated by estimate_models()
    results = fit.estimate_output.results_df
    eligible = results[~results["client_name"].isin(WORST_CASE_EXCLUDE)]
    dropped = sorted(set(results["client_name"].astype(str)) & WORST_CASE_EXCLUDE)
    if dropped:
        print(
            f"Worst-case selection excludes {', '.join(dropped)} "
            f"(still fitted + shown); {eligible['client_name'].nunique()} "
            f"client(s) eligible."
        )
    fit.proposal_output = build_proposal(
        fit.config, eligible, fit.glue_estimate_output, fit.fixtures_df
    )

    fit.write_reports(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
