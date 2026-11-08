---
name: verified-paper-search
description: Retrieve and verify academic-paper metadata for a topic through OpenAlex first, with a bounded five-minute failure-recovery window, anonymous Semantic Scholar bulk-search fallback, and user-supplied Semantic Scholar API-key fallback only when anonymous access fails. Enforces a researcher-approved Boolean strategy, optional PRISMA or SPAR-4-SLR protocol structure, researcher-controlled corpus-size consultation, preliminary triage that never replaces screening, DOI spot-checking, and auditable candidate-corpus export. Optional snowballing is restricted to researcher-approved scoping or realist-informed reviews after initial screening. Journal quality, final eligibility, appraisal, bibliometrics, and synthesis occur in separate skills.
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

# Verified Paper Search & Candidate-Corpus Retrieval

## The Problem This Solves

Language models can generate citations that look real for papers that were never written. This skill mitigates citation hallucination by making each search action explicit, checkable, and grounded in retrieved metadata. It produces an auditable **candidate corpus**, not a final included corpus and not a synthesis. Journal quality assessment, screening, methodological appraisal, bibliometrics, and deep synthesis occur in separate downstream skills.

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

### Step 1B — Select Review-Conduct and Reporting Protocol (User Selection Required)

After the researcher selects a review typology, explain that the typology answers **what kind of review** will be conducted, while the protocol structures **how its process and results will be recorded**. They are complementary choices, not alternatives.

Ask the researcher to select one of the following:

| Option | Use in this pipeline | When to choose it |
|---|---|---|
| **Default audit structure** | Use the skill's existing protocol, query, corpus, and decision records. | Exploratory, critical, or bespoke reviews without a selected reporting framework. |
| **PRISMA 2020 and PRISMA-S** | Preserve query, source, deduplication, screening, and exclusion counts required for PRISMA-oriented reporting. | Systematic or scoping reviews that require conventional evidence-synthesis reporting. |
| **SPAR-4-SLR** | Structure records under Assembling, Arranging, and Assessing. Map Identification and Acquisition here, Organization across corpus records, Purification to `corpus-screening`, and Evaluation and Reporting to downstream skills. | Social-science, management, or information-systems reviews that require transparent conceptual organization and agenda-oriented reporting. |

Explain that **SPAR-4-SLR does not replace the selected review typology**. If the researcher chooses PRISMA 2020, do not create a flow diagram yet. Preserve the required counts here and generate the diagram only after `corpus-screening` supplies final screening counts. If the researcher chooses SPAR-4-SLR, do not claim that its later Evaluation or Reporting stages have been completed at search stage.

