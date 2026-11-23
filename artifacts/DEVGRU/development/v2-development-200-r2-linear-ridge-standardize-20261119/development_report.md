# DEVGRU development experiment report

Status: DEVELOPMENT VALIDATION ONLY; PROVISIONAL SETTINGS.

Bundle: `v2-development-200-r2`
Trusted manifest SHA-256: `043a9d183244645f439c6c8ee134bb6e2058f81d847489bbd1270fb87cc3a7c7`

No development test rows were predicted, scored, or used for selection. The final bundle was not opened.

## Validation metrics

     split  rows      MAE     RMSE   signed_bias             model    feature_set selected_ridge_alpha
     train  9200 0.322844 0.504787  1.159266e-15 linear_regression     sales_only                 None
validation  3000 0.334257 0.535999  3.912659e-03 linear_regression     sales_only                 None
     train  9200 0.318679 0.500161  1.377256e-15 linear_regression stockout_aware                 None
validation  3000 0.334190 0.532689 -6.326944e-03 linear_regression stockout_aware                 None
     train  9200 0.322838 0.504790  1.366636e-15  ridge_regression     sales_only                 10.0
validation  3000 0.334256 0.535890  3.791081e-03  ridge_regression     sales_only                 10.0
     train  9200 0.318674 0.500269  1.375518e-15  ridge_regression stockout_aware                100.0
validation  3000 0.334119 0.531885 -6.927126e-03  ridge_regression stockout_aware                100.0

## Ridge alpha selection

   feature_set  alpha  validation_mae
    sales_only   0.01        0.334257
    sales_only   0.10        0.334257
    sales_only   1.00        0.334257
    sales_only  10.00        0.334256
    sales_only 100.00        0.334261
stockout_aware   0.01        0.334190
stockout_aware   0.10        0.334190
stockout_aware   1.00        0.334190
stockout_aware  10.00        0.334181
stockout_aware 100.00        0.334119

## Paired comparison

            model  MAE_sales_only  MAE_stockout_aware  MAE_difference_stockout_aware_minus_sales_only  bootstrap_ci_lower  bootstrap_ci_upper  bootstrap_repetitions  bootstrap_seed  resampled_series       bootstrap_unit                             interpretation
linear_regression        0.334257            0.334190                                       -0.000066           -0.002323            0.002157                   2000             245               200 store-product series negative favors stockout-aware forecasting
 ridge_regression        0.334256            0.334119                                       -0.000137           -0.002290            0.001933                   2000             246               200 store-product series negative favors stockout-aware forecasting

Bootstrap resampled whole store-product series with reproducible percentile 95% intervals. Negative MAE differences favor stockout-aware forecasting.
