---
name: journal-quality-check
description: Check whether an academic journal is indexed in Redalyc/AmeliCA, SciELO, Scopus, Web of Science, or MEDLINE/PubMed, evaluate how close a journal is to meeting an indexer's admission criteria before submission, or identify documented possible-predatory-journal warning signs without making categorical claims. Use whenever someone asks "is this journal indexed in Scopus/WoS/SciELO," "is this journal MEDLINE-indexed or just in PubMed," "should I submit my paper/journal to X," "is this a predatory journal," "what's the quality of this journal," wants to compare journals for where to publish, or is preparing a journal for indexer submission.
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

# Journal Quality Check

## What "quality" means here

This skill uses indexing status and criteria fulfillment in Redalyc/AmeliCA, Scopus, and Web of Science as a **proxy** for journal quality — not a direct measurement of it. These indexers each run real editorial and bibliometric due diligence (peer-review verification, ethics policies, citation analysis, geographic diversity checks), so meeting their criteria is genuine evidence of a functioning, credible editorial operation. But indexing is not a guarantee that any *specific article* in that journal is correct, and a journal can fail to be indexed for reasons unrelated to quality (too new, too regional, doesn't fit an indexer's current scope) just as easily as for quality reasons. Say this plainly in your output rather than letting "Scopus-indexed" stand in as a silent stamp of truth.

## Two modes — figure out which one is being asked for

1. **Verification mode** — "is Journal X currently indexed in Y?" The person wants today's actual status, not what the criteria say in the abstract.
2. **Self-assessment / gap-analysis mode** — "would my journal qualify," "what do I need to fix before submitting," "how close is this journal to Scopus/WoS standards." The person wants a criteria walkthrough.

These call for different actions — don't run a full criteria audit when someone just wants today's status, and don't just say "yes/no indexed" when someone wants to know what to fix.

## Verification mode

Indexing status changes over time — journals get added, and just as importantly, get **delisted** for failing to maintain criteria (a common pattern for journals that slip into predatory-adjacent practices after initial acceptance). Don't answer from memory; check current status:
- Scopus: search Scopus's source list / Sources search, or web_search the exact journal name + "Scopus indexed"
- Web of Science: search Clarivate's Master Journal List (mjl.clarivate.com) for the journal
- Redalyc/AmeliCA: check the Redalyc catalog directly (redalyc.org) for the journal's page — it will show current indexing badges if any
- SciELO: check the journal's own page within the relevant SciELO collection (scielo.br, scielo.org, or the relevant country's SciELO site) — it lists current indexing/evaluation status directly
- MEDLINE/PubMed: **check whether the journal itself is MEDLINE-indexed, not just whether articles from it appear in PubMed search results** — those are different claims (see `references/indexing_criteria.md` for why). NLM publishes a journal list/catalog for this; a generic "site:ncbi.nlm.nih.gov/pmc [journal name]" search showing up isn't enough on its own.
- Also check: DOAJ (Directory of Open Access Journals) listing and, where relevant, documented concerns in an established predatory-journal watchlist. Treat both as limited signals. A listing or absence from a directory, and appearance or absence from a watchlist, is never by itself proof of legitimacy or misconduct.

Report what you find with a link/source, and the date you checked (status can be stale by the time someone reads this).

## Self-assessment / gap-analysis mode

Read `references/indexing_criteria.md` for the full criteria — it's organized by indexer (Redalyc, Scopus, Web of Science), each with mandatory criteria first and weighted/desirable criteria after. Walk through:

1. **Mandatory criteria first.** These gate everything else — failing one of these means an embargo (6 months for Redalyc, 2+ years for Scopus/WoS) regardless of how well the journal does elsewhere. Flag any mandatory gap as the top priority, before scoring anything else.
2. **Weighted/desirable criteria second**, organized the way the target indexer organizes them (Redalyc's CAV+CD with the 70%/32-of-45 threshold; Scopus's 5 weighted categories; WoS's quality criteria, noting that Impact Evaluation only matters if the goal is SCIE/SSCI/A&HCI rather than ESCI).
3. **Use the cited-reference search technique** from the reference file (Scopus `REFSRCTITLE(...)` or WoS's Cited Reference Search) to check the journal's actual existing citation footprint — this is concrete, checkable evidence of standing rather than a self-report.
4. Where you can't verify something from public sources (e.g., internal peer-review turnaround time), say so explicitly rather than assuming compliance.

Output a clear two-part verdict: what's already met, and a prioritized list of what to fix — mandatory gaps first, since those are what trigger the long embargoes.

## Possible-predatory-journal warning signs (not proof)

Use the label **"possible predatory journal"** only when **multiple independently documented warning signs converge**. Do not classify a journal categorically as predatory. The purpose is to help the researcher examine a risk pattern, not to make an unreviewable allegation.

Potential warning signs that require direct documentation include:
- A claimed peer-review process under two weeks or a "guaranteed publication" promise.
- A rapid increase in publication volume after launch that is not explained by a documented change in scope or publishing model.
- No accessible ethics policy, or a policy that omits plagiarism, conflicts of interest, and retractions.
- An editorial board whose members' institutional affiliations cannot be verified, or whose composition conflicts with the journal's stated international scope.
- Claimed indexing that cannot be verified in the indexer's current official source list.
- **Advertising "indexed in PubMed" without being MEDLINE-indexed.** A journal can have articles reachable through PubMed via PMC or deposit requirements without having passed MEDLINE's journal selection process.

For every check, separate **verified observations** from **interpretation**. Record the source URL and access date. If several indicators converge, report: "Possible predatory journal — multiple documented warning signs require researcher review," then list each observation. If no such pattern is found, report only: "No corroborated warning-sign pattern found in the sources checked." Never report "not predatory."

> Watchlists, directories, and indexer records can be incomplete, delayed, contested, or inaccurate. They are evidence inputs, not final arbiters of journal legitimacy.

## Using this alongside other skills

If you're auditing a source's tier (e.g. in `scientific-reference-reviewer`) or weighing how much to trust a candidate paper from a literature search (e.g. in `verified-paper-search`), a quick venue check from this skill is a useful enrichment: knowing a `peer_reviewed_primary` source has a verified current indexer status and documented editorial-policy information can help the researcher interpret venue context. Do not convert that context into a categorical claim about a paper's truth or a journal's legitimacy. Don't duplicate the full criteria tables into those skills — just pull the verdict from here when venue credibility actually matters to the question being asked.

## A note on scope

This file covers Redalyc/AmeliCA, SciELO, Scopus, Web of Science, and PubMed/MEDLINE. It does not cover discipline-specific or national ranking systems (e.g., Brazil's CAPES/Qualis), which can matter a lot for academic career decisions in some contexts — if that comes up, say so explicitly rather than silently substituting these indexers' criteria for a Qualis question, since they're evaluated differently.
