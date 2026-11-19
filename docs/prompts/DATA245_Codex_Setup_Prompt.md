# DATA 245 Group 3 — Codex setup prompt

Use this once in Farzaan's Codex. Open an empty local folder named `data245-group3` in Codex, then paste everything after the horizontal rule. You do not need to create a GitHub repository first. If you already have a project folder, open it instead; preserve all existing work. This prompt sets up collaboration and imports existing work. It does not authorize implementing the remaining experiments.

After setup, teammates accept the GitHub invitations, clone the repository into their own local folders, open it in Codex, and paste the generated `starter_prompt.md`. Connecting GitHub alone does not synchronize uncommitted work or merge branches.

---

You are setting up our DATA 245 Machine Learning group project. Carry out the setup, rather than only describing it. Keep the repository understandable to students. Work only on repository setup, documentation, and importing existing team artifacts for now. Do not train new models, create new features, run the full data pipeline, generate final findings, or write the final individual reports in this task.

## 1. Repository and collaborators

- Preferred GitHub repository name: `data245-group3`. Display title: `DATA 245 — Group 3: Stockout-Aware Forecasting`.
- Create it as a PRIVATE repository under the currently authenticated user's personal GitHub account. Discover the actual account; never guess Farzaan's GitHub username or choose an organization without instruction.
- Invite exactly `shoddy16` and `timothytran109` with collaborator write/push access. Do not grant admin access. This prompt authorizes creating the repo and sending these repository invitations.
- Use available GitHub tools or authenticated `gh`. Inspect the current directory, `git status`, remotes, and authenticated account first. Never overwrite another project or repoint an unrelated remote. If the name already exists, inspect it and reuse it only if it is clearly this project; otherwise ask one focused question.
- Validate the two GitHub accounts exist, send missing invitations, then read back collaborator/pending-invitation status. Report `pending` separately from `accepted`. Do not claim they can access a private repo until access is accepted/verified.
- If authentication or GitHub tooling is unavailable, complete the local kit anyway, report the exact blocker, and give the shortest remaining commands. Never claim a local repository is already on GitHub. Do not print credentials or tokens.
- The initial bootstrap commit may initialize `main`. Subsequent contributions go through task branches and pull requests. Configure protection against force pushes, PR review, and one approval if supported by the current account/repo plan. If unavailable, document that protection is a team convention, not an enforced rule. Do not change visibility or buy a plan to enable it.
- Do not add AI co-author trailers or fabricate authorship for imported teammate work. Attribute imported files through provenance documentation.

## 2. Actual project and truthful starting point

Project: **Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail.**

Research question: Does adding historical stockout information improve next-day recorded normalized sales forecasts beyond recent sales history, with everything else held matched?

Dataset: FreshRetailNet-50K. Predict `sale_amount` per `(store_id, product_id, dt)`. Recorded sales are not unrestricted latent demand, kilograms, revenue, or measured food waste. Better forecasts might support stocking and SDG 12, especially food-waste prevention, but environmental benefits have not been measured.

We are starting the unfinished modeling and integration from a clean, organized repository. We are NOT pretending that existing team work never happened. Preserve it and its original attribution.

The shared folder is:
https://drive.google.com/drive/folders/1_saUNK4VOT7vpbSjiCw2XKIOpWa3IkHy

Reviewed handoff says Timothy Tran completed preparation and sales-only baselines. Source files, an audit, and a metrics CSV are present. Their presence and contents were reviewed while preparing this prompt; the full raw-data pipeline was NOT independently rerun. All new implementation and formal verification must be described at its actual status.

Inherited audit reports: 1,459,198 raw rows, 19 columns, 90 dates from 2024-03-28 through 2024-06-25, 16,214 store-product series; 16,213 complete 90-day series and one incomplete 28-day series `(420, 764)` excluded; no nulls or duplicate keys reported. These describe the LOCAL EXPORT, not the entire published dataset.

Pilot: seed 245, fixed manifest of 200 complete series, 18,000 rows. Reuse the actual manifest rather than resampling.

| Split | Days | Dates | Rows before lag/eligibility filtering |
|---|---|---|---:|
| Train | 1–60 | 2024-03-28 to 2024-05-26 | 12,000 |
| Validation | 61–75 | 2024-05-27 to 2024-06-10 | 3,000 |
| Test | 76–90 | 2024-06-11 to 2024-06-25 | 3,000 |

