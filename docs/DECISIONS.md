# Decision log

| # | Date | Decision | Why | Alternatives |
|---|---|---|---|---|
| 1 | 2026-10-07 | Problem: forecast tracker | Core Treasury product; needs forecasts and actuals joined; sources update on a schedule | Budget spending by vote (changes once a year) |
| 2 | 2026-10-07 | Repository is public | The repo is portfolio evidence | Private |
| 3 | 2026-10-07 | Transformations in Python notebooks | Code can be reviewed and versioned in Git | Dataflow Gen2 |
| 4 | 2026-10-07 | Platform: Microsoft Fabric, browser only | One platform, Mac-compatible | Power BI Desktop (Windows only) |
| 5 | 2026-10-07 | Post-trial hosting: deferred | Not needed until the trial nears its end | Pausable paid capacity plus Power BI Pro |
| 6 | 2026-10-07 | Project files live in this repo; backlog in GitHub Issues | One version-controlled home; survives long sessions | Separate documents |
| 7 | 2026-10-07 | Paid F2 capacity in New Zealand North, paused between sessions (supersedes the free trial) | Fabric trial refused for this tenant (not eligible); F2 is the smallest capacity | Power BI-only build (would not show Fabric) |
| 8 | 2026-10-07 | This project stays personal: own tenant, own cost, public data only. Any VUW proposal (Databricks-based) is a separate project | Avoids conflict of interest and ownership questions | Employer-funded build |

## Open
- Where to store the Stats NZ API key (before v0.2).
- Whether Direct Lake reports can be published publicly; if not, add an import-mode copy.
- How scheduled runs work with a paused capacity (decide in phase 2: fixed daily window, or public report hosted in a separate Pro workspace).
- Power BI trial started 2026-10-07 on the admin user; note its expiry for the public link.
