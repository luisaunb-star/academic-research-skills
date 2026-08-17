---
name: corpus-screening
description: Screen a candidate corpus against researcher-defined inclusion/exclusion criteria. Supports one-researcher or two-independent-human-screener workflows, optional AI pre-flagging and queue prioritization that never make decisions, optional SPAR-4-SLR or PRISMA-oriented reporting fields, and CSV exports for downstream appraisal, bibliometrics, and synthesis.
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

# 🛑 CRITICAL INSTRUCTIONS

Before executing this skill, you MUST adhere to the following rules:

1. **Human Decision Authority.** Inclusion and exclusion decisions belong to the researcher, not to the AI. Your role is to present evidence from the title, abstract, and metadata to support the researcher's judgment. You MUST NOT make final decisions unilaterally.
2. **No Inference Beyond the Record.** Do not infer thematic relevance from author names, journal names, or citation counts alone. Base every recommendation on the content of the title and abstract.
3. **Transparent Reasoning.** For every paper where you suggest Exclude or Uncertain, you must state which criterion triggered the suggestion and quote the relevant phrase from the title or abstract.
4. **Preserve Uncertain Papers.** Papers marked Uncertain must be retained in the corpus for user review. They must not be silently dropped.
5. **Criteria Primacy.** The user's criteria override any default logic. If the user's criteria are ambiguous for a specific paper, flag the paper as Uncertain and ask the user for clarification.
6. **Independent-Screener Integrity.** In two-screener mode, human screeners must make their first-pass decisions independently. The AI may calculate agreement and organize disagreements, but it must not generate a decision that substitutes for either screener or adjudicate a disagreement.

---

# Step 1: Define Inclusion and Exclusion Criteria

Before screening any paper, the user must define the criteria that will govern all decisions. Present the following prompt to the user:

---

**CORPUS SCREENING — CRITERIA DEFINITION**

Please define your inclusion and exclusion criteria for this review. You may adapt the examples below or replace them entirely with your own.

**Inclusion criteria (papers must meet ALL of these to be included):**

- I1. The paper addresses the central phenomenon of interest (not merely mentions it as a side point).
- I2. The paper presents original empirical data or a systematic synthesis of empirical data.
- I3. The paper was published within the defined time window for this review.
- I4. The paper is written in a language the review team can read.

**Exclusion criteria (papers meeting ANY of these are excluded):**

- E1. Out of thematic scope: the topic is mentioned only tangentially or as a secondary concern, with no substantive contribution to the review question. (Justification: studies captured only by keyword coincidence but with semantic dissociation from the phenomenon of interest should be excluded, as they do not contribute to answering the review question.)
- E2. Inadequate publication type: editorials, book reviews, opinion pieces, conference abstracts, and grey literature without peer review. (Justification: these document types typically do not present new robust empirical data or have not passed traditional peer review.)
- E3. Divergent context, sector, or population: the study sample does not correspond to the target of the review. For example, if the review focuses on SMEs, studies conducted exclusively with large multinational corporations or in B2B-only contexts are excluded. (Justification: studies whose samples do not match the review target deviate from the analytical objective.)
- E4. Outside the temporal or language scope: the paper falls outside the defined publication date range, or is written in a language the review team cannot process accurately. (Justification: temporal and language delimitations are justified by practical constraints and the need to historically bound the phenomenon under review.)
- E5. Full text inaccessible: the full text cannot be retrieved and the abstract alone is insufficient to make a reliable inclusion decision.
- E6. Duplicate: the paper is a duplicate of another record already in the corpus.

**Instructions for the user:**
- Confirm, modify, or replace the criteria above.
- Add any field-specific criteria relevant to your review topic (for example, minimum sample size, specific geographic scope, specific methodology types required).

---

After the user confirms or revises the criteria, first ask the following questions and record each answer before proceeding to Step 2:

---

**SCREENING CONFIGURATION**

