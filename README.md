# Riemann zero check — first 1,000 nontrivial zeros

**Author: Domenic Lipoma — 2026-11-24**

An independent numerical check of the first 1,000 nontrivial zeros of the
Riemann zeta function, recomputed from scratch with arbitrary-precision
arithmetic.

## Why this exists

On 2026-11-20 a claimed proof of the Riemann hypothesis was posted by
Levent Alpöge (working with Claude), formalized in Lean. The Lean and
Mathlib communities certified it on 2026-11-21, and MIT's Andrew Sutherland
independently compiled the export. Confirmation is still ongoing: the final
comparator stage, human peer review, and the Clay prize decision are all
still open.

This repo does **not** verify that proof. It independently recomputes the
*numerical evidence* for the hypothesis — that the zeros lie on the
critical line — up to the 1,000th zero, so anyone can rerun it and check
the numbers themselves.

## Results

| Check | Result |
|---|---|
| Zeros computed | 1,000 |
| Working precision | 30 digits (mpmath) |
| Re(ρ) = 1/2 | Max deviation **0.0** — exact at working precision |
| \|ζ(ρ)\| at each zero | Max **9.24e-28** — rounding level |
| Imaginary parts strictly increasing | Yes — no zero skipped in the sequence |
| First 10 vs published Odlyzko values | Agree to ≥25 digits (worst diff 4.4e-26) |
| First 100 recomputed at 50 digits | Max diff vs 30-digit run **1.2e-29** |
| γ₁₀₀₀ | 1419.42248094599568646598903808 |
| Riemann–von Mangoldt N(T) at γ₁₀₀₀ | 999.418 predicted vs 1,000 found (S(T) ≈ +0.58, as expected) |
| Runtime | 616 s |

## How to rerun

```bash
pip install mpmath
python3 check_zeros.py
```

Writes `results.json` (summary + all 1,000 zeros). The script saves
progress to `zeros_partial.json` every 100 zeros and resumes from it, so
an interrupted run continues instead of starting over.

## Honest scope

Numerical evidence only — this is not a proof, and it is not a check of
the Lean proof. The rigorous record is Platt & Trudgian (2020): all zeros
verified to height 3,000,175,332,800, about 12.4 trillion zeros. This
check covers the first 1,000, to height ~1,419.
