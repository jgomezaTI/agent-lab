import unittest

from backend.app.audit.events import AuditEvent, InMemoryAuditSink


class AuditTests(unittest.TestCase):
    def test_sensitive_metadata_is_redacted(self):
        event = AuditEvent("event", "trace", "actor", "customer-a", "portal", "tool.invoke", "tool", "grades", "allowed", {"token": "secret", "nested": {"password": "hidden"}})
        rendered = event.to_dict()
        self.assertEqual(rendered["metadata"]["token"], "[REDACTED]")
        self.assertEqual(rendered["metadata"]["nested"]["password"], "[REDACTED]")

    def test_sink_preserves_traceable_event(self):
        sink = InMemoryAuditSink()
        sink.append(AuditEvent("event", "trace-1", "actor", "customer-a", "portal", "tool.invoke", "tool", "grades", "denied"))
        self.assertEqual(sink.events[0].trace_id, "trace-1")
