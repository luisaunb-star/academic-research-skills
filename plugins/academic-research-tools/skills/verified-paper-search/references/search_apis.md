# Structured search APIs: OpenAlex, Semantic Scholar, and what doesn't have an API

Read `SKILL.md` for when to use these. This file is the endpoint reference.

## Why structured APIs come before free-text search

A query against a structured metadata API returns title, full author list, venue, year, and DOI as separate, directly comparable fields in one response. That's a stronger verification signal than parsing prose out of search snippets — it's not just faster, it's the actual mechanism that makes the "check title+authors+venue as one combination" verification step (see `verified-paper-search/SKILL.md`, Step 4) reliable rather than approximate.

## In Claude Code (network-enabled bash)

Use `scripts/lookup.py` directly:

```bash
python3 scripts/lookup.py openalex "supply chain digital twin resilience" --limit 5
python3 scripts/lookup.py openalex-doi 10.1080/00207543.2025.2551243
python3 scripts/lookup.py s2 "agile waterfall project success rates" --limit 5
python3 scripts/lookup.py s2-id 10.1080/00207543.2025.2551243
```

Each prints normalized JSON: `title`, `authors`, `year`, `venue`, `doi`, `is_oa`, `citation_count`, `source`, `url`. Pass `--mailto your@email` to the OpenAlex commands if doing more than a handful of calls — it joins OpenAlex's "polite pool," which is faster and less rate-limited.

The script uses only the Python standard library (`urllib`), so there's nothing to `pip install`.

If a call fails with a network error, the script's error message says so explicitly and points back here — that's the signal to switch to the web_fetch approach below instead of assuming the API itself is down.

## In environments without outbound network access from bash (e.g. some claude.ai sandboxes)

`scripts/lookup.py` can't reach the network from inside a sandboxed bash. Use `web_fetch` directly against the same endpoints instead — same URLs, same query parameters, just fetched as a tool call rather than from Python:

- OpenAlex search: `https://api.openalex.org/works?search=<url-encoded query>&per-page=5`
- OpenAlex by DOI: `https://api.openalex.org/works/https://doi.org/<doi>`
- Semantic Scholar search: `https://api.semanticscholar.org/graph/v1/paper/search?query=<url-encoded query>&limit=5&fields=title,authors,year,venue,externalIds,openAccessPdf,citationCount,url`
- Semantic Scholar by ID/DOI: `https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=title,authors,year,venue,externalIds,openAccessPdf,citationCount,url`

`web_fetch` will return the raw JSON as text — read it the same way you'd read the script's output, just without the normalization step (the field names above are the originals, not the script's renamed versions).

## What doesn't have a usable public search API

- **SciELO** — only supports lookup by a known article/journal ID, not free-text discovery. For SciELO-indexed work, use `web_search` with `site:scielo.br` (or the relevant country domain) plus precise terms, then `web_fetch` the resulting page.
- **Redalyc** — no public API at all. Same approach: `web_search site:redalyc.org` plus terms, then `web_fetch` the page.

This is a real coverage gap for regional Latin American / Portuguese-language journals that aren't well represented in OpenAlex or Semantic Scholar — don't treat a clean structured-API miss as "this doesn't exist," it may just mean it's not indexed by these two APIs and needs the manual search path instead.

## A note on what was actually verified while building this

The script's syntax and CLI argument handling were checked locally, but live API calls could not be tested from inside the sandbox used to build this skill — outbound requests to `api.openalex.org` were blocked by that sandbox's network allowlist (a property of that specific tool environment, not of OpenAlex). The script handled that failure gracefully (a clear JSON error, no crash), but the actual data-retrieval path against live OpenAlex/Semantic Scholar should be smoke-tested in the real Claude Code environment before relying on it.
