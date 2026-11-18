import unittest

from backend.app.policies.context import RequestContext
from backend.app.policies.engine import PolicyDenied, PolicyEngine


class PolicyIsolationTests(unittest.TestCase):
    def test_missing_context_is_rejected(self):
        with self.assertRaises(ValueError):
            PolicyEngine().authorize(RequestContext("", "customer-a", "portal", "sandbox"), set())

    def test_missing_permission_is_rejected(self):
        with self.assertRaises(PolicyDenied):
            PolicyEngine().authorize(RequestContext("actor", "customer-a", "portal", "sandbox"), {"grades:read"})
