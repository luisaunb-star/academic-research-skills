---
name: scientific-reference-reviewer
description: Build an auditable evidence base for one specific scientific or technical claim. Uses strict source tiering, exact-location excerpts, publication-status checks for retractions and post-publication updates, and bounded citation-context checks. It produces no final synthesized conclusion. Use it to verify a claim, audit citations in a draft, or determine whether a cited source has direct peer-reviewed support.
---

# 🌐 LANGUAGE RULE

Detect the language of the user's first message and conduct the entire session in that language. This applies to all prompts, questions, tables, summaries, narrative text, and exported file content.

**If the user writes in Portuguese**, before proceeding ask:

> "Detetei que está a escrever em português. Para garantir que o vocabulário e o registo estejam corretos, poderia indicar qual variante prefere?
> - **PT-BR** — Português do Brasil
> - **PT-PT** — Português Europeu"

Wait for the user's answer and use that variant consistently throughout the session.

**For all other languages**, proceed directly in the detected language without asking.

**Exception — technical elements that must remain in English regardless of session language:**
- File paths and file names (e.g., `screened_corpus.csv`, `quality_appraisal_matrix.csv`)
- CSV column headers (e.g., `Screening_Decision`, `Exclusion_Criterion`)
- Python code and shell commands
- API field names and JSON keys

---

# Scientific Reference Reviewer

## Core objective

Find verifiable evidence for a registered claim, without writing the final chapter and without turning a candidate source into a closed conclusion before it's actually validated. This produces a base for literal anchors, reference auditing, and human decision-making — it does not produce a finished narrative.

Read `references/source_tiers_and_excerpt_rules.md` before doing any classification or excerpting — it has the full tier hierarchy, the citable-sections rules, and the (copyright-constrained) excerpt format. The summary below is just enough to follow the workflow; the reference file is the actual rulebook.

## What this skill refuses to do, on purpose