**🛑 STOP: Record the selected reporting protocol and wait for explicit confirmation before drafting the review protocol.**

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
- **Reporting / Conduct Protocol:** State the researcher-selected option and its current-stage obligations. For PRISMA 2020 and PRISMA-S, record search and record-flow fields. For SPAR-4-SLR, state the Identification and Acquisition decisions and the planned Organization, Purification, Evaluation, and Reporting responsibilities across downstream skills.
- **Corpus Boundary:** Use OpenAlex first. State the contingency order (OpenAlex → anonymous Semantic Scholar → Semantic Scholar with the researcher's individual API key), date ranges, language restrictions, and provider-specific search-field limitations. A fallback is not equivalent coverage of the same database. Ask the researcher to approve the fallback strategy alongside the primary strategy, or pause for approval when fallback becomes necessary.
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

**Execution Engine: OpenAlex first, bounded Semantic Scholar contingency**
Use **OpenAlex as the primary provider**. Use the **anonymous Semantic Scholar Academic Graph bulk-search API** only when OpenAlex cannot complete the pending operation under the availability rules in Step 4. If anonymous Semantic Scholar fails after bounded retries, ask for the researcher's individual Semantic Scholar API key and retry the same API with authentication. Do not request a key when anonymous access works.
- Use provider-documented request parameters. In OpenAlex, use `search`, or a scoped parameter such as `search.title` or `search.title_and_abstract`. Do not assume inline `title:(...)` and `abstract:(...)` are validated field selectors merely because a request returns HTTP 200.
- OpenAlex uses uppercase `AND`, `OR`, and `NOT`. Wildcards require the matching `.exact` search variant and at least three characters before the wildcard. Record the selected search scope and stemming mode.
- Semantic Scholar bulk search uses `+`, `|`, and `-` for conjunction, disjunction, and negation, with documented grouping, phrases, and prefix wildcards. Translate the Boolean structure, not individual words through blind string replacement. Its title/abstract coverage is not equivalent to OpenAlex's broad title/abstract/full-text/keyword search. Unsupported filters or query constructs require researcher approval of a documented adaptation, not silent removal.

**Before drafting Boolean strings, read `references/search_apis.md` for the current syntax, authentication, pagination, and fallback rules. Do not invent API syntax.**

**Present the drafted Boolean strings to the user in a structured table before executing any search.** Show the exact query string, the rationale for key term choices, and any synonyms or wildcards applied. Ask the user to confirm, adjust, or reject each string.

| Database | Boolean Query String | Key Term Rationale |
|---|---|---|
| OpenAlex, primary | `("societal impact" OR "social impact") AND (universit* OR "higher education")`, submitted with the approved `.exact` search parameter | Covers concept variants and institutional synonyms. Record the chosen searched fields. |
| Semantic Scholar, contingency only | `("societal impact" | "social impact") + (universit* | "higher education")` | Preserves the Boolean concept groups, but searches the different provider's title/abstract index. |

Show the exact API parameters and metadata filters as well as each query. A contingency row does not authorize executing both providers when OpenAlex works.

**🛑 STOP: Present the Boolean strings to the user and wait for explicit approval (or requested adjustments) before executing any search. Document the final approved strings in the audit trail. If only the primary strategy was approved, pause for approval of the translated Semantic Scholar strategy before executing fallback.**

### Step 4 — Retrieve, Manage Corpus Size, and Export

Before executing the search, read `references/risk_checklist.md` and keep it active in your context throughout this step.

**API availability and contingency (apply without changing researcher decisions):**

1. Start with OpenAlex. Use a real monotonic clock for a maximum **300-second continuous unsuccessful-operation window**, including request timeouts and retry waits. This is not a five-minute limit on the entire search. After a valid successful page, checkpoint the response and reset the window for the next pending operation. Never describe healthy, long-running retrieval as API failure simply because the overall search exceeds five minutes.
2. For connection failures, timeouts, HTTP 429, HTTP 5xx, or malformed success responses, use bounded backoff as detailed in `references/search_apis.md`. Do not allow a single request or sleep to exceed the remaining recovery window. When the pending OpenAlex operation still cannot succeed within 300 seconds, checkpoint all retrieved records and proceed to anonymous Semantic Scholar. A nonrecoverable authentication/permission refusal may trigger contingency sooner, after recording the actual cause and checking whether the response is still needed for completeness. A valid response with zero results is **not** an availability failure. HTTP 400/404/422 requires request/endpoint correction or researcher consultation, not a claim that the service is down.
3. Before the Semantic Scholar request, announce the fallback and its cause. Use the contingency query already approved in Step 3. If no contingency query was approved, or any construct/filter cannot be preserved, show the translated query and scope limitations and wait for approval. Keep every successful OpenAlex response. Semantic Scholar cannot finish an interrupted OpenAlex cursor or prove OpenAlex coverage complete.
4. Use `GET https://api.semanticscholar.org/graph/v1/paper/search/bulk` anonymously, paginate through every continuation token, and do not substitute the relevance endpoint or a top-N list. Do not add an `openAccessPdf` filter merely because the API is publicly accessible. Preserve the 150/500 consultation thresholds, all researcher approval gates, and the separation from screening, quality appraisal, and synthesis.
5. If anonymous Semantic Scholar still fails after at most three attempts or 60 seconds of recovery (whichever comes first), explain the actual error and ask whether the researcher wants to configure their **own Semantic Scholar API key** locally as `SEMANTIC_SCHOLAR_API_KEY`. Use `x-api-key` on the same approved request. Ask for no login password, email password, or unrelated credential. Never put the key in a query URL, transcript, report, CSV, repository, or debug output. Do not claim that a key repairs DNS/TLS failures, local network restrictions, or provider outages. Offer to stop with preserved partial output if the researcher has no key or declines.
6. If authenticated access also fails after the same bounded recovery policy, stop and report the incomplete operations, preserved record counts, and available options. Do not invent records, silently reduce scope, restart with a top-N target, or claim full retrieval. Log provider, anonymous/authenticated mode (never the key), sanitized error, attempted operation, timings, query/filters, page/cursor/token progress, and per-provider completeness status.

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

**4. Optional snowballing, limited to Scoping Review and Realist-Informed Synthesis:** Snowballing is available only when the researcher selected **Scoping Review** or **Realist-Informed Synthesis** in Step 1 and explicitly approves it in the draft protocol. It must begin **after** `corpus-screening` has produced a researcher-confirmed initial seed set. It is not an automatic expansion of the pre-screening search.

- **Backward snowballing:** Retrieve works referenced by each seed paper through its OpenAlex `referenced_works` metadata. If OpenAlex is unavailable under the same contingency policy and the researcher approved this provider adaptation, use the paginated Semantic Scholar `/paper/{paper_id}/references` endpoint. Record missing references and provider coverage limits. Do not infer or fabricate reference metadata.
- **Forward snowballing:** Retrieve works that cite each seed paper using OpenAlex citation metadata, or the paginated Semantic Scholar `/paper/{paper_id}/citations` endpoint under the same approved contingency policy. Bulk search does not supply complete citation/reference edges. Record the provider and retrieval date because citation links change over time.
- Deduplicate snowballed records against `openalex_all_retrieved.json` (or the combined `search_all_retrieved.json` if fallback occurred) and against prior snowballing rounds. Save new records to `/home/ubuntu/articles/snowballing_candidate_register.csv` with Seed_Paper, Direction, Iteration, OpenAlex_ID, Title, DOI, Retrieval_Date, and Duplicate_Status. If Semantic Scholar was used, append Provider and SemanticScholar_ID. Leave unavailable OpenAlex identifiers empty, never fabricate them.
- Send every newly discovered non-duplicate record to `corpus-screening`. Do not include it automatically. The researcher controls all eligibility decisions.
- At the end of each approved iteration, report the number retrieved, duplicates removed, records sent to screening, records screened as Include, and the researcher's decision to continue or stop. **Never declare theoretical saturation autonomously.**
- For all other review typologies, list snowballing as not selected, unless the researcher explicitly requests a separate methodologically justified process.

**5. Audit-preserving pipeline export (CRITICAL):** Save both of the following files:

- `/home/ubuntu/articles/openalex_all_retrieved.json` — every deduplicated record returned by the accepted search strategy, including records the researcher approved for obvious-exclusion removal.
- `/home/ubuntu/articles/openalex_candidate_corpus.json` — every record retained after any researcher-approved obvious exclusions. This is the search-stage candidate corpus, not a final included corpus.

Also save `/home/ubuntu/articles/search_triage_register.csv`, with one row per deduplicated record and the following fields: Title, Authors, Year, Venue, DOI, Query_Source, Triage_Status, Proposed_Criterion, Direct_Evidence, Researcher_Decision, and DOI_Verification_Status. If the approved protocol includes snowballing, also save `/home/ubuntu/articles/snowballing_candidate_register.csv` after each completed snowballing iteration.

**Fallback export compatibility:** When only OpenAlex was used, preserve the existing export names and behavior unchanged. When Semantic Scholar was used, keep the two `openalex_*.json` files as the OpenAlex-only portion (empty if no OpenAlex records were retrieved), explicitly label their completeness/subset status, and additionally write `/home/ubuntu/articles/search_all_retrieved.json` and `/home/ubuntu/articles/search_candidate_corpus.json` for the combined deduplicated records. Preserve each native source response and normalize only actually retrieved metadata according to `references/search_apis.md`. Append Provider, Provider_Record_ID, OpenAlex_ID, SemanticScholar_ID, Retrieval_Date, and Retrieval_Status to the existing `search_triage_register.csv`, which must cover the **entire combined corpus**. Keep all query/provider provenance when duplicates merge. Never convert a Semantic Scholar paperId into a fictional OpenAlex ID or invent unavailable abstracts, language, country, institution, or citation metadata.

`corpus-screening` uses this candidate corpus to make the researcher-controlled inclusion and exclusion decisions. **After fallback, explicitly hand off the combined `search_triage_register.csv`, an already supported screening input, rather than the OpenAlex-only JSON subset.** State that provider-specific bibliometric fields may be unavailable and must not be inferred. After screening, create the final analysis corpus for `bibliometric-scientometric-analysis` by retaining only papers that the researcher marked Include.

### Step 5 — Minimal Corpus Orientation (Metadata Only)

Produce only a concise orientation to the candidate corpus. This stage must not substitute for researcher-controlled screening, quality appraisal, bibliometric analysis, or deep synthesis.

Report the following:

- The number of records actually retrieved by each approved query and provider, provider-reported totals (approximate where applicable), fallback cause and mode, and per-provider retrieval completeness.
- The deduplicated total, the number proposed as clearly out of scope, the number of removals approved by the researcher, and the final candidate-corpus total.
- The year range, document-type distribution, language distribution when available, and the number of records with an abstract and DOI.
- The number of DOI records spot-checked and any DOI metadata flags.
- If snowballing was selected and completed, each iteration's retrieved, duplicate, screening-candidate, included, and researcher stop/continue counts. If it was not run, state why.
- A short statement that the output is a search-stage candidate corpus and that no final screening decision, journal-quality judgment, methodological quality appraisal, thematic synthesis, or full-text analysis has been performed.

Do **not** produce per-paper summaries, theme groupings, evidence-strength ratings, Context-Mechanism-Outcome configurations, literature gaps, conceptual claims, or flowing academic prose. Those activities belong to later skills after the researcher has selected the corpus.

### Step 6 — Produce the Deliverable

Default to a **Markdown file** unless the user requests a Word document (use the `docx` skill for Word). The deliverable must be structured as follows:

```markdown
# Literature Search Candidate Corpus: [Topic]

## 1. Approved Review Protocol
- **Review Question:** [PICOTS/SPIDER]
- **Scope and Boundaries:** [OpenAlex primary, approved Semantic Scholar contingency if used, searched fields, dates, languages, document-type rules]
- **Review Typology:** [The review type selected by the researcher]
- **Reporting / Conduct Protocol:** [Default audit structure / PRISMA 2020 and PRISMA-S / SPAR-4-SLR]
- **Protocol Mapping:** [For SPAR-4-SLR, identify this deliverable as Assembling: Identification and Acquisition, with Organization begun. For PRISMA, identify counts preserved for the later flow diagram.]
- **Downstream Plan:** [`journal-quality-check` → `corpus-screening` → `study-quality-assessment` where full texts are available]

## 2. Search Strategy and Execution
- **Approved Boolean Queries:** [List each exact query]
- **Query Counts:** [Actually retrieved per query/provider, provider-reported totals, and completeness]
- **API Availability and Fallback:** [Primary success / fallback cause, attempt timings, anonymous or authenticated Semantic Scholar, pending operations and preserved partial records. Never include keys.]
- **Deduplication:** [Number removed and deduplicated total]
- **Corpus-Size Decision:** [Researcher decision after the 150/500 consultation, if applicable]
- **Approved Refinements or Metadata Filters:** [Exact changes, or "None"]
- **Snowballing Plan and Status:** [Not selected / Approved for Scoping or Realist-Informed Review after screening / Completed iterations with counts]

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
- **If fallback occurred:** The two `openalex_*.json` files contain only the OpenAlex portion. The combined audit/candidate exports are `search_all_retrieved.json` and `search_candidate_corpus.json`. Use the combined triage CSV for screening.

## 4. Minimal Corpus Orientation
- **Retrieved and deduplicated totals:** [Counts]
- **Candidate-corpus total:** [Count]
- **Proposed and researcher-approved obvious exclusions:** [Counts and criteria]
- **Year range, document types, and languages:** [Metadata profile]
- **Abstract and DOI coverage:** [Counts]
- **DOI spot-check:** [Number checked and metadata flags]
- **Snowballing:** [Status, iteration counts, or not selected]

*No final screening decision, journal-quality judgment, methodological quality appraisal, full-text analysis, thematic synthesis, evidence-strength rating, or literature-gap analysis has been performed at this stage. A PRISMA diagram is generated after screening, not at this stage. SPAR-4-SLR Purification, Evaluation, and Reporting remain downstream.*

## 5. Notes and Limitations
- [Any search coverage constraints, provider changes, incomplete provider operations, unsupported filter adaptations approved by the researcher, unresolved metadata, snowballing status, and reporting-protocol limitations]
- *The output is a search-stage candidate corpus. The researcher must use `corpus-screening` to make final inclusion and exclusion decisions before any downstream analysis.*
```

## Next Steps in Pipeline
- **`journal-quality-check`** — Assess journal/source credibility separately. Do not retroactively treat its output as a substitute for researcher-led eligibility screening.
- **`corpus-screening`** — Make final title/abstract inclusion and exclusion decisions using the candidate corpus and the researcher-approved criteria. This is the required next step before analysis. It produces SPAR-4-SLR Purification outputs when SPAR is selected and PRISMA flow-diagram counts when PRISMA is selected.
- **Optional return to `verified-paper-search` for snowballing** — Only after a researcher-confirmed seed set exists, only for Scoping Review or Realist-Informed Synthesis, and only when the researcher approved snowballing in the protocol.
- **`study-quality-assessment`** — After screening and only when full texts are available, appraise the methodological quality of the researcher-included papers.
- **`bibliometric-scientometric-analysis`** — After final screening, generate visual science mapping and related analyses from the researcher-included corpus.
- **`deep-academic-synthesis`** — After final screening and when full texts are available, move to researcher-controlled, section-by-section synthesis.

## See Also
- `references/risk_checklist.md` for hallucination failure modes.
- `references/search_apis.md` for OpenAlex-first retrieval, Semantic Scholar contingency, authentication, and pagination.
- `journal-quality-check` — For deep-dive criteria on specific indexers if a venue's status is highly contested.
- `scientific-reference-reviewer` — For strict, claim-by-claim audits of specific sentences.
