# Plan

## Purpose
Demonstrate modern Power BI development on Microsoft Fabric across the full life cycle: build, test, release, operate, change. Audience assumed to be a central agency such as the Treasury.

## Requirements (set by Brett, 7 Oct 2026)
- End to end on one cloud platform (Microsoft); developed entirely in the browser (Mac, no Power BI Desktop).
- Free where possible; paid options only where they change things materially. (The free trial was refused, so a small paid capacity is used.)
- Public data, free, fetched automatically from a predictable source.
- Detect when a source changes, load the new data, refresh the report.
- "Done" is the life cycle, not the build: version control, acceptance testing, maintenance, change and feature deployment.
- Prove concepts first, then MVP, then features. Architecture must absorb new data sources.

## Analytical problem
How has the outlook been revised across forecast rounds (Half Year Update 2025, Budget Update 2026, Pre-election Update 2026, and later rounds as published), and how are actuals tracking against the latest forecast? Descriptive only.

## Sources
| # | Source | Access | Release | Verified |
|---|---|---|---|---|
| 1 | Treasury forecast data files, budget.govt.nz/budget/excel/{round}{year}/... | Direct xlsx download, predictable names | v0.1 | File list seen; contents not yet opened |
| 2 | Stats NZ Aotearoa Data Explorer API (GDP, CPI, unemployment) | REST API with free key | v0.2 | Not yet verified |
| 3 | Treasury monthly financial statements | Unknown; may be PDF only | v0.3 | Not yet verified |

## Architecture
- Workspaces: `tft-dev`, `tft-test`, `tft-prod` on one paid F2 Fabric capacity (New Zealand North), paused between sessions; Fabric deployment pipeline promotes Dev -> Test -> Prod.
- Version control: this GitHub repo, connected to `tft-dev` through Fabric Git integration. Work is issue -> branch -> pull request -> main.
- Lakehouse layers: `Files/landing` (raw, immutable, one folder per fetch) -> bronze (as-parsed) -> silver (conformed long format) -> gold (star schema).
- Control tables: `source_registry` (one row per source: address pattern, fetch method, parser, cadence) and `ingest_log` (hash, fetched_at, status). Adding a source = one registry row + one parser function.
- Orchestration: one scheduled data pipeline: detect/fetch -> transform -> test -> refresh model -> alert on failure.
- Gold model: `fact_observation` (indicator, period, vintage, source, value) with `dim_indicator`, `dim_period`, `dim_vintage`, `dim_source`.
- Reporting: Direct Lake semantic model; master report as the reusable template; import-mode copy only if the public link requires it.
- Secrets: never committed. Storage location for the Stats NZ key to be decided before v0.2.

## Phases
| Phase | Outcome | Done when |
|---|---|---|
| 0 Foundations | Tenant, trial, repo, three workspaces, Git connected | A blank notebook round-trips Fabric -> GitHub -> Fabric |
| 1 Proofs | (a) notebook fetches source 1 and source 2; (b) a trivial report is published publicly; (c) code edited in GitHub is pulled into Fabric; (d) Dev -> Test promotion works | All four pass or the design changes |
| 2 MVP v0.1 | Source 1 end to end, one report page | In Prod via signed UAT, tagged, public link live |
| 3 v0.2 | Source 2 added via the registry; forecast-versus-actual page | Released through the full change cycle |
| 4 v0.3 | Failure alerts, data-freshness page, runbook exercised, source 3 | A simulated failure is detected and recovered from the runbook |

## Out of scope for now
Row-level security, Copilot features, cost optimisation beyond the 60-day trial (decide later).
