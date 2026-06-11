# New gas proposal

_Generated 2026-06-11 09:34:57Z · fork `osaka` · anchor_rate 100 Mgas/s_

**Summary:** 84 parameters proposed — 8 increased, 67 decreased, 0 new, 5 unresolved · 0 warnings · 44 poor-fit selections

## Contents

- [Proposed parameters](#proposed-gas-parameters)
- [Client comparison](#client-comparison)
- [Worst-case provenance](#worst-case-provenance-per-gas-param)
- [Warnings](#warnings)
- [Poor-fit selections](#poor-fit-selections)

## Proposed gas parameters

| Gas param | Current gas | Proposed gas | Diff | Diff % |
| --- | --- | --- | --- | --- |
| OPCODE_ADD | 3 | 2 | -1 | -33% |
| OPCODE_SUB | 3 | 2 | -1 | -33% |
| OPCODE_MUL | 5 | 1 | -4 | -80% |
| OPCODE_DIV | 5 | 2 | -3 | -60% |
| OPCODE_SDIV | 5 | 2 | -3 | -60% |
| OPCODE_SIGNEXTEND | 5 | 3 | -2 | -40% |
| OPCODE_EXP_BASE | 10 | 110 | +100 | +1000% |
| OPCODE_MOD | 5 | 2 | -3 | -60% |
| OPCODE_SMOD | 5 | 3 | -2 | -40% |
| OPCODE_ADDMOD | 8 | 3 | -5 | -62% |
| OPCODE_MULMOD | 8 | 4 | -4 | -50% |
| OPCODE_AND | 3 | 1 | -2 | -67% |
| OPCODE_OR | 3 | 1 | -2 | -67% |
| OPCODE_XOR | 3 | 1 | -2 | -67% |
| OPCODE_BYTE | 3 | 1 | -2 | -67% |
| OPCODE_SHL | 3 | 1 | -2 | -67% |
| OPCODE_SHR | 3 | 1 | -2 | -67% |
| OPCODE_SAR | 3 | 2 | -1 | -33% |
| OPCODE_NOT | 3 | 1 | -2 | -67% |
| OPCODE_CLZ | 5 | 1 | -4 | -80% |
| OPCODE_LT | 3 | 3 | 0 | 0% |
| OPCODE_GT | 3 | 3 | 0 | 0% |
| OPCODE_SLT | 3 | 1 | -2 | -67% |
| OPCODE_SGT | 3 | 1 | -2 | -67% |
| OPCODE_EQ | 3 | 2 | -1 | -33% |
| OPCODE_ISZERO | 3 | 1 | -2 | -67% |
| OPCODE_PUSH0 | 2 | 1 | -1 | -50% |
| OPCODE_PUSH | 3 | 1 | -2 | -67% |
| OPCODE_DUP | 3 | 1 | -2 | -67% |
| OPCODE_SWAP | 3 | 1 | -2 | -67% |
| OPCODE_JUMP | 8 | 3 | -5 | -62% |
| OPCODE_JUMPI | 10 | 1 | -9 | -90% |
| OPCODE_JUMPDEST | 1 | 1 | 0 | 0% |
| OPCODE_PC | 2 | 1 | -1 | -50% |
| OPCODE_GAS | 2 | 1 | -1 | -50% |
| OPCODE_BASEFEE | 2 | 1 | -1 | -50% |
| OPCODE_BLOBBASEFEE | 2 | 1 | -1 | -50% |
| OPCODE_CHAINID | 2 | 1 | -1 | -50% |
| OPCODE_COINBASE | 2 | 1 | -1 | -50% |
| OPCODE_GASLIMIT | 2 | 1 | -1 | -50% |
| OPCODE_NUMBER | 2 | 1 | -1 | -50% |
| OPCODE_PREVRANDAO | 2 | 1 | -1 | -50% |
| OPCODE_TIMESTAMP | 2 | 1 | -1 | -50% |
| OPCODE_GASPRICE | 2 | 1 | -1 | -50% |
| OPCODE_ORIGIN | 2 | 1 | -1 | -50% |
| OPCODE_ADDRESS | 2 | 1 | -1 | -50% |
| OPCODE_CALLER | 2 | 1 | -1 | -50% |
| OPCODE_CALLVALUE | 2 | 1 | -1 | -50% |
| OPCODE_CALLDATALOAD | 3 | 10 | +7 | +233% |
| OPCODE_CALLDATASIZE | 2 | 1 | -1 | -50% |
| OPCODE_RETURNDATASIZE | 2 | 1 | -1 | -50% |
| OPCODE_CALLDATACOPY_BASE | 3 | 9 | +6 | +200% |
| OPCODE_RETURNDATACOPY_BASE | 3 | 4 | +1 | +33% |
| OPCODE_MLOAD_BASE | 3 | 2 | -1 | -33% |
| OPCODE_MSTORE_BASE | 3 | 2 | -1 | -33% |
| OPCODE_MSTORE8_BASE | 3 | 2 | -1 | -33% |
| OPCODE_MSIZE | 2 | 1 | -1 | -50% |
| OPCODE_MCOPY_BASE | 3 | 6 | +3 | +100% |
| OPCODE_KECCAK256_BASE | 30 | 12 | -18 | -60% |
| OPCODE_KECCAK256_PER_WORD | 6 | 3 | -3 | -50% |
| PRECOMPILE_ECRECOVER | 3000 | 847 | -2153 | -72% |
| PRECOMPILE_SHA256_BASE | 60 | 96 | +36 | +60% |
| PRECOMPILE_SHA256_PER_WORD | 12 | 1 | -11 | -92% |
| PRECOMPILE_RIPEMD160_BASE | 600 | 94 | -506 | -84% |
| PRECOMPILE_RIPEMD160_PER_WORD | 120 | 6 | -114 | -95% |
| PRECOMPILE_IDENTITY_BASE | 15 | 96 | +81 | +540% |
| PRECOMPILE_IDENTITY_PER_WORD | 3 | 1 | -2 | -67% |
| PRECOMPILE_BLAKE2F_BASE | 0 | 94 | +94 | n/a |
| PRECOMPILE_BLAKE2F_PER_ROUND | 1 | 1 | 0 | 0% |
| PRECOMPILE_P256VERIFY | 6900 | 1406 | -5494 | -80% |
| PRECOMPILE_POINT_EVALUATION | 50000 | 23437 | -26563 | -53% |
| PRECOMPILE_ECADD | 150 | 108 | -42 | -28% |
| PRECOMPILE_ECMUL | 6000 | 840 | -5160 | -86% |
| PRECOMPILE_ECPAIRING_BASE | 45000 | 8247 | -36753 | -82% |
| PRECOMPILE_ECPAIRING_PER_POINT | 34000 | 11717 | -22283 | -66% |
| PRECOMPILE_BLS_G1ADD | 375 | 175 | -200 | -53% |
| PRECOMPILE_BLS_G2ADD | 600 | 212 | -388 | -65% |
| PRECOMPILE_BLS_G1MAP | 5500 | 1038 | -4462 | -81% |
| PRECOMPILE_BLS_G2MAP | 23800 | 4490 | -19310 | -81% |

## Client comparison

Worst client vs. second-worst client per gas parameter. The `Ratio` column is `worst gas / second-worst gas` — values close to 1× mean the worst case sits next to the rest of the field, while large ratios flag the worst client as an outlier.

| Gas param | Worst client | Worst gas | Second-worst client | Second-worst gas | Ratio |
| --- | --- | --- | --- | --- | --- |
| OPCODE_ADD | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_SUB | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_MUL | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_DIV | besu | 2 | erigon | 2 | 1.00× |
| OPCODE_SDIV | besu | 2 | erigon | 2 | 1.00× |
| OPCODE_SIGNEXTEND | besu | 3 | erigon | 1 | 3.00× |
| OPCODE_EXP_BASE | besu | 110 | erigon | 49 | 2.24× |
| OPCODE_MOD | besu | 2 | erigon | 2 | 1.00× |
| OPCODE_SMOD | besu | 3 | erigon | 2 | 1.50× |
| OPCODE_ADDMOD | besu | 3 | erigon | 2 | 1.50× |
| OPCODE_MULMOD | besu | 4 | nethermind | 4 | 1.00× |
| OPCODE_AND | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_OR | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_XOR | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_BYTE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_SHL | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_SHR | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_SAR | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_NOT | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_CLZ | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_LT | besu | 3 | erigon | 1 | 3.00× |
| OPCODE_GT | besu | 3 | erigon | 1 | 3.00× |
| OPCODE_SLT | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_SGT | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_EQ | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_ISZERO | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_PUSH0 | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_PUSH | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_DUP | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_SWAP | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_JUMP | besu | 3 | erigon | 1 | 3.00× |
| OPCODE_JUMPI | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_JUMPDEST | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_PC | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_GAS | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_BASEFEE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_BLOBBASEFEE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_CHAINID | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_COINBASE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_GASLIMIT | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_NUMBER | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_PREVRANDAO | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_TIMESTAMP | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_GASPRICE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_ORIGIN | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_ADDRESS | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_CALLER | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_CALLVALUE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_CALLDATALOAD | geth | 10 | erigon | 8 | 1.25× |
| OPCODE_CALLDATASIZE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_RETURNDATASIZE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_CALLDATACOPY_BASE | besu | 9 | erigon | 2 | 4.50× |
| OPCODE_RETURNDATACOPY_BASE | besu | 4 | erigon | 3 | 1.33× |
| OPCODE_MLOAD_BASE | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_MSTORE_BASE | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_MSTORE8_BASE | besu | 2 | erigon | 1 | 2.00× |
| OPCODE_MSIZE | besu | 1 | erigon | 1 | 1.00× |
| OPCODE_MCOPY_BASE | besu | 6 | geth | 2 | 3.00× |
| OPCODE_KECCAK256_BASE | besu | 12 | geth | 9 | 1.33× |
| OPCODE_KECCAK256_PER_WORD | nethermind | 3 | besu | 2 | 1.50× |
| PRECOMPILE_ECRECOVER | erigon | 847 | geth | 780 | 1.09× |
| PRECOMPILE_SHA256_BASE | erigon | 96 | reth | 39 | 2.46× |
| PRECOMPILE_SHA256_PER_WORD | besu | 1 | erigon | 1 | 1.00× |
| PRECOMPILE_RIPEMD160_BASE | erigon | 94 | besu | 45 | 2.09× |
| PRECOMPILE_RIPEMD160_PER_WORD | besu | 6 | geth | 3 | 2.00× |
| PRECOMPILE_IDENTITY_BASE | erigon | 96 | besu | 39 | 2.46× |
| PRECOMPILE_IDENTITY_PER_WORD | erigon | 1 | geth | 1 | 1.00× |
| PRECOMPILE_BLAKE2F_BASE | erigon | 94 | besu | 41 | 2.29× |
| PRECOMPILE_BLAKE2F_PER_ROUND | besu | 1 | erigon | 1 | 1.00× |
| PRECOMPILE_P256VERIFY | erigon | 1406 | geth | 1185 | 1.19× |
| PRECOMPILE_POINT_EVALUATION | nethermind | 23437 | besu | 20833 | 1.12× |
| PRECOMPILE_ECADD | erigon | 108 | reth | 96 | 1.12× |
| PRECOMPILE_ECMUL | reth | 840 | geth | 643 | 1.31× |
| PRECOMPILE_ECPAIRING_BASE | reth | 8247 | nethermind | 6651 | 1.24× |
| PRECOMPILE_ECPAIRING_PER_POINT | nethermind | 11717 | reth | 6080 | 1.93× |
| PRECOMPILE_BLS_G1ADD | besu | 175 | erigon | 101 | 1.73× |
| PRECOMPILE_BLS_G2ADD | besu | 212 | nethermind | 149 | 1.42× |
| PRECOMPILE_BLS_G1MAP | erigon | 1038 | besu | 984 | 1.05× |
| PRECOMPILE_BLS_G2MAP | erigon | 4490 | besu | 3868 | 1.16× |

Per-client proposed gas for each parameter. Cells are colored by `log2(proposed / current)` — red means the proposal is more expensive than the current gas cost, green means cheaper, and white sits at unchanged. Annotations show the absolute proposed gas value; blank rows are parameters with no prior baseline (see warnings below).

![](figs/proposal/heatmap.png)

## Worst-case provenance per gas param

One collapsible block per gas parameter showing every per-client candidate that the worst-case selector saw. Rows are model combos (the source regression's `test_name`, `target_opcode`, `model_coef_name`, and any `model_by` factors — components constant within a parameter are dropped from the label). Cells carry each candidate's proposed gas; the cell the per-client selector picked is outlined in black. Colors are `log2(proposed / current)` against that parameter's baseline on a per-parameter symmetric scale.

_Single-combo parameters omitted (see proposal table for the sole estimation): `OPCODE_ADD`, `OPCODE_SUB`, `OPCODE_MUL`, `OPCODE_DIV`, `OPCODE_SDIV`, `OPCODE_SIGNEXTEND`, `OPCODE_EXP_BASE`, `OPCODE_AND`, `OPCODE_OR`, `OPCODE_XOR`, `OPCODE_BYTE`, `OPCODE_SHL`, `OPCODE_SHR`, `OPCODE_SAR`, `OPCODE_NOT`, `OPCODE_CLZ`, `OPCODE_LT`, `OPCODE_GT`, `OPCODE_SLT`, `OPCODE_SGT`, `OPCODE_EQ`, `OPCODE_ISZERO`, `OPCODE_PUSH0`, `OPCODE_JUMP`, `OPCODE_JUMPI`, `OPCODE_JUMPDEST`, `OPCODE_PC`, `OPCODE_GAS`, `OPCODE_BASEFEE`, `OPCODE_BLOBBASEFEE`, `OPCODE_CHAINID`, `OPCODE_COINBASE`, `OPCODE_GASLIMIT`, `OPCODE_NUMBER`, `OPCODE_PREVRANDAO`, `OPCODE_TIMESTAMP`, `OPCODE_GASPRICE`, `OPCODE_ORIGIN`, `OPCODE_ADDRESS`, `OPCODE_CALLER`, `OPCODE_CALLVALUE`, `OPCODE_MSIZE`, `PRECOMPILE_ECRECOVER`, `PRECOMPILE_BLS_G1ADD`, `PRECOMPILE_BLS_G2ADD`, `PRECOMPILE_BLS_G1MAP`, `PRECOMPILE_BLS_G2MAP`._

<details>
<summary><code>OPCODE_MOD</code> — 5 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_MOD.png)

</details>

<details>
<summary><code>OPCODE_SMOD</code> — 5 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_SMOD.png)

</details>

<details>
<summary><code>OPCODE_ADDMOD</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_ADDMOD.png)

</details>

<details>
<summary><code>OPCODE_MULMOD</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_MULMOD.png)

</details>

<details>
<summary><code>OPCODE_PUSH</code> — 33 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_PUSH.png)

</details>

<details>
<summary><code>OPCODE_DUP</code> — 16 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_DUP.png)

