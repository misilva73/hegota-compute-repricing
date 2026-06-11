#!/usr/bin/env python3
"""Target-opcode ↔ benchmark mapping → committed ``data/op_reference.csv``.

A static reference: for every compute preset listed in ``fit.yaml``, which benchmark
``test_name`` drives it, which fixture parameters the model varies over, the fixture
filter applied, and the gas parameter(s) it produces. Sourced from the authoritative
``evm-gasfit`` preset registry (``defaults/models.py``), so it tracks the real fit config.

Kept as a precompute (not in ``build_site.py``) so the site build stays free of the
``evm-gasfit``/matplotlib import; ``build_site.py`` only reads the committed CSV.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml
from evm_gasfit.defaults.models import PRESETS

from build_site import _category

ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = ROOT / "data" / "op_reference.csv"


def main() -> None:
    preset_names = yaml.safe_load((ROOT / "fit.yaml").read_text())["models"]["presets"]
    rows: list[dict] = []
    for name in preset_names:
        spec = PRESETS[name]
        target_coef = spec.model_params.get("target_coef", "")
        if spec.target_operation:
            opcode = spec.target_operation
            target_op = opcode
        else:
            # Parameterised target (PUSH/DUP/SWAP): the opcode varies per fixture.
            opcode = target_coef.replace("OPCODE_", "").replace("PRECOMPILE_", "")
            target_op = f"{opcode}* (per {spec.target_operation_param})"
        rows.append({
            "target_op": target_op,
            "category": _category(target_coef, opcode),
            "preset": name,
            "test_name": spec.test_name,
            "fixture_params": ", ".join(spec.model_by) if spec.model_by else "",
            "fixture_filter": ", ".join(spec.filter_by) if spec.filter_by else "",
            "gas_params": ", ".join(dict.fromkeys(spec.model_params.values())),
            "count_source": spec.target_operation_count_source or "",
        })
    df = pd.DataFrame(rows).sort_values(["category", "target_op", "preset"])
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {len(df)} preset mappings → {OUT_CSV}")


if __name__ == "__main__":
    main()