Inherited baseline metrics, saved to six decimals, on ALL 3,000 rows per validation/test split:

| Model | Split | MAE | RMSE | Signed bias |
|---|---|---:|---:|---:|
| Persistence, yesterday's sales | Validation | 0.417757 | 0.677441 | +0.002357 |
| Persistence | Test | 0.444063 | 0.697380 | -0.002777 |
| Mean of preceding seven days | Validation | 0.337380 | 0.551965 | -0.007276 |
| Mean of preceding seven days | Test | 0.362622 | 0.564407 | -0.051647 |

These are inherited team baseline results, not results of the stockout-aware comparison. Do not describe them as independently reproduced unless actually rerun later. Original baseline test scores are already visible; do not claim that no one has seen any test results.

The original handoff identifies five project members. Invite only the two accounts provided, but preserve all five academic roles below as historical/planned assignments, with completion recorded separately:

| Member | Existing or planned responsibility |
|---|---|
| Timothy Tran | Existing preparation, pilot, baseline work; reproduction support |
| Farzaan Dalwai | Experiment protocol, integration, formal leakage audit, evaluation and bias analysis |
| Shoury Ambarish Parab | Linear regression and ridge experiments |
| Denisha Tank | Decision-tree experiments, optional random forest |
| Mansi | Historical stockout features, optional context-length comparisons |

`timothytran109` was supplied for Timothy. `shoddy16` was supplied as another collaborator, but do not infer its full-name mapping. Leave any unconfirmed mapping unconfirmed. Do not redistribute the five-person workload simply because three GitHub accounts are initially involved.

## 3. Import the existing work carefully

Use Drive access if available. If not, inspect only user-provided local project files for the matching handoff; otherwise provide a precise download checklist and leave unavailable files marked missing. Do not bypass access controls or invent file contents.

Verified source IDs, filenames, and expected byte sizes at review time:

| Source | Drive ID | Bytes |
|---|---|---:|
| README.md | 1s4QCLKaMtMlyQXNMzqNr-SqGCCaN7hJm | 23,414 |
| prepare_and_baselines.py | 1jXMsK0fI0s2ofzvJmgX9Kdt20HAzpUwa | 7,958 |
| prepare_and_baselines.ipynb | 1UCl-qTyEnL8PFfnVH6kmFTXeiqbSX4kr | 51,210 |
| data_explore.py | 1mnInCx3wX1WN8-G0xIMimQssWbgYiRbW | 299 |
| pilot_200_series.csv | 18tq2qwOTpe4ViAQ_KowK0zsl9aZAw1RS | 4,530,605 |
| pilot_series_manifest.csv | 1vxeoaH9ztGB9O3krxgCyaaue7xIByO47 | 1,738 |
| excluded_series.csv | 11HF5MPpiqHXId2tPmAz_q6Rzu950utbe | 775 |
| data_audit.txt | 1X-GjOXS9qZOzuS4indgQHoxVFLhuNzgB | 1,554 |
| baseline_metrics.csv | 1KXGtfJJaczk2IyAW4FO0bOvWwQjGCvZZ | 259 |
| baseline_predictions.csv | 1TNVSGdXWIK6ZlooaLg8fuZWXyfUqN5aP | 697,664 |
| freshretail.csv | 1A0nGSmtUDzAi_AGHYbuoxzNub4yLcubL | 323,577,557 |

Resolve files by current folder metadata before downloading; sizes may change. Use exact returned canonical links or IDs. The handoff README is UTF-16 with a BOM: decode properly. Preserve its original bytes and provide a UTF-8 reading copy if helpful; record that conversion.

- Preserve the original relative layout for imported code: `data_prep_pipeline/`, `data/processed/`, and `results/`. The Python script resolves its root from its own file path and expects `data/freshretail.csv`. Do not relocate it and silently break this path.
- Archive the original handoff README in `docs/handoff/`; write a separate root project README. Preserve baseline files without overwriting them with later runs.
- The raw CSV is about 324 MB: do not put it in Git or Git history, and do not download it just to bootstrap this kit. Document its source and local destination in `data/README.md`.
- Ignore raw data, virtual environments, caches, secrets, model binaries, and bulky generated runs. Keep explicit exceptions for the small existing pilot CSV, manifest, exclusions, and baseline artifacts if dataset redistribution terms allow them. Verify source attribution/license before committing dataset extracts; otherwise track acquisition instructions plus checksums instead. Do not apply a blanket code license to teammates' code or third-party data.
- Record source URL/ID, import time, local destination, byte count, SHA-256, original author as stated by source, and verification status in `docs/provenance.md`. Do not fabricate a checksum for an unavailable file.
- Inspect imported scripts/notebook cells before running anything. During this setup, limit checks to file readability, safe syntax/JSON parsing, schemas, manifest consistency, unique keys, and split counts. Do not execute the full notebook or new experiments.

