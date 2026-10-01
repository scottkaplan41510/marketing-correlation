# Marketing Correlation

Give it two or more columns of numbers over the same dates. It tells you
whether they move together.

You get a Pearson and a Spearman for every pair, plus n, plus a warning when
the sample is small or when the two numbers disagree.

Try it free in the browser, no signup:
[redavio.com/tools/correlation](https://www.redavio.com/tools/correlation)

It does not imply causality. It's a quick read on what relates to what.

## Why

In performance marketing you're almost always holding two numbers from two
sources that were never going to match. Ad platform conversions with their own
self-reported attribution, and MQLs in your CRM. Different models, different
tracking, cookie issues.

They won't tie out. A correlation tells you whether they at least move
together, which is often the thing you actually need to know.

## The 30-second version

You get back a value between 1 and -1.

- 1 is a perfect positive relationship. They move together.
- -1 is a perfect negative relationship. One goes up, the other goes down.
- 0 means no relationship.

My rule of thumb: anything consistently around 0.6 and up and I feel pretty good.

## Pearson or Spearman

Run both.

- **Pearson** uses the actual values and asks how close the points sit to a
  straight line.
- **Spearman** ranks both columns first, then runs the same math on the ranks.
  It asks whether the two columns put the periods in the same order. It
  handles relationships that consistently go one direction even when they
  aren't a straight line.

When they disagree by more than about 0.2, you've usually got one outlier
period or a curve. Worth a look.

## Run it

Requires Python 3.8+. Nothing to install.

```
git clone https://github.com/scottkaplan41510/marketing-correlation
cd marketing-correlation
python3 correlate.py examples/platform_vs_crm.csv
```

Your file needs a date (or week) column first, then two or more columns of
numbers. Commas, dollar signs and percent signs are stripped for you.

Options:

- `--lag 1` shifts the second column by one period. If an email drops Tuesday
  and conversions land Friday, the two may not line up until you shift one.
- `--drop 8` leaves out a row by its date label, so you can see how much one
  period is doing.

Or skip all of this. Paste two columns into an LLM and ask for a Pearson and a
Spearman correlation. You'll have it in about three seconds. The script is here
for when you want it repeatable.

## The examples

Both datasets are from the post and are illustrative, not real account data.

**Platform conversions vs CRM MQLs** (`examples/platform_vs_crm.csv`)

```
platform_conversions  vs  crm_mqls
  Pearson   0.91
  Spearman  0.95
  n        8
```

The counts don't match. They move together.

**LLM mentions vs direct sessions** (`examples/llm_mentions_vs_direct.csv`)

```
llm_mentions  vs  direct_sessions
  Pearson   0.75
  Spearman  1.00
  n        8
  ! Pearson and Spearman differ by 0.25.
```

Week 8 is a spike. Pearson gets dragged down by it. Spearman says every week
still ranks in the same order on both sides. Run it with `--drop 8` and Pearson
goes to 1.00.

## Make it yours

Go nuts with it.

- **Any input:** an ad platform export, HubSpot, Salesforce, GA4, a database
  table, an API. If it's numbers by date, it works. Claude Code will wire up
  the connection for you.
- **Any pair:** platform conversions vs CRM MQLs, LLM mentions vs direct and
  branded traffic, email sends vs direct traffic.
- **Fork it:** schedule it, plug it into your reporting, add more checks.
  The Claude Code skill in `.claude/skills/` does most of the lifting.

## The honest caveats

- It doesn't imply causality.
- Pearson won't catch a relationship that isn't a straight line. Spearman
  will, as long as it keeps going one direction. Neither catches a
  relationship that goes up and then comes back down.
- A handful of data points will tell you nothing. The script warns you under
  12 rows. The examples above are 8 rows, on purpose, to keep them readable.
- Timing matters. Use `--lag` when one thing takes time to show up in the other.

If you've got a data scientist, use them. This isn't a replacement. It's a
quick tool to get your head around what relates to what.

## License

MIT