</details>

<details>
<summary><code>OPCODE_SWAP</code> — 16 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_SWAP.png)

</details>

<details>
<summary><code>OPCODE_CALLDATALOAD</code> — 4 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_CALLDATALOAD.png)

</details>

<details>
<summary><code>OPCODE_CALLDATASIZE</code> — 4 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_CALLDATASIZE.png)

</details>

<details>
<summary><code>OPCODE_RETURNDATASIZE</code> — 4 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_RETURNDATASIZE.png)

</details>

<details>
<summary><code>OPCODE_CALLDATACOPY_BASE</code> — 24 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_CALLDATACOPY_BASE.png)

</details>

<details>
<summary><code>OPCODE_RETURNDATACOPY_BASE</code> — 24 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_RETURNDATACOPY_BASE.png)

</details>

<details>
<summary><code>OPCODE_MLOAD_BASE</code> — 5 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_MLOAD_BASE.png)

</details>

<details>
<summary><code>OPCODE_MSTORE_BASE</code> — 5 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_MSTORE_BASE.png)

</details>

<details>
<summary><code>OPCODE_MSTORE8_BASE</code> — 5 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_MSTORE8_BASE.png)

</details>

<details>
<summary><code>OPCODE_MCOPY_BASE</code> — 24 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_MCOPY_BASE.png)

