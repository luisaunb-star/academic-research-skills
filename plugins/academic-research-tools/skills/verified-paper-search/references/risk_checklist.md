# Why citation hallucination happens (and what each workflow step counters)

This is background, not a checklist to recite to the user — read it when you want the reasoning behind a workflow step, or when the user asks "why are you being so careful about this." Each item below is a well-documented mechanism, not a deep-dive theory; this file stays useful precisely by sticking to what's actually established rather than dressing it up.

## 1. Generation doesn't have an "I don't know" button by default
Autoregressive models are trained to keep producing the next plausible token. Nothing in that objective rewards stopping to say "I'm not sure this paper exists." Once a model starts a sentence shaped like a citation, finishing it with *something* is the path of least resistance — and a fluent, well-formatted fake is statistically indistinguishable from a real one until someone checks it against a source.

**Workflow countermeasure:** Step 3 — no citation enters the output unless it was surfaced by a live search this turn. Step 4 — every candidate gets an independent second check before it's presented as real.

## 2. Long-tail topics get "filled in" from pattern, not fact
Frequently-discussed entities (well-known authors, landmark papers, major journals) are represented with high fidelity in a model's training. Niche sub-specialties, recent terms, or cross-disciplinary jargon are sparsely represented — so when asked about them, a model tends to generalize from surface patterns (similar-sounding terms, common author/venue combinations) rather than recalling an actual fact, because it has little actual fact to recall.

**Workflow countermeasure:** Step 1 explicitly flags long-tail/niche topics as higher-risk before searching even begins, so the rest of the workflow treats them with extra scrutiny rather than business-as-usual.

## 3. Confirming a claim is easier (and more rewarded) than checking it
Models tuned with human feedback learn that confident, agreeable answers tend to score better with raters than hedged or contradicting ones — this is documented as sycophancy, and it generalizes naturally to "find me a citation for what I already believe." If you only search to confirm a claim, you'll usually find *something* that pattern-matches, whether or not it actually supports the claim once you read past the headline.

**Workflow countermeasure:** Step 2 requires generating disconfirming search angles, not just confirming ones. Step 5 requires stating the actual verdict (including "contradicted" or "mixed") rather than defaulting to agreement.

## 4. Evaluation regimes that punish "I don't know" produce more confident fabrication
This is a documented finding in how language models are scored: benchmarks that grade strictly on accuracy give zero credit for an honest abstention but partial credit (by chance) for a guess — so training and evaluation pressure pushes toward guessing over admitting uncertainty. The same dynamic shows up in citation search: a thin, honest "I found 2 verified sources, not 8" feels like a worse answer to produce than a padded list, even though it's the more useful one.

**Workflow countermeasure:** Step 4 explicitly treats a short, fully-verified list as a successful outcome, not a failure to compensate for. The "Found but unverified" section in the output template makes thinness visible and explicit rather than something to quietly paper over.

## 5. Plausible combinations of true facts are still fabrications
A model can correctly "know" that an author exists, that a journal exists, and that a topic is associated with both — and still combine them into a paper that was never written. Each fragment is true; the combination is invented. This is the specific failure mode that makes citation hallucination so convincing: it doesn't look like an error, because no individual piece of it is wrong.

**Workflow countermeasure:** Step 4's verification isn't "does this author exist" or "does this journal exist" — it's "does *this exact combination* exist," checked against a source that states the combination directly (a DOI page, an indexed listing), not reconstructed from separately-true pieces.

## 6. Retrieval helps a lot, but doesn't fully solve it
Grounding generation in retrieved/searched documents substantially reduces fabrication compared to generating from parametric memory alone — but it doesn't eliminate it. A model can still misread a retrieved snippet, miss that two snippets describe different papers, or quietly extrapolate beyond what a fetched page actually says. Retrieval is necessary here, not sufficient.

**Workflow countermeasure:** This is why Step 4 requires a *second*, independent confirmation rather than treating "I found it via search" as the finish line.
