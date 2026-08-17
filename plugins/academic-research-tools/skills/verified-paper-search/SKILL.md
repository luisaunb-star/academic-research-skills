---
name: verified-paper-search
description: Find and verify academic papers for a topic or specific claim via the OpenAlex API, minimizing citation hallucination through RAG principles. Enforces a structured review protocol, researcher-approved Boolean search strategy, user-controlled large-corpus consultation at 150 and 500 records, preliminary topical triage that does not replace screening, DOI spot-checking, and auditable OpenAlex candidate-corpus export. Journal quality assessment is handled by `journal-quality-check`, final inclusion/exclusion by `corpus-screening`, and deep synthesis by `deep-academic-synthesis`.
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

# Verified Paper Search & Integrative Synthesis

## The Problem This Solves

Language models are fluent enough to generate citations that look completely real for papers that were never written. This skill mitigates citation hallucination by making every step explicit, checkable, and grounded in retrieved evidence (Retrieval-Augmented Generation / RAG principles). Furthermore, it upgrades a simple "list of papers" into a structured **systematic mapping and realist-informed synthesis**, ensuring the final deliverable is methodologically rigorous, transparent, and aligned with academic review standards.

## Workflow

### Step 1 — Select Review Typology (User Selection Required)

Before initiating any literature search or drafting a protocol, you must explicitly ask the user to select the type of review to be conducted. This decision dictates the inclusion criteria, search exhaustiveness, quality appraisal requirements, and synthesis methods.

Present the following options to the user, grounded in academic literature (e.g., Paré et al., 2015; Whittemore & Knafl, 2005; Pawson et al., 2005), and explain the methodological differences:

**1. Systematic Review**
* **Goal:** To aggregate, critically appraise, and synthesize all empirical evidence that meets pre-specified eligibility criteria to answer a narrow, clearly formulated research question.
* **Methodology:** Requires exhaustive literature search, strict *a priori* inclusion/exclusion criteria, and formal quality/risk-of-bias assessment using validated instruments.
* **Synthesis:** Quantitative (meta-analysis) or qualitative (narrative synthesis, vote counting).

**2. Scoping Review**
* **Goal:** To provide an initial indication of the potential size and scope of extant literature, identify knowledge gaps, or determine the value of undertaking a full systematic review.
* **Methodology:** Comprehensive search using an iterative process. Uses explicit inclusion/exclusion criteria but typically **does not require** formal quality or risk-of-bias assessment.
* **Synthesis:** Tabular or graphical mapping of the extent, nature, and distribution of studies, accompanied by a narrative summary.

**3. Integrative Review**
* **Goal:** To summarize past empirical and theoretical literature to provide a more comprehensive understanding of a particular phenomenon. Allows simultaneous inclusion of diverse methodologies (experimental and non-experimental).
* **Methodology:** Comprehensive search with a specific focus. Quality appraisal is complex due to diverse sources and may require different instruments for different study designs.
* **Synthesis:** Data reduction, display, comparison, and conclusion drawing, often using qualitative data analysis methods.

**4. Realist-Informed Synthesis (Realist Review)**
* **Goal:** To unpack the mechanisms of how complex programs or interventions work (or why they fail) in particular contexts. Answers: "What works, for whom, under what circumstances?"
* **Methodology:** Theory-driven and interpretative. Search and appraisal are purposive and iterative, aiming for theoretical saturation. Quality is judged by relevance and rigor to theory building.
* **Synthesis:** Focuses on identifying and explaining Context-Mechanism-Outcome (CMO) configurations.

**5. Critical Review**
* **Goal:** To provide a critical evaluation and interpretive analysis of existing literature to reveal strengths, weaknesses, contradictions, controversies, or inconsistencies.
* **Methodology:** Seeks a representative (rather than exhaustive) sample. Typically does not require formal quality assessment of primary studies, focusing instead on conceptual contribution.
* **Synthesis:** Narrative, often conceptual or chronological, aiming to derive new theory or hypothesis.

**🛑 STOP: Present this typology to the user. Do not proceed until the user explicitly selects a review type. The selected type will govern the rules for the Draft Review Protocol in Step 2.**

### Step 2 — Diagnose Risk & Draft Review Protocol (User Approval Required)

Before searching, you must establish a rigorous framework for the review. Do not jump straight to executing searches.

**1. Diagnose the Request:**
- **Topic vs. claim:** Is the user exploring a topic or validating a specific statement?
- **Terminology overlap:** Do terms mean different things in different fields (e.g., "agile" in management vs. engineering)?

