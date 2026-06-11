# CLAUDE.md — maintaining hegota-compute-repricing

Pipeline: `benchmarkoor-fetch` → `evm-gasfit` → (`build_bottlenecks.py`, `build_tx_composition.py`,
`compute_fracgas.py`) → `build_site.py` → `docs/` (GitHub Pages, `main`, `/docs`).
README.md has user-facing setup/run docs — this file is for *changing* the repo. Don't duplicate the README.

This dashboard is a sibling of `eip-7904-repricing`: same base pipeline over **all compute
operations** (88 presets), but reframed around two sections at a **100 Mgas/s** anchor:
**Bottleneck** (per-op worst-case throughput; ops below the anchor can't be repriced) and
**Reprice** (the interactive table + runtime/glue reference + a fractional-gas rounding-loss page).

## Layout that matters
- `fetch.yaml` — what benchmark data to pull (pinned suites, fork). `metrics: [runtime, mgas_s]`
  is required — without `mgas_s`, `bench_data.parquet` has no `test_mgas_s` and the bottleneck step fails.
- `fit.yaml` — the estimation: anchor (`1e8` = 100 Mgas/s baseline), clients, `osaka` cost table,
  the 88 compute presets, `new_params`, glue.
- `scripts/build_site.py` — renders `site_src/templates/` → `docs/`, parses `data/gasfit/` reports,
  builds the repricing table (`build_repricing_rows`, bottlenecks excluded via `load_bottleneck_params`),
  the bottleneck table (`build_bottleneck_rows`), and the throughput-loss page (`parse_fracgas`).
- `scripts/build_bottlenecks.py` — p1→min→min worst-case Mgas/s per compute op from the parquet →
  committed `data/bottlenecks.csv`. Owns its own compute-opcode/category map (raw bench mnemonics).
- `scripts/build_tx_composition.py` — Xatu ClickHouse HTTP queries over two CBT hourly tables →
  committed `data/tx_composition_hourly.csv` (per hour × opcode count/gas, from
  `fct_opcode_gas_by_opcode_hourly`), `data/tx_composition.csv` (window-aggregate, summed over
  the hours), and `data/tx_block_gas_hourly.csv` (per-hour total block `gas_used`, from
  `fct_execution_gas_used_hourly` — the all-inclusive denominator). Window via `XATU_DAYS`
  (default 30) / `XATU_END_HOUR`; partial hours dropped via `XATU_MIN_BLOCKS` (default 250).
  `scripts/compute_fracgas.py` — repricing throughput loss → `data/fracgas*.csv`. Scores three
  scenarios (no-reprice `current`, round `ceil(exact)`, fractional `exact`=0 loss) on two metrics
  (unweighted per-op `loss/charged`; gas-weighted over mainnet traffic, denominator = total block
  gas). `fracgas_by_anchor.csv` sweeps both; `fracgas_hourly.csv` carries per-hour `loss_rate_round`
  and `loss_rate_current` (when the hourly composition + block-gas files exist).
- `scripts/build_op_reference.py` — target opcode ↔ test/params mapping from the evm-gasfit
  preset registry → committed `data/op_reference.csv` (a precompute, not part of `build_site.py`,
  because it imports evm-gasfit).
- `scripts/run_gasfit.py` — the `make gasfit` entry point: a thin wrapper over what the
  `evm-gasfit` CLI does that fits every client but excludes `ethrex` from the worst-case
  proposal (see the ethrex gotcha). Also imports evm-gasfit.
- `site_src/{templates,assets}/` — edit these, never `docs/` (regenerated). `assets/plotly.min.js`
  is the vendored Plotly basic build (fracgas charts); copied verbatim by `copy_static`.
- `data/raw/` — fetched inputs; `data/gasfit/` — estimation outputs; `data/*.csv` — the committed
  bottleneck/composition/fracgas artifacts. All committed (the raw bulk excepted, see Gotchas).

## The live anchor (the core feature)
Proposed cost is `ceil(anchor_rate · runtime_ms / 1000)` — exactly linear in the anchor, and
the worst-case client is anchor-invariant (`evm-gasfit` `proposal/aggregate.py`). So
`build_repricing_rows` embeds each param's worst-case `runtime_ms` (+ `current` baseline) into
`repricing.html` as row data attributes, and `anchor_repricing.js` recomputes proposed / diff /
"needs ↑" in place on every slider/number change. **No re-fit is needed to change the anchor** —
only `fit.yaml`'s `anchor_rate` baseline (the slider's initial position) is baked in at build time.

