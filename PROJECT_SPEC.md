# PROJECT_SPEC.md

## 1. Project

**Working Name:** ProductQuant

**Status:** Experimental / Research Prototype

**Version:** v0.1

ProductQuant is an experimental quantitative research system for e-commerce product selection.

The system treats products, SKUs, product families, keywords, and categories as researchable assets and attempts to discover measurable signals that may predict future commercial performance.

The core objective is to build a:

> **Backtestable, explainable, and iteratively improvable product ranking / signal system.**

ProductQuant MUST NOT recommend products merely because a heuristic, LLM, or human intuition claims they "look promising."

Every material ranking factor should eventually be supported, rejected, or qualified by empirical evidence.

---

# 2. Core Research Question

The project asks:

> Can product-selection decisions be formalized as a quantitative ranking problem in which observable signals at time `t` predict measurable product or category performance over a future horizon?

Formally:

Given a universe of products \(U_t\) observable at time \(t\), construct features:

\[
X_{i,t} = \{x_1, x_2, ..., x_n\}
\]

for product or product entity \(i\).

A signal model produces:

\[
S_{i,t} = f(X_{i,t})
\]

Products are ranked by \(S_{i,t}\).

Future outcomes are measured over horizons such as:

- 7 days
- 30 days
- 60 days
- 90 days

The research system evaluates whether ranking at time `t` contains predictive information about those future outcomes.

---

# 3. Product Philosophy

ProductQuant is primarily a **research platform**, not an automated e-commerce business.

v0.1 optimizes for:

1. reproducibility;
2. historical correctness;
3. explainability;
4. data lineage;
5. backtestability;
6. cheap experimentation;
7. modular data sources;
8. iterative factor research.

It does NOT optimize for:

- storefront management;
- automated purchasing;
- supplier negotiation;
- ad placement;
- live inventory management;
- automated order execution;
- automated product listing;
- generative product marketing;
- autonomous commercial decisions.

Those may become downstream applications if the research system demonstrates useful predictive power.

---

# 4. Core Principle

## No Evidence, No Alpha

No factor is considered useful because it sounds reasonable.

Every factor MUST be treated as a hypothesis.

For example:

> "Fast-growing search interest predicts future product demand."

is NOT a fact.

It is a testable hypothesis.

The system should allow researchers to determine whether:

\[
Corr(Factor_{i,t}, Outcome_{i,t+h}) > 0
\]

and whether that relationship is:

- statistically meaningful;
- economically meaningful;
- stable over time;
- stable across categories;
- robust to reasonable parameter changes;
- obtainable without look-ahead bias.

Factors that fail validation SHOULD remain recordable as negative research results.

Negative results are evidence.

---

# 5. Unit of Analysis

ProductQuant MUST NOT assume that a single marketplace SKU is always the correct research unit.

The architecture SHOULD support multiple entity levels:

### SKU / Listing

A specific marketplace listing.

Example:

`marketplace + listing_id`

### Product

A normalized real-world product that may correspond to multiple listings.

### Product Family

A group of related variants.

### Keyword / Product Concept

Example:

`portable espresso maker`

### Category

Example:

`Home > Kitchen > Coffee`

v0.1 MAY implement only a subset.

However, internal schemas SHOULD avoid making future support for other entity levels unnecessarily difficult.

---

# 6. Universe Construction

Every backtest requires an explicitly defined universe.

Example:

```text
Universe:
Marketplace: X
Category: Kitchen
Minimum listing age: 30 days
Minimum observations: 20
Price: 10–100 USD
Observation date: 2026-01-01
```

The universe MUST be reconstructable for historical dates whenever the underlying data permits.

Universe definitions MUST be versioned.

The system MUST avoid survivorship bias where possible.

Products that later disappeared MUST NOT silently disappear from historical universes.

---

# 7. Data Architecture

Use a layered data architecture.

```text
External Sources
      ↓
Collectors
      ↓
Raw Immutable Data
      ↓
Normalization / Entity Resolution
      ↓
Canonical Observations
      ↓
Feature / Factor Computation
      ↓
Signal Generation
      ↓
Ranking
      ↓
Backtest
      ↓
Evaluation / Research Report
```

