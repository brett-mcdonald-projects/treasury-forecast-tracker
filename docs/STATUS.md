# Status

_Last updated: 2026-10-07 18:10 NZDT_

## Where we are
Phase 0 (Foundations), not yet complete. Nothing built in Fabric yet.

## Done
- Plan and decisions 1-6 agreed.
- Project files pushed to GitHub (repo public, Claude has push access).
- Brett has an existing free Azure account (created via portal.azure.com for another project).

- Tenant domain: bldmcdonaldgmail.onmicrosoft.com. Dedicated admin user created: brett@bldmcdonaldgmail.onmicrosoft.com (use this for all Fabric work).

- Fabric trial refused (account not eligible); a Power BI trial started instead. Tenant home region is New Zealand North.
- Workspace `tft-dev` created (no capacity yet, so no Fabric items).
- Decision 7: use a paid F2 capacity.

## Next step
1. Brett: confirm an Azure subscription exists (pay-as-you-go), signed in to portal.azure.com with the personal account.
2. Brett: create Fabric capacity F2 in New Zealand North, admin = brett@bldmcdonaldgmail.onmicrosoft.com. Set a budget alert. Pause when not working.
3. Brett: assign `tft-dev` to the capacity; create lakehouse `lh_tft`; create `tft-test`, `tft-prod`.
4. Connect `tft-dev` to this repo; proof (c): blank notebook round trip.

## Blockers
- None.

## Notes for resuming
- Brett works on a Mac in the browser only.
- Application for the Reporting Developer contract was submitted 7 Oct 2026 describing this demo as in progress; send the recruiter the public link at v0.1.
- Never describe the demo as further along than it is.
- Capacity costs money while running: remind Brett to pause it at the end of every session.
