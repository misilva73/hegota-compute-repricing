#!/usr/bin/env python3
"""Render the EIP-7904 repricing site from ``data/`` into ``docs/``.

Data sources (all produced by ``make fetch`` + ``make gasfit``):

* ``data/raw/meta.json``                — reproducibility footer (suites, fork, run window)
* ``data/gasfit/new_gas_proposal.md``   — rendered wholesale for the new-gas page
* ``data/gasfit/*_report.md``           — parsed into filterable per-fit sections
* ``data/gasfit/glue_results.csv``      — per (client, glue_opcode) glue headline stats
* ``data/gasfit/figs/{proposal,runtime,glue}/`` — copied verbatim into ``docs/figs/``

The runtime and glue pages are the only ones with structured parsing; everything
else is either static narrative or a wholesale markdown render.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from importlib.metadata import PackageNotFoundError, version as pkg_version
from pathlib import Path

import pandas as pd
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
GASFIT = ROOT / "data" / "gasfit"
DATA = ROOT / "data"
SRC = ROOT / "site_src"
TEMPLATES = SRC / "templates"
ASSETS = SRC / "assets"
OUT = ROOT / "docs"

# Assumed eth-transfer throughput ceiling. Operations below it are bottlenecks
# (cannot be repriced cheaper); it is also the default repricing anchor in fit.yaml.
ANCHOR_MGAS = 100.0

# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def package_version(dist_name: str, fallback: str) -> str:
    try:
        return pkg_version(dist_name)
    except PackageNotFoundError:
        return fallback


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


# --------------------------------------------------------------------------- #
# Reproducibility metadata (footer)
# --------------------------------------------------------------------------- #
def load_meta() -> dict:
    raw = json.loads((RAW / "meta.json").read_text())
    return {
        "suites": [s["suite_hash"] for s in raw["suites"]],
        "fork": raw["query"]["fork"],
        "run_timestamp": raw["data_window"]["end"],
        "fetch_version": package_version("benchmarkoor-fetch", raw.get("package_version", "?")),
        "gasfit_version": package_version("evm-gasfit", "?"),
        "commit": git_commit(),
    }


# --------------------------------------------------------------------------- #
# Proposal table (used by the landing page for the headline takeaway)
# --------------------------------------------------------------------------- #
def parse_proposed_table() -> list[dict]:
    """Parse the ``## Proposed gas parameters`` table into rows."""
    text = (GASFIT / "new_gas_proposal.md").read_text()
    block = re.search(r"## Proposed gas parameters\n(.*?)(?=^## )", text, re.S | re.M)
    rows: list[dict] = []
    if not block:
        return rows
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("| -"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] in ("Gas param", ""):
            continue
        rows.append({
            "param": cells[0],
            "current": cells[1],
            "proposed": cells[2],
            "diff": cells[3],
            "diff_pct": cells[4],
        })
    return rows


# --------------------------------------------------------------------------- #
# Repricing table (the interactive, anchor-driven centerpiece)
# --------------------------------------------------------------------------- #
# Map each opcode to its family for grouping/filtering in the table. Precompiles
# are categorised by gas-param prefix instead (see _category).
_OPCODE_CATEGORY: dict[str, str] = {
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
    }.items()
    for op in ops
}


def _category(gas_param: str, opcode: str) -> str:
    if gas_param.startswith("PRECOMPILE_BLS_"):
        return "BLS12-381"
    if gas_param.startswith("PRECOMPILE_"):
        return "Precompile"
    # Numbered variants (PUSH6, DUP2, SWAP4) collapse to their family root.
    base = opcode.rstrip("0123456789")
    return _OPCODE_CATEGORY.get(opcode) or _OPCODE_CATEGORY.get(base, "Other")


def load_bottleneck_params() -> set[str]:
    """``gas_param``s belonging to sub-anchor compute ops, from data/bottlenecks.csv.

    These are excluded from the Repricing table (they cannot be repriced cheaper and
    are covered on the Bottleneck page instead). Returns an empty set when the file is
    absent (so ``make site`` works before the bottleneck step has run) — which is also
    the expected steady state, since the real sub-100 ops are out-of-scope state/IO.
    """
    path = DATA / "bottlenecks.csv"
    if not path.exists():
        return set()
    df = pd.read_csv(path)
    df = df[df["below_anchor"].astype(bool)]
    params: set[str] = set()
    for cell in df.get("gas_params", pd.Series([], dtype=str)).dropna():
        params.update(p for p in str(cell).split(";") if p)
    return params


