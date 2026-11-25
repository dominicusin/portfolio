"""SUR-004 audit tool tests."""
import tempfile
import unittest
from pathlib import Path

from automation.rbac_audit import audit_file


class TestRbacAudit(unittest.TestCase):
    def test_route_with_permission_is_guarded(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "Api.hs"
            f.write_text('handle = get "/api/v1/accounts" $ do\n  requirePermission "accounts.read"\n  pure ()\n')
            out = audit_file(f)
            self.assertEqual(len(out), 1)
            self.assertTrue(out[0]["guarded"])

    def test_route_without_permission_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "Api.hs"
            f.write_text('handle = get "/api/v1/accounts" $ do\n  pure []\n')
            out = audit_file(f)
            self.assertFalse(out[0]["guarded"])

    def test_public_annotation_is_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "Api.hs"
            f.write_text('publicPaths = ["/api/v1/login"]\nget "/api/v1/login" $ pure ()\n')
            self.assertTrue(audit_file(f)[0]["guarded"])


if __name__ == "__main__":
    unittest.main()
