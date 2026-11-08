# Structured search APIs: OpenAlex-first retrieval and Semantic Scholar contingency

Read `SKILL.md` for researcher approval gates and pipeline boundaries. This file documents request construction, availability handling, complete pagination, and provenance. Official documentation checked on 8 November 2026. API rules can change. If an actual response contradicts this reference, record it and consult the official documentation. Do not guess syntax or silently relax the approved strategy.

## 1. Keep lookup separate from corpus retrieval

The existing `scripts/lookup.py` is a **small metadata lookup helper**, not an exhaustive corpus retriever. Its search commands default to five results and do not paginate. Do not use those defaults, `--limit 5`, or any other top-N shortcut to build the review corpus. Its examples concern diagnostic or exact-paper checks only. It does not implement the new five-minute fallback policy or `x-api-key` authentication.

Implement the approved corpus retrieval using the API rules below in network-enabled Claude Code. Use an HTTP client's parameter encoder, a monotonic clock, bounded request execution, checkpoints, and complete pagination. A printed instruction or a request-library timeout alone is not proof that a strict wall-clock deadline is enforced. Do not claim that running this helper executes the entire skill.

If the environment blocks network access, report that restriction. Another authorized tool may access the same approved API, but do not claim that a provider is down because a particular local runtime blocks it. Never send credentials through a public fetch URL. Stop with preserved partial results if there is no usable authorized network route.

## 2. OpenAlex primary requests

Endpoint: `GET https://api.openalex.org/works`.

Use documented search parameters:

- `search`: title, abstract, full text, and keyword matching.
- `search.title`: title text.
- `search.title_and_abstract`: title and abstract text.
- `search.title_abstract_keywords`: title, abstract, and keywords.
- Matching `.exact` forms disable stemming. **Wildcard searches require `.exact`**. At least three characters must precede a wildcard. Leading wildcards are unsupported.
- Boolean operators are uppercase `AND`, `OR`, and `NOT`. Group with parentheses, quote phrases with ASCII double quotes, and encode the resulting parameter value.

Do not assume inline `title:(...) AND abstract:(...)` field selectors are validated merely because HTTP 200 is returned. Prefer the documented parameter-level field scopes. If separate title-versus-abstract constraints cannot be expressed with verified syntax, explain the limitation and obtain approval of an adaptation.

Example of wildcard transport, **only after approval of both query and search scope**:

```python
params = {
    "search.title_and_abstract.exact": '("societal impact" OR "social impact") AND (universit* OR "higher education")',
    "per_page": 100,
    "page": 1,
}
```

`search.exact` is appropriate instead when the researcher approved the broad title/abstract/full-text/keyword scope. Do not silently switch scopes or stemming modes to make a query work. Compiling a researcher-approved wildcard into its documented exact variant must be shown in the approved request parameters.

Use approved metadata filters only, such as `filter=publication_year:2021`. Preserve exact filters and their purpose. Requests have a URL-length limit of approximately 4 KB. A long OR block may be partitioned through a documented logically equivalent union, with query provenance retained. Any nonequivalent rewrite requires approval.

### Authentication and pagination

Basic anonymous use is supported. If the researcher already configured their own OpenAlex key, send `Authorization: Bearer <key>` from a local environment variable, not in a logged URL. Do not request an OpenAlex key merely to avoid the requested Semantic Scholar contingency.

The supported page size is `per_page=100`. The legacy value 200 is deprecated. Basic paging supports at most 10,000 results. For a keyless accepted result set within that range, use basic `page` pagination rather than an unnecessary cursor continuation. Check records actually saved against the reported count and end-of-results response. A count is a consistency check, not permission to drop missing records.

Cursor paging starts with `cursor=*` and continues using `meta.next_cursor`. Current OpenAlex requires a free key after the first cursor page. If a keyless cursor yields 401, first check whether basic paging can complete the same accepted query. If the required corpus exceeds basic paging and no key is configured, record that OpenAlex retrieval cannot be completed and invoke the approved contingency. Never label the first 10,000 as the complete result set. If a returned cursor is unnecessary because completeness was already confirmed, do not treat the refusal of that unnecessary request as loss of corpus completeness.

Persist each successful page and the pending page/cursor before retries or provider changes. Detect repeated cursors, unexpected payloads, duplicate IDs, and count inconsistencies. Report unresolved inconsistencies as incomplete, not as clean completion.

## 3. Five-minute OpenAlex recovery policy

The user's **300-second policy is an operational ceiling**, not an OpenAlex service guarantee and not a cap on overall search duration.

Start a monotonic deadline immediately before the first attempt of the pending operation. Measure request execution, retry sleeps, and all failures against that same deadline. On a validated successful page, checkpoint and start a fresh deadline for the next operation. A search that keeps making progress may run longer than five minutes.

