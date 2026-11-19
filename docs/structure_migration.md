# Three-owner workspace migration

Date: 2026-11-18 (America/Los_Angeles). Owner/requester: SAS. Branch: `SAS/three-person-layout`, integrated by PR #2 as merge commit `35bfa71208d0297c72c41f00c104abed9027235b` at the user’s explicit instruction. No separate teammate approval is claimed. The user explicitly requested the proposed repository layout adapted to the three active contributors, then supplied DELTA/DEVGRU/SAS folder labels and required the identity map in `context.md`. This supersedes the old five-person active allocation while preserving its historical provenance.

## Scope and preservation

All ten originals are retained byte-for-byte beneath `archive/original_pilot/`, preserving the original relative pipeline/data/results layout. The archive has no raw CSV and is not an entry point. `docs/handoff/README.original.md` and its UTF-8 reading copy remain available. The import manifest retains initial `dest` values as import-time history and adds current original/working destinations. Original author/source/date/hash facts were not rewritten as new execution evidence.

Working paths:

- `data_prep_pipeline/prepare_and_baselines.py` -> `src/data_preprocessing_DELTA/prepare_and_baselines.py`, with explicit root/input/output adaptations.
- `data_prep_pipeline/data_explore.py` -> `src/data_preprocessing_DELTA/data_explore.py`, with root-based raw destination and a `main` guard; original download behavior remains unexecuted.
- `data_prep_pipeline/prepare_and_baselines.ipynb` -> `notebooks/DELTA_data/prepare_and_baselines.ipynb`, with nested-root discovery, adapted paths, and cleared outputs/execution counters. Original output evidence stays in the archive. Notebook execution remains unverified.
- The fixed pilot stays at `data/processed/pilot_200_series.csv`, unchanged.
- Fixed manifest/exclusions move to `data/manifests/`, unchanged.
- The three inherited result files move to `results/baselines_DELTA/inherited/`, unchanged.
- Raw destination moves from the old documented `data/freshretail.csv` to `data/raw/freshretail.csv`; it remains absent and ignored everywhere.

The active legacy script/notebook now write only to separate `reproduction` destinations under processed data, manifests, and DELTA baseline results. They still implement historical preparation/sampling/baselines, not the future matched feature/model comparison. Reproduction outputs never become the canonical manifest/pilot automatically. No legacy entry point was executed.

`docs/handoff/migration_manifest.json` records each original archived path/hash and migration-time working-copy hash/status. It is a migration snapshot; future working-code changes need their own provenance rather than overwriting the original source checksum.

## Three-person organization

DELTA owns data/preparation/shared features/baselines; DEVGRU owns linear/ridge; SAS owns tree/evaluation/audit/integration. Component directories contain useful handoff/acceptance notes, not fake model implementations. At migration time the config files mirrored paths/plans and correctly marked the contract pending. The later [contract freeze](contract_freeze.md) records the separately completed source audit and v1 definitions; this does not retroactively turn migration checks into model evidence. `pyproject.toml` is checked workspace metadata, not an asserted installable package. `requirements.txt` remains the dependency source, adding PyYAML for config validation without inventing pinned versions.

The existing protocol/course/provenance/contribution/AI/prompt records, PR template, byte-preservation rules, setup checker, and automatic `AGENTS.md` startup behavior are retained. Methodology/log/responsibility/interface docs and individual report workspace guidance were added. The repository name/remote/privacy and original authorship remain the same. No feature producer, model, evaluator, fixture, final finding, or individual report was implemented by this task.

## Parallel work and gates

After a shared interface review, all three can develop their own components and push separate branches. Clearly labeled schema fixtures can support independent adapter/evaluator development; none were generated here. Real paired model/baseline runs wait for DELTA's frozen verified bundle. New model test evaluation waits for frozen protocol and validation choices. Final comparisons wait for accepted prediction files. See [interfaces](interfaces.md) and [responsibilities](team_responsibilities.md).

## Checks

Completed checks passed with Python 3.14.2 and the already available PyYAML installation:

```sh
python3 scripts/verify_setup.py
python3 -m unittest discover -s tests -v
```

The first checks original/canonical hashes, syntax/JSON, schema/key/calendar/split consistency, current Markdown paths, and ignore/retention rules. The second checks safe migrated script/notebook paths and cleared notebook execution, parses YAML/TOML, and checks owner/path consistency. Neither imports or executes legacy producers, generates data, fits models, or recomputes inherited scores. The new path tests are regression checks for this migration, not evidence that an ML experiment works.

Recorded results: all ten original archive hashes and the unchanged canonical data/evidence copies matched; six Python files parsed; the working notebook JSON/31 cells and 13 code cells parsed; pilot keys/manifest/90-day calendars and 12,000/3,000/3,000 split counts passed; inherited prediction/metric structures passed without rescoring; 53 current Markdown files/paths and expanded ignore/retention checks passed. All three layout unit tests passed (script root/output safety; notebook paths/cleared execution; YAML/TOML/owner/path consistency). No raw CSV exists in the workspace or archive.

Every staged path was reviewed individually: staged blobs matched local bytes, archived originals matched source hashes, and relocated/deleted old paths had the intended preserved replacements. Authored-file whitespace checks passed with inherited CRLF handled explicitly; exact saved prompts and archived sources were excluded from formatting changes. A targeted scan found no saved credentials/private keys or expiring download references. The active legacy source/notebook differences were reviewed against their archived originals and limited to documented migration changes.

Full raw reproduction, notebook runtime, package installation, cross-machine operation, and multi-user coordination remain unverified. PR #2 merged at the user’s direction after agent diff/check review; independent human technical validation remains pending.
