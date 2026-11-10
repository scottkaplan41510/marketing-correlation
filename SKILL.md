---
name: marketing-correlation
description: Checks whether two or more marketing metrics move together over time, with Pearson and Spearman correlation, sample size, optional lag, and warnings for small samples and outliers. Use when someone asks if two numbers are related, correlated, or move together, or whether one follows another, for example ad platform conversions vs CRM MQLs, LLM mentions vs direct traffic, or email sends vs conversions.
license: MIT
compatibility: Needs Python 3.8 or later. Standard library only, no installs, no network.
---

# Marketing correlation

`correlate.py`, in the same folder as this file, prints Pearson and Spearman
correlation for every pair of numeric columns in a CSV, plus n, plus warnings.

## When to use it

- The user has two or more numbers tracked over the same periods (days, weeks,
  months) and wants to know if they move together.
- The user wants to know if one number follows another after a delay.
- Not for: two numbers with no shared time periods, a single column, or proving
  that one thing causes another.

## Steps

1. Get the data into a CSV. First column: the date, week or period label. Then
   two or more numeric columns covering the same periods, one row per period.
   Commas, `$` and `%` are stripped automatically. If the data is in an export,
   a spreadsheet, an API or a database, write a small loader that produces this
   shape. Do not make up or fill in missing values; drop incomplete periods and
   say so.

   ```
   week,platform_conversions,crm_mqls
   1,120,41
   2,135,47
   ```

2. Run it, using the path to the folder this file is in:

   ```
   python3 <skill-folder>/correlate.py data.csv
   ```

3. If one series likely shows up later than the other (an email drops Tuesday,
   conversions land Friday), rerun with `--lag 1`, then `--lag 2`, and report
   which lines up best. `--lag N` shifts the second column of each pair by N
   periods, so it asks "does the second column follow the first by N periods?"
   A lag shortens n by N.

4. If the script warns that Pearson and Spearman differ, find the period doing
   the damage (look for a spike or a dip in the rows) and rerun with
   `--drop <label>` to show how much that one period moves the result.
   `--drop` can repeat.

## Reading the output

```
platform_conversions  vs  crm_mqls
  Pearson   0.91
  Spearman  0.95
  n        8
  ! Small sample (8 rows). Treat this as a rough read, not a finding.
```

- **Values run from -1 to 1.** 1 = they rise and fall together. -1 = one rises
  as the other falls. 0 = no relationship. Around 0.6 and up, consistently, is a
  reasonable sign they move together. Below about 0.3 is weak.
- **Pearson** uses the actual values: how close the points sit to a straight line.
- **Spearman** ranks each column first: do the two put the periods in the same
  order? It holds up for relationships that keep going one direction without
  being a straight line, and it is less sensitive to one extreme period.
- **n** is the number of paired periods used, after any lag or drop.
- **n/a** means a column never changed, so there is nothing to correlate.

## Warnings to pass on

- **Small sample.** Under 12 rows the script warns. Say plainly that the result
  is a rough read, not a finding. A handful of points can produce a high
  correlation by chance.
- **Pearson and Spearman disagree** by more than 0.2. Usually one outlier period
  or a curved relationship. Show the rows and the `--drop` result before
  drawing a conclusion.
- **Correlation is not causation.** Say "moves with" or "correlates with",
  never "drives" or "causes". Both numbers may follow a third thing, such as
  seasonality, budget changes or a launch.
- Neither measure catches a relationship that rises and then falls back.
- Timing matters. A weak result at lag 0 can be strong at lag 1.

## How to report back

Lead with one plain sentence ("Platform conversions and CRM MQLs move together
closely: Pearson 0.91, Spearman 0.95, over 8 weeks"). Then n, any warning, and
what to check next. Keep it short.
