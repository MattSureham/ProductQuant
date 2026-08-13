# Restricted Phase 1 Data-Foundation Verification

## Metadata

- **ID:** `EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`
- **Title:** `Restricted Phase 1 UCI data-foundation verification`
- **Captured UTC:** `2026-08-12T09:13:34Z`
- **Recorded by:** `agent:codex-phase1`
- **Claim supported or challenged:** The clean implementation revision reproducibly acquires, preserves, normalizes, and verifies the pinned UCI Online Retail II transaction-event substrate while failing closed, retaining source-row provenance, enforcing the accepted stitch, and denying every unsupported marketplace/demand capability.
- **Related requirements:** [`PROJECT_SPEC.md` Restricted Phase 1](../PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation)
- **Related ADRs/issues:** [`ADR-20260812T072420Z-uci-transaction-data-foundation`](../ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md); [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](../ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md)
- **Repository revision/state:** `c599a5e245b923764df672aecf6973abdc29e638` on `main`, clean during both official normalized builds and all final verification commands in this record; no push performed.
- **Environment:** macOS 26.3 build 25D125, arm64; Python 3.12.13; uv 0.11.8; DuckDB 1.5.5; openpyxl 3.1.5; PyArrow 25.0.1; pytest 9.1.1.

## Method

### Clean official build

- **Procedure:** Acquire the pinned public UCI ZIP, verify both archive and sole-member size/digest, publish the exact raw response and manifest, stream both workbook sheets into the fixed Parquet schema, apply only the accepted physical-sheet boundary, query aggregates through in-memory DuckDB, publish normalized state, and write a row-free receipt.
- **Exact command/input:**

```bash
NO_PROXY='*' no_proxy='*' \
  uv run --frozen productquant uci prepare --data-root ./data
```

The explicit bypass was used only after macOS system proxy discovery was confirmed to route `urllib` through the configured localhost proxy. The source/final URL remained the fixed official UCI URL.

- **Exit status:** `0`
- **Repeatability:** From revision `c599a5e`, run `uv sync --frozen`, then the command above. A provider byte change is expected to fail rather than update the pin.

### Synthetic, failure, integration, and full-data gates

- **Exact commands/input:**

```bash
uv sync --frozen
uv lock --check
uv run --frozen python -m compileall -q src tests conftest.py
uv run --frozen pytest -q
uv run --frozen pytest -m full_data --data-root ./data -q
uv build
uv run --frozen productquant --help
uv run --frozen productquant uci --help
uv run --frozen productquant uci fetch --help
uv run --frozen productquant uci normalize --help
uv run --frozen productquant uci verify --help
uv run --frozen productquant uci prepare --help
uv run --frozen productquant uci prepare --data-root ./data --offline
uv run --frozen productquant uci verify --data-root ./data
git diff --check
```

- **Exit status:** Every final command exited `0`.
- **Repeatability:** The default pytest collection intentionally deselects, rather than skips, the one official-data test. The explicit `-m full_data` invocation is a separate mandatory gate and fails if the canonical local bundles are absent.

### Isolated deterministic rebuild

- **Procedure:** Create a private temporary data root, copy only the already verified raw bundle, run `prepare --offline` from the same clean revision and lock, then compare the two Parquet artifacts and normalized manifests. The comparison streamed `event_id` in Parquet order into SHA-256 without printing a row or identifier.
- **Exact command/input:**

```bash
repro_root=$(mktemp -d /tmp/productquant-rebuild.XXXXXX)
mkdir -p "$repro_root/raw/uci-online-retail-ii"
chmod 700 "$repro_root" "$repro_root/raw" \
  "$repro_root/raw/uci-online-retail-ii"
cp -Rp \
  data/raw/uci-online-retail-ii/572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb \
  "$repro_root/raw/uci-online-retail-ii/"
uv run --frozen productquant uci prepare \
  --data-root "$repro_root" --offline
```

The comparison required equality of Parquet SHA-256, Arrow schema, streamed event-ID order hash, aggregate profile, and the entire normalized manifest after removing only `build.built_at_utc`.

- **Exit status:** `0`; all comparison assertions passed.
- **Repeatability:** Repeat on the same platform, implementation revision, lock, and verified raw bundle. Cross-platform byte identity is deliberately not claimed.

