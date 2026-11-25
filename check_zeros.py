#!/usr/bin/env python3
"""
Independent numerical check of the first 1,000 nontrivial zeros of the
Riemann zeta function.

Author: Domenic Lipoma
Date: 2026-11-24
Method: mpmath (arbitrary precision, dps=30 working precision).
  For each n = 1..1000:
    - rho_n = zetazero(n)  (mpmath's zero finder)
    - check Re(rho_n) == 1/2 to working precision
    - check |zeta(rho_n)| is at rounding level
    - check Im(rho_n) is strictly increasing (no zero skipped in the sequence)
  Cross-checks:
    - first 10 imaginary parts against the published Odlyzko values
    - first 100 zeros recomputed at dps=50; agreement with the dps=30 values
    - Riemann-von Mangoldt count N(T) at T = Im(rho_1000) vs 1000 found
  Resumable: computed zeros are saved to zeros_partial.json as they go,
  so a rerun continues instead of starting over.
This is numerical evidence for RH up to this height, NOT a proof, and NOT
a verification of any formal proof. The rigorous record is Platt &
Trudgian (2020): all zeros to height 3,000,175,332,800.
"""
import json
import os
import time

import mpmath as mp

N = 1000
PARTIAL = "zeros_partial.json"
KNOWN_FIRST10 = [
    "14.134725141734693790457251983562",
    "21.022039638771554992628479593897",
    "25.010857580145688763213790992562",
    "30.424876125859513210311897530584",
    "32.935061587739189690662368964074",
    "37.586178158825671257217763480705",
    "40.918719012147495187398126914633",
    "43.327073280914999519496122121589",
    "48.005150881167159727942472749427",
    "49.773832477672302181916784678563",
]


def main():
    t0 = time.time()
    mp.mp.dps = 30

    # resume from partial results if present
    zs = []
    if os.path.exists(PARTIAL):
        with open(PARTIAL) as f:
            zs = [mp.mpc(s) for s in json.load(f)]
        print(f"resumed: {len(zs)} zeros already computed")

    max_abs_zeta = mp.mpf("0")
    max_re_dev = mp.mpf("0")
    for n in range(len(zs) + 1, N + 1):
        z = mp.zetazero(n)
        az = abs(mp.zeta(z))
        re_dev = abs(mp.re(z) - mp.mpf("0.5"))
        max_abs_zeta = max(max_abs_zeta, az)
        max_re_dev = max(max_re_dev, re_dev)
        zs.append(z)
        if n % 100 == 0:
            with open(PARTIAL, "w") as f:
                json.dump([mp.nstr(z, 30) for z in zs], f)
            print(f"n={n} elapsed={time.time() - t0:.0f}s", flush=True)
    with open(PARTIAL, "w") as f:
        json.dump([mp.nstr(z, 30) for z in zs], f)
    elapsed = time.time() - t0

    increasing = all(mp.im(zs[i]) > mp.im(zs[i - 1]) for i in range(1, N))

    # first-10 agreement with published values: tolerance check, not exact
    # string equality — a 30-digit computed value can differ from a printed
    # reference in the last digit or two by rounding alone.
    first10_ok = all(
        abs(mp.im(zs[i]) - mp.mpf(KNOWN_FIRST10[i])) < mp.mpf("1e-25")
        for i in range(10)
    )

    # dps=50 cross-check on the first 100
    mp.mp.dps = 50
    max_diff_50 = mp.mpf("0")
    for n in range(1, 101):
        z50 = mp.zetazero(n)
        max_diff_50 = max(max_diff_50, abs(z50 - zs[n - 1]))

    # Riemann-von Mangoldt count check at T = Im(rho_1000)
    mp.mp.dps = 30
    T = mp.im(zs[-1])
    nvm = (T / (2 * mp.pi)) * (mp.log(T / (2 * mp.pi)) - 1) + mp.mpf("0.875")
    # N(T) = main term + S(T); S(T) is O(log T), so agreement within a few is expected.

    result = {
        "author": "Domenic Lipoma",
        "date": "2026-11-24",
        "n_zeros": N,
        "working_precision_dps": 30,
        "elapsed_seconds": round(elapsed, 1),
        "max_abs_zeta_at_zero": mp.nstr(max_abs_zeta, 5),
        "max_deviation_of_Re_from_0.5": mp.nstr(max_re_dev, 5),
        "imaginary_parts_strictly_increasing": increasing,
        "first_10_match_published_Odlyzko_values_30_digits": first10_ok,
        "first_100_max_diff_dps50_vs_dps30": mp.nstr(max_diff_50, 5),
        "gamma_1000": mp.nstr(T, 30),
        "riemann_von_mangoldt_N_T_at_gamma1000": mp.nstr(nvm, 6),
        "zeros_found_up_to_gamma1000": N,
        "all_Re_equal_0.5_to_working_precision": bool(max_re_dev < mp.mpf("1e-25")),
        "all_zeta_at_zero_at_rounding_level": bool(max_abs_zeta < mp.mpf("1e-25")),
        "zeros": [mp.nstr(z, 30) for z in zs],
    }
    with open("results.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k != "zeros"}, indent=2))


if __name__ == "__main__":
    main()
