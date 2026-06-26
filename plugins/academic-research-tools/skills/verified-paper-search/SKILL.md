---
name: verified-paper-search
description: Find, verify, and synthesize academic literature for a topic or specific claim, actively minimizing citation hallucination through RAG principles. Use when someone asks to "find papers on X," wants a systematic/integrative literature review, needs a realist synthesis, or asks for citations to support an argument. This skill enforces a structured review protocol, teaches Boolean search strategy, ranks all sources by relevance, integrates journal quality assessment, and produces an evidence-grounded synthesis following systematic mapping and realist-informed synthesis best practices.
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

**Database-Specific Execution:**
- **OpenAlex:** Use structured API with field-specific syntax (e.g., `title:("social impact") AND abstract:(university)`). Note: OpenAlex supports Boolean logic.
- **Semantic Scholar:** Use for semantic/embedding matching rather than strict Boolean.
- **Google Scholar / Web Search:** Use for free-text search, recent preprints, or grey literature.

**Present all drafted Boolean strings to the user in a structured table before executing any search.** For each database, show the exact query string, the rationale for key term choices, and any synonyms or wildcards applied. Ask the user to confirm, adjust, or reject each string.

| Database | Boolean Query String | Key Term Rationale |
|---|---|---|
| OpenAlex | `("societal impact" OR "social impact") AND (universit* OR "higher education")` | Covers main concept variants and institutional synonyms |
| Semantic Scholar | `societal impact university evaluation` | Semantic matching; less strict syntax needed |
| Google Scholar | `"third mission" OR "knowledge transfer" AND university impact` | Captures grey literature and recent preprints |

**🛑 STOP: Present the Boolean strings to the user and wait for explicit approval (or requested adjustments) before executing any search. Document the final approved strings in the audit trail.**

### Step 4 — Search, Verify, and Assess Quality

Retrieve the papers and verify them before inclusion. Do not put a citation in the output that wasn't surfaced by a search performed *this turn*.

**1. Verify Reality:** Confirm via a second independent source (e.g., publisher page + citation index) that the title, authors, venue, and year actually match.
**2. Assess Relevance:** Read the abstract/metadata to score topical relevance:
   - **High (3):** Directly addresses research question; primary focus. (Candidate for synthesis)
   - **Medium (2):** Indirectly addresses question; secondary focus. (Supporting context)
   - **Low (1):** Tangentially related. (Exclude from synthesis)
**3. Assess Journal Quality (Integrated):** Do not run a separate skill. Evaluate the venue's credibility immediately:
   - Check indexing status (Scopus, Web of Science, SciELO, Redalyc, MEDLINE).
   - Flag predatory warning signs (rapid publication volume, single-editor review, no ethics code).
   - *Note: Venue credibility affects the weight of evidence, but is distinct from the individual paper's quality.*

### Step 5 — RAG-Based Synthesis

Conduct the synthesis using only the verified, high-relevance papers. Follow strict RAG (Retrieval-Augmented Generation) principles to avoid hallucination:

- **Grounding:** Every synthesized claim must be anchored to specific retrieved evidence. Never infer beyond what is explicitly stated in the sources.
- **Evidence Tracking:** Explicitly distinguish whether a claim is supported by the **full-text**, the **abstract**, or just **metadata**. Full-text evidence carries higher weight.
- **Synthesis Structure:** Organize findings according to the approved protocol (e.g., thematic mapping, or Context-Mechanism-Outcome configurations for realist synthesis).
- **Confidence Assessment:** Rate the strength of the synthesized findings (Strong = multiple full-text sources; Moderate = single full-text or multiple abstracts; Tentative = single abstract or conflicting findings).

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
*All sources sorted by relevance. Journal quality assessment is integrated here.*

| Cite Key | Title & Authors | Year | Venue & Quality Assessment | Relevance Score | Inclusion Decision |
|----------|-----------------|------|----------------------------|-----------------|--------------------|
| [Smith24] | Title... | 2024 | *Higher Ed* (Scopus-indexed) | High (3) | Included |
| [Jones23] | Title... | 2023 | *Predatory J* (High Risk) | High (3) | Excluded (Quality) |

## 4. Evidence Synthesis
*Synthesis of included papers based strictly on retrieved text, structured according to the selected review typology (e.g., thematic summary for integrative review, CMO configurations for realist review, or gap mapping for scoping review).*

### Theme / Mechanism / Finding 1: [Name]
- **Details:** [Relevant details based on review type, e.g., Context/Mechanism/Outcome for realist, or Key Concept for integrative]
- **Evidence Base:** [Synthesized narrative grounded in sources. E.g., "Smith (2024) found X based on full-text analysis, while Doe (2022) suggested Y in their abstract."]
- **Evidence Strength:** [Strong / Moderate / Tentative] (Based on full-text availability and consensus)

*(Repeat for other themes/findings)*

## 5. Notes & Limitations
- [Coverage gaps, methodological limitations of the review, papers that couldn't be fully verified or accessed]
```

## See Also
- `references/risk_checklist.md` for hallucination failure modes.
- `references/search_apis.md` for OpenAlex/Semantic Scholar commands.
- `journal-quality-check` — For deep-dive criteria on specific indexers if a venue's status is highly contested.
- `scientific-reference-reviewer` — For strict, claim-by-claim audits of specific sentences.