### Repository and privacy-integrity gates

- **Procedure:** Resolve every tracked relative Markdown link; parse every machine-readable JSON contract; inspect exact bundle contents and POSIX modes; validate every local receipt's keys/run ID/status/mode; scan for partial publications and persistent DuckDB files; scan tracked paths for raw/normalized data extensions, files over 1 MB, and credential/private-key patterns; inspect wheel contents.
- **Exit status:** `0`
- **Repeatability:** Run the repository checks described in [`README.md`](../README.md); the exact tracked-file and local-artifact checks are summarized below and contain no row-level data.

## Raw observation

### Package and tests

```text
revision=c599a5e245b923764df672aecf6973abdc29e638
uv=uv 0.11.8 (0e961dd9a 2026-04-27 aarch64-apple-darwin)
runtime 3.12.13 1.5.5 3.1.5 25.0.1 9.1.1
100 passed, 1 deselected in 1.02s
1 passed, 100 deselected in 0.20s
Successfully built dist/productquant-0.1.0.dev0.tar.gz
Successfully built dist/productquant-0.1.0.dev0-py3-none-any.whl
cli_help=ok
relative_links=ok
tracked_data=0 large_tracked_files=0 secret_pattern_hits=0
```

The wheel contains the console entry point, implementation modules, and all four JSON contracts.

### Official raw and normalized artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| UCI provider ZIP | 45,622,418 | `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` |
| Sole workbook member | 45,622,278 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Raw manifest | 1,618 | `7137efb4ce98bc295e7c37927d33f45f9901c521f72e1c4fbc764124216d4dd3` |
| `events.parquet` | 11,936,741 | `49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f` |
| Normalized manifest | 2,760 | `2305cef31c6ddeacef140c9fee1bee91c715a29c76c62432ffbe6524aa3ff800` |
| `uv.lock` | repository file | `10acdaade93f8f17a84637fcd5414c50f53f0c99b08c2fab2aa337dfb0137569` |
| Wheel | repository-ignored build output | `9b3f3c04fcea0a6db0d032b1d25f3389f926a8547f8f911c2432e05bc1550820` |
| Source distribution | repository-ignored build output | `cdf0e7169a6fc1465dad6dda921dbdc569f598a3823d73b547e3e7f36c1c3cfa` |

The allowlisted raw HTTP observation was status `200`, content type `application/zip`, content length `45622418`, ETag `"305a3235a8d556277eca6897401f6750-6"`, Last-Modified `Tue, 26 Aug 2025 12:47:08 GMT`, and retrieval UTC `2026-08-12T09:07:22.080827Z`. The final URL equalled the pinned official URL.

The normalized manifest records Python 3.12.13, exact runtime dependencies, `git_revision=c599a5e245b923764df672aecf6973abdc29e638`, and `git_dirty=false`.

### Full-data acceptance profile

```text
retained rows / unique event IDs: 1,044,848 / 1,044,848
first sheet input / retained: 525,461 / 502,938
second sheet input / retained: 541,910 / 541,910
boundary-excluded cross-sheet rows: 22,523
event range: 2009-12-01T07:45:00.000000 through 2011-12-09T12:50:00.000000
unique observed stock codes / invoices: 5,305 / 53,628
cancellation / negative-quantity rows: 19,165 / 22,557
zero-price / negative-price rows: 6,024 / 5
missing-description / missing-customer rows: 4,275 / 235,287
numeric descriptions: 4
quantity range: -80,995 through 80,995
unit-price range: -53,594.360 through 38,970.000 GBP
first-sheet boundary violations: 0
second-sheet boundary violations: 0
```

The raw and normalized manifests both contain the exact eight capability declarations. Only transaction-event history is `supported`; marketplace listing state, marketplace supply/competition, independent external demand, a complete product/opportunity universe, and the integrated v0.1 demonstration are `unsupported`; provider revision state and timezone are `unknown`.

### Determinism and state integrity

```json
{"event_id_order_equal":true,"event_id_order_sha256":"d21c7efed4128ecf067d0a1e6ee8b728f9fff2d46841c85871b9b03b55a9d595","git_dirty":false,"git_revision":"c599a5e245b923764df672aecf6973abdc29e638","manifest_invariants_equal":true,"parquet_bytes_equal":true,"parquet_sha256":"49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f","profile_equal":true,"schema_equal":true}
```

