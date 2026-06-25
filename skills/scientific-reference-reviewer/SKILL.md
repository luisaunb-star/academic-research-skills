---
name: scientific-reference-reviewer
description: Build a rigorous, auditable evidence base for one specific scientific/technical claim — strict source tiering, exact-location excerpt anchors, no final synthesized conclusion. Use when someone wants to verify a specific claim, gather evidence for a technical assertion before citing it, audit existing references in a draft, or check whether a thesis/paper/report claim is actually backed by peer-reviewed literature. Trigger on "scientific evidence for," "verificar claim," "revisão de literatura," "buscar fonte peer-reviewed," "sustentar com artigo," "find evidence for," "peer-reviewed source for," and similar — especially in environmental engineering, adsorption, biosorbents, or water/wastewater treatment. Stricter and slower than `verified-paper-search` — use this skill for "prove this exact sentence," that one for "find me papers on this topic."
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

### 3. Classify and excerpt
For every source used, follow `references/source_tiers_and_excerpt_rules.md`: assign the tier, pull the location-anchored excerpt (not a long quote) from an allowed section, and write the full citation.

### 4. Present sources ordered by tier, best first
For each source:
- Tier + type
- Full citation
- Anchor excerpt + paraphrase + exact location (per the reference file's format)
- A brief, honest assessment of how strong/relevant this is for *this specific claim* — not just "this paper exists and is about a related topic"

### 5. If nothing high-tier turns up, say so
Declare the evidence gap explicitly rather than stretching a `weak_context_only` source to look like real support. Suggest concrete next steps: refined search terms, specific databases worth trying, or known reviews that might cover the gap.

### 6. Cross-check in parallel where it helps
If you're running multiple searches or tools at once, cross-validate findings against each other before presenting them — agreement across independent sources is itself evidence; a single hit that nothing else corroborates deserves more scrutiny, not less.

## Output structure for a verified claim

```
Claim → Evidence found (tier X) → Anchor excerpt + location → Full citation → Gaps (if any)
```

## Domain rigor

For this user's typical domains — environmental engineering, adsorption, biosorbents (e.g. sugarcane bagasse), heavy metal removal, constructed wetlands, characterization via TGA/FTIR/ICP, Arduino-based prototypes, C/C₀, isotherms, kinetics — apply extra rigor to experimental parameters, controls, replicates, and quantitative metrics specifically. A claim like "biosorbent X removes Y% of metal Z" needs the actual experimental conditions (concentration, pH, contact time, biosorbent dose) in the paraphrase, not just the headline percentage — the conditions are usually what make the result reproducible or not.

## Using this alongside other skills

- `journal-quality-check` — consult this when a source's venue credibility actually matters to how much weight a `peer_reviewed_primary`/`peer_reviewed_review` tier deserves (e.g., the venue is unfamiliar or its standing is in question for this specific claim).
- `verified-paper-search` — use that skill instead (or first) when the task is finding candidate papers on a topic broadly; come back to this skill once there's a specific claim to validate against a specific candidate source.

## Additional guidelines
- Respond in the language of the user's query (Portuguese or English).
- Maintain full traceability: every supported statement must point to an anchor excerpt + citation + tier.
- Never synthesize a final conclusion or chapter at this stage — present the evidence base neutrally for audit and human decision-making.
