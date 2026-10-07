# Acceptance testing

Each release is tested in `tft-test` before promotion to `tft-prod`. Copy the template per release.

## Template: vX.Y
| # | Check | Expected | Result | Tester | Date |
|---|---|---|---|---|---|
| 1 | Pipeline runs end to end in Test | Succeeds; ingest_log has a new row | | | |
| 2 | Re-run with no source change | No new load; logged as unchanged | | | |
| 3 | Reconciliation | One reported figure matches the published document exactly | | | |
| 4 | Report pages | Render without errors; filters behave | | | |
| 5 | Method note | States sources, as-at date and caveats | | | |

Sign-off: ______  Date: ______
