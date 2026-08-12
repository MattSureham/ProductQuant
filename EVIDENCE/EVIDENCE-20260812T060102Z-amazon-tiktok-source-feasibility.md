# Amazon and TikTok Source Feasibility

## Metadata

- **ID:** `EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility`
- **Title:** `Amazon and TikTok Shop interfaces do not support the v0.1 point-in-time source role`
- **Captured UTC:** `2026-08-12T06:03:48Z–2026-08-12T06:10:26Z`
- **Recorded by:** `agent:codex-phase0-amazon-tiktok`
- **Claim supported or challenged:** Amazon Creators API, Amazon Selling Partner API (SP-API), TikTok Shop Product APIs, and TikTok Shop Bestsellers Analytics are currently documented and their public gateways are reachable, but none provides a credential-free, marketplace-wide, raw-preservable historical source suitable for ProductQuant v0.1 point-in-time backtesting.
- **Related requirements:** [`PROJECT_SPEC.md` sections 8–18, 21, 40–42, 51, and 53](../PROJECT_SPEC.md)
- **Related ADRs/issues:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](../ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md); ADRs `NONE`
- **Repository revision/state:** `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1` on `main`; the pre-existing working tree had modified `HANDOFF.md` and untracked `ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md`; this evidence file was not yet present when the probes ran.
- **Environment:** Darwin `25.3.0` arm64; `curl 8.7.1` (x86_64-apple-darwin25.0, SecureTransport); public network; no Amazon or TikTok credentials supplied; no account created, agreement accepted, or paid service used.

## Method

- **Procedure:** Review current official product, authentication, quota, versioning, and terms pages; then issue one deliberately unauthenticated request to each public production gateway. Capture only safe HTTP status, headers, short error bodies, and response digests. No authenticated operation was attempted.
- **Exact command/input:**

  Amazon Creators API:

  ```sh
  curl --max-time 30 -sS \
    -o /tmp/productquant-amz-tts.r80tFw/amazon-body.json \
    -D /tmp/productquant-amz-tts.r80tFw/amazon-headers.txt \
    -w 'amazon_http=%{http_code} content_type=%{content_type} bytes=%{size_download}\n' \
    -X POST 'https://creatorsapi.amazon/catalog/v1/getItems' \
    -H 'Content-Type: application/json' \
    -H 'x-marketplace: www.amazon.com' \
    --data '{"itemIds":["B09B2SBHQK"],"itemIdType":"ASIN","marketplace":"www.amazon.com","partnerTag":"example-20","resources":["itemInfo.title","offersV2.listings.price"]}'
  ```

  Amazon SP-API Catalog Items:

  ```sh
  curl --max-time 30 -sS \
    -o /tmp/productquant-amz-tts.r80tFw/spapi-body.json \
    -D /tmp/productquant-amz-tts.r80tFw/spapi-headers.txt \
    -w 'spapi_http=%{http_code} content_type=%{content_type} bytes=%{size_download}\n' \
    'https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items/B09B2SBHQK?marketplaceIds=ATVPDKIKX0DER&includedData=attributes,identifiers,images,productTypes,salesRanks,summaries'
  ```

  TikTok Shop Bestsellers Analytics:

  ```sh
  curl --max-time 30 -sS \
    -o /tmp/productquant-amz-tts.r80tFw/tiktok-body.json \
    -D /tmp/productquant-amz-tts.r80tFw/tiktok-headers.txt \
    -w 'tiktok_http=%{http_code} content_type=%{content_type} bytes=%{size_download}\n' \
    'https://open-api.tiktokglobalshop.com/analytics/202511/products/bestselling?start_date=2026-08-01&end_date=2026-08-07&currency=USD'
  ```

  Corrected TikTok Shop request using the endpoint's documented `date` and `time_slot` parameters:

  ```sh
  curl --max-time 30 -sS \
    -o /tmp/productquant-amz-tts.r80tFw/tiktok-corrected-body.json \
    -D /tmp/productquant-amz-tts.r80tFw/tiktok-corrected-headers.txt \
    -w 'tiktok_corrected_http=%{http_code} content_type=%{content_type} bytes=%{size_download}\n' \
    'https://open-api.tiktokglobalshop.com/analytics/202511/products/bestselling?date=2026-08-07&time_slot=7D&currency=USD'
  ```

  Digest calculation:

  ```sh
  shasum -a 256 \
    /tmp/productquant-amz-tts.r80tFw/amazon-body.json \
    /tmp/productquant-amz-tts.r80tFw/spapi-body.json \
    /tmp/productquant-amz-tts.r80tFw/tiktok-body.json \
    /tmp/productquant-amz-tts.r80tFw/tiktok-corrected-body.json
  ```