</details>

<details>
<summary><code>OPCODE_KECCAK256_BASE</code> — 4 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_KECCAK256_BASE.png)

</details>

<details>
<summary><code>OPCODE_KECCAK256_PER_WORD</code> — 4 combos × 5 clients</summary>

![](figs/proposal/provenance__OPCODE_KECCAK256_PER_WORD.png)

</details>

<details>
<summary><code>PRECOMPILE_SHA256_BASE</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_SHA256_BASE.png)

</details>

<details>
<summary><code>PRECOMPILE_SHA256_PER_WORD</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_SHA256_PER_WORD.png)

</details>

<details>
<summary><code>PRECOMPILE_RIPEMD160_BASE</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_RIPEMD160_BASE.png)

</details>

<details>
<summary><code>PRECOMPILE_RIPEMD160_PER_WORD</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_RIPEMD160_PER_WORD.png)

</details>

<details>
<summary><code>PRECOMPILE_IDENTITY_BASE</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_IDENTITY_BASE.png)

</details>

<details>
<summary><code>PRECOMPILE_IDENTITY_PER_WORD</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_IDENTITY_PER_WORD.png)

</details>

<details>
<summary><code>PRECOMPILE_BLAKE2F_BASE</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_BLAKE2F_BASE.png)

</details>

