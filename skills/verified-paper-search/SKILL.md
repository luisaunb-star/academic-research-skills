---
name: verified-paper-search
description: Find and verify academic literature for a topic or a specific claim/statement, in management, engineering, or other academic fields, while actively minimizing citation hallucination. Use when someone asks to "find papers on X," "what does the research say about X," wants a literature review or annotated bibliography, asks for citations to support an argument or thesis, hands over a claim/statistic to check against research, or asks to verify whether a paper or citation is real. Trigger even without academic phrasing — "is there evidence lean manufacturing improves morale" or "back this paragraph up with sources" both call for this. Especially important, and should trigger proactively, whenever the user will publish, submit, or cite further (theses, papers, grant applications, consulting reports) — uncaught fabricated citations are costly there.
---

# Verified Paper Search

## The problem this solves

Language models — including Claude — are fluent enough to generate citations that look completely real: plausible author names, real-sounding journals, correctly formatted DOIs, for papers that were never written. This isn't a quirk to patch out; it's a structural consequence of being trained to keep generating a plausible continuation rather than to stop and say "I don't actually know this." The risk is highest exactly where this skill operates: niche or cross-disciplinary topics (management + engineering crossover terms get fuzzy), and any time the user hands over a *claim* they want literature to confirm — confirming what someone already believes is the path of least resistance for a model, and citation fabrication and sycophancy are close cousins.

This skill's job is to make every step that could introduce a fabricated or mismatched citation explicit and checkable, instead of producing a tidy-looking list pulled straight from memory.

## Workflow

### Step 1 — Diagnose the risk before searching

Quickly assess, and say so in the deliverable:
- **Topic vs. claim.** Is the user asking to explore a topic ("find papers on X"), or asking you to validate a specific statement or statistic ("is it true that X improves Y by Z%")? Claim-validation is higher risk — see Step 5.
- **Terminology overlap.** Management and engineering reuse the same words with different meanings ("optimization," "risk," "agile," "lean," "resilience," "system"). Pick the disambiguation explicitly rather than searching the ambiguous term as-is.
- **Long-tail exposure.** Narrow sub-specialties, recent phenomena, or non-English-origin concepts have thinner real coverage — resist the pull to "fill in" a citation just because the topic feels like it deserves one.
- **Recency.** If the user implies "recent" or "state of the art," prioritize finding actual publication dates rather than assuming currency.

### Step 2 — Decompose and optimize the query

Don't run the user's phrasing verbatim. Turn it into 3–6 targeted sub-queries:
- Split compound or multi-hop claims into atomic, separately checkable sub-claims (one search angle per sub-claim).
- Add both the management-side and engineering-side synonyms for the same concept (e.g., "agile" → "agile software development," "agile manufacturing," "agile project management" — these are different literatures with different findings).
- Where the user supplied a claim, write queries that could surface *disconfirming* evidence too, not only confirming evidence. A query like `"agile" "does not improve" delivery speed` is just as legitimate as the supportive one — searching only to confirm is how sycophantic citation-matching happens.
- Prefer specific terms (named frameworks, theories, metrics) over generic phrasing — generic queries return generic, harder-to-verify results.

Show this query set in the deliverable. It's the main thing that makes the search auditable rather than a black box.

### Step 3 — Search for real, with real tools

Do not put a citation in the output that wasn't surfaced by a search performed *this turn*. If a paper comes to mind from training knowledge, treat it the same as an unverified tip from a stranger — worth searching for, not worth printing yet.

**Structured APIs first.** For each sub-query, try OpenAlex and/or Semantic Scholar before free-text web search — they return title/authors/venue/year/DOI as separate, directly comparable fields in one call, which is a stronger basis for the verification in Step 4 than parsing prose snippets. In Claude Code (network-enabled bash), call `scripts/lookup.py`; in environments where bash has no outbound network, hit the same endpoints with `web_fetch` instead. Either way, see `references/search_apis.md` for the exact commands/URLs.