## 4. The collaboration kit to create

Create these files with useful project-specific content. Avoid extra frameworks, a web app, elaborate orchestration, and unnecessary empty scaffolding.

1. `README.md`: what we are testing, honest status, environment/data setup, source links, collaboration steps, and exact verified commands. Label unrun commands as unverified.
2. `AGENTS.md`: durable instructions every Codex session must follow; keep it compact and direct.
3. `context.md`: concise current shared state, not a transcript. Include objective, fixed protocol, verified/inherited/missing/pending work, team roles, file map, decisions, unresolved issues, and the next bounded task. Distinguish work on a branch from work integrated into main. Use the actual date; do not invent a self-referential 'current commit' hash.
4. `starter_prompt.md`: the reusable prompt all three humans paste when beginning/resuming a session. Include the template below, adapted to the actual repo.
5. `docs/experiment_protocol.md`: fixed design and explicitly documented deviations below.
6. `docs/course_requirements.md`: submission requirements and rubric checklist below, with planned/pending status and evidence paths. Do not claim the kit itself meets the experimental rubric.
7. `docs/provenance.md`, `data/README.md`, and `docs/handoff/` as described above.
8. `docs/contributions.md`: historical roles and evidence-backed contribution log that can later support CRediT. Distinguish human contributor, AI assistance, and imported authorship. Do not credit work simply because someone owns a task.
9. `docs/ai_assistance.md`: log actual tool/model if exposed, exact prompts or repo-relative saved prompt files, date, assistance scope, and human validation. Record unknown model versions as unknown. Save this setup prompt under `docs/prompts/` without claiming it contains earlier unseen conversations. Future substantive AI-assisted changes must update this log.
10. `.gitignore` and a simple `.github/pull_request_template.md`: change, owner, relevant issue, verification/evidence, protocol impact, context/contribution/disclosure updates.

Only add a minimal Python dependency file if grounded in imported code and the intended course stack. Do not invent exact tested package versions or claim an environment is reproducible before checking it. Prefer professor starter code if subsequently supplied, clearly documenting necessary deviations.

### Rules for AGENTS.md and starter_prompt.md

- Git is versioned collaboration, not live shared memory. `context.md` provides orientation; code, artifacts, issue/PR state, and Git history provide evidence. Reading it cannot guarantee that other sessions are idle.
- Before each new task, at meaningful checkpoints of long work, and before a final push: inspect working tree/branch/remotes; fetch origin; read the applicable `AGENTS.md`, current `origin/main:context.md`, local branch context, relevant changed files, and open issues/PRs. Compare against the last fetched base. Fetch is read-only to the working tree; do not blindly pull into dirty work.
- If remote access fails, clearly mark context potentially stale and avoid publishing overlapping changes until coordination is restored. Safe isolated local inspection can continue.
- Each human uses a separate clone. Each task/session uses a distinct branch such as `<username>/<task>`; concurrent sessions on one computer need separate worktrees. Never have multiple sessions switching branches in one shared working directory.
- Check open PRs/issues for overlap and record a task's owner, branch, affected files, dependency, and acceptance criteria before implementation. A GitHub issue assignment is a coordination signal, not an atomic lock. Recheck and coordinate overlaps rather than assuming a claim prevents races. Do not assign tasks to teammates without agreement.
- Start new task branches from current main. For existing task branches, inspect and merge `origin/main` when safe; never silently discard uncommitted edits, run destructive reset/clean, auto-stash someone else's work, or force-push shared branches. Preserve both sides of meaningful conflicts and resolve against the protocol.
- Implement only the assigned bounded task. Do not edit another member's model or notebook without a dependency/bug reason and coordination. Keep the stable data/feature/prediction interfaces documented.
- Update `context.md` with every substantive task commit, not on every keystroke. Keep branch work visibly pending integration. Update contribution/disclosure records when applicable. Make small commits and push the task branch, then open a PR. Do not silently merge it.
- Before merge, a human integrator reviews the diff, latest main, checks, overlapping PRs, and context. Resolve context conflicts semantically, preserving both contributors' valid updates. Merge one PR at a time. After merge, other sessions must fetch and reread context before dependent work.
- Each task's final response must state files changed, checks actually run, results, blockers, branch/PR, and next action. Never label an unexecuted model, inherited number, empty skeleton, or unmerged result as completed evidence.
- Prompt instructions are guardrails, not a concurrency guarantee. Avoid custom distributed locking services for this student project.

