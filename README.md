# DATA 245 — Group 3: Stockout-Aware Forecasting

**Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail.**

We ask whether historical stockout information improves next-day recorded normalized sales forecasts beyond recent sales history, holding the model, eligible target rows, common predictors, and tuning budget matched.

The target is `sale_amount` for `(store_id, product_id, dt)` in FreshRetailNet-50K. Recorded sales are not unrestricted latent demand, kilograms, revenue, or measured food waste. Better stocking could support SDG 12 and waste prevention; this project has not measured environmental benefits.

## Status as of 2026-11-19 (America/Los_Angeles)

The group-approved [v2 protocol](docs/experiment_protocol.md) is the scientific authority. It uses all eligible target dates including stockouts, 200 development/1,000 final series, 14-day primary history, core linear/tree models and approved Ridge/optional Random Forest extensions. Secondary test groups are retrospective stocked/stockout target dates. The final sample, feature bundle and model/evaluation runs are not implemented. Technical interfaces remain draft.

Layout PR #2 is already merged. Remote PR #3 validation assets are now reconciled locally with V2 and preserved separately as historical evidence. The current tree remains uncommitted, two commits behind remote main, with no merge in progress; Git ancestry integration remains pending. See [reconciliation](docs/V2_RECONCILIATION.md). See [context](context.md) and [alignment audit](docs/REPOSITORY_CHANGE_AUDIT.md).

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

Read [context.md](context.md), the [approved protocol](docs/experiment_protocol.md), [course requirements](docs/course_requirements.md), and [contribution record](docs/contributions.md) before new work. The bootstrap is the one initial commit permitted on `main`; future changes use task branches and PRs.

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

The dependency list covers imported code (`pandas`, `numpy`, `IPython`) and YAML configuration checks (`PyYAML`); package versions and model-runtime compatibility have not been tested or pinned. The setup checks establish file integrity, not a reproducible training environment. Prefer professor starter code if supplied later and document necessary deviations.

## Three-owner workspace

DELTA owns data/shared features/baselines; DEVGRU owns linear/ridge; SAS owns tree/evaluation/integration. The explicit real-name mapping is in [context.md](context.md). Current responsibilities are in [docs/team_responsibilities.md](docs/team_responsibilities.md); inherited real-name attribution remains in provenance.

```text
data245-group3/
  README.md  AGENTS.md  context.md  starter_prompt.md
  .gitignore  .gitattributes  requirements.txt  pyproject.toml
  .github/pull_request_template.md
  configs/{dataset,experiments,models}.yaml
  data/
    raw/                       # local raw export; ignored
    processed/                 # fixed pilot; future versioned feature bundles
    manifests/                 # historical pilot manifest; final manifest pending
  src/
    data_preprocessing_DELTA/  # adapted inherited scripts
    features_DELTA/            # shared feature producer; not implemented
    models/
      baselines_DELTA/
      linear_regression_DEVGRU/
      ridge_regression_DEVGRU/
      decision_tree_SAS/
      random_forest_SAS/        # optional, not implemented
    evaluation_SAS/
  notebooks/{DELTA_data,DEVGRU_linear_models,SAS_evaluation}/
  results/
    baselines_DELTA/inherited/  # original baseline evidence
    linear_regression_DEVGRU/
    ridge_regression_DEVGRU/
    decision_tree_SAS/
    random_forest_SAS/
    comparisons_SAS/
    predictions/
    models/                    # binaries ignored
  tests/
  scripts/verify_setup.py
  docs/                        # methodology, protocol, ownership, interfaces,
                               # experiment log, provenance, course, AI/contributions
  reports/{intermediate,individual,final}/
  archive/original_pilot/       # ten byte-identical handoff originals
```

