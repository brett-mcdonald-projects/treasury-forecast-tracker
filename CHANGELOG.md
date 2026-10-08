# Changelog

## Unreleased

## v0.3 - 2026-10-08
- Pipeline `pl_forecast_refresh`: ingest notebook, then `nb_refresh_model` (sync the lakehouse SQL endpoint, refresh the import model, wait for the result). Scheduled daily at 7:00 am New Zealand time.
- Two end-to-end pipeline runs completed. The first showed the model refreshing before the SQL endpoint had the new log rows; the sync step was added and the second run confirmed it.
- Units of measure: chart title and subtitle and the table title follow the selected measure; axis and table values are formatted as % or $ (dynamic format string).
- Pipeline and data quality page now lists every run, newest first, with unambiguous timestamps.
- Solution brief rebuilt to describe the pipeline, with fresh page exports.
- Pipeline definition, second notebook and model table definitions added to the repository.

## v0.2 - 2026-10-08
- Report layout revised: caveat banner, subtitle, "Purpose and function" card, source and publication-date footers, created-by line, wider measure slicer, friendly field names.
- Page navigation buttons: "Data logs" and "Return to tracker".
- Automatic insight: `Insight` measure states what the latest forecast round changed for the selected measure.
- Forecast rounds now sort chronologically and measures in a fixed order (sort-by columns).
- Report definition (PBIR), measure and API helpers added under `fabric/`.
- Purpose card padded; footer text boxes resized so they do not show scroll bars in exports.
- Solution brief updated to describe the revised report, with fresh page exports (taken through the Power BI export API).

## v0.1 - 2026-10-08
- Ingest and transform notebook: source registry, hash-based change detection, raw landing, star schema, eight data tests.
- Lakehouse `lh_tft` loaded with three forecast rounds (HYEFU25, BEFU26, PREFU26).
- Direct Lake model, import model for public publishing, two-page Power BI report, public link.
- Solution brief (docs/brief).
- Project scaffolding: plan, decision log, status, acceptance template.
