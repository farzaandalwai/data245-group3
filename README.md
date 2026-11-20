# DATA 245 — Group 3: Stockout-Aware Forecasting

**Does Sold Out Get Mistaken for Unpopular? Stockout-Aware Forecasting for Fresh Retail.**

We ask whether historical stockout information improves next-day recorded normalized sales forecasts beyond recent sales history, holding the model, eligible target rows, common predictors, and tuning budget matched.

The target is `sale_amount` for `(store_id, product_id, dt)` in FreshRetailNet-50K. Recorded sales are not unrestricted latent demand, kilograms, revenue, or measured food waste. Better stocking could support SDG 12 and waste prevention; this project has not measured environmental benefits.

## Status as of 2026-11-19 (America/Los_Angeles)

The group-approved [v2 protocol](docs/experiment_protocol.md) is the scientific authority. It uses all eligible target dates including stockouts, 200 development/1,000 final series, 14-day primary history, core linear/tree models and approved Ridge/optional Random Forest extensions. Secondary test groups are retrospective stocked/stockout target dates. DELTA producer/inputs/development baselines are operationally verified in its recorded runs. SAS’s Decision Tree/development evaluator passed synthetic checks and real development validation on DELTA’s exact pinned r2 bundle, including 95% paired store-cluster intervals. See [SAS integration](docs/SAS_INTEGRATION.md). Business semantics remain provisional and final test scoring is blocked. See [DELTA handoff](docs/DELTA_DATA_HANDOFF.md) and [SAS handoff](docs/SAS_LOCAL_HANDOFF.md).

DELTA implementation is merged in base `d2a323e`; earlier layout/methodology work is integrated. Current branch `SAS/local-tree-evaluator` contains SAS integration work for an authorized draft PR; no merge is in progress. See [context](context.md) for the current task and [reconciliation](docs/V2_RECONCILIATION.md) for historical integration evidence.

- Timothy Tran's preparation code, notebook, exact 200-series manifest, pilot, exclusions, audit, predictions, and baseline metrics are imported unchanged. The original handoff is in [docs/handoff](docs/handoff/README.utf8.md). Attribution and hashes are in [provenance](docs/provenance.md).
- Setup verifies imported bytes, syntax/JSON, schemas, unique keys, manifest membership, calendar coverage, and split counts. It does not reproduce the full raw-data pipeline or independently reproduce baseline scores.
- Shared features, automated leakage checks and development baselines exist. SAS’s tree/evaluator has synthetic tests and a real development run; final comparison/findings and individual reports remain pending. See [shared context](context.md).
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

DELTA verified Python 3.12.10 in the ignored `.venv`. Windows commands use `.venv/Scripts/python.exe`; equivalent setup elsewhere:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The dependency list covers imported code (`pandas`, `numpy`, `IPython`), YAML checks (`PyYAML`) and SAS trees (`scikit-learn`). DELTA's environment remains in [run evidence](docs/DELTA_V2_RUN_EVIDENCE.json); SAS's separate tested Python 3.14.2 environment is recorded in `requirements-sas-tested.txt`. Cross-machine/Python-3.12 model compatibility remains pending. Prefer professor starter code if supplied later and document necessary deviations.

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
    processed/                 # fixed pilot and versioned feature bundles
    manifests/                 # historical manifests; final manifest inside bundle
  src/
    data_preprocessing_DELTA/  # adapted inherited scripts
    features_DELTA/            # implemented shared V2 feature producer
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

