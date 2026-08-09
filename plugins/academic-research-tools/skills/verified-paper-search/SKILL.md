---
name: verified-paper-search
description: Find and verify academic papers for a topic or specific claim via the OpenAlex API, minimizing citation hallucination through RAG principles. Enforces a structured review protocol, Boolean search strategy with user approval, corpus size management (refinement loop if >150 records), relevance scoring, DOI spot-check, mandatory OpenAlex JSON export for downstream bibliometric analysis, and a brief abstract-level preliminary summary. Journal quality assessment is handled by `journal-quality-check`. Deep academic synthesis is handled by `deep-academic-synthesis`.
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
- **Review Design:** Tailored to the selected typology (e.g., if Scopus Review, focus on mapping; if Realist, focus on CMO configurations).
- **Corpus Boundary:** Databases to search, date ranges, language restrictions.
- **Unit of Analysis:** The paper, or specific claims/passages within the paper.
- **Extraction Fields:** Define what will be extracted (e.g., year, country, paper type, evaluation format, indicator approach, context, mechanism, outcome, evidence strength).
- **Quality & Rigor Approach:** Define how sources will be appraised (e.g., MMAT for empirical, RAMESES logic for realist evidence).

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

### Step 4 — Search, Filter, and Export

Before executing the search, read `references/risk_checklist.md` and keep it active in your context throughout this step.

**0. Retrieval Exhaustiveness and Corpus Size Management (CRITICAL — Do Not Apply Arbitrary Cutoffs):**
Retrieve the full result set for each approved Boolean query. Report the total number of records returned by each query before screening begins. After deduplication across all queries, check the total corpus size.

- If the deduplicated total is **150 records or fewer**, proceed directly to relevance scoring.
- If the deduplicated total **exceeds 150 records**, do NOT silently cut. Instead, propose Boolean refinements to the user (narrower synonyms, additional AND terms, tighter date range, document type filter) and present them in a table with rationale. Ask the user to approve the refinements before re-running the search. Repeat until the corpus is 150 records or fewer, or until the user explicitly accepts a larger corpus and instructs you to proceed.
- Never apply a silent top-N cutoff. Any practical limit must be explicitly stated to the user and recorded in the Search Strategy section of the deliverable.

**1. Assess Relevance:** Read the abstract/metadata to score topical relevance:
   - **High (3):** Directly addresses research question; primary focus. (Candidate for corpus)
   - **Medium (2):** Indirectly addresses question; secondary focus. (Supporting context)
   - **Low (1):** Tangentially related. (Exclude from corpus)

**2. Journal quality — do not assess here.** Record the venue name in the mapping table but do not evaluate indexing status, quartile, or predatory risk. That assessment is the role of `journal-quality-check`, which runs after this skill in the pipeline. Do not mark any paper as "Excluded (Quality)" at this stage.

**3. DOI spot-check:** After relevance scoring, randomly select 3 to 5 papers from the High-relevance group and verify their DOIs by resolving `https://doi.org/{doi}`. If any DOI fails to resolve, flag the paper as "DOI unverified" in the mapping table and report it to the user before exporting.

**4. Snowballing is out of scope for this skill.** Forward snowballing (finding papers that cite your corpus) and backward snowballing (checking reference lists of included papers) are not part of this search step. If the review typology requires snowballing (e.g., systematic review), note it as a limitation in Section 5 of the deliverable and conduct it as a separate manual pass after corpus screening.

**5. Pipeline Export (CRITICAL):** Once the final list of included papers is determined (High and Medium relevance), you MUST save the raw OpenAlex JSON data for those papers to a local file (`/home/ubuntu/articles/openalex_corpus.json`). This JSON file is the required input for `bibliometric-scientometric-analysis`.

### Step 5 — Preliminary Summary (Brief, Abstract-Level Only)

Produce a short, factual summary of the included papers. This is **not** a deep academic synthesis. Its purpose is to give the researcher a quick orientation to the corpus before moving to the next stage of the pipeline.

- Write **one or two sentences per included paper**, drawn strictly from the abstract and metadata. Do not infer, interpret, or elaborate beyond what the abstract states.
- Group papers by the main themes or concepts that emerge naturally from the titles and abstracts.
- Flag any papers where the abstract is absent or too sparse to summarize.
- **Do not** write flowing academic prose, thematic arguments, or theoretical interpretations here. That work belongs in `deep-academic-synthesis`.
- End the summary with a brief note on the most prominent gaps or patterns visible from the corpus at abstract level.

### Step 6 — Produce the Deliverable

Default to a **Markdown file** unless the user requests a Word document (use the `docx` skill for Word). The deliverable must be structured as follows:

```markdown
# Integrative Literature Review: [Topic]

## 1. Approved Review Protocol
- **Review Question:** [PICOTS/SPIDER]
- **Scope & Boundaries:** [Databases, dates, languages]
- **Methodology:** [The specific review typology selected by the user in Step 1]

## 2. Search Strategy & Execution
- **Boolean Queries:** [List exact queries used per database]
- **Execution Summary:** [Total retrieved, total verified, total excluded]

## 3. Systematic Mapping (All Retrieved Sources)
*All sources sorted by relevance score. Journal quality assessment is conducted separately in `journal-quality-check`.*

| Cite Key | Title and Authors | Year | Venue | DOI | Relevance Score | Inclusion Decision |
|---|---|---|---|---|---|---|
| [Smith24] | Title... | 2024 | Higher Education | 10.xxxx/xxxx | High (3) | Included |
| [Jones23] | Title... | 2023 | Journal of X | 10.xxxx/xxxx | Low (1) | Excluded (Relevance) |
| [Brown22] | Title... | 2022 | Journal of Y | DOI unverified | High (3) | Included (DOI unverified — flag for user) |

## 4. Preliminary Summary (Abstract-Level)
*One to two sentences per included paper, grouped by emerging theme. This is not a deep synthesis. For full academic synthesis, proceed to `deep-academic-synthesis`.*

### [Theme / Concept Group Name]
- **[Cite Key]** [Author(s), Year]: [One to two factual sentences drawn strictly from the abstract.]

*(Repeat for all included papers, grouped by theme)*

**Patterns and gaps visible at abstract level:** [Brief note on what the corpus seems to converge on, and where obvious gaps exist.]

## 5. Notes & Limitations
- [Coverage gaps, methodological limitations of the review, papers that couldn't be fully verified or accessed]
- *Note: The preliminary summary above is grounded in abstracts only. Deep thematic analysis, theoretical interpretation, and academic prose synthesis should be conducted using the `deep-academic-synthesis` skill.*
```

## Next Steps in Pipeline
- **`bibliometric-scientometric-analysis`** — To generate visual science mapping, co-authorship networks, and citation trajectory plots using the OpenAlex JSON exported in Step 4.
- **`deep-academic-synthesis`** — If the user has full texts available and wants to move from abstract-level mapping to deep, section-by-section academic synthesis.

## See Also
- `references/risk_checklist.md` for hallucination failure modes.
- `references/search_apis.md` for OpenAlex API commands.
- `journal-quality-check` — For deep-dive criteria on specific indexers if a venue's status is highly contested.
- `scientific-reference-reviewer` — For strict, claim-by-claim audits of specific sentences.
