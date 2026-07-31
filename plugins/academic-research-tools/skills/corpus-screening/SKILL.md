---
description: Screen a corpus of papers retrieved by verified-paper-search against user-defined inclusion/exclusion criteria. Produces a screened corpus list with decisions (Include/Exclude/Uncertain) and exports results to CSV for use in subsequent pipeline stages.
---

# 🛑 CRITICAL INSTRUCTIONS

Before executing this skill, you MUST adhere to the following rules:

1. **Human Decision Authority.** Inclusion and exclusion decisions belong to the researcher, not to the AI. Your role is to present evidence from the title, abstract, and metadata to support the researcher's judgment. You MUST NOT make final decisions unilaterally.
2. **No Inference Beyond the Record.** Do not infer thematic relevance from author names, journal names, or citation counts alone. Base every recommendation on the content of the title and abstract.
3. **Transparent Reasoning.** For every paper where you suggest Exclude or Uncertain, you must state which criterion triggered the suggestion and quote the relevant phrase from the title or abstract.
4. **Preserve Uncertain Papers.** Papers marked Uncertain must be retained in the corpus for user review. They must not be silently dropped.
5. **Criteria Primacy.** The user's criteria override any default logic. If the user's criteria are ambiguous for a specific paper, flag the paper as Uncertain and ask the user for clarification.

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

After the user confirms or revises the criteria, ask the following question before proceeding to Step 2:

---

**Would you like AI pre-flagging during screening?**

If enabled, I will read each title and abstract against your criteria and suggest a preliminary decision (Include, Exclude, or Uncertain) with a direct quote from the text as evidence. You always make the final call and can override any suggestion.

If disabled, I will present each paper without any suggestion, so your decisions are not influenced by my reading.

Type **yes** to enable pre-flagging or **no** to screen without it.

---

Wait for the user's answer and record the preference before proceeding to Step 2.

---

# Step 2: Load the Corpus

Ask the user to provide the corpus. Accepted formats:

- A CSV or Excel file exported from the `verified-paper-search` skill (columns expected: Title, Authors, Year, Source, DOI, Abstract, Relevance Score, Journal Quality).
- A plain text list of paper titles with abstracts pasted directly into the conversation.
- A BibTeX or RIS file.

If the corpus comes from the `verified-paper-search` output, confirm that the Relevance Score and Journal Quality columns are present, as these will be displayed alongside each paper during screening.

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
Relevance Score: [High / Medium / Low] | Journal Quality: [Q1/Q2/Q3/Q4 or N/A]

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

**Papers without abstracts:** Flag these explicitly. Present the title and metadata only, note that no abstract is available, and suggest marking as Uncertain unless the title alone is clearly outside scope.

---

# Step 4: Uncertain Papers — Second Pass

After all papers have been screened once, present all Uncertain papers together for a second-pass review.

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
| Relevance_Score | High / Medium / Low (from verified-paper-search) |
| Journal_Quality | Q1/Q2/Q3/Q4 or N/A (from journal-quality-check) |
| Screening_Decision | Include / Exclude / Uncertain |
| Exclusion_Criterion | E1–E6 or user-defined code (blank for included papers) |
| Exclusion_Reason | Brief reason text (blank for included papers) |
| Screened_By | Researcher name or initials (ask user) |
| Screening_Date | Date of screening session |

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
2. If you have already completed `journal-quality-check`, the Journal Quality column in the export allows you to filter by quartile before proceeding.
3. Pass the Included corpus to `bibliometric-scientometric-analysis` for co-authorship, keyword co-occurrence, and topic modelling analysis.
4. Pass the Included corpus to `deep-academic-synthesis` for full-text thematic synthesis.

---

# APPENDIX: FIELD-SPECIFIC GUIDANCE FOR EXCLUSION CRITERIA

The following notes help calibrate the exclusion criteria for non-health fields.

**E1 — Out of thematic scope (Business, IS, Engineering):** In management and IS research, papers often address multiple constructs simultaneously. A paper should be excluded on E1 grounds only when the phenomenon of interest is mentioned in passing (for example, in a single sentence in the introduction) and the paper's central contribution is clearly to a different construct. If the phenomenon appears in the research questions, hypotheses, or main findings, the paper should be retained.

**E2 — Inadequate publication type (all fields):** Conference papers in computer science and engineering are peer-reviewed and may carry equivalent weight to journal articles in those fields. Do not apply E2 to conference papers in CS/engineering unless the conference is clearly non-peer-reviewed (e.g., workshop abstracts, extended abstracts, or poster-only submissions).

**E3 — Divergent context or population (Business, IS):** Apply this criterion with care when the review scope is defined by a specific sector (e.g., SMEs, public sector, healthcare organizations). A paper studying large firms is not automatically excluded if it develops theory or measures that transfer to the review's target context. Flag as Uncertain rather than Exclude when transferability is plausible.

**E4 — Language scope:** If the review team includes multilingual members, consider whether the language exclusion is genuinely justified or whether it introduces geographic bias. Note any language exclusions explicitly in the Methods section of the final review manuscript.

**E5 — Full text inaccessible:** Before applying E5, attempt to retrieve the full text via DOI, Unpaywall, OpenAlex open access links, or institutional access. Apply E5 only when all retrieval attempts have failed.