**2. Draft the Review Protocol:**
Based on the user's topic and the **selected review typology** from Step 1, draft a working protocol. Present this protocol to the user and **ask for approval** before proceeding.

The draft protocol must align with the chosen typology and include:
- **Review Purpose & Question:** Clarified using PICOTS (Population, Intervention, Context, Outcome, Time, Study design) or SPIDER framework.
- **Review Design:** Tailored to the selected typology (e.g., if Scoping Review, focus on mapping; if Realist-Informed Synthesis, focus on CMO configurations).
- **Corpus Boundary:** Databases to search, date ranges, language restrictions.
- **Unit of Analysis:** The paper, or specific claims/passages within the paper.
- **Search-Stage Extraction Fields:** Define metadata and audit fields only (e.g., title, authors, year, venue, DOI, abstract availability, document type, query source, and preliminary triage status). Do not define theoretical, methodological, evidence-strength, or synthesis fields here. Those belong to downstream stages after researcher-controlled screening.
- **Downstream Appraisal Plan:** State that journal/source credibility will be assessed later with `journal-quality-check`, title/abstract eligibility decisions will be made by the researcher in `corpus-screening`, and methodological quality appraisal will be conducted later with `study-quality-assessment` when full texts are available.

**🛑 STOP: Present the draft protocol and wait for user approval before continuing.**

### Step 3 — Decompose & Optimize the Boolean Search Strategy

Once the protocol is approved, translate the research question into an explicit Boolean search strategy. 

**Teach and apply Boolean principles:**
- **AND:** Narrows results (e.g., `"societal impact" AND university`).
- **OR:** Broadens results with synonyms (e.g., `("societal impact" OR "social impact" OR "third mission")`).
- **NOT:** Excludes off-target results (e.g., `university NOT clinical`).
- **Phrase matching:** Use quotation marks for exact phrases.
- **Wildcards:** Use asterisks for variations (e.g., `evaluat*`).

**Execution Engine: OpenAlex API**
To ensure structured, reproducible metadata that flows into downstream bibliometric tools, this skill exclusively uses the **OpenAlex API** for retrieval.
- Use structured API with field-specific syntax (e.g., `title:("social impact") AND abstract:(university)`).
- OpenAlex fully supports Boolean logic, wildcards, and exact phrase matching.

**Before drafting Boolean strings, read `references/search_apis.md` for the correct OpenAlex API syntax. Do not rely on web searches or internal knowledge for API syntax.**

**Present the drafted Boolean strings to the user in a structured table before executing any search.** Show the exact query string, the rationale for key term choices, and any synonyms or wildcards applied. Ask the user to confirm, adjust, or reject each string.

| Database | Boolean Query String | Key Term Rationale |
|---|---|---|
| OpenAlex | `("societal impact" OR "social impact") AND (universit* OR "higher education")` | Covers main concept variants and institutional synonyms |

**🛑 STOP: Present the Boolean strings to the user and wait for explicit approval (or requested adjustments) before executing any search. Document the final approved strings in the audit trail.**

### Step 4 — Retrieve, Manage Corpus Size, and Export

Before executing the search, read `references/risk_checklist.md` and keep it active in your context throughout this step.

**0. Retrieval Exhaustiveness and Researcher Control (CRITICAL):** Retrieve the complete result set for each approved Boolean query and deduplicate records across queries. Report the number returned by each query and the total after deduplication. The **150-record threshold is a prompt for researcher consultation, not a target corpus size**.

- For **150 or fewer records**, retain every deduplicated record for preliminary topical triage and later researcher-controlled screening.
- For **151 to 500 records**, PAUSE before changing the search or removing any record. Tell the researcher that the corpus may be burdensome to screen and ask them to choose one of the following options: (a) retain the entire corpus for screening, (b) approve one or more proposed Boolean refinements, or (c) apply researcher-selected metadata filters such as date range, language, document type, country, subject area, or open-access status.
- For **more than 500 records**, PAUSE before individual-record filtering. State the total count and explain that screening the unrefined corpus may be burdensome. Present the same three options. Do not impose a retrieval cap, alter a Boolean string, apply a metadata filter, or remove records unless the researcher explicitly approves that action.
- When proposing refinements, present them in a table with the exact revised Boolean string or metadata filter, the expected narrowing logic, and the possible scope cost. Wait for approval before re-running any search.
- **Never aim for, retrieve only, rank to, or stop at 50, 80, 100, 150, or any other arbitrary top-N count unless the researcher explicitly instructs you to do so.** Never silently cap, prioritize, or discard records because of token limits, time constraints, citation count, or model convenience.
- If the researcher accepts a corpus larger than 150 records, retain and export the full accepted corpus. The size itself is not a reason to exclude records.

