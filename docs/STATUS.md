# Status

_Last updated: 2026-10-08 10:40 NZDT_

## Working rules (set by Brett, 8 Oct)
- One task at a time. Each reply gives everything needed for that one task, repeating earlier detail if necessary.
- Keep this task list current so a task can be recalled after errors or a context reset.

## Deadline sprint: 8 Oct 2026
Recruiter Ben Dixon (ref BH-145793) called; client confirmed as the Treasury; he presents candidates **this afternoon**. Brett promised a Fabric / Power BI demo. Deliverables: (1) public link to a live report, (2) PDF showing the report, design and solution, honest about built vs planned. Speed first; quality additions only if time allows.

| # | Task | Owner | State |
|---|---|---|---|
| T1 | Download 4 Treasury xlsx files to Downloads (Claude's sandbox and the Mac bridge cannot reach budget.govt.nz) | Brett | done |
| T2 | Fabric capacity F2 running in NZ North, admin = brett@bldmcdonaldgmail.onmicrosoft.com; assign `tft-dev` to it | Brett | capacity `tftcapacity` created 10:35 (rg-tft, F2, NZ North, paid from Azure promo credit NZ$353 expiring 4 Nov). Workspace assignment still to do |
| T2b | Sign normal Chrome into Fabric as brett@bldmcdonaldgmail.onmicrosoft.com so Claude can drive it (Chrome is currently signed in to the VUW work tenant: do NOT build there) | Brett | **CURRENT** |
| T3 | Parser written and tested against the real files | Claude | done: `notebooks/nb_ingest_transform.py`, 8 data tests pass on BEFU26 + PREFU26 (Spark write section untested until run in Fabric) |
| T4 | Lakehouse `lh_tft` + notebook: fetch, hash, log, load tables | Claude drives Chrome (Brett prefers delegating browser work to Claude) | pending |
| T5 | Import-mode semantic model + one report page | Brett with Claude's spec | pending |
| T6 | Enable and use Publish to web; get link | Brett | pending |
| T7 | PDF solution brief with screenshots | Claude | pending |
| T8 | Send link + PDF to Ben | Brett | pending |
| Opt | Scheduled pipeline; Git connection; second page; Test/Prod workspaces | | only if time |

## Facts learned 8 Oct
- Source files are tidy: `{round}-economic-forecasts-data.xlsx` has an economic sheet (30 quarterly series) and a fiscal sheet (18 June-year series + 'Is forecast' flag). Rounds confirmed: BEFU26, PREFU26. HYEFU25 has no file of this type in the Data Library (notebook probes for it and logs the result).
- Mac bridge: Downloads folder granted; files staged from /Users/brettkircher/Downloads. Neither the cloud workspace nor the Mac bridge can download from budget.govt.nz; Brett downloads by hand.
- Publish to web: enable the tenant setting early (can take time to apply); test it on a throwaway Direct Lake report before designing the real page; if refused, build an import model.
- Brett is fine with the repo staying public; Claude manages Git.

- A personal Microsoft account cannot create a Fabric capacity; the brett@ org user was given Contributor on the subscription and created it.
- Claude can drive Brett's Chrome directly from this session (tab group already open). Extension does not run in incognito.

## Blockers
- None known. Risk: new pay-as-you-go subscriptions can have no Fabric quota; fallback is a Power BI-only build, labelled as such.

## Notes for resuming
- Brett works on a Mac in the browser only.
- Application for the Reporting Developer contract was submitted 7 Oct 2026 describing this demo as in progress; send the recruiter the public link at v0.1.
- Never describe the demo as further along than it is.
- Capacity costs money while running: remind Brett to pause it at the end of every session.
