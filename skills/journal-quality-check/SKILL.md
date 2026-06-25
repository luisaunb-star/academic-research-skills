---
name: journal-quality-check
description: Check whether an academic journal is indexed in Redalyc/AmeliCA, SciELO, Scopus, Web of Science, or MEDLINE/PubMed, evaluate how close a journal is to meeting an indexer's admission criteria before submission, or flag predatory/low-credibility journal warning signs. Use whenever someone asks "is this journal indexed in Scopus/WoS/SciELO," "is this journal MEDLINE-indexed or just in PubMed," "should I submit my paper/journal to X," "is this a predatory journal," "what's the quality of this journal," wants to compare journals for where to publish, or is preparing a journal for indexer submission. Also use this as a supporting check whenever evaluating how much weight to give a cited source — e.g. while auditing references or running a literature search — since the venue a peer-reviewed paper appears in materially affects how much that "peer reviewed" label is worth.
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
- Also worth checking: DOAJ (Directory of Open Access Journals) listing, and whether the journal or publisher appears on a predatory-journal watchlist — these aren't in the reference file but are quick, relevant web searches

Report what you find with a link/source, and the date you checked (status can be stale by the time someone reads this).

## Self-assessment / gap-analysis mode

Read `references/indexing_criteria.md` for the full criteria — it's organized by indexer (Redalyc, Scopus, Web of Science), each with mandatory criteria first and weighted/desirable criteria after. Walk through:

1. **Mandatory criteria first.** These gate everything else — failing one of these means an embargo (6 months for Redalyc, 2+ years for Scopus/WoS) regardless of how well the journal does elsewhere. Flag any mandatory gap as the top priority, before scoring anything else.
2. **Weighted/desirable criteria second**, organized the way the target indexer organizes them (Redalyc's CAV+CD with the 70%/32-of-45 threshold; Scopus's 5 weighted categories; WoS's quality criteria, noting that Impact Evaluation only matters if the goal is SCIE/SSCI/A&HCI rather than ESCI).
3. **Use the cited-reference search technique** from the reference file (Scopus `REFSRCTITLE(...)` or WoS's Cited Reference Search) to check the journal's actual existing citation footprint — this is concrete, checkable evidence of standing rather than a self-report.
4. Where you can't verify something from public sources (e.g., internal peer-review turnaround time), say so explicitly rather than assuming compliance.

Output a clear two-part verdict: what's already met, and a prioritized list of what to fix — mandatory gaps first, since those are what trigger the long embargoes.

## Predatory / low-credibility warning signs

Worth flagging proactively even when not explicitly asked, since the cost of citing or publishing in a predatory journal is high and the signs are checkable:
- Single-editor-only peer review, or review claimed to take under 2 weeks with "guaranteed publication"
- Rapidly ramping publication volume right after launch
- No code of ethics, or a code of ethics that doesn't address plagiarism/conflicts of interest/retractions
- Editorial board with no verifiable institutional affiliations, or an editorial board that's entirely internal to one institution while the journal claims to be international
- Claims of indexing that don't show up when you actually check the indexer's own current source list (this happens — some journals advertise "Scopus indexed" after being delisted, or list an indexer they were never actually in)
- **Advertising "indexed in PubMed" without being MEDLINE-indexed.** This is common and easy to miss: a journal can have a handful of articles reachable via PubMed (through PMC or an NIH deposit mandate) without the journal itself having passed MEDLINE's selective review. "PubMed" alone is not the credential being implied.

## Using this alongside other skills

If you're auditing a source's tier (e.g. in `scientific-reference-reviewer`) or weighing how much to trust a candidate paper from a literature search (e.g. in `verified-paper-search`), a quick venue check from this skill is a useful enrichment: knowing a `peer_reviewed_primary` source sits in a Scopus/WoS-indexed, well-cited journal is meaningfully different from the same tier label on an unindexed or borderline journal. Don't duplicate the full criteria tables into those skills — just pull the verdict from here when venue credibility actually matters to the question being asked.

## A note on scope

This file covers Redalyc/AmeliCA, SciELO, Scopus, Web of Science, and PubMed/MEDLINE. It does not cover discipline-specific or national ranking systems (e.g., Brazil's CAPES/Qualis), which can matter a lot for academic career decisions in some contexts — if that comes up, say so explicitly rather than silently substituting these indexers' criteria for a Qualis question, since they're evaluated differently.
