---
name: run-correlation
description: Check whether two or more marketing metrics move together (Pearson and Spearman) from a CSV, export, or data source. Use when someone asks if two numbers are related, correlated, or move together, e.g. platform conversions vs CRM MQLs, LLM mentions vs direct traffic.
---

# Run a correlation

1. Get the data into a CSV: date (or week) column first, then two or more
   numeric columns covering the same periods. If it comes from an export, an
   API or a database, write a small loader that produces that shape.
2. Run `python3 correlate.py <file>`.
3. If one series likely lags the other (email drops Tuesday, conversions land
   Friday), rerun with `--lag 1`, `--lag 2` and report which lines up best.
4. If the script says Pearson and Spearman differ, find the period doing the
   damage and rerun with `--drop <label>` to show the difference.
5. Explain in plain English: the value, n, and both warnings. Say "moves with"
   or "correlates with", never "causes". Spearman covers relationships that
   consistently go one direction, not every curve.