## Common tasks
- **Re-run end-to-end:** `make` (= `fetch gasfit bottlenecks fracgas site`; `composition` is
  *not* in `make`, see below). `make clean` wipes `data/` + `docs/`.
- **Rebuild site only** (after template/asset edits): `make site` — no token/creds needed, reads
  only committed CSVs.
- **Re-fit only** (after `fit.yaml` edits): `make gasfit && make fracgas && make site` (fracgas
  reads the anchor + `new_gas.csv`, so re-run it after a re-fit or anchor change).
- **Rebuild bottlenecks** (after a re-fetch): `make bottlenecks` — reads the gitignored
  `bench_data.parquet`, so it needs a prior `make fetch` with `mgas_s` in `fetch.yaml`.
- **Refresh mainnet opcode composition:** `make composition` (needs Xatu creds; occasional —
  the committed `data/tx_composition*.csv` + `data/tx_block_gas_hourly.csv` are reused otherwise).
  Window via `XATU_DAYS` (default 30) / `XATU_END_HOUR`; `XATU_MIN_BLOCKS` (default 250) drops
  partial hours.
- **Change the op set:** edit `models.presets` in `fit.yaml` (101 presets available in evm-gasfit;
  see its `defaults/models.py`). After adding presets, run `make gasfit` and resolve any
  `Missing parameters` config errors by declaring them under `new_params`. Two category maps may
  need a new entry: `build_site.py` (`_OPCODE_CATEGORY` / `_category`, keyed by gas-param/opcode)
  and `build_bottlenecks.py` (`_COMPUTE_CATEGORY`, keyed by *raw bench opcode mnemonic*, e.g.
  `SHA2-256`); an op missing from the latter is silently dropped from the bottleneck table. Also
  run `make reference` to refresh `data/op_reference.csv` (the opcode↔test mapping page).
- **Change the default anchor:** edit `anchor_rate` in `fit.yaml`; it sets the build-time proposal,
  the slider's starting Mgas/s, the bottleneck ceiling (mirrored as `ANCHOR_MGAS` in both
  `build_site.py` and `build_bottlenecks.py` — keep them in sync), and the fracgas anchor. Re-run
  `make fracgas && make site` (and `make gasfit` to refresh the baked proposal `.md`).

## Gotchas
- **secrets.json** (gitignored, repo root): `{ "benchmarkoor_bearer_token": "bmk_...",
  "xatu_username": "...", "xatu_password": "..." }`. Makefile reads the token with `jq`, exports
  `BENCHMARKOOR_TOKEN`; `build_tx_composition.py` reads the xatu fields directly. Never put the
  token in `fetch.yaml`.
- **Gitignored raw bulk:** `runtimes.csv`, `bench_data.parquet`, `trace.parquet` are NOT committed
  (regenerate with `make fetch`). `data/raw/meta.json` + `opcounts.json` ARE committed. The
  `data/*.csv` analysis artifacts (bottlenecks/composition/fracgas) ARE committed — `make site`
  depends on them, so commit them whenever you regenerate.
- **Two forks, intentionally:** benchmarks run on `amsterdam` (`fetch.yaml`); gas-cost table is
  `osaka` (`fit.yaml`). Not a typo.
- **`ethrex` is fitted but held out of every worst case.** It's in `fit.yaml`'s `clients` (so
  it's fitted and shows up on the runtime/glue pages and as a per-client column on the
  bottleneck table) but excluded from worst-case derivation on *both* sides via a
  `WORST_CASE_EXCLUDE = {"ethrex"}` constant duplicated in `scripts/run_gasfit.py` and
  `scripts/build_bottlenecks.py` (keep them in sync, like `ANCHOR_MGAS`). The repricing/fit
  side achieves this because `make gasfit` runs the `run_gasfit.py` wrapper, not the
  `evm-gasfit` CLI: it fits every client, then rebuilds the proposal (`new_gas.csv`,
  `new_gas_proposal.md`, `new_gas_all_params.csv`, derived params) from a results frame with
  the excluded clients dropped, via evm-gasfit's public `build_proposal`. The bottleneck side
  computes `worst_mgas_s` as the min over the non-excluded clients only.