Most new component directories contain ownership/handoff guidance only. No new feature/model/evaluator is implemented. `pyproject.toml` supplies checked workspace metadata; dependencies remain in `requirements.txt`. Config files mirror the approved scientific design as metadata; technical contract completion remains pending. The [protocol](docs/experiment_protocol.md#authority-and-evidence-statuses) defines the common authority hierarchy for all assistants; [Copilot guidance](.github/copilot-instructions.md) points to it.

You can develop and push owned components in parallel after agreeing the shared interface. Real model runs need the same verified DELTA feature bundle; final comparisons need accepted predictions, and new model test evaluation waits for the freeze. See [interfaces and dependencies](docs/interfaces.md).

For the migrated layout, these checks are run and reported in the [migration record](docs/structure_migration.md):

```sh
python3 scripts/verify_setup.py
python3 -m unittest discover -s tests -v
```

The layout tests require Python 3.11+ and PyYAML. Full pipeline/model/package installation remains unverified. No model training or notebook execution is part of these checks.

## Data and inherited results

The inherited development pilot is already present at `data/processed/pilot_200_series.csv`: 200 fixed series, 18,000 rows, and 90 dates. Its 23 columns include 19 source fields plus day number, split, and two inherited prediction columns. Do not use a whole-frame predictor selection. Read [data/README.md](data/README.md) for sources, license, schemas, and raw-data acquisition.

The raw `data/raw/freshretail.csv` is intentionally absent and ignored (323,577,557 bytes at Drive metadata readback). It was not downloaded for setup. The original files now live under `archive/original_pilot/`. Path-adapted working copies live in `src/data_preprocessing_DELTA/` and `notebooks/DELTA_data/`; they use separate ignored reproduction destinations and have not been run. The working notebook has cleared saved outputs/counters. The adapted `data_explore.py` still downloads a current upstream training split, which is not proof of reproducing the inherited local export. See the [migration record](docs/structure_migration.md).

Inherited baseline scores in `results/baselines_DELTA/inherited/baseline_metrics.csv` use all 3,000 rows of each validation/test split:

- Persistence validation: MAE 0.417757, RMSE 0.677441, signed bias +0.002357.
- Persistence test: MAE 0.444063, RMSE 0.697380, signed bias -0.002777.
- Preceding seven-day mean validation: MAE 0.337380, RMSE 0.551965, signed bias -0.007276.
- Preceding seven-day mean test: MAE 0.362622, RMSE 0.564407, signed bias -0.051647.

These are historical exploratory team results, not redesigned final-experiment results. New baselines will need scoring on the final sample's matched eligible rows. Baseline test scores have already been seen. The protocol discloses that exposure and the pilot's retrospective complete-series selection.

## Collaboration

At task start, checkpoints, and before final push: inspect status/branch/remotes, fetch origin, read `origin/main:context.md` and local context, compare the fetched base, and check open issues/PRs. Do not blindly pull into dirty work. Record owner, branch, affected files, dependencies, and acceptance criteria before implementation. An issue assignment is a coordination signal, not a lock.

Start a distinct `<codename>/<task>` branch from current main; concurrent sessions need separate worktrees. Keep changes bounded, preserve others' work, update context/contributions/AI disclosure, and push a small PR. A human integrator reviews the latest main, diff, checks, and overlaps, then merges one PR at a time. Other sessions fetch and reread context after each merge. No silent merge or force push.

Suggested optional next step: two teammates independently make tiny documentation PRs, merge sequentially, then each session fetches and identifies both preserved updates from context. That human coordination check has **not** been performed. The remaining technical task is to finalize V2's draft interface details and verify the producer; Git ancestry integration also remains pending; do not start implementation without a bounded assignment.

## Sources and rights

- [Shared team handoff folder](https://drive.google.com/drive/folders/1_saUNK4VOT7vpbSjiCw2XKIOpWa3IkHy).
- [FreshRetailNet-50K dataset and data card](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K), by Dingdong-Inc, licensed CC BY 4.0. See [data attribution](data/README.md#attribution-and-permitted-redistribution).
- [Publisher's baseline repository](https://github.com/Dingdong-Inc/frn-50k-baseline) and [technical report](https://arxiv.org/abs/2505.16319). These are references, not models imported or executed in setup.

There is no blanket repository license. Timothy's imported code retains its original authorship; the upstream baseline repository's license does not automatically license teammate code. Dataset rights remain CC BY 4.0. Final submissions and report prose are individual.