- **Exit status:** Each `curl` process exited `0`; HTTP results were Creators API `401`, SP-API `403`, and TikTok Shop `400`. `shasum` exited `0`. Because `curl -f` was not used, an HTTP 4xx response correctly remained a successful transport-level command.
- **Repeatability:** Re-run the commands without adding credentials. Request IDs and CDN headers will vary. Re-read every linked official document because provider documentation and terms are mutable. An authenticated participant may verify response schemas only after human authorization and must not commit credentials or provider content whose retention is restricted.

### Official sources reviewed

Amazon:

- [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)
- [Creators API registration](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/onboarding/register-for-creators-api)
- [Creators API common headers and parameters](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/concepts/common-request-headers-and-parameters)
- [Creators API operations and resources](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference)
- [SearchItems operation](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/search-items)
- [Creators API rates](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/concepts/api-rates)
- [Creators API best programming practices](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/concepts/best-programming-practices)
- [PA-API 5 deprecation notice](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation)
- [Associates Program IP License and Usage Requirements](https://affiliate-program.amazon.com/help/operating/policies/#Associates%20Program%20IP%20License)
- [SP-API registration overview](https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/sp-api-registration-overview)
- [SP-API application authorization](https://developer-docs.amazon.com/sp-api/lang-en_US/docs/authorizing-selling-partner-api-applications)
- [Catalog Items API](https://developer-docs.amazon.com/sp-api/lang-en_US/docs/catalog-items-api-v2022-04-01-use-case-guide)
- [Catalog Items API rate limits](https://developer-docs.amazon.com/sp-api/lang-US/docs/catalog-items-api-rate-limits)

TikTok Shop:

- [Methods and endpoints](https://partner.tiktokshop.com/docv2/page/methods-and-endpoints)
- [Access scopes](https://partner.tiktokshop.com/docv2/page/access-scope)
- [API entity tags](https://partner.tiktokshop.com/docv2/page/api-entity-tags)
- [Products API overview](https://partner.tiktokshop.com/docv2/page/products-api-overview)
- [Get Product API](https://partner.tiktokshop.com/docv2/page/get-product-202309)
- [Search Products API](https://partner.tiktokshop.com/docv2/page/search-products-202502)
- [Bestsellers Analytics Open API launch](https://partner.tiktokshop.com/docv2/page/3dk9557y)
- [Bestsellers response-data update](https://partner.tiktokshop.com/docv2/page/kpkfccsa)
- [Rate limits](https://partner.tiktokshop.com/docv2/page/rate-limits)
- [API versioning](https://partner.tiktokshop.com/docv2/page/api-versioning)
- [Data security and privacy review](https://partner.tiktokshop.com/docv2/page/data-security-and-privacy-review)
- [TikTok Shop Developer Terms](https://partner.tiktokshop.com/docv2/page/6506bc942f024f02be400315)

## Raw observation

### Gateway responses

The Creators API request at `2026-08-12T06:03:48Z` returned:

```text
amazon_http=401 content_type=application/json bytes=117
{"message":"The authentication token is invalid or malformed","reason":"InvalidToken","type":"UnauthorizedException"}
```

The SP-API request at `2026-08-12T06:06:41Z` returned:

```text
spapi_http=403 content_type=application/json bytes=189
{
  "errors": [
    {
      "code": "Unauthorized",
      "message": "Access to requested resource is denied.",
      "details": "Access token is missing in the request header."
    }
  ]
}
```

The TikTok Shop request at `2026-08-12T06:03:50Z` returned:

```text
tiktok_http=400 content_type=application/json; charset=utf-8 bytes=202
{"code":36009004,"data":null,"message":"Invalid credentials. Invalid 'app_key' query parameter. For more details: https://m.tiktok.shop/s/AIu6dbFhs2XW","request_id":"20260812140352F100F0A36CB8D305CA56"}
```

That first request used `start_date`/`end_date`, which are not the documented Bestsellers parameters. A corrected request using `date=2026-08-07&time_slot=7D` at `2026-08-12T06:10:24Z` reached the same authentication gate:

```text
tiktok_corrected_http=400 content_type=application/json; charset=utf-8 bytes=202
{"code":36009004,"data":null,"message":"Invalid credentials. Invalid 'app_key' query parameter. For more details: https://m.tiktok.shop/s/AIu6dbFhs2XW","request_id":"20260812141026154BC45BF4D020055BAF"}
```

These are authentication-boundary observations, not successful data-access probes.

### Feasibility dimensions

#### Amazon Creators API

| Dimension | Official-document observation |
|---|---|
| Current accessibility | **CONFIRMED:** Creators API is Amazon's supported affiliate product-catalog interface; PA-API 5 is deprecated. The public production endpoint responded, but authenticated catalog access was not available in this environment. |
| Authentication | **CONFIRMED:** OAuth 2.0 client credentials produce a bearer token. Calls also require target marketplace and a marketplace-specific Partner Tag. Registration requires a finally accepted Amazon Associates account, qualified referring sales, and action by the primary account owner. The introduction currently says at least ten qualifying sales in the prior 30 days, while the registration page says qualified sales without that exact count; the exact eligibility rule is therefore **UNKNOWN** until Amazon confirms it for the target account. |
| Cost | **CONFIRMED:** Amazon states that the Associates program is free to join. **UNKNOWN:** no separate per-call Creators API price schedule was found in the reviewed official pages; required qualifying-sales activity and operation of an affiliate site are non-price access conditions. |
| Rate limits | **CONFIRMED:** newly created credentials receive up to `1 TPS` and `8,640 TPD` for the first 30 days. Later allocation depends on shipped revenue; the account loses API access after 30 consecutive days without qualified referring sales. Actual account allocation is observable only after authorization. |
| Available fields | **CONFIRMED:** `SearchItems`, `GetItems`, `GetVariations`, and `GetBrowseNodes` expose current item/catalog data through resources including `ItemInfo`, `Images`, `OffersV2`, `BrowseNodeInfo`, `BrowseNodes`, `ParentASIN`, search refinements, and variation summaries. `SearchItems` returns at most ten items per request, and `GetItems` accepts up to ten ASINs. |
| Historical depth | **CONFIRMED:** the reviewed API reference describes current search, item, offer, variation, and browse-node retrieval. No historical listing-state, prior offer, prior rank, or `as_of` operation is documented. |
| Timestamp semantics | **CONFIRMED:** an API retrieval is a current observation. The IP License requires a display timestamp for pricing/availability refreshed less frequently than hourly, but this is a client display rule, not a provider-issued historical observation timestamp or version identifier. |
| Historical reconstruction | **INFERRED:** prior price, availability, offer, rank, and result-universe states cannot be reconstructed from a later Creators API call. A prospective collector could observe future states, subject to access and terms, but that would not create pre-collector history. |
| Point-in-time safety | **INFERRED:** current responses can be timestamped at retrieval but are not sufficient for historical point-in-time-safe backtesting. Search responses also do not establish a complete marketplace universe. |
| Operational reliability | **CONFIRMED:** access and quota depend on continuing affiliate sales; Amazon may change, deprecate, or republish the interfaces. **INFERRED:** this makes the API an unstable dependency for research whose availability must not depend on affiliate conversion. |
| ToS/licensing | **CONFIRMED:** the US IP License limits Product Advertising Content to driving users and sales to Amazon. Without express prior written approval it prohibits aggregating, analyzing, extracting, or repurposing that content and prohibits model-related use. |
| Raw-response preservation | **CONFIRMED:** images may not be stored, image links may be cached for up to 24 hours, other Product Advertising Content may be cached for up to 24 hours before refresh, and individual ASINs may be retained indefinitely while the license remains active. This does not permit ProductQuant's durable raw-response archive. |
| v0.1 suitability | **NOT SUITABLE:** no historical states, affiliate-dependent access, and explicit analysis/retention restrictions conflict with the research and raw-preservation requirements. Written Amazon approval would still not supply pre-existing history. |

#### Amazon Selling Partner API (SP-API)

| Dimension | Official-document observation |
|---|---|
| Current accessibility | **CONFIRMED:** Catalog Items API `v2022-04-01` is current for sellers and vendors; its public production endpoint responded. It is a selling-partner interface, not anonymous marketplace access. |
| Authentication | **CONFIRMED:** an app must be registered and receive an LWA OAuth authorization from the relevant seller or vendor. Catalog Items operations require an eligible role such as `Product Listing`. A private seller app requires a Professional selling account. |
| Cost | **UNKNOWN:** the reviewed official SP-API pages did not publish a per-call price. A Professional selling account is a prerequisite for private seller applications, but this evidence did not verify the account subscription price or any other indirect cost. |
| Rate limits | **CONFIRMED:** limits can vary by operation, selling-partner account, and application. The response may expose `x-amzn-RateLimit-Limit`, which does not represent every usage-plan limit. No single marketplace-wide quota is published. |
| Available fields | **CONFIRMED:** Catalog Items can return attributes, classifications, dimensions, identifiers, images, product types, relationships, sales ranks, summaries, and vendor-only details. Seller listing interfaces can expose the authorized seller's current offers and fulfillment availability. |
| Historical depth | **CONFIRMED:** the reviewed Catalog Items and Listings documentation exposes current catalog/listing state and seller workflows; no general historical catalog-state or marketplace-wide historical listing endpoint is documented. |
| Timestamp semantics | **INFERRED:** returned catalog/listing state is current at retrieval unless an individual operation explicitly documents another business timestamp. The reviewed catalog interface has no general `as_of` selector or immutable observation version. |
| Historical reconstruction | **INFERRED:** later calls cannot reconstruct a former marketplace universe, catalog attributes, rank, offers, or availability. Seller-authorized data also cannot represent sellers that did not authorize the app. |
| Point-in-time safety | **INFERRED:** prospective snapshots for an authorized seller may be timestamped locally, but SP-API cannot bootstrap the required marketplace-wide historical backtest. |
| Operational reliability | **CONFIRMED:** authorization can be seller/vendor scoped and quotas are dynamic. Interface versions and roles are provider-controlled. Availability for any research loop therefore depends on continuing seller authorization. |
| ToS/licensing | **UNKNOWN:** a full legal review of all applicable SP-API agreements and data-protection policies was not performed. The documented product purpose is providing services to authorized selling partners, not constructing an independent marketplace research corpus. Written permission would be required before treating it as otherwise. |
| Raw-response preservation | **UNKNOWN:** this investigation found no basis to claim that long-term raw SP-API responses may be retained for ProductQuant's independent marketplace research. No raw payload was obtained. |
| v0.1 suitability | **NOT SUITABLE:** it is seller/vendor authorized, not marketplace-wide, and provides no historical marketplace states. This conclusion does not depend on resolving the remaining retention question. |

#### TikTok Shop Product APIs

| Dimension | Official-document observation |
|---|---|
| Current accessibility | **CONFIRMED:** the current production gateway is `https://open-api.tiktokglobalshop.com`. Product APIs manage and retrieve products belonging to an authorized TikTok Shop seller; they are not an anonymous marketplace catalog. |
| Authentication | **CONFIRMED:** Get Product requires `app_key`, request signature, UTC request `timestamp`, `shop_cipher`, seller OAuth token in `x-tts-access-token`, and `seller.product.basic` scope. Even APIs under a “Public” scope still require seller authorization for shop data. |
| Cost | **UNKNOWN:** no fixed API price schedule was found in the reviewed official pages. Account, shop, approval, and compliance costs were not established. |
| Rate limits | **CONFIRMED:** TikTok uses dynamic QPS allocation based on app-by-authorized-shop scope and endpoint characteristics and does not expose one fixed quota. A May 2026 notice documents a separate sandbox threshold of 100 queries/hour; the production Product API's actual allocation remains **UNKNOWN** until authorized operation. |
| Available fields | **CONFIRMED:** current product details include identifiers/status, title, description, brand/category/attributes, images, SKUs, price, and inventory. Search Products can filter by creation/update Unix timestamps and status. Get Product can select a currently live, under-review, or draft version where applicable. |
| Historical depth | **CONFIRMED:** creation/update filters select current product records; they do not request a state as it existed at that time. The overview states that deleting a product removes historical purchases, finance, and related back-end data. No listing-version history endpoint is documented. |
| Timestamp semantics | **CONFIRMED:** request `timestamp` is the signed request's UTC time, not the product state's observation time. Product creation/update timestamps are entity lifecycle timestamps, not immutable versions of title, price, inventory, visibility, or rank. |
| Historical reconstruction | **INFERRED:** the live/under-review/draft selectors can expose limited simultaneous versions during an edit workflow, but cannot reconstruct arbitrary past product, price, inventory, visibility, or universe states. |
| Point-in-time safety | **INFERRED:** only forward snapshots of an authorized shop could be locally observation-timestamped. The interface cannot bootstrap a marketplace-wide historical panel or outcomes for non-authorizing shops. |
| Operational reliability | **CONFIRMED:** quotas are dynamic, inactive sellers can lose API access, new versions may be released monthly, and an older version is guaranteed for only a minimum two-month overlap after a replacement. |
| ToS/licensing | **CONFIRMED:** developer terms limit access to End User-authorized data and delivery of services to that End User; they prohibit aggregating or using End User data for the developer's own purposes. Data-security review and minimization/deletion obligations apply to partner apps. |
| Raw-response preservation | **INFERRED:** long-term raw shop-data retention for an independent ProductQuant research corpus is not supported by the reviewed terms. Retention must be limited to the authorized service purpose, and data must be deleted when no longer necessary or after authorization ends where applicable. Exact retention for every non-personal product field is **UNKNOWN** pending written TikTok confirmation. |
| v0.1 suitability | **NOT SUITABLE:** authorized-shop scope, missing historical versions, dynamic access, and terms restrictions prevent its use as ProductQuant's v0.1 marketplace/backtest source. |

#### TikTok Shop Bestsellers Analytics

| Dimension | Official-document observation |
|---|---|
| Current accessibility | **CONFIRMED:** TikTok launched four version `202511` Bestsellers APIs in April 2026 for products, creators, videos, and LIVE sessions. “Public” availability means ISVs/sellers may request the scope; it does not remove app and seller authorization. |
| Authentication | **CONFIRMED:** calls require seller OAuth in `x-tts-access-token`, app key, signature, request timestamp, `shop_cipher`, and the Bestsellers scope (`data.bestselling.public.read` in the endpoint reference). Results are limited to the authorized seller's registered market. |
| Cost | **UNKNOWN:** no fixed API price schedule was found in the reviewed official pages. |
| Rate limits | **CONFIRMED:** standard TikTok dynamic rate limits apply; the Bestsellers-specific production allocation is **UNKNOWN** without an authorized app/shop pair. |
| Available fields | **CONFIRMED:** each API returns at most the top 100 entities by GMV for the selected market/window. The product interface includes product name, rating, GMV range, and images after the May 2026 enrichment. Exact GMV is unavailable because ranges receive a random privacy offset. |
| Historical depth | **CONFIRMED:** supported windows are `1D`, `7D`, and `30D`, anchored to an inclusive date in the shop's registered timezone, with at least daily granularity. **UNKNOWN:** the oldest permissible anchor date and actual coverage for a newly authorized account were not established without an authenticated request. |
| Timestamp semantics | **CONFIRMED:** the query date is a shop-timezone business date and results are retrospective window aggregates; the request timestamp is UTC authentication metadata. A May 2026 update describes analytics availability as T-1. No revision/version timestamp for previously returned rankings is documented. |
| Historical reconstruction | **INFERRED:** the API may return a retrospective top-100 ranking for an accepted date, but it cannot reconstruct the full candidate universe, exact GMV, listing state, or what the provider would have returned at an earlier observation time. |
| Point-in-time safety | **INFERRED:** a top-100 retrospective aggregate with randomized values and unknown revision semantics is not a point-in-time-safe marketplace panel. It could be a separately labelled discovery signal only after authorized reproducibility and terms checks. |
| Operational reliability | **CONFIRMED:** the interface is recent, authorization and quotas are dynamic, results are deliberately limited/obfuscated, and TikTok versions are provider-controlled. No SLA was found. |
| ToS/licensing | **INFERRED:** using seller-authorized Bestsellers data to build ProductQuant's independent corpus appears outside the reviewed End User service-purpose and own-use restrictions. This is a high-confidence feasibility interpretation, not legal advice; written TikTok confirmation would be required. |
| Raw-response preservation | **UNKNOWN:** no official grant allowing permanent raw Bestsellers response archival for independent research was found. No successful response was obtained. |
| v0.1 suitability | **NOT SUITABLE:** despite useful demand/sales-ranking semantics, its authorized-market top-100 coverage, randomized GMV, unresolved lookback/revision behavior, and retention-purpose restrictions fail v0.1 requirements. |

## Interpretation

- **CONFIRMED:** All three tested public gateways were reachable and enforced documented authentication before returning product data. Creators API is affiliate-oriented; SP-API and TikTok Product APIs are seller/vendor/shop-authorized; TikTok Bestsellers is an authorized-market top-100 analytics interface rather than a full marketplace feed.
- **CONFIRMED:** Creators API's current US terms allow only short-lived Product Advertising Content caching and require express prior written approval for aggregation, analysis, extraction, or repurposing. The raw-response preservation ProductQuant requires is therefore not available under the standard terms reviewed here.
- **CONFIRMED:** None of the reviewed interfaces documents arbitrary historical versions of the complete listing universe, offers, price, availability, and rank with an `as_of` observation boundary.
- **INFERRED:** Amazon Creators API, Amazon SP-API, TikTok Shop Product APIs, and TikTok Shop Bestsellers Analytics are **NOT SUITABLE for v0.1**. They cannot support the initial point-in-time-safe historical marketplace backtest, even before authenticated-access work is considered.
- **INFERRED:** An authenticated TikTok Bestsellers probe could still be useful as an optional future discovery-signal experiment, and authorized seller APIs could support future forward snapshots, but neither role should be represented as historical marketplace reconstruction.
- **UNKNOWN:** Actual authenticated response completeness, target-account quotas, the oldest TikTok Bestsellers date, provider revision behavior, and any negotiated permissions that differ from standard terms. Resolving these requires human-authorized accounts, provider responses, and written retention/use confirmation.

The terms conclusions above are technical feasibility interpretations, not legal advice.

## Limitations and residual uncertainty

- The probes intentionally stopped at each authentication boundary; they do not validate successful schemas, latency, pagination, production quotas, coverage, or data quality.
- Public documentation can change without repository notice. Refresh this evidence before relying on it after 30 days, after a provider changelog/terms update, or before any authenticated integration.
- The Amazon Associates pages contain an eligibility-detail inconsistency: the introduction states ten qualifying sales in 30 days, while the registration page states qualified sales without that number.
- A complete SP-API contract and data-protection legal review was not performed because seller-authorized scope and absent historical states already disqualify it for this milestone.
- TikTok's exact non-personal product-data retention rule and the Bestsellers maximum lookback are unresolved. Absence of a documented permission is not proof that TikTok would refuse a negotiated permission.
- No SLA, authenticated error-rate sample, longitudinal revision comparison, or multi-market comparison was available.
- The transient `/tmp` response files are not project artifacts and may disappear; concise raw bodies and digests are preserved inline above and below.

## Integrity and provenance

- **Artifact location:** `INLINE`; official sources are linked above. Transient probe files were under `/tmp/productquant-amz-tts.r80tFw/` and are intentionally not tracked.
- **Artifact digest:** SHA-256: Creators error body `f3bcca797ad9f3d9de6705ab97ba0f3f127d28ea144d213e3683f585d08216b3`; SP-API error body `a13ce270ac532786e7371c4d9de565d51ee6a664deab609f89937ab549758621`; initial TikTok error body `c962c745e25c9746e78869efa65d991e529868420058b8431b7364d3e0679c98`; corrected TikTok error body `766971064c90e7264a9c4fa51feb3980cbeb44180d34ca2dd0d3924e3b76fc47`.
- **External retention risk:** `HIGH` — provider documentation and terms are mutable, and transient probe responses have no durable external storage. The safe excerpts in this record are the durable evidence.
- **Supersedes / superseded by:** `NONE`

## Corrections

Preserve the original observation. Append attributable corrections rather than silently changing it.

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `2026-08-12T06:10:26Z` | `agent:codex-phase0-amazon-tiktok` | The initial TikTok request used `start_date`/`end_date`, which are not the documented Bestsellers parameters. A second request used `date`/`time_slot` and returned the same missing-`app_key` authentication error. | [Get Bestselling Products](https://partner.tiktokshop.com/docv2/page/get-bestselling-products-202511); corrected raw observation and digest above. |
