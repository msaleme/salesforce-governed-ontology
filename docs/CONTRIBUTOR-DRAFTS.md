# Contributor and recording drafts

These are draft issue bodies, not created GitHub issues. Suggested label:
`good first issue`. The recording outline is not a published video.

## Draft issue: Add a custom inventory metric example

**Goal:** demonstrate `sgo byod` with a non-finance count metric.

**Scope:** one synthetic example JSON and a short explanation of its grain/unit.
Include accepted, denied and expired cases; use full expected results.

**Acceptance:** the example runs offline from an installed wheel, all cases pass,
a wrong-source expectation fails, and `scripts/verify.py` stays green. Do not add
a connector or imply source accuracy.

## Draft issue: Check local Markdown anchors

**Goal:** extend the existing link verifier to catch missing heading fragments.

**Scope:** local `.md` links only; support GitHub-style duplicate heading IDs and
ignore fenced code. No network crawling or new posting workflow.

**Acceptance:** tests show a valid heading passes and a broken fragment fails;
existing links remain valid; diagnostics identify file and target.

## Draft issue: Add a machine-readable schema inspection command

**Goal:** allow `sgo schema` to print the bundled ontology schema for local tooling.

**Scope:** read the packaged resource, output JSON, document it in CLI help.

**Acceptance:** output equals the packaged schema, works outside the checkout,
and preserves existing command exit codes. No schema downloading at runtime.

## Short demo recording outline (approximately 3 minutes)

1. **0:00-0:20 - The problem.** Display the eight verdicts. Say: “A difference is
   arithmetic. An explanation needs evidence.” Identify the demo as offline.
2. **0:20-0:55 - Clarify and bind.** Run `sgo scenario ambiguity`, then
   `sgo scenario binding-mismatch`. Show definition selection and wrong-source refusal.
3. **0:55-1:30 - Difference versus explanation.** Run `sgo scenario difference-only`
   and `sgo scenario explained`; highlight the separate bridge source.
4. **1:30-2:20 - Your definitions.** Open `examples/user-metrics.json`; show its
   custom ID, grain, unit and authored expectations. Run `sgo byod` on that file.
   In a temporary copy change an expected operation, rerun and show exit 1.
5. **2:20-3:00 - Reproduce and delimit.** Run `python3 scripts/verify.py`; show the
   assurance guide and MIT license. State that passing authored cases is not
   live platform validation or authenticated authorization.

Before recording: install from the reviewed commit, use only synthetic files,
keep tokens and other windows offscreen, verify all commands, and record the
commit/Python version. Save locally for review; do not upload without approval.
