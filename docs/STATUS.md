# Status

_Last updated: 2026-10-08 10:05 NZDT_

## Working rules (set by Brett, 8 Oct)
- One task at a time. Each reply gives everything needed for that one task, repeating earlier detail if necessary.
- Keep this task list current so a task can be recalled after errors or a context reset.

## Deadline sprint: 8 Oct 2026
Recruiter Ben Dixon (ref BH-145793) called; client confirmed as the Treasury; he presents candidates **this afternoon**. Brett promised a Fabric / Power BI demo. Deliverables: (1) public link to a live report, (2) PDF showing the report, design and solution, honest about built vs planned. Speed first; quality additions only if time allows.

| # | Task | Owner | State |
|---|---|---|---|
| T1 | Download 4 Treasury xlsx files to Downloads (Claude's sandbox and the Mac bridge cannot reach budget.govt.nz) | Brett | **CURRENT** |
| T2 | Fabric capacity F2 running in NZ North, admin = brett@bldmcdonaldgmail.onmicrosoft.com; assign `tft-dev` to it (state from 7 Oct unknown: ask) | Brett | next |
| T3 | Parser written and tested against the real files | Claude | starts when T1 done |
| T4 | Lakehouse `lh_tft` + notebook: fetch, hash, log, load tables | Brett runs Claude's code | pending |
| T5 | Import-mode semantic model + one report page | Brett with Claude's spec | pending |
| T6 | Enable and use Publish to web; get link | Brett | pending |
| T7 | PDF solution brief with screenshots | Claude | pending |
| T8 | Send link + PDF to Ben | Brett | pending |
| Opt | Scheduled pipeline; Git connection; second page; Test/Prod workspaces | | only if time |

## Blockers
- None known. Risk: new pay-as-you-go subscriptions can have no Fabric quota; fallback is a Power BI-only build, labelled as such.

## Notes for resuming
- Brett works on a Mac in the browser only.
- Application for the Reporting Developer contract was submitted 7 Oct 2026 describing this demo as in progress; send the recruiter the public link at v0.1.
- Never describe the demo as further along than it is.
- Capacity costs money while running: remind Brett to pause it at the end of every session.