Each layer MUST have explicit ownership and schema boundaries.

---

# 8. Data Collection Principles

## 8.1 Source Preference

Data sources SHOULD be preferred approximately in this order:

1. official APIs;
2. licensed or documented third-party APIs;
3. downloadable public datasets;
4. stable public structured endpoints;
5. compliant HTML extraction;
6. browser automation;
7. fragile scraping techniques.

Scraping SHOULD NOT be the default merely because it is technically possible.

---

# 9. Initial Data Sources

The following sources are candidates, not guaranteed dependencies.

Every source MUST undergo feasibility validation before becoming part of the production research pipeline.

## 9.1 Marketplace Listing Data

Desired fields include:

```text
listing_id
product_id
title
category
brand
seller
price
original_price
discount
currency
rating
review_count
sold_count / sales proxy
inventory / availability proxy
shipping cost
delivery estimate
seller rating
listing age
images
attributes
timestamp
```

Not all sources will expose all fields.

Missingness MUST be explicit.

---

## 9.2 eBay

Preferred initial integration candidate:

**eBay Browse API**

Potential capabilities:

- keyword search;
- category search;
- GTIN search;
- product search;
- listing retrieval;
- price;
- seller information;
- shipping information;
- return-policy information;
- product review information where available;
- listing availability.

Authentication and API limitations MUST be documented.

The collector SHOULD persist raw API responses before normalization.

---

# 10. Amazon

Amazon SHOULD be treated as a separate adapter.

Do NOT implement against deprecated assumptions.

Amazon Product Advertising API / PA-API legacy documentation MUST NOT be treated as the current canonical integration path.

Investigate the currently supported Amazon Creators API and any applicable access requirements before implementation.

Potential complementary commercial datasets MAY be evaluated for:

- historical price;
- sales-rank history;
- offer history;
- review history;
- availability.

Any third-party provider MUST be isolated behind an adapter.

ProductQuant MUST remain functional without a specific commercial provider.

---

# 11. TikTok Shop

TikTok Shop SHOULD initially be considered an optional source.

Official seller APIs may expose catalog information for authorized shops but MUST NOT be assumed to provide unrestricted marketplace-wide intelligence.

Possible future acquisition methods include:

- authorized seller data;
- documented marketplace APIs if available;
- approved third-party providers;
- compliant public-page collection.

Feasibility MUST be demonstrated before TikTok Shop becomes a core dependency.

---

# 12. Google Trends

Google Trends is a candidate source for measuring external demand.

Possible observations:

```text
keyword
timestamp
interest
region
search_type
related_query
related_topic
```

Possible search types include:

- Web Search;
- Google Shopping;
- YouTube;
- Image Search;
- News Search.

Third-party providers such as DataForSEO or SerpApi MAY be evaluated.

Direct scraping MAY be explored experimentally but SHOULD NOT become a critical dependency without reliability evidence.

---

# 13. Google Trends Data Warning

Google Trends values MUST NOT be interpreted as absolute search volume.

Trend values are normalized relative measurements.

Therefore the system MUST preserve enough metadata to reconstruct:

```text
query
comparison group
time window
region
search type
retrieval timestamp
provider
```

Historical observations retrieved under incompatible normalization contexts MUST NOT be naively concatenated.

The research pipeline SHOULD investigate:

- anchor keywords;
- overlapping windows;
- calibration;
- repeated sampling;
- smoothing;
- missing-value treatment;
- normalization stability.

This is a research problem in its own right.

---

# 14. Search / Social Demand Sources

Future adapters MAY investigate:

### Search

- Google Trends;
- Google Shopping signals;
- search-volume providers;
- keyword-planning datasets.

### Social

Potential future sources:

- TikTok;
- YouTube;
- Reddit;
- other legally accessible public trend sources.

Potential signals:

```text
mention_count
mention_growth
engagement
engagement_growth
creator_count
video_count
view_velocity
sentiment
topic acceleration
```

Social signals SHOULD NOT enter the core model until reliable historical snapshots exist.

