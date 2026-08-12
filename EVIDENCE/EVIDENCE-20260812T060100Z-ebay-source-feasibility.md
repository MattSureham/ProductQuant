# eBay Source Feasibility

## Metadata

- **ID:** `EVIDENCE-20260812T060100Z-ebay-source-feasibility`
- **Title:** `eBay marketplace-source accessibility, history, and usage constraints`
- **Captured UTC:** `2026-08-12T06:03:25Z`
- **Recorded by:** `agent:codex-ebay-evidence`
- **Claim supported or challenged:** eBay exposes current listing discovery and a prospective change-feed path, but it cannot presently supply ProductQuant with an authorized historical bootstrap or an immediately usable v0.1 marketplace source.
- **Related requirements:** [`PROJECT_SPEC.md` sections 8-18, 21, 40-42, and 51](../PROJECT_SPEC.md)
- **Related ADRs/issues:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](../ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md); ADRs `NONE`
- **Repository revision/state:** `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1` on `main`; at `2026-08-12T06:01:40Z`, `HANDOFF.md` was modified, `ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md` was untracked, and this evidence path did not yet exist.
- **Environment:** Darwin `25.3.0` arm64; `curl 8.7.1`; public internet; no eBay credentials, developer account, EPN account, paid service, or authenticated session used.

## Method