1. **How many human researchers will screen this corpus?**
   - **One researcher** — one researcher makes all decisions. The AI can provide optional pre-flags or queue ordering, but the researcher makes every final decision.
   - **Two independent researchers** — each researcher screens the same records independently before seeing the other person's decisions. The skill then calculates agreement, presents disagreements, and records the human consensus or third-person adjudication.

2. **Was a reporting / conduct protocol selected in `verified-paper-search`?**
   - **SPAR-4-SLR** — label this stage as *Arranging: Purification* and report included and excluded counts by criterion.
   - **PRISMA 2020 and PRISMA-S** — preserve all record-flow counts and exclusion reasons for a later PRISMA flow diagram.
   - **Default audit structure** — use the standard screening register.

If the corpus includes an inherited protocol choice, show it to the researcher and ask for confirmation rather than asking them to recreate the decision.

---

Then ask the following question before proceeding to Step 2:

---

**Would you like AI pre-flagging during screening?**

If enabled, I will read each title and abstract against your criteria and suggest a preliminary decision (Include, Exclude, or Uncertain) with a direct quote from the text as evidence. You always make the final call and can override any suggestion.

If disabled, I will present each paper without any suggestion, so your decisions are not influenced by my reading.

Type **yes** to enable pre-flagging or **no** to screen without it.

---

After recording the AI pre-flag preference, ask:

**Would you like optional active-learning queue prioritization? (yes/no)**

If enabled, after at least 20 completed human decisions that include both Include and Exclude outcomes, the AI may rank the *next* unscreened records by estimated relevance. It must display that this is an ordering aid only. It must not suppress, remove, classify, or declare screened any record. The researcher can switch it off at any time, inspect the default order, and must ultimately decide every record.

Wait for the user's answers and record the screener mode, reporting protocol, pre-flag preference, and queue-prioritization preference before proceeding to Step 2.

---

# Step 2: Load the Corpus

Ask the user to provide the corpus. Accepted formats:

- `openalex_candidate_corpus.json` or `search_triage_register.csv` exported by `verified-paper-search`.
- A CSV or Excel candidate corpus containing, where available, Title, Authors, Year, Source or Venue, DOI, Abstract, Query_Source, and Preliminary_Triage_Status.
- A plain text list of paper titles with abstracts pasted directly into the conversation.
- A BibTeX or RIS file.

If a separate `journal-quality-check` output is provided, retain any venue-credibility note as optional contextual metadata. Do not treat it as an eligibility decision unless the researcher explicitly included a source-quality criterion in the approved screening criteria. Do not require journal-quality data to begin screening.

Parse the corpus and present the user with a summary:

- Total number of records loaded.
- Number of records with abstracts available.
- Number of records without abstracts (these will require a note during screening).
- Date range of the corpus.

Ask the user to confirm the corpus is complete before proceeding.

---

# Step 3: Title and Abstract Screening

Present papers to the user for screening. For each paper, display the following information:

```
[N of Total] — [Title]
Authors: [Authors] | Year: [Year] | Source: [Journal/Conference]
DOI: [DOI or URL if available]
Search-stage triage: [Direct candidate / Potential candidate / Insufficient metadata / Not available]
Optional venue-credibility note: [Only if separately supplied; never a screening decision unless an approved criterion requires it]

Abstract:
[Full abstract text]

AI pre-flag (if enabled): [Include / Exclude (E1) / Uncertain] — [Reason with quote]

Your decision: I = Include | E = Exclude | U = Uncertain | ? = Need more information
```

The user responds with a single letter for each paper:
- **I** — Include in the corpus.
- **E** — Exclude. The user may optionally add the criterion code (e.g., E2) or a brief reason.
- **U** — Uncertain. The paper is retained for a second-pass review at the end.
- **?** — The user needs more information (for example, to retrieve the full text before deciding).

**Batch size:** Present papers in batches of 10 by default. After each batch, ask the user whether to continue with the next batch or pause.

