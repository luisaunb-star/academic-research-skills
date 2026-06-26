---
name: deep-academic-synthesis
description: Synthesize academic literature in depth, grounded strictly in retrieved texts. Uses user-guided configuration for review type, synthesis depth, and discursive format. Enforces strict language constraints (no promotional adjectives, no artificial copulas) and anti-hallucination rules. Use when a user provides a corpus of retrieved literature and needs a methodologically sound, cohesive academic synthesis written in professional academic style.
---

# Deep Academic Synthesis

## The Problem This Solves

Novice researchers frequently conflate the mechanical act of searching for literature with the intellectual act of synthesizing it. A literature review is not an annotated bibliography nor a chronological aggregation of past findings. True academic synthesis requires the researcher to digest, sift, classify, simplify, and combine primary information to generate new knowledge, construct theoretical models, or identify epistemological gaps.

This skill automates the transition from a curated corpus of literature to a structured, methodologically sound academic synthesis. It enforces strict grounding (RAG principles) to prevent hallucination, applies rigorous academic language constraints, and requires the user to explicitly define the architectural parameters of the synthesis before writing begins.

## Language and Stylistic Constraints (CRITICAL)

When acting as an academic researcher synthesizing literature, you **MUST strictly adhere** to the following linguistic constraints. Failure to do so compromises the academic integrity of the output.

1. **Anti-Hallucination (Strict RAG):** The synthesis must be entirely based on the provided materials (full text or abstract). Do not invent, infer, or create any findings, mechanisms, or contexts that are not explicitly stated inside the provided texts.
2. **Cohesive Paragraph Structure:** Use the MEAL plan (Main idea, Evidence, Analysis, Lead out) or SEED plan (Statement, Expand, Evidence, Discussion) to ensure paragraphs are cohesive. Use varied connectives to ensure fluid transitions between paragraphs.
3. **No Vague/Promotional Adjectives:** Completely avoid terms such as: comprehensive, adept, lively, crucial, dynamic, disruptive, effective, efficient, exciting, engaging, essential, strategic, exemplary, fascinating, fundamental, imperative, invaluable, innovative, inspiring, thought-provoking, praiseworthy, meticulous, thorough, multifaceted, powerful, renowned, revolutionary, robust, significant, synergistic, transformative, unique, valuable, vibrant, vital, rich (figurative), profound (metaphorical), impressive, extraordinary, exceptional, notable, brilliant, captivating, spectacular, grand, magnificent, majestic, monumental, matchless, perfect, solid, superior.
4. **No Artificial Copulas:** Never replace "is/are/was/were/has/had" with elaborate constructions. **Prohibited:** "serves as," "acts as," "remains as," "marks a moment," "represents a milestone," "possesses," "presents," "offers" (when "has" suffices), "stands out as." **Prefer:** is, are, was, were, has, had.
5. **No Negative Parallelisms:** Avoid forced structures involving negation: "Not only X, but also Y," "It is not about X, it is about Y," "Without X, without Y, only Z," "It is not about... it is about..."
6. **Punctuation:** **Prohibited:** em-dash (—), semicolon (;), colon (:) except in formal lists, curly quotes. **Use:** commas, periods, parentheses, straight quotes. Avoid long, convoluted clauses.

## Workflow

### Step 1 — Define the Synthesis Architecture (User Configuration)

Before analyzing the texts or writing the synthesis, you must prompt the user to define the parameters of the output. Present the following questionnaire to the user. Provide the definitions inline so the user understands the choices.

**Prompt the user with these questions:**

1. **Review Type:** What is the overarching methodology of this review?
   - *Systematic Review (Aggregative):* Focuses on answering "what works" by pooling homogeneous empirical data.
   - *Scoping Review (Descriptive):* Maps the topography of knowledge, identifies gaps, clarifies concepts (often includes grey literature).
   - *Integrative Review (Comprehensive):* Bridges empirical and theoretical divides, combining diverse methodologies to inform practice.
   - *Qualitative Meta-Synthesis (Interpretivist):* Generates third-order constructs and new theories from qualitative data.
   - *Critical Interpretive Synthesis:* Questions underlying assumptions and problematizes the literature.
2. **Synthesis Type & Discursive Format:** How should the text be structured?
   - *Argumentative-Expository:* Presents evidence to support a specific thesis.
   - *Expository/Descriptive:* Neutrally maps findings and study characteristics.
   - *Comparative:* Contrasts differing methodologies, findings, or theoretical frameworks.
   - *Critical:* Evaluates methodological weaknesses and epistemological gaps.
   - *(Or a specific combination of the above)*
3. **Depth of Analysis:** Should the synthesis focus on high-level thematic mapping, or granular, detailed extraction of specific variables/mechanisms?
4. **Target Audience/Purpose:** Is this synthesis for a dissertation/thesis chapter, an empirical article's background section, or a standalone review article?
5. **Visual Aids:** Do you want to include Markdown graphics or tables? If so, for what purpose (e.g., summary of study characteristics, thematic frequency chart, Context-Mechanism-Outcome mapping)?
6. **Citation Format:** What format should the references and citations follow (e.g., APA 7th, Vancouver, Harvard)?

**🛑 STOP: Wait for the user to answer these architectural questions before proceeding to Step 2.**

### Step 2 — Data Extraction and Charting

Once the user provides the parameters and the corpus of texts, perform a structured data extraction. 

1. Read the provided texts (abstracts or full texts).
2. Extract the data conceptually based on the chosen Review Type (e.g., extracting Context-Mechanism-Outcome for realist reviews, or variables/methodologies for scoping reviews).
3. Do not write the final text yet. Create a mental or scratchpad matrix of the themes, findings, and the specific papers that support them.

### Step 3 — Draft the Synthesis

Draft the synthesis adhering strictly to the user's architectural choices and the **Language and Stylistic Constraints**.

- **Structure:** Organize the literature around specific variables, themes, or concepts (as suggested by Creswell), rather than chronologically or by author.
- **Paragraph Level:** Use the MEAL or SEED framework. Introduce the theme, provide evidence from multiple sources, analyze the consensus or contradiction, and transition smoothly.
- **Grounding:** Ensure every claim is explicitly tied to a citation from the provided corpus.
- **Visuals:** Insert tables or charts if requested in Step 1.

### Step 4 — Deliver and Review

Deliver the synthesis to the user. Include a brief meta-commentary confirming how the specific language constraints (no promotional adjectives, no artificial copulas) and architectural parameters were applied.