<details>
<summary><code>PRECOMPILE_BLAKE2F_PER_ROUND</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_BLAKE2F_PER_ROUND.png)

</details>

<details>
<summary><code>PRECOMPILE_P256VERIFY</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_P256VERIFY.png)

</details>

<details>
<summary><code>PRECOMPILE_POINT_EVALUATION</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_POINT_EVALUATION.png)

</details>

<details>
<summary><code>PRECOMPILE_ECADD</code> — 5 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_ECADD.png)

</details>

<details>
<summary><code>PRECOMPILE_ECMUL</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_ECMUL.png)

</details>

<details>
<summary><code>PRECOMPILE_ECPAIRING_BASE</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_ECPAIRING_BASE.png)

</details>

<details>
<summary><code>PRECOMPILE_ECPAIRING_PER_POINT</code> — 2 combos × 5 clients</summary>

![](figs/proposal/provenance__PRECOMPILE_ECPAIRING_PER_POINT.png)

</details>

## Warnings

### Missing parameters

These names were proposed by a `model_params` RHS or `derived` entry but produced no value — either every candidate fit was skipped (constant opcount, insufficient observations, solver failure) or a referenced upstream value was itself unresolved. Inspect the `evm_gasfit` warnings in `meta.json` for the cause.

| Gas param |
| --- |
| `OPCODE_CALLDATACOPY_PER_WORD` |
| `OPCODE_RETURNDATACOPY_PER_WORD` |
| `OPCODE_MCOPY_PER_WORD` |
| `PRECOMPILE_BLS_G1MUL` |
| `PRECOMPILE_BLS_G2MUL` |

### Incomplete client coverage

**Clients with no estimations at all:** `ethrex`. These configured clients produced no fits for any gas parameter — check that the runtimes CSV contains their rows and that the fixture-name conventions match. Inspect the `evm_gasfit` warnings in `meta.json` for the cause.

### Missing glue adjustments

<details>
<summary><b>Priced glue opcodes with a poor fit</b> — 56 (glue_opcode, client) fits skipped</summary>

`p_value >= glue_contribution_p_value_threshold` (0.05) or `rsquared < glue_contribution_rsquared_threshold` (0.5) — the contribution of these (glue_opcode, client) fits was **skipped** when computing the glue adjustment, so the listed gas params carry a target coefficient that is not net of this glue opcode's runtime on the affected clients. See `glue_opcodes_autogenerated_report.md` for per-fit metrics.