---

# 15. Collection Methods

Collectors MUST implement a common conceptual interface.

Example:

```python
class DataSource:
    def collect(self, query, timestamp):
        ...

    def normalize(self, raw):
        ...

    def metadata(self):
        ...
```

Actual implementation MAY differ.

Each collection event MUST record:

```text
source
collector_version
retrieval_time
query_parameters
raw_response_reference
success/failure
rate_limit_state if known
schema_version
```

---

# 16. Raw Data Preservation

Raw observations SHOULD be immutable.

Recommended structure:

```text
data/
    raw/
        source/
            YYYY/
                MM/
                    DD/
    normalized/
    features/
    datasets/
```

Alternatively, an object store/database MAY be used.

Normalized data MUST be reproducible from raw observations whenever practical.

Never silently overwrite historical observations.

---

# 17. Snapshot Collection

Historical backtesting requires historical state.

Therefore ProductQuant MUST support scheduled snapshot collection.

Example:

```text
daily marketplace snapshot
daily/weekly Google Trends snapshot
weekly review-count snapshot
weekly category snapshot
```

Snapshot frequency MUST be configurable per source.

Collection timestamps MUST be explicit.

---

# 18. Historical Bootstrap

Because the project begins without years of internally collected snapshots, v0.1 SHOULD investigate historical bootstrap sources.

Possible approaches:

- APIs exposing historical observations;
- public datasets;
- commercial datasets;
- price-history providers;
- search-trend history;
- archived marketplace datasets.

Historical bootstrap data MUST be labeled separately from first-party collected snapshots.

Data provenance MUST survive normalization.

---

# 19. Canonical Observation Schema

A normalized marketplace observation SHOULD approximately support:

```text
entity_id
entity_type
source
source_entity_id

timestamp

title
category
brand

price
currency
discount

rating
review_count

sales_value
sales_proxy_type

availability

seller_id
seller_rating

metadata

source_timestamp
retrieved_at
schema_version
```

Null values are acceptable.

Fabricated values are not.

---

# 20. Feature Store

Factors MUST be derived from point-in-time observations.

Example factor families:

## Demand

- search interest;
- search volume proxy;
- review velocity;
- sales-rank proxy;
- sold-count proxy.

## Momentum

- 7d growth;
- 30d growth;
- 90d growth;
- acceleration;
- breakout strength.

## Competition

- active listing count;
- seller count;
- listing growth;
- market concentration;
- price crowding.

## Pricing

- median category price;
- relative price;
- discount intensity;
- price stability;
- price dispersion.

## Margin Proxy

Possible inputs:

- observed retail price;
- estimated wholesale cost;
- fulfillment estimate;
- shipping estimate;
- marketplace fees.

Margin estimates MUST be labeled estimates.

## Social Attention

- mention velocity;
- view velocity;
- creator growth;
- engagement growth.

## Quality

- rating;
- rating change;
- review distribution;
- complaint signals.

## Stability

- demand volatility;
- price volatility;
- ranking volatility.

## Saturation

Example concept:

\[
Saturation =
\frac{SupplyGrowth}{DemandGrowth + \epsilon}
\]

## Risk

Possible proxies:

- abnormal review patterns;
- high price volatility;
- seller concentration;
- product fragility;
- extreme seasonality;
- IP / compliance risk;
- fulfillment complexity.

---

# 21. Point-in-Time Correctness

This is a HARD requirement.

When computing a factor for timestamp `t`, the system MUST use only information that would have been available at or before `t`.

No future observations may leak into:

- factor computation;
- normalization;
- universe construction;
- model training;
- threshold selection.

Backtests violating point-in-time correctness are invalid.

---

# 22. Factor Definition

Each factor MUST have a machine-readable definition.

Example:

```yaml
factor:
  id: search_momentum_30d
  version: 1
  entity_type: product_keyword

  inputs:
    - google_trends_interest

  calculation:
    method: percentage_change
    lookback_days: 30

  direction:
    expected: positive

  hypothesis:
    "Increasing search attention predicts future commercial growth."

  limitations:
    - normalized input
    - sparse low-volume queries
```

