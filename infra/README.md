# Infrastructure

| File | What it is |
|---|---|
| `capacity-schedule.json` | ARM template: two consumption Logic Apps (`la-tft-capacity-resume` at 07:00, `la-tft-capacity-suspend` at 19:00, New Zealand time) that call the Fabric capacity `resume` and `suspend` actions through an Azure Resource Manager connection, plus that connection (`arm-tft`). Deployed to `rg-tft` on 8 October 2026. |

Live hours are parameters of the template (`liveFromHour`, `liveToHour`, `timeZone`); change them there and redeploy. The note on the report ("Live 7:00 am to 7:00 pm NZ time") is typed text and must be changed by hand to match: the report cannot read the Logic App schedule.

Deploy (Azure Cloud Shell, bash):

```
az deployment group what-if -g rg-tft --template-file infra/capacity-schedule.json
az deployment group create  -g rg-tft --template-file infra/capacity-schedule.json
```

After the first deployment the connection must be authorised once by a user with rights to the capacity: open the connection `arm-tft` in the Azure portal, Edit API connection, Authorize, Save. The Logic Apps then act as that user; nothing else needs a role assignment.

Why Logic Apps and not an Automation runbook: a runbook's managed identity needs a role assignment on the resource group, which needs Owner rights the working account does not have. The ARM connector signs in as the user instead.

Cost basis (Azure retail prices, NZ North, NZD, 8 Oct 2026): Fabric capacity NZ$0.3887 per CU-hour, so F2 (2 CU) is NZ$0.7774 an hour: NZ$18.66 a day running 24 hours, NZ$9.33 a day for 12 hours. OneLake storage NZ$0.053 per GB-month. Logic Apps consumption: 4 actions a day, within the free grant.
