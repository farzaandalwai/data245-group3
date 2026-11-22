# SAS development integration request

User authorization, recorded with Markdown escaping normalized:

Continue my DATA 245 work as SAS/Farzaan. Complete the next integration steps,
preserving teammates’ work and original experiment evidence.

First read AGENTS.md, fetch origin, inspect the working tree, and read the latest
context.md and relevant handoffs. Verify the current status of PRs #4 and #6
rather than relying on earlier summaries. Preserve all local changes and work
on a new SAS task branch from the appropriate current base.

Scope:

1. Share my original SAS outputs. Locate the original real-development Decision
Tree predictions, metrics, bootstrap outputs, and run metadata. Validate their
provenance and upload the small shareable artifacts through Git using the
repository’s conventions. Record checksums and reproduction commands. Preserve
the originals; do not silently replace them with reruns. If anything is missing,
identify it precisely.
2. Review and integrate Shoury’s outputs. Inspect PR #6 and its handoff. Use an
isolated checkout if it is unmerged. Validate the predictions against DELTA’s
exact development bundle: file hashes, target keys, split, actual values,
feature conditions, coverage, duplicates, missing values, and prediction policy.
Integrate compatible predictions into the shared evaluator without rewriting
or retraining Shoury’s models.
3. Resolve evaluation differences. Compare bootstrap methods, confidence levels,
seeds, replicate counts, weighting, difference direction, and run metadata.
Follow the latest agreed protocol. Our SAS implementation previously used 95%
paired whole-store bootstrap intervals, seed 245, 2,000 replicates, with difference
defined as stockout-aware minus sales-only. Preserve original results. Write any
harmonized evaluation into a separate, clearly labeled run. Distinguish mechanical
metadata/schema fixes from scientific choices requiring team agreement. Do not
invent provenance or silently declare a proposed setting approved. Continue
independent work if one decision remains blocked.
4. Produce development comparisons. Run all compatible available model predictions
through the same evaluator on identical development rows. Include the matched
simple baselines if available. Export a concise comparison table containing MAE,
RMSE, signed bias, mean underprediction, mean overprediction, and paired MAE
differences with confidence intervals. Record row/store counts and relevant
subgroup results. Create a small set of clear development figures, including
model MAE and paired MAE differences with confidence intervals. Label everything
DEVELOPMENT, not final-test evidence. Report negative or uncertain findings honestly.
5. Prepare the final evaluation handoff. Document what is ready and exactly what
still needs team agreement before final scoring: model settings, feature lists,
preprocessing, clipping policy, tie rules, eligibility, metrics, and bootstrap
settings. Prepare or verify the final-evaluation commands without executing final
test scoring or inspecting new test outcomes. Do not expand the model search to
chase improvement.
6. Verify and publish. Run relevant tests and integrity checks. Update context.md,
contribution records, AI disclosures, and a concise integration handoff with
evidence paths, commands, findings, and blockers. Inspect the diff, stage only
intended SAS integration files, commit, push, and open a PR. Do not merge PRs or
modify teammates’ original outputs.

Proceed through all available steps without stopping after a plan. Ask only if
a missing scientific decision truly blocks dependent work. Finish with a short
summary of completed work, development findings, remaining blockers, PR link,
and the next action needed from each teammate.