def build_repricing_rows(proposed: list[dict], bottleneck_params: set[str]) -> list[dict]:
    """One row per fitted gas param for the live table.

    Carries the worst-case ``runtime_ms`` (anchor-independent) so the browser can
    recompute the proposed cost for any anchor as ``ceil(anchor * runtime_ms / 1000)``
    — the exact formula evm-gasfit uses (proposal/aggregate.py). ``current`` is the
    protocol baseline parsed from the proposal table (``None`` when not numeric, e.g.
    a ``new_params`` entry declared without a baseline). Params flagged as bottlenecks
    are dropped — they belong to the Bottleneck section, not the repricing view.
    """
    current_by_param = {r["param"]: r["current"] for r in proposed}
    df = pd.read_csv(GASFIT / "new_gas.csv")
    rows: list[dict] = []
    for _, r in df.iterrows():
        # Skip params that produced no fit (no winning client / runtime) — they
        # appear in new_gas.csv as empty rows and can't be repriced.
        if pd.isna(r["runtime_ms"]) or pd.isna(r["client_name"]):
            continue
        param = r["gas_param"]
        if str(param) in bottleneck_params:
            continue
        try:
            current = int(str(current_by_param.get(param)).replace(",", ""))
        except (TypeError, ValueError):
            current = None
        rows.append({
            "param": str(param),
            "category": _category(str(param), str(r["selected_opcode"])),
            "client": str(r["client_name"]),
            "current": current,
            "runtime_ms": float(r["runtime_ms"]),
        })
    rows.sort(key=lambda x: (x["category"], x["param"]))
    return rows


# --------------------------------------------------------------------------- #
# Bottleneck table (per-op worst-case throughput vs the eth-transfer ceiling)
# --------------------------------------------------------------------------- #
def build_bottleneck_rows() -> dict:
    """Read the committed data/bottlenecks.csv into rows + facets for the table.

    One row per compute operation: worst-case throughput over all clients, the
    per-client values, and whether it falls below the ANCHOR_MGAS ceiling. Returns an
    empty payload when the file is absent so the page still renders.
    """
    path = DATA / "bottlenecks.csv"
    if not path.exists():
        return {"rows": [], "clients": [], "anchor_mgas": ANCHOR_MGAS, "n_below": 0, "n_total": 0}
    df = pd.read_csv(path)
    clients = [c[len("mgas_s_"):] for c in df.columns if c.startswith("mgas_s_")]
    rows: list[dict] = []
    for _, r in df.iterrows():
        rows.append({
            "opcode": str(r["opcode"]),
            "category": str(r["category"]),
            "worst": float(r["worst_mgas_s"]),
            "per_client": {c: (None if pd.isna(r[f"mgas_s_{c}"]) else float(r[f"mgas_s_{c}"]))
                           for c in clients},
            "below": bool(r["below_anchor"]),
        })
    rows.sort(key=lambda x: (x["category"], x["opcode"]))
    return {
        "rows": rows,
        "clients": clients,
        "anchor_mgas": ANCHOR_MGAS,
        "n_below": int(df["below_anchor"].astype(bool).sum()),
        "n_total": len(df),
    }


# --------------------------------------------------------------------------- #
# Fractional-gas rounding loss (per-op + composition-weighted, at the anchor)
# --------------------------------------------------------------------------- #
def parse_fracgas() -> dict:
    """Read the committed data/fracgas*.csv into per-op rows, summary, and sweep.

    All three files are produced by ``make fracgas``. Returns an empty payload when
    the per-op file is absent so the page still renders. Per-op rows and the anchor
    sweep are passed through as plain dicts for client-side Plotly rendering.
    """
    # Round-trip through pandas' JSON to coerce numpy scalars to plain types and
    # NaN → null, so json.dumps (for the embedded Plotly data) never trips.
    def _records(path: Path) -> list[dict]:
        return json.loads(pd.read_csv(path).to_json(orient="records")) if path.exists() else []

    per_op = DATA / "fracgas.csv"
    if not per_op.exists():
        return {"rows": [], "summary": {}, "sweep": [], "hourly": [], "anchor_mgas": ANCHOR_MGAS}
    rows = _records(per_op)
    summary_rows = _records(DATA / "fracgas_summary.csv")
    summary = summary_rows[0] if summary_rows else {}
    # How many base ops repricing+rounding would make cheaper (new integer price below
    # today's) — restricted to base ops with a current price so it shares the headline's
    # ``n_ops`` denominator. Derived here rather than in fracgas_summary.csv so it stays live.
    priced = [r for r in rows if r.get("is_base") and r.get("current") is not None]
    if priced and summary:
        summary["n_cheaper"] = sum(1 for r in priced if r["rounded"] < r["current"])
    sweep = _records(DATA / "fracgas_by_anchor.csv")
    hourly = _records(DATA / "fracgas_hourly.csv")
    return {"rows": rows, "summary": summary, "sweep": sweep, "hourly": hourly,
            "anchor_mgas": ANCHOR_MGAS}


