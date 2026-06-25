#!/usr/bin/env python3
"""
lookup.py -- structured metadata lookup against OpenAlex and Semantic Scholar.

Used by the verified-paper-search skill to confirm candidate papers via
structured APIs before falling back to free-text web search. Requires
outbound network access (works in Claude Code's bash). In sandboxes with
network disabled (e.g. some claude.ai environments), use web_fetch against
the same endpoints instead -- see references/search_apis.md for the exact
URLs.

Usage:
    python -m scripts.lookup openalex "exact or partial title" [--limit 5] [--mailto you@example.com]
    python -m scripts.lookup openalex-doi 10.1080/00207543.2025.2551243
    python -m scripts.lookup s2 "exact or partial title" [--limit 5]
    python -m scripts.lookup s2-id <paper_id_or_doi>

Each command prints a normalized JSON array to stdout, one entry per result:
    {"title": ..., "authors": [...], "year": ..., "venue": ...,
     "doi": ..., "is_oa": ..., "citation_count": ...,
     "source": "openalex" | "semantic_scholar", "url": ...}

Uses only the standard library (no `requests` dependency) so it runs
anywhere Python 3 does, without an extra pip install.
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

OPENALEX_BASE = "https://api.openalex.org/works"
S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"
DEFAULT_TIMEOUT = 15


def _get(url, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "verified-paper-search-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {body[:500]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Network error reaching {url}: {e}. If this environment has no "
            "outbound network access, use web_fetch against this same URL "
            "instead -- see references/search_apis.md."
        ) from e


def _openalex_authors(work):
    return [
        (a.get("author") or {}).get("display_name")
        for a in work.get("authorships", [])
    ]


def _normalize_openalex(work):
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    doi = work.get("doi") or ""
    return {
        "title": work.get("title"),
        "authors": _openalex_authors(work),
        "year": work.get("publication_year"),
        "venue": source.get("display_name"),
        "doi": doi.replace("https://doi.org/", "") or None,
        "is_oa": (work.get("open_access") or {}).get("is_oa"),
        "citation_count": work.get("cited_by_count"),
        "source": "openalex",
        "url": work.get("id"),
    }


def search_openalex(query, limit=5, mailto=None):
    params = {"search": query, "per-page": str(limit)}
    if mailto:
        params["mailto"] = mailto  # joins OpenAlex's "polite pool": faster, fewer rate limits
    url = f"{OPENALEX_BASE}?{urllib.parse.urlencode(params)}"
    data = _get(url)
    return [_normalize_openalex(w) for w in data.get("results", [])]


def get_openalex_by_doi(doi, mailto=None):
    doi = doi.strip()
    if not doi.startswith("10."):
        doi = doi.split("doi.org/")[-1]
    params = {"mailto": mailto} if mailto else {}
    qs = f"?{urllib.parse.urlencode(params)}" if params else ""
    url = f"https://api.openalex.org/works/https://doi.org/{doi}{qs}"
    data = _get(url)
    return [_normalize_openalex(data)]


def _normalize_s2(paper):
    return {
        "title": paper.get("title"),
        "authors": [a.get("name") for a in (paper.get("authors") or [])],
        "year": paper.get("year"),
        "venue": paper.get("venue"),
        "doi": (paper.get("externalIds") or {}).get("DOI"),
        "is_oa": bool(paper.get("openAccessPdf")),
        "citation_count": paper.get("citationCount"),
        "source": "semantic_scholar",
        "url": paper.get("url"),
    }


_S2_FIELDS = "title,authors,year,venue,externalIds,openAccessPdf,citationCount,url"


def search_semantic_scholar(query, limit=5):
    params = {"query": query, "limit": str(limit), "fields": _S2_FIELDS}
    url = f"{S2_BASE}/search?{urllib.parse.urlencode(params)}"
    data = _get(url)
    return [_normalize_s2(p) for p in data.get("data", [])]


def get_semantic_scholar_by_id(paper_id):
    pid = paper_id.strip()
    if pid.startswith("10."):
        pid = f"DOI:{pid}"
    url = f"{S2_BASE}/{urllib.parse.quote(pid, safe=':')}?fields={_S2_FIELDS}"
    data = _get(url)
    return [_normalize_s2(data)]


def main():
    parser = argparse.ArgumentParser(description="Structured paper lookup via OpenAlex / Semantic Scholar.")
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("openalex", help="Search OpenAlex by title/keywords")
    p1.add_argument("query")
    p1.add_argument("--limit", type=int, default=5)
    p1.add_argument("--mailto", default=None, help="Contact email for OpenAlex's polite pool (optional, recommended)")

    p2 = sub.add_parser("openalex-doi", help="Look up one work in OpenAlex by DOI")
    p2.add_argument("doi")
    p2.add_argument("--mailto", default=None)

    p3 = sub.add_parser("s2", help="Search Semantic Scholar by title/keywords")
    p3.add_argument("query")
    p3.add_argument("--limit", type=int, default=5)

    p4 = sub.add_parser("s2-id", help="Look up one paper in Semantic Scholar by paper ID or DOI")
    p4.add_argument("paper_id")

    args = parser.parse_args()

    try:
        if args.command == "openalex":
            result = search_openalex(args.query, args.limit, args.mailto)
        elif args.command == "openalex-doi":
            result = get_openalex_by_doi(args.doi, args.mailto)
        elif args.command == "s2":
            result = search_semantic_scholar(args.query, args.limit)
        elif args.command == "s2-id":
            result = get_semantic_scholar_by_id(args.paper_id)
        else:
            parser.error("unknown command")
            return
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
