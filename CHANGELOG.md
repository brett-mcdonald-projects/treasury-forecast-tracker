# Changelog

## Unreleased

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