Factor definitions MUST be versioned.

Changing a factor formula creates a new factor version.

---

# 23. Signal Model

v0.1 SHOULD begin with simple interpretable models.

Preferred baseline:

\[
Score_i =
\sum_j w_j z(Factor_{i,j})
\]

where:

- \(Factor_{i,j}\) is factor `j` for product `i`;
- \(z\) is a normalization or ranking transform;
- \(w_j\) is an explicit weight.

Example only:

```text
Demand Momentum      25%
Demand Level         15%
Competition          15%
Margin Proxy         15%
Social Momentum      10%
Quality              10%
Stability            10%
```

These weights MUST NOT be treated as validated.

They are research parameters.

---

# 24. Ranking

The system MUST support:

- absolute scores;
- percentile scores;
- category-relative rankings;
- global rankings;
- factor contribution breakdowns.

For any ranked entity, the system SHOULD be able to explain:

```text
Why is this ranked #3?

+0.81 search momentum
+0.43 review velocity
+0.31 relative margin
-0.22 competition
-0.17 volatility
--------------------
score = ...
```

Explainability is a core requirement.

---

# 25. Outcome / Target Definition

"Good product" is too vague.

Every experiment MUST define a measurable forward target.

Examples:

```text
forward_30d_review_growth
forward_30d_sales_proxy_growth
forward_30d_search_growth
forward_60d_rank_improvement
forward_90d_demand_growth
```

Different targets MAY produce different useful factors.

Targets MUST be versioned and documented.

---

# 26. Product IC

ProductQuant SHOULD implement an Information Coefficient inspired by quantitative finance.

For factor \(F\):

\[
IC_t =
Corr(F_{i,t}, Outcome_{i,t+h})
\]

Evaluate:

```text
Mean IC
Median IC
IC standard deviation
IC hit rate
Rank IC
IC by category
IC by period
IC decay by horizon
```

Spearman rank correlation SHOULD be supported.

Pearson correlation MAY also be supported.

---

# 27. Quantile Analysis

Factors SHOULD support quantile analysis.

Example:

Divide the universe into five buckets:

```text
Q1 — lowest factor
Q2
Q3
Q4
Q5 — highest factor
```

Measure future outcomes for each bucket.

A useful factor SHOULD ideally demonstrate some degree of monotonic relationship.

Example:

```text
Q1    -2.1%
Q2    +0.4%
Q3    +2.8%
Q4    +5.9%
Q5    +11.2%
```

Do not require monotonicity by definition, but report it.

---

# 28. Backtesting

The backtesting engine MUST simulate historical ranking decisions.

Example:

```text
Every Monday:

1. reconstruct observable universe;
2. compute available factors;
3. generate scores;
4. rank products;
5. select Top N;
6. measure future outcomes;
7. record results.
```

Supported rebalance periods SHOULD eventually include:

- daily;
- weekly;
- monthly.

v0.1 MAY implement weekly only.

---

# 29. Portfolio Analogy

ProductQuant MAY treat selected products as a research portfolio.

Example:

```text
Top 10
Top 20
Top decile
Top quintile
```

Metrics MAY include:

```text
average forward outcome
median forward outcome
hit rate
relative performance
turnover
concentration
drawdown-like deterioration
category exposure
```

This does NOT imply financial returns.

Terminology MUST clearly distinguish commercial proxy outcomes from investment returns.

---

# 30. Baselines

Every strategy MUST be compared against baselines.

At minimum:

### Random

Random selection from the same universe.

### Popularity

Highest current demand/popularity.

### Momentum

Highest recent demand growth.

### Simple Heuristic

A manually defined common-sense score.

A complicated model that cannot outperform simple baselines is not considered useful.

---

# 31. Walk-Forward Evaluation

When model fitting is introduced, evaluation SHOULD use walk-forward methodology.

Example:

```text
Train:
Jan–Jun

Validate:
Jul

Advance window

Train:
Feb–Jul

Validate:
Aug
```

Random train/test splits SHOULD NOT be the default for temporal prediction.

