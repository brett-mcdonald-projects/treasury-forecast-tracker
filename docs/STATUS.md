# Status

_Last updated: 2026-10-08 13:45 NZDT_

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

## Report revision round 1 (requested by Brett 12:44, 8 Oct) - DONE 13:15, awaiting Brett's review
All applied through the Fabric REST API (see `fabric/README.md`), checked in the report and on the public link.
| # | Change | State |
|---|---|---|
| R1 | Slicer wide enough that measure labels are not cut off | done (330 wide, header "Measure") |
| R2 | `period_label` shown as "Period" (also "Forecast round", "Value") | done |
| R3 | Caveat "Independent demonstration by Brett McDonald; not a Treasury product" at top, separate from title | done (yellow banner top right, both pages) |
| R4 | "Loaded by an automated Microsoft Fabric pipeline" under the title, smaller | done |
| R5 | "Source: ..." text bottom middle | done |
| R6 | "Created by Brett McDonald on 8 October 2026" bottom right | done (both pages; static text) |
| R7 | "Source data published" per source, bottom left | done: HYEFU 2025 16 Dec 2025; BEFU 2026 28 May 2026; PREFU 2026 29 Sep 2026 (verified by web search 8 Oct; static text) |
| R8 | "Next publishing date" to the right of R7 | done: "not yet set" (Treasury: timing of next forecast update to be determined later) |
| R9 | "Purpose and function" card: what it does, why, how to use it | done |
| R10 | Page 1 button "Data logs" to page 2; page 2 "Return to tracker" | done, both navigate (also on the public link) |
| R11 | Auto-generated insight | done: DAX measure `fact_headline[Insight]` in the import model, shown in a one-cell table above the chart. Spot-checked against the raw BEFU26 and PREFU26 files (OBEGAL excl. ACC 2026/27: -11,441 to -6,750). Also set sort-by columns (round_name by round_order, measure by measure_sort) so the legend is chronological |

Current page 1 layout (1280x720): title + subtitle top left; caveat + "Data logs" top right; slicer (20,92,330x330); purpose card (20,430,330x220); insight (365,92,895x104); chart (365,202,895x226); matrix (365,434,895x216); four footer texts at y=658.

Round 1 follow-up (13:17, Brett: "looks great"): purpose card given left padding (body text now 9pt so it fits); footers moved to y=652 h=66; PDF brief rebuilt with the new text and fresh exports (docs/brief, also in Brett's Downloads). DONE 13:45.

How the PDF pages were exported: Chrome blocked the normal Export > PDF download (automatic downloads from the Fabric site are blocked after an earlier scripted download attempt; Brett can re-allow it from the address bar). Workaround used: Power BI REST `POST .../reports/{id}/ExportTo {format:'PDF'}` from the page, poll `/exports/{id}`, fetch `/file`, base64 it into the `__dump` article in 45k chunks, read with get_page_text, then rebuild the file from the session transcript with a script. Brief build: `/home/claude/brief/build.py` (Playwright) then pdfunite.

Open after round 1:
- Page 2 title text says a 404 means "not yet published"; Treasury now says the timing of the next update is undetermined. Wording is still accurate, could be softened.
- Matrix shows two decimals for $ million figures and the chart has no unit label (cosmetic).

## Facts learned 8 Oct
- Source files are tidy: `{round}-economic-forecasts-data.xlsx` has an economic sheet (30 quarterly series) and a fiscal sheet (18 June-year series + 'Is forecast' flag). Rounds confirmed: BEFU26, PREFU26. HYEFU25 has no file of this type in the Data Library (notebook probes for it and logs the result).
- Mac bridge: Downloads folder granted; files staged from /Users/brettkircher/Downloads. Neither the cloud workspace nor the Mac bridge can download from budget.govt.nz; Brett downloads by hand.
- Publish to web: enable the tenant setting early (can take time to apply); test it on a throwaway Direct Lake report before designing the real page; if refused, build an import model.
- Brett is fine with the repo staying public; Claude manages Git.

- A personal Microsoft account cannot create a Fabric capacity; the brett@ org user was given Contributor on the subscription and created it.
- Claude can drive Brett's Chrome directly from this session (tab group already open). Extension does not run in incognito.

- Two Chrome browsers are connected to Claude: Browser 1 (Mac, correct, tab group has the Fabric tabs signed in as brett@) and Browser 2 (Windows, NOT to be used; the session flipped to it once mid-task). If tabs vanish, call list_connected_browsers and select the Mac one.
- FASTEST WAY TO EDIT THE REPORT OR MODEL: paste `fabric/tools/fabric_api_helpers.js` into the report tab with the javascript tool (it is lost on every page reload), then getAny / edit / putAny. JS calls must be `await (async()=>{...})()`. To read long output, write it into an `<article id="__dump">` element and use get_page_text. Model updates kept the imported data; refresh via the API works (proved 8 Oct). Close any model-view tab before updating the model.
- Format-pane routine that works (slow fallback): select visual > Format > General > Properties; numeric Size/Position inputs accept typed values + Tab; for text boxes use find + form_input because the floating text toolbar covers the inputs.

## After the deadline (backlog order)
1. Brett reviews report + brief; fix anything he flags.
2. Delete `zz_publish_test`; add relationships/dim tables; theme; unit label on the chart; number formats per measure. (Done 8 Oct: insight measure, chronological sort, friendly field names.)
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
