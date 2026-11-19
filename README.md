# DATA 245 — Group 3: Stockout-Aware Forecasting

**Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail.**

We ask whether historical stockout information improves next-day recorded normalized sales forecasts beyond recent sales history, holding the model, eligible target rows, common predictors, and tuning budget matched.

The target is `sale_amount` for `(store_id, product_id, dt)` in FreshRetailNet-50K. Recorded sales are not unrestricted latent demand, kilograms, revenue, or measured food waste. Better stocking could support SDG 12 and waste prevention; this project has not measured environmental benefits.

## Status as of 2026-11-18 (America/Los_Angeles)

- Timothy Tran's preparation code, notebook, exact 200-series manifest, pilot, exclusions, audit, predictions, and baseline metrics are imported unchanged. The original handoff is in [docs/handoff](docs/handoff/README.utf8.md). Attribution and hashes are in [provenance](docs/provenance.md).
- Setup verifies imported bytes, syntax/JSON, schemas, unique keys, manifest membership, calendar coverage, and split counts. It does not reproduce the full raw-data pipeline or independently reproduce baseline scores.
- No new features, trained models, stockout comparison, formal leakage audit, final findings, or individual reports were created. See [shared context](context.md) for current coordination and pending work.
- The private repository is [farzaandalwai/data245-group3](https://github.com/farzaandalwai/data245-group3). Both `shoddy16` and `Timothytran109` accepted their invitations during setup; collaborator and effective-permission readbacks verified write access without admin access. No invitations remained pending at that check.
- Branch protection status and the exact GitHub checks are recorded in [setup verification](docs/setup_verification.md).

## Start here

Each human uses a separate clone after accepting their invitation:

```sh
gh repo clone farzaandalwai/data245-group3
cd data245-group3
```

These teammate clone commands have not been run in their environments. Open that folder as the project in Codex. Codex loads [AGENTS.md](AGENTS.md) as project guidance; it directs the agent to fetch and read shared context when a task begins. No starter-prompt pasting is required. Send a short request such as “Get me oriented,” “Continue my task,” or a specific bounded task. [starter_prompt.md](starter_prompt.md) is an optional reference/fallback. Connecting GitHub alone does not share uncommitted files or merge branches.

Read [context.md](context.md), the [fixed protocol](docs/experiment_protocol.md), [course requirements](docs/course_requirements.md), and [contribution record](docs/contributions.md) before new work. The bootstrap is the one initial commit permitted on `main`; future changes use task branches and PRs.

## Environment and checks

The setup checker uses only the Python standard library. This command was run successfully with Python 3.14.2 during setup:

```sh
python3 scripts/verify_setup.py
```

It reads files and prints checks; it does not execute imported scripts/notebook cells, fit models, recompute scores, or write data. Evidence and limitations are in [docs/setup_verification.md](docs/setup_verification.md).

For later authorized Python work, these commands are **unrun and unverified**:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The dependency list comes from imported code (`pandas`, `numpy`, `IPython`); package versions and model-runtime compatibility have not been tested or pinned. The setup checks establish file integrity, not a reproducible training environment. Prefer professor starter code if supplied later and document necessary deviations.

## Data and inherited results

The pilot is already present at `data/processed/pilot_200_series.csv`: 200 fixed series, 18,000 rows, and 90 dates. Its 23 columns include 19 source fields plus day number, split, and two inherited prediction columns. Do not use a whole-frame predictor selection. Read [data/README.md](data/README.md) for sources, license, schemas, and raw-data acquisition.

The raw `data/freshretail.csv` is intentionally absent and ignored (323,577,557 bytes at Drive metadata readback). It was not downloaded for setup. Do not run `data_explore.py` to substitute a current full upstream dataset for the specific inherited local export. Both imported preparation entry points can overwrite the fixed pilot and baseline files; inspect them and arrange a separate, explicitly authorized reproduction destination before any future execution.

Inherited baseline scores in `results/baseline_metrics.csv` use all 3,000 rows of each validation/test split:

- Persistence validation: MAE 0.417757, RMSE 0.677441, signed bias +0.002357.
- Persistence test: MAE 0.444063, RMSE 0.697380, signed bias -0.002777.
- Preceding seven-day mean validation: MAE 0.337380, RMSE 0.551965, signed bias -0.007276.
- Preceding seven-day mean test: MAE 0.362622, RMSE 0.564407, signed bias -0.051647.

These are inherited team results. They are not the stockout-aware comparison and will need scoring on future matched eligible rows. Baseline test scores have already been seen. The protocol discloses that exposure and the pilot's retrospective complete-series selection.

## Collaboration

At task start, checkpoints, and before final push: inspect status/branch/remotes, fetch origin, read `origin/main:context.md` and local context, compare the fetched base, and check open issues/PRs. Do not blindly pull into dirty work. Record owner, branch, affected files, dependencies, and acceptance criteria before implementation. An issue assignment is a coordination signal, not a lock.

Start a distinct `<username>/<task>` branch from current main; concurrent sessions need separate worktrees. Keep changes bounded, preserve others' work, update context/contributions/AI disclosure, and push a small PR. A human integrator reviews the latest main, diff, checks, and overlaps, then merges one PR at a time. Other sessions fetch and reread context after each merge. No silent merge or force push.

Suggested optional next step: two teammates independently make tiny documentation PRs, merge sequentially, then each session fetches and identifies both preserved updates from context. That human coordination check has **not** been performed. The first future technical task is to inspect stockout semantics and freeze the matched eligibility/feature contract; do not start it without a bounded assignment.

## Sources and rights

- [Shared team handoff folder](https://drive.google.com/drive/folders/1_saUNK4VOT7vpbSjiCw2XKIOpWa3IkHy).
- [FreshRetailNet-50K dataset and data card](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K), by Dingdong-Inc, licensed CC BY 4.0. See [data attribution](data/README.md#attribution-and-permitted-redistribution).
- [Publisher's baseline repository](https://github.com/Dingdong-Inc/frn-50k-baseline) and [technical report](https://arxiv.org/abs/2505.16319). These are references, not models imported or executed in setup.

There is no blanket repository license. Timothy's imported code retains its original authorship; the upstream baseline repository's license does not automatically license teammate code. Dataset rights remain CC BY 4.0. Final submissions and report prose are individual.
