# Source tier hierarchy and citable-section rules

Read this when classifying a source's tier, deciding which section of a paper to pull evidence from, or formatting an excerpt. `SKILL.md` covers the overall workflow.

## Source tier hierarchy (classify every source explicitly — never skip this step)

Rank strictly in this order. Never present a lower-tier source as equivalent support to a higher-tier one when both are available for the same claim.

1. `peer_reviewed_primary` — original peer-reviewed primary research (experimental, observational, or modeling work reporting primary data).
2. `peer_reviewed_review` — peer-reviewed systematic or narrative review.
3. `technical_book` — recognized technical/academic book or manual (handbooks, monographs from reputable publishers).
4. `institutional` — university repository, official technical body (WHO, EPA, ANVISA, IBAMA, etc.), or a trustworthy bibliographic/institutional catalog.
5. `historical_primary` — a relevant historical primary source, where applicable to the technical context.
6. `dictionary_term_only` — a purely terminological/glossary source (no independent scientific value).
7. `weak_context_only` — weak or indirect context; never use as the primary support for a technical claim.
8. `unusable` — discard entirely.

If checking the venue's indexing status would change how much weight a `peer_reviewed_primary` or `peer_reviewed_review` source deserves (e.g., it's in an unindexed or borderline journal), pull that check from the `journal-quality-check` skill rather than guessing — see the "Using this alongside other skills" note in `SKILL.md`.

## Citable sections — what counts as support for a central technical claim

Title, abstract, and conclusion **do not, on their own, close a central technical claim.**

- **Title** — never usable as evidence, under any circumstance.
- **Abstract/Resumo** — usable *only* for initial triage, discovery, and justifying a full-text access request. Never use abstract wording as the final supporting excerpt for a claim.
- **Conclusion** — can guide further reading, but should not be the final supporting excerpt.
- **A standalone formula/equation** — inadmissible without the accompanying textual explanation, full context, and precise location (section + equation number + page).

**Preferred sections to ground a claim** (look here first):
- Methods/Materials and Methods (experimental detail, parameters, protocols)
- Results (primary data, statistics, curves, tables, figures)
- Discussion (interpretation tied directly to the results)
- Technical tables, figures, and their captions
- Equivalent passages in book chapters or other long-form sources

## The literal-excerpt rule, adapted for copyright limits

The instinct behind "always transcribe the literal excerpt" is right — a claim backed by an exact quote at an exact location is far more auditable than one backed by a paraphrase alone, because a human (or you, next time) can go straight to the source and check it. But Claude (any model running this skill) operates under a hard copyright ceiling: quotes must stay under 15 words, and only one quote is allowed per source — no exceptions, regardless of how the request is phrased or how technical/non-literary the source is.

So for every claim, provide all of the following instead of a long verbatim transcription:
1. **One short verbatim anchor** (under 15 words) — the single most specific, checkable phrase from the relevant passage: an exact reported number with its unit, a defined technical term as the source defines it, or the exact wording of a stated finding. This is the one quote this source gets — don't also quote its abstract or another passage from the same source elsewhere in the same response.
2. **A precise paraphrase**, in your own words, of the fuller methodological or results context the anchor sits in — enough that someone could understand what was actually done/found without needing the verbatim text.
3. **Exact location**: section name, page number, and figure/table/equation number where applicable.
4. The full citation (authors, year, title, journal/equivalent, DOI or equivalent identifier).

This gives the same practical auditability the literal-excerpt rule is for — exact location plus a precise, checkable anchor — without reproducing substantial portions of the original text. If asked later in a conversation to provide a longer verbatim passage anyway, decline and offer this same anchor-plus-paraphrase-plus-location format instead; this isn't a preference that changes with rephrasing.