---

# 32. Factor Decay

The system SHOULD measure predictive strength across horizons.

Example:

```text
Factor: search_momentum

7d IC     0.21
30d IC    0.17
60d IC    0.08
90d IC    0.01
```

This allows estimation of signal decay.

---

# 33. Factor Stability

A factor MUST NOT be judged only by full-period performance.

Evaluate across:

- time periods;
- categories;
- marketplaces;
- price ranges;
- product maturity;
- demand regimes.

The research report SHOULD expose unstable factors.

---

# 34. Missing Data

Missing data MUST remain distinguishable from zero.

The system MUST NOT silently:

- convert unavailable values to zero;
- forward-fill indefinitely;
- interpolate without recording the transformation.

Missing-data policy MUST be explicit per feature.

---

# 35. LLM Usage

LLMs MAY assist with:

- entity normalization;
- category mapping;
- attribute extraction;
- semantic product clustering;
- review classification;
- product-risk classification;
- research report generation;
- hypothesis generation.

LLMs MUST NOT be treated as empirical evidence.

Example:

```text
LLM says:
"Portable blenders appear promising."

Evidence status:
UNVALIDATED HYPOTHESIS
```

LLM-generated factors MUST undergo the same backtesting requirements as manually designed factors.

---

# 36. Entity Resolution

The same real-world product may appear under multiple listings or marketplaces.

The architecture SHOULD eventually support:

```text
Listing A ─┐
Listing B ─┼── Canonical Product
Listing C ─┘
```

Possible evidence:

- GTIN;
- UPC/EAN;
- brand;
- model number;
- normalized title;
- attributes;
- image similarity;
- semantic similarity.

v0.1 MAY defer sophisticated entity resolution.

---

# 37. Data Leakage Tests

The test suite MUST include safeguards against:

- look-ahead bias;
- future-derived normalization;
- future category membership;
- survivor-only datasets;
- improperly joined timestamps.

At least one synthetic dataset SHOULD intentionally contain future information and verify that the pipeline rejects or isolates it.

---

# 38. Reproducibility

Every experiment MUST record:

```text
experiment_id
git_commit
dataset_version
universe_version
factor_versions
target_version
signal_model_version
parameters
start_date
end_date
random_seed
execution_timestamp
results
```

Given preserved data and code, an experiment SHOULD be reproducible.

---

# 39. Research Registry

The project SHOULD maintain a machine-readable research registry.

Example:

```text
factor_id
hypothesis
status
tested_period
universe
target
mean_ic
rank_ic
hit_rate
notes
evidence
```

Possible statuses:

```text
PROPOSED
TESTING
SUPPORTED
WEAK
REJECTED
UNSTABLE
BLOCKED
```

A rejected factor SHOULD NOT be deleted.

---

# 40. Data Source Registry

Maintain a registry containing:

```text
source_id
provider
source_type
official/unofficial
authentication
cost
rate_limits
historical_depth
fields
terms_constraints
reliability
collector_status
last_verified
```

Source capabilities MUST be evidence-backed.

Do not assume that a field exists because a blog post or previous implementation says so.

---

# 41. Source Feasibility Spike

Before building substantial factor infrastructure, the first implementation milestone SHOULD conduct a source feasibility spike.

For each candidate source, determine:

```text
Can we access it?
What does it cost?
What fields exist?
Is history available?
How stable is it?
Can it be automated?
What are the rate limits?
What legal/ToS constraints exist?
Can raw observations be persisted?
Can historical backtests be supported?
```

Results MUST be recorded as evidence.

---

# 42. Suggested v0.1 Source Strategy

Prefer a minimal combination of:

### Marketplace Source

One marketplace with sufficiently accessible structured listing data.

Candidate:

- eBay Browse API.

### External Demand Source

One independent attention/demand signal.

Candidate:

- Google Trends through a reliable provider or validated collection method.

### Historical Source

At least one source capable of providing enough historical information to perform a meaningful initial backtest.

If no sufficiently good historical marketplace source can be obtained cheaply, the project SHOULD:

1. explicitly document the limitation;
2. begin snapshot accumulation;
3. use historical proxy targets for early research;
4. avoid pretending that a proper historical backtest exists.

---

# 43. Storage

v0.1 SHOULD prefer simple local infrastructure.

Acceptable starting stack:

```text
DuckDB
+
Parquet
```

or equivalent.

Do NOT introduce distributed infrastructure without evidence that it is needed.

The system SHOULD make migration to larger analytical storage possible later.

---

# 44. CLI / Research Interface

v0.1 SHOULD expose a simple research interface.

Illustrative commands:

```bash
productquant source list

productquant collect ebay --query "portable espresso maker"

productquant collect trends --query "portable espresso maker"

productquant factor compute search_momentum_30d

productquant backtest run experiments/baseline.yaml

productquant report experiment <id>
```

Exact command names are implementation decisions.

A GUI is NOT required for v0.1.

---

# 45. Experiment Configuration

Experiments SHOULD be declarative.

Example:

```yaml
experiment:
  name: momentum_baseline

universe:
  marketplace: ebay
  category: example-category

period:
  start: 2025-01-01
  end: 2026-01-01

rebalance:
  frequency: weekly

factors:
  - search_momentum_30d
  - review_velocity_30d
  - competition_density

signal:
  method: weighted_sum

target:
  metric: forward_demand_growth
  horizon_days: 30

selection:
  method: top_n
  n: 20
```

---

# 46. Reports

Each experiment SHOULD produce a human-readable report containing:

```text
Experiment
Universe
Dataset
Period

Factor definitions

Coverage / missingness

Factor distributions

IC
Rank IC
IC over time

Quantile performance

Top-N performance

Baseline comparison

Factor contribution

Failure cases

Known biases

Conclusion
```

Reports SHOULD distinguish observations from interpretations.

---

# 47. Architecture Boundary

Recommended conceptual modules:

```text
productquant/

    sources/
        ebay/
        amazon/
        trends/

    ingestion/

    storage/

    entities/

    universe/

    features/

    factors/

    signals/

    targets/

    backtest/

    evaluation/

    experiments/

    reports/

    cli/
```

This is guidance, not a mandatory directory layout.

Architecture MAY evolve through ADRs.

---

# 48. Explicit Non-Goals for v0.1

Do NOT prioritize:

- web dashboard;
- mobile app;
- automated store creation;
- automated product purchasing;
- supplier negotiation;
- advertisement automation;
- generative product photography;
- automated listing publication;
- real-money inventory allocation;
- complex deep learning;
- reinforcement learning;
- autonomous agents making commercial commitments.

---

# 49. v0.1 Success Criteria

v0.1 is successful when the repository can demonstrate an end-to-end research loop:

```text
Acquire Data
      ↓
Preserve Raw Observations
      ↓
Normalize
      ↓
Construct Historical Dataset
      ↓
Define Universe
      ↓
Compute ≥ 3 Factors
      ↓
Generate Ranking
      ↓
Define Forward Target
      ↓
Run Backtest
      ↓
Compare Against Baselines
      ↓
Calculate IC / Rank IC
      ↓
Generate Reproducible Report
```

At least one experiment MUST be reproducible from repository instructions.

---

# 50. Minimum Research Demonstration

Before declaring v0.1 complete, demonstrate:

- ≥1 marketplace source;
- ≥1 independent demand source;
- ≥1 historical or pseudo-historical dataset;
- ≥3 factors;
- ≥1 composite ranking signal;
- ≥2 baselines;
- ≥1 forward target;
- point-in-time-safe backtesting;
- IC or Rank IC;
- quantile analysis;
- reproducible experiment configuration;
- generated research report.

The project does NOT need to discover profitable alpha.

A valid conclusion may be:

> "The tested factors contain no meaningful predictive information."

That is a successful research result if the experiment is methodologically sound.

---

# 51. Initial Milestones

## Phase 0 — Research & Source Validation

Investigate candidate sources.

Produce:

- source registry;
- API/scraping feasibility evidence;
- cost estimates;
- historical-data assessment;
- recommended initial marketplace;
- recommended initial demand source.