# --------------------------------------------------------------------------- #
# Reference: target opcode ↔ benchmark test/params mapping
# --------------------------------------------------------------------------- #
def parse_op_reference() -> dict:
    """Read the committed data/op_reference.csv into rows + category facet."""
    path = DATA / "op_reference.csv"
    if not path.exists():
        return {"rows": [], "categories": []}
    df = pd.read_csv(path).fillna("")
    return {"rows": df.to_dict("records"), "categories": sorted(df["category"].unique())}


# --------------------------------------------------------------------------- #
# Runtime report → filterable sections
# --------------------------------------------------------------------------- #
_DETAILS_RE = re.compile(
    r"<details><summary>(?P<client>\w+) — NNLS regression summary</summary>\s*"
    r"```\n(?P<nnls>.*?)\n```(?P<rest>.*?)</details>",
    re.S,
)


def _parse_md_table(text: str) -> dict[str, dict]:
    """Parse the per-client summary table at the top of a runtime subsection."""
    rows: dict[str, dict] = {}
    table_lines = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    for line in table_lines:
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] in ("client", "") or set("".join(cells)) <= set("-: "):
            continue
        rows[cells[0]] = {
            "nobs": cells[1], "rsquared": cells[2], "coef": cells[3],
            "pvalue": cells[4], "ci": cells[5],
        }
    return rows


def _split_combo(heading: str) -> tuple[str, str]:
    m = re.match(r"(?P<test>.+?) — combo `(?P<combo>.+)`", heading)
    if m:
        return m.group("test").strip(), m.group("combo")
    return heading.strip(), "all"


def parse_runtime() -> dict:
    text = (GASFIT / "runtime_estimation_autogenerated_report.md").read_text()
    sections: list[dict] = []
    opcodes: list[str] = []

    opcode_parts = re.split(r"^## (.+)$", text, flags=re.M)
    for i in range(1, len(opcode_parts), 2):
        opcode = opcode_parts[i].strip()
        if opcode.lower() == "contents":
            continue
        opcodes.append(opcode)
        body = opcode_parts[i + 1]

        sub_parts = re.split(r"^### (.+)$", body, flags=re.M)
        for j in range(1, len(sub_parts), 2):
            test, combo = _split_combo(sub_parts[j].strip())
            sub = sub_parts[j + 1]
            table = _parse_md_table(sub)
            for m in _DETAILS_RE.finditer(sub):
                client = m.group("client")
                figs = re.findall(r"!\[\]\((figs/runtime/[^)]+)\)", m.group("rest"))
                sections.append({
                    "opcode": opcode, "test": test, "combo": combo, "client": client,
                    "nnls": m.group("nnls"), "figs": figs,
                    **table.get(client, {}),
                })

    return {
        "sections": sections,
        "opcodes": opcodes,
        "clients": sorted({s["client"] for s in sections}),
    }


# --------------------------------------------------------------------------- #
# Glue report + CSV → filterable sections
# --------------------------------------------------------------------------- #
def _parse_glue_appendix() -> list[dict]:
    """Per-client tier/joint NNLS summaries, grouped by client."""
    text = (GASFIT / "glue_opcodes_autogenerated_report.md").read_text()
    out: list[dict] = []
    client_parts = re.split(r"^## (.+)$", text, flags=re.M)
    for i in range(1, len(client_parts), 2):
        client = client_parts[i].strip()
        if client.lower() == "contents":
            continue
        body = client_parts[i + 1]
        fits: list[dict] = []
        sub_parts = re.split(r"^### (.+)$", body, flags=re.M)
        for j in range(1, len(sub_parts), 2):
            heading = sub_parts[j].strip()
            for m in re.finditer(r"```\n(.*?)\n```", sub_parts[j + 1], re.S):
                fits.append({"heading": heading, "nnls": m.group(1)})
        if fits:
            out.append({"client": client, "fits": fits})
    return out