**1. Preliminary Topical Triage (not screening):** This step supports later screening. It does not make final inclusion or exclusion decisions.

Classify each record using title, abstract, and metadata only:

| Triage status | Meaning | Action at this stage |
|---|---|---|
| Direct candidate | The central phenomenon appears to be a primary focus. | Retain for `corpus-screening`. |
| Potential candidate | The record may address the question but relevance is ambiguous, secondary, or context-dependent. | Retain for `corpus-screening`. |
| Insufficient metadata | Title, abstract, or metadata is insufficient for a defensible preliminary reading. | Retain for `corpus-screening` and flag the missing information. |
| Clearly out of scope (proposed) | A pre-approved exclusion criterion is directly evidenced in the title, abstract, or metadata. | Do not remove yet. Add to the Obvious Exclusions Register for researcher confirmation. |

- Never use preliminary topical triage as an inclusion decision.
- Never classify a record as clearly out of scope because it has low citations, an unfamiliar venue, missing full text, or a sparse abstract.
- The only records that may be proposed for removal are clearly out-of-scope records that meet a **pre-approved** criterion with direct evidence. For each such record, quote the relevant title, abstract, or metadata phrase and state the criterion code.
- Present the complete **Obvious Exclusions Register** to the researcher and wait for their decision before removing any record. Records not explicitly approved for removal must remain in the candidate corpus.

| Record | Proposed status | Approved criterion | Direct evidence | Researcher decision |
|---|---|---|---|---|
| [Author, Year, Title] | Clearly out of scope | E1 | "[exact phrase]" | Approve removal / Retain |

**2. Journal quality — do not assess here.** Record the venue name only. Do not evaluate indexing status, quartile, peer-review status, or predatory risk. Do not mark any paper as "Excluded (Quality)" at this stage. Those assessments belong to `journal-quality-check`, which runs separately in the pipeline.

**3. DOI metadata spot-check:** If at least three records contain DOIs, randomly select 3 to 5 records across the retained corpus and resolve each DOI through `https://doi.org/{doi}`. If a DOI fails to resolve, record "DOI unverified" in the mapping and report it to the researcher. A failed DOI check is a metadata flag, not a basis for exclusion at this stage.

**4. Snowballing is out of scope for this skill.** Forward snowballing (finding papers that cite the candidate corpus) and backward snowballing (checking reference lists) are not part of this search step. If the chosen review typology requires snowballing, list it as a limitation in the deliverable and conduct it as a separate pass after `corpus-screening`.

**5. Audit-preserving pipeline export (CRITICAL):** Save both of the following files:

- `/home/ubuntu/articles/openalex_all_retrieved.json` — every deduplicated record returned by the accepted search strategy, including records the researcher approved for obvious-exclusion removal.
- `/home/ubuntu/articles/openalex_candidate_corpus.json` — every record retained after any researcher-approved obvious exclusions. This is the search-stage candidate corpus, not a final included corpus.

Also save `/home/ubuntu/articles/search_triage_register.csv`, with one row per deduplicated record and the following fields: Title, Authors, Year, Venue, DOI, Query_Source, Triage_Status, Proposed_Criterion, Direct_Evidence, Researcher_Decision, and DOI_Verification_Status.

`corpus-screening` uses this candidate corpus to make the researcher-controlled inclusion and exclusion decisions. After screening, create the final analysis corpus for `bibliometric-scientometric-analysis` by retaining only papers that the researcher marked Include.

### Step 5 — Minimal Corpus Orientation (Metadata Only)

Produce only a concise orientation to the candidate corpus. This stage must not substitute for researcher-controlled screening, quality appraisal, bibliometric analysis, or deep synthesis.

Report the following:

- The number of records returned by each approved query.
- The deduplicated total, the number proposed as clearly out of scope, the number of removals approved by the researcher, and the final candidate-corpus total.
- The year range, document-type distribution, language distribution when available, and the number of records with an abstract and DOI.
- The number of DOI records spot-checked and any DOI metadata flags.
- A short statement that the output is a search-stage candidate corpus and that no final screening decision, journal-quality judgment, methodological quality appraisal, thematic synthesis, or full-text analysis has been performed.

