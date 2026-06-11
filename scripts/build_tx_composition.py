#!/usr/bin/env python3
"""Mainnet opcode composition + block-gas totals from Xatu → committed ``data/tx_*.csv``.

Manual/occasional step (``make composition``). Needs ``xatu_username``/``xatu_password``
in ``secrets.json`` (repo root). Reads two pre-aggregated CBT tables over a recent window
of whole hours:

* ``mainnet.fct_opcode_gas_by_opcode_hourly`` — per-opcode execution count and gas, one
  row per (hour, opcode). The *numerator* source: how often each opcode runs and the gas
  it burns. Precompiles never appear (they execute behind CALL, not as opcodes), so they
  carry no composition weight downstream.
* ``mainnet.fct_execution_gas_used_hourly`` — total block ``gas_used`` per hour. The
  *denominator* source: this is all gas the chain burns (opcode + the 21k intrinsic +
  calldata + memory + everything), so rounding-loss shares read against real block gas,
  not just the opcode slice.

Both tables live only behind the ``{cbt_cluster}`` macro and are **replicated across the
cluster's nodes**, so ``cluster('{cbt_cluster}', …)`` returns every row once per node
(3× today). We therefore ``GROUP BY`` the primary key and collapse the identical copies
with ``any()`` — never a raw ``sum()``, which would multiply by the replica count. The
tables also set ``force_primary_key``, so every query filters on ``hour_start_date_time``.

Window is configurable via env: ``XATU_DAYS`` (default 30) and ``XATU_END_HOUR``
(default = the gas table's latest hour). Hours with fewer than ``XATU_MIN_BLOCKS`` blocks
(default 250 ≈ a full 300-block hour) are dropped as partial.

Outputs (all committed; the rest of the pipeline and ``make site`` need no credentials):
* ``data/tx_composition.csv``        — window-aggregate opcode composition (summed over the
  hourly rows): one row per opcode with ``total_count``, ``total_gas``, ``weight``.
* ``data/tx_composition_hourly.csv`` — per (hour, opcode) count and gas; the per-hour
  opcode mix that ``compute_fracgas.py`` turns into the per-hour rounding-loss distribution.
* ``data/tx_block_gas_hourly.csv``   — per-hour total block ``gas_used`` (+ block count);
  the denominator for both the headline/sweep and the per-hour loss metrics.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "tx_composition.csv"
OUT_HOURLY_CSV = ROOT / "data" / "tx_composition_hourly.csv"
OUT_BLOCK_GAS_CSV = ROOT / "data" / "tx_block_gas_hourly.csv"
SECRETS = ROOT / "secrets.json"

XATU_URL = "https://clickhouse.xatu.ethpandaops.io:443/"
OPCODE_TABLE = "mainnet.fct_opcode_gas_by_opcode_hourly"
GAS_USED_TABLE = "mainnet.fct_execution_gas_used_hourly"
DAYS = int(os.environ.get("XATU_DAYS", "30"))
MIN_BLOCKS = int(os.environ.get("XATU_MIN_BLOCKS", "250"))


def _query(sql: str, auth: tuple[str, str]) -> pd.DataFrame:
    r = requests.post(XATU_URL, data=sql.encode(), auth=auth, timeout=300)
    if r.status_code != 200:
        sys.exit(f"Xatu query failed ({r.status_code}): {r.text[:300]}")
    return pd.read_csv(pd.io.common.StringIO(r.text), sep="\t")


def _scalar(sql: str, auth: tuple[str, str]) -> str:
    r = requests.post(XATU_URL, data=sql.encode(), auth=auth, timeout=300)
    if r.status_code != 200:
        sys.exit(f"Xatu query failed ({r.status_code}): {r.text[:300]}")
    return r.text.strip()


def main() -> None:
    if not SECRETS.exists():
        sys.exit(f"{SECRETS} missing — need xatu_username/xatu_password.")
    s = json.loads(SECRETS.read_text())
    try:
        auth = (s["xatu_username"], s["xatu_password"])
    except KeyError:
        sys.exit("secrets.json needs xatu_username and xatu_password.")

    end = os.environ.get("XATU_END_HOUR")
    if not end:
        end = _scalar(
            f"SELECT max(hour_start_date_time) FROM cluster('{{cbt_cluster}}', {GAS_USED_TABLE})",
            auth,
        )
    # Inclusive whole-hour window [end - DAYS, end]; literal datetimes so we never lean on a
    # subquery under force_primary_key.
    window = (
        f"hour_start_date_time BETWEEN toDateTime('{end}') - INTERVAL {DAYS} DAY "
        f"AND toDateTime('{end}')"
    )
    print(f"Aggregating mainnet composition over {DAYS} days of hours ending {end}…")

    # --- Denominator: total block gas per hour (drop partial hours) ----------
    gas = _query(
        f"""
        SELECT hour_start_date_time AS hour_start,
               any(total_gas_used) AS total_gas_used,
               any(block_count) AS block_count
        FROM cluster('{{cbt_cluster}}', {GAS_USED_TABLE}) FINAL
        WHERE {window}
        GROUP BY hour_start
        HAVING block_count >= {MIN_BLOCKS}
        ORDER BY hour_start
        FORMAT TabSeparatedWithNames
        """,
        auth,
    )
    if gas.empty:
        sys.exit("Empty block-gas result — check the window / table access.")
    valid_hours = set(gas["hour_start"])

    # --- Numerator: per (hour, opcode) execution count and gas ---------------
    hourly = _query(
        f"""
        SELECT hour_start_date_time AS hour_start,
               opcode,
               any(total_count) AS total_count,
               any(total_gas) AS total_gas
        FROM cluster('{{cbt_cluster}}', {OPCODE_TABLE}) FINAL
        WHERE {window}
        GROUP BY hour_start, opcode
        ORDER BY hour_start, total_count DESC
        FORMAT TabSeparatedWithNames
        """,
        auth,
    )
    if hourly.empty:
        sys.exit("Empty opcode result — check the window / table access.")
    # Keep only opcodes from the whole hours we kept a denominator for.
    hourly = hourly[hourly["hour_start"].isin(valid_hours)].reset_index(drop=True)

    # --- Window aggregate: sum the hourly rows per opcode --------------------
    agg = (
        hourly.groupby("opcode", as_index=False)[["total_count", "total_gas"]]
        .sum()
        .sort_values("total_count", ascending=False)
    )
    agg["weight"] = agg["total_count"] / agg["total_count"].sum()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(OUT_CSV, index=False)
    hourly.to_csv(OUT_HOURLY_CSV, index=False)
    gas.to_csv(OUT_BLOCK_GAS_CSV, index=False)

    total_op_gas = int(agg["total_gas"].sum())
    total_block_gas = int(gas["total_gas_used"].sum())
    print(
        f"Wrote {len(agg)} opcodes → {OUT_CSV.name}; "
        f"{len(hourly)} (hour, opcode) rows → {OUT_HOURLY_CSV.name}; "
        f"{len(gas)} hours → {OUT_BLOCK_GAS_CSV.name}. "
        f"Opcode gas {total_op_gas / 1e12:.2f} Tgas is "
        f"{100 * total_op_gas / total_block_gas:.0f}% of block gas {total_block_gas / 1e12:.2f} Tgas "
        f"(top: {', '.join(agg['opcode'].head(5))})"
    )


if __name__ == "__main__":
    main()
