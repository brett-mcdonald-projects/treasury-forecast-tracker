# Treasury Forecast Tracker

A demonstration Microsoft Fabric and Power BI solution by Brett McDonald.

**Question:** how has New Zealand's economic and fiscal outlook been revised across the Treasury's successive forecast rounds? (Planned next: how actual results are tracking against the latest forecast.)

**Live report:** https://app.fabric.microsoft.com/view?r=eyJrIjoiNzdhOWU5OGItZWYyYS00ODAxLTg0ODgtYzg2ODNlYTFmZTBjIiwidCI6ImZlNzZjMzBlLWY2OWUtNDczNy1hNzMwLTk0OGI1MDIxZTFiOCJ9

**Solution brief (PDF):** [docs/brief](docs/brief/Treasury_Forecast_Tracker_Solution_Brief_Brett_McDonald.pdf)

**Status:** working and scheduled (8 Oct 2026): a Fabric pipeline runs the load and the model refresh daily at 7:00 am. A failure alert, Dev/Test/Prod and Git-connected deployment are still to come. See [docs/STATUS.md](docs/STATUS.md).

This is an independent portfolio project built on public data. It is not affiliated with or endorsed by the Treasury or Stats NZ. It describes forecast revisions and outturns; it does not assess forecast quality.

## How it works

1. A Fabric pipeline (`pl_forecast_refresh`, daily at 7:00 am) runs the ingest notebook, which probes each registered public source and compares a file hash against an ingest log.
2. When a source has changed, the raw file is landed untouched in the lakehouse, then cleaned and loaded to a star schema.
3. Eight automated data tests run; the reporting tables refresh only if all pass. (Reconciliation against the Treasury's published tables is not built yet.)
4. A second notebook syncs the lakehouse SQL endpoint, refreshes the report's semantic model and waits for the result, so the Power BI report updates.

Planned: changes move Dev -> Test (acceptance testing) -> Prod through a Fabric deployment pipeline, with this repository connected to the Dev workspace. Today there is one workspace, and the notebook, pipeline, report and model definitions are copied here by hand (see [fabric/](fabric/README.md)).

## Documents

| File | Purpose |
|---|---|
| [docs/PLAN.md](docs/PLAN.md) | Scope, architecture, phases |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Decision log |
| [docs/STATUS.md](docs/STATUS.md) | Current state and next step |
| [docs/UAT.md](docs/UAT.md) | Acceptance checklist per release |
| [docs/RUNBOOK.md](docs/RUNBOOK.md) | Operating and recovery procedures |
| [CHANGELOG.md](CHANGELOG.md) | Release history |

Backlog and defects are tracked in GitHub Issues.

## Data sources and licence

- The Treasury, Economic and Fiscal Update data files (budget.govt.nz)
- Stats NZ, Aotearoa Data Explorer (planned)

Source data remains under its publishers' terms (to be confirmed and recorded here).

## How it was built

Requirements, subject and approach were set by Brett McDonald. An AI assistant (Claude) wrote the notebook code and the DAX measures, built the pipeline, and carried out much of the Fabric configuration and report build under his direction.
