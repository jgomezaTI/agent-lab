import unittest

from backend.app.capabilities.registry import InMemoryCapabilityRegistry
from backend.app.mcp.mock_gateway import MockGateway
from backend.app.mcp.mock_runtime import MockRuntime
from backend.app.policies.context import RequestContext
from backend.app.services.synthetic_customer_data import SyntheticCustomerData


class RuntimeInvocationTests(unittest.TestCase):
    def test_authorized_runtime_call_uses_customer_scoped_data(self):
        data = SyntheticCustomerData()
        data.set_grades("customer-a", "course-1", [{"student": "s-1", "grade": 95}])
        runtime = MockRuntime()
        runtime.publish("get_course_grades", {"description": "read-only grades"}, lambda context, arguments: data.get_course_grades(context.customer_id, arguments["course_id"]))
        registry = InMemoryCapabilityRegistry()
        registry.register({"capability_id": "cap_a", "name": "get_course_grades", "artifact_id": "artifact_a", "customer_id": "customer-a", "product_id": "portal", "environment": "sandbox", "permissions": ["grades:read"], "transport": "mcp", "status": "active"})
        context = RequestContext("actor", "customer-a", "portal", "sandbox", frozenset({"grades:read"}))
        result = MockGateway(registry, runtime).call(context, "get_course_grades", {"course_id": "course-1"})
        self.assertEqual(result["customer_id"], "customer-a")
        self.assertEqual(result["grades"][0]["grade"], 95)

    def test_other_customer_cannot_invoke_same_runtime_tool(self):
        runtime = MockRuntime()
        runtime.publish("get_course_grades", {}, lambda context, arguments: {"customer_id": context.customer_id, "course_id": arguments["course_id"]})
        registry = InMemoryCapabilityRegistry()
        registry.register({"capability_id": "cap_a", "name": "get_course_grades", "artifact_id": "artifact_a", "customer_id": "customer-a", "product_id": "portal", "environment": "sandbox", "permissions": ["grades:read"], "transport": "mcp", "status": "active"})
        context = RequestContext("actor", "customer-b", "portal", "sandbox", frozenset({"grades:read"}))
        with self.assertRaises(PermissionError):
            MockGateway(registry, runtime).call(context, "get_course_grades", {"course_id": "course-1"})