For transport errors, timeouts, HTTP 429, HTTP 5xx, and malformed successful responses, retry with exponential backoff starting at 5 seconds and capped at 30 seconds. Respect a valid `Retry-After`, including an HTTP-date form. If its wait exceeds the remaining deadline, do not retry earlier than permitted. Wait only until the deadline and then invoke contingency. Bound each request to at most 30 seconds **and** the remaining deadline. Enforce a real wall-clock bound on request execution, for example with a cancellable subprocess timeout. Socket connect/read timeouts alone may not bound an entire transfer or DNS operation.

At the deadline, cancel the pending attempt if necessary, save partial progress, and move to the approved anonymous Semantic Scholar strategy. Do not continually reset the deadline after another failure. Do not keep retrying indefinitely.

Classify failures:

- A valid HTTP 200 response with an empty results list is not an outage. Check whether it is a legitimate zero-result query or the end of pagination.
- HTTP 400/404/422 may identify a query, parameter, URL-length, or endpoint error. Correct verified transport syntax without changing the approved logic, or pause for approval. A provider switch or a key cannot repair a malformed strategy.
- HTTP 401/403 identifies an authentication/permission problem, not a connection timeout. Inspect the sanitized body and pagination requirements. A nonrecoverable refusal of a necessary operation may trigger contingency before 300 seconds.
- HTTP 429 identifies throttling or budget exhaustion, not zero papers. Use bounded recovery and record the cause.
- DNS, TLS, connection errors, and timeouts are transport failures. HTTP 5xx identifies provider/proxy server failure. Preserve the distinction in the audit trail.

## 4. Anonymous Semantic Scholar bulk search

Endpoint: `GET https://api.semanticscholar.org/graph/v1/paper/search/bulk`.

Use **bulk**, not relevance `/paper/search`. The relevance endpoint retrieves at most 1,000 ranked results and does not have bulk Boolean syntax. Bulk returns up to 1,000 records **per response**, with continuation tokens and a provider ceiling of 10 million results per query. Page size is not a target corpus size.

Translate the approved Boolean structure with a syntax-aware method. Do not apply blind global text replacement inside quoted phrases. Documented bulk constructs are `+` for AND, `|` for OR, `-` for negation, parentheses, quoted phrases, prefix `*`, and documented proximity/fuzzy `~N`. Do not assume OpenAlex `AND/OR/NOT`, `?`, full-text scopes, or field selectors transfer unchanged. Send literal `+` through parameter encoding as `%2B`.

Bulk searches **title and abstract**, with English stemming. It does not document OpenAlex-equivalent full-text or keyword search or a title-only selector. Explain changed coverage and pause unless the researcher already approved the contingency strategy and limitations. A completed Semantic Scholar search does not prove completion of an interrupted OpenAlex search.

Example, only with approval:

```python
params = {
    "query": '("societal impact" | "social impact") + (universit* | "higher education")',
    "year": "2021",
    "fields": "paperId,title,authors,year,venue,journal,externalIds,abstract,url,publicationTypes,openAccessPdf,citationCount",
}
```

Supply a nonempty `query`. `fields` selects metadata returned, **not fields searched**. Omitted fields otherwise yield only IDs/titles. Request abstracts and authors explicitly. Treat unavailable metadata as missing rather than generating it.

Supported filters include `year`, `publicationDateOrYear`, `publicationTypes`, `venue`, `fieldsOfStudy`, `minCitationCount`, and the presence-only `openAccessPdf` flag. Add only researcher-approved filters with verified mappings. OpenAlex language/country/institution/topic filters cannot be copied as if equivalent. Do not silently drop an unsupported boundary. Explain options for a researcher-approved adaptation or keep the search incomplete. **Anonymous access does not mean open-access-only articles**, so do not add `openAccessPdf` merely to use the public API. Do not introduce citation-count thresholds.

Read `data`, preserve each response, and repeat identical query/filters/fields with the returned opaque `token` until it is absent. Do not use `offset` or `limit` on bulk search. `total` is approximate and is not an early-stop condition. Detect repeated tokens and report incomplete pagination. If a provider ceiling prevents full retrieval, consult the researcher about approved, documented query partitioning, rather than returning an arbitrary subset.

### Anonymous failure and individual key

Anonymous traffic shares the provider's public pool and may receive 429 even when earlier calls worked. Current official documentation describes a shared 1,000-request-per-second public pool, not a per-user allocation or guaranteed capacity. Individual keys start at 1 request per second across endpoints. Keep requests sequential and respect rate-limit responses.