```json
{"artifact_modes":"private","bundle_contents":"exact","duckdb_files":0,"partial_artifacts":0,"raw_content_length":"45622418","raw_http_status":200,"receipt_count":7,"receipt_status_counts":{"failure":1,"success":6}}
```

The final offline `prepare` and `verify` invocations both reported `status=verified`; neither rewrote a valid artifact.

### Preserved negative findings and corrections

1. With the configured localhost HTTP proxy, the first provider response ended cleanly at 6,377,267 bytes. The command returned integrity exit `4`, published no raw bundle, removed its stage, and wrote a failure receipt containing only the observed byte count/digest and sanitized metadata.
2. A credential-free real range probe against the same official URL returned HTTP `206`, `Content-Range: bytes 6377267-6377366/45622418`, and exactly 100 bytes. The implementation therefore added bounded, exact sequential range recovery for clean early EOF. Synthetic tests cover complete recovery, wrong status/range metadata, empty range bodies, mid-stream read failures, request bounds, and non-publication of partial state. A later proxy-backed run passed the original truncation point before being operator-cancelled due throughput; it published no final artifact.
3. Clearing proxy environment variables alone did not bypass macOS system proxy discovery. Explicit `NO_PROXY=*` produced a direct connection to UCI CloudFront and the successful official status-200 acquisition recorded above.
4. The first explicit full-data pytest invocation rejected `--data-root` because the option hook was below pytest's initial conftest discovery boundary. Moving only the repository-wide option/collection hooks to root `conftest.py` corrected the entry point. The exact approved command then passed.
5. Two deliberately operator-cancelled pre-publication download attempts were reconciled immediately; their incomplete staging directories were moved outside the repository, no final artifact or receipt was claimed for the forced termination, and no process remains live.

## Interpretation

- **CONFIRMED:** The pinned raw response is preserved byte-for-byte and independently matches both required archive and workbook-member digests.
- **CONFIRMED:** The fixed-schema Parquet artifact contains exactly 1,044,848 physically identified retained events, with every accepted stitch and quality invariant satisfied and no tuple deduplication.
- **CONFIRMED:** Synthetic tests exercise identifier/description coercion, whitespace/null/sign/extreme preservation, cancellation derivation, decimal fidelity, source drift, offline behavior, corruption, atomic failures, receipts, CLI errors, range recovery, and point-in-time filtering without using official transaction rows as test output.
- **CONFIRMED:** Two isolated same-platform builds from the same clean revision and lock produced identical Parquet bytes, Arrow schema, event-ID order hash, aggregate profile, and normalized manifest invariants.
- **CONFIRMED:** Raw, normalized, and receipt state is ignored by Git, owner-only on POSIX, free of partial publications and persistent DuckDB files, and absent from the committed package/history.
- **INFERRED:** The foundation is operationally sufficient for a separately specified transaction-demand research phase, subject to new owner authorization and explicit factor/target semantics.
- **UNKNOWN:** Dataset timezone, historical provider revision state, cross-platform Parquet byte identity, future provider availability, and all marketplace/external-demand observations remain unresolved.

## Limitations and residual uncertainty

- This verifies transaction-event history only. It does not establish marketplace listings, availability, supply, competition, independent demand, a complete opportunity universe, rankings, targets, factors, or backtest validity.
- No cross-platform rebuild ran; the contract requires logical equality across platforms but claims byte equality only for the same lock/platform.
- UCI can revise or remove its current object. The pinned adapter will fail closed on a revision but cannot reconstruct the provider's historical revision state.
- The observed proxy truncation is environment-specific. Range recovery is bounded and fail-closed, but broader network reliability has not been measured longitudinally.
- Customer references remain in local ignored raw/normalized data. This record includes only aggregate null counts and no transaction or customer-reference values.
- No remote push, data publication, account creation, credentials, purchase, external cost, marketplace/demand integration, or Phase 2 implementation occurred.

## Integrity and provenance

