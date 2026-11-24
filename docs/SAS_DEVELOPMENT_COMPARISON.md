# SAS development integration — 2026-11-20 (r4 update 2026-11-23)

## r4 update — 2026-11-23 (current shareable comparison)

Branch `SAS/rf-comparison-r4` from merged `main` `4dffb0d`. Package:
`artifacts/SAS/development/harmonized-200-series-20261123-r4/`. Same bundle, rows,
evaluator and bootstrap as r3; r3 is unchanged and every r3 metric/interval is
reproduced exactly.

- **Pin:** PR #6 merged with DEVGRU correction `1f4e6a4`, which changed only
  `INVENTORY.md`. `docs/SAS_DEVGRU_PR6_PIN.json` now pins that commit; the old
  `044fac1` record is kept under `supersedes`. The malformed
  `paired_validation_comparison.csv` checksum is fixed. The inventory entries for
  `development_report.md` and `run_metadata.json` still differ from the published bytes,
  so DEVGRU's note that they always matched is not confirmed.
- **Random Forest:** the run `sas-forest-dev-200-r1` is shared byte-for-byte under
  `artifacts/SAS/development/random-forest-200-series-20261120/` and accepted only at its
  recorded manifest SHA-256.
- **Relative MAE improvement** (100 × (sales − aware) / sales, point estimate only):
  Linear +0.020%, Ridge +0.041%, Decision Tree −1.095%, Random Forest −0.159%.

| Model | Sales MAE | Aware MAE | Aware − sales | 95% store interval |
| --- | --- | --- | --- | --- |
| Linear | 0.334257 | 0.334190 | −0.000066 | [−0.002462, +0.002373] |
| Ridge | 0.334256 | 0.334119 | −0.000137 | [−0.002427, +0.002148] |
| Decision Tree | 0.348255 | 0.352070 | +0.003814 | [−0.003332, +0.013629] |
| Random Forest | 0.335969 | 0.336504 | +0.000535 | [−0.003533, +0.005357] |

Baselines on the same rows: persistence 0.417757, 7-day mean 0.337380. All four intervals
include zero; no stockout-feature benefit is established. DEVELOPMENT only.

