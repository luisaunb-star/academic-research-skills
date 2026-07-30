---
name: deep-academic-synthesis
description: Synthesize academic literature in depth, grounded strictly in retrieved texts, with the human researcher in full control of the intellectual architecture. Uses a three-stage model (Corpus Overview -> Thematic Agenda Setting -> Incremental Prose Generation) to prevent cognitive outsourcing. Enforces strict anti-hallucination mode (say "I don't know", cite every claim, quote before analyzing), language constraints, and RAG grounding throughout.
---

# Deep Academic Synthesis

## The Problem This Solves

When an AI produces a complete synthesis in one shot, the researcher's role collapses from active synthesist to passive reviewer. The intellectual work of deciding which themes matter, how findings relate, and what the argument should be gets delegated, resulting in cognitively outsourced writing that may be technically correct but epistemologically hollow.

This skill solves that by acting as a pipeline continuation of the `verified-paper-search` skill. It shifts from breadth (abstracts) to depth (full texts) while keeping the human researcher in strict control of the intellectual architecture through a three-stage, interactive process.

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
   - Do you have an existing AI-generated synthesis (e.g., from `verified-paper-search`) that I should use as a starting point?
   - **Do you have full PDF files for the included papers, or only abstracts/metadata?** This determines the reading mode:
     - **Mode A (Abstract-Only):** You have only abstracts or the mapping table from `verified-paper-search`. Every claim will be tagged `[Abstract only]` and this limitation will be disclosed in the deliverable.
     - **Mode B (Full-Text):** You have PDF files for some or all papers. The synthesis will be grounded in full-text evidence, read in 4-page batches to avoid context-window errors.
   - Should I treat the existing synthesis as a draft to be deepened, or as a reference to be critically compared against what the full texts actually say?
2. **Review Type:** What is the overarching methodology of this review? (Systematic, Scoping, Integrative, Qualitative Meta-Synthesis, or Critical Interpretive Synthesis).
3. **Synthesis Type & Discursive Format:** How should the text be structured? (Argumentative-Expository, Expository/Descriptive, Comparative, Critical, or a combination).
4. **Depth of Analysis:** Should the synthesis focus on high-level thematic mapping, or granular, detailed extraction of specific variables/mechanisms?
5. **Target Audience/Purpose:** Is this synthesis for a dissertation/thesis chapter, an empirical article's background section, or a standalone review article?
6. **Citation Format:** What format should the references and citations follow (e.g., APA 7th, Vancouver, Harvard)?

**🛑 STOP: Wait for the user to answer these questions and provide the corpus before proceeding to Stage 1.**

---

### Stage 1 — Corpus Overview (AI-Generated, Read-Only)

Do not ask the user for themes yet. If the user sets the thematic agenda before seeing what the corpus actually contains, they risk anchoring on preconceptions.

#### 1a. Determine Reading Mode

Based on the user's answer to the Pre-Flight question about full text availability, select one of two reading modes:

**Mode A — Abstract-Only Mode** (when the user does not have full PDFs)

Use this mode when the user has only abstracts, metadata, or the output table from `verified-paper-search`. In this mode:
- Read the abstracts and metadata for all included papers.
- Apply Rule 3 (Quote Before Analyzing) to abstracts: extract the exact abstract text before drawing any observation from it.
- Label every claim in the synthesis with the tag `[Abstract only]`.
- Proceed directly to Stage 1b after reading all abstracts.

**Mode B — Full-Text Mode** (when the user has PDF files)

If the user has provided PDF files, you **MUST NOT read any PDF in full**. Reading a full PDF will either crash the session with an unrecoverable context-window error or produce shallow output. There are no exceptions.

For every PDF provided, follow this protocol:

1. **Verify the file** exists at the provided path.
2. **Copy it** to `/home/ubuntu/articles/` if it is not already there.
3. **Split it** into 4-page chunks:
   ```bash
   mkdir -p /home/ubuntu/articles/split_<pdf_name>
   python3 /home/ubuntu/skills/split-pdf/scripts/split_pdf.py \
     /home/ubuntu/articles/<pdf_name>.pdf \
     /home/ubuntu/articles/split_<pdf_name>
   ```
   If PyPDF2 is not installed, run `sudo pip3 install PyPDF2` first.
4. **Read exactly 3 split files at a time** (~12 pages per batch) using the `file` tool.
5. **After each batch**, update a running `notes.md` file with structured dimensions:
   - Research question and purpose
   - Methodology and study design
   - Data sources, sample, time period
   - Key findings and results (with direct quotes and page references)
   - Theoretical frameworks referenced
   - Geographic/contextual scope
   - Any passage where the text contradicts or complicates the abstract
6. **Pause after each batch** and confirm with the user before reading the next 3 splits.

**Exception:** Papers shorter than approximately 15 pages may be read directly without splitting.

#### 1b. Corpus Overview

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

Now that the user has seen the corpus overview, ask them to propose the themes, arguments, or questions they want the synthesis to address.

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

1. **Extract first.** Before writing a paragraph, list the quotes or abstract passages you will use as evidence for that paragraph. Do not write prose until the evidence is assembled.
2. **Write using MEAL or SEED.** Introduce the theme (Main idea/Statement), present the evidence as direct quotes or attributed abstract passages (Evidence), analyze what the evidence shows (Analysis/Discussion), and transition to the next paragraph (Lead out).
3. **Cite inline.** Every sentence that makes a factual claim must carry an inline citation in the user's chosen format.
4. **Flag gaps.** If a paragraph requires a claim that cannot be grounded in the corpus, write: "The corpus does not provide sufficient evidence to address [specific point]. This gap may warrant further search."

**After each section:**

**🛑 STOP.** Present the drafted section to the user with a brief note on:
- Which claims are grounded in full text (Mode B) vs. abstract only (Mode A).
- Any claims that were retracted because no source could be found.
- Any gaps flagged during drafting.

Ask the user to approve, revise, or redirect before drafting the next section. Repeat until the synthesis is complete.

---

### Final Deliverable

The completed synthesis must include a **Transparency Log** as a final appendix. The log records:

| Section | Claim | Source | Evidence Type | Retracted? |
|---|---|---|---|---|
| [Section name] | [Summarized claim] | [Author, Year, p. X or DOI] | Full text / Abstract / Metadata | No / Yes (reason) |

This log allows the researcher to audit every AI judgment and override any entry before submitting the work.