- **Artifact location:** Canonical ignored artifacts under `data/raw/uci-online-retail-ii/<archive-sha256>/` and `data/normalized/uci-online-retail-ii/<archive-sha256>/transaction-event-v1/`; exact digests above. The isolated comparison root was temporary local state and is not a durable source of project truth.
- **Artifact digest:** Raw, normalized, lock, and build-output SHA-256 values are listed in the observation table. This evidence record intentionally does not duplicate or publish dataset bytes.
- **External retention risk:** The local ignored artifacts are not protected by Git. Reproduction depends on either retaining the verified raw bundle locally or UCI continuing to serve the pinned bytes.
- **Supersedes / superseded by:** Complements the source/dataset evidence in [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](EVIDENCE-20260812T060103Z-historical-dataset-probes.md) and [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md); superseded by `NONE`.

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `2026-08-12T09:31:09Z` | `agent:codex-phase1-final-independent-review` | The original record did not establish safe no-clobber publication, preservation of existing directory modes, pre-publication manifest validity, formula/error rejection, signed-int64 bounds, bounded initial streaming, ignored custom in-worktree roots, or partial `prepare` provenance. Its broad fail-closed and coverage claims were therefore overstated. | Independent review reproduced each defect in private temporary paths and returned the Phase 1 issue to `IMPLEMENTING`; the complete round is preserved in the linked issue. |
| `2026-08-12T09:31:09Z` | `agent:codex-phase1-final-independent-review` | The provider ZIP and raw manifest were acquired and published at clean revision `e049af3628a280e4c2af2b760f27efb802cd34e8`, not at `c599a5e245b923764df672aecf6973abdc29e638`. Revision `c599a5e` changed only root/test pytest-hook placement, cleanly verified and reused that raw bundle, and built the superseded normalized manifest. | `git diff --exit-code e049af3 c599a5e -- README.md pyproject.toml uv.lock src .python-version .gitignore PROJECT_SPEC.md ADR` returned `0`; the complete name-status difference was only added root `conftest.py` and modified `tests/conftest.py`. The immutable raw ZIP/manifest digests did not change. |
| `2026-08-12T09:54:59Z` | `agent:codex-phase1` | Post-review implementation revision `0ca3d86f4935e2538d950c6da46b7bb7c5e5d8f7` supersedes the original runtime verification. It cleanly reverified the unchanged raw bundle, rebuilt normalized state, passed the expanded gates, and produced the corrected hashes/results below. The original undocumented event-order digest is retained above but is replaced for reproducibility by the explicit NUL-delimited digest procedure below. | Clean-revision manifest provenance, expanded tests, full-data acceptance, isolated rebuild, exact scripts, and outputs in the appended revalidation section. |
| `2026-08-12T10:12:21Z` | `agent:codex-phase1` | The first post-review correction at `0ca3d86` still checked only five final artifact filenames for Git-ignore coverage. It did not prove that staging descendants of a custom in-worktree data root were ignored. Final implementation revision `c937c3f8eca6b9d54ad77c47313647710abbe7d8` supersedes that privacy conclusion and its build/package hashes. | Independent round 2 reproduced the granular-ignore gap. Revision `c937c3f` requires the data-root directory itself to match Git ignore before network or writes, adds a regression for final-files-only rules, and passed the final clean gates and deterministic rebuild recorded below. |

## Post-review correction and revalidation

This section appends rather than rewrites the original observations. The first independent implementation review found material defects; revision `0ca3d86f4935e2538d950c6da46b7bb7c5e5d8f7` corrects them with host-native atomic no-replace publication, real-file/directory validation, existing-mode preservation, staged raw-manifest verification, formula/error rejection, signed-int64 bounds, a one-byte oversize sentinel, an in-worktree Git-ignore guard, and accumulated failure-receipt provenance. It adds no dependency, generic adapter, persistent database, external source, factor, universe, target, ranking, or backtest.

### Corrected clean build and gates

The old normalized bundle was moved to a private temporary backup. With the documentation work stashed and `git status --porcelain=v1` empty, this command rebuilt normalized state from the unchanged verified raw bundle:

```bash
uv run --frozen productquant uci prepare --data-root ./data --offline
```

