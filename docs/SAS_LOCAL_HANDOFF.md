# SAS local implementation handoff

Historical first-phase snapshot. The newer [SAS integration record](SAS_INTEGRATION.md) supersedes local-only publication restrictions, missing-bundle status and deferred intervals below. Real development validation and paired bootstrap intervals have now run; final/test scoring is still blocked.

## Scope recorded before implementation

2026-11-19. Requester: SAS / Farzaan Dalwai, authenticated GitHub
`farzaandalwai`. Branch: `SAS/local-tree-evaluator`, clean base `d2a323e`.
Fetched origin and inspected open issues/PRs (none). The user authorized local
SAS work and explicitly withheld publication. No staging, commit, push or merge.

Implement the required Decision Tree consumer and shared prediction evaluator
against DELTA producer 2.0.0. Owned paths: `src/models/decision_tree_SAS/`,
`src/evaluation_SAS/`, a SAS command-line entry point and behavioral tests.
Update affected status/dependency/AI records without changing the science.

The real V2 bundles/raw export are absent in this checkout. Acceptance for this
task is reproducible synthetic integration, golden metric/key checks, train-only
fitting and validation-only selection, rejection of incompatible inputs, and
preserved original evidence. Synthetic checks are never research findings.

Development tree settings are explicitly provisional; this task does not freeze
team preprocessing, tuning, prediction or uncertainty decisions. No final-input
training/scoring or learned-model test scoring is authorized by this workflow.
Random Forest remains optional and deferred until the core comparison works.
DELTA data/features and DEVGRU models will not be changed.

## Implemented locally

- [Decision Tree consumer](../src/models/decision_tree_SAS/v2.py): explicit keyed
  joins/allowlists; identical candidate grids for sales-only/stockout-aware;
  train-only fitting, validation-MAE selection, deterministic tie breaking and no
  validation refit. Produces train/validation predictions only.
- [Shared evaluator](../src/evaluation_SAS/v2.py): exact authoritative coverage,
  actual/split/condition checks, common baselines, pooled/subgroup/series/store
  MAE/RMSE/signed-bias/under/over metrics, paired MAE differences and relative
  improvement. Empty/zero-denominator metrics stay undefined. Retrospective labels
  are joined after prediction. Development subgroup outputs are debug evidence.
- [Run adapter](../src/evaluation_SAS/runs.py): trusted manifest pinning,
  protocol/sample/bundle/producer compatibility, artifact checksums, immutable
  transactional output, source/environment/selection provenance and DELTA V2
  baseline-format compatibility. Evaluator imports no model implementation.
- [CLI](../scripts/sas_v2.py), [21 SAS behavior tests](../tests/test_sas_v2.py),
  [provisional development policy](../src/models/decision_tree_SAS/development_policy.json)
  and [development exchange envelope](../src/evaluation_SAS/README.md#provisional-development-run-envelope).

The development policy has 12 ordered candidates per condition: depth
3/5/8/unlimited crossed with leaf size 5/20/50, seed 245, squared-error criterion,
no transform/imputation/clipping. These are local development settings; shared
final settings remain draft. No DELTA/DEVGRU implementation was changed. Current
README/context/status metadata and AI/contribution records now identify this
local task; previous DELTA uncommitted labels are historical snapshots.

## Verification actually completed

- `python3 -m unittest discover -s tests -q`: **56 passed** (35 existing + 21 SAS).
- `python3 scripts/verify_setup.py`: passed originals/canonical hashes, syntax,
  schemas, local Markdown links and ignore/retention rules. It did not execute
  legacy code or reproduce real-data results.
- CLI synthetic producer -> train-tree -> evaluate completed locally. DELTA's
  unchanged fixture producer supplied 2 series / 152 observations, split
  92/30/30. SAS emitted 244 predictions (122 per condition, train/validation
  only), then compared the 30 validation keys per condition. All outputs are
  explicitly `SYNTHETIC_NOT_RESEARCH`.
- An integration test combined those tree consumers with two DELTA-compatible
  synthetic baseline models. Coverage/identity/tamper/final-scoring rejection,
  train-only fitting, no test prediction calls, test/metadata perturbations,
  equal tuning budgets, stable ties and numeric JSON-tree reconstruction passed.
- `git diff --check` passed. Originals, canonical pilot/manifests, inherited
  results, DELTA code and DEVGRU code remain unchanged.

Initial tests exposed arithmetic overflow handling and percent-rounding edge
cases; corrected before the passing full-suite/CLI run. Environment actually
tested: Python 3.14.2, NumPy 2.4.3, pandas 3.0.1, scikit-learn 1.9.0, SciPy 1.18.1.
See [requirements-sas-tested.txt](../requirements-sas-tested.txt). Existing local
packages were used; no clean installation or Python-3.12/teammate-machine
compatibility is claimed. DELTA's separate tested lock remains unchanged.

Exact local artifact identities/source hashes and limits:
[SAS_LOCAL_RUN_EVIDENCE.json](SAS_LOCAL_RUN_EVIDENCE.json). Ignored smoke artifacts:

- `data/processed/feature_bundles/sas-local-fixture-20261119-r1/`
- `results/decision_tree_SAS/v2/sas-synthetic-tree-20261119-r1/`
- `results/comparisons_SAS/v2/sas-synthetic-comparison-20261119-r1/`

## Real-data dependencies and publication status

DELTA's raw CSV and real `v2-development-200-r2` / `v2-final-1000-r2` bundles are
absent from this checkout. No real learned-model run has happened. Do not rebuild
the pilot into an unofficial substitute bundle or silently download a different
export. Obtain the exact DELTA development bundle and use its trusted handoff
manifest hash. The local entry point is ready for that separate validation:

```sh
python3 -m scripts.sas_v2 train-tree \
  --bundle data/processed/feature_bundles/v2-development-200-r2 \
  --manifest-sha256 043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7 \
  --run-id sas-tree-dev-200-r1
```

This command has **not run** because that bundle is missing. A full model
comparison also needs accepted DEVGRU prediction files. SAS implementation does
not depend on those files; the comparison results do. Final scoring, uncertainty
intervals and research figures still need the shared technical/validation freeze,
human acceptance and a separately reviewed final workflow. Current commands
unconditionally reject final bundles/test scoring.

All changes remain on local `SAS/local-tree-evaluator`, unstaged/uncommitted.
Nothing was pushed, merged or published. Automated validation is not independent
human review, personal student implementation credit or a real forecasting result.
