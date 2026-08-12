# Demand Source Feasibility: Google Trends and Documented Providers

## Metadata

- **ID:** EVIDENCE-20260812T060101Z-demand-source-feasibility
- **Title:** Google Trends, DataForSEO, SerpApi, and BigQuery demand-source feasibility
- **Captured UTC:** 2026-08-12T06:03:58Z
- **Recorded by:** agent:codex-demand-evidence
- **Claim supported or challenged:** No examined demand source is currently both authorized for this repository and demonstrated to reconstruct historical provider states. The official Google Trends API is the preferred strategic candidate but remains limited-access alpha; DataForSEO Google Trends Explore Standard is the preferred practical authenticated probe only after human authorization.
- **Related requirements:** [PROJECT_SPEC.md section 12](../PROJECT_SPEC.md#12-google-trends), [section 13](../PROJECT_SPEC.md#13-google-trends-data-warning), [section 41](../PROJECT_SPEC.md#41-source-feasibility-spike), [section 42](../PROJECT_SPEC.md#42-suggested-v01-source-strategy)
- **Related ADRs/issues:** [ISSUE-20260812T031400Z-phase-0-source-feasibility](../ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md)
- **Repository revision/state:** HEAD 3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1 on main tracking origin/main. Before this record was added, git status showed modified HANDOFF.md and untracked ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md; no earlier demand evidence record existed.
- **Environment:** Darwin 25.3.0 arm64; curl 8.7.1 via SecureTransport; Git 2.50.1; Asia/Shanghai host timezone; observations and timestamps below use UTC. No account, credential, authorization header, API key, paid service, or browser automation was used.

## Method

- **Procedure:** Read the current official Google Trends API, Trends Help, Google Cloud, DataForSEO, and SerpApi documentation. Compare access, authentication, cost, rate limits, fields, history, timestamp semantics, reconstructability, point-in-time safety, reliability, terms, and raw-response retention. Then issue one credential-free request to each practical endpoint and one ordinary request to the public Trends Explore page. Inspect Google Trends robots.txt without crawling disallowed paths beyond the single feasibility request.
- **Exact command/input:**

        probe_dir=$(mktemp -d /tmp/productquant-demand-probe.XXXXXX)
        date -u '+captured=%Y-%m-%dT%H:%M:%SZ'
        uname -srm
        curl -sS -D "$probe_dir/google_ui.headers" -o "$probe_dir/google_ui.body" -w 'google_ui http=%{http_code} bytes=%{size_download} content_type=%{content_type}\n' 'https://trends.google.com/trends/explore?date=today%2012-m&q=wireless%20earbuds'
        curl -sS -D "$probe_dir/dataforseo_standard.headers" -o "$probe_dir/dataforseo_standard.body" -w 'dataforseo_standard http=%{http_code} bytes=%{size_download} content_type=%{content_type}\n' -H 'Content-Type: application/json' --data '[{"keywords":["wireless earbuds"],"location_name":"United States","language_code":"en","type":"web","date_from":"2025-01-01","date_to":"2025-01-31"}]' 'https://api.dataforseo.com/v3/keywords_data/google_trends/explore/task_post'
        curl -sS -D "$probe_dir/dataforseo_sandbox.headers" -o "$probe_dir/dataforseo_sandbox.body" -w 'dataforseo_sandbox http=%{http_code} bytes=%{size_download} content_type=%{content_type}\n' -H 'Content-Type: application/json' --data '[{"keywords":["wireless earbuds"],"location_name":"United States","language_code":"en","type":"web","date_from":"2025-01-01","date_to":"2025-01-31"}]' 'https://sandbox.dataforseo.com/v3/keywords_data/google_trends/explore/task_post'
        curl -sS -D "$probe_dir/serpapi.headers" -o "$probe_dir/serpapi.body" -w 'serpapi http=%{http_code} bytes=%{size_download} content_type=%{content_type}\n' --get --data-urlencode 'engine=google_trends' --data-urlencode 'q=wireless earbuds' --data-urlencode 'date=2025-01-01 2025-01-31' --data-urlencode 'data_type=TIMESERIES' 'https://serpapi.com/search.json'
        curl -sS -D "$probe_dir/bigquery_tables.headers" -o "$probe_dir/bigquery_tables.body" -w 'bigquery_tables http=%{http_code} bytes=%{size_download} content_type=%{content_type}\n' 'https://bigquery.googleapis.com/bigquery/v2/projects/bigquery-public-data/datasets/google_trends/tables'
        curl -sS 'https://trends.google.com/robots.txt' | sed -n '1,220p' | rg -n 'explore|api|Disallow|Allow' | sed -n '1,120p'
        shasum -a 256 "$probe_dir"/*.body "$probe_dir"/*.headers

- **Exit status:** The shell commands and all curl transports exited 0. Application responses were HTTP 429 for the public Trends Explore page and HTTP 401 for DataForSEO Standard, DataForSEO sandbox, SerpApi, and the BigQuery REST table-list request. These are negative access observations, not successful data retrievals.
- **Repeatability:** Re-run the commands from any networked shell without credentials. HTTP status may vary by network reputation, provider policy, and time. Re-read every linked provider page because pricing, quotas, access status, and terms are mutable. An authorized payload test requires a separate human-approved account and must preserve its complete request, response, retrieval time, and normalization context.

## Raw observation

### Credential-free endpoint observations

| Target | HTTP response | Concise unaltered response | Response-body SHA-256 |
|---|---:|---|---|
| Google Trends Explore page | 429; 1,701 bytes; text/html | Error 429 (Too Many Requests) | 0f3675e9d1c9eea537c48d88702a445668f5f4ad6c972847fa131eca03710b02 |
| DataForSEO Standard task POST | 401; 223 bytes; application/json | {"status_code":40100,"status_message":"You are not Authorized to Access this Resource. Your Login Information Here: https:\/\/app.dataforseo.com\/login .","time":"0 sec.","cost":0,"tasks_count":0,"tasks_error":0,"tasks":[]} | 08c970d9cb960d054b36b3ef905189ca7e658907b7de2217f63af62e5180cdd6 |
| DataForSEO sandbox task POST | 401; 223 bytes; application/json | {"status_code":40100,"status_message":"You are not Authorized to Access this Resource. Your Login Information Here: https:\/\/app.dataforseo.com\/login .","time":"0 sec.","cost":0,"tasks_count":0,"tasks_error":0,"tasks":[]} | 08c970d9cb960d054b36b3ef905189ca7e658907b7de2217f63af62e5180cdd6 |
| SerpApi Google Trends | 401; 97 bytes; application/json | { "error": "Invalid API key. Your API key should be here: https://serpapi.com/manage-api-key" } | 9739e353f7ed3e477cd58a80e7bbe169d7041cec08bf9d4c47a9bc984b82551d |
| BigQuery Google Trends table list | 401; 838 bytes; application/json | Request is missing required authentication credential. | 89287e48eb34fcbc20f41d0c455c6e30a11cd9dfc94bdb02311ee8e2911754c1 |

The Trends robots.txt observation was:

        4:Disallow: /explore?
        5:Disallow: /trends/explore?

No endpoint returned demand data. The DataForSEO responses reported cost 0. The HTTP 429 and robots directives demonstrate that direct unattended collection from the Explore website is operationally fragile from this environment; they do not by themselves establish a contractual prohibition or universal failure from every network.

### Authoritative documentation checked

- Google Trends API alpha: https://developers.google.com/search/apis/trends
- Google Trends API announcement: https://developers.google.com/search/blog/2025/07/trends-api
- Google Trends sampling and normalization FAQ: https://support.google.com/trends/answer/4365533?hl=en
- Google Trends CSV export and attribution: https://support.google.com/trends/answer/4365538?hl=en
- Google Trends BigQuery dataset: https://support.google.com/trends/answer/12764470?hl=en
- Google Cloud BigQuery dataset semantics: https://cloud.google.com/blog/products/data-analytics/top-25-google-search-terms-now-in-bigquery
- DataForSEO Google Trends Explore Live documentation: https://docs.dataforseo.com/v3/keywords_data-google-trends-explore-live/
- DataForSEO Keywords Data overview: https://docs.dataforseo.com/v3/keywords-data-overview/
- DataForSEO Google Trends pricing: https://dataforseo.com/pricing/keywords-data/google-trends
- DataForSEO rate and task limits: https://dataforseo.com/help-center/rate-limits-and-request-limits
- DataForSEO result retention: https://dataforseo.com/help-center/how-long-do-you-keep-results
- DataForSEO trial and minimum payment: https://dataforseo.com/help-center/minimum-payment
- DataForSEO terms: https://dataforseo.com/terms-of-service
- DataForSEO proprietary Trends API reference: https://docs.dataforseo.com/v3/keywords_data-dataforseo_trends-explore-live/
- DataForSEO proprietary Trends API pricing: https://dataforseo.com/pricing/keywords-data/dataforseo-trends-api-pricing
- SerpApi Google Trends reference: https://serpapi.com/google-trends-api
- SerpApi pricing: https://serpapi.com/pricing
- SerpApi result retention and SLA FAQ: https://serpapi.com/faq
- SerpApi Google Trends release notes: https://serpapi.com/google-trends-api/release-notes
- SerpApi terms: https://serpapi.com/legal

### Official Google Trends API alpha

- **Current accessibility:** CONFIRMED application-only alpha for a limited tester cohort. It is not documented as generally available.
- **Authentication:** UNKNOWN. Public pages do not disclose the endpoint, credential form, application acceptance mechanics beyond the form, or production onboarding contract.
- **Cost and rate limits:** UNKNOWN. No public alpha price, quota, per-user limit, or billing model was found.
- **Available fields/capabilities:** CONFIRMED documentation advertises consistently scaled relative search interest, region and subregion restrictions, and daily, weekly, monthly, and yearly aggregation. A complete response schema is not public.
- **Historical depth:** CONFIRMED rolling 1,800 days, approximately five years, with data through two days before retrieval.
- **Timestamp semantics:** CONFIRMED documented values represent aggregated search-interest periods, not absolute search counts. UNKNOWN whether responses expose provider observation time, revision version, data-finality status, or vintage.
- **Historical reconstruction and point-in-time safety:** UNKNOWN. Consistent cross-request scaling would improve longitudinal collection, but public documentation does not establish revision policy, historical vintages, or an as-of interface. A series retrieved today for an old interval is not evidence of what the API returned at that old date.
- **Operational reliability:** INFERRED pre-production risk because Google explicitly describes the alpha as limited testing for functionality and feedback. Public SLA and incident history are unavailable.
- **Terms/licensing and raw preservation:** Google documents use of Trends information subject to Google Terms and requires attribution when reused. The public alpha page does not establish the eventual API agreement or long-term raw-response retention rights.
- **v0.1 status:** CONDITIONAL strategic preference. Apply only with human authorization; do not treat it as an available v0.1 dependency until access, terms, quotas, raw retention, and a real revision probe are verified.

### Google Trends website and manual CSV

- **Current accessibility and authentication:** CONFIRMED public manual interface and documented manual CSV export; no authentication requirement is stated for ordinary use. The single direct request from this environment returned HTTP 429.
- **Cost and rate limits:** CONFIRMED no charge was requested for manual access. Published automation quota is UNKNOWN.
- **Available fields:** CONFIRMED the website supports interest-over-time comparisons, geography, search type, and related topics/queries. Values are sampled, anonymized, aggregated, normalized to the request's time and location context, and scaled 0–100; low volume may appear as zero and statistical noise may be present.
- **Historical depth:** CONFIRMED current Help supports custom time ranges and multi-year comparison. Exact maximum history for every search type was not established from Google Help in this check.
- **Timestamp semantics:** Chart dates are search-event aggregation intervals. The CSV is generated at retrieval; it does not provide a historical provider-state version. ProductQuant must add retrieval timestamp, query, comparison terms, window, region, category, and search type.
- **Historical reconstruction and point-in-time safety:** UNKNOWN. Re-running an old range retrieves a current retrospective calculation. Window-relative normalization, sampling, noise, and undocumented revision behavior prevent the result from proving what was observable at the historical decision time.
- **Operational reliability:** The HTTP 429 and robots directives make undocumented unattended extraction unsuitable as a core collector. Manual CSV remains useful for human spot checks.
- **Terms/licensing and raw preservation:** Google explicitly documents CSV export and reuse with attribution subject to Google Terms. This does not establish permission for high-volume automated collection. Manual raw CSV can be preserved technically, but an automated archival policy was not validated.
- **v0.1 status:** NOT SUITABLE as an automated dependency; useful only for manual verification.

### Official Google Trends BigQuery public dataset

- **Current accessibility and authentication:** CONFIRMED Google documents access through BigQuery and a no-credit-card BigQuery sandbox. The direct REST table-list request without OAuth returned HTTP 401, so unattended API access was not demonstrated.
- **Cost and rate limits:** CONFIRMED BigQuery free tier advertises up to 1 TB of queries and 10 GB of storage per month; use above those thresholds follows ordinary BigQuery pricing. A Trends-specific request-rate limit is not published.
- **Available fields:** CONFIRMED top 25 and top 25 rising terms, with fields demonstrated in official SQL including refresh_date, week, DMA name/ID, term, score, and rank. International tables add country and region dimensions.
- **Historical depth:** CONFIRMED United States daily data has a rolling five-year historical window and hourly data has a rolling one-year window; international daily data has a rolling five-year window.
- **Timestamp semantics:** CONFIRMED refresh_date identifies the daily published set. Each selected term is enriched with retrospective historical values. Official documentation says daily top/rising sets are new partitions retained for 30 days.
- **Historical reconstruction and point-in-time safety:** INFERRED not suitable as an arbitrary-keyword historical universe. The current top-25 selection determines which terms receive historical backfill, so old values inside a current partition contain current-selection information. Only retained refresh-date partitions or prospectively preserved snapshots can support selection-time analysis.
- **Operational reliability:** Google-managed structured delivery is preferable to scraping, but the limited top-25 universe and 30-day partition retention are hard source constraints. No authenticated query or SLA measurement was performed.
- **Terms/licensing and raw preservation:** Query results can be exported technically, and Google permits Trends reuse subject to Terms and attribution. Dataset-specific long-term archival terms were not independently resolved in this spike.
- **v0.1 status:** SUITABLE only for discovery, cross-checking, or prospective top-term snapshots; not the primary arbitrary-product demand source and not a historical point-in-time bootstrap.

### DataForSEO Google Trends Explore

- **Current accessibility and authentication:** CONFIRMED documented Standard and Live endpoints using account-issued API login/password with HTTP Basic authentication. Both production and sandbox rejected the credential-free request. The sandbox requires an account and returns generated samples rather than request-reflective live data.
- **Cost:** CONFIRMED Standard costs USD 0.0027 per task and Live costs USD 0.011 per task, with up to five keywords per task. New accounts are advertised a USD 1 trial credit; paid top-up has a USD 50 minimum. No account was created and no credit was consumed.
- **Rate limits:** CONFIRMED Standard supports up to 2,000 API calls per minute and recommends at most 100 tasks per POST. Live is one task per call, may encounter errors above 250 Google Trends Explore tasks per minute, and shares a documented 500,000-request daily Google Trends capacity across DataForSEO users.
- **Available fields:** CONFIRMED web, news, YouTube, images, and Google Shopping search types; graph, map, related-topics, and related-queries results; request context; result retrieval datetime; interval date_from/date_to; Unix timestamp; missing_data; relative values; geographic identifiers; and a Google Trends check URL.
- **Historical depth:** CONFIRMED documentation accepts web history from 2004-01-01 and other search types from 2008-01-01.
- **Timestamp semantics:** The result datetime is when DataForSEO received the response. Graph timestamps and date ranges are search-interest intervals. Neither is a historical provider-vintage identifier.
- **Historical reconstruction and point-in-time safety:** INFERRED pseudo-historical only. The endpoint obtains a current Google Trends Explore calculation over a requested old range; it does not expose what Google or DataForSEO returned at the old date. Ending the requested range at a decision date reduces obvious future-window normalization leakage but does not resolve sampling, revisions, backfills, or historical-vintage uncertainty.
- **Operational reliability:** DataForSEO self-reports 99.95% uptime, while its own Google Trends documentation warns of upstream capacity restrictions and recommends Standard. A real response, repeated-sample stability, revision behavior, and endpoint-specific incident performance remain untested.
- **Terms/licensing and raw preservation:** CONFIRMED Standard results remain retrievable from DataForSEO for 30 days; Live results are not retained by DataForSEO and its documentation tells clients to store them if needed. This establishes technical preservation, not a clear licence for permanent ProductQuant archival or downstream modelling. Google reuse remains subject to Google Terms and attribution; provider and source retention rights require clarification.
- **v0.1 status:** CONDITIONAL preferred practical probe, specifically the Google Trends Explore Standard endpoint rather than DataForSEO's separate proprietary Trends signal. Proceed only after the human owner authorizes an account and zero-purchase trial, then preserve raw JSON and test repeat sampling, overlapping windows, historical revisions, timestamps, and retention terms.

### SerpApi Google Trends

- **Current accessibility and authentication:** CONFIRMED documented API-key authentication; the credential-free request returned HTTP 401.
- **Cost and rate limits:** CONFIRMED free plan offers 250 searches per month and throughput of 50 per hour. Starter is USD 25 per month for 1,000 searches and 200 per hour; higher plans increase both.
- **Available fields:** CONFIRMED timeseries, region comparison, interest by region, related topics, and related queries. Responses include request parameters, creation/processing metadata, timeline dates and Unix timestamps, relative values, and provider links to JSON and raw HTML.
- **Historical depth:** CONFIRMED the official endpoint reference defines `all` as 2004–present and accepts custom dates from 2004 to present. Completeness for every Google search property remains unverified without an authenticated response.
- **Timestamp semantics:** search_metadata creation/processing times describe SerpApi retrieval. Timeline timestamps describe retrospective search-interest intervals. No historical provider-vintage field is documented.
- **Historical reconstruction and point-in-time safety:** INFERRED pseudo-historical for the same reason as DataForSEO: a response produced now for an old period does not reconstruct the response available then.
- **Operational reliability:** SerpApi advertises a 99.95% SLA, but its own Google Trends release notes list several recent failures and degradation events, including response-time and timeout remediation in July 2026. No authenticated request or independent uptime measurement was performed.
- **Terms/licensing and raw preservation:** CONFIRMED SerpApi stores JSON and raw HTML for 31 days. Its terms disclaim uninterrupted/error-free service and leave downstream lawful use with the client; they do not establish ownership of underlying Google data. Permanent client-side retention rights remain unresolved.
- **v0.1 status:** NOT RECOMMENDED as the primary source at current evidence. It may be useful as a later authenticated cross-check, but is more expensive than DataForSEO Standard and has documented recent Google Trends incidents.

### DataForSEO proprietary Trends API

This is a separate product from DataForSEO Google Trends Explore. It must not be described as Google Trends data.

- **Current accessibility and authentication:** CONFIRMED the official reference documents a Live proprietary Trends endpoint under the authenticated Keywords Data API. No authenticated call was made; the Google Trends Explore `401` probe does not verify this endpoint's successful payload.
- **Cost and rate limits:** CONFIRMED the current proprietary Trends pricing page advertises USD 0.0012 per task. Exact account/effective limits and charged cost remain UNKNOWN without an authorised account probe.
- **Available fields and methodology:** CONFIRMED the provider describes relative keyword popularity and related data for Google Search, Google News, and Google Shopping. Its documented proprietary algorithm combines association with relevant pages/articles/listings, content popularity, and anonymous user web-behaviour data from multiple sources. Source weights, calibration, revision, and validation methodology are not disclosed sufficiently for ProductQuant reproducibility.
- **Historical depth:** CONFIRMED the official reference advertises web history from 2004-01-01 and other types from 2008-01-01.
- **Timestamp and point-in-time semantics:** UNKNOWN whether the proprietary estimates are versioned or reconstruct the provider state available at historical factor time `t`. The relative scale and opaque algorithm prevent an independent point-in-time reconstruction claim.
- **Raw preservation, terms, and reliability:** JSON is technically returnable, but permanent archival/use rights, underlying-source licences, input revisions, and endpoint-specific reliability were not established. The general DataForSEO contractual limitations described above still require review.
- **v0.1 status:** NOT SUITABLE. Its opaque blended methodology conflicts with the first backtest's explainability and reproducibility goals; use Google Trends Explore rather than this product for any authorised provider comparison.

## Interpretation

- **CONFIRMED:** The official Google Trends API offers the strongest documented scaling semantics for future longitudinal research, but remains limited-access alpha with public authentication, cost, quota, schema, SLA, and archival terms unresolved.
- **CONFIRMED:** Google Trends values are relative, sampled, normalized, aggregated, and noised; they are not absolute search volume.
- **CONFIRMED:** Manual CSV export is documented, but a single normal Explore request from this environment was throttled and robots.txt disallows query-bearing Explore paths.
- **CONFIRMED:** DataForSEO and SerpApi expose structured retrieval and provider retrieval timestamps only after account authentication. The credential-free probes verified the access boundary, not returned fields or data quality.
- **CONFIRMED:** BigQuery is limited to top and rising terms and uses refresh-date partitions with retrospective history; it is not an arbitrary-keyword history interface.
- **INFERRED:** A time series whose points refer to 2025 but which was retrieved in 2026 is retrospective or pseudo-historical. It is not a preserved 2025 provider state unless the source supplies a historical vintage/as-of contract or ProductQuant actually captured the response in 2025.
- **INFERRED:** At high confidence, but not as legal advice, provider-side ability to return or retain JSON does not itself grant ProductQuant the right to archive underlying Google data permanently or use it for modelling. Written terms or provider clarification must resolve that separately.
- **INFERRED:** There is no currently cleared external-demand source for strict point-in-time v0.1 backtesting. Strategically prefer the official API if alpha access is granted. Practically prefer one human-authorized, zero-purchase DataForSEO Google Trends Explore Standard probe; retain SerpApi only as a possible cross-check.
- **UNKNOWN:** Whether any alpha applicant from this project would be accepted, what agreement would apply, and whether the official API preserves or versions revisions.
- **UNKNOWN:** Whether DataForSEO permits permanent raw-response archival and ProductQuant modelling under its contract and the underlying Google terms.
- **UNKNOWN:** Actual repeated-sample variation, late revision magnitude, missing-value behavior, response schema stability, and query latency for all authenticated candidates.

## Limitations and residual uncertainty

- No account was created, no credential was available or used, and no paid or trial task was submitted. Therefore authenticated accessibility, real response fields, costs charged, and data quality remain unverified.
- The HTTP 429 is one request from one network and cannot establish global availability. It does establish that an undocumented UI collector would need anti-throttling work immediately, which this milestone intentionally does not introduce.
- Published prices, quotas, access status, terms, and provider retention periods can change. Re-check before any account authorization and after 30 days or a provider announcement.
- Provider uptime and SLA claims were not independently measured. SerpApi incident observations come from its own release notes.
- No repeated retrievals were available to measure sampling or revisions. No claim of point-in-time safety is made for retrospective Google Trends results.
- Terms analysis is a technical feasibility reading, not legal advice.
- Probe bodies and headers were kept only in a disposable /tmp directory long enough to hash and excerpt them; they are not committed because they contain no demand data and the inline excerpts are sufficient to reproduce the access observations.

## Integrity and provenance

- **Artifact location:** INLINE in this record; authoritative mutable sources are the URLs listed under Raw observation.
- **Artifact digest:** Probe response-body SHA-256 values are recorded in the credential-free endpoint table. Header SHA-256 values: Google UI e8d5c74538ddc4b11d2af73c46c0c5b7326629db8ee224c9e8f4c453556947d5; DataForSEO Standard bb9a8a1192384dd2898b4fc5cc1694d7f6e0d49efc0e56ffd90f378c17b95c04; DataForSEO sandbox 0f25c02ca5409659d64cd942633a114360d0df0a3b4debd7463032f19ed3c5a4; SerpApi 2bc2e4867b4fa04b71f7f4d26b931a9c90df0591a244db04b5e5f47589877f89; BigQuery 36447b9b7c8ce5dde77add9a1f91da51d98690cbd999f1e6a6d5294b9608f388.
- **External retention risk:** HIGH. Documentation and terms are mutable; Google alpha details are incomplete; DataForSEO Standard retains task results for 30 days; SerpApi retains JSON/raw HTML for 31 days; BigQuery refresh partitions are documented as 30-day sets. Preserve future authorized responses locally with retrieval metadata only after retention rights are confirmed.
- **Supersedes / superseded by:** NONE

## Corrections

Preserve the original observation. Append attributable corrections rather than silently changing it.

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| NONE | NONE | NONE | NONE |