It exited `0` with raw action `verified`, normalized action `created`, and manifest build provenance `git_revision=0ca3d86f4935e2538d950c6da46b7bb7c5e5d8f7`, `git_dirty=false`. The superseded normalized backup and isolated comparison root were then moved to Trash after comparison; the canonical ignored artifacts remain under `data/`.

The final clean implementation-tree gates were:

```bash
uv sync --frozen
uv lock --check
uv run --frozen python -m compileall -q src tests conftest.py
uv run --frozen pytest -q
uv run --frozen pytest -m full_data --data-root ./data -q
uv build
uv run --frozen productquant --help
uv run --frozen productquant uci --help
uv run --frozen productquant uci fetch --help
uv run --frozen productquant uci normalize --help
uv run --frozen productquant uci verify --help
uv run --frozen productquant uci prepare --help
uv run --frozen productquant uci prepare --data-root ./data --offline
uv run --frozen productquant uci verify --data-root ./data
git diff --check
test -z "$(git status --porcelain=v1)"
```

Observed output: `132 passed, 1 deselected`; explicit official gate `1 passed, 132 deselected`; lock, compile, build, six help commands, offline prepare, verify, whitespace, and clean-tree checks all exited `0`. Offline prepare and verify both reported `verified/verified` for raw/normalized. The full-data test now contains literal, test-owned assertions for the 17-field schema, every required aggregate, both source artifact sizes/digests, stitch values, IDs, and capability denials instead of delegating them to mutable production constants.

Expanded synthetic/failure coverage includes competing file/directory/symlink targets, a late target race, two concurrent publishers, pre-commit and post-commit sync failures, symlink bundle/member rejection, receipt collision/failure windows, preservation of pre-existing modes, unignored/ignored in-worktree roots, staged invalid HTTP provenance, bounded oversized response, real raw and Parquet write failures, archive/member size drift, formula/error cells, exact zero and `±80,995` quantities, signed-int64 endpoints/overflow, partial `prepare` provenance, and exact Parquet writer settings. Concurrent success remains unsupported; the tested contract is one complete winner and a safe no-clobber failure for every loser.

### Corrected artifacts and package output

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| UCI provider ZIP | 45,622,418 | `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` |
| Sole workbook member | 45,622,278 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Raw manifest | 1,618 | `7137efb4ce98bc295e7c37927d33f45f9901c521f72e1c4fbc764124216d4dd3` |
| `events.parquet` | 11,936,741 | `49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f` |
| Corrected normalized manifest | 2,760 | `59a6197c56e97acf956573ef4a577f273c27c471470fd449fbaa868a02032cae` |
| `uv.lock` | repository file | `10acdaade93f8f17a84637fcd5414c50f53f0c99b08c2fab2aa337dfb0137569` |
| Corrected wheel | ignored build output | `d0d5440514df3220e7e480ef06e5afef4637d5e66333d7416160899033f1a276` |
| Corrected source distribution | ignored build output | `92ba2e60c71cf276ab26b4f9b9b17f5924a9c460cf50effba71955b0c826201f` |

The normalized Parquet bytes are unchanged by the corrections because the pinned workbook has no formula/error cells and all official quantities fit `int64`. The manifest changed only through its corrected clean build revision/time. The full acceptance profile remains exactly the profile recorded above.

### Exact deterministic comparison

The corrected comparison used a private `mktemp` root, copied only the verified raw bundle, ran offline prepare from clean revision `0ca3d86`, and executed this aggregate-only script. It emits no event or customer-reference value:

```python
import hashlib, json, os
from pathlib import Path
import pyarrow.parquet as pq

h = "572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb"
official = Path("data/normalized/uci-online-retail-ii") / h / "transaction-event-v1"
rebuilt = (
    Path(os.environ["PHASE1_REBUILD_ROOT"])
    / "normalized/uci-online-retail-ii" / h / "transaction-event-v1"
)

def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()

def order_digest(path):
    value = hashlib.sha256()
    for batch in pq.ParquetFile(path).iter_batches(columns=["event_id"]):
        for event_id in batch.column(0).to_pylist():
            value.update(event_id.encode("utf-8"))
            value.update(b"\0")
    return value.hexdigest()

def manifest(path):
    value = json.loads(path.read_text())
    value["build"].pop("built_at_utc")
    return value

op = official / "events.parquet"
rp = rebuilt / "events.parquet"
om = manifest(official / "manifest.json")
rm = manifest(rebuilt / "manifest.json")
result = {
    "event_id_order_equal": order_digest(op) == order_digest(rp),
    "event_id_order_sha256": order_digest(op),
    "git_dirty": rm["build"]["git_dirty"],
    "git_revision": rm["build"]["git_revision"],
    "manifest_invariants_equal": om == rm,
    "parquet_bytes_equal": digest(op) == digest(rp),
    "parquet_sha256": digest(op),
    "profile_equal": om["profile"] == rm["profile"],
    "schema_equal": (
        pq.ParquetFile(op).schema_arrow == pq.ParquetFile(rp).schema_arrow
    ),
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
```