Do NOT build large abstractions before this is complete.

## Phase 1 — Data Foundation

Implement:

- source adapters;
- raw persistence;
- normalized schema;
- timestamp semantics;
- basic dataset construction.

### Restricted Phase 1 — UCI Transaction-Event Data Foundation

**Status:** `ACCEPTED`

**Authority:** `DECISION-PHASE0-01` and `DECISION-PHASE1-01`, approved by `human:technical-owner` and durably recorded at `2026-08-12T07:24:20Z`.

Phase 1 MUST initially use UCI Online Retail II only as a historical transaction-event research substrate. This authorization does not make UCI a marketplace observation source and does not authorize any inference or reconstruction of historical listings, availability, marketplace supply, competition, independent demand, or a complete product-selection universe.

The Phase 1 deliverable MUST:

1. preserve the byte-exact, digest-pinned UCI ZIP as immutable local raw data outside Git;
2. normalize retained physical workbook rows into a versioned `transaction_event.v1` Parquet artifact with source-row provenance;
3. apply `uci-online-retail-ii-sheet-boundary-v1`: retain `Year 2009-2010` only before dataset-local naïve `2010-12-01T00:00:00`, and retain `Year 2010-2011` at or after that boundary;
4. preserve within-sheet duplicates, cancellations, signed quantities and prices, nulls, extremes, observed text, and pseudonymous source customer references without imputation or future-derived enrichment;
5. record retrieval/build provenance, source and output digests, schema/adapter versions, explicit timestamp semantics, quality counts, success/failure, and raw references in immutable manifests and receipts;
6. fail closed on source digest, archive member, workbook sheet/header, required type, or normalized schema drift;
7. provide deterministic rebuilds and local DuckDB verification without making a persistent DuckDB database a second source of truth; and
8. keep every unsupported capability explicit in manifests, documentation, and later reports.

The accepted `transaction_event.v1` contract contains:

```text
event_id: string, required
raw_artifact_id: string, required
source_id: string, required
source_member: string, required
source_sheet: string, required
source_row_number: int64, required
event_time_local: timestamp[us] without timezone, required
source_invoice_id: string, required
source_product_code: string, required
description_observed: string, nullable
quantity: int64, required
unit_price: decimal128(18,3), required
currency_code: string, required and provider-declared GBP
customer_reference: string, nullable
country_observed: string, required
invoice_is_cancellation: boolean, required
schema_version: string, required and equal to transaction_event.v1
```

`event_id` MUST be derived deterministically from the pinned raw artifact, canonical source sheet, and 1-based physical Excel row. Numeric integral identifiers MUST become base-10 strings without a `.0` suffix; existing strings MUST NOT be trimmed or case-normalized. Numeric descriptions MAY be losslessly represented as integral text while the original cell remains recoverable through the raw artifact, sheet, and row pointer. Prices MUST NOT be silently rounded to fit the contract.

The exact event ID is:

```text
uci-online-retail-ii:sha256:<lowercase-archive-sha256>:<sheet-token>:<source-row-number>
```

The only sheet-token mappings are `Year 2009-2010 -> year-2009-2010` and `Year 2010-2011 -> year-2010-2011`. The source row is 1-based and includes the header, so the first data row is `2`.

The supported Phase 1 software interface is limited to:

```text
productquant uci fetch     --data-root PATH [--offline]
productquant uci normalize --data-root PATH
productquant uci verify    --data-root PATH
productquant uci prepare   --data-root PATH [--offline]
```

The default data root is `./data`. Offline operation MUST NOT access the network and requires a complete raw bundle, including its acquisition manifest. Exit status `0` means success, including a verified idempotent no-op; `2` means usage error, `3` network failure, `4` source-integrity or schema drift, `5` local I/O/state conflict, and `1` an unexpected internal failure.

