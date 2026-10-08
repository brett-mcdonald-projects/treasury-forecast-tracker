# Step 2 of pipeline pl_forecast_refresh. Runs only after the ingest notebook has succeeded.
#   a) ask the lakehouse SQL analytics endpoint to sync the Delta tables the ingest notebook just wrote
#   b) refresh the import-mode semantic model behind the public report and wait for the outcome
# Any failure raises, which fails the pipeline run.
import time, requests

WORKSPACE_ID = "6fc0ae0f-a1c1-485e-b7c3-0022d860b8a8"      # tft-dev
SQL_ENDPOINT_ID = "90d79a36-3161-4ef3-b4e8-f1ccbfe9ab0a"   # SQL analytics endpoint of lakehouse lh_tft
DATASET_ID = "68cf5727-e77f-4361-ba33-7c4c286b0464"        # sm_forecast_tracker_public
FABRIC = "https://api.fabric.microsoft.com/v1"
REFRESHES = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/refreshes"

def headers():
    return {"Authorization": "Bearer " + notebookutils.credentials.getToken("pbi"), "Content-Type": "application/json"}

# a) SQL endpoint sync. Added after the first pipeline run (8 Oct 2026) refreshed the model
#    about 10 seconds before the endpoint had picked up the new ingest_log rows.
r = requests.post(f"{FABRIC}/workspaces/{WORKSPACE_ID}/sqlEndpoints/{SQL_ENDPOINT_ID}/refreshMetadata",
                  headers=headers(), json={}, timeout=600)
if r.status_code == 202:                                    # long-running: poll the operation
    op = r.headers.get("x-ms-operation-id")
    for _ in range(60):
        time.sleep(5)
        state = requests.get(f"{FABRIC}/operations/{op}", headers=headers(), timeout=60).json()
        if state.get("status") in ("Succeeded", "Failed"):
            break
    if state.get("status") != "Succeeded":
        raise Exception(f"SQL endpoint sync did not succeed: {state}")
    r = requests.get(f"{FABRIC}/operations/{op}/result", headers=headers(), timeout=60)
if r.status_code != 200:
    raise Exception(f"SQL endpoint sync rejected: {r.status_code} {r.text[:300]}")
tables = r.json().get("value", [])
failed = [t for t in tables if t.get("status") == "Failure"]
print("SQL endpoint sync:", {t["tableName"]: t["status"] for t in tables})
if failed:
    raise Exception(f"SQL endpoint sync failed for: {failed}")

# b) Model refresh
r = requests.post(REFRESHES, headers=headers(), json={"notifyOption": "NoNotification"}, timeout=60)
if r.status_code not in (200, 202):
    raise Exception(f"Refresh request rejected: {r.status_code} {r.text[:300]}")
latest = {}
for _ in range(90):                          # wait up to 15 minutes
    time.sleep(10)
    latest = requests.get(REFRESHES + "?$top=1", headers=headers(), timeout=60).json()["value"][0]
    if latest.get("status") != "Unknown":    # "Unknown" means still running
        break
print("Model refresh:", latest.get("status"), "| ended:", latest.get("endTime"))
if latest.get("status") != "Completed":
    raise Exception(f"Model refresh did not complete: {latest}")