Observed output:

```json
{"event_id_order_equal":true,"event_id_order_sha256":"0e0fa0104f115eca3d581cc10a8d5836b648945929b776356fca71269dc99bdc","git_dirty":false,"git_revision":"0ca3d86f4935e2538d950c6da46b7bb7c5e5d8f7","manifest_invariants_equal":true,"parquet_bytes_equal":true,"parquet_sha256":"49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f","profile_equal":true,"schema_equal":true}
```

### Exact repository, link, and local-state scans

The tracked-data/large-file/secret scan was:

```python
import json, re, subprocess
from pathlib import Path

tracked = [
    Path(value)
    for value in subprocess.check_output(["git", "ls-files", "-z"])
    .decode().split("\0") if value
]
tracked_data = [
    str(path) for path in tracked
    if path.suffix.lower() in {".zip", ".xlsx", ".parquet", ".duckdb"}
    or "data" in path.parts
]
large = [
    str(path) for path in tracked
    if path.is_file() and path.stat().st_size > 1_000_000
]
patterns = [
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(
        rb'''(?i)(?:api[_-]?key|password|secret|access[_-]?token)'''
        rb'''\s*[:=]\s*["'][^"']{8,}["']'''
    ),
]
secret_hits = []
for path in tracked:
    if path.is_file() and any(pattern.search(path.read_bytes()) for pattern in patterns):
        secret_hits.append(str(path))
result = {
    "large_tracked_files": large,
    "secret_pattern_hits": secret_hits,
    "tracked_data": tracked_data,
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
assert not any(result.values())
```

Observed output was `{"large_tracked_files":[],"secret_pattern_hits":[],"tracked_data":[]}`. A separate exact link/contract script parsed all four JSON contracts, resolved every tracked relative Markdown link, and returned `{"broken_relative_links":[],"contracts_parsed":4}`.

```python
import json, re
from pathlib import Path

root = Path(".")
link_pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
broken = []
for path in root.rglob("*.md"):
    if any(part in {".git", ".venv"} for part in path.parts):
        continue
    for target in link_pattern.findall(path.read_text(encoding="utf-8")):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "/")):
            continue
        if not (path.parent / target).resolve().exists():
            broken.append(f"{path}:{target}")
contracts = list((root / "src/productquant/contracts").glob("*.json"))
for path in contracts:
    json.loads(path.read_text(encoding="utf-8"))
print(json.dumps({
    "broken_relative_links": broken,
    "contracts_parsed": len(contracts),
}, sort_keys=True, separators=(",", ":")))
assert not broken and len(contracts) == 4
```

The local-state script asserted real, non-symlink raw/normalized bundle directories; exact two-file contents; POSIX `0700` directories and `0600` files; the exact receipt schema/run-ID/status/mode for every receipt; and absence of `*.duckdb`, `.part`, or publication-claim paths. It returned:

```python
import json, os, re, stat
from pathlib import Path

h = "572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb"
root = Path("data")
raw = root / "raw/uci-online-retail-ii" / h
norm = root / "normalized/uci-online-retail-ii" / h / "transaction-event-v1"
receipts = root / "receipts/uci-online-retail-ii"
assert {path.name for path in raw.iterdir()} == {
    "online-retail-ii.zip", "manifest.json"
}
assert {path.name for path in norm.iterdir()} == {
    "events.parquet", "manifest.json"
}
for directory in (raw, norm):
    assert not directory.is_symlink()
    if os.name == "posix":
        assert stat.S_IMODE(directory.lstat().st_mode) == 0o700
for path in (*raw.iterdir(), *norm.iterdir()):
    assert path.is_file() and not path.is_symlink()
    if os.name == "posix":
        assert stat.S_IMODE(path.lstat().st_mode) == 0o600
required = {
    "schema_version", "run_id", "command", "started_at_utc",
    "finished_at_utc", "status", "data_root", "git_revision",
    "git_dirty", "artifacts", "statistics", "error",
}
counts = {"success": 0, "failure": 0}
for path in receipts.glob("*.json"):
    value = json.loads(path.read_text(encoding="utf-8"))
    assert set(value) == required and value["status"] in counts
    counts[value["status"]] += 1
    assert re.fullmatch(r"\d{8}T\d{12}Z-[0-9a-f]{8}", value["run_id"])
    assert not path.is_symlink()
    if os.name == "posix":
        assert stat.S_IMODE(path.lstat().st_mode) == 0o600
partials = [
    str(path) for path in root.rglob("*")
    if ".part" in path.name or "publish-claim" in path.name
]
duckdb = [str(path) for path in root.rglob("*.duckdb")]
print(json.dumps({
    "bundle_contents": "exact",
    "duckdb_files": len(duckdb),
    "partial_artifacts": len(partials),
    "receipt_count": sum(counts.values()),
    "receipt_status_counts": counts,
}, sort_keys=True, separators=(",", ":")))
assert not partials and not duckdb
```

```json
{"bundle_contents":"exact","duckdb_files":0,"partial_artifacts":0,"receipt_count":13,"receipt_status_counts":{"failure":1,"success":12}}
```

These counts are an observation at the clean-gate cutoff, not a fixed contract; later successful CLI verification legitimately appends receipts.

### Corrected residual uncertainty

- Native no-replace publication was exercised on this macOS/APFS host, including deterministic fault/race simulations. Linux and Windows paths are implemented but not exercised here; no real power-loss or cross-platform rebuild was available.
- A post-commit parent-directory sync failure can report exit `5` while leaving a complete final bundle/receipt; the next command verifies that real final state. This is intentional fail-closed recovery behavior, not a partial publication.
- Concurrent writers are unsupported. Tests establish only safe no-clobber resolution, not fairness, locking, or concurrent throughput.
- Provider revision history, source timezone, cross-platform Parquet byte identity, marketplace state, external demand, complete opportunity universe, cancellation/netting policy, and every Phase 2 research semantic remain unknown, unsupported, or unauthorised exactly as stated in the accepted scope.

## Final revalidation after the Round 2 privacy correction

Independent implementation-review round 2 accepted ten of the eleven round-1 resolutions but reproduced one remaining defect: five granular final-file ignore rules could pass the privacy check while transient staging descendants remained trackable. Revision `c937c3f8eca6b9d54ad77c47313647710abbe7d8` resolves that single remaining finding by requiring the in-worktree data-root directory itself to match `git check-ignore --no-index`. The directory-form probe covers all present and future final, receipt, and staging descendants without changing the policy for roots outside a Git worktree.

The regression `test_final_files_only_ignore_rules_do_not_cover_staging_or_pass_policy` establishes that granular final-file patterns are rejected before network access, subdirectory creation, writes, or mode mutation. The contract and README use the same root-level rule. No dependency, persistence format, public command, event field, source, dataset row, factor, universe, target, rank, or backtest behavior changed.

### Final clean implementation gates

With Phase 1 documentation changes stashed and `git status --porcelain=v1` empty, the unchanged verified raw bundle was used to rebuild normalized state from `c937c3f8eca6b9d54ad77c47313647710abbe7d8`:

```bash
uv run --frozen productquant uci prepare --data-root ./data --offline
```

The command exited `0`, reported raw `verified` and normalized `created`, and published a normalized manifest with `git_revision=c937c3f8eca6b9d54ad77c47313647710abbe7d8` and `git_dirty=false`. The following clean-tree gates then all exited `0`:

