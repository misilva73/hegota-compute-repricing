BENCHMARKOOR_TOKEN := $(shell jq -r .benchmarkoor_bearer_token secrets.json)
export BENCHMARKOOR_TOKEN

PORT ?= 8000

# Use the project venv's interpreter/entrypoints (override with VENV=… or BIN=…).
VENV ?= .venv
BIN := $(VENV)/bin

.PHONY: all fetch gasfit bottlenecks composition fracgas reference site serve clean

all:
	$(MAKE) fetch
	$(MAKE) gasfit
	$(MAKE) bottlenecks
	$(MAKE) fracgas
	$(MAKE) reference
	$(MAKE) site

fetch:
	$(BIN)/benchmarkoor-fetch run --config fetch.yaml --out data/raw/

# Wraps `evm-gasfit run`: fits every client but excludes ethrex from the
# worst-case proposal (scripts/run_gasfit.py — WORST_CASE_EXCLUDE).
gasfit:
	$(BIN)/python scripts/run_gasfit.py --config fit.yaml \
		--runtimes data/raw/runtimes.csv \
		--opcounts data/raw/opcounts.json \
		--out data/gasfit/

# Per-operation worst-case throughput → committed data/bottlenecks.csv. Reads the
# gitignored bench_data.parquet (needs `make fetch` first, with mgas_s metric).
bottlenecks:
	$(BIN)/python scripts/build_bottlenecks.py

# Average mainnet opcode composition from Xatu → committed data/tx_composition.csv.
# Manual/occasional step — needs xatu_username/xatu_password in secrets.json.
composition:
	$(BIN)/python scripts/build_tx_composition.py

# Fractional-gas rounding loss at the fit.yaml anchor → committed data/fracgas*.csv.
# Reads only committed inputs (new_gas.csv + tx_composition.csv); no credentials.
fracgas:
	$(BIN)/python scripts/compute_fracgas.py

# Target-opcode ↔ benchmark/test/param mapping → committed data/op_reference.csv.
# Static config from the evm-gasfit preset registry; regenerate after fit.yaml preset edits.
reference:
	$(BIN)/python scripts/build_op_reference.py

site:
	$(BIN)/python scripts/build_site.py

serve:
	$(BIN)/python -m http.server $(PORT) --directory docs/

clean:
	rm -rf data/ docs/