def parse_glue() -> dict:
    gr = pd.read_csv(GASFIT / "glue_results.csv")
    sections: list[dict] = []
    for _, r in gr.iterrows():
        client, opcode = r["client_name"], r["glue_opcode"]
        figs = [
            f"figs/glue/{opcode}__{client}__{kind}.png"
            for kind in ("regression", "bootstrap", "diagnostics")
        ]
        figs = [f for f in figs if (GASFIT / f).exists()]
        sections.append({
            "client": client, "glue_opcode": opcode,
            "nobs": int(r["nobs"]),
            "glue_runtime_ms": float(r["glue_runtime_ms"]),
            "p_value": float(r["p_value"]),
            "rsquared": float(r["rsquared"]),
            "figs": figs,
        })
    return {
        "sections": sections,
        "clients": sorted(gr["client_name"].unique().tolist()),
        "glue_opcodes": sorted(gr["glue_opcode"].unique().tolist()),
        "appendix": _parse_glue_appendix(),
    }


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def build_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["sci"] = lambda v: f"{v:.3e}"
    env.filters["g4"] = lambda v: f"{v:.4g}"
    return env


def copy_static() -> None:
    OUT.mkdir(exist_ok=True)
    # Disable GitHub Pages' Jekyll processing so files/dirs with leading
    # underscores are served verbatim instead of being silently dropped.
    (OUT / ".nojekyll").touch()
    for asset in ASSETS.iterdir():
        shutil.copy2(asset, OUT / asset.name)
    figs_src = GASFIT / "figs"
    if figs_src.exists():
        shutil.copytree(figs_src, OUT / "figs", dirs_exist_ok=True)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    env = build_env()
    meta = load_meta()
    proposed = parse_proposed_table()
    fit_cfg = yaml.safe_load((ROOT / "fit.yaml").read_text())
    base_anchor_mgas = float(fit_cfg["anchor_rate"]) / 1e6

    bottleneck = build_bottleneck_rows()
    common = {"meta": meta, "anchor_mgas": ANCHOR_MGAS}

    # Landing page — static narrative + headline counts at the baseline anchor.
    n_up = sum(1 for r in proposed if r["diff"].startswith("+"))
    n_down = sum(1 for r in proposed if r["diff"].startswith("-"))
    (OUT / "index.html").write_text(env.get_template("index.html").render(
        page="index", proposed=proposed, n_up=n_up, n_down=n_down,
        base_anchor_mgas=base_anchor_mgas, n_params=len(proposed),
        n_below=bottleneck["n_below"], n_ops=bottleneck["n_total"], **common,
    ))

    # Bottleneck page — per-op worst-case throughput vs the eth-transfer ceiling.
    (OUT / "bottleneck.html").write_text(env.get_template("bottleneck.html").render(
        page="bottleneck", **bottleneck, **{k: v for k, v in common.items() if k != "anchor_mgas"},
    ))

    # Bottlenecks methodology page — static narrative, config-driven values.
    (OUT / "bottleneck_methodology.html").write_text(
        env.get_template("bottleneck_methodology.html").render(
            page="bottleneck_methodology", fit=fit_cfg, **common,
        )
    )

    # Repricing page — the interactive centerpiece. One row per fitted gas param
    # (bottlenecks excluded), rescaled live in the browser from a user anchor.
    bottleneck_params = load_bottleneck_params()
    rows = build_repricing_rows(proposed, bottleneck_params)
    (OUT / "repricing.html").write_text(env.get_template("repricing.html").render(
        page="repricing", rows=rows, base_anchor_mgas=base_anchor_mgas,
        n_params=len(rows), n_excluded=len(bottleneck_params), **common,
    ))

    # Runtime page — filterable per-fit sections.
    (OUT / "runtime.html").write_text(env.get_template("runtime.html").render(
        page="runtime", **parse_runtime(), **common,
    ))

    # Glue page — filterable per (client, glue_opcode) sections + appendix.
    (OUT / "glue.html").write_text(env.get_template("glue.html").render(
        page="glue", **parse_glue(), **common,
    ))

    # Fractional-gas page — rounding loss at the anchor + interactive Plotly charts.
    fracgas = parse_fracgas()
    (OUT / "fracgas.html").write_text(env.get_template("fracgas.html").render(
        page="fracgas",
        fracgas_rows_json=json.dumps(fracgas["rows"]),
        fracgas_sweep_json=json.dumps(fracgas["sweep"]),
        fracgas_hourly_json=json.dumps(fracgas["hourly"]),
        summary=fracgas["summary"], rows=fracgas["rows"], **common,
    ))

    # Reference page — target opcode ↔ benchmark test/params mapping.
    (OUT / "reference.html").write_text(env.get_template("reference.html").render(
        page="reference", **parse_op_reference(), **common,
    ))

    # Methodology page — static narrative, config-driven values.
    (OUT / "methodology.html").write_text(env.get_template("methodology.html").render(
        page="methodology", fit=fit_cfg, **common,
    ))

    copy_static()
    print(f"Built site → {OUT}")


if __name__ == "__main__":
    main()