Successful commands MUST emit exactly one JSON object plus newline to stdout with fields `command`, `status`, `data_root`, `artifacts`, `statistics`, and `receipt_path`. `status` is `created` if any requested artifact was created and otherwise `verified`. Failures after a valid command is recognized MUST emit exactly one row-free JSON object plus newline to stderr with fields `command`, `status: error`, `error: {code, message}`, and nullable `receipt_path`. A parser/usage failure before a valid command is recognized MUST use the same shape with `command: null`, exit `2`, and `receipt_path: null`; parser help remains ordinary text on stdout and does not create a receipt. No command may log transaction or customer rows. No public Python API is part of this phase.

Command receipts are immutable local operational state and contain only execution/provenance metadata, artifact references, aggregate statistics, and sanitized errors. They MUST NOT contain row values. Raw, normalized, and receipt artifacts MUST remain under Git-ignored local `data/`; on POSIX, newly created data directories/files MUST be owner-only. Publishing, remotely storing, enriching, or linking `customer_reference` to another identity requires a separate privacy/authority decision.

For any future as-of consumer, information available at cutoff `t` is limited to rows with `event_time_local <= t`. Future targets, when separately authorized, begin strictly after `t`. Phase 1 MUST NOT materialize a product universe, target, factor, ranking, backtest, or research result. It MUST NOT use later descriptions, prices, product codes, aggregate statistics, or any other future information to fill earlier state.

Each raw and normalized manifest MUST declare at least:

```text
transaction-event history: supported
marketplace listing state: unsupported
marketplace supply/competition: unsupported
independent external demand: unsupported
complete product/opportunity universe: unsupported
integrated ProductQuant v0.1 demonstration: unsupported
historical provider revision state: unknown
timezone: unknown
```

This wording was reconciled at `2026-08-12T08:27:52Z` to preserve the exact
owner-approved `DECISION-PHASE1-01` requirement that every manifest carry these
capability declarations; the earlier accepted text incorrectly limited the
declarations to normalized manifests.

The marketplace and demand blockers remain unresolved. Section 50 remains unmet. Any Phase 2 transaction-demand factor semantics, including cancellation/return/netting policy, require a separate accepted specification before implementation.

## Phase 2 — Factor Engine

Implement at least three factors.

Recommended initial hypotheses:

1. demand momentum;
2. competition/saturation;
3. price positioning.

## Phase 3 — Backtesting

Implement:

- historical universe;
- forward targets;
- ranking;
- baselines;
- IC;
- Rank IC;
- quantile analysis.

## Phase 4 — Research Report

Produce the first evidence-backed report.

Answer:

> Did any tested signal predict future product performance better than trivial baselines?

## Phase 5 — Review

Conduct independent review of:

- data leakage;
- source assumptions;
- timestamp correctness;
- survivorship bias;
- factor validity;
- reproducibility;
- conclusions.

Material findings MUST be resolved or explicitly accepted before milestone closure.

---

# 52. Protocol Integration

This repository follows the project's existing multi-agent collaboration protocol.

Agents MUST treat:

- `BOOTSTRAP.md`
- `PROJECT_SPEC.md`
- `HANDOFF.md`
- ADRs
- evidence records

according to the authority hierarchy defined by that protocol.

Implementation state MUST NOT silently redefine product requirements.

Changes to this specification require explicit justification.

Architectural decisions SHOULD be captured in ADRs.

Material claims SHOULD be supported by evidence.

Incomplete work MUST leave sufficient state for another agent instance to resume without relying on conversational memory.

---

# 53. Human Authority Boundary

Agents MAY autonomously:

- research public data sources;
- implement collectors;
- design schemas;
- write tests;
- run experiments;
- propose factors;
- reject unsupported hypotheses;
- refactor implementation;
- update HANDOFF/evidence according to protocol.

Agents MUST escalate before:

- purchasing paid datasets or API plans;
- creating material external costs;
- accepting restrictive commercial terms;
- publishing data;
- using private credentials not already authorized;
- performing actions against real merchant accounts;
- making real commercial transactions.

---

# 54. Guiding Question

Every major feature should ultimately help answer:

> **What information available at time `t` helps rank products by their expected future commercial performance, and how strong, stable, and reproducible is that information?**

If a proposed feature does not materially help answer that question, it is probably outside the current scope.
