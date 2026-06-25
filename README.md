# Academic Research Skills for Claude

Three [Agent Skills](https://agentskills.io) focused on academic literature search, claim verification, and journal credibility checking — built to actively minimize citation hallucination rather than just produce plausible-looking output.

## Skills in this repo

| Skill | What it does |
|---|---|
| [`plugins/academic-research-tools/skills/verified-paper-search`](plugins/academic-research-tools/skills/verified-paper-search) | Finds and independently verifies academic papers for a topic or a specific claim, using the OpenAlex and Semantic Scholar APIs before falling back to free-text web search. Produces a markdown deliverable with the search strategy, verified papers, and (for claim requests) an explicit supported/contradicted/mixed verdict. |
| [`plugins/academic-research-tools/skills/journal-quality-check`](plugins/academic-research-tools/skills/journal-quality-check) | Checks whether a journal is currently indexed in Redalyc/AmeliCA, SciELO, Scopus, Web of Science, or MEDLINE/PubMed, evaluates a journal against those indexers' admission criteria for self-assessment before submission, and flags predatory-journal warning signs. |
| [`plugins/academic-research-tools/skills/scientific-reference-reviewer`](plugins/academic-research-tools/skills/scientific-reference-reviewer) | Builds a strict, auditable evidence base for one specific scientific/technical claim: explicit 8-tier source classification, exact-location excerpt anchors, and no synthesized conclusion — leaves the final call to the human writer. |

All three ship together as one plugin, `academic-research-tools`, so one install command gets you all of them. Each skill is still self-contained (its own `SKILL.md` + `references/`) if you'd rather copy out just one.

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

cp -r academic-research-skills/plugins/academic-research-tools/skills/verified-paper-search        ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/journal-quality-check         ~/.claude/skills/
cp -r academic-research-skills/plugins/academic-research-tools/skills/scientific-reference-reviewer ~/.claude/skills/
```

Either way — marketplace or manual copy — Claude Code discovers the skills automatically at the start of a session. No restart, no separate registration step.

## Installing in claude.ai (web/desktop)

claude.ai uses a separate, zip-upload-based mechanism (Settings/Customize → Skills) that isn't connected to GitHub or to the plugin system above. GitHub doesn't let you download a single subfolder as a zip, so zip it yourself after cloning:

```bash
cd academic-research-skills/plugins/academic-research-tools/skills/verified-paper-search
zip -r verified-paper-search.zip .
```

Then upload `verified-paper-search.zip` under **Customize → Skills → "+" → Upload a skill**. Repeat per skill you want there. Requires Code execution and file creation enabled in Settings → Capabilities.

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
