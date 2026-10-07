# Status

_Last updated: 2026-10-08 12:50 NZDT_

## Working rules (set by Brett, 8 Oct)
- One task at a time. Each reply gives everything needed for that one task, repeating earlier detail if necessary.
- Keep this task list current so a task can be recalled after errors or a context reset.

## Deadline sprint: 8 Oct 2026
Recruiter Ben Dixon (ref BH-145793) called; client confirmed as the Treasury; he presents candidates **this afternoon**. Brett promised a Fabric / Power BI demo. Deliverables: (1) public link to a live report, (2) PDF showing the report, design and solution, honest about built vs planned. Speed first; quality additions only if time allows.

| # | Task | Owner | State |
|---|---|---|---|
| T1 | Download 4 Treasury xlsx files to Downloads (Claude's sandbox and the Mac bridge cannot reach budget.govt.nz) | Brett | done |
| T2 | Fabric capacity F2 running in NZ North, admin = brett@bldmcdonaldgmail.onmicrosoft.com; assign `tft-dev` to it | Brett | capacity `tftcapacity` created 10:35 (rg-tft, F2, NZ North, paid from Azure promo credit NZ$353 expiring 4 Nov). `tft-dev` assigned to it 10:43 (workspace id 6fc0ae0f-a1c1-485e-b7c3-0022d860b8a8) |
| T2b | Sign normal Chrome into Fabric as brett@bldmcdonaldgmail.onmicrosoft.com so Claude can drive it (Chrome is currently signed in to the VUW work tenant: do NOT build there) | Brett | done 10:40 |
| T3 | Parser written and tested against the real files | Claude | done: `notebooks/nb_ingest_transform.py`, 8 data tests pass on BEFU26 + PREFU26 (Spark write section untested until run in Fabric) |
| T4 | Lakehouse `lh_tft` + notebook: fetch, hash, log, load tables | Claude drives Chrome | done 10:55. Notebook `nb_ingest_transform` (id 9c0ed747-0f7f-432a-9a2e-1c545a4c8c7a) ran in Fabric: fetched HYEFU25, BEFU26, PREFU26 live from budget.govt.nz (HYEFU26 = 404 not_published, logged), 8/8 tests passed, tables: dim_round 3, dim_series 48, fact_forecast 12,411, fact_headline 1,421, fact_revision 468, ingest_log, source_registry, test_results |
| T5 | Semantic models + report | Claude (Brett delegated all of it) | DONE 11:30. Import model `sm_forecast_tracker_public` (id 68cf5727-e77f-4361-ba33-7c4c286b0464); Direct Lake model `sm_forecast_tracker`. Report `Treasury Forecast Tracker` (id 92794f35-4986-4e37-935f-173abf578c2e), canvas 1280x720: page "Forecast tracker" (single-select slicer on fact_headline[measure], line chart period_label x value x round_name sorted by period_label asc, matrix, title + note text boxes, page filter period_end on or after 01/07/2022) and page "Pipeline and data quality" (ingest_log and test_results tables). No DAX measures or relationships yet (model-view editing was unresponsive in a background tab) |
| T6 | Publish to web | Claude | DONE 11:30. First embed code showed a stale cached placeholder, so it was deleted and re-created. CURRENT PUBLIC LINK: https://app.fabric.microsoft.com/view?r=eyJrIjoiNzdhOWU5OGItZWYyYS00ODAxLTg0ODgtYzg2ODNlYTFmZTBjIiwidCI6ImZlNzZjMzBlLWY2OWUtNDczNy1hNzMwLTk0OGI1MDIxZTFiOCJ9 (verified rendering both pages). Saved edits can take up to an hour to show publicly. The link only works while the F2 capacity is running |
| T7 | PDF solution brief | Claude | DONE 11:40: docs/brief/ (2-page brief + 2 pages exported from Power BI). States built vs not built, and that Claude wrote the code and did much of the configuration |
| T8 | Send link + PDF to Ben Dixon | Brett | **CURRENT** |
| Opt | Scheduled pipeline; Git connection; second page; Test/Prod workspaces | | only if time |

## Report revision round 1 (requested by Brett 12:44, 8 Oct) - CURRENT
| # | Change | State |
|---|---|---|
| R1 | Slicer wide enough that measure labels are not cut off | todo |
| R2 | Rename `period_label` to "Period" (and tidy `measure` header) | todo |
| R3 | Caveat "Independent demonstration by Brett McDonald; not a Treasury product" at top, separate from title | todo |
| R4 | "Loaded by an automated Microsoft Fabric pipeline" under the title, smaller | todo |
| R5 | "Source: ..." text bottom middle | todo |
| R6 | "Created by Brett McDonald on [date]" bottom right | todo |
| R7 | "Source data published on [date]" per source, bottom left (dates must be verified, not guessed) | todo |
| R8 | "Next publishing date for sources ..." to the right of R7 (verify) | todo |
| R9 | "Purpose and function" card: what it does, why, how to use it | todo |
| R10 | Page 1 link "Data logs" to page 2; page 2 "Return to tracker" | todo |
| R11 | Auto-generated insights: Brett asked whether possible. Proposal: rule-based insight sentence per measure generated in the notebook (largest revision between the latest two rounds), stored as a column on fact_headline so the slicer drives it with no relationships | proposed |

## Facts learned 8 Oct
- Source files are tidy: `{round}-economic-forecasts-data.xlsx` has an economic sheet (30 quarterly series) and a fiscal sheet (18 June-year series + 'Is forecast' flag). Rounds confirmed: BEFU26, PREFU26. HYEFU25 has no file of this type in the Data Library (notebook probes for it and logs the result).
- Mac bridge: Downloads folder granted; files staged from /Users/brettkircher/Downloads. Neither the cloud workspace nor the Mac bridge can download from budget.govt.nz; Brett downloads by hand.
- Publish to web: enable the tenant setting early (can take time to apply); test it on a throwaway Direct Lake report before designing the real page; if refused, build an import model.
- Brett is fine with the repo staying public; Claude manages Git.

- A personal Microsoft account cannot create a Fabric capacity; the brett@ org user was given Contributor on the subscription and created it.
- Claude can drive Brett's Chrome directly from this session (tab group already open). Extension does not run in incognito.

- Two Chrome browsers are connected to Claude: Browser 1 (Mac, correct, tab group has the Fabric tabs signed in as brett@) and Browser 2 (Windows, NOT to be used; the session flipped to it once mid-task). If tabs vanish, call list_connected_browsers and select the Mac one.
- Format-pane routine that works: select visual > Format > General > Properties; numeric Size/Position inputs accept typed values + Tab; for text boxes use find + form_input because the floating text toolbar covers the inputs.

## After the deadline (backlog order)
1. Brett reviews report + brief; fix anything he flags.
2. Delete `zz_publish_test`; add relationships/dim tables and a revision measure; sort rounds chronologically; friendly field names; theme.
3. Scheduled pipeline + failure alert; connect workspace to this repo (Fabric Git integration); Test/Prod workspaces + deployment pipeline; UAT run.
4. Stats NZ actuals as source 2.
5. Capacity: F2 bills hourly from the NZ$353 Azure credit (expires 4 Nov 2026); pausing it takes the public link down.

## Blockers
- None known. Risk: new pay-as-you-go subscriptions can have no Fabric quota; fallback is a Power BI-only build, labelled as such.

## Notes for resuming
- Brett works on a Mac in the browser only.
- Application for the Reporting Developer contract was submitted 7 Oct 2026 describing this demo as in progress; send the recruiter the public link at v0.1.
- Never describe the demo as further along than it is.
- Capacity costs money while running: remind Brett to pause it at the end of every session.