DELTA producer/baselines and local SAS Decision Tree/development evaluator are implemented. DEVGRU models and the optional SAS forest remain pending. `pyproject.toml` supplies checked workspace metadata; dependencies remain in `requirements.txt`. The broader technical freeze remains pending. The [protocol](docs/experiment_protocol.md#authority-and-evidence-statuses) defines the authority hierarchy; [Copilot guidance](.github/copilot-instructions.md) points to it.

You can develop and push owned components in parallel after agreeing the shared interface. Real model runs need the same verified DELTA feature bundle; final comparisons need accepted predictions, and new model test evaluation waits for the freeze. See [interfaces and dependencies](docs/interfaces.md).

For the migrated layout, these checks are run and reported in the [migration record](docs/structure_migration.md):

```sh
python3 scripts/verify_setup.py
python3 -m unittest discover -s tests -v
```

Layout checks require Python 3.11+ and PyYAML; the full suite additionally imports the declared data/model dependencies and trains tiny synthetic trees. It does not train on real inputs, run final/test scoring, or execute legacy notebooks.

## Data and inherited results

The inherited development pilot is already present at `data/processed/pilot_200_series.csv`: 200 fixed series, 18,000 rows, and 90 dates. Its 23 columns include 19 source fields plus day number, split, and two inherited prediction columns. Do not use a whole-frame predictor selection. Read [data/README.md](data/README.md) for sources, license, schemas, and raw-data acquisition.

DELTA's recorded raw export has 323,577,557 verified bytes; its SHA-256 and provenance limits are in the handoff. The raw CSV and final bundle are absent here. DELTA’s exact development r2 bundle was located in Drive, verified and imported locally; Git does not distribute these ignored bytes. The original files remain under `archive/original_pilot/`. Path-adapted working copies live in `src/data_preprocessing_DELTA/` and `notebooks/DELTA_data/`; they use separate ignored reproduction destinations and have not been run here. The working notebook has cleared execution state. The adapted downloader fetches a current upstream split, which cannot silently replace the registered local export. See [migration](docs/structure_migration.md).

Inherited baseline scores in `results/baselines_DELTA/inherited/baseline_metrics.csv` use all 3,000 rows of each validation/test split:

- Persistence validation: MAE 0.417757, RMSE 0.677441, signed bias +0.002357.
- Persistence test: MAE 0.444063, RMSE 0.697380, signed bias -0.002777.
- Preceding seven-day mean validation: MAE 0.337380, RMSE 0.551965, signed bias -0.007276.
- Preceding seven-day mean test: MAE 0.362622, RMSE 0.564407, signed bias -0.051647.

These are historical exploratory team results, not redesigned final-experiment results. New baselines will need scoring on the final sample's matched eligible rows. Baseline test scores have already been seen. The protocol discloses that exposure and the pilot's retrospective complete-series selection.

## Collaboration

At task start, checkpoints, and before final push: inspect status/branch/remotes, fetch origin, read `origin/main:context.md` and local context, compare the fetched base, and check open issues/PRs. Do not blindly pull into dirty work. Record owner, branch, affected files, dependencies, and acceptance criteria before implementation. An issue assignment is a coordination signal, not a lock.

Start a distinct `<codename>/<task>` branch from current main; concurrent sessions need separate worktrees. Keep changes bounded, preserve others' work, update context/contributions/AI disclosure, and push a small PR. A human integrator reviews the latest main, diff, checks, and overlaps, then merges one PR at a time. Other sessions fetch and reread context after each merge. No silent merge or force push.

Suggested optional next step: two teammates independently make tiny documentation PRs, merge sequentially, then each session fetches and identifies both preserved updates from context. That human coordination check has **not** been performed. Remaining tasks are human producer acceptance and the joint model/evaluation freeze; do not start implementation without a bounded assignment.

## Sources and rights

- [Shared team handoff folder](https://drive.google.com/drive/folders/1_saUNK4VOT7vpbSjiCw2XKIOpWa3IkHy).
- [FreshRetailNet-50K dataset and data card](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K), by Dingdong-Inc, licensed CC BY 4.0. See [data attribution](data/README.md#attribution-and-permitted-redistribution).
- [Publisher's baseline repository](https://github.com/Dingdong-Inc/frn-50k-baseline) and [technical report](https://arxiv.org/abs/2505.16319). These are references, not models imported or executed in setup.

There is no blanket repository license. Timothy's imported code retains its original authorship; the upstream baseline repository's license does not automatically license teammate code. Dataset rights remain CC BY 4.0. Final submissions and report prose are individual.

Tested environment lock: `requirements-v2-tested.txt` (Python 3.12.10). Install with `python -m pip install -r requirements-v2-tested.txt` when exact local package versions are needed.