Reusable starter prompt template:

```text
Work in this repository under its AGENTS.md instructions.

First inspect the working tree, branch, and remote. Fetch origin without
discarding local changes. Read the latest origin/main context.md and relevant
merged changes, then the local context and any open issue/PR touching my task.
If the network is unavailable, state that shared state may be stale.

Resolve my identity from the authenticated GitHub account; do not infer it
from Git author settings alone. Use my own task branch/worktree. Briefly state
what is completed, what is still pending, any overlapping work, and the task
you are taking. If I have not given a task, orient me and suggest the next
bounded task; do not start the remaining project automatically.

For my assigned task, preserve the fixed series manifest, chronological splits,
feature timing, matched row sets, and original teammate attribution. Make only
the necessary changes, run relevant checks, update context.md and applicable
contribution/AI records, fetch again, inspect new upstream work, and push a
small task branch with a PR. Do not merge without my instruction. Never force
push shared work or overwrite another member's changes. State exactly what
was verified and what remains unverified.

My task for this session: [describe the bounded task, or say orientation only].
```

## 5. Experimental protocol to document, not implement yet

- Primary 14-day recent-history comparison, same models with and without historical stockout features. Common predictors include sales lags 1 and 7, recent mean/standard deviation, known weekday and categorical context. Stockout condition adds past stockout hours, affected-day count/proportion, and last-day availability.
- All historical predictors for target date t must use observations through t-1 within the same series. Known calendar fields for t are allowed. Target-day actual sales, stock status/hourly sales, realized weather, and any unverified future promotion/discount fields must not enter predictors. Use an explicit predictor allowlist; do not accidentally feed baseline prediction columns, split labels, or target-derived metadata into models.
- Start eligible examples at day 29 for the planned common 7/14/28-day comparison; retain original split boundaries. Primary training, validation, and test targets have zero reported stockout hours in 06:00–22:00, after independently confirming field semantics and array indexing. Target-day availability is retrospective eligibility metadata only. Preserve stockout days in prior input history. Report rows removed by each filter.
- Both conditions use identical eligible target keys and common features, model families, and tuning budgets. Fit preprocessing on training only, treat IDs as categories, select hyperparameters on validation only, and freeze parameters for final evaluation. Walk-forward daily features may use prior observed validation/test days, with no future data or parameter refitting.
- Core models: linear regression and decision-tree regression. Ridge if covered; random forest optional after confirming course fit. No CNN/RNN/LSTM/deep learning. Do not add unrelated models to inflate scope.
- Recompute inherited persistence and seven-day-average baseline metrics on exactly the matched eligible evaluation rows. Planned additional baselines: lag-7 same-weekday sales; recent mean over stocked historical dates with ordinary historical mean fallback. Do not silently call these existing implementations.
- Metrics: MAE, RMSE, signed bias mean(prediction - actual), mean underprediction mean(max(actual - prediction, 0)), mean overprediction mean(max(prediction - actual, 0)). Add useful course-appropriate metrics with limitations documented; avoid undefined percentage errors on zero sales. Apply nonnegative predictions consistently. Report overall/per-series/store-level results and history-with/without-stockout strata. Paired store-clustered uncertainty if enough stores exist; do not treat all daily rows as independent.
- Pilot goal from the proposal: at least 10% lower MAE with stockout features and no greater mean underprediction. This is a target, not an achieved outcome or permission to tune on test. Report null/negative findings honestly.
- Document two existing limitations now: (a) inherited pilot selection required completeness across all 90 days, unlike the proposal's training-only selection intention; this introduces a retrospective availability-selection limitation, not proof of target leakage; preserve the manifest and disclose the deviation. A training-only-selection sensitivity study is optional later and must be explicitly versioned. (b) baseline test scores have already been seen; freeze subsequent feature/model/metric choices before new model test evaluation, and disclose prior exposure rather than claiming a completely pristine test.
- Prediction handoff contract to agree before modeling: unique `(store_id, product_id, dt, model, feature_set, split)` plus actual, prediction, run identifier; retain eligibility and feature provenance separately. Do not implement model-output producers in setup.

