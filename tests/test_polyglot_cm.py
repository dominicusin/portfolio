"""POLY-001 conflict-detection tests."""
import unittest

from automation.polyglot_cm import Fabric, Manager, ManagerConflict, Resource


class TestPolyglotFabric(unittest.TestCase):
    def setUp(self):
        self.fabric = Fabric()
        self.fabric.register(Manager("ansible", lambda r: "ansible:" + r.id))
        self.fabric.register(Manager("nix", lambda r: "nix:" + r.id))
        self.resource = Resource("host:wdmch", "host")

    def test_owner_can_apply(self):
        self.fabric.declare_owner(self.resource, "ansible")
        self.assertEqual(self.fabric.apply(self.resource, "ansible"), "ansible:host:wdmch")

    def test_foreign_manager_cannot_apply(self):
        self.fabric.declare_owner(self.resource, "ansible")
        with self.assertRaises(ManagerConflict):
            self.fabric.apply(self.resource, "nix")
        self.assertEqual(self.fabric.applied(), [])

    def test_second_owner_is_rejected(self):
        self.fabric.declare_owner(self.resource, "ansible")
        with self.assertRaises(ManagerConflict):
            self.fabric.declare_owner(self.resource, "nix")

    def test_conflict_detection(self):
        claims = [("host:a", "ansible"), ("host:b", "nix"), ("host:a", "nix")]
        self.assertEqual(self.fabric.conflicts(claims), ["host:a: ansible vs nix"])

    def test_unknown_manager_is_rejected(self):
        with self.assertRaises(KeyError):
            self.fabric.declare_owner(self.resource, "puppet")


if __name__ == "__main__":
    unittest.main()
