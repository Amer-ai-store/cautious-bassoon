"""Offline, read-only regression tests for export inventory reconciliation."""
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "jawafa_drive_readonly_verify.py"
spec = importlib.util.spec_from_file_location("jawafa_drive_readonly_verify", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.inventory = [
            {"schema_name": "public", "table_name": "a"},
            {"schema_name": "public", "table_name": "b"},
        ]
        self.manifest = [{"file": "public.a.csv"}, {"file": "public.b.csv"}]
        self.files = {"public.a.csv": {}, "public.b.csv": {}}

    def test_matching_unique_lists_are_verified(self):
        result = verifier.reconcile(self.inventory, self.manifest, self.files, [], len(self.files))
        self.assertTrue(result["verified"])

    def test_matching_counts_but_wrong_manifest_are_rejected(self):
        manifest = [{"file": "public.a.csv"}, {"file": "public.c.csv"}]
        files = {"public.a.csv": {}, "public.c.csv": {}}
        result = verifier.reconcile(self.inventory, manifest, files, [], len(files))
        self.assertFalse(result["verified"])
        self.assertEqual(result["missing_from_drive"], ["public.b.csv"])
        self.assertEqual(result["extra_in_manifest"], ["public.c.csv"])

    def test_duplicate_inventory_rows_are_rejected(self):
        inv = [self.inventory[0], self.inventory[0]]
        result = verifier.reconcile(inv, self.manifest, self.files, [], len(self.files))
        self.assertFalse(result["verified"])

    def test_duplicate_manifest_rows_are_rejected(self):
        manifest = [self.manifest[0], self.manifest[0]]
        result = verifier.reconcile(self.inventory, manifest, self.files, [], len(self.files))
        self.assertFalse(result["verified"])

    def test_duplicate_drive_filenames_are_rejected(self):
        result = verifier.reconcile(self.inventory, self.manifest, self.files, [], 3)
        self.assertFalse(result["verified"])

    def test_hash_failure_is_rejected(self):
        failures = [{"file": "public.a.csv", "error": "sha256_mismatch"}]
        result = verifier.reconcile(self.inventory, self.manifest, self.files, failures, len(self.files))
        self.assertFalse(result["verified"])

    def test_missing_file_is_rejected(self):
        files = {"public.a.csv": {}}
        result = verifier.reconcile(self.inventory, self.manifest, files, [], len(files))
        self.assertFalse(result["verified"])
        self.assertEqual(result["missing_from_drive"], ["public.b.csv"])


if __name__ == "__main__":
    unittest.main()
