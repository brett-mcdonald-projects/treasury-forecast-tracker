# Fabric item definitions

Source-controlled copies of what is deployed in the `tft-dev` workspace.

| Path | What it is |
|---|---|
| `report/Treasury Forecast Tracker.Report/` | The Power BI report in PBIR format (one JSON file per page and visual), exported with the Fabric REST API on 8 October 2026. The Microsoft base theme file is not included. |
| `semantic-model/Insight.dax` | The `Insight` measure on `fact_headline` in the import model `sm_forecast_tracker_public`. |
| `tools/fabric_api_helpers.js` | Browser-console helpers used to read and update item definitions through the Fabric REST API. |

Model settings made alongside the measure: `fact_headline[round_name]` is sorted by `round_order`, and `fact_headline[measure]` by `measure_sort`.

These files are a manual export for now. Connecting the workspace to this repository with Fabric Git integration (backlog) will replace the manual step.