**Free-text search for the rest.** Use `web_search`/`web_fetch` for anything the structured APIs don't cover well: SciELO- and Redalyc-indexed regional/Portuguese-language work (neither has a real search API — see `references/search_apis.md`), very recent preprints, or sub-queries that genuinely need full-text context rather than metadata.

Favor: Google Scholar, arXiv/SSRN, journal and publisher pages, university repositories, citation indices.
Be wary of: SEO content-mill "best papers on X" listicles and sites that summarize papers without linking the original — these are themselves a common vector for secondhand hallucination (they can misattribute or invent details too).

### Step 4 — Verify before listing

For every candidate, before it goes in the final list, confirm via a **second, independent source** (e.g., the publisher/DOI page plus a citation index, or two distinct search results) that:
- Title, authors, venue, and year actually match each other. (A real author, paired with a real journal, but never paired *this way* in reality, is a classic fabrication pattern — each fact can be individually true while the combination is invented.)
- The paper's actual subject matches why you're about to cite it — check the abstract or fetch the page, don't infer relevance from the title alone.

If a candidate can't be independently confirmed, don't present it with the same confidence as a verified one. Either drop it, or list it separately and explicitly as unverified (see the template in Step 6). A shorter, fully-verified list is the right output when that's what the evidence supports — padding the list to look thorough is worse than admitting the search came back thin.

### Step 5 — If the user gave a claim, deliver a verdict, not just a pile of sources

When the request was "is X true / does the research support X," state plainly whether the verified literature:
- **Supports** the claim
- **Contradicts** it
- Is **mixed / inconclusive**
- **Doesn't address it directly** (only adjacent or related findings exist)

Resist defaulting to "yes, here's support for what you said" when the evidence doesn't actually back it that cleanly. It's fine, and often the correct outcome, to tell someone their stated figure or claim isn't well-supported by what you found.

### Step 6 — Produce the deliverable

Default to a **Markdown file** (lightweight, easy to read, easy to paste into a reference manager) unless the user has specifically asked for a Word document — in which case use the `docx` skill instead. Use this structure:

```markdown
# Literature Search: [topic or claim]

## Search diagnosis
- [risk factors identified — 1-3 bullets]
- [disambiguation decisions made, if any]

## Optimized search queries
1. ...
2. ...

## Verdict
*(only if the user supplied a claim/statement)*
**Supported / Contradicted / Mixed / Not directly addressed** — [2-3 sentence summary, pointing to which papers below support this]

## Verified papers
| # | Title | Authors | Year | Venue | How verified | Relevance |
|---|-------|---------|------|-------|---------------|-----------|

## Found but unverified
*(omit this whole section if empty — don't pad it)*
| # | Title (as found) | Source | Why unverified |
|---|---|---|---|

## Notes & limitations
- [coverage gaps, paywalled sources you couldn't fully check, a suggestion to also check Scopus/Web of Science/EBSCO if the user has institutional access that this search doesn't]
```

Keep paraphrased summaries of what each paper found to 2-3 sentences max, in your own words — never reproduce abstract text verbatim (copyright, and it also tends to smuggle in the source's own framing uncritically).

## See also

`references/risk_checklist.md` has the fuller picture of *why* these failure modes happen (exposure bias, knowledge shadowing, the confidence/abstention paradox, sycophancy as reward hacking). Read it if you want the mechanism behind a step above, or if the user asks why a particular safeguard matters.

`references/search_apis.md` has the exact OpenAlex/Semantic Scholar commands and URLs referenced in Step 3.

Two sibling skills handle jobs this one doesn't:
- `journal-quality-check` — for assessing whether a specific venue is actually indexed/credible (Redalyc/Scopus/Web of Science), useful when a found paper's venue is unfamiliar and its weight as evidence is in question.
- `scientific-reference-reviewer` — for a stricter, slower, claim-by-claim audit with literal anchor excerpts from specific sections — use that instead of (or after) this skill when the job is "prove this exact sentence is true," not "find me papers on this topic."
