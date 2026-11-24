# Team presentation handoff

Use the reconciled `submission_local/presentation/slides.md` and `submission_local/report/final_report.md`. New verified run: `final-1000-attested-20261124T094349Z`. The November20 identity remains unverified; these are new preserved outputs, not recovered old files. No scoring or plots were regenerated for this handoff.

## Results to present
Each of eight model/condition/baseline test groups contains15,000 matched observations over183 stores. Ridge-aware is best by MAE and RMSE:
- Ridge-aware MAE0.377191, RMSE0.618490, bias-0.056262.
- Linear-aware MAE0.377354, RMSE0.618750.
- Relative aware MAE improvement: Ridge0.343760%, Linear0.305113% (modest).
- Tree aware MAE0.397487 versus sales0.396510: worsens0.246452%.
- Seven-day mean MAE0.381992; persistence0.472728.

| Model | Test MAE difference, aware minus sales | Correct paired95% interval |
| --- | ---: | --- |
| Linear | -0.001154878581 | [-0.002183659272,-0.000134824602] |
| Ridge | -0.001301106070 | [-0.002301963340,-0.000290025655] |
| Tree | +0.000977206891 | [+0.000054234535,+0.001937705144] |

Negative favors aware. These conditional pooled-row whole-store intervals exclude zero; do not say all FINAL intervals include zero. Development R3 intervals are different and remain zero-spanning. This is not a test of Ridge-versus-Linear superiority or a claim that effects generalize.

## Essential interpretation
Overall improvement does NOT imply better stockout-date predictions. Ridge stockout-day MAE increases0.412801 to0.415083; fully-stocked-date MAE improves0.353003 to0.349039. Linear has the same directional caveat. There are8,606 fully-stocked and6,394 stockout test targets per group. Both linear models underpredict on average.

Earlier pilot/test exposure and retrospective complete-90-day series selection make this descriptive, not pristine confirmatory evidence. The bootstrap conditions on selected fitted models; common calendar shocks, cross-store dependence and selection/refitting uncertainty are not resolved. Target is normalized observed sales, not latent demand, lost sales, or measured food-waste reduction.

The prospective freeze records Timothy's direct authorization and his November24,2026 project-lead attestation that DEVGRU/SAS approved. Their original messages/dates were unavailable; do not describe the record as direct signatures from all teammates.

## Slides/tables to reconcile in any external deck
- Slides5?6: frozen train-only controls; Forest explicitly excluded, not called a failed optional implementation.
- Slide7 and report final-results table: verified MAEs, Ridge-aware best by MAE/RMSE; distinguish validation from test rows.
- Slide8: replace ALL three old intervals and the all-include-zero conclusion with the table above; 2,000 whole-store draws, pooled-row denominator, seed245.
- Slide9: add stockout-day deterioration and negative bias; show aggregate versus subgroup distinction.
- Slides10?11 and report abstract/conclusion: modest aggregate effects, historical exposure, lead-attestation provenance, no causal/sustainability overclaim.
- Slide12 / appendix: new run ID and original manifest/freeze; remove legacy run commands and the missing November20 output citation.

No PDF/PPTX exports or automatic build pipeline were located in the relevant project roots. Update each actual external presentation PPTX/PDF and individual report PDF separately, visually inspect it, and verify it matches the reconciled Markdown. Do not claim those external files were updated by this publication.

## Demonstrate without final data
1. Open `docs/TEAM_FINAL_PIPELINE_HANDOFF.md` to explain ownership and raw-to-results flow.
2. Open the supplied verified results CSV and select split=test in the original overall/interval tables.
3. Explain one corrected interval and the subgroup caveat.
4. Run the guide's small-package SHA-256 check. Optionally show `python -m scripts.sas_final_evaluation check` blocked with closed main gates.
5. Use the guide's optional synthetic test command only if you want a toy demonstration. Never launch real final scoring or retune models.

Saved outputs are the demo; no new graph, metric, fitted model or experiment is required. For tomorrow, review the scope/attestation/evidence package, merge only after human review, pull main, finish external exports and rehearsals, and obtain the separately approved bulk archive if full prediction-level evidence is needed. Git alone contains a partial mirror.
