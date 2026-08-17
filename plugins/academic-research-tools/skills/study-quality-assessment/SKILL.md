---
name: study-quality-assessment
description: Appraise the methodological and reporting quality of academic papers using full-text batch extraction and field-calibrated CASP, JBI, MMAT, and QuADS checklists. Produces individual appraisal records and a consolidated quality matrix for the full corpus.
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

# 🛑 CRITICAL INSTRUCTIONS (ANTI-HALLUCINATION AND READING DISCIPLINE)

Before executing this skill, you MUST adhere to the following rules without exception:

1. **Full-Text Mandate.** Quality appraisal cannot be performed on abstracts alone. You must have access to the full text (PDF, DOCX, or MD). If full text is unavailable, the paper must be marked "Excluded (E5: Inaccessible)" and skipped.
2. **Universal Batch Reading.** Regardless of file length or format, you MUST always read in batches. There is no "short enough to skip" exception. This rule exists because the "lost in the middle" attention degradation problem (Liu et al., 2023; Chroma Research, 2025) affects all document lengths, not only long ones.
3. **No Blind "Can't Tell".** Before marking any item "Can't Tell" or "No", you must state which specific section of the paper you searched (e.g., "Searched Methods section and Limitations section"). If you cannot name the section, you must re-read it before finalizing the response.
4. **No Inference of Ethics or Reflexivity.** Do not infer ethical approval or researcher reflexivity from context. If it is not explicitly reported, the answer is "Can't Tell" (or "No" depending on the checklist guidance).
5. **Field-Specific Calibration.** You must apply the calibration rules detailed in Step 3. Do not penalize business, IS, or engineering papers for lacking clinical trial features (blinding, probability sampling) unless the study design explicitly requires them.

---

# Step 1: Verify Inputs and Identify Study Designs

Before reading any paper, collect the following information:

1. Confirm that the full text is available for each paper. If not, mark the paper "Excluded (E5: Inaccessible)" and remove it from the appraisal list.
2. For each remaining paper, identify the study design from the abstract or title page. If the design is ambiguous, read the Methods section first (in a single targeted batch) to confirm.
3. Route each paper to the correct checklist using the instrument routing table below.
4. For mixed, multi-method, design-science, or otherwise heterogeneous papers, ask the researcher whether the appraisal purpose requires **MMAT** or **QuADS** before assigning an instrument. Do not treat the two instruments as interchangeable.
5. Present the list of papers, their identified designs, the proposed appraisal purpose, and assigned checklists to the user. Ask for confirmation before proceeding.

**Instrument Routing:**

| Study Design | Checklist |
|---|---|
| Qualitative (case study, ethnography, phenomenology, grounded theory) | CASP Qualitative |
| Descriptive or survey-based cross-sectional | CASP Cross-Sectional |
| Analytical cross-sectional (exposure-outcome association) | JBI Analytical Cross-Sectional |
| Quasi-experimental (non-randomized intervention, pre-post, time-series) | JBI Quasi-Experimental |
| Systematic or scoping review | CASP Systematic Review |
| Explicit mixed-methods design with qualitative, quantitative, and integration components that require design-specific appraisal | MMAT 2018 |
| Diverse multi- or mixed-method corpus where the researcher needs one cross-design appraisal of methodological and reporting quality | QuADS 2021 |
| Design science or unclassified study | Ask the researcher whether MMAT's integration criteria or QuADS's cross-design reporting profile better fits the appraisal purpose. Record the limitation of either choice. |

---

### QuADS calibration before corpus-wide appraisal

If **QuADS** is selected, explain that it uses a 0 to 3 scale and requires reviewer judgment in relation to the particular body of literature. It has **no validated overall cut-off** for high or low quality. Do not use a total score to exclude a paper automatically.