For a failed anonymous operation, use at most **three attempts or 60 seconds** of recovery, whichever comes first. Count request execution and sleeps. Retry 429/5xx/transport failures with 5- then 10-second backoff, subject to `Retry-After` and the deadline. A nonrecoverable 401/403 may proceed immediately to the key prompt. Malformed request errors require correction or researcher approval, not a key prompt.

If access remains unsuccessful, state the cause and ask whether the researcher wants to configure **their own Semantic Scholar key** as `SEMANTIC_SCHOLAR_API_KEY` locally. Offer stopping with preserved partial output. Do not ask them to paste credentials into conversation or commit them. No account password, email password, or additional personal detail is needed.

Use the **same approved endpoint and request**, adding only the authentication header:

```python
import os
headers = {"x-api-key": os.environ["SEMANTIC_SCHOLAR_API_KEY"]}
```

Never print this dictionary, echo the variable, put the key in a URL, save it in outputs, or include it in an exception. The individual-key path is authenticated access to the same API, not a different database. Invalid keys can return 401 or 403. Apply the same bounded recovery to authenticated access, then stop honestly if it still fails. Keys do not repair network restrictions, DNS/TLS failure, or service outages.

## 5. Corpus preservation and compatible handoff

Preserve original native responses before normalization. Normalize only retrieved title, authors, year, venue, DOI, abstract, document type, OA/PDF availability, citation counts, and provider IDs. Missing Semantic Scholar abstract does not authorize reconstruction from model memory. Missing PDF URL does not establish that an article is paywalled. Missing language/country/institution/citation-network fields remain unavailable.

Use a valid normalized DOI as a cross-provider exact duplicate key. Otherwise use the provider plus a real provider record ID. Title/year/author similarity is only a proposed duplicate requiring confirmation, not an automatic merge. Retain every source record and query/provider provenance when exact duplicates merge. Do not collapse records that lack both DOI and provider ID. Never manufacture an OpenAlex ID from a Semantic Scholar paperId.

When OpenAlex alone succeeds, retain existing file names and exports unchanged. When fallback is used, retain the OpenAlex-only JSON files as clearly labeled subsets and produce the combined `search_all_retrieved.json`, `search_candidate_corpus.json`, and existing **combined** `search_triage_register.csv`. Include source-native records and provider-specific completeness in the combined audit. Hand off the combined CSV to `corpus-screening`, which already accepts it. Do not hand off the OpenAlex-only subset as the whole review corpus.

Report actual saved counts per provider/query, approximate totals separately, exact duplicate merges, and completeness of every attempted provider operation. A fully paginated Semantic Scholar corpus and an interrupted OpenAlex corpus have different completeness statuses. Provider-native bibliometric fields may remain unavailable downstream. No synthetic affiliations, topics, abstracts, references, or citation links may be supplied.

## 6. Optional snowballing under the existing approval gates

Keep OpenAlex as default. If the same failure policy invokes an approved Semantic Scholar adaptation, use separate paginated endpoints:

- Backward: `/graph/v1/paper/{paper_id}/references`, records under `citedPaper`.
- Forward: `/graph/v1/paper/{paper_id}/citations`, records under `citingPaper`.

These endpoints use integer `offset`, `limit` up to 1,000, and returned `next` offsets. Bulk search does not supply complete nested citation/reference edges. Preserve the existing restriction to explicitly approved scoping or realist-informed reviews after researcher-confirmed initial screening, and send all new nonduplicate candidates back to screening. Record missing links, provider coverage, iteration, seed, direction, IDs, and retrieval date. Never claim database links cover an entire bibliography or independently declare theoretical saturation.

## Official sources and test boundaries

- OpenAlex search syntax and fields: https://help.openalex.org/api/searching/
- OpenAlex authentication: https://help.openalex.org/api/authentication/
- OpenAlex pagination: https://help.openalex.org/api/paging/
- Semantic Scholar Academic Graph specification: https://api.semanticscholar.org/graph/v1/swagger.json
- Semantic Scholar tutorial: https://www.semanticscholar.org/product/api/tutorial
- Semantic Scholar public/authenticated access: https://www.semanticscholar.org/product/api
- Officially linked AI2 developer FAQ: https://github.com/allenai/s2-folks/blob/main/FAQ.md

Manus integration probes verified actual anonymous responses from both APIs, OpenAlex wildcard HTTP 400 versus exact-search HTTP 200, OpenAlex cursor-continuation HTTP 401, successful public Semantic Scholar bulk retrieval, and a real Semantic Scholar HTTP 429. A separate policy prototype tested simulated failure/timing/authentication events. These tests do **not** establish that Claude Code or any particular model will follow every instruction, do not prove a real five-minute outage deadline, and do not validate a real individual Semantic Scholar key.
