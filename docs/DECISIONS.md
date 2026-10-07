# Decision log

| # | Date | Decision | Why | Alternatives |
|---|---|---|---|---|
| 1 | 2026-10-07 | Problem: forecast tracker | Core Treasury product; needs forecasts and actuals joined; sources update on a schedule | Budget spending by vote (changes once a year) |
| 2 | 2026-10-07 | Repository is public | The repo is portfolio evidence | Private |
| 3 | 2026-10-07 | Transformations in Python notebooks | Code can be reviewed and versioned in Git | Dataflow Gen2 |
| 4 | 2026-10-07 | Platform: Microsoft Fabric trial, browser only | One platform, free for 60 days, Mac-compatible | Power BI Desktop (Windows only) |
| 5 | 2026-10-07 | Post-trial hosting: deferred | Not needed until the trial nears its end | Pausable paid capacity plus Power BI Pro |
| 6 | 2026-10-07 | Project files live in this repo; backlog in GitHub Issues | One version-controlled home; survives long sessions | Separate documents |

## Open
- Where to store the Stats NZ API key (before v0.2).
- Whether Direct Lake reports can be published publicly; if not, add an import-mode copy.
- Trial start date and expiry (record once started).
