#!/usr/bin/env python3
"""Throughput loss of three repricing scenarios → committed ``data/fracgas*.csv``.

Reads only committed inputs — ``fit.yaml`` (the anchor), ``data/gasfit/new_gas.csv`` (the
worst-case per-op runtime), ``data/gasfit/new_gas_proposal.md`` (today's gas cost), and the
``data/tx_*.csv`` mainnet composition — so ``make fracgas`` needs no credentials.

At a throughput anchor the *fair* per-op gas is the exact fractional cost
``exact = anchor_rate · runtime_ms / 1000`` — the price at which a block of that op runs at
exactly the anchor's Mgas/s. We compare three ways the protocol could actually charge it:

* **No reprice**  — keep today's integer cost (``current``).        loss = max(current − exact, 0)
* **Round**       — reprice to ``max(ceil(exact), 1)`` (integer ≥ 1). loss = ⌈exact⌉ − exact
* **Fractional**  — charge ``exact`` itself (fractional gas).         loss = 0  (the ideal)

"Loss" is the gas charged above the fair price; overcharging the cheap compute ops wastes
throughput (the gas limit binds before the real-time budget). Fractional pricing is loss-free
by construction, so it's the zero baseline the other two are measured against.

The no-reprice loss focuses on the **operations repricing makes cheaper**: only ops overcharged
today (``exact < current``) carry a loss. An op that repricing would make *more* expensive
(``exact > current``, underpriced today) is held at **zero loss** — it's undercharged, not
wasting throughput, and that undercharge never nets against another op's overcharge.

Two metrics:

* **Opcode-level** (unweighted, per fitted param): ``loss / charged`` — the share of the gas
  you pay for that op that is rounding/misprice waste. Round → ``(⌈exact⌉−exact)/⌈exact⌉``,
  no-reprice → ``max(current−exact, 0)/current`` (zero once a high anchor pushes exact above the
  current cost — those ops are underpriced, not wasting throughput).
* **Mainnet traffic** (gas-weighted): ``Σ wᵢ·lossᵢ / G`` where ``wᵢ`` = mainnet execution count
  of per-execution ("base") op i and ``G`` = **total block gas used** over the window — all gas
  the chain burns, including the 21k intrinsic and calldata, from
  ``fct_execution_gas_used_hourly``. So the loss reads as a share of real block gas. (When the
  block-gas file is absent we fall back to summed opcode gas, the narrower old denominator.)

Per-word/round/point coefficients are listed per-op but excluded from the weighted aggregate
(their weight depends on data sizes we don't model).

Outputs:
* ``fracgas.csv``            — one row per fitted gas param (both scenarios' loss + rate)
* ``fracgas_summary.csv``    — headline scalars (both metrics × scenarios) at the anchor
* ``fracgas_by_anchor.csv``  — the same scalars swept over a range of anchors
* ``fracgas_hourly.csv``     — per-hour weighted loss for both scenarios (when the hourly
  composition exists; feeds the per-hour loss distribution)
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from build_bottlenecks import normalize_opcode
from build_site import _category

ROOT = Path(__file__).resolve().parent.parent
NEW_GAS = ROOT / "data" / "gasfit" / "new_gas.csv"
PROPOSAL = ROOT / "data" / "gasfit" / "new_gas_proposal.md"
COMPOSITION = ROOT / "data" / "tx_composition.csv"
COMPOSITION_HOURLY = ROOT / "data" / "tx_composition_hourly.csv"
BLOCK_GAS_HOURLY = ROOT / "data" / "tx_block_gas_hourly.csv"
OUT = ROOT / "data"

# Anchors (Mgas/s) for the sweep chart. The configured anchor is added if missing.
SWEEP_MGAS = [10, *range(25, 325, 25)]
_PER_SUFFIXES = ("_PER_WORD", "_PER_ROUND", "_PER_POINT")
# Opcode names in the composition that differ from new_gas.csv's selected_opcode mnemonics.
_COMP_ALIAS = {"SHA3": "KECCAK256"}


def load_composition() -> tuple[dict[str, float], float]:
    """``(normalized opcode → execution count, summed opcode gas)`` over the window.

    The counts (summed across stack variants) weight each base op's loss. The summed opcode
    gas is only the *fallback* denominator, used when the block-gas file is missing.
    """
    if not COMPOSITION.exists():
        return {}, 0.0
    df = pd.read_csv(COMPOSITION)
    counts: dict[str, float] = {}
    for _, r in df.iterrows():
        op = normalize_opcode(_COMP_ALIAS.get(str(r["opcode"]), str(r["opcode"])))
        counts[op] = counts.get(op, 0.0) + float(r["total_count"])
    return counts, float(df["total_gas"].sum())


def load_hourly_composition() -> dict[str, dict[str, float]]:
    """``hour → {normalized opcode → execution count}``.

    Reads the optional ``tx_composition_hourly.csv`` (one row per hour × opcode). Returns
    ``{}`` when absent, so the per-hour loss chart simply doesn't render until the hourly
    composition has been fetched.
    """
    if not COMPOSITION_HOURLY.exists():
        return {}
    df = pd.read_csv(COMPOSITION_HOURLY)
    hours: dict[str, dict[str, float]] = {}
    for _, r in df.iterrows():
        op = normalize_opcode(_COMP_ALIAS.get(str(r["opcode"]), str(r["opcode"])))
        bucket = hours.setdefault(str(r["hour_start"]), {})
        bucket[op] = bucket.get(op, 0.0) + float(r["total_count"])
    return hours


def load_block_gas() -> tuple[dict[str, float], float]:
    """``(hour → total block gas_used, summed block gas)`` — the all-inclusive denominator.

    Total block gas (opcode + 21k intrinsic + calldata + memory + everything) from
    ``tx_block_gas_hourly.csv``. Returns ``({}, 0.0)`` when absent so callers fall back to
    the narrower opcode-gas denominator.
    """
    if not BLOCK_GAS_HOURLY.exists():
        return {}, 0.0
    df = pd.read_csv(BLOCK_GAS_HOURLY)
    per_hour = {str(r["hour_start"]): float(r["total_gas_used"]) for _, r in df.iterrows()}
    return per_hour, float(df["total_gas_used"].sum())


def load_current_gas() -> dict[str, int]:
    """Gas param → current protocol cost, parsed from the proposal markdown table.

    Powers the "no reprice" scenario: the loss if today's integer gas cost is kept. Params
    with a non-numeric current (e.g. ``new_params`` declared without a baseline) are skipped.
    """
    if not PROPOSAL.exists():
        return {}
    import re

    text = PROPOSAL.read_text()
    block = re.search(r"## Proposed gas parameters\n(.*?)(?=^## )", text, re.S | re.M)
    current: dict[str, int] = {}
    if not block:
        return current
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("| -"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] in ("Gas param", ""):
            continue
        try:
            current[cells[0]] = int(cells[1].replace(",", ""))
        except (IndexError, ValueError):
            continue
    return current


def _scenario_cols(runtime_ms: pd.Series, current: pd.Series, anchor_rate: float):
    """Per-row exact / round / no-reprice gas and losses at an anchor (gas/s).

    The no-reprice loss focuses on the **cost decreases**: an op whose fair price is below
    today's cost (``exact < current``) is overcharged, and keeping the current cost wastes
    throughput. An op that would get an *increase* (``exact > current``, underpriced today)
    is treated as **zero loss** rather than a negative offset — undercharging one op can't
    buy back the throughput another op wastes, so it never nets against the overcharges.
    """
    exact = anchor_rate * runtime_ms / 1000.0
    rounded = exact.apply(lambda e: max(math.ceil(e), 1))
    loss_round = rounded - exact
    has_cur = current.notna() & (current > 0)
    loss_current = (current.where(has_cur) - exact).clip(lower=0)
    return exact, rounded, loss_round, has_cur, loss_current


def aggregate(base: pd.DataFrame, anchor_mgas: float, denom: float) -> dict:
    """Headline scalars (both metrics × scenarios) over the per-execution rows at an anchor.

    Opcode-level rates are unweighted ``loss/charged`` (fraction of paid gas that is waste);
    traffic rates are ``Σ wᵢ·lossᵢ / denom`` against total block gas. The no-reprice loss is
    floored at zero per op, so it counts only the ops repricing makes cheaper — ops the anchor
    pushes above today's price are underpriced and contribute nothing, never offsetting.
    """
    anchor_rate = anchor_mgas * 1e6
    exact, rounded, loss_round, has_cur, loss_current = _scenario_cols(
        base["runtime_ms"], base["current"], anchor_rate
    )
    rate_round = loss_round / rounded
    rate_current = loss_current / base["current"].where(has_cur)
    w = base["count"]
    has_w = w.notna() & (w > 0)
    has_wc = has_w & has_cur

    def weighted(loss_mask, loss_vals):
        return (
            float((w[loss_mask] * loss_vals[loss_mask]).sum() / denom)
            if loss_mask.any() and denom
            else float("nan")
        )

    return {
        "anchor_mgas": anchor_mgas,
        # Opcode-level (unweighted, fraction of charged gas).
        "op_mean_round": float(rate_round.mean()),
        "op_median_round": float(rate_round.median()),
        "op_mean_current": float(rate_current[has_cur].mean()) if has_cur.any() else float("nan"),
        "op_median_current": float(rate_current[has_cur].median()) if has_cur.any() else float("nan"),
        # Mainnet traffic (gas-weighted against total block gas).
        "traffic_round": weighted(has_w, loss_round),
        "traffic_current": weighted(has_wc, loss_current),
        "frac_below_1": float((exact < 1.0).mean()),
        "n_below_1": int((exact < 1.0).sum()),
        "n_ops": int(len(base)),
        "n_current": int(has_cur.sum()),
    }


def hourly_losses(base: pd.DataFrame, anchor_rate: float,
                  hourly: dict[str, dict[str, float]],
                  hourly_gas: dict[str, float]) -> pd.DataFrame:
    """Per-hour gas-weighted loss for the round and no-reprice scenarios.

    For each hour, sum each base op's loss weighted by that hour's execution count and divide
    by that hour's total block gas: ``Σ wᵢ·lossᵢ / Gₕ`` — the traffic metric with that hour's
    opcode mix and gas total. The spread shows how much the loss depends on what the chain
    happens to be running.
    """
    exact, rounded, loss_round, has_cur, loss_current = _scenario_cols(
        base["runtime_ms"], base["current"], anchor_rate
    )
    ops = list(zip(base["norm_opcode"], loss_round, loss_current.fillna(np.nan), has_cur))
    out: list[dict] = []
    for hour in sorted(hourly):
        counts = hourly[hour]
        total_gas = hourly_gas.get(hour, 0.0)
        if total_gas <= 0:
            continue
        num_round = num_current = exec_count = 0.0
        for op, lr, lc, hc in ops:
            wgt = counts.get(op)
            if not wgt:
                continue
            num_round += wgt * lr
            exec_count += wgt
            if hc:
                num_current += wgt * lc
        out.append({
            "hour_start": hour,
            "loss_rate_round": num_round / total_gas,
            "loss_rate_current": num_current / total_gas,
            "total_count": exec_count,
        })
    return pd.DataFrame(out)


def main() -> None:
    anchor_rate = float(yaml.safe_load((ROOT / "fit.yaml").read_text())["anchor_rate"])
    anchor_mgas = anchor_rate / 1e6
    comp, total_op_gas = load_composition()
    current_gas = load_current_gas()
    hourly_comp = load_hourly_composition()
    block_gas, total_block_gas = load_block_gas()

    # Denominator: total block gas when available, else the narrower summed opcode gas.
    denom = total_block_gas or total_op_gas
    denom_is_block = bool(total_block_gas)

    df = pd.read_csv(NEW_GAS).dropna(subset=["runtime_ms", "selected_opcode"]).copy()
    df["opcode"] = df["selected_opcode"].astype(str)
    df["category"] = [_category(str(p), str(o)) for p, o in zip(df["gas_param"], df["opcode"])]
    df["is_base"] = ~df["gas_param"].astype(str).str.endswith(_PER_SUFFIXES)
    df["norm_opcode"] = df["opcode"].map(normalize_opcode)
    df["current"] = df["gas_param"].astype(str).map(current_gas)
    # Composition weight only attaches to per-execution (base) costs.
    df["count"] = [
        comp.get(op) if is_base else None
        for op, is_base in zip(df["norm_opcode"], df["is_base"])
    ]

    exact, rounded, loss_round, has_cur, loss_current = _scenario_cols(
        df["runtime_ms"], df["current"], anchor_rate
    )
    df["exact"] = exact
    df["rounded"] = rounded
    df["loss_round"] = loss_round
    df["rate_round"] = loss_round / rounded
    df["loss_current"] = loss_current
    df["rate_current"] = loss_current / df["current"].where(has_cur)
    df["below_1"] = exact < 1.0

    base = df[df["is_base"]].copy()
    total_base_count = base["count"].dropna().sum()
    df["weight"] = df["count"] / total_base_count if total_base_count else float("nan")

    cols = [
        "gas_param", "opcode", "category", "client_name", "runtime_ms", "exact", "rounded",
        "current", "loss_round", "rate_round", "loss_current", "rate_current",
        "below_1", "is_base", "count", "weight",
    ]
    out = (df[cols].rename(columns={"client_name": "client"})
           .sort_values("rate_round", ascending=False))
    out.to_csv(OUT / "fracgas.csv", index=False)

    anchors = sorted(set(SWEEP_MGAS) | {round(anchor_mgas)})
    sweep = pd.DataFrame([aggregate(base, a, denom) for a in anchors])
    sweep.to_csv(OUT / "fracgas_by_anchor.csv", index=False)

    # Per-hour loss distribution (only when the hourly composition has been fetched). Use the
    # per-hour block gas when present, else fall back to per-hour summed opcode gas.
    hourly_denom = block_gas
    if not hourly_denom and hourly_comp:
        # Fallback: per-hour opcode gas isn't loaded separately here; without block gas the
        # hourly chart is skipped rather than mixing denominators.
        hourly_comp = {}
    hourly = hourly_losses(base, anchor_rate, hourly_comp, hourly_denom)
    hourly_mean_round = float(hourly["loss_rate_round"].mean()) if not hourly.empty else float("nan")
    hourly_mean_current = float(hourly["loss_rate_current"].mean()) if not hourly.empty else float("nan")
    hourly_median_round = float(hourly["loss_rate_round"].median()) if not hourly.empty else float("nan")
    hourly_median_current = float(hourly["loss_rate_current"].median()) if not hourly.empty else float("nan")
    if not hourly.empty:
        hourly.to_csv(OUT / "fracgas_hourly.csv", index=False)

    summary_row = aggregate(base, anchor_mgas, denom)
    summary_row["hourly_mean_round"] = hourly_mean_round
    summary_row["hourly_mean_current"] = hourly_mean_current
    summary_row["hourly_median_round"] = hourly_median_round
    summary_row["hourly_median_current"] = hourly_median_current
    summary_row["n_hours"] = int(len(hourly))
    summary_row["denom_is_block"] = denom_is_block
    summary = pd.DataFrame([summary_row])
    summary.to_csv(OUT / "fracgas_summary.csv", index=False)

    s = summary.iloc[0]
    print(
        f"Wrote {len(out)} rows → fracgas.csv; at {anchor_mgas:.0f} Mgas/s traffic loss "
        f"round {s['traffic_round'] * 100:.2f}% vs no-reprice {s['traffic_current'] * 100:.2f}% "
        f"(denom = {'block gas' if denom_is_block else 'opcode gas (fallback)'}); "
        f"{s['n_below_1']}/{s['n_ops']} base ops below 1 gas; "
        f"{'%d hours, mean round %.2f%% / no-reprice %.2f%%' % (len(hourly), hourly_mean_round * 100, hourly_mean_current * 100) if not hourly.empty else 'no hourly composition'}"
    )


if __name__ == "__main__":
    main()
