# Academic Research Skills for Claude

Seven [Agent Skills](https://agentskills.io) focused on academic literature search, corpus screening, methodological quality appraisal, bibliometric science mapping, evidence synthesis, claim verification, and journal credibility checking — built to actively minimize citation hallucination and cognitive outsourcing rather than just produce plausible-looking output.

The skills form a deliberate pipeline: `verified-paper-search` retrieves and maps the literature via OpenAlex, `journal-quality-check` audits venue credibility, `corpus-screening` applies user-defined inclusion/exclusion criteria to produce the final corpus, `study-quality-assessment` appraises the methodological quality of each included paper using CASP, JBI, and MMAT checklists, `bibliometric-scientometric-analysis` generates visual science mapping and network analyses, `deep-academic-synthesis` takes the researcher from abstract-level mapping to full-text section-by-section synthesis with the human in control of the intellectual architecture, and `scientific-reference-reviewer` validates individual claims.

## Skills in this repo

The pipeline runs in the order shown in the table below. Each skill is self-contained but designed to receive the output of the preceding stage.

| # | Skill | What it does |
|---|---|---|
| 1 | [`plugins/academic-research-tools/skills/verified-paper-search`](plugins/academic-research-tools/skills/verified-paper-search) | Finds and verifies academic papers using the **OpenAlex API exclusively**, with structured Boolean search strategy, user-approved protocol, relevance scoring, integrated journal quality assessment, and mandatory OpenAlex JSON export for downstream bibliometric analysis. Produces a Markdown deliverable with the search strategy, systematic mapping table, and preliminary abstract-level evidence summary. |
| 2 | [`plugins/academic-research-tools/skills/journal-quality-check`](plugins/academic-research-tools/skills/journal-quality-check) | Checks whether a journal is currently indexed in Redalyc/AmeliCA, SciELO, Scopus, Web of Science, or MEDLINE/PubMed, evaluates a journal against those indexers' admission criteria for self-assessment before submission, and flags predatory-journal warning signs. |
| 3 | [`plugins/academic-research-tools/skills/corpus-screening`](plugins/academic-research-tools/skills/corpus-screening) | Guides the researcher through title and abstract screening against user-defined inclusion/exclusion criteria. Presents papers one by one (or in batches), supports AI pre-flagging with transparent reasoning, handles a second-pass review of Uncertain papers, and exports the screened corpus to CSV for use in subsequent pipeline stages. |
| 4 | [`plugins/academic-research-tools/skills/study-quality-assessment`](plugins/academic-research-tools/skills/study-quality-assessment) | Appraises the methodological quality of each included paper using full-text batch reading and field-calibrated checklists: CASP Qualitative (2024), CASP Cross-Sectional (2024), JBI Quasi-Experimental (2024), JBI Analytical Cross-Sectional (2025), CASP Systematic Review (2024), and MMAT 2018. Applies field-specific calibration rules for non-health research. Produces individual appraisal records and a consolidated quality matrix exported to CSV. |
| 5 | [`plugins/academic-research-tools/skills/bibliometric-scientometric-analysis`](plugins/academic-research-tools/skills/bibliometric-scientometric-analysis) | Takes the OpenAlex JSON corpus exported by `verified-paper-search` and generates visual science mapping using pyBibX. Offers nine analysis groups (descriptive/EDA, author analysis, source analysis, geographic analysis, keyword co-occurrence, citation analysis, network analysis, strategic indicators, and topic modelling via spaCy and Gensim LDA). Produces interactive HTML plots and a Markdown report with data-grounded interpretive commentary. |
| 6 | [`plugins/academic-research-tools/skills/deep-academic-synthesis`](plugins/academic-research-tools/skills/deep-academic-synthesis) | Takes the corpus produced by `verified-paper-search` and synthesizes it in depth using a three-stage, human-in-control model: (1) AI-generated corpus overview from split PDFs read in 4-page batches, (2) user-driven thematic agenda setting with AI evidence feedback, and (3) incremental prose generation approved section by section. Enforces strict language constraints (no promotional adjectives, no artificial copulas) and anti-hallucination rules throughout. |
| 7 | [`plugins/academic-research-tools/skills/scientific-reference-reviewer`](plugins/academic-research-tools/skills/scientific-reference-reviewer) | Builds a strict, auditable evidence base for one specific scientific/technical claim: explicit 8-tier source classification, exact-location excerpt anchors, and no synthesized conclusion — leaves the final call to the human writer. |

All seven ship together as one plugin, `academic-research-tools`, so one install command gets you all of them. Each skill is still self-contained (its own `SKILL.md` + `references/`) if you'd rather copy out just one.

## Installing in Claude Code (recommended: plugin marketplace)

This repo is set up as a Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces), so installing — and later updating — is two commands, run inside a Claude Code session:

```
/plugin marketplace add luisaunb-star/academic-research-skills
/plugin install academic-research-tools@academic-research-skills
```