| Glue opcode | Affected clients | Affected gas params |
| --- | --- | --- |
| `AND` | `besu` (R²), `erigon` (R²), `ethrex` (R²), `geth` (R²) | — |
| `CALLDATACOPY` | `besu` (R²), `erigon` (R²), `ethrex` (R²), `reth` (R²) | `PRECOMPILE_BLS_G2MAP`, `PRECOMPILE_POINT_EVALUATION` |
| `CALLDATALOAD` | `besu` (both), `erigon` (R²), `ethrex` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) | `OPCODE_ADDMOD`, `OPCODE_MOD`, `OPCODE_MULMOD`, `OPCODE_SMOD` |
| `EXP` | `erigon` (R²), `nethermind` (both) | — |
| `GT` | `besu` (R²), `erigon` (R²), `geth` (R²) | `PRECOMPILE_BLAKE2F_BASE`, `PRECOMPILE_ECADD`, `PRECOMPILE_ECMUL`, `PRECOMPILE_ECPAIRING_BASE`, `PRECOMPILE_IDENTITY_BASE`, `PRECOMPILE_P256VERIFY`, `PRECOMPILE_POINT_EVALUATION`, `PRECOMPILE_RIPEMD160_BASE`, `PRECOMPILE_SHA256_BASE` |
| `ISZERO` | `erigon` (R²) | — |
| `JUMP` | `besu` (R²), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (both) | `OPCODE_ADDMOD`, `OPCODE_MULMOD` |
| `JUMPDEST` | `besu` (R²) | `OPCODE_ADDMOD`, `OPCODE_CALLDATALOAD`, `OPCODE_JUMP`, `OPCODE_MULMOD`, `PRECOMPILE_BLAKE2F_BASE`, `PRECOMPILE_BLS_G1MAP`, `PRECOMPILE_BLS_G2MAP`, `PRECOMPILE_ECADD`, `PRECOMPILE_ECMUL`, `PRECOMPILE_ECPAIRING_BASE`, `PRECOMPILE_ECRECOVER`, `PRECOMPILE_IDENTITY_BASE`, `PRECOMPILE_P256VERIFY`, `PRECOMPILE_POINT_EVALUATION`, `PRECOMPILE_RIPEMD160_BASE`, `PRECOMPILE_SHA256_BASE` |
| `JUMPI` | `besu` (R²), `erigon` (R²), `ethrex` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) | `PRECOMPILE_BLAKE2F_BASE`, `PRECOMPILE_ECADD`, `PRECOMPILE_ECMUL`, `PRECOMPILE_ECPAIRING_BASE`, `PRECOMPILE_IDENTITY_BASE`, `PRECOMPILE_P256VERIFY`, `PRECOMPILE_POINT_EVALUATION`, `PRECOMPILE_RIPEMD160_BASE`, `PRECOMPILE_SHA256_BASE` |
| `KECCAK256` | `besu` (R²), `erigon` (R²), `ethrex` (both), `geth` (R²), `nethermind` (both), `reth` (both) | — |
| `LT` | `besu` (R²), `erigon` (R²) | — |
| `MSTORE` | `ethrex` (R²), `reth` (R²) | `OPCODE_KECCAK256_BASE`, `PRECOMPILE_ECPAIRING_BASE`, `PRECOMPILE_ECRECOVER`, `PRECOMPILE_IDENTITY_BASE`, `PRECOMPILE_P256VERIFY`, `PRECOMPILE_POINT_EVALUATION` |
| `MSTORE8` | `besu` (R²), `erigon` (R²), `ethrex` (R²), `reth` (R²) | `OPCODE_MCOPY_BASE`, `OPCODE_RETURNDATACOPY_BASE` |
| `MUL` | `besu` (R²), `erigon` (R²) | — |
| `PC` | `besu` (R²) | `OPCODE_JUMP`, `PRECOMPILE_BLAKE2F_BASE`, `PRECOMPILE_ECADD`, `PRECOMPILE_ECMUL`, `PRECOMPILE_ECPAIRING_BASE`, `PRECOMPILE_IDENTITY_BASE`, `PRECOMPILE_P256VERIFY`, `PRECOMPILE_POINT_EVALUATION`, `PRECOMPILE_RIPEMD160_BASE`, `PRECOMPILE_SHA256_BASE` |
| `RETURNDATASIZE` | `besu` (R²), `erigon` (R²) | `OPCODE_RETURNDATACOPY_BASE` |
| `SELFBALANCE` | `besu` (R²), `nethermind` (R²) | `OPCODE_MSIZE` |
| `SUB` | `geth` (R²) | `PRECOMPILE_BLAKE2F_BASE`, `PRECOMPILE_ECADD`, `PRECOMPILE_ECMUL`, `PRECOMPILE_ECPAIRING_BASE`, `PRECOMPILE_IDENTITY_BASE`, `PRECOMPILE_P256VERIFY`, `PRECOMPILE_POINT_EVALUATION`, `PRECOMPILE_RIPEMD160_BASE`, `PRECOMPILE_SHA256_BASE` |
| `SWAP` | `besu` (R²), `erigon` (R²) | — |

</details>

## Poor-fit selections

Rows where the winning fit's p-value exceeded `modeling.poor_fit_p_value_threshold` (0.05) or its R² fell below `modeling.poor_fit_rsquared_threshold` (0.5). The failing threshold(s) are noted alongside each row; selections in `### Winners with poor fit` still drive the proposal, while `### Other weak candidates` lists losing candidates that the selector dropped in favor of a qualified alternative. See `runtime_estimation_autogenerated_report.md` for per-fit `runtime_ms`, `pvalue`, and `rsquared` metrics.

### Winners with poor fit