```bash
uv sync --frozen
uv lock --check
uv run --frozen python -m compileall -q src tests conftest.py
uv run --frozen pytest -q
uv run --frozen pytest -m full_data --data-root ./data -q
uv build
uv run --frozen productquant --help
uv run --frozen productquant uci --help
uv run --frozen productquant uci fetch --help
uv run --frozen productquant uci normalize --help
uv run --frozen productquant uci verify --help
uv run --frozen productquant uci prepare --help
uv run --frozen productquant uci prepare --data-root ./data --offline
uv run --frozen productquant uci verify --data-root ./data
git diff --check
test -z "$(git status --porcelain=v1)"
```

Observed output was `133 passed, 1 deselected`; the explicit official-data gate was `1 passed, 133 deselected`. Lock validation, compilation, build, all six help commands, offline prepare, verify, whitespace, and clean-worktree checks passed. Offline prepare and verify both reported raw/normalized `verified/verified` without rewriting valid bundles.

### Final artifact and deterministic-rebuild observations

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| UCI provider ZIP | 45,622,418 | `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` |
| Sole workbook member | 45,622,278 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Raw manifest | 1,618 | `7137efb4ce98bc295e7c37927d33f45f9901c521f72e1c4fbc764124216d4dd3` |
| `events.parquet` | 11,936,741 | `49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f` |
| Final normalized manifest | 2,760 | `79c6f9e087033eb01afb70f761ab5abf70c49a3de72812f3e3238c8725956e64` |
| `uv.lock` | repository file | `10acdaade93f8f17a84637fcd5414c50f53f0c99b08c2fab2aa337dfb0137569` |
| Final wheel | 27,066 | `763bfc2532ac6e674fc4ef14003544b5288eb20dced5130e100fe2087eee0593` |
| Final source distribution | 21,636 | `c78ca629b3ac00b1a5f0a43aceafc7fcc8516b9c6e2e98bfdece04d932fcc3af` |

The raw artifacts and normalized Parquet bytes remain unchanged. Only normalized build provenance/time and package contents changed. A second isolated offline build from the same clean revision and lock was compared explicitly with the canonical artifact. `cmp` proved byte-identical Parquet; the Arrow schemas, 1,044,848-row event order, aggregate profile, and complete manifest after removing only `build.built_at_utc` were equal. The NUL-delimited event-order SHA-256 was again `0e0fa0104f115eca3d581cc10a8d5836b648945929b776356fca71269dc99bdc`.

The exact final comparison used `cmp` on the two Parquet files, `diff -u` on `jq -S 'del(.build.built_at_utc)'` for both manifests, and a frozen PyArrow script that streamed only `event_id` into NUL-delimited SHA-256. Both silent commands exited `0`; the script and final assertion emitted:

```text
{'canonical': {'rows': 1044848, 'event_order_sha256': '0e0fa0104f115eca3d581cc10a8d5836b648945929b776356fca71269dc99bdc'}, 'rebuild': {'rows': 1044848, 'event_order_sha256': '0e0fa0104f115eca3d581cc10a8d5836b648945929b776356fca71269dc99bdc'}, 'schema_equal': True, 'all_equal': True}
deterministic_rebuild=PASS
```

Both normalized manifests recorded `git_revision=c937c3f8eca6b9d54ad77c47313647710abbe7d8` and `git_dirty=false`. Because the manifests excluding build time were equal, this also establishes profile, stitch, schema text, artifact digest, dependency, capability, and provenance-reference invariants without emitting row values.

At the `2026-08-12T10:12:21Z` observation cutoff, canonical bundle directories/files were real non-symlinks with owner-only modes, 18 row-free receipts existed (`17` success, `1` failure), and no partial publication, symlink, or persistent DuckDB file was present under `data/`. Receipt count is observational and grows on later successful verification. The isolated rebuild, its command summaries, and the superseded normalized backup were moved to the system Trash after comparison; canonical ignored raw and normalized artifacts remain locally reproducible under `data/`.

This final implementor revalidation does not self-approve the milestone. A later fresh independent review must directly verify the remaining privacy correction and classify architecture drift before the Phase 1 issue can close. Linux/Windows native no-replace execution, real power loss, cross-platform byte identity, provider revision history/timezone, marketplace state, independent external demand, complete opportunity universe, cancellation/netting policy, and all Phase 2 semantics remain unverified, unsupported, or unauthorised.