Do **not** produce per-paper summaries, theme groupings, evidence-strength ratings, Context-Mechanism-Outcome configurations, literature gaps, conceptual claims, or flowing academic prose. Those activities belong to later skills after the researcher has selected the corpus.

### Step 6 — Produce the Deliverable

Default to a **Markdown file** unless the user requests a Word document (use the `docx` skill for Word). The deliverable must be structured as follows:

```markdown
# Literature Search Candidate Corpus: [Topic]

## 1. Approved Review Protocol
- **Review Question:** [PICOTS/SPIDER]
- **Scope and Boundaries:** [OpenAlex, dates, languages, document-type rules]
- **Review Typology:** [The review type selected by the researcher]
- **Downstream Plan:** [`journal-quality-check` → `corpus-screening` → `study-quality-assessment` where full texts are available]

## 2. Search Strategy and Execution
- **Approved Boolean Queries:** [List each exact query]
- **Query Counts:** [Records returned by each query]
- **Deduplication:** [Number removed and deduplicated total]
- **Corpus-Size Decision:** [Researcher decision after the 150/500 consultation, if applicable]
- **Approved Refinements or Metadata Filters:** [Exact changes, or "None"]

## 3. Candidate-Corpus Register
*This is not a final included corpus. It records preliminary topical triage only. Journal quality is assessed separately in `journal-quality-check`; final title/abstract inclusion and exclusion decisions are made by the researcher in `corpus-screening`.*

| Cite Key | Title and Authors | Year | Venue | DOI | Preliminary Triage Status | Direct Evidence or Metadata Note | Researcher Decision |
|---|---|---|---|---|---|---|---|
| [Smith24] | Title... | 2024 | Higher Education | 10.xxxx/xxxx | Direct candidate | Abstract addresses [phenomenon] as the study's stated aim | Retained for screening |
| [Jones23] | Title... | 2023 | Journal of X | 10.xxxx/xxxx | Clearly out of scope (proposed) | E1: "[exact title/abstract phrase]" | Pending researcher confirmation |
| [Brown22] | Title... | 2022 | Journal of Y | DOI unverified | Insufficient metadata | Abstract unavailable; DOI spot-check did not resolve | Retained for screening |

- **Full audit export:** `/home/ubuntu/articles/openalex_all_retrieved.json`
- **Candidate-corpus export:** `/home/ubuntu/articles/openalex_candidate_corpus.json`
- **Triage register:** `/home/ubuntu/articles/search_triage_register.csv`

## 4. Minimal Corpus Orientation
- **Retrieved and deduplicated totals:** [Counts]
- **Candidate-corpus total:** [Count]
- **Proposed and researcher-approved obvious exclusions:** [Counts and criteria]
- **Year range, document types, and languages:** [Metadata profile]
- **Abstract and DOI coverage:** [Counts]
- **DOI spot-check:** [Number checked and metadata flags]

*No final screening decision, journal-quality judgment, methodological quality appraisal, full-text analysis, thematic synthesis, evidence-strength rating, or literature-gap analysis has been performed at this stage.*

## 5. Notes and Limitations
- [Any search coverage constraints, unresolved metadata, and any required snowballing pass]
- *The output is a search-stage candidate corpus. The researcher must use `corpus-screening` to make final inclusion and exclusion decisions before any downstream analysis.*
```

## Next Steps in Pipeline
- **`journal-quality-check`** — Assess journal/source credibility separately. Do not retroactively treat its output as a substitute for researcher-led eligibility screening.
- **`corpus-screening`** — Make final title/abstract inclusion and exclusion decisions using the candidate corpus and the researcher-approved criteria. This is the required next step before analysis.
- **`study-quality-assessment`** — After screening and only when full texts are available, appraise the methodological quality of the researcher-included papers.
- **`bibliometric-scientometric-analysis`** — After final screening, generate visual science mapping and related analyses from the researcher-included corpus.
- **`deep-academic-synthesis`** — After final screening and when full texts are available, move to researcher-controlled, section-by-section synthesis.

## See Also
- `references/risk_checklist.md` for hallucination failure modes.
- `references/search_apis.md` for OpenAlex API commands.
- `journal-quality-check` — For deep-dive criteria on specific indexers if a venue's status is highly contested.
- `scientific-reference-reviewer` — For strict, claim-by-claim audits of specific sentences.