## 6. Course requirements to preserve

Final submissions are INDIVIDUAL and focus on each student's actual contribution. Shared project code and evidence do not authorize identical report prose or invented roles. No final report is requested in this setup.

Final report requirements from the supplied assignment:

- PDF using the IEEE computer science journal LaTeX template; upload `.tex` source to support the LaTeX point.
- At least 12 pages of main report text, excluding appendices and citations; useful technical substance rather than filler. Aim for approximately 1 MB or less per submitted file. Large model artifacts go to accessible Drive links with sizes and justification in the evidence appendix.
- No code in the report; avoid screenshots when tables/vector plots/text work.
- Appendix explaining each rubric item in the exact order below, with honest claims and concrete accessible evidence. Mark not met/pending when appropriate.
- Meaningful literature subsections, relevant prior work, verified bibliographic details, consistent citations, and explicit comparison against available solutions. Prior report references are leads, not independently verified sources.
- Document lessons learned, technical difficulties, best practices, all tools including GenAI, exact prompts/model details when known, and a CRediT contributor statement.
- Answer the mandatory 'similar solutions / Generative AI or other sources' questions with details of model, prompt, website/person, relevant assignment item and help. Course suggests the separate SJSU AI disclosure certificate at https://sjsusaid.vercel.app; do not claim one exists or was submitted.
- If a competition dataset/entry triggers the assignment's leaderboard requirement, preserve leaderboard and solution-comparison evidence; do not invent a rank. Check applicability rather than assuming this pilot has one.
- Assigned in-class presentation is required; slides/video are later work. The exact calendar final deadline and presentation slot remain to be checked in Canvas. 'Friday 11:59pm' is supplied without an unambiguous date; do not infer one.
- Course relevance is classical regression, feature engineering, validation, evaluation, and relevant optional ensembles. UI/full-stack work does not substitute for ML evidence. Sustainability link is an argued potential benefit, not a measured waste reduction.

| Final report rubric, exact order | Points |
|---|---:|
| Report | 7 |
| Relates to sustainability | 5 |
| Lessons learned | 5 |
| Prospects of winning competition / publication | 3 |
| Innovation | 5 |
| Evaluation of performance | 5 |
| Technical difficulty | 7 |
| Used LaTeX | 1 |
| Literature Survey | 5 |
| Total | 43 |

Also retain proposal provenance: abstract, motivation, literature, methodology, deliverables/milestones, team roles, course relevance, technical difficulty, novelty, impact, and Heilmeier questions were required. Historical proposal milestones are not current completion evidence. The uploaded proposal and intermediate report may be imported as references if available, but this prompt provides the necessary starting design without requiring another upload.

Useful source leads for later verification:
https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K
https://github.com/Dingdong-Inc/frn-50k-baseline
https://arxiv.org/abs/2505.16319
https://doi.org/10.1287/opre.1100.0906
https://doi.org/10.1016/j.ijforecast.2019.06.004
https://www.overleaf.com/latex/templates/ieee-demo-template-for-computer-science-journals/fxrxvtcsjqmm
https://credit.niso.org/
https://sdgs.un.org/goals/goal12

## 7. Finish setup and stop

- Check generated Markdown and paths, imported Python syntax without executing it, notebook JSON structure, missing-file labels, source attribution, and that `.gitignore` excludes raw CSV/secrets while retaining intended small artifacts. Inspect staged files individually; do not blindly `git add .` with data present.
- Commit and push the bootstrap if authenticated. Verify the actual repo URL, remote branch contents, and each collaborator invitation status.
- Provide a short handoff: repository URL, setup/import status, pending invitations or blockers, how teammates clone/open/run `starter_prompt.md`, and what remains pending.
- Recommend a cheap coordination check as the next optional step: two teammates make separate tiny documentation PRs, merge sequentially, then have each session fetch and identify both merged updates from context. Success = both contributions preserved, both sessions can state the current shared state, and neither edits main directly. Do not create fake teammate commits or claim this multi-user check passed before the humans do it.
- Stop after setup and migration. Offer the first future technical task: inspect pilot schema/stockout semantics and freeze the matched eligibility/feature contract. Do not start it automatically.
