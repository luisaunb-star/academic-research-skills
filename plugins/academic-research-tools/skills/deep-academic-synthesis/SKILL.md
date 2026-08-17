---
name: deep-academic-synthesis
description: Synthesize academic literature in depth, grounded strictly in retrieved texts, with the human researcher in control of the intellectual architecture. Uses Corpus Overview, Thematic Agenda Setting, and Incremental Prose Generation. Enforces direct quotation, claim-level verification, Popay-informed narrative-synthesis options, semantic provenance mapping, and explicit uncertainty controls to reduce factual, logical, and contextual hallucination.
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

# Deep Academic Synthesis

## The Problem This Solves

When an AI produces a complete synthesis in one shot, the researcher's role collapses from active synthesist to passive reviewer. The intellectual work of deciding which themes matter, how findings relate, and what the argument should be gets delegated, resulting in cognitively outsourced writing that may be technically correct but epistemologically hollow.

This skill continues the pipeline after researcher-controlled screening. It shifts from candidate-corpus metadata and abstracts to full-text evidence, while keeping the human researcher in control of the intellectual architecture through a three-stage, interactive process. It does not treat the search-stage orientation as a synthesis or as evidence beyond the retrieved records.

---

## Anti-Hallucination Mode (CRITICAL — All Constraints Active Simultaneously)

These three rules are always active. They cannot be suspended, relaxed, or traded off against each other. If any one of them cannot be satisfied for a given claim, the claim must not appear in the synthesis.

### Rule 1 — Say "I Don't Know"

If you do not have a credible source for a claim, say so. Do not guess. Do not infer. Do not fill gaps with plausible-sounding reasoning. "I do not have data on this in the provided corpus" is always a valid and required answer when the evidence is absent.

This applies to:
- Causal claims ("X causes Y") that are not explicitly stated in the source.
- Generalizations that go beyond the scope of the studies in the corpus.
- Contextual background that was not retrieved as part of the corpus.
- Any claim about a paper's findings that is not directly supported by the extracted text or abstract.

### Rule 2 — Cite Every Claim

