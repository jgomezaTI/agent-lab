import unittest

from backend.app.capabilities.registry import InMemoryCapabilityRegistry
from backend.app.capabilities.service import CapabilityService
from backend.app.policies.context import RequestContext


class CapabilityDiscoveryTests(unittest.TestCase):
    def test_discovery_filters_customer_environment_and_permissions(self):
        registry = InMemoryCapabilityRegistry()
        registry.register({"capability_id": "cap_a", "name": "get_course_grades", "artifact_id": "artifact_a", "customer_id": "a", "product_id": "portal", "environment": "sandbox", "permissions": ["grades:read"], "transport": "mcp", "status": "active"})
        registry.register({"capability_id": "cap_b", "name": "get_course_grades", "artifact_id": "artifact_b", "customer_id": "b", "product_id": "portal", "environment": "sandbox", "permissions": ["grades:read"], "transport": "mcp", "status": "active"})
        context = RequestContext("actor", "a", "portal", "sandbox", frozenset({"grades:read"}))
        result = CapabilityService(registry).discover(context)
        self.assertEqual([item["capability_id"] for item in result], ["cap_a"])

    def test_discovery_is_deny_by_default_for_missing_permission(self):
        registry = InMemoryCapabilityRegistry()
        registry.register({"capability_id": "cap_a", "name": "get_course_grades", "artifact_id": "artifact_a", "customer_id": "a", "product_id": "portal", "environment": "sandbox", "permissions": ["grades:read"], "transport": "mcp", "status": "active"})
        context = RequestContext("actor", "a", "portal", "sandbox")
        self.assertEqual(CapabilityService(registry).discover(context), [])