That installs all three skills at once. To update later, after you've pushed changes to this repo:

```
/plugin marketplace update academic-research-skills
```

To remove it:

```
/plugin uninstall academic-research-tools@academic-research-skills
```

### Manual install (no marketplace, just copy the files)

If you'd rather not use the plugin system, the skills are plain folders and work the same way copied directly into Claude Code's skills directories:

- **Personal** — available in every project on your machine: `~/.claude/skills/`
- **Project** — lives in one repo, shareable with your team via git: `<your-project>/.claude/skills/`

```bash
git clone https://github.com/luisaunb-star/academic-research-skills.git
mkdir -p ~/.claude/skills

cp -r academic-research-skills/plugins/academic-research-tools/skills/verified-paper-search              ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/journal-quality-check               ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/corpus-screening                    ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/study-quality-assessment            ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/bibliometric-scientometric-analysis ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/deep-academic-synthesis             ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/scientific-reference-reviewer       ~/.claude/skills/
```

Either way — marketplace or manual copy — Claude Code discovers the skills automatically at the start of a session. No restart, no separate registration step.

## Installing in claude.ai (web/desktop)

claude.ai uses a separate, zip-upload-based mechanism (Settings/Customize → Skills) that isn't connected to GitHub or to the plugin system above. GitHub doesn't let you download a single subfolder as a zip, so zip it yourself after cloning:

```bash
cd academic-research-skills/plugins/academic-research-tools/skills/verified-paper-search
zip -r verified-paper-search.zip .
```

Then upload `verified-paper-search.zip` under **Customize → Skills → "+" → Upload a skill**. Repeat per skill you want there. Requires Code execution and file creation enabled in Settings → Capabilities.

## A note on `corpus-screening`

This skill requires no additional Python packages. It works with CSV, Excel, plain text, BibTeX, or RIS input from `verified-paper-search`. The exported `screened_corpus.csv` is the recommended input for `study-quality-assessment` and `bibliometric-scientometric-analysis`. The skill is designed for title and abstract screening only; full-text screening decisions should be made using `study-quality-assessment`.

## A note on `study-quality-assessment`

This skill requires no additional Python packages beyond those used by `split-pdf`. It embeds all six checklists (CASP Qualitative 2024, CASP Cross-Sectional 2024, JBI Quasi-Experimental 2024, JBI Analytical Cross-Sectional 2025, CASP Systematic Review 2024, and MMAT 2018) with detailed per-item guidance. The exported `quality_appraisal_matrix.csv` can be opened directly in Excel or Google Sheets and included in the Methods section of a review manuscript.

## A note on `bibliometric-scientometric-analysis`

This skill requires **pyBibX** (`pip install pybibx`), which it installs automatically. Topic modelling (Group 9) uses spaCy and Gensim LDA, which the skill also installs. The skill takes as input the `openalex_corpus.json` file exported by `verified-paper-search` in Step 4. If you applied `journal-quality-check` or `corpus-screening` exclusions, ensure those papers are removed from the JSON before passing it to this skill.

## A note on `deep-academic-synthesis`

This skill requires the `split-pdf` skill to be available in your skills directory, as it calls `split-pdf/scripts/split_pdf.py` to read PDF full texts in 4-page batches. If you install via the plugin marketplace, ensure `split-pdf` is also installed. If you install manually, copy it alongside the others. The skill also requires `PyPDF2`, which it will install automatically via `sudo pip3 install PyPDF2` if not already present.

## A note on `verified-paper-search`

That skill bundles `scripts/lookup.py`, which calls the public OpenAlex and Semantic Scholar APIs (standard library only, no `pip install` needed). It needs outbound network access from Claude Code's bash — which Claude Code has by default. In sandboxed environments without that (some claude.ai code-execution contexts), the skill falls back to calling the same endpoints via `web_fetch` instead — see that skill's `references/search_apis.md`.

## Maintaining this repo

Before pushing changes, validate the marketplace and plugin manifests from a Claude Code session in this repo:

```
claude plugin validate .
claude plugin validate ./plugins/academic-research-tools
```

To test a change before publishing it, add the marketplace from your local working copy instead of from GitHub:

```
/plugin marketplace add ./academic-research-skills
/plugin install academic-research-tools@academic-research-skills
```

Bump `version` in both `plugins/academic-research-tools/.claude-plugin/plugin.json` and the matching entry in `.claude-plugin/marketplace.json` on every release people should actually receive — Claude Code only re-fetches an installed plugin when that string changes.

## Before you install any skill from anywhere

Skills can include executable code and can influence how Claude behaves. Read the `SKILL.md` and any bundled scripts before installing one — from this repo or anyone else's. These three are provided as-is; review them the same way you'd review any third-party code.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Skills are plain Markdown plus optional reference files and scripts. PRs welcome — please test changes against a few realistic prompts before submitting, and keep each skill focused on one job rather than expanding scope into another skill's territory.
