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
| 9 | 2026-10-08 | Public report runs on an import-mode copy of the model | Publish to web refused the Direct Lake report | Power BI Embedded; sharing inside the tenant only |
| 10 | 2026-10-08 | Report and model changes are made as code through the Fabric REST API (getDefinition / updateDefinition) and the result is exported to `fabric/` | Repeatable, reviewable, and far faster than clicking; works from a Mac browser | Hand editing in the web designer |
| 11 | 2026-10-08 | The automatic insight is a DAX measure in the model, shown in a one-cell table | Report-level measures are not supported by Publish to web; card visuals truncated long text | Sentence generated in the notebook; Copilot narrative (needs a larger capacity) |
| 12 | 2026-10-08 | The pipeline is two notebook activities; the model refresh is called from a notebook through the Power BI REST API | A semantic-model-refresh activity needs a connection that must be signed in by hand; a notebook uses the run identity and can wait for and check the result | Semantic model refresh activity; scheduled refresh on the model (no ordering with the load) |
| 13 | 2026-10-08 | The refresh notebook first syncs the lakehouse SQL endpoint (refreshMetadata) | The first pipeline run refreshed the import model before the endpoint showed the rows just written | Fixed wait; point the import model at the Delta tables directly |
| 14 | 2026-10-08 | Schedule: daily at 7:00 am New Zealand time, to 31 Dec 2026 | The source changes a few times a year; a daily probe is cheap because unchanged files are skipped by hash | Hourly; event-driven (no event source available) |
| 15 | 2026-10-08 | Units are shown through model measures (dynamic titles and a dynamic format string) | One chart and one table serve measures in different units | A separate visual per unit |
| 16 | 2026-10-08 | Capacity runs 7:00 am to 10:00 pm NZ time, switched by two Logic Apps using an ARM connection signed in as Brett | 15 hours a day uses most of the trial credit by 4 Nov with about NZ$45 spare; the ARM connector needs no role assignment, which the working account cannot grant | Automation runbook with managed identity (needs Owner); 12 hours (leaves NZ$105 unused); 24 hours (credit gone by 27 Oct) |

## Open
- Where to store the Stats NZ API key (before v0.2).
- The subscription is a free trial that ends 4 Nov 2026 (credit US$200). Decide before then whether to upgrade to pay-as-you-go (about NZ$12 a day at 15 hours) or let the demo lapse; the public link dies with the capacity.
- Power BI trial started 2026-10-07 on the admin user; note its expiry for the public link.