- In a multi-researcher appraisal, ask reviewers to independently score the same 3 to 5 included papers, discuss disagreements, and agree a written application note before scoring the remaining corpus.
- In a one-researcher appraisal, select 3 to 5 varied papers as a calibration subset. Present the provisional criterion-by-criterion rationale to the researcher before continuing. This checks that the proposed interpretations fit the field and review question.
- For every QuADS judgment, retain the direct evidence, section or page location, score, and the field-specific application note when one was needed.

---

# Step 2: Checklist-Anchored Batch Reading

For each paper, load the relevant checklist items into your active context BEFORE reading the paper. You are reading specifically to find evidence for or against each checklist item. This prevents the distractor amplification problem identified in long-context research.

**Reading protocol by format:**

**PDF files:** Use the split-pdf protocol. Copy the file to `/home/ubuntu/articles/`, split it into 4-page chunks using the split-pdf script, read exactly 3 chunks per batch, update your notes file after each batch, and PAUSE for user confirmation before the next batch.

**DOCX or MD files:** Use Sequential Range Reading. Read 100 lines per batch using the `range` parameter of the file tool. Update your notes file after each batch. Continue until the entire file is read.

**After each batch**, update a structured notes file for the paper with the following fields:
- Research question and aims
- Study design and sample description
- Data collection method and instruments
- Analysis approach
- Key findings
- Ethical approval statement (exact quote if present)
- Reflexivity or positionality statement (exact quote if present)
- Limitations acknowledged by the authors
- Checklist items provisionally answered so far, with supporting quotes

---

# Step 3: Apply Field-Specific Calibration Rules

When answering checklist items, apply these calibration rules to avoid unfairly penalizing non-health research:

1. **Sampling acceptability (Business, IS, Engineering).** Convenience and panel sampling (Prolific, MTurk, LinkedIn) are standard practice in these fields. Mark "Yes" if the sampling limitation is acknowledged and the study does not claim population-level generalization. Mark "No" only if the study claims representativeness it cannot support.
2. **Reflexivity in non-health qualitative research.** Reflexivity may be implicit through audit trails, member checking, or triangulation rather than a formal dedicated section. Absence of a formal reflexivity statement should be "Can't Tell", not "No". Mark "No" only if researcher positionality is entirely absent from the paper.
3. **Instrument validation.** Descriptive surveys using previously validated scales from the literature do not require new Confirmatory Factor Analysis. Mark "Yes" if established, cited scales are used. Reserve "No" or "Can't Tell" for studies that measure latent constructs without any validation evidence.
4. **Blinding.** Rarely applicable outside clinical settings. Mark "Not Applicable" (N/A) for business, management, and engineering studies unless the study involves human subjects in a clinical-adjacent context.
5. **Generalizability and transferability.** IS and engineering case studies aim for analytical (theoretical) generalization, not population representativeness. Mark "No" (not "Can't Tell") when the study explicitly limits its claims to the studied context. Mark "Can't Tell" only when the scope of claims is genuinely ambiguous.
6. **Protocol papers.** Execution-dependent items (complete follow-up, analysis results, outcome consistency) must be marked "Unclear". Only planned procedures, instrument selection, and ethical approval can be assessed based on the protocol description.

---

# Step 4: Targeted Second Pass (Cross-Section Consistency Check)

After completing all reading batches for a paper, perform a targeted second pass on the Methods, Sample, Analysis, and Limitations sections. This step works on your extracted notes rather than the full paper, so it does not require re-reading the entire document.

Check for the following three consistency issues:
- Does the sampling procedure described in Methods match the limitations acknowledged in the Discussion? If the Discussion acknowledges a convenience sample but Methods implied a representative one, revise the relevant checklist items.
- Does the analysis approach described in Methods match the results actually reported? If the Methods describe SEM but the Results only report descriptive statistics, flag this under the analysis item.
- Is ethical approval mentioned in Methods consistent with the participant description? If the study describes vulnerable populations but no ethics statement is present, revise the ethics item.

Update your provisional checklist answers based on this second pass before finalizing the appraisal record.

---

