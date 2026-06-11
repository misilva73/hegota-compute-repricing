#!/usr/bin/env python3
"""Per-operation worst-case throughput (Mgas/s) → committed ``data/bottlenecks.csv``.

Heavy step: reads the gitignored ``data/raw/bench_data.parquet`` (~80 MB) and writes a
small COMMITTED CSV that ``build_site.py`` renders. Kept out of ``make site`` so the
site always builds from committed artifacts only.

Worst-case logic — "slowest binds" throughout (throughput, so worst = slowest = min):

* per (operation, fixture, client): **p1** of ``test_mgas_s`` (the slow tail, robust to
  the single worst run);
* per (operation, client): **min** over that operation's fixtures;
* per operation: **min** over clients *eligible for the worst case* — every client's
  per-client value is kept and shown, but ``WORST_CASE_EXCLUDE`` clients (ethrex) do
  not get to set the binding worst case. The fit side mirrors this (run_gasfit.py).

Restricted to the 300M-gas fixtures and to the **compute operations** (the opcode set
the ``fit.yaml`` presets target). An operation is a *bottleneck* when its worst-case
throughput is below the 100 Mgas/s anchor — it cannot be repriced cheaper than a plain
transfer. State/IO ops (SLOAD/SSTORE/CALL/LOG/CREATE/…), which are the real sub-100
ops, are out of scope and never appear here.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PARQUET = ROOT / "data" / "raw" / "bench_data.parquet"
NEW_GAS = ROOT / "data" / "gasfit" / "new_gas.csv"
OUT_CSV = ROOT / "data" / "bottlenecks.csv"

BLOCK_LIMIT = 300          # focus on the 300M-gas fixtures
ANCHOR_MGAS = 100.0        # assumed eth-transfer throughput ceiling
PERCENTILE = 0.01          # p1 per fixture (the slow end of the run distribution)

# Clients shown per-op but excluded from the worst-case (min) over clients.
# Mirrors run_gasfit.py's WORST_CASE_EXCLUDE — keep the two in sync.
WORST_CASE_EXCLUDE = {"ethrex"}

# Compute operations only (matches fit.yaml's preset selection), keyed by the raw
# benchmark opcode mnemonic → display category. Numbered stack variants collapse to
# their root (PUSH/DUP/SWAP) via ``normalize_opcode``. State/IO families are absent.
_COMPUTE_CATEGORY: dict[str, str] = {
    op: cat
    for cat, ops in {
        "Arithmetic": "ADD SUB MUL DIV SDIV SIGNEXTEND EXP MOD SMOD ADDMOD MULMOD".split(),
        "Bitwise": "AND OR XOR BYTE SHL SHR SAR NOT CLZ".split(),
        "Comparison": "LT GT SLT SGT EQ ISZERO".split(),
        "Stack": "PUSH0 PUSH DUP SWAP".split(),
        "Control flow": "JUMP JUMPI JUMPDEST PC GAS".split(),
        "Block/tx": (
            "BASEFEE BLOBBASEFEE CHAINID COINBASE GASLIMIT NUMBER "
            "PREVRANDAO TIMESTAMP GASPRICE ORIGIN".split()
        ),
        "Call context": (
            "ADDRESS CALLER CALLVALUE CALLDATALOAD CALLDATASIZE "
            "RETURNDATASIZE CALLDATACOPY RETURNDATACOPY".split()
        ),
        "Memory": "MLOAD MSTORE MSTORE8 MSIZE MCOPY".split(),
        "Hashing": ["KECCAK256"],
        "Precompile": (
            "ECRECOVER SHA2-256 RIPEMD-160 IDENTITY BLAKE2F P256VERIFY "
            "POINT_EVALUATION ECADD ECMUL ECPAIRING".split()
        ),
        "BLS12-381": (
            "BLS12_G1ADD BLS12_G2ADD BLS12_MAP_FP_TO_G1 BLS12_MAP_FP_TO_G2 "
            "BLS12_G1MSM BLS12_G2MSM".split()
        ),
    }.items()
    for op in ops
}

# new_gas.csv records precompile opcodes without the EEST hyphenation.
_OPCODE_ALIAS = {"SHA2-256": "SHA256", "RIPEMD-160": "RIPEMD160"}


def normalize_opcode(op: str) -> str:
    """PUSH6→PUSH, DUP2→DUP, SWAP4→SWAP; PUSH0 is its own op; others pass through."""
    if op != "PUSH0" and re.fullmatch(r"(PUSH|DUP|SWAP)\d+", op):
        return re.sub(r"\d+$", "", op)
    return op


def gas_params_by_opcode() -> dict[str, list[str]]:
    """Operation → fitted ``gas_param``s, from new_gas.csv (drives the reprice join).

    Empty when new_gas.csv is absent. Keys use the benchmark mnemonic (e.g.
    ``SHA2-256``) so they line up with the table's opcode column.
    """
    if not NEW_GAS.exists():
        return {}
    df = pd.read_csv(NEW_GAS).dropna(subset=["selected_opcode"])
    inv_alias = {v: k for k, v in _OPCODE_ALIAS.items()}
    out: dict[str, list[str]] = {}
    for _, r in df.iterrows():
        op = normalize_opcode(str(r["selected_opcode"]))
        op = inv_alias.get(op, op)
        out.setdefault(op, []).append(str(r["gas_param"]))
    return out


def main() -> None:
    if not PARQUET.exists():
        sys.exit(f"{PARQUET} missing — run `make fetch` first.")
    df = pd.read_parquet(PARQUET)
    if "test_mgas_s" not in df.columns:
        sys.exit(
            "test_mgas_s missing from bench_data.parquet — re-run `make fetch` with "
            "`metrics: [runtime, mgas_s]` in fetch.yaml."
        )

    df = df[["client_name", "test_title", "test_opcode", "block_limit_million", "test_mgas_s"]]
    df = df[df["block_limit_million"] == BLOCK_LIMIT].dropna(subset=["test_mgas_s"])
    df["operation"] = df["test_opcode"].astype(str).map(normalize_opcode)
    df = df[df["operation"].isin(_COMPUTE_CATEGORY)]
    if df.empty:
        sys.exit(f"No compute fixtures at block_limit_million == {BLOCK_LIMIT}.")

    # p1 per fixture/client → min over fixtures → (later) min over clients.
    p1 = (
        df.groupby(["operation", "test_title", "client_name"])["test_mgas_s"]
        .quantile(PERCENTILE)
        .reset_index(name="mgas_s")
    )
    per_client = p1.groupby(["operation", "client_name"])["mgas_s"].min().reset_index()
    clients = sorted(per_client["client_name"].unique())
    wide = per_client.pivot(index="operation", columns="client_name", values="mgas_s").reindex(
        columns=clients
    )

    # Worst case = min over the eligible clients only; excluded clients are still
    # reported per-op below, they just don't get to bind the worst case.
    worst_clients = [c for c in clients if c not in WORST_CASE_EXCLUDE]
    if not worst_clients:
        sys.exit(f"No clients left after excluding {sorted(WORST_CASE_EXCLUDE)}.")

    gp = gas_params_by_opcode()
    out = pd.DataFrame({"opcode": wide.index})
    out["category"] = out["opcode"].map(_COMPUTE_CATEGORY)
    out["worst_mgas_s"] = wide[worst_clients].min(axis=1, skipna=True).values
    for c in clients:
        out[f"mgas_s_{c}"] = wide[c].values
    out["gas_params"] = out["opcode"].map(lambda o: ";".join(gp.get(o, [])))
    out["below_anchor"] = out["worst_mgas_s"] < ANCHOR_MGAS
    out = out.sort_values("worst_mgas_s").reset_index(drop=True)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False, float_format="%.3f")
    n_below = int(out["below_anchor"].sum())
    excluded = [c for c in clients if c in WORST_CASE_EXCLUDE]
    excl_note = f"; excluded from worst case: {', '.join(excluded)}" if excluded else ""
    print(
        f"Wrote {len(out)} compute ops → {OUT_CSV} "
        f"({n_below} below {ANCHOR_MGAS:.0f} Mgas/s, "
        f"worst-case clients: {', '.join(worst_clients)}{excl_note})"
    )


if __name__ == "__main__":
    main()
