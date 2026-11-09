#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright OpenBMC Authors
"""Generate a seed corpus for the query_param_fuzzer.

Each seed is one query-parameter string (the part after '?' in a Redfish
URI).  Random mutation rarely produces the exact $-prefixed keys and the
balanced parenthesis/levels syntax the parser looks for, so the seeds cover
the valid grammar ($expand with levels, $select tries, $top/$skip, only,
$filter expressions), combinations, and invalid values that drive the
error-message paths.

Usage: query_param_fuzzer_seeds.py <output-zip>
"""

import zipfile

SEEDS = [
    "only",
    "$expand=*",
    "$expand=.",
    "$expand=.($levels=1)",
    "$expand=*($levels=2)",
    "$expand=*($levels=9)",
    "$expand=Chassis($levels=1),Power",
    "$expand=Power,Thermal,Sensors",
    "$select=Id",
    "$select=Status/Health,PowerState",
    "$select=a/b/c",
    "$select=a/b/c/d/e/f/g/h",
    "$top=1",
    "$skip=2&$top=3",
    "$filter=Id=cpu0",
    "$filter=Health=^OK&$top=1",
    "$filter=A=B&$filter=C=D",
    "$expand=*&$select=Id&$top=2&$skip=0&only",
    "$unknown=1",
    "$top=99999999999999999999",
    "$top=-1",
    "$skip=-1",
    "$expand=bogus",
    "$expand=($levels=1)",
    "$select=",
    "$filter=",
    "only=unexpected",
    "%24expand=%2A",
    "a=1&a=2&a=3",
    "k=",
    "=v",
    "&",
    "$expand",
    "$top=0",
]

DICT = r'''# Dictionary for query_param_fuzzer: Redfish query keys, values and syntax.
"$expand="
"$select="
"$top="
"$skip="
"$filter="
"only"
"("
")"
"*"
"."
"($levels=1)"
"($levels=2)"
"Chassis"
"Power"
"Thermal"
"Sensors"
"Id"
"Status/Health"
"PowerState"
"="
"^"
"<"
">"
"&"
","
"/"
"1"
"0"
"-1"
'''


def main() -> None:
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output-zip>", file=sys.stderr)
        raise SystemExit(1)
    out = sys.argv[1]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for index, seed in enumerate(SEEDS, 1):
            z.writestr(f"{index:04d}", seed.encode())
    print(f"wrote {len(SEEDS)} seeds to {out}")


if __name__ == "__main__":
    main()
