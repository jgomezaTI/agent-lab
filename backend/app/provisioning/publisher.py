from __future__ import annotations

from typing import Any

from .models import GeneratedArtifact


class PublicationDenied(PermissionError):
    pass


class MockPublisher:
    def __init__(self) -> None:
        self.deployments: list[dict[str, Any]] = []

    def publish(self, artifact: GeneratedArtifact, customer_id: str, runtime_id: str, transport: str = "mcp") -> dict[str, Any]:
        if not artifact.is_approved():
            raise PublicationDenied("only approved artifacts can be published")
        artifact.lifecycle_state = "published"
        deployment = {
            "deployment_id": f"deployment_{len(self.deployments) + 1}",
            "artifact_id": artifact.artifact_id,
            "customer_id": customer_id,
            "runtime_id": runtime_id,
            "transport": transport,
            "status": "active",
        }
        self.deployments.append(deployment)
        return deployment
