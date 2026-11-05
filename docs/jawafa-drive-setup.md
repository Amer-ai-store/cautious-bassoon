# Jawafa Drive integration

The public GitHub Pages dashboard cannot authenticate to a private Google Drive folder by itself. Deploy the read-only verifier on a private authenticated runner. Grant a dedicated Google service account `drive.readonly` access to the Jawafa export folder, save credentials in a private secret store, and keep all CSV contents private. Run `tools/jawafa_drive_readonly_verify.py` to check all files using pagination and SHA-256 before publishing only non-sensitive aggregates to an authenticated dashboard API. Never write to the original financial database.

## GitHub Actions failure 42016753725 (2026-11-05)

The `inventory` job failed at `Validate federation configuration` (step 5). The runner resolved BOTH `vars.JAWAFA_WIF_PROVIDER` and `vars.JAWAFA_WIF_SERVICE_ACCOUNT` to empty strings. Python and pip succeeded; Google Cloud authentication and the Drive export check were skipped. This is a **missing trust configuration**, not a Python or Drive checksum error. Do not rerun and count it as fixed until a new job successfully authenticates and verifies the source files.

### One-time setup by a Google Cloud administrator

1. In the **correct Google Cloud project** enable **IAM, IAM Credentials, Security Token Service, and Google Drive API**. Create or reuse a **dedicated service account** without database write roles.
2. Create a **Workload Identity Pool** and OIDC provider with issuer `https://token.actions.githubusercontent.com`. Map `google.subject=assertion.sub`, `attribute.repository=assertion.repository`, and `attribute.ref=assertion.ref`. Restrict the provider with **both** `assertion.repository == 'Amer-ai-store/cautious-bassoon'` and `assertion.ref == 'refs/heads/codespace-cautious-bassoon-pjv45qw999wj396px'` (update the ref when the default branch changes). Do not grant federation to every GitHub repository.
3. On the service account grant only `roles/iam.workloadIdentityUser` to the principal set from this specific identity pool and repository. Example principal: `principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/attribute.repository/Amer-ai-store/cautious-bassoon`. The provider condition must independently restrict the branch.
4. Share only the Jawafa export folder in private Google Drive with the service account's email as **Viewer**. The verifier currently expects `inventory_tables.csv`, `manifest_sha256.csv`, and `data/`. WIF authentication by itself does **not** grant Drive folder access.
5. In **this repository**, open **Settings → Secrets and variables → Actions → Variables** and add the two **repository variables** shown below. Do not place a JSON service-account key or any private token in repository variables or source code. Other repositories' variables are not inherited.

| Name | Value (replace placeholders with actual GCP resources) |
| --- | --- |
| `JAWAFA_WIF_PROVIDER` | `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID` |
| `JAWAFA_WIF_SERVICE_ACCOUNT` | `SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com` |

An authenticated admin can also save those identifiers using GitHub CLI:

```bash
gh variable set JAWAFA_WIF_PROVIDER -R Amer-ai-store/cautious-bassoon --body 'projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID'
gh variable set JAWAFA_WIF_SERVICE_ACCOUNT -R Amer-ai-store/cautious-bassoon --body 'SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com'
```

### Required evidence before closing

- Trigger **a new** `Jawafa Drive inventory verification` run and confirm **all three** steps succeed: federation preflight, Google OIDC authentication, and private export verification.
- Independently confirm service account Viewer access to the correct Drive folder, expected file coverage, and each manifest SHA-256 before saying `verified`.
- Record new run URL, timestamp, source evidence and QA review. No CSV data, finance details, or tokens go into public Actions logs or GitHub Pages.
- **Do not claim** GATE-15 acceptance, live SQL connection, financial reconciliation, or any original Jawafa_DB modification based on this workflow alone.

**Until the Google Cloud identity and repository variables are actually configured and a new run passes: `BLOCKED — NOT VERIFIED`.**
