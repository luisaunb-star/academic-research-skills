# Academic Research Skills for Claude

Three [Agent Skills](https://agentskills.io) focused on academic literature search, claim verification, and journal credibility checking — built to actively minimize citation hallucination rather than just produce plausible-looking output.

## Skills in this repo

| Skill | What it does |
|---|---|
| [`skills/verified-paper-search`](skills/verified-paper-search) | Finds and independently verifies academic papers for a topic or a specific claim, using the OpenAlex and Semantic Scholar APIs before falling back to free-text web search. Produces a markdown deliverable with the search strategy, verified papers, and (for claim requests) an explicit supported/contradicted/mixed verdict. |
| [`skills/journal-quality-check`](skills/journal-quality-check) | Checks whether a journal is currently indexed in Redalyc/AmeliCA, SciELO, Scopus, Web of Science, or MEDLINE/PubMed, evaluates a journal against those indexers' admission criteria for self-assessment before submission, and flags predatory-journal warning signs. |
| [`skills/scientific-reference-reviewer`](skills/scientific-reference-reviewer) | Builds a strict, auditable evidence base for one specific scientific/technical claim: explicit 8-tier source classification, exact-location excerpt anchors, and no synthesized conclusion — leaves the final call to the human writer. |

Each skill is self-contained (its own `SKILL.md` + `references/`), so you can install just the one(s) you need.

## Installing in Claude Code

Skills are filesystem-based in Claude Code — no upload step. Clone this repo, then copy (or symlink) whichever skill(s) you want into one of:

- **Personal** — available in every project on your machine: `~/.claude/skills/`
- **Project** — lives in one repo, shareable with your team via git: `<your-project>/.claude/skills/`

```bash
git clone https://github.com/<you>/<this-repo>.git
mkdir -p ~/.claude/skills

cp -r <this-repo>/skills/verified-paper-search        ~/.claude/skills/
cp -r <this-repo>/skills/journal-quality-check         ~/.claude/skills/
cp -r <this-repo>/skills/scientific-reference-reviewer ~/.claude/skills/
```

Prefer a symlink instead of `cp -r` if you want `git pull` in this repo to keep your installed copy current:

```bash
ln -s "$(pwd)/<this-repo>/skills/verified-paper-search" ~/.claude/skills/verified-paper-search
```

That's it — Claude Code discovers skills from those directories automatically at the start of a session. No restart command, no registration step.

## Installing in claude.ai (web/desktop)

claude.ai uses a separate, zip-upload-based mechanism (Settings/Customize → Skills) and isn't connected to this repo automatically. GitHub doesn't let you download a single subfolder as a zip, so zip it yourself after cloning:

```bash
cd <this-repo>/skills/verified-paper-search
zip -r verified-paper-search.zip .
```

Then upload `verified-paper-search.zip` under **Customize → Skills → "+" → Upload a skill**. Repeat per skill you want there. Requires Code execution and file creation enabled in Settings → Capabilities.

## A note on `verified-paper-search`

That skill bundles `scripts/lookup.py`, which calls the public OpenAlex and Semantic Scholar APIs (standard library only, no `pip install` needed). It needs outbound network access from Claude Code's bash — which Claude Code has by default. In sandboxed environments without that (some claude.ai code-execution contexts), the skill falls back to calling the same endpoints via `web_fetch` instead — see that skill's `references/search_apis.md`.

## Before you install any skill from anywhere

Skills can include executable code and can influence how Claude behaves. Read the `SKILL.md` and any bundled scripts before installing one — from this repo or anyone else's. These three are provided as-is; review them the same way you'd review any third-party code.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Skills are plain Markdown plus optional reference files and scripts. PRs welcome — please test changes against a few realistic prompts before submitting, and keep each skill focused on one job rather than expanding scope into another skill's territory.