- **Procedure:** Read the current official eBay developer documentation listed below; compare Browse, Feed Beta, Marketplace Insights, deprecated interfaces, and seller Product Research against ProductQuant's required fields and point-in-time semantics; then make credential-free requests to production and sandbox API endpoints.
- **Official documentation inputs (checked 2026-08-12 UTC):**
  - [Browse API overview](https://developer.ebay.com/api-docs/buy/api-browse.html)
  - [Browse `ItemSummary` fields](https://developer.ebay.com/api-docs/buy/browse/types/gct%3AItemSummary)
  - [Browse `Item` fields](https://developer.ebay.com/api-docs/buy/browse/types/gct%3AItem)
  - [Buy APIs requirements](https://developer.ebay.com/api-docs/buy/buy-requirements.html)
  - [OAuth authorization](https://developer.ebay.com/develop/guides-v2/authorization)
  - [Default API call limits](https://developer.ebay.com/develop/get-started/api-call-limits)
  - [Feed Beta overview and feed-file filters](https://developer.ebay.com/api-docs/buy/api-feed_beta.html)
  - [`getItemFeed`](https://developer.ebay.com/api-docs/buy/feed/resources/item/methods/getItemFeed)
  - [`getItemSnapshotFeed`](https://developer.ebay.com/api-docs/buy/feed/resources/item_snapshot/methods/getItemSnapshotFeed)
  - [Buy API marketplace support](https://developer.ebay.com/api-docs/buy/ref-marketplace-supported.html)
  - [API deprecation status](https://developer.ebay.com/develop/get-started/api-deprecation-status)
  - [Developer account tiers](https://developer.ebay.com/signin)
  - [API status](https://developer.ebay.com/support/api-status)
  - [API License Agreement](https://developer.ebay.com/join/api-license-agreement)
  - [Seller Product Research description](https://export.ebay.com/en/resources/seller-news/releases-archive/2024-july-seller-update/tools-you-can-trust/)
- **Exact command/input:**

```sh
curl -sS --connect-timeout 10 --max-time 30 \
  -o /dev/null -w 'http_status=%{http_code}\n' \
  'https://api.ebay.com/buy/browse/v1/item_summary/search?q=phone&limit=1'

curl -sS --connect-timeout 10 --max-time 30 \
  -H 'Authorization: Bearer deliberately-invalid-phase0-probe' \
  -w '\nhttp_status=%{http_code}\n' \
  'https://api.ebay.com/buy/browse/v1/item_summary/search?q=phone&limit=1'

curl -sS --connect-timeout 10 --max-time 30 \
  -H 'Accept: application/json,text/tab-separated-values' \
  -H 'X-EBAY-C-MARKETPLACE-ID: EBAY_US' \
  -H 'Range: bytes=0-1023' \
  -w '\nhttp_status=%{http_code}\n' \
  'https://api.ebay.com/buy/feed/v1_beta/item?feed_scope=ALL_ACTIVE&category_id=625'

curl -sS --connect-timeout 10 --max-time 30 \
  -H 'Authorization: Bearer deliberately-invalid-phase0-probe' \
  -w '\nhttp_status=%{http_code}\n' \
  'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?q=phone&limit=1'
```

- **Exit status:** all four `curl` processes exited `0`; HTTP statuses were respectively `403`, `401`, `400`, and `401`.
- **Repeatability:** Run the commands from any internet-connected host. The fake bearer value is intentional and is not a credential. Re-read all linked terms before relying on the result because access rules, schemas, quotas, and licence terms can change.

## Raw observation

### Credential-free endpoint probes

Captured at `2026-08-12T06:03:04Z` to `2026-08-12T06:03:25Z`:

```text
Browse production, no Authorization header:
http_status=403
exit_status=0

Browse production, deliberately invalid bearer:
{
  "errors": [{
    "errorId": 1001,
    "domain": "OAuth",
    "category": "REQUEST",
    "message": "Invalid access token",
    "longMessage": "Invalid access token. Check the value of the Authorization HTTP request header."
  }]
}
http_status=401
exit_status=0

Feed Beta production, no Authorization header:
{
  "errors": [{
    "errorId": 1002,
    "domain": "OAuth",
    "category": "REQUEST",
    "message": "Missing access token",
    "longMessage": "Access token is missing in the Authorization HTTP request header."
  }]
}
http_status=400
exit_status=0

Browse sandbox, deliberately invalid bearer:
{
  "errors": [{
    "errorId": 1001,
    "domain": "OAuth",
    "category": "REQUEST",
    "message": "Invalid access token",
    "longMessage": "Invalid access token. Check the value of the Authorization HTTP request header."
  }]
}
http_status=401
exit_status=0
```

These observations establish endpoint reachability and authentication enforcement only. They do not establish successful access, response fields in practice, marketplace coverage, completeness, latency, or production reliability.

### Official-interface observations

| Dimension | Observation and evidence | Assessment |
|---|---|---|
| Current accessibility | Browse documentation and endpoints are live. All Browse methods require an OAuth application access token. eBay says production Buy API use is intended for approved partners; approval depends on the business model, EPN/application review, and signed contracts, with no guarantee of approval. Feed Beta is Limited Release and available only to selected developers approved by eBay business units. Marketplace Insights is restricted and not open to new users. | `CONFIRMED`: public documentation and authentication gates are reachable. `UNKNOWN`: ProductQuant production approval. |
| Authentication | Browse uses an application token from the OAuth client-credentials grant. Feed Beta additionally requires the `buy.item.feed` scope, marketplace header, and byte `Range` header for file retrieval. Sandbox still requires a developer keyset/token; supported sandbox data are limited or mocked. | `CONFIRMED` by official OAuth/API documentation and negative probes. |
| Cost | The developer sign-in page advertises an always-free account tier with 5,000 calls/day and sandbox access. Higher limits/support have a premium tier, while Buy production access can require business-model-specific agreements. No authoritative public price for the exact ProductQuant production/feed arrangement was found. | `CONFIRMED`: a free developer tier exists. `UNKNOWN`: production commercial terms and any contractual cost for this use case. |
| Rate limits | The published defaults are 5,000 Browse calls/day; 10,000 Feed Beta calls/day across the item, item-group, and item-priority resources; and 75,000 item-snapshot calls/day. Higher limits require review. | `CONFIRMED` as published defaults, not measured effective quotas. |
| Available fields | Browse search/item schemas expose representative fields including item/listing identifiers, title, category, localized aspects, brand, condition, images, price/current bid, bid count, buying options, seller and feedback, location, shipping and delivery estimates, return terms, availability/estimated quantity, product-review information where available, and creation/origin/end timestamps. Feed files expose a large but filtered TSV representation including identifiers, title/category/aspects, price, availability, seller trust, images, shipping/returns, item creation/end times, and snapshot timestamps. | `CONFIRMED` in the published schemas. Actual population, missingness, and category coverage remain `UNKNOWN` without authenticated samples. No general sold-count or historical sales-outcome field is documented in Browse. |
| Historical depth | Browse is a current listing/search interface and documents no `as_of` request or version-history resource. Feed Beta offers the latest weekly active bootstrap, daily newly-listed files retained for 14 days with 48-72 hour generation latency, and hourly changed-item snapshots retained for 7 days with about two hours of generation latency. Seller Product Research advertises up to three years of sold/pricing history in eBay's seller UI, but no supported developer API or raw bulk export for that research dataset was identified. | `CONFIRMED`: only short feed lookback plus a latest bootstrap is programmatically documented. `INFERRED`: the seller UI is not a safe automation contract. |
| Timestamp semantics | Browse `itemCreationDate` is when the listing record was created; `itemOriginDate` is when it was first available and survives relisting; `itemEndDate` is the current scheduled/actual end timestamp. Browse has no response-level historical observation timestamp, so a collector would need its own receipt time. Feed weekly bootstrap represents items in the category on Sunday and returns generation/as-of information in `Last-Modified`; daily files represent a listing day but arrive later; `itemSnapshotDate` is when a change was picked up for the hourly snapshot. Feed timestamps are documented as UTC/GMT where specified. | `CONFIRMED` semantics. `UNKNOWN`: clock/revision guarantees and whether every marketplace mutation is captured in practice. |
| Universe and reconstruction | Browse results are query-, filter-, marketplace-, ranking-, and request-context-dependent current results. Feed daily/weekly files are fixed-price only; daily and weekly files are further filtered to Top Rated/Above Standard sellers and exclude condition `7000`; Real Estate is excluded. Hourly snapshots describe changed active fixed-price items. The official status log records a resolved June 2026 incident involving missing categories in the hourly feed. | `CONFIRMED`: the feed is not the unrestricted eBay listing universe. `INFERRED`: even prospective capture would form a provider-filtered panel, not a complete marketplace universe. |
| Historical-state reconstruction | Neither Browse nor the currently accessible Feed Beta retention window can reconstruct listing prices, availability, search rank, or universe membership before capture began. The short feed windows can fill only recent gaps around a current bootstrap. Finding and Shopping APIs were decommissioned on 2025-02-04 in favour of Browse. The one documented sold-history API, Marketplace Insights, is closed to new users. | `CONFIRMED` for documented interfaces. eBay cannot serve as ProductQuant's historical bootstrap under current access. |
| Point-in-time safety | A raw Browse response can evidence what one query returned at collector receipt time. After approval, a continuously captured weekly/daily/hourly feed with recorded headers and receipt times could support forward point-in-time observations for the filtered fixed-price universe. Neither path establishes past provider state before capture, and no accessible sold-outcome stream was found for label construction. | `INFERRED`: potentially point-in-time-safe for prospective observations only, contingent on coverage validation and permitted retention. Not sufficient for an integrated historical backtest. |
| Operational reliability | Production and sandbox hosts completed TLS/HTTP requests during the probe. eBay publishes an API status page and default quotas. Feed Beta is Limited Release/beta and its schemas/filters may change; the status page shows a recent resolved missing-category feed incident. No authenticated sustained test, SLA, uptime commitment, completeness audit, or retry behaviour was available. | `CONFIRMED`: endpoints responded and status reporting exists. `UNKNOWN`: reliability adequate for ProductQuant. |
| ToS/licensing constraints | The current API License Agreement limits the program to promoting/facilitating eBay Services; requires express written permission for specified site/category statistics and average selling-price or GMV derivations; prohibits using eBay Content to suggest/model eBay prices; prohibits algorithm/ML/AI training on eBay Content; and prohibits copying/storing/modifying content outside allowed purposes. Feed guidance permits storing items to operate an approved eBay integration, but that does not establish permission for independent long-term research archival. | `INFERRED` with high confidence: ProductQuant's raw archival, category/pricing research, ranking, and model-development purposes are materially incompatible or at least unresolved without explicit written eBay permission and the use-case-specific production contract. This is not legal advice. |
| Raw-response preservation | TSV/GZIP feeds and JSON Browse responses are technically downloadable; feed documentation even describes storing item state and its as-of date for synchronization. However, long-term retention of complete raw responses for ProductQuant research is not clearly authorized by the public agreement, displayed listing data must be refreshed promptly, and personal data have additional deletion duties. | `CONFIRMED`: technical preservation is possible. `UNKNOWN/BLOCKED`: permitted retention scope, duration, deletion requirements, and derived-data rights for ProductQuant. |
| v0.1 suitability | Browse is the strongest technical candidate among the investigated marketplaces for current discovery; Feed Beta is the stronger prospective state-capture mechanism. Production access, permitted analytical use, and long-term raw retention are unresolved, and neither is a historical bootstrap. | `CONDITIONAL/BLOCKED`: do not adopt eBay as the v0.1 marketplace source yet. After written approval and authenticated validation, consider it only for forward collection. |

## Interpretation

- **CONFIRMED:** eBay offers a current Browse API and a limited-release Feed Beta API with useful listing fields, explicit timestamps, published default quotas, and OAuth-gated production/sandbox endpoints.
- **CONFIRMED:** Browse does not expose historical listing versions. Feed Beta exposes a latest filtered bootstrap plus only 14 days of newly-listed files and 7 days of hourly change files; it therefore cannot recreate arbitrary earlier marketplace states.
- **CONFIRMED:** the programmatically documented feed universe is filtered and fixed-price-focused, Marketplace Insights is not open to new users, and the Finding/Shopping fallback APIs are decommissioned.
- **INFERRED:** with eBay approval, written retention/analysis permission, and continuous capture, the feed could support a forward-only, point-in-time panel for its filtered universe. This would still need coverage, omission, revision, latency, and outage tests.
- **INFERRED:** the current public licence presents material conflicts with ProductQuant's intended archival and quantitative-research/model use. This interpretation is not legal advice and must be resolved through eBay and qualified human/legal review, not by implementation convenience.
- **UNKNOWN:** whether eBay will approve ProductQuant's exact business model; the final agreement, cost, retention/deletion rights, derived-data rights, authenticated field population, completeness, effective quotas, and service reliability.
- **v0.1 recommendation:** `CONDITIONAL/BLOCKED`. Do not use eBay as the historical bootstrap or claim it as an operational v0.1 source. Reconsider it only as a prospective marketplace collector after written use-case permission, production credentials, and an authenticated validation sample.

## Limitations and residual uncertainty

- No developer account, application keyset, OAuth token, EPN membership, production approval, or private contract was available or used; successful payloads and actual missingness were not observed.
- Negative authentication responses prove enforcement and endpoint reachability, not entitlement, data quality, coverage, or uptime.
- Documentation is mutable. Recheck the schemas, limits, status page, production process, and licence before any integration, and treat this record as stale after 30 days or any announced API/terms change.
- No sustained rate-limit, pagination, search-result stability, cross-marketplace consistency, feed-completeness, or revision test was run.
- Product Research was assessed only as a documented seller-facing UI. Browser automation, scraping, and undocumented endpoints were deliberately excluded.
- No legal opinion was obtained. Exact retention and analytical-use permission remain a human-owned blocker.

## Integrity and provenance

- **Artifact location:** `EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md`; official live URLs listed under Method; probe output recorded inline.
- **Artifact digest:** `NOT AVAILABLE` for the self-referential Markdown record; Git object identity after the parent Phase 0 commit will provide repository integrity. No raw response artifact was retained outside this concise record.
- **External retention risk:** `HIGH` — official pages, API schemas, status entries, access policy, and licence terms may change or disappear. Reproduction should record a new evidence item rather than overwrite this observation.
- **Supersedes / superseded by:** `NONE`

## Corrections

Preserve the original observation. Append attributable corrections rather than silently changing it.

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `NONE` | `NONE` | `NONE` | `NONE` |
