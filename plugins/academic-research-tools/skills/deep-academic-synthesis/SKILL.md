---
name: deep-academic-synthesis
description: Synthesize academic literature in depth, grounded strictly in retrieved texts, with the human researcher in full control of the intellectual architecture. Uses a three-stage model (Corpus Overview -> Thematic Agenda Setting -> Incremental Prose Generation) to prevent cognitive outsourcing. Integrates directly with outputs from `verified-paper-search`. Enforces strict language constraints and anti-hallucination rules.
---

# Deep Academic Synthesis

## The Problem This Solves

When an AI produces a complete synthesis in one shot, the researcher's role collapses from active synthesist to passive reviewer. The intellectual work of deciding which themes matter, how findings relate, and what the argument should be gets delegated, resulting in cognitively outsourced writing that may be technically correct but epistemologically hollow.

This skill solves that by acting as a pipeline continuation of the `verified-paper-search` skill. It shifts from breadth (abstracts) to depth (full texts) while keeping the human researcher in strict control of the intellectual architecture through a three-stage, interactive process.

## Language and Stylistic Constraints (CRITICAL)

When acting as an academic researcher synthesizing literature, you **MUST strictly adhere** to the following linguistic constraints. Failure to do so compromises the academic integrity of the output.

1. **Anti-Hallucination (Strict RAG):** The synthesis must be entirely based on the provided materials (full text or abstract). Do not invent, infer, or create any findings, mechanisms, or contexts that are not explicitly stated inside the provided texts.
2. **Cohesive Paragraph Structure:** Use the MEAL plan (Main idea, Evidence, Analysis, Lead out) or SEED plan (Statement, Expand, Evidence, Discussion) to ensure paragraphs are cohesive. Use varied connectives to ensure fluid transitions between paragraphs.
3. **No Vague/Promotional Adjectives:** Completely avoid terms such as: comprehensive, adept, lively, crucial, dynamic, disruptive, effective, efficient, exciting, engaging, essential, strategic, exemplary, fascinating, fundamental, imperative, invaluable, innovative, inspiring, thought-provoking, praiseworthy, meticulous, thorough, multifaceted, powerful, renowned, revolutionary, robust, significant, synergistic, transformative, unique, valuable, vibrant, vital, rich (figurative), profound (metaphorical), impressive, extraordinary, exceptional, notable, brilliant, captivating, spectacular, grand, magnificent, majestic, monumental, matchless, perfect, solid, superior.
4. **No Artificial Copulas:** Never replace "is/are/was/were/has/had" with elaborate constructions. **Prohibited:** "serves as," "acts as," "remains as," "marks a moment," "represents a milestone," "possesses," "presents," "offers" (when "has" suffices), "stands out as." **Prefer:** is, are, was, were, has, had.
5. **No Negative Parallelisms:** Avoid forced structures involving negation: "Not only X, but also Y," "It is not about X, it is about Y," "Without X, without Y, only Z," "It is not about... it is about..."
6. **Punctuation:** **Prohibited:** em-dash (—), semicolon (;), colon (:) except in formal lists, curly quotes. **Use:** commas, periods, parentheses, straight quotes. Avoid long, convoluted clauses.

## Workflow

### Pre-Flight: Pipeline Connection & Architectural Setup

Before analyzing the texts or writing the synthesis, you must prompt the user to establish the pipeline connection and define the parameters of the output.

**Prompt the user with these questions:**

1. **Pipeline Connection:** 
   - Do you have an existing AI-generated synthesis (e.g., from `verified-paper-search`) that I should use as a starting point?
   - Do you have full texts available for any of the included papers, or are we working from abstracts only?
   - Should I treat the existing synthesis as a draft to be deepened, or as a reference to be critically compared against what the full texts actually say? (Often, full texts reveal nuances or limitations concealed by abstracts).
2. **Review Type:** What is the overarching methodology of this review? (Systematic, Scoping, Integrative, Qualitative Meta-Synthesis, or Critical Interpretive Synthesis).
3. **Synthesis Type & Discursive Format:** How should the text be structured? (Argumentative-Expository, Expository/Descriptive, Comparative, Critical, or a combination).
4. **Depth of Analysis:** Should the synthesis focus on high-level thematic mapping, or granular, detailed extraction of specific variables/mechanisms?
5. **Target Audience/Purpose:** Is this synthesis for a dissertation/thesis chapter, an empirical article's background section, or a standalone review article?
6. **Citation Format:** What format should the references and citations follow (e.g., APA 7th, Vancouver, Harvard)?

**🛑 STOP: Wait for the user to answer these questions and provide the corpus before proceeding to Stage 1.**

### Stage 1 — Corpus Overview (AI-Generated, Read-Only)

Do not ask the user for themes yet. If the user sets the thematic agenda before seeing what the corpus actually contains, they risk anchoring on preconceptions. 

1. Read all provided texts (and the previous synthesis, if provided).
2. Produce a structured overview for the user:
   - Total number of studies and data types (full text vs. abstract only).
   - Distribution of study designs and methodologies.
   - Geographic/contextual distribution.
   - Most frequently addressed concepts and theoretical frameworks.
   - *If applicable:* Explicitly note where the full texts contradict or complicate the abstract-based synthesis from the previous step.

**🛑 STOP: Present this overview to the user. This is purely informational.**

### Stage 2 — Thematic Agenda Setting (User-Driven)

Now that the user has seen the corpus overview, ask them to propose the themes, arguments, or questions they want the synthesis to address. 

Once the user provides their agenda, check each proposed theme against the corpus and report back:
- Which papers support the theme?
- Which papers contradict or complicate it?
- Where is the evidence thin?
- Where did you (the AI) have to make a judgment call?

**🛑 STOP: Present this feedback and wait for the user to approve or revise the thematic agenda before writing any prose.**

### Stage 3 — Incremental Prose Generation (User-Approved, Section by Section)

With the agenda finalized, draft the synthesis **one section at a time**, strictly following the user-approved structure and the **Language and Stylistic Constraints**.

- **Paragraph Level:** Use the MEAL or SEED framework. Introduce the theme, provide evidence from multiple sources, analyze the consensus or contradiction, and transition smoothly.
- **Grounding:** Ensure every claim is explicitly tied to a citation from the provided corpus. Track evidence strength (e.g., noting if a claim relies solely on an abstract).

**🛑 STOP after drafting each section.** Ask the user to approve, revise, or redirect the argument before you draft the next section. Repeat until the synthesis is complete.
