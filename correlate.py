#!/usr/bin/env python3
"""Pearson and Spearman correlation for every pair of numeric columns in a file.

Standard library only. No installs.

    python correlate.py examples/platform_vs_crm.csv
    python correlate.py my_data.csv --lag 1
    python correlate.py my_data.csv --drop 8

The first column is treated as the date (or week, or period) and is only used
for labels and --drop. Every other column must be numbers.
"""

import argparse
import csv
import math
import sys
from itertools import combinations

SMALL_N = 12          # below this many paired rows, results are a rough read at best
DIVERGENCE = 0.2      # Pearson and Spearman this far apart usually means an outlier or a curve


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return None  # a column that never changes has no correlation
    return sxy / math.sqrt(sxx * syy)


def ranks(values):
    """Rank values 1..n. Ties share the average of their ranks."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(x, y):
    """Spearman is Pearson run on the ranks."""
    return pearson(ranks(x), ranks(y))


def read_table(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if any(cell.strip() for cell in r)]
    if len(rows) < 3:
        sys.exit("Need a header row plus at least two rows of data.")
    header, body = rows[0], rows[1:]
    if len(header) < 3:
        sys.exit("Need a date column plus at least two numeric columns.")
    labels = [r[0] for r in body]
    columns = {}
    for c, name in enumerate(header[1:], start=1):
        vals = []
        for line, r in enumerate(body, start=2):
            raw = r[c].strip().replace(",", "").replace("$", "").replace("%", "") if c < len(r) else ""
            try:
                vals.append(float(raw))
            except ValueError:
                sys.exit(f'Row {line}, column "{name}": "{raw}" is not a number.')
        columns[name] = vals
    return labels, columns


def shift(x, y, lag):
    """Line up x at period t with y at period t + lag."""
    if lag > 0:
        return x[:-lag], y[lag:]
    if lag < 0:
        return x[-lag:], y[:lag]
    return x, y


def fmt(v):
    return "n/a " if v is None else f"{v:5.2f}"


def main():
    p = argparse.ArgumentParser(description="Pearson and Spearman for every pair of columns.")
    p.add_argument("file", help="CSV with a date column first, then two or more numeric columns")
    p.add_argument("--lag", type=int, default=0,
                   help="shift the second column of each pair by N periods "
                        "(1 = does the second column follow the first by one period?)")
    p.add_argument("--drop", action="append", default=[],
                   help="leave out a row by its date label, e.g. --drop 8 (repeatable)")
    args = p.parse_args()

    labels, columns = read_table(args.file)
    keep = [i for i, lab in enumerate(labels) if lab not in args.drop]
    if args.drop:
        missing = set(args.drop) - set(labels)
        if missing:
            sys.exit(f"--drop: no row labeled {', '.join(sorted(missing))}.")
        columns = {k: [v[i] for i in keep] for k, v in columns.items()}

    if args.lag:
        print(f"Lag: {args.lag} period(s). Second column shifted.")
    if args.drop:
        print(f"Dropped rows: {', '.join(args.drop)}")

    for a, b in combinations(columns, 2):
        x, y = shift(columns[a], columns[b], args.lag)
        n = len(x)
        print(f"\n{a}  vs  {b}")
        if n < 3:
            print("  Not enough rows to compare after the lag.")
            continue
        r, rho = pearson(x, y), spearman(x, y)
        print(f"  Pearson  {fmt(r)}")
        print(f"  Spearman {fmt(rho)}")
        print(f"  n        {n}")
        if n < SMALL_N:
            print(f"  ! Small sample ({n} rows). Treat this as a rough read, not a finding.")
        if r is not None and rho is not None and abs(r - rho) > DIVERGENCE:
            print(f"  ! Pearson and Spearman differ by {abs(r - rho):.2f}. "
                  "Usually one outlier period or a curved relationship. Look at the rows.")


if __name__ == "__main__":
    main()
