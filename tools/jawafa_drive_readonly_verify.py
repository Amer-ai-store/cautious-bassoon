#!/usr/bin/env python3
"""Jawafa Drive inventory verifier. Run only on an authorized private host.
Requires pip install google-api-python-client google-auth
and GOOGLE_APPLICATION_CREDENTIALS pointing to a read-only service account JSON.
Share the Drive folder with that service account before running.
Never publish CSV contents, tokens or financial records to GitHub Pages.
"""
import csv, hashlib, io, json, os, sys

FOLDER = os.environ.get("JAWAFA_DRIVE_FOLDER", "1X9MuorGVaaAwolc25_MG4kgKQGPiWard")
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
def client():
    import google.auth
    from googleapiclient.discovery import build
    creds, _ = google.auth.default(scopes=SCOPES)
    return build("drive", "v3", credentials=creds, cache_discovery=False)
def children(api, folder):
    token = None
    while True:
        result = api.files().list(
            q="'%s' in parents and trashed = false" % folder,
            fields="nextPageToken,files(id,name,mimeType,size)",
            pageSize=1000, pageToken=token,
            supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        yield from result.get("files", [])
        token = result.get("nextPageToken")
        if not token: break
def download(api, file_id):
    from googleapiclient.http import MediaIoBaseDownload
    request = api.files().get_media(fileId=file_id, supportsAllDrives=True)
    out = io.BytesIO()
    downloader = MediaIoBaseDownload(out, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return out.getvalue()
def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
def reconcile(inv, manifest, files, failures, drive_file_count):
    """Require exact, unique filename coverage across all three inventories."""
    expected_names = [x["schema_name"] + "." + x["table_name"] + ".csv" for x in inv]
    manifest_names = [x["file"] for x in manifest]
    expected = set(expected_names)
    hashes = set(manifest_names)
    actual = set(files)
    return {
        "inventory_count": len(inv),
        "manifest_count": len(manifest),
        "drive_csv_count": drive_file_count,
        "missing_from_drive": sorted(expected - actual),
        "missing_from_manifest": sorted(expected - hashes),
        "extra_in_manifest": sorted(hashes - expected),
        "sha256_failures": failures,
        "verified": (
            len(inv) == len(expected)
            and len(manifest) == len(hashes)
            and drive_file_count == len(actual)
            and expected == hashes == actual
            and not failures
        ),
    }


def main():
    api = client()
    root = {x["name"]: x for x in children(api, FOLDER)}
    inv = rows(download(api, root["inventory_tables.csv"]["id"]))
    manifest = rows(download(api, root["manifest_sha256.csv"]["id"]))
    hashes = {x["file"]:x for x in manifest}
    data_folder = root["data"]["id"]
    drive_entries = [x for x in children(api, data_folder) if x["name"].lower().endswith(".csv")]
    files = {x["name"]: x for x in drive_entries}
    failures = []
    for name, item in files.items():
        if name not in hashes:
            failures.append({"file":name,"error":"unexpected_file"})
            continue
        blob = download(api, item["id"])
        if hashlib.sha256(blob).hexdigest().lower() != hashes[name]["sha256"].lower():
            failures.append({"file":name,"error":"sha256_mismatch"})
    result = reconcile(inv, manifest, files, failures, len(drive_entries))
    # Private host output only; do not copy this report into a public repository.
    print(json.dumps(result,ensure_ascii=False))
    if not result["verified"]: sys.exit(2)
if __name__=="__main__": main()