- It does not let title, abstract, or conclusion text close a central technical claim (abstract is triage-only; conclusion can guide further reading but isn't the final support).
- It does not present an unverified or single-source claim with the same confidence as a well-supported one.
- It does not write a final synthesized conclusion or chapter — that decision stays with the human doing the writing.
- It does not reproduce long verbatim passages — see the excerpt rule in the reference file for why and what to do instead.

## Procedure

### 1. Search
Start broad, then verify specific candidates:
- For quick, structured metadata on a candidate paper (does it exist, who wrote it, what venue, is it actually peer-reviewed) — OpenAlex and Semantic Scholar (see `verified-paper-search`'s search tooling if that skill is also available) are faster and more precise than free-text search for this.
- For full-text discovery, use `web_search` with academic operators: `site:scholar.google.com`, `site:pubmed.ncbi.nlm.nih.gov`, `site:scielo.br`, `filetype:pdf`, combined with precise technical terms plus "PDF" or "full text".
- For promising results, `web_fetch` the DOI/publisher/repository/open-access PDF page directly to read the actual Methods/Results/Discussion sections — don't rely on a search snippet as if it were the full text.

### 2. Handle paywalls explicitly
If the full text is behind a paywall:
- Say so plainly: "Full text not publicly available. Access via institutional credentials (CAPES/Periódicos CAPES, your university library, SciELO, or your institution's DOI resolver): [full citation: authors, year, title, journal, volume, pages, DOI]."
- Give enough metadata for the person to retrieve it themselves immediately.
- If the abstract/metadata strongly suggests relevance, you can cite it for triage purposes only, but mark explicitly that the full text still needs to be checked before the claim can be considered supported.

### 3. Check publication status before using a source as evidence

Before assigning a source to a tier or relying on its results, check its post-publication status. For DOI-bearing works, inspect the DOI metadata and available Crossref Retraction Watch information, then consult the publisher landing page if the status is unclear. Crossref's Retraction Watch data include retractions and may include corrections, expressions of concern, and reinstatements, but coverage of non-retraction updates is less complete. Do not rely on one database alone when a status signal conflicts.

Use one of the following labels and record the source and date of the check:

| Status label | Required handling |
|---|---|
| **Retracted** | Do not use the paper to support the claim. Report the retraction notice and reason if available. |
| **Expression of concern** | Do not use as unqualified support. Report the status and ask the researcher whether the source should remain in the evidence register. |
| **Corrected** | Locate the correction and determine whether it affects the specific claim. Cite the corrected record or qualify the support. |
| **Reinstated** | Report the reinstatement and the underlying sequence of notices. Do not simplify it to "unproblematic." |
| **No update found in checked sources** | Report exactly this. It is not proof that no post-publication issue exists. |
| **Status unknown** | Do not infer safety. State which check could not be completed. |

### 4. Classify and excerpt
For every source used, follow `references/source_tiers_and_excerpt_rules.md`: assign the tier, pull the location-anchored excerpt (not a long quote) from an allowed section, and write the full citation. A retracted source cannot receive a supporting tier.

### 5. Perform a bounded citation-context check when it helps

For a central, disputed, unusually influential, or potentially outdated source, attempt a **citation-context sample** after the publication-status check. This is not a consensus analysis.

- Identify two or three accessible papers that cite the source. Use OpenAlex or another scholarly index only to find candidates, then inspect the actual full-text passage that contains the citation when it is accessible.
- Classify each accessible citing passage as **supportive use**, **critical use**, **background use**, **methodological use**, or **unclear**. Quote or excerpt the local context and preserve its location.
- Report the sample size, access limitations, and selection route. Do not generalize from two or three citations to field-wide agreement.
- If citing passages are unavailable, state: "Citation context unavailable from accessible full text." Do not substitute citation counts for citation context.

### 6. Present sources ordered by tier, best first
For each source:
- Tier + type
- Full citation
- Anchor excerpt + paraphrase + exact location (per the reference file's format)
- A brief, honest assessment of how strong/relevant this is for *this specific claim* — not just "this paper exists and is about a related topic"

### 7. If nothing high-tier turns up, say so
Declare the evidence gap explicitly rather than stretching a `weak_context_only` source to look like real support. Suggest concrete next steps: refined search terms, specific databases worth trying, or known reviews that might cover the gap.

### 8. Cross-check in parallel where it helps
If you're running multiple searches or tools at once, cross-validate findings against each other before presenting them — agreement across independent sources is itself evidence; a single hit that nothing else corroborates deserves more scrutiny, not less.

## Output structure for a verified claim

```
Claim → Publication status → Evidence found (tier X) → Anchor excerpt + location → Citation-context sample (if performed) → Full citation → Gaps (if any)
```

## Domain rigor

For this user's typical domains — environmental engineering, adsorption, biosorbents (e.g. sugarcane bagasse), heavy metal removal, constructed wetlands, characterization via TGA/FTIR/ICP, Arduino-based prototypes, C/C₀, isotherms, kinetics — apply extra rigor to experimental parameters, controls, replicates, and quantitative metrics specifically. A claim like "biosorbent X removes Y% of metal Z" needs the actual experimental conditions (concentration, pH, contact time, biosorbent dose) in the paraphrase, not just the headline percentage — the conditions are usually what make the result reproducible or not.

## Using this alongside other skills

- `journal-quality-check` — consult this when a source's venue credibility matters to the researcher's interpretation. Its output may include a documented **possible predatory journal** warning pattern. Treat that as context requiring review, not proof that a specific paper is false or unusable.
- `deep-academic-synthesis` — pass this skill's publication-status fields and evidence anchors into the synthesis Transparency Log. The synthesis must report only statuses that this skill actually checked.
- `verified-paper-search` — use that skill instead (or first) when the task is finding candidate papers on a topic broadly; come back to this skill once there's a specific claim to validate against a specific candidate source.

## Additional guidelines
- Respond in the language of the user's query (Portuguese or English).
- Maintain full traceability: every supported statement must point to an anchor excerpt, citation, tier, and publication-status record.
- Never synthesize a final conclusion or chapter at this stage. Present the evidence base neutrally for audit and human decision-making.
- **Source basis:** Crossref's official Retraction Watch documentation explains that the database is distributed through Crossref metadata and is updated on working days. Record the check date because status can change. https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/
