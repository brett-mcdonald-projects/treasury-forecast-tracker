# Treasury Forecast Tracker

A demonstration Microsoft Fabric and Power BI solution by Brett McDonald.

**Question:** how has New Zealand's economic and fiscal outlook been revised across the Treasury's successive forecast rounds, and how are actual results tracking against the latest forecast?

**Live report:** https://app.fabric.microsoft.com/view?r=eyJrIjoiNzdhOWU5OGItZWYyYS00ODAxLTg0ODgtYzg2ODNlYTFmZTBjIiwidCI6ImZlNzZjMzBlLWY2OWUtNDczNy1hNzMwLTk0OGI1MDIxZTFiOCJ9

**Solution brief (PDF):** [docs/brief](docs/brief/Treasury_Forecast_Tracker_Solution_Brief_Brett_McDonald.pdf)

**Status:** first release working (8 Oct 2026); scheduling, Dev/Test/Prod and Git-connected deployment still to come. See [docs/STATUS.md](docs/STATUS.md).

This is an independent portfolio project built on public data. It is not affiliated with or endorsed by the Treasury or Stats NZ. It describes forecast revisions and outturns; it does not assess forecast quality.

## How it works

1. A Fabric notebook (run on demand for now; scheduling is the next step) probes each registered public source and compares a file hash against an ingest log.
2. When a source has changed, the raw file is landed untouched in the lakehouse, then cleaned and loaded to a star schema.
3. Automated data tests run, including reconciliation to a published figure.
4. The semantic model refreshes and the Power BI report updates.

Planned: changes move Dev -> Test (acceptance testing) -> Prod through a Fabric deployment pipeline, with this repository connected to the Dev workspace. Today there is one workspace and the notebook source is copied here by hand.

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

Requirements, subject and approach were set by Brett McDonald. An AI assistant (Claude) wrote the notebook code and carried out much of the Fabric configuration under his direction.
