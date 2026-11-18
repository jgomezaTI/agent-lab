import unittest

from backend.app.audit.events import InMemoryAuditSink
from backend.app.policies.context import RequestContext
from backend.app.provisioning.proposal_builder import build_tool_proposal
from backend.app.services.audited_workflow import AuditedDiscovery, AuditedProposal


class AuditedWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.audit = InMemoryAuditSink()
        self.context = RequestContext("actor", "customer-a", "portal", "sandbox", trace_id="trace-1", agent_id="support-agent")

    def test_proposal_and_discovery_write_traceable_events(self):
        graph = {"graph_id": "graph_fixture", "nodes": [{"id": "node_grades", "label": "grades.py", "path": "grades.py"}]}
        proposal = AuditedProposal(build_tool_proposal, self.audit).build(self.context, "notas", graph, "commit-1", "portal")
        discovery = AuditedDiscovery(type("Discovery", (), {"discover": lambda _self, _context, _name=None: [{"name": proposal.name}]})(), self.audit)
        discovery.discover(self.context, proposal.name)
        self.assertEqual([event.action for event in self.audit.events], ["proposal.created", "capability.discovery"])
        self.assertEqual(self.audit.events[0].trace_id, "trace-1")
