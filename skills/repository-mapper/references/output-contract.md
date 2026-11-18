# Repository mapper output contract

The generated artifact must conform to
`specs/001-dynamic-tool-provisioning/contracts/application-graph.schema.json`.

At minimum it includes:

- `graph_id`
- `repository.commit`
- `scope`
- `nodes[]`
- `relationships[]`
- `generated_at`
- `analyzer.name`
- `analyzer.version`
- `analyzer.configuration_hash`