**Two-independent-screener mode:** Create two identical blank screening files, `/home/ubuntu/articles/screening_screener_1.csv` and `/home/ubuntu/articles/screening_screener_2.csv`, with stable `Record_ID` values and no AI decision populated. Each human screener completes their own file without seeing the other file. Do not compare or reconcile decisions until both files are supplied.

**Optional active-learning queue prioritization:** When the researcher enabled it and the minimum evidence threshold is met, show the next batch in the selected priority order and mark the ordering as "AI queue priority only." Keep every remaining record in the export and allow the researcher to request the original order at any time. Do not use a priority score as a final decision, an exclusion reason, or a stopping rule.

**Papers without abstracts:** Flag these explicitly. Present the title and metadata only, note that no abstract is available, and suggest marking as Uncertain unless the title alone is clearly outside scope.

---

# Step 4: Reconciliation and Uncertain Papers — Second Pass

**If one-researcher mode was selected:** After all papers have been screened once, present all Uncertain papers together for a second-pass review.

**If two-independent-screener mode was selected:** First validate that both completed files contain the same `Record_ID` values and no merged or overwritten decisions. Calculate the raw agreement and unweighted Cohen's kappa across the three first-pass categories (Include, Exclude, Uncertain). Report the number of records compared, agreement percentage, kappa value, and any records excluded from the calculation because a decision is missing. Do not present a kappa threshold as an automatic pass/fail rule.

Then create a disagreement register containing only records where the screeners disagree. Show each paper's title, abstract, criterion evidence, Screener_1_Decision, Screener_2_Decision, and both recorded reasons. Ask the human researchers to enter a consensus decision, or name a third human adjudicator. The AI may quote the record and the pre-approved criteria but must not supply the final reconciliation decision.

After reconciliation, present all records that remain Uncertain together for a second-pass review.