| Gas param | Client | Test | Target opcode | Coef | runtime_ms | pvalue | rsquared | Failed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OPCODE_MUL` | `erigon` | `test_arithmetic` | `MUL` | `target_coef` | 3.232e-06 | 0.001 | 0.4417 | R² |
| `OPCODE_SIGNEXTEND` | `besu` | `test_arithmetic` | `SIGNEXTEND` | `target_coef` | 2.203e-05 | 0.001 | 0.2451 | R² |
| `OPCODE_EXP_BASE` | `erigon` | `test_arithmetic` | `EXP` | `target_coef` | 0.0004819 | 0.001 | 0.1806 | R² |
| `OPCODE_EXP_BASE` | `nethermind` | `test_arithmetic` | `EXP` | `target_coef` | 0 | 1 | 0 | both |
| `OPCODE_AND` | `erigon` | `test_bitwise` | `AND` | `target_coef` | 1.911e-06 | 0.001 | 0.09128 | R² |
| `OPCODE_BYTE` | `nethermind` | `test_bitwise` | `BYTE` | `target_coef` | 1.458e-06 | 0.001 | 0.4854 | R² |
| `OPCODE_SHL` | `besu` | `test_bitwise` | `SHL` | `target_coef` | 5.304e-06 | 0.001 | 0.333 | R² |
| `OPCODE_SHR` | `besu` | `test_bitwise` | `SHR` | `target_coef` | 5.025e-06 | 0.001 | 0.3219 | R² |
| `OPCODE_SHR` | `erigon` | `test_bitwise` | `SHR` | `target_coef` | 3.524e-06 | 0.001 | 0.4111 | R² |
| `OPCODE_SAR` | `besu` | `test_bitwise` | `SAR` | `target_coef` | 1.981e-05 | 0.001 | 0.1529 | R² |
| `OPCODE_SAR` | `nethermind` | `test_bitwise` | `SAR` | `target_coef` | 2.234e-06 | 0.001 | 0.2227 | R² |
| `OPCODE_LT` | `besu` | `test_comparison` | `LT` | `target_coef` | 2.161e-05 | 0.001 | 0.1771 | R² |
| `OPCODE_LT` | `erigon` | `test_comparison` | `LT` | `target_coef` | 2.994e-06 | 0.001 | 0.471 | R² |
| `OPCODE_GT` | `besu` | `test_comparison` | `GT` | `target_coef` | 2.151e-05 | 0.001 | 0.182 | R² |
| `OPCODE_SGT` | `erigon` | `test_comparison` | `SGT` | `target_coef` | 3.092e-06 | 0.001 | 0.4299 | R² |
| `OPCODE_ISZERO` | `erigon` | `test_iszero` | `ISZERO` | `target_coef` | 1.238e-06 | 0.001 | 0.345 | R² |
| `OPCODE_PUSH0` | `besu` | `test_push` | `PUSH0` | `target_coef` | 2.622e-06 | 0.001 | 0.374 | R² |
| `OPCODE_SWAP` | `besu` | `test_swap` | `SWAP4` | `target_coef` | 3.169e-06 | 0.001 | 0.494 | R² |
| `OPCODE_JUMP` | `besu` | `test_jump_benchmark` | `JUMP` | `target_coef` | 2.788e-05 | 0.001 | 0.4972 | R² |
| `OPCODE_JUMPI` | `besu` | `test_jumpi_fallthrough` | `JUMPI` | `target_coef` | 6.968e-06 | 0.001 | 0.3368 | R² |
| `OPCODE_JUMPI` | `erigon` | `test_jumpi_fallthrough` | `JUMPI` | `target_coef` | 3.232e-06 | 0.001 | 0.2155 | R² |
| `OPCODE_JUMPDEST` | `besu` | `test_jumpdests` | `JUMPDEST` | `target_coef` | 1.897e-06 | 0.001 | 0.236 | R² |
| `OPCODE_NUMBER` | `erigon` | `test_block_context_ops` | `NUMBER` | `target_coef` | 1.806e-06 | 0.001 | 0.4457 | R² |
| `OPCODE_GASPRICE` | `besu` | `test_call_frame_context_ops` | `GASPRICE` | `target_coef` | 3.407e-06 | 0.001 | 0.4926 | R² |
| `OPCODE_ORIGIN` | `besu` | `test_call_frame_context_ops` | `ORIGIN` | `target_coef` | 3.269e-06 | 0.001 | 0.4773 | R² |
| `OPCODE_CALLVALUE` | `besu` | `test_callvalue_from_origin` | `CALLVALUE` | `target_coef` | 4.957e-06 | 0.001 | 0.3478 | R² |
| `OPCODE_CALLVALUE` | `erigon` | `test_callvalue_from_origin` | `CALLVALUE` | `target_coef` | 1.906e-06 | 0.001 | 0.4563 | R² |
| `OPCODE_CALLDATALOAD` | `besu` | `test_calldataload` | `CALLDATALOAD` | `target_coef` | 3.563e-05 | 0.001 | 0.1967 | R² |
| `OPCODE_CALLDATALOAD` | `erigon` | `test_calldataload` | `CALLDATALOAD` | `target_coef` | 7.127e-05 | 0.001 | 0.1261 | R² |
| `OPCODE_CALLDATALOAD` | `geth` | `test_calldataload` | `CALLDATALOAD` | `target_coef` | 9.117e-05 | 0.001 | 0.07158 | R² |
| `OPCODE_CALLDATALOAD` | `nethermind` | `test_calldataload` | `CALLDATALOAD` | `target_coef` | 7.173e-05 | 0.001 | 0.002198 | R² |
| `OPCODE_RETURNDATASIZE` | `besu` | `test_returndatasize_nonzero` | `RETURNDATASIZE` | `target_coef` | 5.662e-06 | 0.001 | 0.3972 | R² |
| `OPCODE_MLOAD_BASE` | `reth` | `test_memory_access` | `MLOAD` | `target_coef` | 1.728e-06 | 0.001 | 0.4123 | R² |
| `PRECOMPILE_SHA256_PER_WORD` | `besu` | `test_sha256_uncachable` | `SHA256` | `size_words` | 1.032e-07 | 0.061 | 0.9238 | p-value |
| `PRECOMPILE_SHA256_PER_WORD` | `erigon` | `test_sha256_uncachable` | `SHA256` | `size_words` | 4.94e-07 | 0.136 | 0.9663 | p-value |
| `PRECOMPILE_SHA256_PER_WORD` | `reth` | `test_sha256_fixed_size` | `SHA256` | `size_words` | 0 | 1 | 0.9943 | p-value |
| `PRECOMPILE_IDENTITY_PER_WORD` | `besu` | `test_identity_fixed_size` | `IDENTITY` | `size_words` | 0 | 1 | 0.9012 | p-value |
| `PRECOMPILE_IDENTITY_PER_WORD` | `reth` | `test_identity_fixed_size` | `IDENTITY` | `size_words` | 3.589e-08 | 0.232 | 0.9946 | p-value |
| `PRECOMPILE_BLAKE2F_PER_ROUND` | `reth` | `test_blake2f_benchmark` | `BLAKE2F` | `num_rounds` | 0 | 1 | 0.9896 | p-value |
| `PRECOMPILE_ECMUL` | `besu` | `test_alt_bn128_uncachable` | `ECMUL` | `target_coef` | 0.005302 | 0.001 | 0.07796 | R² |
| `PRECOMPILE_ECMUL` | `erigon` | `test_alt_bn128_uncachable` | `ECMUL` | `target_coef` | 0.00582 | 0.001 | 0.09823 | R² |
| `PRECOMPILE_ECMUL` | `geth` | `test_alt_bn128_uncachable` | `ECMUL` | `target_coef` | 0.006424 | 0.001 | 0.1739 | R² |
| `PRECOMPILE_ECMUL` | `nethermind` | `test_alt_bn128_uncachable` | `ECMUL` | `target_coef` | 0.005584 | 0.001 | 0.08927 | R² |
| `PRECOMPILE_ECMUL` | `reth` | `test_alt_bn128_uncachable` | `ECMUL` | `target_coef` | 0.008392 | 0.001 | 0.0662 | R² |

### Other weak candidates

<details>
<summary><code>OPCODE_MOD</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_arithmetic` | `MOD` | `target_coef` | — | `erigon` (R²) |

