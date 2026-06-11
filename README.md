# Compute Repricing

A static, multi-page site analyzing the EVM's **compute operations** around a
**100 Mgas/s** throughput anchor (the rate a plain ETH transfer sustains, taken as the
chain's ceiling). It answers two paired questions:

- **Bottlenecks** — each operation's worst-case throughput (Mgas/s) measured from client
  benchmarks; the ones below 100 Mgas/s can't be repriced cheaper.
- **Reprice** — of the operations that keep up, which are overpriced for their measured
  runtime and should become **cheaper** (NNLS fits via
  [`evm-gasfit`](https://github.com/misilva73/evm-gasfit)), plus how much gas is lost to
  integer rounding at the anchor (weighted by real mainnet opcode usage from Xatu).

The repricing page is interactive: move the anchor slider and every proposed cost, diff,
and flag is recomputed **live in the browser** — no re-fit, no server.

## Scope

All compute operations: arithmetic, bitwise, comparison, stack, control-flow, hashing
(KECCAK256), memory, block/transaction and call context, and every precompile (including
BLS12-381) — 88 `evm-gasfit` presets, listed in [fit.yaml](fit.yaml). The state/IO-bound
families (storage, account access, transient storage, CREATE, BLOCKHASH) are excluded, as
their runtime is dominated by state access rather than compute. They are also the genuine
sub-100 Mgas/s bottlenecks, so the compute set on the Bottleneck page typically shows none.

## Why the live anchor works

`evm-gasfit` derives each proposed cost as `new_gas = ceil(anchor_rate · runtime_ms / 1000)`
— **strictly linear** in the anchor, with the worst-case client anchor-invariant. The build
embeds each operation's measured `runtime_ms` in the page, so the browser recomputes every
cost exactly (same `ceil` rounding) for any anchor you pick.

## Pipeline

```text
benchmarkoor-fetch  →  evm-gasfit  →  build_bottlenecks.py  ┐
   (data/raw/)         (data/gasfit/)  build_tx_composition.py├→ build_site.py → docs/
                                       compute_fracgas.py     ┘    (Jinja2)   (GitHub Pages)
```

1. **Fetch** — `benchmarkoor-fetch` pulls the pinned benchmark suites into `data/raw/`,
   driven by [fetch.yaml](fetch.yaml). `metrics: [runtime, mgas_s]` records throughput too.
2. **Fit** — `evm-gasfit` runs the NNLS estimation (driven by [fit.yaml](fit.yaml)) and
   emits the proposal artifacts and reports into `data/gasfit/`.
3. **Bottlenecks** — `scripts/build_bottlenecks.py` aggregates worst-case Mgas/s per
   operation from `data/raw/bench_data.parquet` into committed `data/bottlenecks.csv`.
4. **Composition** *(occasional)* — `scripts/build_tx_composition.py` queries Xatu for
   average mainnet opcode usage into committed `data/tx_composition.csv`.
5. **Fractional gas** — `scripts/compute_fracgas.py` computes rounding loss at the anchor
   into committed `data/fracgas*.csv`.
6. **Build** — `scripts/build_site.py` renders the Jinja2 templates in `site_src/` into
   `docs/`, reading the committed CSVs above.
7. **Deploy** — GitHub Pages serves `docs/` from `main`.

`data/` (minus the gitignored raw bulk) is committed alongside `docs/` so the published
site is self-contained and auditable, and `make site` needs no token or credentials.

## Setup

Requires Python ≥ 3.11, plus `make` and `jq`.

```bash
pip install -e .          # installs benchmarkoor-fetch, evm-gasfit, jinja2, pandas
```

### Secrets

`make fetch` needs a Benchmarkoor API key, and `make composition` needs Xatu ClickHouse
credentials. Create a gitignored `secrets.json` at the repo root:

```json
{
  "benchmarkoor_bearer_token": "bmk_...",
  "xatu_username": "...",
  "xatu_password": "..."
}
```

The `Makefile` reads the token with `jq` and exports `BENCHMARKOOR_TOKEN` before invoking
`benchmarkoor-fetch`; the token must never live in `fetch.yaml`. `build_tx_composition.py`
reads the Xatu fields directly. `make site` and `make fracgas` need no secrets.

## Running

```bash
make fetch        # → data/raw/    (reads token from secrets.json; mgas_s metric on)
make gasfit       # → data/gasfit/
make bottlenecks  # → data/bottlenecks.csv    (worst-case Mgas/s per op; reads parquet)
make composition  # → data/tx_composition.csv (Xatu opcode usage; needs xatu creds)
make fracgas      # → data/fracgas*.csv       (rounding loss at the anchor)
make reference    # → data/op_reference.csv   (opcode ↔ test/params mapping)
make site         # renders site_src/templates → docs/, copies figures + plotly
make serve        # preview docs/ locally on http://localhost:8000 (override PORT=…)
# or end-to-end (fetch → gasfit → bottlenecks → fracgas → reference → site):
make
```

`make composition` is an occasional step (the committed CSV is reused); `make` does not run
it. `make clean` removes `data/` and `docs/`.

## Layout

| Path | Purpose |
| --- | --- |
| `fetch.yaml` | benchmarkoor-fetch config (pinned suites, amsterdam fork, `runtime`+`mgas_s`) |
| `fit.yaml` | evm-gasfit config (anchor 1e8, osaka cost table, 88 compute presets, glue on) |
| `scripts/build_site.py` | renders templates → `docs/`, builds the repricing/bottleneck tables, copies figures |
| `scripts/build_bottlenecks.py` | worst-case Mgas/s per op from the parquet → `data/bottlenecks.csv` |
| `scripts/build_tx_composition.py` | Xatu opcode-usage query → `data/tx_composition.csv` |
| `scripts/compute_fracgas.py` | rounding loss at the anchor → `data/fracgas*.csv` |
| `scripts/build_op_reference.py` | opcode ↔ test/params mapping from evm-gasfit presets → `data/op_reference.csv` |
| `site_src/templates/` | Jinja2 templates (`base.html` + one per page) |
| `site_src/assets/` | `style.css`, `*_filter.js`, `anchor_repricing.js`, `fracgas_charts.js`, vendored `plotly.min.js` |
| `data/raw/` | fetched benchmark inputs (bulk parquet/CSV gitignored; `meta.json`/`opcounts.json` committed) |
| `data/gasfit/` | estimation outputs (CSVs, reports, `figs/`) |
| `data/*.csv` | committed bottleneck / composition / fractional-gas artifacts |
| `docs/` | generated static site (served by GitHub Pages) |
