# Fabric item definitions

Source-controlled copies of what is deployed in the `tft-dev` workspace.

| Path | What it is |
|---|---|
| `report/Treasury Forecast Tracker.Report/` | The Power BI report in PBIR format (one JSON file per page and visual), exported with the Fabric REST API on 8 October 2026 (last synced 2:15 pm). The Microsoft base theme file is not included. |
| `pipeline/pl_forecast_refresh.json` | The Data Factory pipeline: two notebook activities in sequence (ingest and transform, then refresh the report model), with the daily 7:00 am schedule noted. |
| `semantic-model/Insight.dax` | The `Insight` measure on `fact_headline` in the import model `sm_forecast_tracker_public`. |
| `semantic-model/definition/tables/` | TMDL for the two tables that carry hand-made changes: `fact_headline` (measures `Insight`, `Forecast value` with a dynamic format string, `Chart title`, `Unit label`, `Table title`; sort-by columns) and `ingest_log` (format strings). The SQL endpoint host name is replaced with a placeholder. |
| `tools/fabric_api_helpers.js` | Browser-console helpers used to read and update item definitions through the Fabric REST API. |

The notebooks the pipeline runs are in `/notebooks` (`nb_ingest_transform.py`, `nb_refresh_model.py`).

Model settings made alongside the measures: `fact_headline[round_name]` is sorted by `round_order`, and `fact_headline[measure]` by `measure_sort`.

These files are a manual export for now. Connecting the workspace to this repository with Fabric Git integration (backlog) will replace the manual step.