Every recommendation, finding, or interpretive statement must be anchored to one of the following:
- A specific passage extracted from a file in the current corpus (with file name and page or section reference).
- An abstract retrieved from OpenAlex (with the paper's DOI or OpenAlex ID).
- A named author, paper title, and year.

If you generate a claim during drafting and cannot immediately identify a supporting source from the corpus, you must retract it before presenting the text. Do not present unsupported claims and then add a caveat. Remove them entirely.

### Rule 3 — Quote Before Analyzing

When working from documents (Mode B, full-text), extract the actual text first before analyzing it. Ground every analytical statement in a word-for-word quotation from the source. Reference the quote explicitly when making your point.

The required pattern is:

> [Author, Year, p. X] states: "exact quoted text."
> This indicates that [your analytical point, directly derived from the quote].

Do not paraphrase a source and then analyze the paraphrase. The quote must come first. Paraphrase is permitted only as a supplement to a direct quote, never as a replacement for it.

In Mode A (abstract-only), direct quotation from abstracts is required in the same way. Tag every such quote with `[Abstract only]`.

### Rule 4 — Match the Control to the Hallucination Risk

Use observable controls rather than claiming access to the model's internal reasoning.

| Risk | Required control |
|---|---|
| **Factual** | Retrieve the relevant corpus passage, quote it, preserve the source location, and state uncertainty when the passage is absent. |
| **Logical** | For comparative, causal, theoretical, or multi-study claims, use the Claim Verification Ledger before drafting. |
| **Contextual** | Build and refresh a section-aware evidence map. Do not aggregate across documents or sections when the provenance record is incomplete. |

Retrieval, prompting, and verification are **governance controls**. They make evidence trails inspectable. They do not prove that an AI reasoning trace exposes internal cognition.

---

## Language and Stylistic Constraints (CRITICAL)

When writing the synthesis, you **MUST strictly adhere** to the following linguistic constraints. Failure to do so compromises the academic integrity of the output.

1. **Cohesive Paragraph Structure:** Use the MEAL plan (Main idea, Evidence, Analysis, Lead out) or SEED plan (Statement, Expand, Evidence, Discussion). Use varied connectives to ensure fluid transitions between paragraphs.
2. **No Vague/Promotional Adjectives:** Completely avoid: comprehensive, adept, lively, crucial, dynamic, disruptive, effective, efficient, exciting, engaging, essential, strategic, exemplary, fascinating, fundamental, imperative, invaluable, innovative, inspiring, thought-provoking, praiseworthy, meticulous, thorough, multifaceted, powerful, renowned, revolutionary, robust, significant, synergistic, transformative, unique, valuable, vibrant, vital, rich (figurative), profound (metaphorical), impressive, extraordinary, exceptional, notable, brilliant, captivating, spectacular, grand, magnificent, majestic, monumental, matchless, perfect, solid, superior.
3. **No Artificial Copulas:** Never replace "is/are/was/were/has/had" with elaborate constructions. **Prohibited:** "serves as," "acts as," "remains as," "marks a moment," "represents a milestone," "possesses," "presents," "offers" (when "has" suffices), "stands out as." **Prefer:** is, are, was, were, has, had.
4. **No Negative Parallelisms:** Avoid: "Not only X, but also Y," "It is not about X, it is about Y," "Without X, without Y, only Z."
5. **Punctuation:** **Prohibited:** em-dash (—), semicolon (;), colon (:) except in formal lists, curly quotes. **Use:** commas, periods, parentheses, straight quotes. Avoid long, convoluted clauses.

---

## Workflow

### Pre-Flight: Pipeline Connection & Architectural Setup

Before analyzing the texts or writing the synthesis, prompt the user to establish the pipeline connection and define the parameters of the output.

**Prompt the user with these questions:**

1. **Pipeline Connection:**
   - Do you have an existing draft, notes, or prior AI-generated text that I should critically compare with the included corpus? Treat it as a draft only. Do not use it as evidence unless its claims can be traced to the retrieved materials.
   - Have you completed `corpus-screening` and, where relevant, `study-quality-assessment`? If yes, load their exports as contextual metadata. Do not treat screening or appraisal results as a substitute for reading the underlying texts.
   - **Do you have full PDF files for the included papers, or only abstracts/metadata?** This determines the reading mode:
     - **Mode A (Abstract-Only):** You have abstracts or metadata for the researcher-included corpus but no full texts. Every claim will be tagged `[Abstract only]` and this limitation will be disclosed in the deliverable.
     - **Mode B (Full-Text):** You have PDF files for some or all papers. The synthesis will be grounded in full-text evidence, read in 4-page batches to avoid context-window errors.
2. **Review Type:** What is the overarching methodology of this review? (Systematic, Scoping, Integrative, Qualitative Meta-Synthesis, or Critical Interpretive Synthesis).
3. **Synthesis Type & Discursive Format:** How should the text be structured? (Argumentative-Expository, Expository/Descriptive, Comparative, Critical, or a combination).
4. **Depth of Analysis:** Should the synthesis focus on high-level thematic mapping, or granular, detailed extraction of specific variables/mechanisms?
5. **Target Audience/Purpose:** Is this synthesis for a dissertation/thesis chapter, an empirical article's background section, or a standalone review article?
6. **Citation Format:** What format should the references and citations follow (e.g., APA 7th, Vancouver, Harvard)?
7. **Optional synthesis protocol:** Would you like a **Popay-informed narrative-synthesis mode**? Explain that this records four activities, an initial theoretical account, preliminary synthesis, exploration of relationships, and assessment of robustness. It does not impose themes. The researcher must approve the theoretical account and relationship questions before prose is drafted.

**🛑 STOP: Wait for the user to answer these questions and provide the corpus before proceeding to Stage 1.**

---

### Stage 1 — Corpus Overview (AI-Generated, Read-Only)

Do not ask the user for themes yet. If the user sets the thematic agenda before seeing what the corpus actually contains, they risk anchoring on preconceptions.

#### 1a. Determine Reading Mode

Based on the user's answer to the Pre-Flight question about full text availability, select one of two reading modes:

**Mode A — Abstract-Only Mode** (when the user does not have full PDFs)

Use this mode only when the researcher-included corpus has abstracts or metadata but no full texts. Do not use a pre-screening candidate-corpus table from `verified-paper-search` as a synthesis corpus unless the researcher explicitly confirms that its records are the intended included set. In this mode:
- Read the abstracts and metadata for all included papers.
- Apply Rule 3 (Quote Before Analyzing) to abstracts: extract the exact abstract text before drawing any observation from it.
- Label every claim in the synthesis with the tag `[Abstract only]`.
- Proceed directly to Stage 1b after reading all abstracts.

**Mode B — Full-Text Mode** (when the user has PDF files)

If the user has provided PDF files, you **MUST NOT read any PDF in one uninterrupted context**. Every PDF, including short PDFs, must be processed through the universal batch-reading rule. There are no length-based exceptions.

For every PDF provided, follow this semantic-provenance protocol:

1. **Verify and register the file.** Confirm the path, assign a stable `Document_ID`, and copy it to `/home/ubuntu/articles/` if needed.
2. **Create a section map before analysis.** Identify page ranges for abstract, introduction, methods, results or findings, discussion, conclusion, tables, appendices, and any field-specific sections. Save `/home/ubuntu/articles/evidence_maps/<Document_ID>_section_map.csv` with Document_ID, Section, Start_Page, End_Page, and Notes.
3. **Split into bounded page chunks.** Use the split-pdf protocol to create 4-page chunks. Map every chunk to the section map. A chunk is a delivery unit, not the intellectual unit of analysis.
4. **Read by coherent section in small batches.** Read up to three split files at a time. When a section crosses a batch boundary, record the unfinished section and resume it before drawing an interpretation. Never read a whole document directly because it is short.
5. **After each batch, update the evidence ledger.** Save direct quotations with Document_ID, section, page, chunk, evidence type, and a provisional interpretation. Record research question, method, sample, data sources, findings, theory, contextual scope, and any contradiction with the abstract.
6. **Pause after each batch** and confirm with the user before reading the next three splits.
7. **Refresh before cross-paper drafting.** Before drafting any section that compares papers, reload the relevant evidence-ledger rows and section-map references. If a claim crosses documents or sections without traceable evidence, mark it unsupported and do not draft it.

#### 1b. Corpus Overview

If the researcher selected Popay-informed narrative-synthesis mode, record an **initial theoretical account** at this point. The AI may describe theories and mechanisms explicitly present in the corpus, but it must not propose the account as the review's architecture. Present it as a provisional evidence map for the researcher to approve, revise, or reject.

Using the extracted notes and any abstracts or prior synthesis provided, produce a structured overview for the user:

- Total number of studies and data types (full text vs. abstract only).
- Distribution of study designs and methodologies.
- Geographic/contextual distribution.
- Most frequently addressed concepts and theoretical frameworks.
- Explicit note on where full texts contradict or complicate the abstract-based synthesis, if applicable.
- Any papers where evidence was too sparse to summarize (flag as "Insufficient evidence — I don't know").

**🛑 STOP: Present this overview to the user. This is purely informational. Do not propose themes.**

---

### Stage 2 — Thematic Agenda Setting (User-Driven)

Now that the user has seen the corpus overview, ask them to propose the themes, arguments, or questions they want the synthesis to address. If Popay-informed mode is selected, also ask the researcher to approve or revise the provisional theoretical account and specify which relationships across studies should be examined, for example by population, context, design, exposure, mechanism, outcome, or theoretical framework.

Once the user provides their agenda, check each proposed theme against the corpus and report back:
- Which papers support the theme, with specific evidence (quote or abstract passage)?
- Which papers contradict or complicate it?
- Where is the evidence thin or absent? (Apply Rule 1: say "I don't have sufficient evidence for this theme in the corpus.")
- Where did you (the AI) have to make a judgment call? Flag these explicitly.

**🛑 STOP: Present this feedback and wait for the user to approve or revise the thematic agenda before writing any prose.**

---

### Stage 3 — Incremental Prose Generation (User-Approved, Section by Section)

With the agenda finalized, draft the synthesis **one section at a time**, strictly following the user-approved structure, the Anti-Hallucination Mode rules, and the Language and Stylistic Constraints.

**Paragraph-level protocol:**

1. **Extract first.** Before writing a paragraph, list the quotes or abstract passages and their Document_ID, section, and page references. Do not write prose until the evidence is assembled.
2. **Use the Claim Verification Ledger when required.** For any comparative, causal, theoretical, or multi-study claim, decompose the claim into component propositions. Form focused verification questions, retrieve the exact supporting or contradictory passages, and mark every proposition Supported, Qualified, Contradicted, or Unsupported. Revise or retract the sentence when any necessary proposition is unsupported. Do not use the ledger mechanically for trivial factual descriptions.
3. **Write using MEAL or SEED.** Introduce the theme (Main idea/Statement), present the evidence as direct quotes or attributed abstract passages (Evidence), analyze only what the evidence permits (Analysis/Discussion), and transition to the next paragraph (Lead out).
4. **Cite inline.** Every sentence that makes a factual claim must carry an inline citation in the user's chosen format.
5. **Flag gaps.** If a paragraph requires a claim that cannot be grounded in the corpus, write: "The corpus does not provide sufficient evidence to address [specific point]. This gap may warrant further search."
6. **Popay-informed robustness check, if selected.** Before finalizing a section, record what evidence supports the preliminary synthesis, what relationships were examined, how heterogeneity affects interpretation, and what methodological or reporting limitations constrain the conclusion. Do not translate counts of papers into a claim of consensus.

**After each section:**

**🛑 STOP.** Present the drafted section to the user with a brief note on:
- Which claims are grounded in full text (Mode B) vs. abstract only (Mode A).
- Any claims that were retracted because no source could be found.
- Any gaps flagged during drafting.

Ask the user to approve, revise, or redirect before drafting the next section. Repeat until the synthesis is complete.

---

### Final Deliverable

The completed synthesis must include a **Transparency Log** and an **evidence-control appendix**. These records allow the researcher to audit every AI judgment and override any entry before submitting the work.

| Section | Claim | Component Propositions Verified? | Source and Location | Evidence Type | Verification Status | Publication Status Check |
|---|---|---|---|---|---|---|
| [Section name] | [Summarized claim] | Yes / Not required | [Author, Year, Document_ID, section, p. X or DOI] | Full text / Abstract / Metadata | Supported / Qualified / Contradicted / Retracted | Verified by `scientific-reference-reviewer` / Not assessed |

Also export:

- `claim_verification_ledger.csv` for claims that required a CoVe-style verification pass.
- `evidence_ledger.csv` with Document_ID, source location, quotation, evidence type, and draft-section use.
- `section_map_index.csv` linking each document's semantic section map to its evidence ledger.
- `popay_synthesis_record.md` when Popay-informed mode was selected, documenting the researcher-approved theoretical account, preliminary synthesis, explored relationships, and robustness assessment.

The publication-status field must report only a check actually performed by `scientific-reference-reviewer`. Do not infer that a source is unretracted because no status record is present.