</details>

<details>
<summary><code>OPCODE_SMOD</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_arithmetic` | `SMOD` | `target_coef` | — | `nethermind` (both) |

</details>

<details>
<summary><code>OPCODE_ADDMOD</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_arithmetic` | `ADDMOD` | `target_coef` | — | `nethermind` (both) |

</details>

<details>
<summary><code>OPCODE_MULMOD</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_arithmetic` | `MULMOD` | `target_coef` | — | `erigon` (R²), `nethermind` (both) |

</details>

<details>
<summary><code>OPCODE_PUSH</code> — 2 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_push` | `PUSH0` | `target_coef` | `param_opcode=PUSH0` | `besu` (R²) |
| `test_push` | `PUSH1` | `target_coef` | `param_opcode=PUSH1` | `erigon` (R²) |

</details>

<details>
<summary><code>OPCODE_DUP</code> — 15 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_dup` | `DUP1` | `target_coef` | `param_opcode=DUP1` | `besu` (R²) |
| `test_dup` | `DUP10` | `target_coef` | `param_opcode=DUP10` | `besu` (R²), `erigon` (R²) |
| `test_dup` | `DUP11` | `target_coef` | `param_opcode=DUP11` | `besu` (R²) |
| `test_dup` | `DUP12` | `target_coef` | `param_opcode=DUP12` | `besu` (R²) |
| `test_dup` | `DUP13` | `target_coef` | `param_opcode=DUP13` | `besu` (R²) |
| `test_dup` | `DUP14` | `target_coef` | `param_opcode=DUP14` | `besu` (R²), `erigon` (R²) |
| `test_dup` | `DUP15` | `target_coef` | `param_opcode=DUP15` | `besu` (R²) |
| `test_dup` | `DUP16` | `target_coef` | `param_opcode=DUP16` | `besu` (R²) |
| `test_dup` | `DUP3` | `target_coef` | `param_opcode=DUP3` | `besu` (R²), `erigon` (R²) |
| `test_dup` | `DUP4` | `target_coef` | `param_opcode=DUP4` | `besu` (R²) |
| `test_dup` | `DUP5` | `target_coef` | `param_opcode=DUP5` | `besu` (R²), `erigon` (R²) |
| `test_dup` | `DUP6` | `target_coef` | `param_opcode=DUP6` | `besu` (R²) |
| `test_dup` | `DUP7` | `target_coef` | `param_opcode=DUP7` | `besu` (R²) |
| `test_dup` | `DUP8` | `target_coef` | `param_opcode=DUP8` | `besu` (R²), `erigon` (R²) |
| `test_dup` | `DUP9` | `target_coef` | `param_opcode=DUP9` | `besu` (R²), `erigon` (R²) |

</details>

<details>
<summary><code>OPCODE_SWAP</code> — 16 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_swap` | `SWAP1` | `target_coef` | `param_opcode=SWAP1` | `besu` (R²), `erigon` (R²) |
| `test_swap` | `SWAP10` | `target_coef` | `param_opcode=SWAP10` | `besu` (R²) |
| `test_swap` | `SWAP11` | `target_coef` | `param_opcode=SWAP11` | `besu` (R²), `erigon` (R²), `nethermind` (R²) |
| `test_swap` | `SWAP12` | `target_coef` | `param_opcode=SWAP12` | `besu` (R²), `erigon` (R²) |
| `test_swap` | `SWAP13` | `target_coef` | `param_opcode=SWAP13` | `besu` (R²) |
| `test_swap` | `SWAP14` | `target_coef` | `param_opcode=SWAP14` | `besu` (R²), `nethermind` (R²) |
| `test_swap` | `SWAP15` | `target_coef` | `param_opcode=SWAP15` | `besu` (R²), `erigon` (R²) |
| `test_swap` | `SWAP16` | `target_coef` | `param_opcode=SWAP16` | `besu` (R²), `erigon` (R²), `nethermind` (R²) |
| `test_swap` | `SWAP2` | `target_coef` | `param_opcode=SWAP2` | `besu` (R²) |
| `test_swap` | `SWAP3` | `target_coef` | `param_opcode=SWAP3` | `besu` (R²), `nethermind` (R²) |
| `test_swap` | `SWAP4` | `target_coef` | `param_opcode=SWAP4` | `nethermind` (R²) |
| `test_swap` | `SWAP5` | `target_coef` | `param_opcode=SWAP5` | `besu` (R²) |
| `test_swap` | `SWAP6` | `target_coef` | `param_opcode=SWAP6` | `besu` (R²) |
| `test_swap` | `SWAP7` | `target_coef` | `param_opcode=SWAP7` | `besu` (R²), `erigon` (R²), `nethermind` (R²) |
| `test_swap` | `SWAP8` | `target_coef` | `param_opcode=SWAP8` | `besu` (R²) |
| `test_swap` | `SWAP9` | `target_coef` | `param_opcode=SWAP9` | `besu` (R²), `nethermind` (R²) |

</details>