- **Composition reads the CBT `fct_*` hourly tables** (`mainnet.fct_opcode_gas_by_opcode_hourly`
  for the opcode mix, `mainnet.fct_execution_gas_used_hourly` for the block-gas denominator) —
  real hourly timestamps (`hour_start_date_time`), not the old block-number proxy. **Two query
  gotchas:** (1) these tables live only behind the `cluster('{cbt_cluster}', …)` macro and are
  *replicated across the cluster's nodes*, so `cluster()` returns every row once per node (3×
  today) — must `GROUP BY` the PK and collapse with `any()`, **never raw `sum()`** (would multiply
  by the replica count); (2) they set `force_primary_key`, so every query must filter on
  `hour_start_date_time`. (The earlier `canonical_execution_transaction_structlog_agg` route was a
  fallback from when the role lacked `fct_*` access; that's no longer the case.) Precompiles never
  appear in the opcode table (they run behind CALL), so they get no composition weight in fracgas.
- **Bottleneck "worst = slowest = min":** per-fixture **p1** of `test_mgas_s`, min over fixtures,
  min over clients, on the **300M** fixtures only. Don't flip to p99 — slow binds, not fast.
- **Excluded ops are deliberate:** the state/IO families (warm_/cold_/account_/storage_t*) and
  `system_create`/`block_blockhash` are left out of `fit.yaml`. `block_blockhash` *also* crashes
  the fit (null `block` group key), so don't re-add it without handling that.
- **Coverage gaps surface as empty `new_gas.csv` rows** (per-word copy coeffs, BLS MSM with no
  fixtures). `build_repricing_rows` skips rows with NaN `runtime_ms`/`client_name`, so they're
  absent from the table. MODEXP has no upstream preset at all.
- **build_site.py parsing is brittle by design.** It regex-parses the exact markdown shape of
  evm-gasfit's reports for the runtime/glue pages. After bumping `evm-gasfit`, eyeball those pages.
  The repricing table reads `new_gas.csv` (structured), so it's robust to report-format changes.

## Site pages
Nav groups them as Overview · **Bottleneck** · **Reprice** (Repricing table / Throughput loss /
Runtime model / Glue runtime) · **Reference** (Methodology / Test reference). The grouped nav
lives in `base.html` (`reprice_pages`/`reference_pages` sets + `.nav-group`/`.subnav` CSS).
- `index` — static narrative, two paired analyses, headline bottleneck + reducible counts.
- `bottleneck` — per-op worst-case Mgas/s table, flags ops below the anchor; **live anchor
  slider/number** (worst-case Mgas/s is anchor-invariant, so the browser only re-decides the
  below-anchor flag/count — `bottleneck_filter.js`), plus category filter, only-bottlenecks
  toggle, and click-to-sort. Reads `data/bottlenecks.csv`.
- `repricing` — **the interactive table.** Anchor slider/number + filters; bottlenecks excluded;
  "only cheaper"/"only increase" toggles; client-side rescale (`anchor_repricing.js`).
- `fracgas` — **throughput loss of repricing** (page title "Throughput loss", file still
  `fracgas.html`). Compares three scenarios (no reprice / reprice+round / reprice+fractional=0)
  across two metrics (opcode-level + mainnet-traffic): a headline scenario×metric table, two anchor
  sweeps (opcode-level median + gas-weighted traffic, each with the three scenario lines), the
  per-hour traffic-loss distribution (no-reprice vs round histograms + means), and a per-op grouped
  bar + table. Charts from JSON injected by `build_site`, rendered by `fracgas_charts.js` against
  vendored `plotly.min.js`. Reads `data/fracgas*.csv` (per-hour chart needs `fracgas_hourly.csv`).
- `runtime` — filterable per-fit sections parsed from `runtime_estimation_autogenerated_report.md`
  (`runtime_filter.js`).
- `glue` — filterable sections from `glue_results.csv` + `glue_opcodes_autogenerated_report.md`.
- `reference` — target opcode ↔ benchmark test/params/gas-param mapping (`reference_filter.js`).
  Reads `data/op_reference.csv` (from `make reference`).
- `methodology` — static narrative, reads live values from `fit.yaml`; documents the bottleneck
  and fractional-gas methods too.