Reproduce (needs DELTA's ignored r2 bundle; PR #6 is now on `main`, so no isolated checkout):

```sh
python3 -m scripts.sas_development_comparison verify
python3 -m scripts.sas_development_comparison compare --output runs/SAS/reproduce-development-r5
```

Pass `--sas-forest ""` to omit the forest. Older sections below are the 2026-11-20 record.


Owner/requester: SAS / Farzaan Dalwai (`farzaandalwai`, authenticated).
Branch: `SAS/development-comparison`, clean fetched main base `c54f9ab`.
PR #4 is MERGED; PR #6 is OPEN at `044fac1a9ed0fae52179df25946a5a994f2826b5`.
The PR #6 checkout is isolated and read-only. No teammate branch is merged or
modified. The initial working tree was clean; ignored originals remain in place.

Authorized scope: publish byte-identical original SAS development evidence;
validate PR #6 artifacts against the exact DELTA development bundle; adapt
metadata in memory; apply the current shared development evaluator/whole-store
bootstrap in a separate run; add development figures, tests and handoff records;
commit/push and open a SAS PR. No model retraining, expanded search, original
output replacement, final bundle scoring or PR merge.

## Original evidence acceptance

Both original SAS run manifests and their 14 registered output files match the
previously committed evidence. Copies are placed under
`artifacts/SAS/development/original-200-series-20261119/`, leaving ignored original
paths untouched. Numeric tree JSON exports exist; no executable pickle was saved.
Bootstrap summaries/seed/settings exist; individual bootstrap draw arrays were
not saved by the original runner. Reproduction is evaluation-only from original
predictions, not a claim of recovering unsaved arrays or retraining models.

PR #6 contains all four original prediction files, tuning/metrics/paired interval
results and enriched metadata. The four prediction checksums match its inventory.
Its supporting inventory has mismatches for `run_metadata.json`,
`development_report.md` and `paired_validation_comparison.csv`; these will be
reported without rewriting the source package. The package is separately pinned
to exact Git blob bytes from the PR commit. Metadata's source revision is the old
base, not a complete dirty-source snapshot; saved DEVGRU fitted models are absent.
These provenance limits remain explicit even when predictions pass numerical
and coverage checks. Original series-bootstrap results remain historical inputs;
the new harmonized output will use the approved development store bootstrap.

`docs/SAS_DEVGRU_PR6_PIN.json` pins all 11 published PR #6 package files to the
exact commit's Git bytes. All four prediction hashes match the original inventory;
all 48,800 prediction rows match the exact authoritative train/validation keys,
targets and splits. Each source file has 9,200 train + 3,000 validation rows,
correct model/condition/run labels, no duplicates/nulls/nonfinite values or test
rows, and correct paired coverage. Stored MAE/RMSE/bias and selected-alpha
evidence match the original predictions/recorded candidate minima. No candidate
model was retrained to validate those scores.

Three inventory discrepancies remain: `run_metadata.json` and
`development_report.md` have different published bytes from their inventory
hash/size entries; `paired_validation_comparison.csv` has a malformed 63-character
checksum in the inventory. Published Git bytes are separately pinned and the
original paired bootstrap CSV numerically reproduces. Metadata is enriched, and
the source revision records the pre-implementation base without dirty-source
hashes. These limits require DEVGRU correction/confirmation for final provenance;
passing numeric checks is not proof of the exact original execution environment.
No files in the PR package were edited.

Code inspection and the existing 11 DEVGRU synthetic tests support train-fitted
standardization, validation-MAE alpha selection and raw finite prediction output.
The original aware predictions include 9 negative Linear and 6 negative Ridge
forecasts (train+validation), inconsistent with a blanket nonnegative clip.
Metadata alone is not accepted as proof of compliance. Original fitted DEVGRU
models were not saved; they cannot be verified by reloading. SAS's saved numeric
trees reconstruct all 24,400 original train/validation predictions exactly,
without fitting and without opening any final input.

## Mechanical adaptation versus scientific policy

DEVGRU has distinct run IDs per model/condition; SAS's exchange validator expects
one family run ID for paired conditions. The adapter changes `run_id` in memory
only and records all four original-to-evaluation IDs. Keys, actuals, splits,
prediction values and source bytes are unchanged. Enriching the evaluation's
source ledger is a mechanical handoff operation, not a new provenance claim.

Both original methods use 95% percentile intervals, 2,000 repetitions and
aware-minus-sales MAE differences. DEVGRU resamples 200 store-product series,
with seeds 245 (Linear) / 246 (Ridge), averaging series means. Its 15 validation
dates per series make its point estimate equal to the pooled row estimate on
this sample. Series resampling does not preserve dependence among products in
the same store. Its original intervals were independently reproduced from
original CSVs without invoking its model runner.

The latest shared protocol explicitly specifies whole stores, seed 245 and 2,000
replicates for development comparisons. The separate harmonized run uses that
existing approval for every learned model, retaining all matched rows and each
replicate's pooled row denominator. It does not relabel original series intervals
as store intervals. No new scientific choice or search expansion was introduced.
Unresolved group tie rules/final acceptance remain unresolved.

## Harmonized DEVELOPMENT results

Published run: `artifacts/SAS/development/harmonized-200-series-20261120-r3/`.
All model conditions and both baselines use exactly **3,000 validation rows,
200 series, 113 stores**, 2024-05-27 through 2024-06-10. Training rows were checked
for input acceptance but are not scored in this combined report. Original
source manifests hash/validate the full development bundle structurally;
the final 1,000-series bundle was never opened or scored.

The concise CSV includes MAE, RMSE, signed bias (prediction minus actual), mean
underprediction/overprediction over all rows, row/store counts and paired MAE
differences/intervals. Point findings:

- Linear MAE: sales 0.334257 / aware 0.334190; difference -0.000066,
  95% store interval [-0.002462, +0.002373].
- Ridge MAE: sales 0.334256 / aware 0.334119; difference -0.000137,
  interval [-0.002427, +0.002148].
- Decision Tree MAE: sales 0.348255 / aware 0.352070; difference +0.003814,
  interval [-0.003332, +0.013629].
- Common references: persistence MAE 0.417757; previous-7-day mean 0.337380.
  They were newly materialized from DELTA's validation-sliced accepted predictors
  using its unchanged helper; original DELTA baseline output files were absent.
  No baseline test predictions were materialized or scored in this integration.

Every paired interval includes zero. There is no clear stockout-feature benefit
on these development data. The tree point result is worse; Linear/Ridge point
gains are small. All intervals condition on validation-selected fitted models;
they omit refitting/tuning uncertainty and assume independent stores. Shared
calendar shocks, retrospective sampling, historic test exposure and multiple
comparisons remain limitations. No final, causal, latent-demand or sustainability
finding is claimed. See the original protocol's limitations as well.

Retrospective validation subgroups contain **1,698 fully-stocked rows** and
**1,302 stockout rows**, each covering all 113 stores. Their metrics are separate
debugging summaries of the same predictions, not different training populations.
Overall paired intervals do not imply subgroup interval coverage.

PNG/SVG development MAE and paired-interval figures were rendered and visually
checked. Initial derived runs r1/r2 are preserved under ignored
`runs/SAS/superseded/`; they were superseded for inventory-warning/figure-layout
improvements, not changed predictions or tuning. Original experiment runs remain
unchanged. The r3 package is the reviewed shareable comparison.

## Reproduction without retraining

Install `requirements.txt`; exact local versions are recorded in
`requirements-sas-tested.txt` and the comparison manifest. Obtain DELTA's exact
development r2 bundle (trusted SHA-256
`043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`).
Git intentionally does not distribute that input bundle.

PR #6 is still unmerged at review time. Use an isolated checkout at its pinned
commit and pass its package directory (do not merge the teammate branch to run
this review). Example from repository root, replacing `/path/to/pr6-checkout`:

```sh
python3 -m scripts.sas_development_comparison verify --devgru-root /path/to/pr6-checkout/artifacts/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119
python3 -m scripts.sas_development_comparison compare --devgru-root /path/to/pr6-checkout/artifacts/DEVGRU/development/v2-development-200-r2-linear-ridge-standardize-20261119 --output runs/SAS/reproduce-development-r4
```

The output directory must not exist. Once the exact PR package is on main, omit
`--devgru-root`; the default uses its published artifact path. Changed package
bytes require a new reviewed pin; they are not silently accepted. The local task
also preserves an identical ignored cache at `runs/SAS/incoming/DEVGRU-pr6-044fac1`.
Commands validate originals and recompute evaluations only. The original SAS
package can independently be checked with `shasum -a 256 -c SHA256SUMS` from its
directory. No model runner, alpha search or final outcome is used by these commands.

## Final evaluation handoff — BLOCKED, no final scoring performed

The following distinctions must remain explicit before a final workflow:

- **Already approved, verify unchanged:** DELTA's 1,000-series fixed manifest and
  all-eligible population including stockouts; 14-day history/day-15 boundary;
  exact 9 common + 5 added historical features; key-only IDs; chronological
  train/validation/test dates; common rows/actuals/splits; train-only transforms;
  no clipping; MAE primary, RMSE/bias/under/over secondary. No amendments here.
- **Verified development behavior:** standardization in DEVGRU is fitted on
  train and reused; Ridge uses validation MAE on five recorded alpha candidates;
  SAS uses its same 12-candidate tree budget. No grid expansion. These are not
  automatically selected/frozen final-1,000-series settings.
- **Team decision still needed:** adopt/freeze exact final model grids/settings
  and per-condition tuning budget; freeze actual validation selections and
  contract/bundle/code/environment hashes before final test scoring. Confirm
  Linear intercept/standardization details and retained feature order as part
  of the technical freeze, not by selecting on test performance.
- **Tie rules not collectively approved:** actual SAS development rule is first
  exact grid tie; actual DEVGRU Ridge rule prefers smaller alpha on an exact MAE
  tie. The proposal for larger alpha / shallower trees / larger leaves remains
  a proposal. No near-tie tolerance has been agreed and none was added here.
- **Uncertainty:** development store-bootstrap settings remain 95%, seed 245,
  2,000 replicates, pooled row weighting and aware-minus-sales direction. Team
  acceptance of their use/limitations in a final workflow is pending. No change
  to originals, bootstrap refitting, subgroup/multiple-comparison procedure, or
  final inferential claim is implied.
- **Provenance/review:** Shoury must correct/confirm the three inventory issues
  and execution lineage/model-file limitations. DELTA must confirm final bundle
  acceptance and outstanding export/business semantics. Human review remains
  pending; no API policy declaration or config flag substitutes for it.

Verified safe command: `python3 -m scripts.sas_final_preflight` reads configuration
only and exits **2 (blocked)**. It opens no bundle/outcome CSV even if flags are
manually flipped. It is not a final evaluator. Current development commands also
reject final-purpose manifest headers *before* loading outcome CSVs. There is
no reviewed final-scoring entry point yet; it must be separately reviewed after
the freeze. Do not use the development command on a final bundle as a workaround.

## Checks, ownership and next actions

All **84 tests passed**: original 61, 11 DEVGRU synthetic tests, 12 new SAS
integration checks. The first full run exposed a missing ignored DELTA synthetic
fixture; its exact Drive r2 copy was retrieved and verified against
`3c51884b4d24a615d797578af8fc047c1109d82ec55b3017ce97556b7b180769` before rerunning.
No teammate tests were changed. Synthetic checks fit only tiny test fixtures;
no real model was refit or reselected. Integrity, links, staged retention and
whitespace checks are recorded with publication. The two real-data figures were
visually checked; all original hashes were rechecked after evaluation.

Next actions: DEVGRU confirms/corrects its artifact inventory and execution
metadata, without substituting newly trained outputs; DELTA reviews exact
producer/final bundle acceptance and limitations; SAS reviews the published
comparison and coordinates the technical freeze/final-entry-point review.
This task opens its own PR, without merging PR #6 or any other PR.

The setup checker originally assumed every README was publishable, including the new ignored incoming-cache README. It now excludes only documented local `runs/` and `outputs/` roots from source-link/README retention scans, explicitly asserts their READMEs stay ignored, and keeps raw-file and reviewed-artifact retention checks. A new negative retention test covers this boundary; no source-integrity check was waived.

The isolated review checkout remains clean/read-only at `/Users/farzu/.codex/worktrees/sas-review-devgru-pr6/data245-group3`. Managed archival was attempted, but the app protects it as the chat’s primary checkout; it was retained rather than removed manually. The implementation checkout and task branch are `/Users/farzu/Desktop/data245-group3` / `SAS/development-comparison`; use that explicit root for subsequent SAS work. The immutable incoming cache and Git pins preserve reproducibility independently of the review checkout.