<details>
<summary><code>OPCODE_CALLDATALOAD</code> — 4 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_calldataload` | `CALLDATALOAD` | `target_coef` | `param_calldata_size=0` | `besu` (both), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) |
| `test_calldataload` | `CALLDATALOAD` | `target_coef` | `param_calldata_size=1024` | `erigon` (R²), `nethermind` (R²) |
| `test_calldataload` | `CALLDATALOAD` | `target_coef` | `param_calldata_size=256` | `besu` (R²), `erigon` (R²), `geth` (R²) |
| `test_calldataload` | `CALLDATALOAD` | `target_coef` | `param_calldata_size=32` | `besu` (R²), `geth` (R²), `nethermind` (both), `reth` (R²) |

</details>

<details>
<summary><code>OPCODE_RETURNDATASIZE</code> — 3 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_returndatasize_nonzero` | `RETURNDATASIZE` | `target_coef` | `param_returned_size=0` | `besu` (R²), `erigon` (R²) |
| `test_returndatasize_nonzero` | `RETURNDATASIZE` | `target_coef` | `param_returned_size=1024` | `besu` (R²), `erigon` (R²) |
| `test_returndatasize_nonzero` | `RETURNDATASIZE` | `target_coef` | `param_returned_size=256` | `besu` (R²) |

</details>

<details>
<summary><code>OPCODE_CALLDATACOPY_BASE</code> — 12 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=0` / `param_mem_size=10240` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=0` / `param_mem_size=1048576` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=0` / `param_mem_size=256` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=1024` / `param_mem_size=1048576` | `nethermind` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=1024` / `param_mem_size=32` | `nethermind` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=256` / `param_mem_size=0` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=256` / `param_mem_size=1024` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=256` / `param_mem_size=1048576` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=256` / `param_mem_size=32` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=32` / `param_mem_size=0` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=32` / `param_mem_size=1024` | `erigon` (R²) |
| `test_calldatacopy_from_origin` | `CALLDATACOPY` | `target_coef` | `param_calldata_size=32` / `param_mem_size=1048576` | `erigon` (R²) |

</details>

<details>
<summary><code>OPCODE_RETURNDATACOPY_BASE</code> — 21 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=0` / `param_return_size=0` | `besu` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=0` / `param_return_size=10240` | `geth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=0` / `param_return_size=1048576` | `besu` (R²), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=0` / `param_return_size=256` | `erigon` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=0` / `param_return_size=32` | `besu` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=1024` / `param_return_size=0` | `besu` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=1024` / `param_return_size=1024` | `erigon` (R²), `nethermind` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=1024` / `param_return_size=10240` | `erigon` (R²), `geth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=1024` / `param_return_size=1048576` | `besu` (R²), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=1024` / `param_return_size=256` | `erigon` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=1024` / `param_return_size=32` | `besu` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=256` / `param_return_size=1024` | `nethermind` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=256` / `param_return_size=10240` | `geth` (R²), `nethermind` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=256` / `param_return_size=1048576` | `besu` (R²), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=256` / `param_return_size=256` | `erigon` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=256` / `param_return_size=32` | `besu` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=32` / `param_return_size=0` | `besu` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=32` / `param_return_size=10240` | `geth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=32` / `param_return_size=1048576` | `besu` (R²), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=32` / `param_return_size=256` | `erigon` (R²) |
| `test_returndatacopy` | `RETURNDATACOPY` | `target_coef` | `param_mem_size=32` / `param_return_size=32` | `besu` (R²) |

</details>

<details>
<summary><code>OPCODE_MLOAD_BASE</code> — 4 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_memory_access` | `MLOAD` | `target_coef` | `param_mem_size=0` | `reth` (R²) |
| `test_memory_access` | `MLOAD` | `target_coef` | `param_mem_size=1024` | `reth` (R²) |
| `test_memory_access` | `MLOAD` | `target_coef` | `param_mem_size=256` | `reth` (R²) |
| `test_memory_access` | `MLOAD` | `target_coef` | `param_mem_size=32` | `reth` (R²) |

</details>

<details>
<summary><code>OPCODE_MSTORE8_BASE</code> — 2 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_memory_access` | `MSTORE8` | `target_coef` | `param_mem_size=0` | `erigon` (R²) |
| `test_memory_access` | `MSTORE8` | `target_coef` | `param_mem_size=32` | `reth` (R²) |

</details>

<details>
<summary><code>OPCODE_MCOPY_BASE</code> — 10 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=0` / `param_mem_size=0` | `besu` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=1024` / `param_mem_size=0` | `erigon` (both) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=1024` / `param_mem_size=1024` | `erigon` (both) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=1024` / `param_mem_size=10240` | `reth` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=1024` / `param_mem_size=1048576` | `geth` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=256` / `param_mem_size=1024` | `erigon` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=256` / `param_mem_size=10240` | `erigon` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=256` / `param_mem_size=1048576` | `erigon` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=256` / `param_mem_size=256` | `erigon` (R²) |
| `test_mcopy` | `MCOPY` | `target_coef` | `param_copy_size=256` / `param_mem_size=32` | `erigon` (R²) |

</details>

<details>
<summary><code>PRECOMPILE_SHA256_PER_WORD</code> — 2 weak combos</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_sha256_fixed_size` | `SHA256` | `size_words` | — | `besu` (p-value), `erigon` (p-value) |
| `test_sha256_uncachable` | `SHA256` | `size_words` | — | `reth` (p-value) |

</details>

<details>
<summary><code>PRECOMPILE_IDENTITY_PER_WORD</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_identity_uncachable` | `IDENTITY` | `size_words` | — | `besu` (p-value), `reth` (p-value) |

</details>

<details>
<summary><code>PRECOMPILE_BLAKE2F_PER_ROUND</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_blake2f_uncachable` | `BLAKE2F` | `num_rounds` | — | `erigon` (p-value), `reth` (p-value) |

</details>

<details>
<summary><code>PRECOMPILE_ECMUL</code> — 1 weak combo</summary>

| Test | Target opcode | Coef | Combo | Failing clients |
| --- | --- | --- | --- | --- |
| `test_alt_bn128` | `ECMUL` | `target_coef` | — | `besu` (R²), `erigon` (R²), `geth` (R²), `nethermind` (R²), `reth` (R²) |

</details>