# Step 5: Individual Appraisal Records

For each paper, produce a complete appraisal record in the format below.

For the first paper appraised (and every 5th paper thereafter), you MUST pause and present the record to the user for confirmation before continuing to the next paper. This spot-check prevents systematic drift in your interpretations across a large corpus.

**Template: Quality Appraisal Record**

Paper: [Title, Author, Year, DOI]
Study Design: [Identified design]
Checklist Used: [e.g., CASP Qualitative]

| Item | Question Summary | Judgment | Evidence (Direct Quote and Section) |
|---|---|---|---|
| 1 | [Full item text] | [Yes / No / Can't Tell / N/A / Unclear] | "[Direct quote from paper]" (Section, page) |
| 2 | ... | ... | ... |

Overall Assessment: [Instrument-specific narrative profile, with strengths, limitations, and any field-calibration note]
Inclusion Decision: [Researcher decision only. Do not automatically exclude a study from the review on the basis of a checklist total.]

**For QuADS records:** Report the 13 criterion scores and a criterion-level narrative profile. You may calculate a descriptive total out of 39 only if the researcher requests it, but state that QuADS has no validated high/low-quality cut-off and that the total must not determine inclusion automatically.

---

# Step 6: Consolidated Quality Appraisal Matrix

After all individual appraisal records are complete, produce a consolidated matrix. This is the deliverable intended for inclusion in the Methods section of a systematic or integrative review manuscript.

**Matrix format:** Use instrument-specific item names. Do not force different checklists into an artificial 10-item grid.

| Paper (Author, Year) | Design | Checklist | Criterion / Item | Judgment or Score | Evidence Location | Field-Calibration Note | Researcher Decision |
|---|---|---|---|---|---|---|---|
| [Author, Year] | [Design] | [Instrument] | [Full item label] | Y/N/CT/NA/U or 0–3 for QuADS | [Direct quote, section, page] | [If used] | [Researcher decision] |

Also provide a paper-level summary table with one row per paper and an instrument-specific profile. For QuADS, include Criterion 1 through Criterion 13, any researcher-requested descriptive total out of 39, and a statement that no cut-off was applied.

**Legend:** Y = Yes, N = No, CT = Can't Tell, NA = Not Applicable, U = Unclear (protocol papers only). QuADS uses 0 = not reported or absent, 1 = minimal or broad evidence, 2 = partial or adequate evidence, and 3 = detailed and well-supported evidence.

After presenting the matrices, export the long-format evidence matrix as `/home/ubuntu/articles/quality_appraisal_matrix.csv` and the paper-level summary as `/home/ubuntu/articles/quality_appraisal_summary.csv`. Inform the user that both can be opened directly in Excel or Google Sheets.

Provide a brief narrative summary describing patterns by criterion, the main methodological or reporting limitations, and the role of any field-specific calibration. Do not state that papers were excluded by checklist score unless the researcher explicitly made and documented that decision.

---

# APPENDIX: EMBEDDED CHECKLISTS

Load the relevant checklist before reading each paper.

---

## Checklist 1: CASP Qualitative (2024)
Response options: Yes, No, Can't Tell.

**Section A. Are the results valid?**
1. Was there a clear statement of the aims of the research? (Consider: goal, why it is important, relevance)
2. Is a qualitative methodology appropriate? (Consider: does the research seek to interpret or illuminate actions/subjective experiences?)
3. Was the research design appropriate to address the aims of the research? (Consider: justification for the chosen design)
4. Was the recruitment strategy appropriate to the aims of the research? (Consider: justification for participant selection, reasons why some participants chose not to take part)
5. Was the data collected in a way that addressed the research issue? (Consider: setting justified, clear data collection method, methods modified during study, form of data collected, researcher involvement discussed)
6. Has the relationship between researcher and participants been adequately considered? *(Apply Calibration Rule 2)* (Consider: researcher critically examined their own role, potential bias and influence during formulation of research questions, data collection, including sample recruitment and choice of location)

**Section B. What are the results?**
7. Have ethical issues been taken into consideration? *(Require explicit reporting. Apply Critical Instruction 4)* (Consider: sufficient details of how the research was explained to participants for them to assess whether they wanted to participate, whether ethics committee approval was sought, issues around informed consent/confidentiality)
8. Was the data analysis sufficiently rigorous? (Consider: in-depth description of the analysis process, thematic derivation, sufficient data presented to support findings, contradictory data taken into account, researcher critically examined their own role/bias during analysis)
9. Is there a clear statement of findings? (Consider: findings explicit, adequate discussion of evidence, credibility discussed e.g. triangulation/respondent validation, findings discussed in relation to original research question)

**Section C. Will the results help locally?**
10. How valuable is the research? (Consider: contribution to existing knowledge/understanding, identification of new areas for research, transferability to other populations)

**Key guidance:** "Can't Tell" means the researchers have not been explicit or transparent enough, not necessarily that they did not perform the task. If there are many "Can't tell" responses, interpret the results with caution.

---

## Checklist 2: CASP Cross-Sectional (2024)
Response options: Yes, No, Can't Tell.

1. Did the study address a clearly focused issue? (Consider: population studied, risk factors studied, outcomes considered)
2. Did the authors use an appropriate method to answer their question? (Consider: is a cross-sectional study appropriate to answer the question?)
3. Were the subjects recruited in an acceptable way? *(Apply Calibration Rule 1)* (Consider: was the cohort representative of a defined population, was there something special about the cohort, was everybody included who should have been)
4. Were the measures accurately measured to reduce bias? *(Apply Calibration Rule 3)* (Consider: subjective or objective measurements, do the measures truly reflect what you want them to, have they been validated)
5. Were the data collected in a way that addressed the research issue? (Consider: setting justified, clear data collection method, methods modified during study, form of data collected)
6. Did the study have enough participants to minimise the play of chance? (Consider: is there a power calculation)
7. How are the results presented and what is the main result? (Consider: are the bottom line results clear, have they reported the rate or proportion between the exposed/unexposed, how large is the size of proportion or odds ratio, how meaningful is the result)
8. Was the data analysis sufficiently rigorous? (Consider: are the statistical methods appropriate, is there an assessment of confounding factors, have they been taken into account in the design and/or analysis)
9. Is there a clear statement of findings? (Consider: are the findings explicit, is there adequate discussion of the evidence for and against the researchers' arguments, has the credibility of findings been discussed)
10. Can the results be applied to the local population? *(Apply Calibration Rule 5)* (Consider: are the subjects covered in the study sufficiently different from your population to cause concern, does your local setting differ much from that of the study)
11. How valuable is the research? (Consider: does the study add to the literature, what are the implications for policy/practice)

**Key guidance:** "Can't Tell" means the researchers have not been explicit or transparent enough, not necessarily that they did not perform the task. If there are many "Can't tell" responses, interpret the results with caution.

---

## Checklist 3: JBI Quasi-Experimental (2024 revision)
Response options: Yes, No, Unclear, N/A.

1. Is it clear in the study what is the "cause" and what is the "effect" (i.e., there is no confusion about which variable comes first)? (Check: is it clear that the exposure occurred prior to the outcome?)
2. Was there a control group? *(In single-group pre-post studies, the answer is typically No)* (Check: is there an independent control group, or did participants act as their own control?)
3. Were the participants included in any comparisons similar? (Check: are the characteristics of the participants in the different comparison groups similar, or are differences accounted for?)
4. Were the participants included in any comparisons receiving similar treatment or care, other than the exposure or intervention of interest? (Check: are there co-interventions that could affect the outcome, and were they similar across groups?)
5. Were there multiple measurements of the outcome, both pre and post the intervention or exposure? (Check: are measurements taken before and after the intervention, and are there multiple measurements to establish trends?)
6. Were the outcomes of participants included in any comparisons measured in the same way? (Check: were the same instruments or methods used for outcome measurement across all groups?)
7. Were outcomes measured in a reliable way? (Check: is the outcome measure valid and reliable? Was it measured objectively?)
8. Was follow-up complete and, if not, were differences between groups in terms of their follow-up adequately described and analyzed? (Check: were there dropouts or loss to follow-up, and was this accounted for in the analysis?)
9. Was appropriate statistical analysis used? (Check: does the statistical analysis account for the study design, the nature of the data, and potential confounding?)

**Key guidance:** Items 5 through 9 may need to be answered separately per outcome. The tool does not provide fixed thresholds for low, moderate, or high risk of bias. Reviewers should provide domain-level judgments and report them narratively. For protocol papers, apply Calibration Rule 6.

---

## Checklist 4: JBI Analytical Cross-Sectional (2025 revision)
Response options: Yes, No, Unclear, N/A.

1. Were the criteria for inclusion in the sample clearly defined? (Check: explicit description of inclusion/exclusion criteria used to determine participant eligibility, developed prior to recruitment)
2. Were objective, standard criteria used for measurement of the condition? (Check: was diagnosis or condition definition based on objective, standard criteria as opposed to self-diagnosis? Were matching groups documented if relevant?)
3. Was the exposure measured in a valid and reliable way? (Check: clear description of how exposure was measured and determined, valid determination, appropriate exposure window)
4. Were the outcomes measured in a valid and reliable way? (Check: clear outcome measures, consistently applied definitions and procedures, valid and reliable measurement for the outcome type)
5. Were confounding factors identified? (Check: identification of variables that could distort the exposure-outcome association, explicitly named or discussed)
6. Were strategies to deal with confounding factors stated? (Check: design or analytic strategies used to address confounding, e.g., stratification, regression, matching, standardization, inverse probability weighting)
7. Was appropriate statistical analysis used? (Check: analysis matches design and question, appropriate for variable types, outcome/result-level analyses presented clearly)

**Key guidance:** The revised JBI tool is designed for analytical cross-sectional studies, not descriptive prevalence-only surveys. Each question is phrased so that "Yes" generally indicates lower risk of bias. Thresholds should be defined before review use for multi-reviewer consistency.

---

## Checklist 5: CASP Systematic Review (2024)
Response options: Yes, No, Can't Tell.

1. Did the review address a clearly focused question? *(Consider framing in PECO terms: Population, Exposure/Risk factor, Comparator/Controls, Outcome/s or Event/s)*
2. Did the authors look for the right type of papers? (Consider: best sort of studies would address the review's question and have an appropriate study design)
3. Do you think all the important, relevant studies were included? (Consider: which bibliographic databases were used, follow up from reference lists, personal contact with experts, unpublished as well as published studies, non-English language studies)
4. Did the review's authors do enough to assess quality of the included studies? (Consider: did the authors consider the rigour of the studies they identified? Lack of rigour may affect the studies' results)
5. If the results of the review have been combined, was it reasonable to do so? (Consider: were results similar from study to study, are results of all included studies clearly displayed, are results of different studies similar, are reasons for any variations in results discussed)
6. What are the overall results of the review? (Consider: are you clear about the review's 'bottom line' results, what are these numerically if appropriate, how were the results expressed e.g. NNT, odds ratio)
7. How precise are the results? (Consider: look at the confidence intervals, if given)
8. Can the results be applied to the local population? *(Apply Calibration Rule 5)* (Consider: could the patients/populations covered by the review be sufficiently different to your population to cause concern, is your local setting likely to differ much from that of the review)
9. Were all important outcomes considered? (Consider: is there other information you would like to have seen)
10. Are the benefits worth the harms and costs? (Consider: even if this is not addressed by the review, what do you think based on the evidence presented)

**Key guidance for non-health fields:** "Can't Tell" means the researchers have not been explicit or transparent enough. For Item 3, evaluate databases appropriate to the discipline (ACM Digital Library and IEEE Xplore for computer science, EBSCO Business Source for management). For Item 5, absence of meta-analysis should not be penalized in IS and management, where narrative synthesis and systematic mapping are the norms.

---

## Checklist 6: MMAT 2018 (Mixed Methods and Unclassified Designs)
Response options: Yes, No, Can't Tell.

**For all studies, first answer the two screening questions:**
S1. Are there clear research questions?
S2. Do the collected data and planned analyses address the research questions?

**Then apply the component criteria for the relevant study type(s):**

**Qualitative component (Qual 1-5):**
Qual1. Is the qualitative approach appropriate to answer the research question?
Qual2. Are the qualitative data collection methods adequate to address the research question?
Qual3. Are the findings adequately derived from the data?
Qual4. Is the interpretation of results sufficiently substantiated by data?
Qual5. Is there coherence between qualitative data sources, collection, analysis, and interpretation?

**Quantitative non-randomized component (Quant-NR 1-5):**
QNR1. Are the participants representative of the target population? (Check: description of target population and sample, inclusion/exclusion criteria, reasons for non-participation)
QNR2. Are measurements appropriate regarding both the outcome and intervention/exposure? (Check: clear definitions, justified measures, validated instruments)
QNR3. Are there complete outcome data? (Check: follow-up rate acceptable for the field, reasons for attrition)
QNR4. Are the confounders accounted for in the design and analysis? (Check: identification and management of confounders via stratification, regression, matching, etc.)
QNR5. During the study period, is the intervention administered (or exposure occurred) as intended? (Check: for observational studies, how changes in exposure status or co-exposures were handled)

**Quantitative descriptive component (Quant-D 1-5):**
QD1. Is the sampling strategy relevant to address the research question? (Check: probability or non-probability strategy justified for the question)
QD2. Is the sample representative of the target population? (Check: match between respondents and target population, attempts to achieve representativeness)
QD3. Are the measurements appropriate? (Check: variables clearly defined and accurately measured)
QD4. Is the risk of nonresponse bias low? (Check: response rate, reasons for nonresponse, statistical compensation like imputation)
QD5. Is the statistical analysis appropriate to answer the research question? (Check: analysis stated and justified for the design)

**Mixed methods integration criteria (MM 1-5):**
MM1. Is there an adequate rationale for using a mixed methods design to address the research question?
MM2. Are the different components of the study effectively integrated to answer the research question? (Check: integration rather than parallel use only)
MM3. Are the outputs of the integration of qualitative and quantitative components adequately interpreted?
MM4. Are divergences and inconsistencies between quantitative and qualitative results adequately addressed? (Check: explicit handling of divergences)
MM5. Do the different components of the study adhere to the quality criteria of each tradition of the methods involved? (Check: rate the relevant qualitative and quantitative component criteria as well)

**Key guidance for Design Science Research:** No standard checklist fully covers DSR. Do not route every DSR paper automatically to MMAT. Ask whether the study actually integrates qualitative and quantitative components, in which case MMAT may be appropriate, or whether a cross-design appraisal of methodological and reporting quality is needed, in which case QuADS may be more informative. In either case, add an explicit note that a specialized framework such as FEDS (Venable, Pries-Heje, and Baskerville, 2016) may be more appropriate for formal DSR evaluation.

---

## Checklist 7: QuADS 2021 (Quality Assessment for Diverse Studies)

**Use when:** The researcher needs a single criterion-based appraisal of methodological and reporting quality across a diverse multi- or mixed-method corpus. Do not use QuADS as a mechanical substitute for MMAT when explicit mixed-methods integration is the central appraisal question.

**Response scale:** 0 = no mention or absent, 1 = minimal or broad evidence, 2 = partial or adequate evidence, 3 = detailed and well-supported evidence. Apply the official score descriptors for each criterion. Do not use a total score as a high/low-quality cut-off or as an automatic exclusion rule.

1. **Theoretical or conceptual underpinning to the research.** Check whether concepts or theories are named and whether they actually inform the design, materials, or outcomes. Score 0 for no mention, 1 for broad reference, 2 for identified concepts with some link to the work, and 3 for explicit application throughout the study.
2. **Statement of research aim/s.** Check whether the main body has an explicit, detailed aim statement. Score 0 for no stated aim, 1 for an implied aim, 2 for an aim limited to the abstract or lacking detail, and 3 for a detailed main-text statement.
3. **Clear description of research setting and target population.** Check the specific setting and target population. Score 0 for no description, 1 for only a broad research area, 2 for a setting description with missing detail, and 3 for a specific setting and target population.
4. **The study design is appropriate to address the stated research aim/s.** Compare the stated aims and design. Score 0 when no aim is stated or the design is unsuitable, 1 when only some aspects can be addressed, 2 when the design can answer the aim but a stronger alternative is apparent, and 3 when the design appears the most suitable available approach.
5. **Appropriate sampling to address the research aim/s.** Check how sample, cases, or sites were selected and justified. Score 0 for no sampling approach, 1 for basic consideration of sample characteristics, 2 for consideration linked to the aims, and 3 for detailed sample-size, iterative-sampling, or case-selection justification linked to the aims.
6. **Rationale for choice of data collection tool/s.** Check why each tool was selected. Score 0 for no rationale, 1 for minimal explanation such as availability, 2 for a basic rationale such as prior similar use, and 3 for a detailed rationale linked to study aims, co-design, target population, or tool quality.
7. **The format and content of data collection tool is appropriate to address the stated research aim/s.** Check whether the instrument format and content can elicit the required data. Score 0 when tools or aims are not described, 1 for superficial fit, 2 for broad fit with a plausible need for refinement, and 3 when the tools allow detailed data on all relevant aspects of the aim.
8. **Description of data collection procedure.** Check when, where, and how collection occurred. Score 0 for no procedure, 1 for a brief outline, 2 for stages described with material gaps, and 3 for sufficiently detailed procedures that another researcher could follow them.
9. **Recruitment data provided.** Check numbers approached, invited, recruited, completed, and attrition where relevant. Score 0 for no recruitment data, 1 for minimal figures, 2 for incomplete but meaningful figures, and 3 for a full recruitment account with attrition explained.
10. **Justification for analytic method selected.** Check why the analytic approach fits the study. Score 0 for no rationale, 1 for a minimal rationale, 2 for basic reference to prior similar work, and 3 for detailed justification linked to the aims or the method's strengths.
11. **The method of analysis was appropriate to answer the research aim/s.** Compare the analysis with the aims. Score 0 for no reported analysis, 1 for only basic or broad fit, 2 for adequate fit with a stronger plausible alternative, and 3 when the analysis appears the most suitable approach for answering the aims in detail.
12. **Evidence that research stakeholders have been considered in research design or conduct.** Check for target-population, advisory-group, pilot, or stakeholder input. Score 0 for no mention, 1 for limited consideration without planning-stage involvement, 2 for input that influenced design or conduct, and 3 for substantial identifiable consultation throughout planning or preliminary work.
13. **Strengths and limitations critically discussed.** Check whether the discussion addresses design, methods, tools, sample, and analysis. Score 0 for no discussion, 1 for very limited discussion, 2 for some key strengths and weaknesses with omissions, and 3 for a thorough critical discussion across the study.

**QuADS team guidance:** Before corpus-wide scoring, review teams should independently apply QuADS to the same 3 to 5 papers, discuss differences, and document their shared application rules. The tool's 13 criteria are unweighted. Report patterns across individual criteria narratively rather than treating a summary score as a decision rule.

**Source:** Harrison, Jones, Gardner, and Lawton (2021), official QuADS Criteria and User Guide v1.0, supplementary files to https://doi.org/10.1186/s12913-021-06122-y.