For each Uncertain paper, display the same information as in Step 3 and add a note summarizing why it was flagged as Uncertain in the first pass (either the user's own note or the AI pre-flag reason).

The user must assign a final decision (I or E) to each Uncertain paper. If the user cannot decide without the full text, the paper may remain as Uncertain and will be noted as "Pending full-text review" in the export.

---

# Step 5: Export Screened Corpus

After all decisions are finalized, produce the following outputs:

**1. Screened corpus summary:**

| Decision | Count | Percentage |
|---|---|---|
| Included | [N] | [%] |
| Excluded | [N] | [%] |
| Uncertain (pending full text) | [N] | [%] |
| **Total screened** | [Total] | 100% |

**2. Exclusion breakdown:**

| Exclusion Criterion | Count |
|---|---|
| E1 — Out of thematic scope | [N] |
| E2 — Inadequate publication type | [N] |
| E3 — Divergent context/population | [N] |
| E4 — Outside temporal/language scope | [N] |
| E5 — Full text inaccessible | [N] |
| E6 — Duplicate | [N] |
| Other (user-defined) | [N] |

**3. CSV export:**

Save the full screened corpus to `/home/ubuntu/articles/screened_corpus.csv` with the following columns:

| Column | Description |
|---|---|
| Title | Full paper title |
| Authors | Author list |
| Year | Publication year |
| Source | Journal or conference name |
| DOI | DOI or URL |
| Abstract | Abstract text |
| Search_Triage_Status | Search-stage triage if supplied, otherwise blank |
| Venue_Credibility_Note | Optional output from `journal-quality-check`, not an eligibility decision unless an approved criterion requires it |
| Reporting_Protocol | Default audit structure / PRISMA 2020 and PRISMA-S / SPAR-4-SLR |
| Screener_Mode | One researcher / Two independent researchers |
| Screener_1_Decision | Include / Exclude / Uncertain (or the one researcher's decision) |
| Screener_1_Reason | Criterion code and short rationale |
| Screener_2_Decision | Include / Exclude / Uncertain (blank in one-researcher mode) |
| Screener_2_Reason | Criterion code and short rationale (blank in one-researcher mode) |
| Screening_Decision | Final Include / Exclude / Uncertain after second pass or human reconciliation |
| Exclusion_Criterion | E1–E6 or user-defined code (blank for included papers) |
| Exclusion_Reason | Brief reason text (blank for included papers) |
| Reconciliation_Status | Not applicable / Agreement / Human consensus / Third-person adjudication / Pending |
| Adjudicator | Human name or initials, if applicable |
| Screening_Date | Date of final decision |
| Queue_Priority_Used | Yes / No. This records ordering only, not a decision basis. |

Also save `/home/ubuntu/articles/screening_agreement_report.md` in two-independent-screener mode. It must document the comparison population, raw agreement, Cohen's kappa, missing-decision handling, disagreement count, and human reconciliation process. If SPAR-4-SLR was selected, include a **Purification** table with included and excluded counts by criterion. If PRISMA 2020 and PRISMA-S was selected, include a flow-diagram-ready counts table covering records received, duplicates removed before screening, title/abstract decisions, full-text-pending records, and final inclusions.

Inform the user that the CSV can be opened directly in Excel or Google Sheets, and that the Included and Uncertain rows form the input corpus for the next pipeline stage.

---

# Step 6: Pipeline Handoff

After export, present the following handoff note:

---

**SCREENING COMPLETE — PIPELINE HANDOFF**

The screened corpus has been saved to `/home/ubuntu/articles/screened_corpus.csv`.

- **Included papers ([N])** are ready for the next pipeline stage.
- **Uncertain papers ([N])** require full-text review before a final decision can be made. Retrieve the full texts and re-run this skill on the Uncertain subset, or make final decisions manually.

**Next recommended steps:**

1. If you have not yet run `study-quality-assessment`, apply it to the Included corpus to assess methodological quality before synthesis.
2. If you have completed `journal-quality-check`, retain its result as separate source-credibility information. Do not use it to alter the final screening decision unless the researcher had explicitly defined a source-quality eligibility criterion.
3. Pass the Included corpus to `bibliometric-scientometric-analysis` for co-authorship, keyword co-occurrence, and topic modelling analysis.
4. Pass the Included corpus to `deep-academic-synthesis` for full-text thematic synthesis.
5. If SPAR-4-SLR was selected, treat this completed export as **Arranging: Purification**. If PRISMA 2020 and PRISMA-S was selected, use the preserved counts to produce the later flow diagram.

---

# APPENDIX: FIELD-SPECIFIC GUIDANCE FOR EXCLUSION CRITERIA

The following notes help calibrate the exclusion criteria for non-health fields.

**E1 — Out of thematic scope (Business, IS, Engineering):** In management and IS research, papers often address multiple constructs simultaneously. A paper should be excluded on E1 grounds only when the phenomenon of interest is mentioned in passing (for example, in a single sentence in the introduction) and the paper's central contribution is clearly to a different construct. If the phenomenon appears in the research questions, hypotheses, or main findings, the paper should be retained.

**E2 — Inadequate publication type (all fields):** Conference papers in computer science and engineering are peer-reviewed and may carry equivalent weight to journal articles in those fields. Do not apply E2 to conference papers in CS/engineering unless the conference is clearly non-peer-reviewed (e.g., workshop abstracts, extended abstracts, or poster-only submissions).

**E3 — Divergent context or population (Business, IS):** Apply this criterion with care when the review scope is defined by a specific sector (e.g., SMEs, public sector, healthcare organizations). A paper studying large firms is not automatically excluded if it develops theory or measures that transfer to the review's target context. Flag as Uncertain rather than Exclude when transferability is plausible.

**E4 — Language scope:** If the review team includes multilingual members, consider whether the language exclusion is genuinely justified or whether it introduces geographic bias. Note any language exclusions explicitly in the Methods section of the final review manuscript.

**E5 — Full text inaccessible:** Before applying E5, attempt to retrieve the full text via DOI, Unpaywall, OpenAlex open access links, or institutional access. Apply E5 only when all retrieval attempts have failed.
